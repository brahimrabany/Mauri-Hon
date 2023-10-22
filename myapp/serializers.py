from   .models import User_App
from rest_framework import serializers
from  .models import Message

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User_App
        fields = ['id','username', 'password']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User_App.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User_App.objects.all())
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
