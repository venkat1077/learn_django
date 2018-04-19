from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'relativeurl/index.html')

def page1(request):
    return render(request, 'relativeurl/page1.html')

def page2(request):
    return render(request, 'relativeurl/page2.html')
