from django.urls import path
from . import views


urlpatterns = [
    path("", views.get_blog_list, name="index"),
    path('blogger/blogger/<int:blog_id>', views.blog, name="blog_by_id"),
    path('blogger/<int:post_id>', views.like, name="post_by_id"),
    path('login', views.log_in, name="login"),
    path('logout', views.log_out, name="logout"),
    path('signup', views.sign_up, name="signup"),
    path('<int:blog_id>/create_post_', views.create_post_, name="create_post_"),
    path('<int:blog_id>/edit_blog', views.edit_blog, name="edit_blog"),
    path('<int:blog_id>/list', views.list, name="list"),
    path('<int:comment_id>', views.complaint, name="complaint"),
]