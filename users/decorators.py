from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def groups_required(*group_names):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if any(request.user.groups.filter(name=group_name).exists() for group_name in group_names):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator