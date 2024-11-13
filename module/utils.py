from librouteros import connect
from flask import session

def get_connection():
    """Función para conectar a la API de MikroTik utilizando las credenciales de la sesión."""
    credentials = session.get('credentials')
    if credentials:
        return connect(**credentials)
    else:
        raise Exception("No se proporcionaron credenciales")

def get_interface_id(api, interface_name):
    """Obtiene el ID de una interfaz a partir de su nombre."""
    interfaces = api('/interface/print')
    for interface in interfaces:
        if interface['name'] == interface_name:
            return interface['.id']
    return None