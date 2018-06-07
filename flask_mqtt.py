import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = "52.36.175.99"
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
controllertopic = "controller/register"

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')

#@socketio.on('publish')
#def handle_publish(json_str):
 #   data = json.loads(json_str)
  #  mqtt.publish(data['topic'], data['message'])


#@socketio.on('subscribe')
#def handle_subscribe(json_str):
 #   data = json.loads(json_str)
  #  mqtt.subscribe(data['topic'])

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("MQTT connected")
    mqtt.subscribe(controllertopic)

@mqtt.on_subscribe()
def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed to Topic: " + controllertopic)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(client, userdata, message.payload.decode())
    print(message.payload.decode())
    mqtt.publish("controller/status",message.payload.decode())
    # data = dict(
    #     topic=message.topic,
    #     payload=message.payload.decode()
    # )
  #  socketio.emit('mqtt_message', data=data)


# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
#     print(level, buf)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, use_reloader=True, debug=True)