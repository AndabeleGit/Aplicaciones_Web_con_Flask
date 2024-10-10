from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    name = None
    friends = ['Ándres', 'Juan', 'Pedro']
    return render_template('index.html', name = name, friends = friends)


@app.route('/Hello')
@app.route('/Hello/<name>')
@app.route('/Hello/<name>/<int:age>')
def Hello(name = None, age = None):
    if name == None and age == None:
        return "<h1>Hola Mundo</h1>"
    elif age == None:
        return f"<h1>Hola {name}"
    else:
        return f'Hola {name}, y tu edad es {age}'

app.route('code/<path:code>')
def code(code):
    return f'<code> {escape(code)}</code>'