from django.shortcuts import (
    render,
    redirect)

from django.http import (
    HttpResponseServerError,
    HttpResponseRedirect)

from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout)

from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from .forms import AuthRequestForm, AuthResponseForm

from .utils import sendcode


@csrf_exempt
def nonce_request(
        request,
        template_name='registration/authrequest.html',
        auth_request_form=AuthRequestForm):

    form = auth_request_form(data=request.POST or None)
    if form.is_valid():
        mobile = request.POST['mobile']
        nonce_return = sendcode(mobile)
        request.session['nonce'] = nonce_return['nonce']
        request.session['mobile'] = nonce_return['mobile']
        request.session['count'] = 0
        return redirect('nonce_response')
    return render(request, template_name, {'form': form})


@csrf_exempt
def nonce_resposne(
        request,
        template_name='registration/authresponse.html',
        auth_response_form=AuthResponseForm):

    form = auth_response_form(data=request.POST or None)
    if form.is_valid():
        mobile = request.session['mobile']
        nonce = request.session['nonce']
        code = form.cleaned_data['code']
        match = (str(code) == str(nonce))
        if request.session['count'] < 3:
            if match:
                user = authenticate(mobile=mobile)
                django_login(request, user)
                return HttpResponseRedirect(redirect('home'))
            else:
                request.session['count'] += 1
        else:
            request.session.flush()
            return redirect('login')
    return render(request, template_name, {'form': form})
