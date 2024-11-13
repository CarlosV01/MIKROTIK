from flask import Flask, render_template, request, redirect, session, url_for
from module.management_dhcp import management_dhcp_bp
from module.management_firewall import management_firewall_dp
from module.management_ip import management_ip
from module.management_queues import management_queues
from module.management_session import management_session_bp
from module.utils import get_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para manejar sesiones

############      Login, logout       ############
app.register_blueprint(management_session_bp)
#################           BANDWITH       #########################
app.register_blueprint(management_queues)
##################       ADD IP       #####################
app.register_blueprint(management_ip)
##############        DHCP          #######################
app.register_blueprint(management_dhcp_bp)
#############            FIREWALL           #########################
app.register_blueprint(management_firewall_dp)
##############################################################################################
@app.route('/')
def index():
    if 'credentials' not in session:  # Verifica si hay credenciales en la sesión
        return redirect(url_for('management_session.login'))  # Redirige al login si no está autenticado
    
    try:
        api = get_connection()
        ip_addresses = api('/ip/address/print')
        return render_template('index.html', ip_addresses=ip_addresses)
    except Exception as e:
        return f"Error al cargar las direcciones IP: {e}"

if __name__ == '__main__':
    app.run(debug=True)
