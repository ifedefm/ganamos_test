import streamlit as st
import requests
from datetime import datetime
import re
import time

# Configuración
API_URL = "https://streamlit-test-eiu8.onrender.com"  # Asegúrate que esta URL sea correcta
TIMEOUT_API = 30  # Aumentamos el timeout a 30 segundos para Render
st.set_page_config(
    page_title="Sistema de Pagos Reales",
    page_icon="💳",
    layout="wide"
)

# Estado de la sesión
if 'preference_id' not in st.session_state:
    st.session_state.preference_id = None
if 'payment_id' not in st.session_state:
    st.session_state.payment_id = None
if 'usuario_id' not in st.session_state:
    st.session_state.usuario_id = ""
if 'email_comprador' not in st.session_state:
    st.session_state.email_comprador = ""
if 'ultima_verificacion' not in st.session_state:
    st.session_state.ultima_verificacion = None
if 'pago_generado' not in st.session_state:
    st.session_state.pago_generado = False

# Funciones auxiliares mejoradas
def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def call_api(endpoint, payload):
    try:
        response = requests.post(
            f"{API_URL}/{endpoint}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT_API
        )
        
        # Debug: Imprimir respuesta de la API
        print(f"Respuesta de la API ({endpoint}):", response.status_code, response.text)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": True,
                "detail": f"Error {response.status_code}: {response.text[:200]}"  # Limitar longitud del mensaje
            }
    except requests.exceptions.Timeout:
        return {"error": True, "detail": "El servidor tardó demasiado en responder"}
    except requests.exceptions.RequestException as e:
        return {"error": True, "detail": f"Error de conexión: {str(e)}"}
    except Exception as e:
        return {"error": True, "detail": f"Error inesperado: {str(e)}"}

# Interfaz principal
st.title("💵 Sistema de Carga de Saldo")

# Formulario de pago
with st.form("form_pago"):
    col1, col2 = st.columns(2)
    with col1:
        usuario_id = st.text_input("ID de Usuario*:", value=st.session_state.usuario_id)
    with col2:
        email_comprador = st.text_input("Email del Comprador*:", value=st.session_state.email_comprador)
    
    monto = st.number_input("Monto (ARS)*:", min_value=10.0, value=50.0, step=10.0)
    
    if st.form_submit_button("Generar Pago", type="primary"):
        if not all([usuario_id, email_comprador, monto > 0]):
            st.error("Completa todos los campos obligatorios (*)")
        elif not validar_email(email_comprador):
            st.error("Ingresa un email válido")
        else:
            with st.spinner("Generando link de pago..."):
                result = call_api("crear_pago", {
                    "usuario_id": usuario_id,
                    "monto": float(monto),
                    "email": email_comprador
                })
            
            if result.get("error"):
                st.error(f"Error al generar pago: {result.get('detail')}")
            else:
                st.session_state.preference_id = result["preference_id"]
                st.session_state.usuario_id = usuario_id
                st.session_state.email_comprador = email_comprador
                st.session_state.pago_generado = True
                st.session_state.ultima_verificacion = None
                
                st.success("¡Pago listo para procesar!")
                st.markdown(
                    f"""
                    <div style='border:1px solid #e6e6e6; padding:15px; border-radius:8px; margin-top:20px;'>
                        <h3 style='color:#00a650;'>🛒 Orden de Pago</h3>
                        <p><strong>Usuario:</strong> {usuario_id}</p>
                        <p><strong>Email:</strong> {email_comprador}</p>
                        <p><strong>Monto:</strong> ${monto:.2f} ARS</p>
                        <a href="{result['url_pago']}" target="_blank">
                            <button style='
                                background-color: #00a650;
                                color: white;
                                padding: 12px 24px;
                                border: none;
                                border-radius: 6px;
                                font-size: 16px;
                                margin-top: 10px;
                                cursor: pointer;'>
                                Pagar con Mercado Pago
                            </button>
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# Sección de verificación (solo visible si se generó un pago)
if st.session_state.pago_generado:
    st.divider()
    st.subheader("Verificación de Pago")
    
    if st.button("Consultar Estado"):
    if not st.session_state.preference_id:
        st.warning("Primero genera un pago")
    else:
        with st.spinner("Verificando estado del pago..."):
            result = call_api("verificar_pago", {
                "preference_id": st.session_state.preference_id,
                "usuario_id": st.session_state.usuario_id
            })
            
            st.session_state.ultima_verificacion = datetime.now()
            
            if result.get("error"):
                st.error(f"Error al verificar: {result.get('detail')}")
            elif result.get("payment_id"):  # Verificación explícita de payment_id
                st.session_state.payment_id = result["payment_id"]
                st.balloons()
                st.success(f"""
                ✅ **Pago Confirmado**  
                - ID Transacción: {result['payment_id']}  
                - Monto: ${result.get('monto', 0):.2f}  
                - Fecha: {result.get('fecha', 'N/A')}
                """)
            else:
                st.warning(f"""
                ⏳ **Pago no registrado completamente**  
                
                ID de preferencia: `{st.session_state.preference_id}`  
                
                Posibles causas:  
                1. El pago no se ha completado  
                2. La notificación no ha sido procesada  
                3. Problema de sincronización  
                
                **Solución:**  
                1. Espera 5 minutos  
                2. Vuelve a verificar  
                3. Si persiste, contacta soporte  
                """)

    # Mostrar última verificación si existe
    if st.session_state.ultima_verificacion:
        st.caption(f"Última verificación: {st.session_state.ultima_verificacion.strftime('%H:%M:%S')}")

# Panel de información
st.sidebar.markdown("""
### 📌 Instrucciones
1. Ingresa tu **ID de usuario** y **email real**
2. Genera el pago y completa el proceso en Mercado Pago
3. Después de pagar, verifica el estado aquí

### 📞 Soporte
soporte@ejemplo.com  
Tel: +54 11 1234-5678
""")

# Debug: Mostrar estado de la sesión (opcional)
if st.sidebar.checkbox("Mostrar estado de depuración"):
    st.sidebar.write("Estado actual:", st.session_state)
