from django.shortcuts import render, redirect
from .indeedScript import parseIndeed
# Create your views here.
def index(request):
    return render(request,"index.html")
def refineSearch(request):
    myUrl  = request.POST['url']
    response = parseIndeed(myUrl)
    if response['error_message']:
        return redirect('/')
    else:
        context = {
            'results': response['results'],
            'original': response['original'],
            'new': response['newLen']
        }
        return render(request,'results.html', context)
