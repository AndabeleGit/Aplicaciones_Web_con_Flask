from flask import Flask, render_template, url_for, request
from markupsafe import escape
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY = 'dev'
)

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

@app.route('/code/<path:code>')
def code(code):
    return f'<code> {escape(code)}</code>'

# Crear formularios

class RegisterForm(FlaskForm):
    username = StringField("Nombre de usuario: ", validators=[DataRequired(), Length(min = 4, max = 20)])
    password = PasswordField("Contraseña: ", validators=[DataRequired(), Length(min = 6, max = 20)])
    submit = SubmitField("Registar")

# Registrar usuario
@app.route('/auth/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        return f'Nombre de usuario: {username}, Contraseña; {password}'

        
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
        
    #     if len(username) >= 4 and len(username) <= 10 and len(password) >= 6 and len(password) <= 20:
    #         return f'Nombre de usuario: {username}, Contraseña; {password}'
    #     else:
    #         error = """Nombre de usuario debe tener entre 4 y 10 caracteres y
    #         la contraseña debe tener entre 6 y 20 caracteres"""
    #         return render_template('register.html', error = error, form = form)
    return render_template('register.html', form = form)