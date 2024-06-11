from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item, List

def home_page(request: HttpRequest):
    return render(request, 'home.html')

def view_list(request: HttpRequest):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request: HttpRequest):
    list_user = List.objects.create()
    Item.objects.create(text = request.POST['item_text'], list = list_user)
    return redirect('/lists/the-new-page/')
