import json

from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from logic import jpg_to_png, watermark_with_transparency, send_love_message, geo_distance, float_normalize
from mysite.settings import MEDIA_ROOT
from .models import Participant
from .serializers import ParticipantSerializer, MatchSerializer, ParticipantFilter, DistanceSerializer
from django_filters.rest_framework import DjangoFilterBackend


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
            location = request.POST.get('location')
            if not Participant.objects.filter(username=username).exists():
                participant = Participant.objects.create(username=username, password=password, avatar=avatar, name=name,
                                                         email=email,
                                                         gender=gender, location=location)
                participant.save()
                part_get = Participant.objects.get(username=username)
                avatar_url = MEDIA_ROOT + '/' + str(part_get.avatar)
                new_avatar_url = jpg_to_png(str(part_get.avatar))
                part_get.avatar = new_avatar_url
                part_get.save()
                new_avatar_url = MEDIA_ROOT + '/' + new_avatar_url
                watermark_with_transparency(avatar_url, new_avatar_url, MEDIA_ROOT + '/watermark.png',
                                            position=(0, 0))
                part_get.save()
                return Response(json.dumps({"message": "User " + username + " registration successful"}), status=200)
            else:
                raise Exception
        except Exception as e:
            return Response(json.dumps({"message": str(e)}), status=200)


class MatchView(ListAPIView):
    model = Participant
    serializer_class = MatchSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get(self, request, *args, **kwargs):
        from_id = int(request.GET.get('from_id'))
        to_id = int(request.GET.get('to_id'))
        if Participant.objects.filter(id=from_id).exists() and Participant.objects.filter(id=to_id).exists():
            from_participant = Participant.objects.get(id=from_id)
            to_participant = Participant.objects.get(id=to_id)
            likes_json = str(to_participant.likes).replace("'", '"')
            likes_list = json.loads(likes_json)
            from_participant.likes[str(to_participant.id)] = 1
            from_participant.save()
            if from_id in list(map(int, likes_list.keys())):
                email1 = from_participant.email
                email2 = to_participant.email
                send_love_message(email1,
                                  'Поздравляем! У вас взаимная симпатия с пользователем ' + to_participant.name +
                                  '!\n Вот почта для связи: ' + to_participant.email)
                send_love_message(email2,
                                  'Поздравляем! У вас взаимная симпатия с пользователем ' + from_participant.name +
                                  '!\n Вот почта для связи: ' + from_participant.email)
                return Response(json.dumps({"message": "Match! Emails were successfully sent"}), status=200)
            else:
                return Response(json.dumps({"message": "User added to the liked list. No match"}), status=200)
        else:
            return Response(json.dumps({"message": "ids not exist"}), status=200)


class ParticipantList(ListAPIView):
    serializer_class = ParticipantSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ParticipantFilter

    def get_queryset(self):
        return Participant.objects.all()


class DistanceView(ListAPIView):
    serializer_class = DistanceSerializer

    def get(self, request, *args, **kwargs):
        participant1 = Participant.objects.get(id=request.GET.get('id1'))
        participant2 = Participant.objects.get(id=request.GET.get('id2'))
        coords1_str = participant1.location.split()
        coords2_str = participant2.location.split()
        coords1 = (float(float_normalize(coords1_str[0])), float(float_normalize(coords1_str[1])))
        coords2 = (float(float_normalize(coords2_str[0])), float(float_normalize(coords2_str[1])))
        distance = geo_distance(coords1, coords2)
        return Response(json.dumps({"message": str(distance)}), status=200)
