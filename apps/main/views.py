from django.shortcuts import render, redirect
from .indeedScript import parseIndeed
# Create your views here.
def index(request):
    return render(request,"index.html")
def refineSearch(request):
    myUrl = request.POST['url']
    myResults= parseIndeed(myUrl)
    context = {
        'results': myResults[0],
        'original': myResults[1],
        'new': myResults[2]
    }
    return render(request,'results.html', context)
