from django.shortcuts import (
    render,
    redirect)

from django.http import (
    HttpResponseServerError)

from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout)

from django.views.decorators.csrf import csrf_exempt

from .forms import (
    MobileForm,
    NonceForm)

from .utils import sendcode


@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = MobileForm(request.POST)
        if form.is_valid():
            mobile = request.POST['mobile']
            nonce_return = sendcode(mobile)
            request.session['nonce'] = nonce_return['nonce']
            request.session['mobile'] = nonce_return['mobile']
            request.session['count'] = 0
            return redirect('enternonce')
    else:
        form = MobileForm()
    return render(request, 'login.html', {'form': form})


@csrf_exempt
def enternonce(request):
    if request.method == 'POST':
        form = NonceForm(request.POST)
        if form.is_valid():
            mobile = request.session['mobile']
            nonce = request.session['nonce']
            code = form.cleaned_data['code']
            match = (str(code) == str(nonce))
            if request.session['count'] < 3:
                if match:
                    user = authenticate(mobile=mobile)
                    django_login(request, user)
                    return redirect('home')
                else:
                    request.session['count'] += 1
            else:
                request.session.flush()
                return redirect('login')
        else:
            return HttpResponseServerError("Form invalid")
    else:
        form = NonceForm()
    return render(request, 'nonce.html', {'form': form})


def logout(request):
    ''' simple function to logout user '''
    django_logout(request)
    return redirect('home')
