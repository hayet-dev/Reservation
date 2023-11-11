from django.urls import path
from .views import HomeTemplateView, AppTemplateView, ManageTemplateView

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('appointment/', AppTemplateView.as_view(), name='appointment'),
    path('manage-appointments/', ManageTemplateView.as_view(), name='manage'),
]