from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
import datetime
from django.core.paginator import Paginator

posts = Postovi.objects.all().order_by("-date")

def index(request):
    global posts
    if request.method == "POST":
        if 'new' in request.POST: #sorting by submit time (newest)
            posts = Postovi.objects.all().order_by("-date")
        elif 'top' in request.POST: #sorting by highest voted
            posts = Postovi.objects.all().order_by("-vote_score")
        elif 'old' in request.POST:  #sorting by submit time (oldest)
            posts = Postovi.objects.all().order_by("date")

        # Paginator for 10 posts per page
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        usercu = request.user.id  #tcurrently logged in user id
        return render(request, "network/index.html",{
            "posts" : posts,
            'page_obj': page_obj,
            "usercu": usercu,
            "page_number": page_number,
})
    else:
        # Sorting posts by newests
        #postovi = Postovi.objects.all().order_by("-date")

        # Paginator for 10 posts per page
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        usercu = request.user.id
        return render(request, "network/index.html",{
            "postovi" : posts,
            'page_obj': page_obj,
            "usercu": usercu,
            "page_number": page_number
        })


def login_view(request):
    if request.method == "POST":

        # Logging
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Auth check
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("reddit:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("reddit:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Password check
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Creating new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("reddit:index"))
    else:
        return render(request, "network/register.html")
@login_required(login_url='/login')
def profile(request, korisnikp_id):

    # Logic for following a user
    if request.method == "POST" and request.POST.get("dugmeu") == "Follow / Unfollow":
        user = User.objects.get(username=request.user)
        if not user.pratioci.filter(kogaprate= korisnikp_id) and user.pratioci.filter(kogaprate= korisnikp_id) != request.user.id : #provera da li ulogovani user vec prati datog usera na cijem je profilu i uslov da ne bi mogao da yaprati sam sebe
            fol = Follow4Follow()
            fol.pratioci = User.objects.get(username=request.user)
            fol.kogaprate = User.objects.get(id= korisnikp_id)
            fol.save()
        else:
            user.pratioci.filter(kogaprate= korisnikp_id).delete()

    # Profil of the user with his subbmited posts via GET method
    usercu = request.user.id
    postoviusera = Postovi.objects.filter(userid_id = korisnikp_id).order_by("-id")
    usercr = korisnikp_id
    sumfollowers = Follow4Follow.objects.filter(kogaprate_id = korisnikp_id).count()
    sumfollowing = Follow4Follow.objects.filter(pratioci_id = korisnikp_id).count()
    return render(request, "network/user.html",{
        "postoviusera": postoviusera,
        "usercu" : usercu,
        "usercr" : usercr,
        "sumfollowers": sumfollowers,
        "sumfollowing" : sumfollowing,
    })
@login_required(login_url='/login')
def following(request):
    user = request.user.id
    ids_following= []
    usersf = Follow4Follow.objects.filter(pratioci_id=user).values()
    for i in usersf:
        ids_following.append(i["kogaprate_id"])
    ids_following = tuple(ids_following)
    posts = Postovi.objects.filter(userid_id__in=ids_following)
    return render(request, "network/following.html",{
        "posts" : posts
    })

@login_required(login_url='/login')
def voting(request,postid):
    # Logic for upvote and downvote using django-vote
    user = request.user.id
    if request.method == "POST":
        vote = Postovi.objects.get(id = postid)
        if 'upvote' in request.POST:
            vote.votes.up(user)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

            return HttpResponseRedirect(reverse("reddit:index"))
        if 'downvote' in request.POST:
            vote.votes.down(user)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
            #return HttpResponseRedirect(reverse("reddit:index"))

# Editing post
@login_required(login_url='/login')
def edit(request,pid):
    userid = request.user.id
    orig_userid = Postovi.objects.get(id=pid)
    if userid == orig_userid.userid_id:
        if request.method == "POST" and request.POST.get("edit"):
            editedpost =request.POST.get("edit")
            post_for_edit = Postovi.objects.get(id=pid)
            post_for_edit.post1 =editedpost
            post_for_edit.title = request.POST.get("titl")
            post_for_edit.save()
            return HttpResponseRedirect(reverse("reddit:index"))
        else:
            post1 = Postovi.objects.get(id=pid)
            return render(request, "network/edit.html",{
                "post1" : post1,

            })
    else:
         return HttpResponseRedirect(reverse("reddit:index"))

# Logic for creating a new post
@login_required(login_url='/login')
def npost(request):
    if request.method == "POST" and request.POST.get("dugme") == "Send post":
            post = Newpost1(request.POST)
            if post.is_valid():
                new_post = Postovi(likes = 0,username = request.user, userid = User.objects.get(username=request.user),title =post.cleaned_data["title"], post1 =post.cleaned_data["post1"], date=datetime.datetime.now(),)
                new_post.save()
            return HttpResponseRedirect(reverse("reddit:index"))
    else:
        post1 = Newpost1()
        return render(request, "network/npost.html", {
            'post1':post1,
        })


# Single post diplay
def post(request, postid):
    post = Postovi.objects.get(pk=postid)
    usercu = request.user.id
    comments= Komentar.objects.filter(post = postid, parent_id=None)
    replies= Komentar.objects.filter(post =postid).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent_id not in replyDict.keys():
            replyDict[reply.parent_id]=[reply]
        else:
            replyDict[reply.parent_id].append(reply)
    commentform = CommentForm()
    return render(request, "network/post.html",{
        "post":post,
        "usercu":usercu,
        "comments": comments,
        "replies" : replyDict,
        "commentform": commentform,
    })

# Adding a comment
@login_required(login_url='/login')
def comment(request,postid):
    post = CommentForm(request.POST)
    if post.is_valid():
        parent = request.POST.get('Parent')
        if parent == "":
            print(post.cleaned_data["comment"])
            newcomment= Komentar(post = Postovi.objects.get(id=postid),user = request.user, comment = post.cleaned_data["comment"])
            newcomment.save()
            return HttpResponseRedirect(reverse(viewname='reddit:post', args=(postid)))
        else:
            print(post.cleaned_data["comment"])
            newcomment= Komentar(post = Postovi.objects.get(id=postid),user = request.user,parent_id = parent, comment = post.cleaned_data["comment"])
            newcomment.save()
            next = request.POST.get('', '/')
            return HttpResponseRedirect(reverse(viewname='reddit:post', args=(postid,)))
    else:
        return HttpResponseRedirect(reverse("reddit:index"))


# Search logic
@login_required(login_url='/login')
def search(request):
    sta_se_trazi=request.GET.get('q')
    result = Postovi.objects.filter(title__icontains=sta_se_trazi)
    paginator = Paginator(result, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    usercu = request.user.id
    return render(request,"network/index.html",{
        "post" : result,
        'page_obj': page_obj,
        "usercu": usercu,
        "page_number": page_number,
    })
