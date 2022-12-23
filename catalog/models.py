from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse
from isbnlib import *
from datetime import *

class BulletinGroup(models.Model):
    name = models.CharField(max_length=100, null=True)
    members = models.ManyToManyField(User, blank=True)

    def __str__(self):
        #String representing model object
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    board = models.ForeignKey(BulletinGroup, related_name="posts", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=30, blank=True, null=True)
    body = models.TextField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

class PostComment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField(max_length=500, blank=True, null=True)

class Library(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #picture = ResizedImageField(size=[500, 500], crop=['middle', 'center'], null=True, blank=True, upload_to='images/', default='images/logo.png')
    name = models.CharField(default="My Library", max_length=40, null=True)
    bio = models.CharField(default="This is my bio. Edit me!!", max_length=200)

    def __str__(self):
        #String representing model object
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_library(sender, instance, created, **kwargs):
    if created:
        Library.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_library(sender, instance, **kwargs):
    instance.library.save()

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    isbn = models.CharField('ISBN', max_length=100)

    title = models.CharField(max_length=500, null=True, blank=True)

    image_src = models.CharField(max_length=400, null=True, blank=True)

    author = models.CharField(max_length=50, null=True, blank=True)

    desc = models.CharField(max_length=1000, null=True, blank=True)

    LOAN_STATUS = (
        ('AVAILABLE', 'Available'),
        ('ON LOAN', 'On Loan'),
        ('ON HOLD', 'On Hold'),
    )

    GENRES = {
        ('REALISTIC FICTION', 'Realistic Fiction'),
        ('HISTORICAL FICTION', 'Historical Fiction'),
        ('SCIENCE FICTION', 'Science Fiction'),
        ('ADVENTURE', 'Adventure'),
        ('FANTASY', 'Fantasy'),
        ('HORROR', 'Horror'),
        ('MYSTERY', 'Mystery'),
        ('NON-FICTION', 'Nonfiction'),
    }

    genre = models.CharField(
        max_length=30,
        choices=GENRES,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=LOAN_STATUS,
        blank=True,
        default='Available',
    )

    def __str__(self):
        #String representing model object
        return self.title

class LoanInstance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    loaner = models.CharField(max_length=50, null=True)

    loaner_email = models.EmailField(blank=True, null=True)

    book_loaned = models.ForeignKey(Book, on_delete=models.CASCADE,
                                    blank=False, null=True)

    due_date = date.today()+timedelta(days=21)

    overdue = models.BooleanField(default=False)

    loan_status = not overdue

class News(models.Model):

    TYPE = (
        ('1', 'Newsletter'),
        ('2', 'Book Rec'),
        ('3', 'Book List'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=100, null=True)

    desc = models.CharField(max_length=80, null=True)

    type = models.CharField(max_length=50, choices=TYPE, null=True)

    link = models.URLField(max_length=300, null=True)
