from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Blog, Post, Comment, Like, View, Follow, Complaint
from .forms import LoginForm, RegistrationForm, PostForm, BlogEditForm


def log_out(request):
    logout(request)
    redirect_url = request.GET.get('next') or reverse('index')
    return redirect(redirect_url)


def log_in(request):
    if request.method == 'POST':
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET['next'])
            else:
                messages.error(request, 'username or password not correct')
                return redirect('login')
                # form.add_error('Invalid credentials!')
    else: # GET
        form = LoginForm()
    return render(request, 'blogger/login.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST,  request.FILES)
        if form.is_valid():
            logout(request)
            blog_title = form.cleaned_data['blog_title']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            avatar = form.cleaned_data['avatar']
            permission = form.cleaned_data['permission']
            bio = form.cleaned_data['bio']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'User already exists!')
            elif password != password_again:
                form.add_error('password_again', 'Passwords mismatch!')
            else:
                user = User.objects.create_user(username, email, password)
                if avatar: #and bio:
                    blog = Blog.objects.create(author=user, title=blog_title, avatar=avatar, permission=permission, bio=bio)
                elif bio:
                    blog = Blog.objects.create(author=user, title=blog_title, permission=permission, bio=bio)
                elif avatar:
                    blog = Blog.objects.create(author=user, title=blog_title, permission=permission, avatar=avatar)
                else:
                     blog = Blog.objects.create(author=user, permission=permission, title=blog_title)
                login(request, user)
                context = {'blog': blog, 'posts': []}
                return render(request, 'blogger/blog.html', context)
    else: # GET
        form = RegistrationForm()
    return render(request, 'blogger/signup.html', {'form': form})


def get_blog_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        blogs = Blog.objects.filter(title__icontains=search_query).order_by('-created_at')
    else:
        blogs = Blog.objects.order_by('-created_at')
    context = {'blogs': blogs}
    return render(request, 'blogger/index.html', context)


@login_required(login_url='/blogger/login')
def blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        return follow(request, blog_id)
    if blog.author_id != request.user.id:
        new_view, created = View.objects.get_or_create(viewer=request.user, blog_id=blog_id)
        if created:
            blog.views = blog.views + 1
            blog.save()

    return render_blog(request, blog_id)


def render_blog(request, blog_id, additional_context={}):
    blog = get_object_or_404(Blog, id=blog_id)
    comments=[]
    for post in blog.post_set.order_by('-created_at'):
        for comment in post.comment_set.order_by('-created_at'):
            comments.append(comment)
    if blog.author_id != request.user.id:
        if Follow.objects.filter(following=blog.author, follower=request.user).exists():
            context = {
                'blog': blog,
                'posts': blog.post_set.order_by('-created_at'),
                'comments': comments,
                'is_followed':True,
                **additional_context
            }
            return render(request, 'blogger/blog.html', context)
        else:
            context = {
                'blog': blog,
                'posts': blog.post_set.order_by('-created_at'),
                'comments': comments,
                'is_followed': False,
                **additional_context
            }
            return render(request, 'blogger/blog.html', context)
    else:
        context = {
            'blog': blog,
            'posts': blog.post_set.order_by('-created_at'),
            'comments': comments,
            **additional_context
        }
    return render(request, 'blogger/blog.html', context)


def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    comment_post = request.POST['comment_post']
    comment_post_error = None
    if not comment_post or comment_post.isspace():
        comment_post_error = 'Please provide non-empty comment!'

    if len(comment_post) > 300:
        comment_post_error='Please make comment shorter!'

    if comment_post_error:
        error_context = {
            'comment_post_error': comment_post_error,
            'comment_post': comment_post
        }
        return render_blog(request, post.blog.id, error_context)
    else:
        Comment(comment_post=comment_post, author=request.user, commented_image=post).save()
        return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': post.blog.id}))
        #return render(request, 'blogger/blog.html', {'blog': blog})


def create_post_(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        if blog.author_id != request.user.id:
            return HttpResponseForbidden('You are not allowed to post in this blog!')
        form = PostForm(request.POST, request.FILES) #, blog_id=blog.id)
        #form = PostForm(request.POST, request.FILES, blog_id=blog.id)
        if form.is_valid():
            # form.blog = blog
            post = form.save(commit=False)
            post.blog = blog
            post.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            # return render(request, 'blogger/create_post_.html', {'form': form, 'img_obj': img_obj})
            return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': blog_id}))
    else:
        form = PostForm()#(blog_id=blog.id)
    return render(request, 'blogger/create_post_.html', {'blog_id':blog_id ,'form': form})


def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    # if request.method == 'POST':
    if blog.author_id != request.user.id:
        return HttpResponseForbidden('You are not allowed to post in this blog!')
    if 'Delete_blog' == request.GET.get('name'):
        return delete_user(request)
    else:
        form = BlogEditForm(request.POST or None, request.FILES or None, instance=blog)  # , blog_id=blog.id)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': blog_id}))

                # return delete_user(request)
        else:
            form = BlogEditForm(instance=blog)  # (blog_id=blog.id)

    return render(request, 'blogger/edit_blog.html', {'blog_id': blog_id, 'form': form})


def delete_user(request):
    user = get_object_or_404(User, id=request.user.id)
    logout(request)
    user.delete()   # or save edits
    # return get_blog_list(request)
    return HttpResponseRedirect(reverse('index'))


def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        # if 'Like' in request.POST:
        if 'Like' == request.GET.get('name'):
            new_like, created = Like.objects.get_or_create(user=request.user, post_id=post_id)
            if not created:
                post.likes = post.likes - 1
                post.save()
                Like.objects.get(user=request.user, post_id=post_id).delete()
                return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': post.blog.id}))
                # the user already liked this picture before
            else:
                post.likes = post.likes + 1
                post.save()
                return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': post.blog.id}))
            # oll korrekt
        elif 'Edit_post' == request.GET.get('name'):
            return edit_post(request, post_id)
        elif 'Delete_post' == request.GET.get('name'):
            return delete_post(request, post_id)
        else:
            return create_comment(request, post_id)
    else:
        return render_blog(request, post.blog.id)


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
     # , blog_id=blog.id)
    if post.blog.author_id != request.user.id:
        return HttpResponseForbidden('You are not allowed to post in this blog!')
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    # form = PostForm(request.POST, request.FILES, blog_id=blog.id)
    if form.is_valid():
        # form.blog = blog
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': post.blog.id}))
    else:
        form = PostForm(instance=post)  # (blog_id=blog.id)
    return render(request, 'blogger/edit_post.html', {'blog_id': post.blog.id, 'form': form})


def delete_post(request,  post_id):
    post = get_object_or_404(Post, id=post_id)
    blog = post.blog
    if post.blog.author_id != request.user.id:
        return HttpResponseForbidden('You are not allowed to post in this blog!')
    else:
        post.delete()   # or save edits
        return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': blog.id}))


def follow(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    # if request.method == 'POST':
    if blog.author_id == request.user.id:
        return HttpResponseForbidden('You are not allowed to follow your blog!')
    else:
        follow, created = Follow.objects.get_or_create(following=blog.author, follower=request.user)
        if not created:

            Follow.objects.get(following=blog.author, follower=request.user).delete()
            return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': blog.id}))

        else:
            return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': blog.id}))


def list(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    user_follow = []
    if 'Following' == request.GET.get('name'):
        for us in blog.author.follower.all():
            user_follow.append(us.following)  #Follow.objects.filter(following=blog.author).order_by('-created')
    else:
        for us in blog.author.following.all():
            user_follow.append(us.follower)
        # user_follow = blog.author.following.all() #Blog.objects.filter(follower__id=blog.author_id).order_by('-created')
    # return render(request, 'blogger/list.html', context)
    return render(request, 'blogger/list.html', {'blog': blog, 'user_follow': user_follow})


def complaint(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        # if 'Like' in request.POST:
            new_complaint, created = Complaint.objects.get_or_create(user=request.user, comment_id=comment_id)
            if not created:
                comment.complaints = comment.complaints - 1
                comment.save()
                Complaint.objects.get(user=request.user, comment_id=comment_id).delete()
                return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': comment.commented_image.blog.id}))
                # the user already liked this picture before
            else:
                comment.complaints = comment.complaints + 1
                comment.save()
                blog_id = comment.commented_image.blog.id
                if comment.complaints == 5:
                    comment.delete()
                return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': blog_id}))
    else:
        return render_blog(request, comment.post.blog.id)