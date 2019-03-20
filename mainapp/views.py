import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
# from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, PostPhoto, Tag, Category, Document, Article, Message, Contact
from .models import Registry, Menu
from .models import Staff
from .forms import PostForm, ArticleForm, DocumentForm
from .forms import SendMessageForm, SubscribeForm, AskQuestionForm, DocumentSearchForm, SearchRegistryForm
from .adapters import MessageModelAdapter
from .message_tracker import MessageTracker
from .utilites import UrlMaker
from .registry_import import Importer, data_url
# Create your views here.
def index(request):

    """this is mainpage view with forms handler and adapter to messages"""
    title = "Главная - АЦ Владимир"
    tracker = MessageTracker()
    if request.method == 'POST':
        request_to_dict = dict(zip(request.POST.keys(), request.POST.values()))
        form_select = {
            'send_message_button': SendMessageForm,
            'subscribe_button': SubscribeForm,
            'ask_question': AskQuestionForm,
        }
        for key in form_select.keys():
            if key in request_to_dict:
                print('got you!', key)
                form_class = form_select[key]
        form = form_class(request_to_dict)
        if form.is_valid():

            # saving form data to messages (need to be cleaned in future)
            adapted_data = MessageModelAdapter(request_to_dict)
            adapted_data.save_to_message()
            print('adapted data saved to database')
            tracker.check_messages()
            tracker.notify_observers()
        else:
            raise ValidationError('form not valid')

    main_page_news = Post.objects.filter(
        publish_on_main_page=True).order_by('-published_date')[:2]

    not_pictured_posts = Post.objects.filter(
        secondery_main=True).order_by('-published_date')[:3]

    main_page_documents = Document.objects.filter(
        publish_on_main_page=True).order_by('-created_date')[:3]

    # main_page_secondery_news = Post.objects.filter(
    #     secondery_main=True).order_by('-published_date')[:4]
    pictured_posts = {}
    for post in main_page_news:
        pictured_posts[post] = PostPhoto.objects.filter(post__pk=post.pk).first()
    # print(pictured_posts)

    main_page_articles = Article.objects.filter(
        publish_on_main_page=True).order_by('-published_date')[:3]

    main_page_links = Menu.objects.all()

    # print(request.resolver_match)
    # print(request.resolver_match.url_name)

    content = {
        'title': title,
        'pictured_posts': pictured_posts,
        'not_pictured_posts': not_pictured_posts,
        'articles': main_page_articles,
        'docs': main_page_documents,
        'send_message_form': SendMessageForm(),
        'subscribe_form': SubscribeForm(),
        'ask_question_form': AskQuestionForm(),
    }

    return render(request, 'mainapp/index.html')

def svarshik(request):
    return render(request, 'mainapp/svarshik.html')

def news(request):
    """this is the news view"""
    title = "Новости АЦ"
    all_news = Post.objects.all().filter(
        publish_on_news_page=True).order_by('-created_date')
    # all_documents = Document.objects.all().order_by('-created_date')[:5]
    # side_posts = Post.objects.all().order_by('-created_date')[:4]
    post_list = [dict({'post': post, 'picture': PostPhoto.objects.filter(
        post__pk=post.pk).first()}) for post in all_news]
    # показываем несколько новостей на странице
    print(post_list)
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    # articles = Article.objects.all().order_by('-created_date')[:3]

    # print(request.resolver_match)
    # print(request.resolver_match.url_name)
    print(posts)
    content = {
        'title': title,
        'news': posts,
        # 'documents': all_documents,
        # 'side_posts': side_posts,
        # 'bottom_related': articles

    }
    return render(request, 'mainapp/news.html', content)

def contact(request):
    return render(request, 'mainapp/contacti.html')

def doc(request):
    documents = Document.objects.all()
    content = {
        'title': 'Documents',
        'docs': documents
    }
    return render(request, 'mainapp/doc.html', content)

def center(request):
    #TODO test a todo creation - page about us
    return render(request, 'mainapp/center.html')

def political(request):
    return render(request, 'mainapp/political.html')

def all_news(request):
    return render(request, 'mainapp/all_news.html')

def reestr(request):
    return render(request, 'mainapp/reestr.html')

def profstandard(request):
    return render(request, 'mainapp/profstandarti.html')

def svarproizvodstva(request):
    return render(request, 'mainapp/svarproizvodstva.html')

def details(request, content=None, pk=None):
    print(request.resolver_match)
    print(request.resolver_match.url_name)
    return_link = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.GET:
        content = request.GET.get('content_type')
        pk = request.GET.get('pk')

    content_select = {
        'post': Post,
        'article': Article
    }

    obj = get_object_or_404(content_select[content], pk=pk)
    print(obj)
    common_content = {'title': obj.title}
    if content == 'post':
        attached_images = PostPhoto.objects.filter(post__pk=pk)
        attached_documents = Document.objects.filter(post__pk=pk)

        # side_related = Post.objects.filter(publish_on_news_page=True).exclude(
        #     id=pk).order_by('-published_date')[:3]
        side_related = Document.objects.all().order_by('-created_date')[:3]
        # side_related_posts = [dict({'post': post, 'picture': PostPhoto.objects.filter(
        #     post__pk=post.pk).first()}) for post in side_related]
        post_content = {
            'post': obj,
            'images': attached_images,
            'documents': attached_documents,
            'side_related': side_related,
            'bottom_related': Article.objects.all().order_by(
                '-created_date')[:3]
        }
    return render(request, 'mainapp/news_two.html')

def atestatechonlogy(request):
    return render(request, 'mainapp/atestatechonlogy.html')

def atestatsvaroborud(request):
    return render(request, 'mainapp/atestatsvaroborud.html')
