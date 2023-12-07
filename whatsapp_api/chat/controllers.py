from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
from django.http import JsonResponse

from chat.repositorys import ChatroomRepository
from rest_framework import generics

from chat.entitys import Chatroom
from chat.serililzers import ChatRoomSerializer


def index(request):
    print(request.path)
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
from django.views.decorators.csrf import csrf_exempt

# class CreateChatRoom(APIView):
@csrf_exempt
def create_chatroom(request):
    # Implementation for creating a chatroom
    if request.method == 'POST':
        # Assuming the request data is in JSON format
        data = request.POST  # Adjust accordingly for your data format

        name = data.get('name')
        max_members = data.get('max_members')

        if not name or not max_members:
            return JsonResponse({'error': 'Name and max_members are required.'}, status=400)

        try:
            # Assuming you have a ChatroomService for business logic
            chatroom = ChatroomRepository.create_chatroom(name, max_members)
            response_data = {
                'id': chatroom.id,
                'name': chatroom.name,
                'max_members': chatroom.max_members,
            }
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def list_chatrooms(request):
    # Implementation for listing chatrooms
    if request.method == 'GET':
        try:
            # Assuming you have a ChatroomService for business logic
            chatroom = ChatroomRepository.get_chatrooms()
            print(chatroom)
            return JsonResponse(chatroom, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

class CreateListChatRooms(generics.ListCreateAPIView):
    # permission_classes = [IsAnyUser]
    queryset = Chatroom.objects.all()
    serializer_class = ChatRoomSerializer


class EnterLeaveRoom(generics.RetrieveDestroyAPIView):
    queryset = Chatroom.objects.all()
    serializer_class = ChatRoomSerializer
    
    
def leave_chatroom(request, chatroom_id, user_id):
    # Implementation for leaving a chatroom
    pass

def enter_chatroom(request, chatroom_id, user_id):
    # Implementation for entering a chatroom
    pass

def send_message(request, chatroom_id):
    # Implementation for sending a message
    pass

def list_messages(request, chatroom_id):
    # Implementation for listing messages   
    pass