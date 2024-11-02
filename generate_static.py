from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Agrega aquí otras rutas que quieras generar como estáticas
@app.route('/about')
def about():
    return render_template('about.html')  # Asegúrate de tener esta plantilla

# Función para generar archivos estáticos
def generate_static_files(output_folder='static_site'):
    with app.test_request_context():
        routes = [
            ('/', 'index.html'),
             # Añade aquí otras rutas
        ]

        # Crea la carpeta de salida si no existe
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Genera archivos estáticos para cada ruta
        for route, filename in routes:
            response = app.test_client().get(route)
            if response.status_code == 200:
                with open(os.path.join(output_folder, filename), 'wb') as f:
                    f.write(response.data)
                print(f"Página {filename} generada correctamente.")
            else:
                print(f"Error al generar la página {filename}.")

if __name__ == '__main__':
    generate_static_files()
