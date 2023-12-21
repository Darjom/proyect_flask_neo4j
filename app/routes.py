from app import app
from flask import render_template, jsonify, request, redirect, url_for, flash, session
from app.models.neo4j_model import test_connection, verify_credentials, create_user,get_user_info

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/test_db')
def test_db():
    result = test_connection()
    return jsonify({"result": result})

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']

    if verify_credentials(username, password):
        session['username'] = username
        return redirect(url_for('perfil'))  # Redirigir a la página principal o del perfil
    else:
        flash('Nombre de usuario o contraseña incorrectos.', 'error')
        return redirect(url_for('login_form'))

@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_submit():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    username = request.form['username']
    password = request.form['password']
    rol = request.form['rol']

    user_created = create_user(nombre, apellido, username, password, rol)
    if user_created:
        flash('Cuenta creada exitosamente.', 'success')
    else:
        flash('Hubo un problema al crear la cuenta.', 'error')

    return redirect(url_for('login_form'))

@app.route('/perfil')
def perfil():
    if 'username' in session:
        username = session['username']
        user_info = get_user_info(username)  # Asegúrate de definir esta función
        return render_template('perfil.html', user=user_info)
    else:
        return redirect(url_for('login_form'))

