from django.urls import path

# from django.views.generic import RedirectView
from . import views

# app_name='catalog'

urlpatterns=[
        path('home/',views.index,name='home'),
        path('book/',views.book_func,name='book'),
        path('page/<int:pk>',views.book_function,name='book_function_with_pk'),
        path('books/',views.BookListView.as_view(), name='books'),
        # path('book-details/<int:pk>',views.view_details,name='book-detail'),
        path('book/<int:pk>',views.my_model_detail,name='my_book_detail'),
        path('author/',views.AuthorListView.as_view(),name='author_list'),
        path('author/<pk>',views.author_views,name='author_details'),
        # path('accounts/login/',views.login,name='login'),
        # path('accounts/login/',name='login'),
        # path('accounts/logout/' name='logout'),
        # path('accounts/password_change/' name='password_change')
        # path('accounts/password_change/done/' name='password_change_done')
        # path('accounts/password_reset/'name='password_reset')
        # path('accounts/password_reset/done/',name='password_reset_done')
        # path('accounts/reset/<uidb64>/<token>/',name='password_reset_confirm')
        # path('accounts/reset/done/' ,name='password_reset_complete')
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/',views.BookCreate.as_view(),name='book-create'),
    path('book/success_url/',views.success_url,name='success-url'),
    path('book/update/<int:pk>',views.BookUpdate.as_view(),name='success-update'),
    path('book/delete/<int:pk>',views.BookDelete.as_view(),name='success-delete'),
    path('register/',views.register_,name='register'),
#         path('login/',views.login,name='login'),
]