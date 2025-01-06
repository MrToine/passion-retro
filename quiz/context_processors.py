from .models import Quiz
from users.decorators import groups_required

groups_required('Administrateur', 'SuperAdmin')
def pending_quizes_count(request):
    count = Quiz.objects.filter(is_active=False).count()
    return {'pending_quizes_count': count}