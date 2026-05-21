from django.shortcuts import render
import requests

def users(request):
# obtener datos desde un rest api de terceras partes
    response = requests.get('https://jsonplaceholder.typicode.com/users')
# convertir los datos de repuesta en formato json
    usuarios = response.json()
    return render(request, "core/usuarios.html", {'usuarios': usuarios})

