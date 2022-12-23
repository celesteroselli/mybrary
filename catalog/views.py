import isbnlib
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import BookForm, BulletinAdd, EditBookForm, LibraryEdit, LoanAdd, ManualBookForm, PostAdd, AddComment
from .models import Book, BulletinGroup, LoanInstance, Post, News, Library
from django.core.paginator import Paginator

@login_required
def Index(request):
    books = Book.objects.filter(user=request.user)
    newsletters = News.objects.filter(type=1)
    object_list = LoanInstance.objects.filter(user=request.user)
    paginator = Paginator(object_list, 8) # Show 8 loans per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalog/index.html', {'loans': object_list, 'page_obj': page_obj, 'books': books, 'newsletters': newsletters})

def Settings(request):
    user = request.user
    library = get_object_or_404(Library, user=request.user)
    return render(request, 'catalog/settings.html', {'user': user, 'object':library})

def Edit(request):
    user = request.user
    library = get_object_or_404(Library, user=request.user)
    initial_data = {
        "user": user,
        "name": library.name,
        "bio": library.bio,
    }
    if request.method == "POST":
        form = LibraryEdit(request.POST, request.FILES)
        if form.is_valid():
            library.name = form.cleaned_data['name']
            library.bio = form.cleaned_data['bio']
            #if form.cleaned_data['picture'] == None:
                #library.picture = library.picture
            #else:
                #library.picture = form.cleaned_data['picture']
            user.username = form.cleaned_data['user']
            library.save()
            user.save()
            return redirect('settings')
            
    form = LibraryEdit(initial=initial_data)
    return render(request, 'catalog/settings.html', {'user': user, 'form': form, 'object':library})

def AddBook(request):
    search_post = request.GET.get('search')
    if search_post:
        list = Book.objects.filter(user=request.user)
        object_list = list.filter(Q(title__contains=search_post) | Q(author__contains=search_post) | Q(isbn__contains=search_post))
    else:
        object_list = Book.objects.filter(user=request.user)
    paginator = Paginator(object_list, 15) # Show 25 contacts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = BookForm(request.POST)
    if form.is_valid():
        Book1 = form.save(commit=False)
        Book1.user = request.user
        Book1.title = (isbnlib.meta(Book1.isbn))['Title']
        Book1.author = str((isbnlib.meta(Book1.isbn))['Authors']).strip("'[]")
        Book1.desc = (isbnlib.desc(Book1.isbn))
        Book1.image_src = (isbnlib.cover(Book1.isbn)).get('smallThumbnail')
        Book1.save()
        return redirect('books')
    return render(request, 'catalog/book_list.html', {'form': form, 'object_list': object_list, 'page_obj': page_obj})

def BoardList(request):
    boards = BulletinGroup.objects.filter(members=request.user)
    form = BulletinAdd(request.POST)
    if request.method == "POST":
        if form.is_valid():
            board = form.save(commit=False)
            board.save()
            board.members.add(request.user)
            return render(request, "catalog/share_board.html", {"board":board})
    return render(request, "catalog/bulletingroup_list.html", {"form": form, "boards": boards})

class BookSearchView(generic.ListView):
    model = Book

    def get_queryset(self):
        query = self.request.GET.get('q')
        filtered_list = Book.objects.filter(
            Q(title__contains=query) | Q(author__contains=query) | Q(isbn__contains=query)
        )
        return filtered_list

class BoardListView(generic.ListView):
    model = BulletinGroup

    def get_queryset(self):
        return BulletinGroup.objects.filter(members=self.request.user)

def BulletinBoard(request, pk):
    form = PostAdd(request.POST or None)
    form2 = AddComment(request.POST or None)
    board = BulletinGroup.objects.get(pk=pk)
    if request.method == 'POST':
        if 'add' in request.POST:
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.board = board
                post.save()
                return redirect("bulletin", pk)
        else:
            postpk = request.POST.get("comment")
            attatched_post = Post.objects.get(pk=postpk)
            if form2.is_valid():
                comment = form2.save(commit=False)
                comment.user = request.user
                comment.post = attatched_post
                comment.save()
                return redirect("bulletin", pk)
    return render(request, "catalog/bulletin.html", {"board": board, "add_form": form, "comment_form": form2})

def CommentBulletin(request, pk, postpk):
    board = BulletinGroup.objects.get(pk=pk)
    form2 = PostAdd()
    post = BulletinGroup.objects.get(pk=postpk)
    form = AddComment(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect("bulletin", pk)
    return render(request, "catalog/bulletin.html", {"board": board, "form": form2, "comment_form": form})

def AddBoard(request):
    form = BulletinAdd(request.POST)
    if form.is_valid():
        Board = form.save(commit=False)
        Board.save()
        return redirect('bulletin_list')
    return render(request, 'catalog/board_add.html', {'form': form})

def JoinGroup(request, pk):
    board = BulletinGroup.objects.get(pk=pk)
    board.members.add(request.user)
    return redirect('boards')

def AddPost(request, pk):
    form = PostAdd(request.POST)
    if form.is_valid():
        Post = form.save(commit=False)
        Post.user = request.user
        Post.board = BulletinGroup.objects.filter(pk=pk)
        Post.save()
        return redirect('bulletin')
    return render(request, 'catalog/post_add.html', {'form': form})

        
class LoanListView(generic.ListView):
    model = LoanInstance
    template_name = 'catalog/loan_list.html'  # Specify your own template name/location
    context_object_name = 'loan_list'

    def get_queryset(self):
        return LoanInstance.objects.filter(user=self.request.user)

def BookDetail(request, pk):
    instance = get_object_or_404(Book, pk=pk)
    form = LoanAdd(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            LoanInstance = form.save(commit=False)
            LoanInstance.book_loaned = instance
            instance.status = 'ON LOAN'
            LoanInstance.user = request.user
            LoanInstance.save()
            instance.save()
            return redirect('books')
    return render(request, 'catalog/book_detail.html', {'form': form, 'book': instance})

class BookEdit(generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'genre', 'desc']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return '/' # or whatever url you want to redirect to

def ManualAddBook(request):
    form = ManualBookForm(request.POST)
    if form.is_valid():
        Book = form.save(commit=False)
        Book.user = request.user
        Book.image_src = (isbnlib.cover(Book.isbn)).get('smallThumbnail')
        Book.save()
        return redirect('books')
    return render(request, 'catalog/manual_book_add.html', {'form': form})

def ReturnBook(request, pk):
    instance = get_object_or_404(Book, pk=pk)
    loan = get_object_or_404(LoanInstance, book_loaned=instance)
    loan.delete()
    instance.status = 'AVAILABLE'
    instance.save()
    return redirect('books')

def AddLoan(request, pk):
    instance = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = LoanAdd(request.POST)
        if form.is_valid():
            LoanInstance = form.save(commit=False)
            LoanInstance.book_loaned = instance
            instance.status = 'ON LOAN'
            LoanInstance.user = request.user
            LoanInstance.save()
            instance.save()
            return redirect('books')

    form = LoanAdd()
    return render(request, 'catalog/loan_add.html', {'form': form})

def DeleteBook(request, pk):
    instance = get_object_or_404(Book, pk=pk)
    instance.delete()
    return redirect('books')

class FilterOverdue(generic.ListView):
    model = Book

    def get_queryset(self):
        return Book.objects.filter(status = 'ON LOAN')

def UserCreate(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('index')
    return render(request, 'create_user.html', {'form': form})

class PostDetail(generic.DetailView):
    model = Post