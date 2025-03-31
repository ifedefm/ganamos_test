import streamlit as st
import requests
from datetime import datetime
import re

# Configuración
API_URL = "https://render-notify-mp.onrender.com"  # Cambiar por tu URL real
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

# Funciones auxiliares
def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def call_api(endpoint, payload):
    try:
        response = requests.post(
            f"{API_URL}/{endpoint}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        return response.json() if response.status_code == 200 else {"error": True, "detail": response.text}
    except Exception as e:
        return {"error": True, "detail": str(e)}

# Interfaz
st.title("💵 Sistema de Carga de Saldo")

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
            result = call_api("crear_pago/", {
                "usuario_id": usuario_id,
                "monto": float(monto),
                "email": email_comprador
            })
            st.write(result)
            
            if result.get("error"):
                st.error(f"Error: {result.get('detail', 'Contacta al soporte')}")
            else:
                st.session_state.preference_id = result["preference_id"]
                st.session_state.usuario_id = usuario_id
                st.session_state.email_comprador = email_comprador
                
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

# Sección de verificación
st.divider()
st.subheader("Verificación de Pago")

if st.button("Consultar Estado", key="verificar_pago"):
    if not st.session_state.preference_id:
        st.warning("Primero genera un pago")
    else:
        with st.spinner("Verificando estado..."):
            result = call_api("verificar_pago", {
                "preference_id": st.session_state.preference_id,
                "usuario_id": st.session_state.usuario_id
            })
            
            st.session_state.ultima_verificacion = datetime.now()
            
            if result.get("error"):
                st.error(f"Error: {result.get('detail')}")
            else:
                if result.get("status") == "approved":
                    st.session_state.payment_id = result.get("payment_id")
                    st.balloons()
                    st.success(f"""
                    ✅ **Pago Aprobado**  
                    - **ID Transacción:** {result.get('payment_id')}  
                    - **Monto:** ${result.get('monto', 0):.2f} ARS  
                    - **Fecha:** {result.get('fecha', 'N/A')}  
                    """)
                else:
                    st.warning(f"""
                    ⚠️ **Estado Actual:** {result.get('status', 'pending')}  
                    *Los pagos pueden tardar hasta 5 minutos en procesarse*
                    """)

if st.session_state.ultima_verificacion:
    st.caption(f"Última verificación: {st.session_state.ultima_verificacion.strftime('%H:%M:%S')}")

# Panel de información
st.sidebar.markdown("""
### 📌 Instrucciones
1. Ingresa tu **ID de usuario** y **email real**
2. Genera el pago y completa el proceso en Mercado Pago
3. Verifica el estado cuando finalices

### 📞 Soporte
123@twinky.com  
Tel: +54 11 1234-5678
""")