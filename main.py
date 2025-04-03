import streamlit as st
import requests
from datetime import datetime
import re
import time
from funciones_ganamos import carga_ganamos

# Configuración
API_URL = "https://streamlit-test-eiu8.onrender.com"
TIMEOUT_API = 30
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
        return response.json() if response.status_code == 200 else {"error": True, "detail": response.text}
    except Exception as e:
        return {"error": True, "detail": str(e)}

# Interfaz principal
st.title("💵 Sistema de Carga de Saldo")

# Formulario de pago con diseño mejorado
with st.form("form_pago"):
    st.markdown("### 🛒 Datos del Pago")
    col1, col2 = st.columns(2)
    with col1:
        usuario_id = st.text_input("ID de Usuario*:", value=st.session_state.usuario_id)
    with col2:
        email_comprador = st.text_input("Email del Comprador*:", value=st.session_state.email_comprador)
    
    monto = st.number_input("Monto (ARS)*:", min_value=10.0, value=50.0, step=10.0)
    
    submit_button = st.form_submit_button(
        "Generar Pago", 
        type="primary",
        help="Haz clic para generar el link de pago"
    )
    
    if submit_button:
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
                st.session_state.pago_procesado = False
                
                st.success("¡Pago listo para procesar!")
                st.balloons()
                
                # Tarjeta de resumen con diseño mejorado
                st.markdown(
                    f"""
                    <div style='
                        border: 1px solid #e6e6e6;
                        border-radius: 10px;
                        padding: 20px;
                        margin-top: 20px;
                        background-color: #f9f9f9;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    '>
                        <h3 style='color: #00a650; margin-top: 0;'>Resumen de Pago</h3>
                        <p><strong>👤 Usuario:</strong> {usuario_id}</p>
                        <p><strong>📧 Email:</strong> {email_comprador}</p>
                        <p><strong>💰 Monto:</strong> ${monto:.2f} ARS</p>
                        <p><strong>🆔 ID de Transacción:</strong> {result["id_pago_unico"]}</p>
                        <a href="{result['url_pago']}" target="_blank">
                            <button style='
                                background-color: #00a650;
                                color: white;
                                padding: 12px 24px;
                                border: none;
                                border-radius: 6px;
                                font-size: 16px;
                                margin-top: 15px;
                                cursor: pointer;
                                width: 100%;
                                transition: all 0.3s;
                            '
                            onMouseOver="this.style.backgroundColor='#008f45'"
                            onMouseOut="this.style.backgroundColor='#00a650'"
                            >
                                🔹 Pagar con Mercado Pago
                            </button>
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# Sección de verificación mejorada
if st.session_state.pago_generado:
    st.divider()
    st.markdown("### 🔍 Verificación de Pago")
    
    verify_col1, verify_col2 = st.columns([3, 1])
    with verify_col1:
        st.info(f"ID de Transacción: `{st.session_state.id_pago_unico}`")
    with verify_col2:
        if st.button(
            "🔄 Consultar Estado", 
            key="verificar_pago",
            help="Verifica si el pago fue aprobado"
        ):
            if not st.session_state.id_pago_unico:
                st.warning("Primero genera un pago")
            else:
                with st.spinner("Verificando estado del pago..."):
                    result = call_api("verificar_pago", {
                        "id_pago_unico": st.session_state.id_pago_unico
                    })
                
                st.session_state.ultima_verificacion = datetime.now()
                
                if result.get("error"):
                    st.error(f"""
                    ❌ **Error al verificar el pago**  
                    Detalle: {result.get('detail')}  
                    ID de transacción: `{st.session_state.id_pago_unico}`
                    """)
                elif result.get("payment_id"):
                    st.session_state.payment_id = result["payment_id"]
                    
                    if result.get("status") == "approved":
                        if not st.session_state.pago_procesado:
                            with st.spinner("💸 Procesando carga en Ganamos..."):
                                success, balance = carga_ganamos(
                                    st.session_state.usuario_id,
                                    result.get('monto', 0)
                                )
                                
                                if success:
                                    st.session_state.pago_procesado = True
                                    st.success(f"""
                                    ✅ **Carga Exitosa**  
                                    - **Monto cargado:** ${result.get('monto', 0):.2f}  
                                    - **Balance actual:** ${balance:.2f}  
                                    - **Hora:** {datetime.now().strftime('%H:%M:%S')}
                                    """)
                                    st.balloons()
                                else:
                                    st.error(f"""
                                    ❌ **Error en la carga**  
                                    - **Monto a cargar:** ${result.get('monto', 0):.2f}  
                                    - **Balance actual:** ${balance:.2f}  
                                    - **Hora:** {datetime.now().strftime('%H:%M:%S')}
                                    """)
                        else:
                            st.warning("⚠️ Esta transacción ya fue procesada anteriormente")
                        
                        st.markdown(
                            f"""
                            <div style='
                                border-left: 4px solid #00a650;
                                padding: 10px 15px;
                                background-color: #f0fff4;
                                margin: 15px 0;
                                border-radius: 4px;
                            '>
                                <p style='margin: 0;'><strong>✅ Pago Confirmado</strong></p>
                                <p style='margin: 5px 0;'>ID MercadoPago: <code>{result['payment_id']}</code></p>
                                <p style='margin: 5px 0;'>Estado: {result.get('status', 'approved').capitalize()}</p>
                                <p style='margin: 5px 0;'>Fecha: {result.get('fecha_actualizacion', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.warning(f"""
                        ⏳ **Pago Pendiente**  
                        
                        *Si ya realizaste el pago:*  
                        1. Espera 5 minutos (las notificaciones pueden tardar)  
                        2. Vuelve a verificar  
                        3. Si persiste, contacta soporte con el ID de transacción  
                        """)

    if st.session_state.ultima_verificacion:
        st.caption(f"Última verificación: {st.session_state.ultima_verificacion.strftime('%H:%M:%S')}")

# Panel de información mejorado
with st.sidebar:
    st.markdown("""
    <div style='
        padding: 15px;
        background-color: #f0f7ff;
        border-radius: 10px;
        margin-bottom: 20px;
    '>
        <h3 style='color: #0056b3; margin-top: 0;'>📌 Instrucciones</h3>
        <ol style='padding-left: 20px;'>
            <li>Ingresa tu <strong>ID de usuario</strong></li>
            <li>Coloca un <strong>email válido</strong></li>
            <li>Especifica el <strong>monto</strong> a cargar</li>
            <li>Haz clic en <strong>Generar Pago</strong></li>
            <li>Completa el pago en Mercado Pago</li>
            <li>Verifica el estado aquí</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='
        padding: 15px;
        background-color: #fff4f4;
        border-radius: 10px;
    '>
        <h3 style='color: #d63638; margin-top: 0;'>📞 Soporte</h3>
        <p><strong>Email:</strong> soporte@ejemplo.com</p>
        <p><strong>Teléfono:</strong> +54 11 1234-5678</p>
        <p><strong>Horario:</strong> Lunes a Viernes 9-18hs</p>
    </div>
    """, unsafe_allow_html=True)

    if st.checkbox("Mostrar detalles técnicos", key="debug_checkbox"):
        st.json({
            "id_pago": st.session_state.id_pago_unico,
            "usuario": st.session_state.usuario_id,
            "procesado": st.session_state.pago_procesado,
            "ultima_verificacion": st.session_state.ultima_verificacion
        })
