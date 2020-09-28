from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm, ShopUserLoginForm
from authapp.models import ShopUser
from authapp.forms import ShopUserProfileEditForm


def register(request):
    title = 'регистрация'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            new_user = register_form.save()
            if send_verify_mail(new_user):
                print('сообщение подтверждения отправлено')
                context = {
                    'verif_message': 'Вам на почту направлена ссылка с кодом подтверждения регистрации'
                }
                return render(request, 'authapp/register.html', context)
                #return HttpResponseRedirect(reverse('index'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))
            #auth.login(request, new_user)
            #return HttpResponseRedirect(reverse('index'))
    else:
        register_form = ShopUserRegisterForm()

    context = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', context)


def login(request):
    title = 'вход'

    next = request.GET['next'] if 'next' in request.GET.keys() else None

    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    context = {'title': title, 'login_form': login_form, 'next': next}
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, request.FILES, instance=request.user.shopuserprofile)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    context = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form}

    return render(request, 'authapp/edit.html', context)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', kwargs={
        'email': user.email,
        'activation_key': user.activation_key,
    })

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and user.is_activation_key_valid():
            user.is_active = True
            user.save()
            auth.login(request, user)
        else:
            print(f'error activation user: {user}')
        return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))



# Create your views here.
