import streamlit as st
import requests
from datetime import datetime
import re
import time
from funciones_ganamos import carga_ganamos
import logging

# Configuración
API_URL = "https://streamlit-test-eiu8.onrender.com"
TIMEOUT_API = 30
st.set_page_config(
    page_title="Sistema de Pagos Reales",
    page_icon="💳",
    layout="wide"
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='pagos_ganamos.log'
)

# Estado de la sesión
session_defaults = {
    'id_pago_unico': None,
    'preference_id': None,
    'payment_id': None,
    'usuario_id': "",
    'email_comprador': "",
    'ultima_verificacion': None,
    'pago_generado': False,
    'pago_procesado': False,
    'intentos_autenticacion': 0
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Funciones auxiliares
def validar_email(email):
    """Valida el formato de un email"""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def call_api(endpoint, payload):
    """Realiza llamadas a la API con manejo de errores"""
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
            error_msg = f"Error {response.status_code}: {response.text[:200]}"
            logging.error(f"API Error - {endpoint}: {error_msg}")
            return {"error": True, "detail": error_msg}
            
    except requests.exceptions.Timeout:
        logging.error("Timeout al conectar con la API")
        return {"error": True, "detail": "El servidor tardó demasiado en responder"}
    except requests.exceptions.RequestException as e:
        logging.error(f"Error de conexión: {str(e)}")
        return {"error": True, "detail": f"Error de conexión: {str(e)}"}
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        return {"error": True, "detail": f"Error inesperado: {str(e)}"}

def ejecutar_carga_ganamos(alias: str, monto: float) -> bool:
    """Ejecuta y monitorea la carga en Ganamos"""
    try:
        with st.spinner("Procesando carga en Ganamos..."):
            logging.info(f"Iniciando carga para {alias}, monto: {monto}")
            exito, balance = carga_ganamos(alias, monto)
            
            if exito:
                st.session_state.pago_procesado = True
                st.session_state.intentos_autenticacion = 0
                msg = f"Carga exitosa! Usuario: {alias}, Monto: ${monto:.2f}, Balance: ${balance:.2f}"
                logging.info(msg)
                st.success(f"✅ {msg}")
                return True
            else:
                st.session_state.intentos_autenticacion += 1
                error_msg = f"Fallo en carga. Usuario: {alias}, Monto: ${monto:.2f}, Balance: ${balance:.2f}"
                logging.error(error_msg)
                
                if st.session_state.intentos_autenticacion >= 3:
                    st.error("🔐 Problema persistente de autenticación. Contacte al soporte.")
                else:
                    st.error(f"❌ {error_msg}")
                
                mostrar_logs()
                return False
                
    except Exception as e:
        logging.error(f"Error crítico: {str(e)}", exc_info=True)
        st.error(f"🔥 Error crítico: {str(e)}")
        mostrar_logs()
        return False

def mostrar_logs():
    """Muestra los últimos logs en la interfaz"""
    try:
        with open('pagos_ganamos.log', 'r') as f:
            logs = f.read().splitlines()[-10:]  # Últimas 10 líneas
        with st.expander("📄 Registros de error (últimos 10)"):
            st.code("\n".join(logs))
    except FileNotFoundError:
        st.warning("No se encontró el archivo de registros")

def formulario_pago():
    """Componente del formulario de pago"""
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
                procesar_pago(usuario_id, email_comprador, monto)

def procesar_pago(usuario_id: str, email_comprador: str, monto: float):
    """Procesa la generación del pago"""
    with st.spinner("Generando link de pago..."):
        result = call_api("crear_pago", {
            "usuario_id": usuario_id,
            "monto": float(monto),
            "email": email_comprador
        })
    
    if result.get("error"):
        st.error(f"Error al generar pago: {result.get('detail')}")
    else:
        actualizar_estado_pago(result, usuario_id, email_comprador)
        mostrar_resumen_pago(result, usuario_id, email_comprador, monto)

def actualizar_estado_pago(result: dict, usuario_id: str, email_comprador: str):
    """Actualiza el estado de la sesión con los datos del pago"""
    st.session_state.id_pago_unico = result["id_pago_unico"]
    st.session_state.preference_id = result["preference_id"]
    st.session_state.usuario_id = usuario_id
    st.session_state.email_comprador = email_comprador
    st.session_state.pago_generado = True
    st.session_state.ultima_verificacion = None
    st.session_state.pago_procesado = False
    st.session_state.intentos_autenticacion = 0

def mostrar_resumen_pago(result: dict, usuario_id: str, email_comprador: str, monto: float):
    """Muestra el resumen del pago generado"""
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

def verificar_pago():
    """Componente de verificación de pago"""
    st.divider()
    st.subheader("Verificación de Pago")
    
    if st.button("Consultar Estado", key="verificar_pago"):
        if not st.session_state.id_pago_unico:
            st.warning("Primero genera un pago")
        else:
            verificar_estado_pago()

def verificar_estado_pago():
    """Verifica el estado del pago con la API"""
    with st.spinner("Verificando estado del pago..."):
        result = None
        for intento in range(3):
            result = call_api("verificar_pago", {
                "id_pago_unico": st.session_state.id_pago_unico
            })
            
            if not result.get("error"):
                break
            time.sleep(2)
        
        st.session_state.ultima_verificacion = datetime.now()
        procesar_respuesta_verificacion(result)

def procesar_respuesta_verificacion(result: dict):
    """Procesa la respuesta de verificación de pago"""
    if result.get("error"):
        st.error(f"""
        ❌ **Error al verificar el pago**  
        Detalle: {result.get('detail')}  
        ID de transacción: `{st.session_state.id_pago_unico}`
        """)
    elif result.get("payment_id"):
        manejar_pago_exitoso(result)
    else:
        mostrar_pago_pendiente()

def manejar_pago_exitoso(result: dict):
    """Maneja la lógica cuando el pago es exitoso"""
    st.session_state.payment_id = result["payment_id"]
    
    if result.get("status") == "approved" and not st.session_state.pago_procesado:
        procesar_carga_ganamos(result)
    
    mostrar_resumen_pago_exitoso(result)

def procesar_carga_ganamos(result: dict):
    """Procesa la carga en Ganamos para pagos aprobados"""
    with st.spinner("Procesando pago en el sistema Ganamos..."):
        if ejecutar_carga_ganamos(
            alias=st.session_state.usuario_id,
            monto=result.get('monto', 0)
        ):
            st.balloons()
        else:
            st.session_state.pago_procesado = False

def mostrar_resumen_pago_exitoso(result: dict):
    """Muestra el resumen del pago exitoso"""
    st.success(f"""
    ✅ **Pago Confirmado en MercadoPago**  
    - **ID de Transacción:** {st.session_state.id_pago_unico}  
    - **ID de Pago MercadoPago:** {result['payment_id']}  
    - **Monto:** ${result.get('monto', 0):.2f} ARS  
    - **Estado:** {result.get('status', 'approved').capitalize()}  
    - **Fecha:** {result.get('fecha_actualizacion', 'N/A')}  
    """)

def mostrar_pago_pendiente():
    """Muestra estado de pago pendiente"""
    st.warning(f"""
    ⏳ **Pago Pendiente de Confirmación**  
    
    **ID de Transacción:** `{st.session_state.id_pago_unico}`  
    
    *Si ya realizaste el pago:*  
    1. Espera 5 minutos (las notificaciones pueden tardar)  
    2. Vuelve a verificar  
    3. Si persiste, contacta soporte con el ID de transacción  
    """)

def panel_informacion():
    """Panel lateral de información"""
    st.sidebar.markdown("""
    ### 📌 Instrucciones
    1. Ingresa tu **ID de usuario** y **email real**
    2. Genera el pago y completa el proceso en Mercado Pago
    3. Después de pagar, verifica el estado aquí

    ### 📞 Soporte
    soporte@ejemplo.com  
    Tel: +54 11 1234-5678
    """)
    
    if st.sidebar.checkbox("Mostrar estado de depuración"):
        st.sidebar.json({
            "id_pago_unico": st.session_state.id_pago_unico,
            "usuario": st.session_state.usuario_id,
            "pago_procesado": st.session_state.pago_procesado,
            "intentos_auth": st.session_state.intentos_autenticacion
        })

# Interfaz principal
st.title("💵 Sistema de Carga de Saldo")

# Componentes principales
formulario_pago()

if st.session_state.pago_generado:
    verificar_pago()
    if st.session_state.ultima_verificacion:
        st.caption(f"Última verificación: {st.session_state.ultima_verificacion.strftime('%H:%M:%S')}")

panel_informacion()
