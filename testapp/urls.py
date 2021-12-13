from django.urls import path, include
from .views import *

urlpatterns = [
    path('', test2, name='test'),
    path('rubric/<int:pk>', get_rubric, name='rubric'),
]
