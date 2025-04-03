from funciones_ganamos import carga_ganamos, login_ganamos  # Asegúrate de importar ambas funciones
import streamlit as st
import requests
from datetime import datetime
import re
import time

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
if 'pago_generado' not in st.session_state:
    st.session_state.pago_generado = False
if 'pago_procesado' not in st.session_state:
    st.session_state.pago_procesado = False
if 'intentos_verificacion' not in st.session_state:  # Nuevo estado para reintentos
    st.session_state.intentos_verificacion = 0

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

# Formulario de pago
with st.form("form_pago"):
    col1, col2 = st.columns(2)
    with col1:
        usuario_id = st.text_input("ID de Usuario*:", value=st.session_state.usuario_id)
    with col2:
        email_comprador = st.text_input("Email del Comprador*:")
    
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
                st.session_state.pago_generado = True
                st.session_state.pago_procesado = False
                st.session_state.intentos_verificacion = 0  # Resetear intentos
                
                st.success("¡Pago generado correctamente!")
                st.markdown(
                    f"""
                    <div style='margin-top:20px;'>
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
                                Ir a Pagar con Mercado Pago
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
                result = call_api("verificar_pago", {
                    "id_pago_unico": st.session_state.id_pago_unico
                })
            
            if result.get("error"):
                st.error(f"Error al verificar: {result.get('detail')}")
            elif result.get("payment_id"):
                st.session_state.payment_id = result["payment_id"]
                st.session_state.intentos_verificacion += 1
                
                if result.get("status") == "approved":
                    if not st.session_state.pago_procesado:
                        # Añadir barra de progreso para visualizar el tiempo de espera
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i in range(6):  # 6 segundos aproximados
                            time.sleep(1)
                            progress_bar.progress((i + 1) / 6)
                            status_text.text(f"Procesando carga en Ganamos... ({i+1}/6 segundos)")
                        
                        # Ejecutar la carga
                        success, balance = carga_ganamos(
                            st.session_state.usuario_id,
                            result.get('monto', 0)
                        )
                        
                        # Limpiar elementos de progreso
                        progress_bar.empty()
                        status_text.empty()
                        
                        if success:
                            st.session_state.pago_procesado = True
                            st.success(f"""
                            ✅ **Carga Exitosa**  
                            - Monto: ${result.get('monto', 0):.2f}  
                            - Balance actual: ${balance:.2f}  
                            - Hora: {datetime.now().strftime('%H:%M:%S')}
                            """)
                        else:
                            st.error(f"""
                            ❌ **Error en la carga**  
                            - Monto: ${result.get('monto', 0):.2f}  
                            - Balance: ${balance:.2f}  
                            - Hora: {datetime.now().strftime('%H:%M:%S')}
                            """)
                    else:
                        st.warning("⚠️ Esta transacción ya fue procesada")
                    
                    st.markdown(f"""
                    **Detalles del pago:**  
                    - ID MercadoPago: {result['payment_id']}  
                    - Estado: {result.get('status', 'approved').capitalize()}  
                    - Fecha: {result.get('fecha_actualizacion', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}  
                    - Intentos de verificación: {st.session_state.intentos_verificacion}
                    """)
                else:
                    st.warning(f"""
                    ⏳ Pago aún no confirmado (Intento {st.session_state.intentos_verificacion})  
                    Si ya pagaste, espera unos minutos y vuelve a verificar.
                    """)
            else:
                st.warning("No se encontró información de pago. Intenta nuevamente más tarde.")

# --- MODO PRUEBAS LOCAL (ELIMINAR EN PRODUCCIÓN) ---
if st.sidebar.checkbox("🔧 Modo Pruebas Local"):
    st.session_state.pago_generado = True
    st.session_state.id_pago_unico = "simulado_123"
    st.session_state.usuario_id = st.sidebar.text_input("Usuario TEST", value="test_user")
    monto_simulado = st.sidebar.number_input("Monto TEST", value=50.0)
    
    if st.sidebar.button("Simular Pago Aprobado"):
        # Simular respuesta de API
        result = {
            "payment_id": "simulado_"+str(int(time.time())),
            "status": "approved",
            "monto": monto_simulado,
            "fecha_actualizacion": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with st.spinner("Simulando carga..."):
            success, balance = carga_ganamos(st.session_state.usuario_id, monto_simulado)
            
            if success:
                st.success(f"✅ Simulación exitosa! Balance: ${balance:.2f}")
            else:
                st.error(f"❌ Simulación fallida. Balance: ${balance:.2f}")
# ---------------------------------------------------

# Información de contacto
st.divider()
st.markdown("""
**Soporte:**  
Email: soporte@ejemplo.com  
Tel: 11 1234-5678
""")

