from django.urls import path

from datings.views import CreateUserView, MatchView

urlpatterns = [
    path('clients/create', CreateUserView.as_view(), name="create-profile"),
    path('clients/match', MatchView.as_view(), name="match_view")
]
