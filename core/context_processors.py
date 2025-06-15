from .views import is_admin, is_user

def user_roles(request):
    return {
        'is_admin': is_admin(request.user) if request.user.is_authenticated else False,
        'is_user': is_user(request.user) if request.user.is_authenticated else False,
    }
