import paho.mqtt.client as paho
import paho.mqtt as mqtt


def _do_publish(client):
    
    message = client._userdata.pop()

    if isinstance(message, dict):
        client.publish(**message)
    elif isinstance(message, tuple):
        client.publish(*message)
    else:
        raise ValueError('message must be a dict or a tuple')


def _on_connect(client, userdata, flags, rc):
    
    if rc == 0:
        if len(userdata) > 0:
            _do_publish(client)
    else:
        raise mqtt.MQTTException(paho.connack_string(rc))


def _on_publish(client, userdata, mid):
    """Internal callback"""
    #pylint: disable=unused-argument

    if len(userdata) == 0:
        client.disconnect()
    else:
        _do_publish(client)


def multiple(msgs, hostname="52.36.175.99", port=1883, client_id="", keepalive=60,
             will=None, auth=None, tls=None, protocol=paho.MQTTv311,
             transport="tcp"):
    

    if not isinstance(msgs, list):
        raise ValueError('msgs must be a list')

    client = paho.Client(client_id=client_id,
                         userdata=msgs, protocol=protocol, transport=transport)

    client.on_publish = _on_publish
    client.on_connect = _on_connect

    if auth:
        username = auth.get('username')
        if username:
            password = auth.get('password')
            client.username_pw_set(username, password)
        else:
            raise KeyError("The 'username' key was not found, this is "
                           "required for auth")

    if will is not None:
        client.will_set(**will)

    if tls is not None:
        if isinstance(tls, dict):
            client.tls_set(**tls)
        else:
            client.tls_set_context(tls)

    client.connect(hostname, port, keepalive)
    client.loop_forever()


def single(topic, payload=None, qos=0, retain=False, hostname="52.36.175.99",
           port=1883, client_id="", keepalive=60, will=None, auth=None,
           tls=None, protocol=paho.MQTTv311, transport="tcp"):
    

    msg = {'topic':topic, 'payload':payload, 'qos':qos, 'retain':retain}

    multiple([msg], hostname, port, client_id, keepalive, will, auth, tls,
protocol, transport)