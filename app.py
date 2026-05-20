import json
import os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, url_for, abort
from werkzeug.utils import secure_filename

# Carpeta compartida de red donde se guardan los videos.
# Puedes cambiarla con la variable de entorno VIDEO_SHARE_PATH.
VIDEO_ROOT = os.environ.get('VIDEO_SHARE_PATH', r"\\cofs04\Gindustrial\Industrial\TV´S Lean")
SHARED_FOLDER = Path(VIDEO_ROOT)

CONFIG_FILE = Path(__file__).resolve().parent / 'processes.json'
DEFAULT_PROCESSES = [
    {'id': 'proceso1', 'label': 'Emulsiones'},
    {'id': 'proceso2', 'label': 'Hidroalcoholes'},
    {'id': 'proceso3', 'label': 'Maquillajes'},
    {'id': 'proceso4', 'label': 'Almacén'},
]

PROCESSES = {}
try:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = json.load(file)
        process_list = config.get('processes', DEFAULT_PROCESSES)
    else:
        process_list = DEFAULT_PROCESSES
    for item in process_list:
        PROCESSES[item['id']] = item['label']
except Exception:
    PROCESSES = {item['id']: item['label'] for item in DEFAULT_PROCESSES}

for process_dir in PROCESSES:
    (SHARED_FOLDER / process_dir).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'.mp4', '.webm', '.ogg', '.mov', '.m4v'}

app = Flask(__name__, static_folder=str(Path(__file__).resolve().parent), static_url_path='')


def allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def process_folder(process_name: str) -> Path:
    if process_name not in PROCESSES:
        abort(404)
    return SHARED_FOLDER / process_name


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/processes', methods=['GET'])
def list_processes():
    return jsonify({'processes': [{'id': key, 'label': value} for key, value in PROCESSES.items()]})


@app.route('/api/videos/<process_name>', methods=['GET'])
def list_videos(process_name: str):
    folder = process_folder(process_name)
    videos = []
    for path in sorted(folder.iterdir()):
        if path.is_file() and allowed_file(path.name):
            videos.append({
                'name': path.name,
                'url': url_for('serve_video', process_name=process_name, filename=path.name)
            })
    return jsonify({'videos': videos, 'process': process_name, 'label': PROCESSES[process_name]})


@app.route('/api/upload', methods=['POST'])
def upload_video():
    process_name = request.args.get('process') or request.form.get('process')
    if not process_name:
        return jsonify({'error': 'Debe especificar un proceso.'}), 400

    folder = process_folder(process_name)

    if 'file' not in request.files:
        return jsonify({'error': 'No se recibió ningún archivo.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'El nombre de archivo es inválido.'}), 400

    filename = secure_filename(file.filename)
    if not allowed_file(filename):
        return jsonify({'error': 'Solo se permiten archivos de video: mp4, webm, ogg, mov, m4v.'}), 400

    target_path = folder / filename
    file.save(target_path)
    return jsonify({'message': f'Video cargado con éxito en {PROCESSES[process_name]}.'}), 201


@app.route('/videos/<process_name>/<path:filename>')
def serve_video(process_name: str, filename: str):
    folder = process_folder(process_name)
    if not allowed_file(filename):
        abort(404)
    return send_from_directory(str(folder), filename, conditional=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
