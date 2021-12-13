from django.shortcuts import render
from .models import Rubric


def test2(request):
    return render(request, "testapp/test2.html", {'rubrics': Rubric.objects.all()})


def get_rubric(request):
    pass