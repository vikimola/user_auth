from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
# Create your views here.
from django.urls import reverse
from django.views import View

# class DumpPython(View):
#     def get(self, request):
#         resp = "<pre>\n User data in python:\n\n"
#         resp += "Login url: " + reverse("log_in") + "\n"
#         resp += "Logout url: " + reverse("log_out") + "\n\n"
#         return resp
#
# def log_in(request):
#     pass
#
#
# def log_out(request):
#     pass

# Use authenticate() to verify a set of credentials.
# It takes credentials as keyword arguments, username and password
# for the default case, checks them against each authentication
# backend, and returns a User object if the credentials are valid
# for a backend. If the credentials aren’t valid for any backend
# or if a backend raises PermissionDenied, it returns None.
from .models import Cat

user = authenticate(username="admin", password="lucykutya2")

if user is not None:
    print("YAAS")
else:
    print("F")


# Assuming you have an application with an
# app_label foo and a model named Bar,
# to test for basic permissions you should use:
#
# add: user.has_perm('foo.add_bar')
# change: user.has_perm('foo.change_bar')
# delete: user.has_perm('foo.delete_bar')
# view: user.has_perm('foo.view_bar')

def user_gains_perm(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # any permission check will cache the current set of permissions
    print(user)
    user.has_perm('dj_auth.change_cat')

    content_type = ContentType.objects.get_for_model(Cat)
    permission = Permission.objects.get(
        codename="change_cat",
        content_type=content_type,
    )

    user.user_permissions.add(permission)

    # Checking the cached permission set
    user.has_perm('dj_auth.change_cat')  # False

    # Request new instance of User
    # Be aware that user.refresh_from_db() won't clear the cache.
    user = get_object_or_404(User, pk=user_id)

    # Permission cache is repopulated from the database
    user.has_perm('dj_auth.change_cat')  # True
    return HttpResponse("Hello")


def log_in(request):
    if request.method == "POST":
        name = request.POST["name"]
        password = request.POST["password"]

        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.add_message(request, messages.INFO, 'Invalid credentials.')
            return HttpResponseRedirect(reverse("home"))
            # using reverse to not hardcode the url
            # szimpla redirect() jobb, szebb


def log_out(request):
    logout(request)
    # the session data for the current request is completely cleaned out.
    return redirect("home")


def home(request):
    message = []
    storage = get_messages(request)
    for mesage in storage:
        message.append(mesage)
    return render(request, 'dj_auth/templates/dj_auth/home.html', {"message": message})


def user_profile(request, user_id):
    if not request.user.is_authenticated:
        return redirect("home")
    else:
        user = User.objects.get(id=user_id)
        return render(request, 'dj_auth/templates/dj_auth/user_profile.html')


@login_required(login_url="home")
def user_profile2(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'dj_auth/templates/dj_auth/user_profile.html')
    # If the user isn’t logged in, redirect to settings.LOGIN_URL
    # (alapjaraton /accounts/login/, most atirva "home"-ra),
    # passing the current absolute path in the query string.
    # Example: /accounts/login/?next=/polls/3/.
    # By default, the path that the user should be redirected
    # to upon successful authentication is stored in a
    # query string parameter called "next" -> change 'next' w/ redirect_field_name
    # login_required() also takes an optional login_url parameter


# LoginRequiredMixin
class MyView(LoginRequiredMixin, View):
    login_url = "home"
    # redirect_field_name = "redirect_to"

    def get(self, request):
        return render(request, 'dj_auth/templates/dj_auth/user_profile.html')


# Limiting access to logged-in users that pass a test
def my_view(request):
    if not request.user.username.endswith("l"):
        return redirect("home")
    return render(request, 'dj_auth/templates/dj_auth/user_profile.html')


def username_check(user):
    return user.username.endswith("l")


@user_passes_test(username_check, login_url="home")
def my_view2(request):
    return render(request, 'dj_auth/templates/dj_auth/user_profile.html')


# UserPassesTestMixin
class MyView2(UserPassesTestMixin, View):
    login_url = "home"

    def test_func(self):
        return self.request.user.username.endswith('l')


@login_required(login_url="home")  # -> we can combo it
@permission_required('dj_auth.change_cat', login_url="home")
def perm(request):
    return render(request, 'dj_auth/templates/dj_auth/user_profile.html')


# PermissionRequiredMixin
class perm2(PermissionRequiredMixin, View):
    login_url = "home"
    permission_required = 'dj_auth.change_cat'

    # or multiple permissions:
    # permission_required=('dj_auth.add_cat',  'dj_auth.change_cat')
    def get(self, request):
        return render(request, 'dj_auth/templates/dj_auth/user_profile.html')


# idek
def pw_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("home")

    else:
        return redirect("home")
