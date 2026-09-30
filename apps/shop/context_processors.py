from .models import Category

def categories(request):
    return {
        'categories': Category.objects.filter(parent=None, is_active=True)
    }