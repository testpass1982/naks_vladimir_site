import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
# from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, PostPhoto, Tag, Category, Document, Article, Message, Contact
from .models import Registry, Menu, Service, Attestat
from .models import Staff, DocumentCategory, Profile
from .forms import PostForm, ArticleForm, DocumentForm, ProfileImportForm
from .forms import SendMessageForm, SubscribeForm, AskQuestionForm, DocumentSearchForm, SearchRegistryForm
from .adapters import MessageModelAdapter
from .message_tracker import MessageTracker
from .utilites import UrlMaker
from .registry_import import Importer, data_url
# from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


# Create your views here.
from django.conf import settings
from .utilites import update_from_dict

def import_profile(request):
    content = {}
    if request.method == "POST":
        if len(request.FILES) > 0:
            form = ProfileImportForm(request.POST, request.FILES)
            if form.is_valid():
                data = request.FILES.get('file')
                file = data.readlines()
                import_data = {}
                for line in file:
                    string = line.decode('utf-8')
                    if string.startswith('#') or string.startswith('\n'):
                        print('Пропускаем: ', string)
                        continue
                    splitted = string.split("::")
                    import_data.update({splitted[0].strip(): splitted[1].strip()})
                    print('Импортируем:', string)
                profile = Profile.objects.first()
                if profile is None:
                    profile = Profile.objects.create(org_short_name="DEMO")
                try:
                    #updating existing record with imported fields
                    update_from_dict(profile, import_data)
                    content.update({'profile_dict': '{}'.format(profile.__dict__)})
                    content.update({'profile': profile})
                    print('***imported***')
                except Exception as e:
                    print("***ERRORS***", e)
                    content.update({'errors': e})
        else:
            content.update({'errors': 'Файл для загрузки не выбран'})
        return render(request, 'mainapp/includes/profile_load.html', content)

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
        publish_on_main_page=True).order_by('-published_date')[:3]

    content = {
        'title': title,
        # 'pictured_posts': pictured_posts,
        'posts': main_page_news,
        # 'articles': main_page_articles,
        # 'docs': main_page_documents,
        'send_message_form': SendMessageForm(),
        'subscribe_form': SubscribeForm(),
        'ask_question_form': AskQuestionForm(),
    }
    return render(request, 'mainapp/index.html', content)

def svarshik(request):
    return render(request, 'mainapp/svarshik.html')
def contacti(request):
    return render(request, 'mainapp/contacti.html')

def news(request):
    """this is the news view"""
    title = "Новости АЦ"
    all_news = Post.objects.all().filter(
        publish_on_news_page=True).order_by('-created_date')
    # all_documents = Document.objects.all().order_by('-created_date')[:5]
    # side_posts = Post.objects.all().order_by('-created_date')[:4]
    # post_list = [dict({'post': post, 'picture': PostPhoto.objects.filter(
    #     post__pk=post.pk).first()}) for post in all_news]
    # показываем несколько новостей на странице
    # print(post_list)
    # import pdb; pdb.set_trace()
    paginator = Paginator(all_news, 8)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    # articles = Article.objects.all().order_by('-created_date')[:3]

    # print(request.resolver_match)
    # print(request.resolver_match.url_name)
    print(posts)
    # import pdb; pdb.set_trace()
    content = {
        'title': title,
        'news': posts,
        # 'documents': all_documents,
        # 'side_posts': side_posts,
        # 'bottom_related': articles
    }
    return render(request, 'mainapp/all_news.html', content)

def contact(request):
    contacts = Contact.objects.all().order_by('number')

    content = {
        'title': 'Контакты',
        'contacts': contacts,
    }

    return render(request, 'mainapp/contacti.html', content)

def doc(request):
    """view for documents page"""

    content = {
        'title': 'Документы',
        'documents': Document.objects.all().order_by('number'),
        'categories': DocumentCategory.objects.all().order_by('number'),
        'services': Service.objects.all().order_by('number'),
    }

    return render(request, 'mainapp/doc.html', content)

def center(request):
    #TODO test a todo creation - page about us
    content = {
        'title': 'О центре',
        'attestats': Attestat.objects.all().order_by('number')
    }
    return render(request, 'mainapp/center.html', content)

def all_news(request):
    return render(request, 'mainapp/all_news.html')

def reestr(request):
    return render(request, 'mainapp/reestr.html')

def profstandarti(request):
    return render(request, 'mainapp/profstandarti.html')

def details(request, pk):
    print(request.resolver_match)
    print(request.resolver_match.url_name)
    return_link = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    obj = get_object_or_404(Post, pk=pk)
    print(obj)
    common_content = {'title': obj.title}
    attached_images = PostPhoto.objects.filter(post__pk=pk)
    attached_documents = Document.objects.filter(post__pk=pk)
    # import pdb; pdb.set_trace()
    side_related = Post.objects.filter(publish_on_news_page=True).exclude(
                id=pk).order_by('-published_date')[:4]
    # side_related = Document.objects.all().order_by('-created_date')[:3]
    # side_related_posts = [dict({'post': post, 'picture': PostPhoto.objects.filter(
    #     post__pk=post.pk).first()}) for post in side_related]
    post_content = {
        'post': obj,
        'images': attached_images,
        'documents': attached_documents,
        'side_related': side_related,
        # 'bottom_related': Article.objects.all().order_by(
            # '-created_date')[:3]
    }
    return render(request, 'mainapp/post_details.html', post_content)

def service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    content = {
        'title': 'Описание услуги',
        'service': service,
        'other_services': Service.objects.all().exclude(pk=service.pk).order_by('number')
    }
    return render(request, 'mainapp/service_template.html', content)
