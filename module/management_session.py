from flask import Blueprint, request, session, redirect, url_for, render_template
from module.utils import get_connection

management_session_bp = Blueprint('management_session', __name__)

@management_session_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        host = request.form['host']

        try:
            # Guardar las credenciales en la sesión
            session['credentials'] = {
                'username': username,
                'password': password,
                'host': host
            }
            # Probar la conexión
            api = get_connection()
            return redirect(url_for('index'))  # Redirige al index después de un login exitoso
        except Exception as e:
            return f"Error de autenticación: {e}"

    return render_template('login.html')


@management_session_bp.route('/logout')
def logout():
    session.pop('username', None)  # Elimina el nombre de usuario de la sesión
    return redirect(url_for('management_session.login'))  # Redirige al login