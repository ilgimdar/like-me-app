from django.urls import path

from datings.views import CreateUserView

urlpatterns = [
    path('clients/create', CreateUserView.as_view(), name="create-profile"),
]
