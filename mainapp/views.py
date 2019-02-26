from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'mainapp/index.html')

def svarshik(request):
    return render(request, 'mainapp/svarshik.html')
    
def news(request):
    return render(request, 'mainapp/news.html')

def contacti(request):
    return render(request, 'mainapp/contacti.html')

def doc(request):
    return render(request, 'mainapp/doc.html')

def center(request):
    return render(request, 'mainapp/center.html')

def political(request):
    return render(request, 'mainapp/political.html')

def reestr(request):
    return render(request, 'mainapp/reestr.html')

def profstandarti(request):
    return render(request, 'mainapp/profstandarti.html')

def svarproizvodstva(request):
    return render(request, 'mainapp/svarproizvodstva.html')

def news_two(request):
    return render(request, 'mainapp/news_two.html')

def atestatetchnology(request):
    return render(request, 'mainapp/atestatetchnology.html')

def atestatsvaroborud(request):
    return render(request, 'mainapp/atestatsvaroborud.html')

def all_news(request):
    return render(request, 'mainapp/all_news.html')
