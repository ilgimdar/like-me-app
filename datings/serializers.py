from rest_framework import serializers

from datings.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        #Необходимые для регистрации поля
        fields = ('username', 'password', 'avatar', 'gender', 'email', 'name')
