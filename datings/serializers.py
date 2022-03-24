from django_filters import rest_framework as filters
from rest_framework import serializers

from datings.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        # Необходимые для регистрации поля
        fields = ('username', 'password', 'avatar', 'gender', 'email', 'name', 'location')


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('from_id', 'to_id')


class ParticipantFilter(filters.FilterSet):
    gender = filters.BaseInFilter(lookup_expr='in')
    name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Participant
        # Поля для фильтрации
        fields = ('gender', 'name')


class DistanceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id1', 'id2')
