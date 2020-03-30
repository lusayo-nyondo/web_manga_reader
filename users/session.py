from users.models import SiteUser

# All logic that goes into establishing, verifying
# and authenticating a user session should go here.

def get_authenticated_user(request):
    try:
        if request.user.is_authenticated:
            return request.user
        else:
            return None
    except AttributeError:
        return None
    
    return None

def attach_active_user_to_context(context, request):
    user = get_authenticated_user(request)
    
    context["site_user"] = user

    return context
