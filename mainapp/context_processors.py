from .models import Document
from .models import Profile, Chunk, Service
from .forms import ProfileImportForm, OrderForm
import random

def random_documents(request):
    all_documents = Document.objects.all()
    if len(all_documents) > 2:
        all_document_pks = [doc.pk for doc in all_documents]
        documents = [Document.objects.get(pk=random.choice(all_document_pks)) for i in range(0, 3)]
        return {'random_documents': documents}
    else:
        return {'random_documents': ['Нет документов в базе данных']}

def profile_chunks(request):
    profile = Profile.objects.first()
    return {'profile': profile}

def services(request):
    all_services = Service.objects.all().order_by('number')
    return {'all_services': all_services}

def profile_import(request):
    profile_import_form = ProfileImportForm()
    return {'profile_import_form': profile_import_form}

def order_form(request):
    order_form = OrderForm()
    return {'order_form': order_form}