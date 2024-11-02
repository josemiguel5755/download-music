# from flask import Flask, render_template, request, jsonify, send_file
# import yt_dlp
# import os

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/download', methods=['POST'])
# def download_video():
#     data = request.get_json()
#     video_url = data['url']

#     try:
#         # Configuración para descargar solo el mejor audio
#         ydl_opts = {
#     'format': 'bestaudio/best',
#     'outtmpl': 'downloads/%(title)s.%(ext)s',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192',
#     }],
#     'ffmpeg_location': r'c:\Users\jose miguel\OneDrive - República Digital Educación\Escritorio\JOSEMGUEL\ffmpeg-7.1-essentials_build\bin',  
# }


#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(video_url, download=True)
#             mp3_path = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")

#         if os.path.exists(mp3_path):
#             return send_file(mp3_path, as_attachment=True)
#         else:
#             return jsonify({'error': 'Error during download'}), 500

#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     if not os.path.exists('downloads'):
#         os.mkdir('downloads')
#     app.run(debug=True)




# import re
# from flask import Flask, render_template, request, jsonify, send_file
# from flask_socketio import SocketIO, emit
# import yt_dlp
# import os

# app = Flask(__name__)
# socketio = SocketIO(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

# # Función de progreso mejorada para enviar actualizaciones a través de WebSocket
# def progress_hook(d):
#     if d['status'] == 'downloading':
#         percent_str = d['_percent_str']
#         match = re.search(r"(\d+\.\d+)", percent_str)  # Extrae el número decimal
#         if match:
#             percent = float(match.group(1))  # Convierte el valor extraído a float
#             socketio.emit('download_progress', {'progress': percent})
#         else:
#             print(f"Error parsing progress: {percent_str}")

# @app.route('/download', methods=['POST'])
# def download_video():
#     data = request.get_json()
#     video_url = data['url']

#     if not os.path.exists('downloads'):
#         os.makedirs('downloads')

#     try:
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'outtmpl': 'downloads/%(title)s.%(ext)s',
#             'progress_hooks': [progress_hook],
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#             'ffmpeg_location': r'c:\Users\jose miguel\OneDrive - República Digital Educación\Escritorio\JOSEMGUEL\ffmpeg-7.1-essentials_build\bin',
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(video_url, download=True)
#             mp3_path = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")

#         if os.path.exists(mp3_path):
#             return send_file(mp3_path, as_attachment=True)
#         else:
#             return jsonify({'error': 'Error during download'}), 500

#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     socketio.run(app, debug=True)


# from flask import Flask, render_template, request, jsonify, send_file
# from flask_socketio import SocketIO, emit
# import yt_dlp
# import os
# import threading
# from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget
# from PyQt5.QtCore import QUrl
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# import sys

# app = Flask(__name__)
# socketio = SocketIO(app)

# # Ruta de almacenamiento de las descargas
# DOWNLOAD_FOLDER = 'downloads'
# if not os.path.exists(DOWNLOAD_FOLDER):
#     os.makedirs(DOWNLOAD_FOLDER)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/download', methods=['POST'])
# def download_video():
#     data = request.get_json()
#     video_url = data['url']

#     try:
#         # Asegúrate de que esta ruta sea correcta o que ffmpeg esté en el PATH del sistema
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
#             'ffmpeg_location': r'c:\Users\jose miguel\OneDrive - República Digital Educación\Escritorio\JOSEMGUEL\ffmpeg-7.1-essentials_build\bin',  # Ajusta esta ruta si es necesario
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#             'progress_hooks': [progress_hook],
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(video_url, download=True)
#             mp3_path = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")

#         if os.path.exists(mp3_path):
#             return send_file(mp3_path, as_attachment=True)
#         else:
#             return jsonify({'error': 'Error during download'}), 500

#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({'error': str(e)}), 500

# def progress_hook(d):
#     if d['status'] == 'downloading':
#         progress = d.get('_percent_str', '').strip()
#         socketio.emit('download_progress', {'progress': progress})

# # Iniciar Flask en un hilo separado para evitar bloquear la interfaz PyQt
# def run_flask():
#     socketio.run(app, port=5000)

# # Interfaz PyQt para mostrar la aplicación de Flask embebida
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.browser = QWebEngineView()
#         self.browser.setUrl(QUrl("http://localhost:5000"))

#         container = QWidget()
#         layout = QVBoxLayout()
#         layout.addWidget(self.browser)
#         container.setLayout(layout)

#         self.setCentralWidget(container)
#         self.setWindowTitle("YouTube Music Downloader")
#         self.resize(800, 600)

# if __name__ == '__main__':
#     flask_thread = threading.Thread(target=run_flask)
#     flask_thread.start()

#     app_qt = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app_qt.exec_())


from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import yt_dlp
import os
import threading
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

# Inicializar Flask con SocketIO especificando el modo asíncrono.
app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')  # Usa 'threading' como modo predeterminado

# Ruta de almacenamiento de las descargas
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data['url']

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'ffmpeg_location': r'c:\Users\jose miguel\OneDrive - República Digital Educación\Escritorio\JOSEMGUEL\ffmpeg-7.1-essentials_build\bin',  # Ajusta esta ruta si es necesario
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            mp3_path = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        if os.path.exists(mp3_path):
            return send_file(mp3_path, as_attachment=True)
        else:
            return jsonify({'error': 'Error during download'}), 500

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

def progress_hook(d):
    if d['status'] == 'downloading':
        progress = d.get('_percent_str', '').strip()
        socketio.emit('download_progress', {'progress': progress})

# Iniciar Flask en un hilo separado para evitar bloquear la interfaz PyQt
def run_flask():
    socketio.run(app, port=5000)

# Interfaz PyQt para mostrar la aplicación de Flask embebida
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://localhost:5000"))

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.setWindowTitle("HODEN")
        self.setWindowIcon(QIcon("static/imagenes/a-unique-logo-for-a-music-downloader-desktop-appli-8sgjAUswS7O9PjgC2o8B3w-6Phv0isPTaC-HUAXi2TdHg.ico"))  # Cambia esta ruta al icono
        self.resize(800, 600)

if __name__ == '__main__':
    from PyQt5.QtGui import QIcon  # Importa QIcon aquí

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Daemon para que se cierre al salir de la aplicación principal
    flask_thread.start()

    app_qt = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app_qt.exec_())
