
from django.urls import path

from . import views

app_name = 'reddit'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:korisnikp_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("edit/<int:pid>", views.edit, name="edit"),
    path("npost", views.npost, name="npost"),
    path("voting/<int:postid>/", views.voting, name="voting"),
    path("post/<int:postid>", views.post, name="post"),
    path("comment/<int:postid>", views.comment, name="comment"),
    path("search",views.search, name="search"),
    #path("commentvoting/<int:postid>", views.commentvoting, name="commentvoting"),
]
