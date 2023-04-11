from django.shortcuts import render, redirect
from .models import Book, Author, BookInstance, Genre
from django.core.paginator import Paginator
from django.views import generic
from django.shortcuts import redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .form import CustomUserCreationForm
import datetime
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from .form import RenewBookForm
# Create your views here.

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    # Generating the count for the genres 
    num_genre=Genre.objects.all().count()
    # This contains the word FEAR
    num_book_word_count = Book.objects.filter(title__contains='War').count()
    

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre':num_genre,
        'num_book_word_count':num_book_word_count,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
@login_required
def book_func(request):
    book_=Book.objects.all()
    paginator=Paginator(book_,2)
    page_number=request.GET.get('page')
    if page_number==None:
        page_number=1
    context={
        'page_obj':paginator.page(page_number),
        'page_number':page_number
    }
    return render(request, 'book.html', context=context)

# def detail(request):
#     return render(request, 'page.html')
@login_required
def book_function(request,pk):
    book_=Book.objects.all()
    paginator=Paginator(book_,2)
    page_number=request.GET.get('page')
    # page_obj=paginatior.get_page(page_number)
    context={
        'page_obj':paginator.page(pk)
    }
    return render(request, 'page.html', context=context)
# @login_required
class BookListView(generic.ListView):
    model=Book
    context_object_name='book_list' # Your own name for the list as a template variable
    #queryset=Book.objects.filter(title__icontains='war')[:5] # Get 5 books conataining the title war
    queryset=Book.objects.all()
    template_name=r'C:\Users\USCHIP\locallibrary\locallibrary\templates\books_list.html'
    paginate_by=1


# def view_details(request, pk):
#     book_details = Book.objects.get(pk=pk)
#     return redirect(book_details.get_absolute_url())
@login_required
def my_model_detail(request, pk):
    my_model = get_object_or_404(Book, pk=pk)
    context = {'my_model': my_model}
    return render(request, 'my_model_detail.html', context)
from file_path import ROOT_DIR
import os
print(ROOT_DIR)
print(os.path.join(ROOT_DIR, 'templates','author_list.html'))
print(r'C:\Users\USCHIP\locallibrary-1\locallibrary\templates\author_list.html')
# @login_required
class AuthorListView(generic.ListView):
    model=Author
    context_object_name='author_list' # Your own name for the list as a template variable
    #queryset=Book.objects.filter(title__icontains='war')[:5] # Get 5 books conataining the title war
    queryset=Author.objects.all()
    template_name=os.path.join(ROOT_DIR, 'templates','author_list.html')
    paginate_by=1
@login_required  
def author_views(request,pk):
    author = get_object_or_404(Author, pk=pk)
    context = {'author': author}
    return render(request, 'author_.html', context)



# Creating User

# def register(request):
#     #Create user and save to the database
#     if request.Method =='POST':
#         username=request.POST.get('username')
#         email=request.POST.get('email')
#         password=request.POST.get('password')
        
#         # Create a new user with the collected data
#         user= User.objects.create_user(username=username,email=email,password=password)
        
#         # Set any additional user properties as needed
#         user.is_staff=True
#         user.is_superuser=False
#         user.save()
#         messages.success(request,f'Account created for {username}!')
#         return redirect('login')
#     else:
#         return render(request,'register.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
     
def register_(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
       
  
    


# def login(request):
#     if request.method=='POST':
#          #Collect username and password from the POST request
#          username=request.POST.get('username')  
#          password=request.POST.get('password')
         
#          #Authenticate the user
#          user = authenticate(request,username=username,
#                              password=password)
         
#          if user is not None:
#              # Log in the user and redirect to a success page
#              login(request, user)
#              return redirect('home')
#          else:
#              # Return an error message to the user
#              return render(request,'login.html',{'error':'Invalid credentials'})
#     else:
#         return render(request,'login.html')

@login_required
def renew_book_librarian(request, pk):
    book_instance=get_object_or_404(BookInstance, pk=pk)
    
    # If this is a POST request then process the Form data
    
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request(binding):
        form = RenewBookForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
           # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
           book_instance.due_back=form.cleaned_data['renewal_date']
           book_instance.save()
           
           # redirect to a new URL:
           return HttpResponseRedirect(reverse('all-borrowed'))
         # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)           
            
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    template_name=os.path.join(ROOT_DIR, 'templates','author_form.html')
    # template_name=r'C:\Users\USCHIP\locallibrary-1\locallibrary\templates\author_form.html'
class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    template_name=os.path.join(ROOT_DIR, 'templates','author_form.html')
    # template_name=r'C:\Users\USCHIP\locallibrary-1\locallibrary\templates\author_form.html'
class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name=os.path.join(ROOT_DIR, 'templates','author_confirm_delete.html')
    # template_name=r'C:\Users\USCHIP\locallibrary-1\locallibrary\templates\author_confirm_delete.html'
       
       
class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn','genre','language']
    success_url = reverse_lazy('success-url') 
    def form_valid(self, form):
        form.instance.user = self.request.user # set the user field to the current user
        return super().form_valid(form)
    # initial = {'date_of_death': '11/06/2020'}
    template_name=os.path.join(ROOT_DIR, 'templates','book_form.html')
    # template_name=r'C:\Users\USCHIP\locallibrary-1\locallibrary\templates\book_form.html'
class BookUpdate(UpdateView):
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    template_name=os.path.join(ROOT_DIR, 'templates','book_form.html')
    # template_name=r'C:\Users\USCHIP\locallibrary-1\locallibrary\templates\book_form.html'
    success_url = reverse_lazy('success-url') 
    def form_valid(self, form):
        form.instance.user = self.request.user # set the user field to the current user
        return super().form_valid(form)
    
class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('success-url')
    template_name=os.path.join(ROOT_DIR, 'templates','book_confirm_delete.html')
    # template_name=r'C:\Users\USCHIP\locallibrary-1\locallibrary\templates\book_confirm_delete.html'
    


def success_url(request):
    return render(request, 'success_url.html')

# Note: Other common types of tests include black box, white box, manual,
# automated, canary, smoke, conformance, acceptance, functional, system, 
# performance, load, and stress tests. Look them up for more information.