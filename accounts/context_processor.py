from accounts.models import User

def new_users_count(request):
    """ Reurn count of new users """
    return {'new_users_count' : User.objects.filter(is_active=False, groups__isnull=True).count()}
