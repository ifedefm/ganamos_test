import streamlit as st
import requests
from datetime import datetime
import re
import time
from funciones_ganamos import *


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

col1, col2, col3 = st.columns([1, 2, 1])  # La columna del medio es más grande

with col2:  # Solo usamos la columna central
    tab1, tab2, tab3 = st.tabs(["Crear Usuario", "Cargar Saldo", "Retirar Saldo"])


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


with tab1:
    st.title("👤 Crear Usuario")

    with st.form("form_usuario"):
        col1, col2,col3 = st.columns(3)
        with col1:
            usuario_id = st.text_input("ID de Usuario*:", value=st.session_state.usuario_id)
            contraseña = st.text_input("Contraseña*:", type="password")
        with col2:
            email_nuevo_usuario = st.text_input("Email del Nuevo Usuario*:", value="")
            repetir_contraseña = st.text_input("Repetir Contraseña*:", type="password")
            if repetir_contraseña != contraseña:
                st.error("Las contraseñas no coinciden")
        with col3:
            telefono = st.text_input("Teléfono*:", value="", key=int,help='''Ingrese el número de teléfono sin el 0 y sin el 15.
                                                                                Ejemplo: 2611234567''')        

        if st.form_submit_button("Crear Usuario", type="primary"):
            if not all([usuario_id, contraseña, email_nuevo_usuario, repetir_contraseña]):
                st.error("Completa todos los campos obligatorios (*)")
            elif not validar_email(email_nuevo_usuario):
                st.error("El email no es válido")
            elif contraseña != repetir_contraseña:
                st.error("Las contraseñas no coinciden")
            else:
                with st.spinner("Creando usuario..."):
                    result = nuevo_jugador(nueva_contrasenia=contraseña, nuevo_usuario=usuario_id)
                    nuevo_cliente = guardar_usuario(usuario=usuario_id, contraseña=contraseña, email=email_nuevo_usuario, telefono=telefono)
                    st.write("Resultado:", result)
                if nuevo_cliente:  
                    st.session_state.usuario_id = usuario_id 
                    st.success("¡Usuario creado exitosamente!")
                else:
                    st.error("Error al crear el usuario. Intenta nuevamente.")

with tab2:
        st.title("💵 Carga de Saldo")

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
                            "usuario_id": usuario_id.lower(),
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
                        ## IDENTAD
                        if result.get("status") == "approved":
                            st.success(f"""
                            ✅ **Pago Aprobado**  
                            - Monto: ${result.get('monto', 0):.2f}  
                            - Hora: {datetime.now().strftime('%H:%M:%S')}
                            """)
                            
                            st.markdown(f"""
                            **Detalles del pago:**  
                            - ID MercadoPago: {result['payment_id']}  
                            - Estado: {result.get('status', 'approved').capitalize()}  
                            - Fecha: {result.get('fecha_actualizacion', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}  
                            """)
                            
                            # Nuevo código para mostrar estado de Ganamos
                            if result.get("ganamos_success"):
                                st.success(f"✅ Saldo cargado en Ganamos correctamente. Balance actual: ${result.get('ganamos_balance', 0):.2f}")
                            elif result.get("procesado_ganamos") and not result.get("ganamos_success"):
                                st.error("⚠️ El pago fue aprobado pero hubo un error al cargar el saldo en Ganamos. Contacta a soporte.")
                            else:
                                st.info("⏳ El pago fue aprobado y se está procesando la carga en Ganamos...")
                        else:
                            st.warning(f"""
                            ⏳ Pago aún no confirmado  
                            Estado actual: {result.get('status', 'pending')}  
                            Si ya pagaste, espera unos minutos y vuelve a verificar.
                            """)
                    else:
                        st.warning("No se encontró información de pago. Intenta nuevamente más tarde.")

# Información de contacto
st.divider()
st.markdown("""
**Soporte:**  
Email: soporte@ejemplo.com  
Tel: 11 1234-5678
""")
