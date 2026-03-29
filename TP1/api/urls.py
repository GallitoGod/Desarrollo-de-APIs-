from django.urls import path 
from .views import obtener_agregar_items, eliminar_item, modificar_item

urlpatterns = [
    path('items/', obtener_agregar_items, name='obtener_agregar_items'),
    path('items/<int:id>/', eliminar_item, name= 'eliminar_item'),
    path('items/ediatr/<int:id>', modificar_item, name= 'modificar_item'),
]
