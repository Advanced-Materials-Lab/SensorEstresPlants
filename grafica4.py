import dash
from dash import dcc, html, dash_table
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from collections import deque
import paho.mqtt.client as mqtt
import pandas as pd

# --- Datos ---
MAX_POINTS = 100
tiempo = deque(maxlen=MAX_POINTS)
voltaje = deque(maxlen=MAX_POINTS)
resistencia = deque(maxlen=MAX_POINTS)

# Todos los datos para descarga CSV
datos_totales = []

# Estados
estado_sd = "Desconocido"
estado_mqtt = "Desconectado"

# --- MQTT ---
def on_connect(client, userdata, flags, rc):
    global estado_mqtt
    if rc == 0:
        estado_mqtt = "Conectado"
        # 👇 Suscribirse a los mismos topics que publica el ESP32
        client.subscribe("eve/esp32/datos")
        client.subscribe("eve/esp32/estado")
    else:
        estado_mqtt = f"Error (rc={rc})"

def on_message(client, userdata, msg):
    global estado_sd, datos_totales
    payload = msg.payload.decode()
    print("📩 Recibido:", msg.topic, payload)  # 👈 Debug para ver datos en consola
    if msg.topic == "eve/esp32/datos":
        try:
            t, v, r = payload.split(',')
            tiempo.append(int(t))
            voltaje.append(float(v))
            resistencia.append(float(r))
            datos_totales.append({
                'Tiempo_s': int(t),
                'Voltaje_V': float(v),
                'Resistencia_Ohm': float(r)
            })
        except Exception as e:
            print("⚠️ Error procesando:", payload, e)
    elif msg.topic == "eve/esp32/estado":
        estado_sd = payload

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 👇 Usa la misma IP de tu broker local (PC o servidor Mosquitto)
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

# --- Dash app ---
app = dash.Dash(__name__)
server = app.server  # Para despliegue

app.layout = html.Div([
    html.H2("Dashboard ESP32 - Voltaje en Tiempo Real", style={'textAlign':'center'}),
    html.Div([
        # Gráfica
        dcc.Graph(id='live-graph', style={'width':'65%', 'display':'inline-block'}),
        
        # Panel lateral
        html.Div([
            html.H4("Panel de Estado"),
            html.Pre(id='status-panel', style={'whiteSpace': 'pre-line', 'fontFamily':'monospace', 'fontSize':14}),
            html.H4("Últimos 10 Registros"),
            dash_table.DataTable(
                id='tabla-datos',
                columns=[
                    {"name":"Tiempo_s", "id":"Tiempo_s"},
                    {"name":"Voltaje_V", "id":"Voltaje_V"},
                    {"name":"Resistencia_Ohm", "id":"Resistencia_Ohm"}
                ],
                style_cell={'textAlign':'center', 'fontFamily':'monospace'},
                style_header={'fontWeight':'bold'},
                page_size=10
            ),
            html.Br(),
            html.Button("Descargar CSV", id="btn-download"),
            dcc.Download(id="download-data")
        ], style={'width':'33%', 'display':'inline-block', 'verticalAlign':'top', 'padding':'10px'})
    ]),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
])

# --- Callbacks ---
@app.callback(
    [Output('live-graph','figure'),
     Output('status-panel','children'),
     Output('tabla-datos','data')],
    [Input('interval-component','n_intervals')]
)
def update_dashboard(n):
    # Gráfica
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(tiempo), y=list(voltaje), mode='lines', name='Voltaje (V)'))
    fig.update_layout(xaxis_title='Tiempo (s)', yaxis_title='Voltaje (V)', template='plotly_dark')
    
    # Panel estado
    if len(tiempo) > 0:
        t_val = tiempo[-1]
        v_val = voltaje[-1]
        r_val = resistencia[-1]
    else:
        t_val = v_val = r_val = "-"
    status_text = f"⏱ Tiempo: {t_val} s\n🔋 Voltaje: {v_val} V\n⚡ Resistencia: {r_val} Ω\n📡 MQTT: {estado_mqtt}\n💾 SD: {estado_sd}"
    
    # Tabla últimos 10 registros
    tabla_data = datos_totales[-10:]
    
    return fig, status_text, tabla_data

# --- Callback descarga CSV ---
@app.callback(
    Output("download-data","data"),
    [Input("btn-download","n_clicks")]
)
def download_csv(n_clicks):
    if n_clicks is None:
        return dash.no_update
    df = pd.DataFrame(datos_totales)
    return dcc.send_data_frame(df.to_csv, "datos_mqtt.csv", index=False)

# --- Run server ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)

