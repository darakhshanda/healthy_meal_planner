from django.shortcuts import render
from django.views import generic
from .models import Post
from django.http import HttpResponse

# Create your views here.


class RecipeList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "post_list.html"


def main_page(request):
    return HttpResponse("Welcome to the Healthy Meal Planner!")
