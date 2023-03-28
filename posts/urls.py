from django.urls import path

from accounts.views import like_post, ProfileView
from posts.views import IndexView, PostAddView, MainView, create_comment

urlpatterns = [
    path("main/", IndexView.as_view(), name="index_page"),
    path('post/add/', PostAddView.as_view(), name="add_post"),
    path("", MainView.as_view(), name="main"),
    path('post/<int:post_pk>/comment/', create_comment, name='create_comment'),
    path('<int:post_pk>/like/', like_post, name='like'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),


]
