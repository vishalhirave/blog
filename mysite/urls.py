from django.urls import path
from . import views

app_name='mysite'

urlpatterns = [
    path('',views.home,name='home'),
    path('registration', views.registration,name='registration'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('PostCreate',views.PostCreateView.as_view(),name='PostCreate'),
    path('PostListView', views.PostListView.as_view(), name='PostList'),
    path('PostDetail/<int:pk>',views.PostDetailView.as_view(),name='PostDetail'),
    path('PostEdit/<int:pk>', views.PostEditView.as_view(), name='PostEdit'),
    path('PostDelete/<int:pk>', views.PostDeleteView.as_view(), name='PostDelete'),
]