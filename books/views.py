from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .forms import CommentForm

from .models import Book


class BookListView(generic.ListView):
    model = Book
    paginate_by = 4
    template_name = 'book/book_list.html'
    context_object_name = 'books'


# class BookDetailView(generic.DetailView):
#     model = Book
#     template_name = 'book/book_detail.html'

# @LoginRequiredMixin
def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book_comments = book.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.book = book
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    return render(request, 'book/book_detail.html', {
        'book': book,
        'comments': book_comments,
        'comment_form': comment_form
    })


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover', ]
    template_name = 'book/book_create.html'


class BookUpdateView(LoginRequiredMixin,UserPassesTestMixin, generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover', ]
    template_name = 'book/book_update.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class BookDeleteView(LoginRequiredMixin,UserPassesTestMixin, generic.DeleteView):
    model = Book
    template_name = 'book/book_delete.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
