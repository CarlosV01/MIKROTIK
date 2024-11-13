from flask import session, redirect, url_for, render_template, request, Blueprint
from librouteros.query import Key
from module.utils import get_connection

management_queues = Blueprint('management_queues', __name__)


def format_limit(limit):
    if limit >= 1_000_000:
        return f"{limit / 1_000_000:.1f}M"  # M para Mega
    elif limit >= 1_000:
        return f"{limit / 1_000:.1f}K"  # K para Kilo
    else:
        return str(limit)


@management_queues.route('/queues')
def queues():
    if 'credentials' not in session:  # Verifica si hay credenciales en la sesión
        return redirect(url_for('login'))  # Redirige al login si no está autenticado

    try:
        api = get_connection()

        # Define las claves que quieres seleccionar
        id_key = Key('.id')
        name_key = Key('name')
        target_key = Key('target')
        max_limit_key = Key('max-limit')

        # Realiza la consulta usando las claves
        query = api.path('queue', 'simple').select(id_key, name_key, target_key, max_limit_key)

        # Inicializa una lista para almacenar las colas
        queues = []

        # Itera sobre el objeto query para obtener los resultados
        for row in query:
            # Procesa cada fila
            if 'max-limit' in row:
                upload, download = row['max-limit'].split('/')  # Suponiendo que el formato es "upload/download"
                row['upload_max_limit'] = format_limit(int(upload))  # Formatea el límite de carga
                row['download_max_limit'] = format_limit(int(download))  # Formatea el límite de descarga
            else:
                row['upload_max_limit'] = 'N/A'  # Si no hay límite de carga
                row['download_max_limit'] = 'N/A'  # Si no hay límite de descarga

            queues.append(row)  # Agrega la fila procesada a la lista

        return render_template('queues.html', queues=queues)  # Renderiza la plantilla
    except Exception as e:
        return f"Error al cargar las colas: {e}"


@management_queues.route('/add_queue', methods=['GET', 'POST'])
def add_queue():
    if request.method == 'POST':
        name = request.form.get('name')
        target = request.form.get('target')
        upload_limit = request.form.get('upload_limit')
        download_limit = request.form.get('download_limit')

        try:
            api = get_connection()
            # Usa el formato correcto para max-limit
            api.path('queue', 'simple').add(
                name=name,
                target=target,
                **{
                    'max-limit': f"{upload_limit}/{download_limit}"  # Combina límites en un solo parámetro
                }
            )
            return redirect(url_for('management_queues.queues'))  # Redirige a la página de colas
        except Exception as e:
            return f"Error al agregar la cola: {e}", 500

    return render_template('add_queue.html')


@management_queues.route('/delete_queue/<queue_id>', methods=['POST'])
def delete_queue(queue_id):
    try:
        api = get_connection()
        api.path('queue', 'simple').remove(queue_id)  # Elimina la cola especificada
        return redirect(url_for('management_queues.queues'))  # Redirige a la página de colas
    except Exception as e:
        return f"Error al eliminar la cola: {e}", 500