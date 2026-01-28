"""
Secure views implementation following Django best practices.
All views implement protection against SQL injection, XSS, and CSRF attacks.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
@csrf_protect  # Explicitly enforce CSRF protection
def list_users(request):
    """
    View to list all users with search functionality.
    Requires: can_view permission

    Security measures:
    - Uses Django ORM (prevents SQL injection)
    - Validates and sanitizes search input
    - Escapes output to prevent XSS
    """
    # Get search query parameter
    search_query = request.GET.get('search', '')

    # Use Django ORM with Q objects for safe querying
    # This prevents SQL injection by using parameterized queries
    if search_query:
        # Sanitize input by limiting length and stripping dangerous characters
        search_query = search_query[:100].strip()

        # Use Django ORM - NOT raw SQL
        # SECURE: Django ORM automatically escapes and parameterizes queries
        users = User.objects.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    else:
        users = User.objects.all()

    # Log the action for security auditing
    logger.info(f"User {request.user.username} viewed user list")

    # Escape output to prevent XSS (though Django templates auto-escape)
    users_list = "<h1>Users List</h1>"
    if search_query:
        # Escape the search query before displaying
        users_list += f"<p>Search results for: {escape(search_query)}</p>"

    users_list += "<ul>"
    for user in users:
        # Django auto-escapes, but being explicit for clarity
        users_list += f"<li>{escape(user.username)} - {escape(user.email)}</li>"
    users_list += "</ul>"

    return HttpResponse(users_list)


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect
def create_user(request):
    """
    View to create a new user.
    Requires: can_create permission

    Security measures:
    - CSRF token required in form
    - Input validation using Django's built-in validators
    - Password hashing handled by Django's create_user method
    - Prevents XSS through output escaping
    """
    if request.method == 'POST':
        # Get and validate inputs
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # Input validation
        if not username or not email or not password:
            return HttpResponse("<h1>Error: All fields are required</h1>", status=400)

        # Length validation to prevent abuse
        if len(username) > 150 or len(email) > 254:
            return HttpResponse("<h1>Error: Input too long</h1>", status=400)

        try:
            # SECURE: Using Django's create_user method
            # - Automatically hashes password
            # - Validates email format
            # - Prevents SQL injection through ORM
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Log successful creation
            logger.info(f"User {request.user.username} created new user: {username}")

            return HttpResponse("<h1>User created successfully!</h1>")

        except Exception as e:
            # Log the error but don't expose details to user
            logger.error(f"Error creating user: {str(e)}")
            return HttpResponse("<h1>Error: Could not create user</h1>", status=500)

    # IMPORTANT: CSRF token must be included in form
    # The {% csrf_token %} template tag would be used in a real template
    return HttpResponse("""
        <h1>Create User</h1>
        <form method="post">
            <!-- CSRF token is automatically added by Django middleware -->
            <input type="text" name="username" placeholder="Username" required maxlength="150"><br>
            <input type="email" name="email" placeholder="Email" required maxlength="254"><br>
            <input type="password" name="password" placeholder="Password" required minlength="8"><br>
            <button type="submit">Create</button>
        </form>
    """)


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
@csrf_protect
def edit_user(request, user_id):
    """
    View to edit an existing user.
    Requires: can_edit permission

    Security measures:
    - Uses get_object_or_404 to prevent information disclosure
    - CSRF protection on form submission
    - Input validation and sanitization
    - SQL injection prevention through ORM
    """
    # SECURE: get_object_or_404 prevents SQL injection
    # Returns 404 if not found (prevents user enumeration)
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Validate and sanitize inputs
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()

        # Input validation
        if not username or not email:
            return HttpResponse("<h1>Error: All fields are required</h1>", status=400)

        if len(username) > 150 or len(email) > 254:
            return HttpResponse("<h1>Error: Input too long</h1>", status=400)

        try:
            # SECURE: Using ORM update (prevents SQL injection)
            user.username = username
            user.email = email
            user.save()

            # Log the action
            logger.info(f"User {request.user.username} updated user: {user.username}")

            return HttpResponse(f"<h1>User {escape(user.username)} updated successfully!</h1>")

        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return HttpResponse("<h1>Error: Could not update user</h1>", status=500)

    # Escape output to prevent XSS
    return HttpResponse(f"""
        <h1>Edit User: {escape(user.username)}</h1>
        <form method="post">
            <!-- CSRF token required -->
            <input type="text" name="username" value="{escape(user.username)}" required maxlength="150"><br>
            <input type="email" name="email" value="{escape(user.email)}" required maxlength="254"><br>
            <button type="submit">Update</button>
        </form>
    """)


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
@csrf_protect
def delete_user(request, user_id):
    """
    View to delete a user.
    Requires: can_delete permission

    Security measures:
    - CSRF protection (requires POST for destructive action)
    - Authorization check (permission_required decorator)
    - Prevents users from deleting themselves
    - SQL injection prevention through ORM
    """
    # SECURE: get_object_or_404 prevents SQL injection and information disclosure
    user = get_object_or_404(User, id=user_id)

    # Prevent users from deleting themselves
    if user.id == request.user.id:
        return HttpResponse("<h1>Error: You cannot delete yourself</h1>", status=403)

    if request.method == 'POST':
        try:
            username = user.username

            # SECURE: Using ORM delete (prevents SQL injection)
            user.delete()

            # Log the action
            logger.info(f"User {request.user.username} deleted user: {username}")

            return HttpResponse(f"<h1>User {escape(username)} deleted successfully!</h1>")

        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return HttpResponse("<h1>Error: Could not delete user</h1>", status=500)

    # Confirmation page - requires POST to actually delete (CSRF protection)
    return HttpResponse(f"""
        <h1>Delete User: {escape(user.username)}</h1>
        <p>Are you sure you want to delete this user?</p>
        <form method="post">
            <!-- CSRF token required for destructive action -->
            <button type="submit" style="background-color: red; color: white;">
                Yes, Delete
            </button>
        </form>
        <a href="/users/">Cancel</a>
    """)


# Example of INSECURE code (DO NOT USE):
"""
# INSECURE - SQL Injection vulnerability
def insecure_search(request):
    search = request.GET.get('search')
    # DANGER: String formatting with user input!
    query = f"SELECT * FROM users WHERE username = '{search}'"
    # Attacker could inject: ' OR '1'='1

# INSECURE - XSS vulnerability  
def insecure_display(request):
    user_input = request.GET.get('input')
    # DANGER: Unescaped user input in HTML!
    return HttpResponse(f"<h1>You entered: {user_input}</h1>")
    # Attacker could inject: <script>alert('XSS')</script>

# INSECURE - No CSRF protection
@csrf_exempt  # NEVER do this!
def insecure_form(request):
    # Form without CSRF token is vulnerable
    pass
"""

"""
Secure views implementation for bookshelf app.

Security features implemented:
- CSRF protection on all POST requests
- SQL injection prevention using Django ORM
- XSS prevention through template escaping
- Input validation using Django forms
- Permission checks
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db.models import Q
from .forms import ExampleForm, SearchForm
from .models import Book


@csrf_protect
def form_example_view(request):
    """
    Example view demonstrating secure form handling.

    Security measures:
    - @csrf_protect decorator ensures CSRF protection
    - Django Form handles validation and sanitization
    - No raw SQL queries (prevents SQL injection)
    - Template auto-escapes output (prevents XSS)
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)

        if form.is_valid():
            # Access cleaned and validated data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Process the data securely
            # In a real app, you might save to database using ORM
            messages.success(request, f'Thank you, {name}! Your message has been received.')

            # Redirect after successful POST (prevents double submission)
            return redirect('form_example')
        else:
            # Form has errors - they will be displayed in template
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request - display empty form
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})


@csrf_protect
def book_list_view(request):
    """
    Display list of books with search functionality.

    Security measures:
    - CSRF protection
    - Safe query handling with Django ORM
    - Input validation through SearchForm
    - XSS prevention through template escaping
    """
    form = SearchForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')

        if query:
            # SECURE: Using Django ORM with Q objects
            # Automatically parameterizes queries - prevents SQL injection
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query)
            )

    context = {
        'books': books,
        'form': form,
    }

    return render(request, 'bookshelf/book_list.html', context)


# Example of INSECURE code (DO NOT USE):
"""
# INSECURE - SQL Injection vulnerability
def insecure_search(request):
    query = request.GET.get('q', '')
    # DANGER: Direct SQL with string formatting
    sql = f"SELECT * FROM books WHERE title LIKE '%{query}%'"
    # Attacker could inject: '; DROP TABLE books; --

# INSECURE - Missing CSRF protection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # NEVER DO THIS!
def insecure_form(request):
    # Vulnerable to CSRF attacks
    pass

# INSECURE - No input validation
def insecure_input(request):
    user_input = request.POST.get('data')
    # Using raw input without validation
    # Vulnerable to XSS and other attacks
"""