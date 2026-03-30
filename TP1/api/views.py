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

    
        
@csrf_exempt
def eliminar_item(request, id):
    if request.method == 'DELETE':
        for item in items:
            if item['id'] == id:
                items.remove(item)
                return JsonResponse({'mensaje': 'Item eliminado'}, status = 204)
        return JsonResponse({'mensaje': 'No existe item con ese id'}, status = 400)

@csrf_exempt  
def modificar_item(request, id):
    if request.method == 'PUT' or request.method == 'PATCH':
        data = json.loads(request.body)
        for item in items:
            if item['id'] == id:
                if request.method == 'PATCH':
                    item['nombre'] = data.get('nombre', item['nombre'])
                elif request.method == 'PUT':
                    item['nombre'] = data.get('nombre', 'sin nombre')
                return JsonResponse(item, status = 200)
            
        return JsonResponse({'error': 'No existe item con ese id'}, status = 400)



#   EDITAR
# (.venv) PS D:\Documentos\universidad\desarrolloAPIs\trabajos_catedra> curl -X PUT "http://127.0.0.1:8000/api/items/editar/1" -H "Content-Type: application/json" -d
#  '{"nombre": "Item Actualizado"}'
# {"id": 1, "nombre": "Item Actualizado"}


#   ELIMINAR
# (.venv) PS D:\Documentos\universidad\desarrolloAPIs\trabajos_catedra> curl -v -X DELETE "http://127.0.0.1:8000/api/items/eliminar/1/"
# *   Trying 127.0.0.1:8000...
# * Established connection to 127.0.0.1 (127.0.0.1 port 8000) from 127.0.0.1 port 64211
# * using HTTP/1.x
# > DELETE /api/items/eliminar/1/ HTTP/1.1
# > Host: 127.0.0.1:8000
# > User-Agent: curl/8.18.0
# > Accept: */*
# >
# * Request completely sent off
# < HTTP/1.1 204 No Content
# < Date: Mon, 30 Mar 2026 12:41:45 GMT
# < Server: WSGIServer/0.2 CPython/3.13.1
# < Content-Type: application/json
# < X-Frame-Options: DENY
# < Content-Length: 29
# < X-Content-Type-Options: nosniff
# < Referrer-Policy: same-origin
# < Cross-Origin-Opener-Policy: same-origin
# <
# * Excess found writing body: excess = 29, size = 0, maxdownload = 0, bytecount = 0
# * shutting down connection #0