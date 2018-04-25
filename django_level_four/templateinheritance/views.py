from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'templateinheritance/index.html')

def page1(request):
    return render(request, 'templateinheritance/page1.html')

def page2(request):
    return render(request, 'templateinheritance/page2.html')
