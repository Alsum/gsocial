import re
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from mysocial.forms import RegistrationForm, LoginForm
from mysocial.models import EmailConfirmed

SHA1_RE = re.compile('^[a-f0-9]{40}$')


def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    messages.success(request, "<strong>Successfully Logged out</strong>. Feel free to <a href='%s'>login</a> again." % (
        reverse("mysocial:login")), extra_tags='safe, abc')
    return HttpResponseRedirect('%s' % (reverse("mysocial:login")))


def login_view(request):
    form = LoginForm(request.POST or None)
    btn = "Login"
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Successfully Logged In. Welcome Back!")
        return HttpResponseRedirect("/")
    context = {
        "form": form,
        "submit_btn": btn,
    }
    return render(request, "login_form.html", context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    btn = "Join"
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()
        messages.success(request, "Successfully Registered. Please confirm your email now.")
        return HttpResponseRedirect("/")
    # username = form.cleaned_data['username']
    # password = form.cleaned_data['password']
    # user = authenticate(username=username, password=password)
    # login(request, user)

    context = {
        "form": form,
        "submit_btn": btn,
    }
    return render(request, "form.html", context)


def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.success(request, "There was an error with your request.")
            return HttpResponseRedirect("/")
        if instance is not None and not instance.confirmed:
            page_message = "Confirmation Successful! Welcome."
            instance.confirmed = True
            user = User.objects.get(id=instance.user_id)
            user.is_active = True
            user.save()
            instance.activation_key = "Confirmed"
            instance.save()
            messages.success(request, "Successfully Confirmed! Please login.")
        elif instance is not None and instance.confirmed:
            page_message = "Already Confirmed"
            messages.success(request, "Already Confirmed.")
        else:
            page_message = ""

        context = {"page_message": page_message}
        return render(request, "registration/activation_complete.html", context)
    else:
        raise Http404
