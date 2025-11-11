import unittest
import json
from app import app, tasks  # ✅ Cambia esta línea

class TestTaskAPI(unittest.TestCase):
    
    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.app = app.test_client()
        self.app.testing = True
        # Limpiar las tareas antes de cada test
        tasks.clear()
        
    def test_home_endpoint(self):
        """Test 1: Verificar que el endpoint principal funciona"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('mensaje', data)
        self.assertIn('Pamela Moposita', data['mensaje'])
    
    def test_health_endpoint(self):
        """Test 2: Verificar que el endpoint de salud funciona"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
    
    def test_get_tasks_empty(self):
        """Test 3: Verificar que inicialmente no hay tareas"""
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total'], 0)
        self.assertEqual(len(data['tasks']), 0)
    
    def test_create_task(self):
        """Test 4: Crear una nueva tarea"""
        new_task = {
            'title': 'Completar taller',
            'description': 'Taller de Git, Docker y CI/CD'
        }
        response = self.app.post('/tasks',
                                 data=json.dumps(new_task),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Completar taller')
        self.assertEqual(data['id'], 1)
        self.assertFalse(data['completed'])
    
    def test_create_task_without_title(self):
        """Test 5: Intentar crear tarea sin título (debe fallar)"""
        new_task = {
            'description': 'Sin título'
        }
        response = self.app.post('/tasks',
                                 data=json.dumps(new_task),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_specific_task(self):
        """Test 6: Obtener una tarea específica"""
        # Primero crear una tarea
        new_task = {'title': 'Tarea de prueba'}
        self.app.post('/tasks',
                     data=json.dumps(new_task),
                     content_type='application/json')
        
        # Luego obtenerla
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)
    
    def test_get_nonexistent_task(self):
        """Test 7: Intentar obtener tarea que no existe"""
        response = self.app.get('/tasks/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_delete_task(self):
        """Test 8: Eliminar una tarea"""
        # Crear tarea
        new_task = {'title': 'Tarea a eliminar'}
        self.app.post('/tasks',
                     data=json.dumps(new_task),
                     content_type='application/json')
        
        # Eliminar tarea
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)
        
        # Verificar que ya no existe
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()