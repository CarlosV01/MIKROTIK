from flask import Blueprint, render_template, request, redirect
from module.utils import get_connection

management_dhcp_bp = Blueprint('management_dhcp', __name__)

@management_dhcp_bp.route('/dhcp_server')
def dhcp_server():
    try:
        api = get_connection()
        dhcp_servers = api.path('ip', 'dhcp-server').select('.id', 'name', 'interface', 'lease-time', 'address-pool', 'use-radius', 'dynamic', 'invalid', 'disabled')
        return render_template('dhcp_server.html', dhcp_servers=dhcp_servers)
    except Exception as e:
        return f"Error al cargar servidores DHCP: {e}"

@management_dhcp_bp.route('/add_dhcp_server', methods=['GET', 'POST'])
def add_dhcp_server():
    if request.method == 'POST':
        name = request.form['name']
        interface = request.form['interface']
        address_pool = request.form['pool']
        lease_time = request.form['lease_time']

        try:
            api = get_connection()
            api.path('ip', 'dhcp-server').add(
                name=name,
                interface=interface,
                **{'address-pool': address_pool, 'lease-time': lease_time}
            )
            return redirect('/dhcp_server')
        except Exception as e:
            return f"Error al agregar el servidor DHCP: {e}"
    else:
        try:
            api = get_connection()
            interfaces = api('/interface/print')
            pools = api('/ip/pool/print')
            return render_template('add_dhcp_server.html', interfaces=interfaces, pools=pools)
        except Exception as e:
            return f"Error al cargar las interfaces o pools: {e}"

@management_dhcp_bp.route('/delete_dhcp/<dhcp_id>', methods=['POST'])
def delete_dhcp(dhcp_id):
    try:
        api = get_connection()
        api.path('ip', 'dhcp-server').remove(dhcp_id)
        return redirect('/dhcp_server')
    except Exception as e:
        return f"Error al eliminar el DHCP Server: {e}", 500

@management_dhcp_bp.route('/add_pool', methods=['GET', 'POST'])
def add_pool():
    if request.method == 'POST':
        name = request.form['name']
        range_start = request.form['range_start']
        range_end = request.form['range_end']

        try:
            api = get_connection()
            api.path('ip', 'pool').add(name=name, ranges=f"{range_start}-{range_end}")
            return redirect('/add_dhcp_server')
        except Exception as e:
            return f"Error al agregar el pool de direcciones: {e}"
    else:
        return render_template('add_pool.html')