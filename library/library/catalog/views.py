from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
    #num_genre = Genre.objects.filter(name__icontains=list_genre.name).count()
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
            #'num_genre': num_genre,
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

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')