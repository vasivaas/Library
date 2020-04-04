from django.shortcuts import render, redirect
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import RenewBookModelForm #, RenewBookForm

# Create your views here.
def index(request):
    """
    Функція відображення головної сторінки сайту
    :param request:
    :return: index.html
    """

    num_of_books = Book.objects.all().count()
    num_of_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    authors = Author.objects.all().count()
    num_book_and_genre = Book.objects.filter(title__icontains='the').count() + Genre.objects.filter(
        name__iexact='Poem').count()

    list_genre = Genre.objects.all()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # num_genre = Genre.objects.filter(name__icontains=list_genre.name).count()
    # генерація HTML шаблона index.html з даними всередині
    # змінною контексту context
    return render(
        request, 'index.html', context={
            'num_of_books': num_of_books,
            'num_of_instances': num_of_instances,
            'num_instances_available': num_instances_available,
            'num_authors': authors,
            'num_book_and_genre': num_book_and_genre,
            'list_genre': list_genre,
            'num_visits': num_visits,
            # 'num_genre': num_genre,
        }
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.all()


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    models = BookInstance
    template_name = 'catalog/myprofile_bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    @property
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


from .forms import CreateUserForm
from django.contrib import messages

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Акаунт створив ' + user)
                return redirect('login')
        context = {'form': form, }
        return render(request, 'register/register.html', context)

'''
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
'''

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'first_name':'Імя', 'last_name':'Прізвище', 'date_of_birth':'11/04/1965', 'date_of_death':'04/12/2000',}
    success_url = reverse_lazy('authors')
    # Для того щоб змінити суфікс шаблону з model_name_form.html на model_name_create.html
    template_name_suffix = '_create'


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death' ]
    success_url = reverse_lazy('authors')
    template_name_suffix = '_update'


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    # Для того щоб змінити суфікс шаблону з model_name_confirm_delete.html на model_name_delete.html
    template_name_suffix = '_delete'


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('book.get_absolute_url')
    template_name_suffix = '_create'


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('book.get_absolute_url')
    template_name_suffix = '_update'


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    template_name_suffix = '_delete'
