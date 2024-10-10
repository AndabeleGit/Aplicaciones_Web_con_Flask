from flask import Flask, render_template, url_for
from markupsafe import escape
from datetime import datetime

app = Flask(__name__)

# filtro personalizado
@app.add_template_filter
def today(date):
    return date.strftime('%d-%m-%Y')

# funcion personalizada
# manera para no enviarla por el reder template
@app.add_template_global 
def repeat(s, n):
    return s * n

# ruta principal
@app.route('/')
def index():
    print(url_for('index'))
    print(url_for('Hello'))
    name = 'Alex'
    date = datetime.now()
    friends = ['Ándres', 'Juan', 'Pedro']
    return render_template('index.html', 
                           name = name, 
                           friends = friends, 
                           fecha = date,
                        )

@app.route('/Hello')
@app.route('/Hello/<name>')
@app.route('/Hello/<name>/<int:age>')
@app.route('/Hello/<name>/<int:age>/<email>')
def Hello(name = None, age = None, email = None):
    datos = {
        'name': name,
        'age': age,
        'email': email
    }
    return render_template('hello.html',
                       datos = datos)

app.route('code/<path:code>')
def code(code):
    return f'<code> {escape(code)}</code>'