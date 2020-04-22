from accounts.models import User

def new_users_count(request):
    """ Reurn count of new users """
    return {'new_users_count' : User.objects.filter(is_registered=False).count()}
