from flask import Blueprint, request, redirect, render_template, url_for
from module.utils import get_connection

management_firewall_dp = Blueprint('management_firewall', __name__)

@management_firewall_dp.route('/add_firewall_rule', methods=['GET', 'POST'])
def add_firewall_rule():
    if request.method == 'POST':
        chain = request.form['chain']
        action = request.form['action']
        src_address = request.form['src_address']
        dst_address = request.form['dst_address']
        protocol = request.form['protocol']
        port = request.form['port'] or '0'  # Asegúrate de manejar el puerto adecuadamente

        try:
            api = get_connection()
            # Actualizamos los nombres de los parámetros para que coincidan con los de la API de MikroTik
            api.path('ip', 'firewall', 'filter').add(
                chain=chain,
                action=action,
                **{
                    'src-address': src_address,
                    'dst-address': dst_address,
                    'protocol': protocol,
                    'dst-port': port  # Cambia 'port' a 'dst-port'
                }
            )
            return redirect('/firewall_rules')
        except Exception as e:
            return f"Error al agregar la regla de firewall: {e}"
    else:
        return render_template('add_firewall_rule.html')

@management_firewall_dp.route('/firewall_rules', methods=['GET'])
def firewall_rules():
    try:
        api = get_connection()
        # Asegúrate de usar los nombres correctos de las propiedades
        firewall_rules = api.path('ip', 'firewall', 'filter').select('.id', 'chain', 'action', 'src-address', 'dst-address', 'protocol', 'dst-port')
        return render_template('firewall_rules.html', firewall_rules=firewall_rules)
    except Exception as e:
        return f"Error al cargar las reglas de firewall: {e}"

@management_firewall_dp.route('/delete_firewall_rule/<rule_id>', methods=['POST'])
def delete_firewall_rule(rule_id):
    try:
        api = get_connection()
        api.path('ip', 'firewall', 'filter').remove(rule_id)  # Elimina la regla de firewall especificada
        return redirect(url_for('management_firewall.firewall_rules'))  # Redirige a la página de reglas de firewall
    except Exception as e:
        return f"Error al eliminar la regla de firewall: {e}", 500