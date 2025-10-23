import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Configuración de página
st.set_page_config(
    page_title="Control MQTT",
    page_icon="🌡️",
    layout="centered"
)

# Estilos CSS minimalistas
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #2563EB;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .control-section {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid #E2E8F0;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-on {
        background: #10B981;
    }
    .status-off {
        background: #EF4444;
    }
    .stButton button {
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 500;
        width: 100%;
        transition: all 0.3s ease;
    }
    .btn-on {
        background: #10B981;
        color: white;
    }
    .btn-on:hover {
        background: #059669;
        color: white;
    }
    .btn-off {
        background: #EF4444;
        color: white;
    }
    .btn-off:hover {
        background: #DC2626;
        color: white;
    }
    .btn-send {
        background: #2563EB;
        color: white;
    }
    .btn-send:hover {
        background: #1D4ED8;
        color: white;
    }
    .info-box {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Variables de estado
if 'current_status' not in st.session_state:
    st.session_state.current_status = "OFF"
if 'last_value' not in st.session_state:
    st.session_state.last_value = 0.0
if 'last_message' not in st.session_state:
    st.session_state.last_message = ""

# Callbacks MQTT
def on_publish(client, userdata, result):
    st.toast("✅ Mensaje publicado exitosamente")

def on_message(client, userdata, message):
    global message_received
    time.sleep(1)
    message_received = str(message.payload.decode("utf-8"))
    st.session_state.last_message = message_received

# Configuración MQTT
broker = "157.230.214.127"
port = 1883

# Header
st.markdown('<div class="main-title">🌡️ Control MQTT</div>', unsafe_allow_html=True)

# Información del sistema
with st.expander("ℹ️ Información del sistema", expanded=False):
    st.write(f"**Versión de Python:** {platform.python_version()}")
    st.write(f"**Broker:** {broker}:{port}")
    st.write(f"**Cliente ID:** GIT-HUB")

# Sección de control ON/OFF
st.markdown("### Control de Estado")

col1, col2 = st.columns(2)

with col1:
    if st.button('🔘 ENCENDER', key='on_btn', use_container_width=True):
        st.session_state.current_status = "ON"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": "ON"})
        client1.publish("cmqtt_s", message)
        client1.disconnect()

with col2:
    if st.button('⚫ APAGAR', key='off_btn', use_container_width=True):
        st.session_state.current_status = "OFF"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": "OFF"})
        client1.publish("cmqtt_s", message)
        client1.disconnect()

# Indicador de estado actual
status_color = "🟢" if st.session_state.current_status == "ON" else "🔴"
st.markdown(f"**Estado actual:** {status_color} {st.session_state.current_status}")

# Sección de control analógico
st.markdown("### Control Analógico")

values = st.slider(
    'Selecciona el valor analógico',
    0.0, 100.0,
    value=st.session_state.last_value,
    step=0.1,
    format="%.1f"
)

st.write(f"**Valor seleccionado:** {values}")

if st.button('Enviar Valor Analógico', use_container_width=True):
    st.session_state.last_value = values
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_a", message)
    client1.disconnect()

st.markdown('</div>', unsafe_allow_html=True)

# Sección de mensajes recibidos
st.markdown("### Mensajes Recibidos")

if st.button('🔄 Actualizar Mensajes', use_container_width=True):
    try:
        client1 = paho.Client("GIT-HUB")
        client1.on_message = on_message
        client1.connect(broker, port)
        client1.subscribe("Sensores")
        client1.loop_start()
        time.sleep(2)
        client1.loop_stop()
        client1.disconnect()
    except Exception as e:
        st.error(f"Error al recibir mensajes: {e}")

if st.session_state.last_message:
    st.write("**Último mensaje recibido:**")
    st.code(st.session_state.last_message)
else:
    st.info("No hay mensajes recibidos. Haz clic en 'Actualizar Mensajes' para ver los últimos datos.")


