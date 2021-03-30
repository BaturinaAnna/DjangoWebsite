from django import forms
from .models import Post, Blog


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    blog_title = forms.CharField(label='Blog Title', max_length=50)
    avatar = forms.ImageField(label='Avatar', required=False)
    username = forms.CharField(label='Username', max_length=32)
    bio = forms.CharField(label='BIO', max_length=300, required=False, widget=forms.Textarea)
    email = forms.EmailField(label='E-Mail', max_length=128)
    permission = forms.BooleanField(label='Permission', required=False)
    password = forms.CharField(label='Password', min_length=8, max_length=128, widget=forms.PasswordInput)
    password_again = forms.CharField(label='Password, again', min_length=8, max_length=128, widget=forms.PasswordInput)


class PostForm(forms.ModelForm):
    subject = forms.CharField(max_length=50)
    text = forms.CharField(max_length=1000, widget=forms.Textarea)
    address = forms.CharField(max_length=80)

    # def __init__(self, *args, **kwargs):
    #     blog_id = kwargs.pop('blog_id', '')
    #     super(PostForm, self).__init__(*args, **kwargs)   #what is this shit
    #     if blog_id:
    #         self.fields['blog'].initial = blog_id

    class Meta:
        model = Post
        fields = ['subject', 'text', 'address', 'photo']
        # widgets = {'blog': forms.HiddenInput()}

    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.fields['text'].widget.attrs.update({'class': 'postTextField'})


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['comment_post']

class BlogEditForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    bio = forms.CharField(max_length=1500, widget=forms.Textarea)

    class Meta:
        model = Blog
        fields = ['title', 'avatar', 'bio', 'permission']
