from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def search(request):
    return render(request, "search.html")

def filter(request):
    return render(request, "filter.html")

def latest(request):
    return render(request, "latest-news.html")

def add_item(request):
    return render(request, "add-item.html")

def top(request):
    return render(request, "top.html")
def edit(request):
    return render(request, "edit.html")