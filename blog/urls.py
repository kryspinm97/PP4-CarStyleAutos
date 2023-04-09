from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("car_gallery/", views.CarGallery.as_view(), name="cargallery"),
    path("account/login/", views.LoginView.as_view(), name="login"),
    path("account/register/", views.RegisterView.as_view(), name="register"),
    path("account/logout/", views.LogoutView.as_view(), name="logout"),
    path("addpost_form", views.AddPost.as_view(), name="addpost"),
    path("car/<slug:slug>/", views.ViewCarPost.as_view(), name="view_car_post"),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('like-car-post/<int:car_id>/', views.like_car_post, name='like_car_post'),
    path('delete-comment/<int:comment_id>/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('user-posts/<str:username>/', views.UserPostsListView.as_view(), name='user_posts'),
    path('edit-post/<slug:slug>/', views.edit_car_post, name='edit_post'),
    path('cars/<slug:slug>/delete/', views.DeleteCarView.as_view(), name='delete_car'),
]
