from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

@app.route('/reply', methods=['POST'])
def reply():
    reply = request.get_json()['reply']
    emit('reply', reply, namespace='', broadcast=True)
    return 'ok'

@app.route('/reply_large', methods=['POST'])
def reply_large():
    reply = request.get_json()['reply']
    print(f"Emitting reply_large event with: {reply}")
    emit('reply_large', reply, namespace='', broadcast=True)
    return 'ok'

@app.route('/image_data', methods=['POST'])
def image_data():
    image_data = request.get_json()['image_data']
    emit('image_data', image_data, namespace='', broadcast=True)
    return 'ok'

@app.route('/stop_talking', methods=['POST'])
def stop_talking():
    emit('stop_talking', namespace='', broadcast=True)
    return 'ok'

@app.route('/idle', methods=['POST'])
def idle():
    emit('idle', namespace='', broadcast=True)
    return 'ok'

@app.route('/idle_stop', methods=['POST'])
def idle_stop():
    emit('idle_stop', namespace='', broadcast=True)
    return 'ok'

@app.route('/change_background', methods=['POST'])
def change_background():
    index = request.get_json()['index']
    emit('change_background', index, namespace='', broadcast=True)
    return 'ok'

if __name__ == '__main__':
    socketio.run(app, debug=True)