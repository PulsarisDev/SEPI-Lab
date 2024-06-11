from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item, List

def home_page(request: HttpRequest):
    return render(request, 'home.html')

def view_list(request: HttpRequest, list_id: str):
    list_user = List.objects.get(id = list_id)
    return render(request, 'list.html', {'list': list_user})

def new_list(request: HttpRequest):
    list_user = List.objects.create()
    Item.objects.create(text = request.POST['item_text'], list = list_user)
    return redirect(f'/lists/{list_user.id}/')

def add_item(request: HttpRequest, list_id: str):
    list_user = List.objects.get(id = list_id)
    Item.objects.create(text = request.POST['item_text'], list = list_user)
    return redirect(f'/lists/{list_user.id}/')
