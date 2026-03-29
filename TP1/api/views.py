from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
import json
# Base de datos en memoria (simulación)
items = [{"id": 1, "nombre": "Laptop"}, {"id": 2, "nombre": "Telefono"}]
@csrf_exempt # Desactiva la verificación CSRF para pruebas
def obtener_agregar_items(request):
    if request.method == 'GET': # Devolver la lista de ítems en formato JSON
        return JsonResponse(items, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body) # Convertir JSON en diccionario
            nuevo_item = { "id": len(items) + 1,
            "nombre": data.get("nombre", "Sin nombre")}
            items.append(nuevo_item) # Agregar el nuevo ítem a la lista
            return JsonResponse(nuevo_item, status=201) # Respuesta
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400) 

    
        

def eliminar_item(request, id):
    if request.method == 'DELETE':
        for item in items:
            if item['id'] == id:
                items.remove(item)
                return JsonResponse({'mensaje': 'Item eliminado'}, status = 204)
        return JsonResponse({'mensaje': 'No existe item con ese id'}, status = 400)
    
def modificar_item(request, id):
    if request.method == 'PUT' or request.method == 'PATCH':
        data = json.loads(request.body)
        for item in items:
            if request.method == 'PATCH':
                item['nombre'] = data.get('nombre', item['nombre'])
            elif request.method == 'PUT':
                item['nombre'] = data.get('nombre', 'sin nombre')
            return JsonResponse(item, status = 200)
        return JsonResponse({'errpr': 'No existe item con ese id'}, status = 400)

