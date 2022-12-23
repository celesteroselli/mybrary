from django import forms
from .models import Book, BulletinGroup, Library, LoanInstance, Post, PostComment

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('isbn', 'genre',)

        widgets = {
            'isbn': forms.NumberInput(attrs={'class': 'form-control', 'use_required_attribute':'False'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
        }

class BulletinAdd(forms.ModelForm):
    class Meta:
        model = BulletinGroup
        fields = ("name",)

class LibraryEdit(forms.Form):
    user = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Username...",
                "class": "form-control",
                "rows": "1",
            }
        ),
        label="",

    )

    name = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Library name...",
                "class": "form-control",
                "rows": "1",
            }
        ),
        label="",
    )

    bio = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Bio...",
                "class": "form-control",
                "rows": "6",
            }
        ),
        label="",
    )
    picture = forms.ImageField(
        required=False,
        widget=forms.widgets.FileInput(
            attrs={"class": "form-control",}
        ),
        label="",
    )

class AddComment(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Comment...",
                "class": "form-control, w-75",
                "rows": "1",
            }
        ),
        label="",
    )
    
    class Meta:
        model = PostComment
        exclude = ("user", "post",)

class PostAdd(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Title...",
                "class": "form-control",
                "rows": "1",
            }
        ),
        label="",
    )
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Post something...",
                "class": "form-control",
                "rows": "5",
            }
        ),
        label="",
    )
    class Meta:
        model = Post
        exclude = ("user","board",)
        
class ManualBookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ("user", "image_src",)

class LoanAdd(forms.ModelForm):
    class Meta:
        model = LoanInstance
        exclude = ("user", "book_loaned","loan_status", "overdue")

class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ("user",)

