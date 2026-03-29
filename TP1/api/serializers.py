from rest_framework import serializers
from .models import Objetos

class ObjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objetos
        fields = ('id','nombre')


#Estaba probando la documentacion de Django rest framework