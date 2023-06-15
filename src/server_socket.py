from flask import Flask, render_template
from flask_socketio import SocketIO
import logging
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot.yobot import YoBot

app = Flask(__name__)
socketio = SocketIO(app)

class SocketIOHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        socketio.emit('newlog', {'log': msg})

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    pass  # Connection successful, no further action required

def start_server(yobot: 'YoBot'):
    logger = yobot.log  # Assuming `yobot` is your bot instance
    handler = SocketIOHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    socketio.run(app, port=5412)
