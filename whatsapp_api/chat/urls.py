from django.urls import path

from . import controllers

urlpatterns = [
    path("", controllers.CreateListChatRooms.as_view(), name="index"),
    path("room_list/", controllers.CreateListChatRooms.as_view(), name="index"),
    path("<int:id>/", controllers.EnterLeaveRoom.as_view(), name="room"),
]
