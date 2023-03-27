from django.urls import path

from accounts.views import like_post
from posts.views import IndexView, PostAddView, MainView, UserProfileView, create_comment

urlpatterns = [
    path("main/", IndexView.as_view(), name="index_page"),
    path('post/add/', PostAddView.as_view(), name="add_post"),
    path("", MainView.as_view(), name="main"),
    path('users/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('post/<int:post_pk>/comment/', create_comment, name='create_comment'),
    path('<int:post_pk>/like/', like_post, name='like'),

]
