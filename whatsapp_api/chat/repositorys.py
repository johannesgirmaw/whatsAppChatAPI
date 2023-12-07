from .entitys import Chatroom
from django.core.serializers import serialize
from django.db import models
class ChatroomRepository:
    @classmethod
    def create_chatroom(cls, name, max_members):
        """
        Create a new chatroom.

        Args:
            name (str): Name of the chatroom.
            max_members (int): Maximum number of members allowed in the chatroom.

        Returns:
            Chatroom: The created chatroom instance.
        """
        if not name or not max_members:
            raise ValueError("Name and max_members are required.")

        # Additional validation logic can be added here if needed

        # Create the chatroom
        chatroom = Chatroom.objects.create(name=name, max_members=max_members)

        return chatroom
    
    @classmethod
    def get_chatrooms(cls):
        """
        get all chatrooms.

        Returns:
            Chatroom: all chat rooms.
        """
        # Create the chatroom
        chatroom = Chatroom.objects.all()
        json_data = serialize('json', chatroom)
        return json_data
