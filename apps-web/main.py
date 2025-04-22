import webview
import subprocess
import os

# Función para iniciar Flask
def start_flask():
    if os.name == 'nt':
        subprocess.Popen(['python', 'app.py'])  # Windows
    else:
        subprocess.Popen(['python3', 'app.py'])  # Mac/Linux

# Iniciar el servidor Flask
start_flask()

# Crear una ventana de escritorio que cargue la URL del servidor Flask
window = webview.create_window('Datalake Utils Webapp', 'http://127.0.0.1:5000')
webview.start()
