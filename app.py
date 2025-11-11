from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)


tasks = []
task_id_counter = 1

@app.route('/')
def home():
    return jsonify({
        'mensaje': 'API de Tareas - Pamela Moposita',
        'version': '1.0.1',
        'endpoints': {
            'GET /': 'Información de la API',
            'GET /tasks': 'Listar todas las tareas',
            'POST /tasks': 'Crear nueva tarea',
            'GET /tasks/<id>': 'Obtener tarea específica',
            'DELETE /tasks/<id>': 'Eliminar tarea',
            'GET /health': 'Estado del servicio'
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        'tasks': tasks,
        'total': len(tasks)
    })

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'El campo title es requerido'}), 400
    
    new_task = {
        'id': task_id_counter,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    task_id_counter += 1
    
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task is None:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task is None:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    
    return jsonify({'message': 'Tarea eliminada correctamente'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)