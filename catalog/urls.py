from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('search/', views.BookSearchView.as_view(), name='book_search'),
    path('loans/', views.LoanListView.as_view(), name='loans'),
    path('book_add/', views.AddBook, name='book_add'),
    path('book_add/', views.AddBook, name='books'),
    path('manual_book_add/', views.ManualAddBook, name='manual_book_add'),
    path('loan_add/<int:pk>/', views.AddLoan, name='loan_add'),
    path('loan_return/<int:pk>/', views.ReturnBook, name='loan_return'),
    path('book_delete/<int:pk>/', views.DeleteBook, name='book_delete'),
    path('filter/overdue/', views.FilterOverdue.as_view(), name='filter_overdue'),
    path("<int:pk>/", views.BookDetail, name="book_detail"),
    path('<pk>/update', views.BookEdit.as_view(), name="book_edit"),
    path('bulletin/<pk>/', views.BulletinBoard, name="bulletin"),
    path('bulletin/<pk>/join/', views.JoinGroup, name="join"),
    path('bulletin/', views.BoardList, name="boards"),
    path('post/<pk>/', views.PostDetail.as_view(), name="post"),
    path("create_user/", views.UserCreate, name="create_user"),
    path('settings/', views.Settings, name="settings"),
    path('settings/edit/', views.Edit, name="settings_edit"),
]