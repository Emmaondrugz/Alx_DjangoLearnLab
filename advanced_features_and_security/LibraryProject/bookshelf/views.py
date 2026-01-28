from django.shortcuts import render
from .models import Book
from django.views.generic import DetailView, TemplateView, ListView, CreateView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def book_list_view(request):
    books = Book.objects.all()
    context = {'books_data': books}
    return render(request, 'books.html', context)

class BookListView(ListView):
    model = Book
    template_name = 'book.html'
    context_object_name = 'books'

class BookTemplateView(TemplateView):
    template_name = 'books.html'

class BookCreateView(CreateView):
    model = Book
    fields = ['author', 'title', 'publication_year']
    template_name = 'book/add_book.html'
    success_url = 'book/my_books.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong, please try again later.')
        return super().form_invalid(form)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = '/books.html'
    template_name = 'registration/sign_up.html'


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def list_users(request):
    """
    View to list all users.
    Requires: can_view permission
    """
    users = User.objects.all()
    users_list = "<h1>Users List</h1><ul>"
    for user in users:
        users_list += f"<li>{user.username} - {user.email}</li>"
    users_list += "</ul>"
    return HttpResponse(users_list)


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_user(request):
    """
    View to create a new user.
    Requires: can_create permission
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return HttpResponse("<h1>User created successfully!</h1>")

    return HttpResponse("""
        <h1>Create User</h1>
        <form method="post">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="email" name="email" placeholder="Email" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Create</button>
        </form>
    """)


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_user(request, user_id):
    """
    View to edit an existing user.
    Requires: can_edit permission
    """
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return HttpResponse(f"<h1>User {user.username} updated successfully!</h1>")

    return HttpResponse(f"""
        <h1>Edit User: {user.username}</h1>
        <form method="post">
            <input type="text" name="username" value="{user.username}" required><br>
            <input type="email" name="email" value="{user.email}" required><br>
            <button type="submit">Update</button>
        </form>
    """)


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_user(request, user_id):
    """
    View to delete a user.
    Requires: can_delete permission
    """
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = user.username
        user.delete()
        return HttpResponse(f"<h1>User {username} deleted successfully!</h1>")

    return HttpResponse(f"""
        <h1>Delete User: {user.username}</h1>
        <p>Are you sure you want to delete this user?</p>
        <form method="post">
            <button type="submit">Yes, Delete</button>
        </form>
    """)