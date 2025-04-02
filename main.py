import streamlit as st
import requests
from datetime import datetime
import re
import time
from funciones_ganamos import carga_ganamos  # Importamos la función del archivo local

# Configuración
API_URL = "https://streamlit-test-eiu8.onrender.com"  # Cambia por tu URL real
TIMEOUT_API = 30  # Timeout aumentado para Render
st.set_page_config(
    page_title="Sistema de Pagos Reales",
    page_icon="💳",
    layout="wide"
)

# Estado de la sesión
if 'id_pago_unico' not in st.session_state:
    st.session_state.id_pago_unico = None
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
if 'pago_procesado' not in st.session_state:
    st.session_state.pago_procesado = False

# Funciones auxiliares
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
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": True,
                "detail": f"Error {response.status_code}: {response.text[:200]}"
            }
    except requests.exceptions.Timeout:
        return {"error": True, "detail": "El servidor tardó demasiado en responder"}
    except requests.exceptions.RequestException as e:
        return {"error": True, "detail": f"Error de conexión: {str(e)}"}
    except Exception as e:
        return {"error": True, "detail": f"Error inesperado: {str(e)}"}

def ejecutar_carga_ganamos(alias: str, monto: float):
    """Ejecuta la función de carga_ganamos con manejo robusto de errores"""
    max_intentos = 3
    intento = 0
    
    while intento < max_intentos:
        try:
            resultado = carga_ganamos(alias=alias, monto=monto)
            if resultado and resultado.get('success'):
                st.session_state.pago_procesado = True
                st.success("✅ Carga en Ganamos procesada correctamente")
                return resultado
            elif resultado:
                st.warning(f"Intento {intento+1}: La carga no fue exitosa. Motivo: {resultado.get('message', 'Desconocido')}")
            else:
                st.warning(f"Intento {intento+1}: La carga no fue exitosa (respuesta vacía)")
        except Exception as e:
            error_msg = str(e)
            if "session_id" in error_msg:
                st.warning(f"Intento {intento+1}: Error de autenticación. Reintentando...")
            else:
                st.error(f"Intento {intento+1}: Error inesperado - {error_msg}")
        
        intento += 1
        if intento < max_intentos:
            time.sleep(5)  # Espera 5 segundos entre intentos
    
    st.error("""
    ❌ No se pudo completar la carga después de 3 intentos. 
    
    **Por favor:**
    1. Verifica que las credenciales en funciones_ganamos.py sean correctas
    2. Revisa la conexión a internet
    3. Contacta al soporte técnico con el ID de transacción
    """)
    return None

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
                st.session_state.id_pago_unico = result["id_pago_unico"]
                st.session_state.preference_id = result["preference_id"]
                st.session_state.usuario_id = usuario_id
                st.session_state.email_comprador = email_comprador
                st.session_state.pago_generado = True
                st.session_state.ultima_verificacion = None
                st.session_state.pago_procesado = False  # Resetear estado de procesamiento
                
                st.success("¡Pago listo para procesar!")
                st.markdown(
                    f"""
                    <div style='border:1px solid #e6e6e6; padding:15px; border-radius:8px; margin-top:20px;'>
                        <h3 style='color:#00a650;'>🛒 Orden de Pago</h3>
                        <p><strong>Usuario:</strong> {usuario_id}</p>
                        <p><strong>Email:</strong> {email_comprador}</p>
                        <p><strong>Monto:</strong> ${monto:.2f} ARS</p>
                        <p><strong>ID de Transacción:</strong> {result["id_pago_unico"]}</p>
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

# Sección de verificación
if st.session_state.pago_generado:
    st.divider()
    st.subheader("Verificación de Pago")
    
    if st.button("Consultar Estado", key="verificar_pago"):
        if not st.session_state.id_pago_unico:
            st.warning("Primero genera un pago")
        else:
            with st.spinner("Verificando estado del pago..."):
                # Intentar hasta 3 veces con delay
                result = None
                for intento in range(3):
                    result = call_api("verificar_pago", {
                        "id_pago_unico": st.session_state.id_pago_unico
                    })
                    
                    if not result.get("error"):
                        break
                    time.sleep(2)  # Espera 2 segundos entre intentos
                
                st.session_state.ultima_verificacion = datetime.now()
                
                if result.get("error"):
                    st.error(f"""
                    ❌ **Error al verificar el pago**  
                    Detalle: {result.get('detail')}  
                    ID de transacción: `{st.session_state.id_pago_unico}`
                    """)
                elif result.get("payment_id"):
                    st.session_state.payment_id = result["payment_id"]
                    
                    # Verificar si el pago está aprobado y no se ha procesado aún
                    if result.get("status") == "approved" and not st.session_state.pago_procesado:
                        with st.spinner("Procesando pago en el sistema Ganamos..."):
                            # Ejecutar la función carga_ganamos con reintentos
                            ejecucion_exitosa = ejecutar_carga_ganamos(
                                alias=st.session_state.usuario_id,
                                monto=result.get('monto', 0))
                            
                            # Mostrar resultado solo si no hubo éxito
                            if not ejecucion_exitosa:
                                st.warning("""
                                ⚠️ **Pago verificado pero hubo un error al procesar la carga**
                                
                                El pago en MercadoPago fue exitoso, pero no se pudo completar 
                                la carga en el sistema Ganamos. Por favor:
                                
                                1. Espera unos minutos y verifica nuevamente
                                2. Si persiste, contacta al soporte con el ID de transacción
                                """)
                                # No marcamos como procesado para permitir reintentos
                                st.session_state.pago_procesado = False
                    
                    st.balloons()
                    st.success(f"""
                    ✅ **Pago Confirmado**  
                    - **ID de Transacción:** {st.session_state.id_pago_unico}  
                    - **ID de Pago MercadoPago:** {result['payment_id']}  
                    - **Monto:** ${result.get('monto', 0):.2f} ARS  
                    - **Estado:** {result.get('status', 'approved').capitalize()}  
                    - **Fecha:** {result.get('fecha_actualizacion', 'N/A')}  
                    """)
                else:
                    st.warning(f"""
                    ⏳ **Pago Pendiente de Confirmación**  
                    
                    **ID de Transacción:** `{st.session_state.id_pago_unico}`  
                    
                    *Si ya realizaste el pago:*  
                    1. Espera 5 minutos (las notificaciones pueden tardar)  
                    2. Vuelve a verificar  
                    3. Si persiste, contacta soporte con el ID de transacción  
                    """)

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

# Debug: Mostrar estado de la sesión
if st.sidebar.checkbox("Mostrar estado de depuración"):
    st.sidebar.write("Estado actual de la sesión:", {
        "id_pago_unico": st.session_state.id_pago_unico,
        "preference_id": st.session_state.preference_id,
        "payment_id": st.session_state.payment_id,
        "usuario_id": st.session_state.usuario_id,
        "ultima_verificacion": st.session_state.ultima_verificacion,
        "pago_generado": st.session_state.pago_generado,
        "pago_procesado": st.session_state.pago_procesado
    })
