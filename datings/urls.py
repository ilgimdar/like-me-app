from django.urls import path

from datings.views import CreateUserView, MatchView, ParticipantList, DistanceView

urlpatterns = [
    path('clients/create', CreateUserView.as_view(), name="create_profile"),
    path('clients/match', MatchView.as_view(), name="match_view"),
    path('list', ParticipantList.as_view(), name="participant_list"),
    path('distance', DistanceView.as_view(), name="distance_view"),
]
