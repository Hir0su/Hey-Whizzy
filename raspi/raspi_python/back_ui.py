from flask import Flask, request
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

@app.route('/reply', methods=['POST'])
def handle_reply():
    reply = request.get_json()['reply']
    emit('reply', reply, namespace='', broadcast=True)
    return 'ok'

if __name__ == '__main__':
    socketio.run(app, debug=True)