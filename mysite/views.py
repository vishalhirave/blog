from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.urls import reverse_lazy


# registeration page handler
def registration(request):
    form = UserInfoForm
    register = False
    # check if method is post or get,id method is post then check for form validation and save that form if its valid
    if request.method == 'POST':
        form = UserInfoForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            register = True
    return render(request, 'registration.html', {'UserInfoForm': form, 'register': register})


# login function for checking username and password
def home(request):
    # if user is already logged in then redirect to list view
    if request.user.is_authenticated:
        return redirect('mysite:PostList')
    # if user is not already logged and method is post then check username and password of user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('mysite:PostList')
            else:
                return HttpResponse('Account not active')
        else:
            return HttpResponse('Wrong Credentials')
    return render(request, 'login.html')


# logout function,if user already logged then only user can log out,that why we need to use login_required decorator
@login_required
def user_logout(request):
    logout(request)
    return redirect('mysite:home')


# to create of new posts.user can create blogs only after logged in
class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = 'mysite:home'
    form_class = PostForm
    model = Post

    # below method is used because when any user post any post then author name of that blog should
    # automatically assigned to user who is currently logged in
    def form_valid(self, form):
        response = super(PostCreateView, self).form_valid(form)
        post = form.save(commit=False)
        current_user = self.request.user
        post.author_id = current_user.id
        post.save()
        return response


# detail view of blogs
class PostDetailView(LoginRequiredMixin, DetailView):
    # login_url is needed because if user is not logged in and user tries to hit url
    # then user will get redirected to login page
    login_url = 'mysite:home'
    model = Post


# below CBV will show list of all blogs
class PostListView(LoginRequiredMixin, ListView):
    login_url = 'mysite:home'
    model = Post

    # in order to show latest blogs first ,we have override below function
    def get_queryset(self):
        return Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')


# to edit already created blogs
class PostEditView(LoginRequiredMixin, UpdateView):
    login_url = 'mysite:home'
    form_class = PostForm
    model = Post


# to delete blogs
class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'mysite:home'
    model = Post
    # success url is needed for to wait till user gives confirmation for deleting blog
    success_url = reverse_lazy('mysite:PostList')
