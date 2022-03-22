import json

from PIL import Image
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from mysite.settings import MEDIA_ROOT
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
            participant = Participant.objects.create(username=username, password=password, avatar=avatar, name=name,
                                                     email=email,
                                                     gender=gender)
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
            return HttpResponse(json.dumps({'message': 'User ' + username + ' registration successful'}), status=200)
        except Exception as e:
            return HttpResponse(json.dumps({'message': str(e)}), status=200)


def watermark_with_transparency(input_image_path,
                                output_image_path,
                                watermark_image_path,
                                position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    watermark.thumbnail(base_image.size)
    width, height = base_image.size

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent.save(output_image_path)


def jpg_to_png(img_url):
    return img_url.replace('.jpg', '.png')
