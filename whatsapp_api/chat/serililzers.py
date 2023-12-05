from rest_framework import serializers

from chat.entitys import Chatroom

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = '__all__'

