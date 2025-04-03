import streamlit as st
import requests
from datetime import datetime
import re
from funciones_ganamos import carga_ganamos

# Configuración básica
API_URL = "https://streamlit-test-eiu8.onrender.com"
st.set_page_config(page_title="Sistema de Pagos", page_icon="💳", layout="wide")

# Estado mínimo de la sesión
if 'id_pago' not in st.session_state:
    st.session_state.id_pago = None
    st.session_state.usuario_id = ""
    st.session_state.pago_procesado = False

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def call_api(endpoint, payload):
    try:
        response = requests.post(f"{API_URL}/{endpoint}", json=payload, timeout=30)
        return response.json() if response.status_code == 200 else {"error": True, "detail": response.text}
    except Exception as e:
        return {"error": True, "detail": str(e)}

# Interfaz principal
st.title("💵 Carga de Saldo en Ganamos")

# Formulario de pago
with st.form("form_pago"):
    usuario_id = st.text_input("ID de Usuario en Ganamos*", value=st.session_state.usuario_id)
    email = st.text_input("Email*", help="Para recibir confirmación")
    monto = st.number_input("Monto ARS*", min_value=10.0, value=50.0, step=10.0)
    
    if st.form_submit_button("Generar Pago", type="primary"):
        if not all([usuario_id, email, monto > 0]) or not validar_email(email):
            st.error("Complete todos los campos correctamente")
        else:
            with st.spinner("Creando link de pago..."):
                result = call_api("crear_pago", {
                    "usuario_id": usuario_id,
                    "monto": float(monto),
                    "email": email
                })
            
            if result.get("error"):
                st.error(f"Error: {result.get('detail')}")
            else:
                st.session_state.id_pago = result["id_pago_unico"]
                st.session_state.usuario_id = usuario_id
                st.success("Pago creado correctamente")
                st.markdown(f"""
                **ID de Pago:** {result['id_pago_unico']}  
                **Monto:** ${monto:.2f}  
                [Pagar ahora]({result['url_pago']})  
                """)

# Verificación de pago
if st.session_state.id_pago:
    st.divider()
    st.subheader("Verificar Estado del Pago")
    
    if st.button("Verificar ahora"):
        with st.spinner("Verificando estado..."):
            result = call_api("verificar_pago", {"id_pago_unico": st.session_state.id_pago})
            
            if result.get("error"):
                st.error(f"Error: {result.get('detail')}")
            elif result.get("status") == "approved":
                if not st.session_state.pago_procesado:
                    with st.spinner("Procesando en Ganamos..."):
                        success, balance = carga_ganamos(st.session_state.usuario_id, result.get('monto', 0))
                        
                        if success:
                            st.session_state.pago_procesado = True
                            st.success(f"✅ Carga exitosa! Balance actual: ${balance:.2f}")
                            st.balloons()
                        else:
                            st.error(f"❌ Falló la carga. Balance actual: ${balance:.2f}")
            else:
                st.warning("El pago aún no ha sido aprobado. Intente nuevamente más tarde.")

# Panel de ayuda
st.sidebar.markdown("""
### 📌 Instrucciones
1. Ingrese su ID de usuario de Ganamos
2. Complete su email válido
3. Especifique el monto a cargar
4. Haga clic en Pagar
5. Verifique el estado

### 🛠 Soporte Técnico
soporte@ejemplo.com  
Tel: 11 1234-5678
""")
