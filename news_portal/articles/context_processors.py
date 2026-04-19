from articles.models import Category


def navbar_context(request):
    """Context processor to provide categories for navbar"""
    return {
        'categories': Category.objects.all()
    }
