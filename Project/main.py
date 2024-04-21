from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Tadaaaaa. . . '

@app.route('/home')
def home():
    return 'DRE NATA MAG MAGIC! HAHHAHAHAHAHAA. . . '

if __name__ == '__main__':
     app.run(debug=True,host='0.0.0.0')