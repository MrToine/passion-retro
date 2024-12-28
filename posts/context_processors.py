from .models import Post
from users.decorators import groups_required

groups_required('Administrateur', 'SuperAdmin')
def pending_posts_count(request):
    count = Post.objects.filter(active=False).count()
    return {'pending_posts_count': count}