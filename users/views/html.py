from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import loader, redirect

from users.models import SiteUser

from users import session as user_session

# Create your views here.

def index(request):
    return account_view(request)

def privacy_policy(request):
    template = loader.get_template('users/legal/privacy_policy.dtl.html')
    context = {}
    
    return HttpResponse(template.render(context, request))

def sign_in_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    url = request.path
    
    for key in request.GET.keys():
        url += '?{0}='.format(key)
        url += '{0}&'.format(request.GET.get(key))

    url = url[:-1]
    
    if username and password:
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                next = request.POST.get('next')

                if next:
                    return redirect(next)
                else:
                    raise KeyError('next is not defined')

            except KeyError:                
                return redirect('/manga_list')
        else:
            context = {
                'authentication_status': 'login_failed',
                'authentication_message_context': 'warning',
                'authentication_description': 'Either the username or the password was incorrect.',
            }
    else:
        context = {}

    template = loader.get_template('users/modules/sign_in.dtl.html')
    return HttpResponse(template.render(context, request))

def register_view(request):
    user_email = request.POST.get('user_email')
    user_password = request.POST.get('user_password')
    user_firstname = request.POST.get('user_firstname')
    user_lastname = request.POST.get('user_lastname')
    user_alias = request.POST.get('user_alias')

    template = loader.get_template('users/modules/register.dtl.html')
    
    context = None

    if user_email and user_password and user_firstname and user_lastname:     
        try:
            user = SiteUser.objects.get(email=user_email)
            user = SiteUser.objects.get(alias=user_alias)

            context = {
                'authentication_status':'register_failed',
                'authentication_description':'The email or alias provided is already registered to another account.',
                'user': user,
            }

            return HttpResponse(template.render(context, request))

        except SiteUser.DoesNotExist:
            user = SiteUser.objects.create(
                email=user_email,
                first_name=user_firstname,
                last_name=user_lastname,
                username=user_alias,
            )

            user.set_password(user_password)

            user.save()

            context = {
                'authentication_status': 'register_successful',
                'authentication_description': 'The new user has been created',
                'user': user,
            }

            return redirect_authenticated_user(request, context)

    return HttpResponse(template.render(context, request))

def redirect_authenticated_user(request, context):
    user = context['user']
    
    request.session['user_authenticated'] = True
    request.session['user_id'] = user.id
    request.session['authentication_status'] = context['authentication_status']
    request.session['authentication_description'] = context['authentication_description']

    referrer = request.META.get('HTTP_REFERER')
    response = None

    #if referrer:
    #    response = redirect(referer)
    #else:
    #    response = redirect('/')

    redirection_url = '/'
    response = redirect(redirection_url)
    
    return response

@login_required
def account_view(request):
    template = loader.get_template('users/modules/profile.dtl.html')

    user = user_session.get_authenticated_user(request)

    context = {
        'user': user,
    }

    return HttpResponse(template.render(context, request))

@login_required
def logout_view(request):
    logout(request)

    return redirect('/account/sign_in')

