from django.db import models
from django.urls import reverse
import uuid  # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Genre(models.Model):
    """
    Model representing a book genre
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction etc.)")
    genre_image = models.ImageField(upload_to='picture/%Y/%m/%d/', blank=True)

    @property
    def photo_url(self):
        if self.genre_image and hasattr(self.genre_image, 'url'):
            return self.genre_image.url

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a book language")

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model representing a book
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)  # one to many
    # on_delete=models.SET_NULL - delete author info in db if book delete
    # null=True - allows the db to store the value=Null
    book_image = models.ImageField(upload_to='picture/book/%Y/%m/%d/', null=True, blank=True)
    summary = models.TextField(max_length=750, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN namber</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    link = models.CharField(max_length=200, default='https://python.swaroopch.com')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return '{id} ({title})'.format(id=self.id, title=self.book.title)


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{last}, {first}'.format(last=self.last_name, first=self.first_name)

    class Meta:
        ordering = ['last_name']


