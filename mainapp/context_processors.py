from .models import Document
import random

def random_documents(request):
    all_documents = Document.objects.all()
    all_document_pks = [doc.pk for doc in all_documents]
    documents = [Document.objects.get(pk=random.choice(all_document_pks)) for i in range(0, 3)]
    return {'random_documents': documents}