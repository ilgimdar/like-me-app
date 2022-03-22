import json

from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import Participant
from .serializers import ParticipantSerializer


class CreateUserView(CreateAPIView):
    model = Participant
    serializer_class = ParticipantSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    '''
    Пока абсолютно каждый пользователь интернета с помощью корректного запроса может регистрировать новых 
    пользователей
    '''

    def post(self, request, *args, **kwargs):
        '''
        В случае успеха, данные пользователя попадают в БД и возвращается сообщение о том, что регистрация прошла \
        успешно. В противном случае возвращатеся сообщение с конкретной ошибкой (но со статусом 200)
        '''
        try:
            avatar = request.data['image']
            username = request.POST.get('username')
            password = request.POST.get('password')
            name = request.POST.get('name')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            Participant.objects.create(username=username, password=password, avatar=avatar, name=name, email=email,
                                       gender=gender)
            return HttpResponse(json.dumps({'message': 'User ' + username + ' registration successful'}), status=200)
        except Exception as e:
            return HttpResponse(json.dumps({'message': e}), status=200)
