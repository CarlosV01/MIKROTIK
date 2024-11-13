from idlelib.run import manage_socket

from flask import Blueprint, render_template, request, redirect, session, url_for
from module.utils import get_connection, get_interface_id

management_ip = Blueprint('management_ip', __name__)

# Modificar las rutas para usar las credenciales de la sesión
@management_ip.route('/add_ip', methods=['GET', 'POST'])
def add_ip():
    if 'credentials' not in session:  # Verifica si hay sesión
        return redirect(url_for('login'))  # Redirige al login si no está autenticado

    # El resto de la lógica para agregar IP
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        interface_name = request.form['interface']
        try:
            api = get_connection()
            interface_id = get_interface_id(api, interface_name)

            if interface_id is None:
                return "Error: interfaz no encontrada."

            api.path('ip', 'address').add(interface=interface_id, address=ip_address)
            return redirect('/')
        except Exception as e:
            return f"Error al agregar IP: {e}"
    else:
        try:
            api = get_connection()
            interfaces = api('/interface/print')
            return render_template('add_ip.html', interfaces=interfaces)
        except Exception as e:
            return f"Error al cargar interfaces: {e}"


@management_ip.route('/delete_ip/<ip_id>', methods=['POST'])
def delete_ip(ip_id):
    try:
        api = get_connection()
        api.path('ip', 'address').remove(ip_id)
        return redirect('/')
    except Exception as e:
        return f"Error al eliminar la dirección IP: {e}"