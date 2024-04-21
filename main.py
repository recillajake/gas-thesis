from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Function to generate random numbers and emit them using SocketIO
def generate_random_numbers():
    while True:
        random_number = random.randint(1, 100)
        socketio.emit('update_number', {'number': random_number}, namespace='/test')
        time.sleep(0)

# Thread to run the random number generator function
generator_thread = threading.Thread(target=generate_random_numbers)
generator_thread.daemon = True
generator_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
