"""
Django settings for LibraryProject project.

SECURITY CONFIGURATION:
This settings file includes comprehensive security configurations for production deployment,
with a focus on HTTPS enforcement and secure communication.

For production deployment, ensure:
1. DEBUG = False
2. SECRET_KEY stored in environment variable
3. HTTPS is properly configured on web server
4. SSL/TLS certificates are valid and up-to-date
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Point to custom User model
AUTH_USER_MODEL = 'bookshelf.CustomUser'


# =====================================================
# CORE SECURITY SETTINGS
# =====================================================

# SECURITY WARNING: keep the secret key used in production secret!
# In production, load from environment variable for security
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-wo0#jx_)(kz#l1$$rf(eyl@jq_094!+2@@&2$pu*#0h^xxy-cs'
)

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False prevents information disclosure through error pages
# In production, detailed error information could expose:
# - Database schema and queries
# - File paths and directory structure
# - Installed packages and versions
# - Secret keys and configuration
DEBUG = False

# ALLOWED_HOSTS: Prevents HTTP Host Header attacks
# Only requests with Host headers matching these values will be processed
# This prevents attackers from poisoning cache or triggering password resets
# to arbitrary domains
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.yourdomain.com',        # Matches yourdomain.com and all subdomains
    'www.yourdomain.com',
    # Add your production domain here
]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'csp',                    # Content Security Policy middleware
    'bookshelf',
    'relationship_app',
]

MIDDLEWARE = [
    # SecurityMiddleware: Handles security-related middleware functionality
    # Must be first to apply security settings to all requests
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # CsrfViewMiddleware: Protects against Cross-Site Request Forgery attacks
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # XFrameOptionsMiddleware: Protects against clickjacking attacks
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # CSPMiddleware: Implements Content Security Policy
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =====================================================
# STEP 1: HTTPS ENFORCEMENT AND CONFIGURATION
# =====================================================

# SECURE_SSL_REDIRECT: Redirect all HTTP requests to HTTPS
# When True, SecurityMiddleware redirects all non-HTTPS requests to HTTPS
# This ensures all traffic is encrypted and protects against:
# - Man-in-the-middle attacks
# - Session hijacking
# - Credential theft
# - Data tampering
# IMPORTANT: Only enable this after HTTPS is properly configured on your server
SECURE_SSL_REDIRECT = True

# SECURE_HSTS_SECONDS: HTTP Strict Transport Security (HSTS) max-age
# Instructs browsers to ONLY access the site via HTTPS for the specified duration
# 31536000 seconds = 1 year
# Benefits:
# - Prevents SSL stripping attacks
# - Blocks protocol downgrade attacks
# - Eliminates the insecure initial HTTP request
# NOTE: Start with a small value (e.g., 300) for testing, then increase to 31536000
SECURE_HSTS_SECONDS = 31536000  # 1 year

# SECURE_HSTS_INCLUDE_SUBDOMAINS: Apply HSTS to all subdomains
# When True, HSTS policy applies to all subdomains
# Example: If set on example.com, applies to api.example.com, www.example.com, etc.
# WARNING: Ensure ALL subdomains support HTTPS before enabling
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SECURE_HSTS_PRELOAD: Allow HSTS preload list submission
# Enables submission to browser HSTS preload lists
# Browsers with preload lists will NEVER make an HTTP request to your domain
# To submit: https://hstspreload.org/
# Requirements:
# - SECURE_HSTS_SECONDS >= 31536000
# - SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# - Valid HTTPS certificate
# WARNING: Preloading is difficult to undo. Test thoroughly first.
SECURE_HSTS_PRELOAD = True

# SECURE_PROXY_SSL_HEADER: Detect HTTPS behind a proxy
# Required when Django is behind a reverse proxy (nginx, Apache, load balancer)
# The proxy terminates SSL and forwards requests to Django over HTTP
# This setting tells Django to trust the X-Forwarded-Proto header
# SECURITY WARNING: Only enable if you trust your proxy completely
# Malicious clients could spoof this header if not behind a trusted proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# =====================================================
# STEP 2: SECURE COOKIE CONFIGURATION
# =====================================================

# SESSION_COOKIE_SECURE: Only send session cookies over HTTPS
# When True, browsers will only send the session cookie over HTTPS connections
# Prevents session hijacking if user accidentally visits HTTP version
# REQUIRED when HTTPS is enabled
# Without this, session cookies could be intercepted over HTTP
SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_SECURE: Only send CSRF token cookies over HTTPS
# When True, browsers will only send CSRF cookies over HTTPS connections
# Prevents CSRF token theft if user accidentally visits HTTP version
# REQUIRED when HTTPS is enabled
CSRF_COOKIE_SECURE = True

# SESSION_COOKIE_HTTPONLY: Prevent JavaScript access to session cookies
# When True, JavaScript cannot access the session cookie via document.cookie
# Primary defense against XSS attacks stealing session tokens
# Even if XSS vulnerability exists, attacker cannot steal session
SESSION_COOKIE_HTTPONLY = True

# CSRF_COOKIE_HTTPONLY: Prevent JavaScript access to CSRF cookies
# When True, JavaScript cannot access the CSRF cookie
# Provides defense-in-depth against XSS attacks
CSRF_COOKIE_HTTPONLY = True

# SESSION_COOKIE_SAMESITE: Restrict when session cookies are sent
# Options: 'Strict', 'Lax', or 'None'
# - 'Strict': Cookie only sent for same-site requests (most secure)
# - 'Lax': Cookie sent for top-level navigations (balances security/usability)
# - 'None': Cookie sent with all requests (requires Secure flag)
# Protects against CSRF attacks by limiting cross-site cookie transmission
SESSION_COOKIE_SAMESITE = 'Strict'

# CSRF_COOKIE_SAMESITE: Restrict when CSRF cookies are sent
# Same options as SESSION_COOKIE_SAMESITE
# 'Strict' provides maximum CSRF protection
CSRF_COOKIE_SAMESITE = 'Strict'

# SESSION_COOKIE_AGE: Session timeout in seconds
# Default is 2 weeks (1209600 seconds)
# Shorter values are more secure but less convenient
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# SESSION_SAVE_EVERY_REQUEST: Update session on every request
# When True, session cookie expiry is refreshed on every request
# Provides better user experience (session doesn't expire while active)
# Slight performance impact due to more database writes
SESSION_SAVE_EVERY_REQUEST = False

# CSRF_TRUSTED_ORIGINS: Trusted origins for CSRF protection
# Required when CSRF_COOKIE_SECURE = True and using cross-origin requests
# List domains that are allowed to make POST requests
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
    # Add other trusted domains here
]


# =====================================================
# STEP 3: SECURE HTTP HEADERS
# =====================================================

# X_FRAME_OPTIONS: Clickjacking protection
# Controls whether the site can be embedded in <frame>, <iframe>, or <object>
# Options:
# - 'DENY': Never allow framing (most secure)
# - 'SAMEORIGIN': Allow framing only from same domain
# Prevents attackers from embedding your site in malicious pages
# and tricking users into performing unintended actions
X_FRAME_OPTIONS = 'DENY'

# SECURE_CONTENT_TYPE_NOSNIFF: Prevent MIME-type sniffing
# When True, adds X-Content-Type-Options: nosniff header
# Forces browsers to respect the declared Content-Type
# Prevents browsers from interpreting files as a different MIME type
# Example: Prevents .txt file from being executed as JavaScript
# Protects against attacks where malicious files are uploaded
SECURE_CONTENT_TYPE_NOSNIFF = True

# SECURE_BROWSER_XSS_FILTER: Enable browser XSS protection
# When True, adds X-XSS-Protection: 1; mode=block header
# Enables browser's built-in XSS filter
# If XSS attack is detected, browser blocks the page instead of sanitizing
# NOTE: Modern browsers rely more on CSP, but this provides defense-in-depth
SECURE_BROWSER_XSS_FILTER = True

# SECURE_REFERRER_POLICY: Control Referer header
# Controls how much referrer information is sent with requests
# Options: 'no-referrer', 'no-referrer-when-downgrade', 'origin',
#          'origin-when-cross-origin', 'same-origin', 'strict-origin',
#          'strict-origin-when-cross-origin', 'unsafe-url'
# 'same-origin': Only send referrer for same-origin requests
# Prevents leaking sensitive URLs to external sites
SECURE_REFERRER_POLICY = 'same-origin'


# =====================================================
# STEP 4: CONTENT SECURITY POLICY (CSP)
# =====================================================

# Content Security Policy: Primary defense against XSS attacks
# Defines which sources browsers should consider valid for loading content
# Browsers will only execute/render content from approved sources

# CSP_DEFAULT_SRC: Default policy for all resource types
# 'self': Only allow resources from same origin
CSP_DEFAULT_SRC = ("'self'",)

# CSP_SCRIPT_SRC: Control where JavaScript can be loaded from
# 'self': Only execute scripts from same origin
# Prevents injection of malicious external scripts
CSP_SCRIPT_SRC = ("'self'",)

# CSP_STYLE_SRC: Control where CSS can be loaded from
# 'self': Only load stylesheets from same origin
# 'unsafe-inline': Allow inline styles (use cautiously, reduces security)
# For maximum security, remove 'unsafe-inline' and use external stylesheets
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")

# CSP_IMG_SRC: Control where images can be loaded from
# 'self': Same origin images
# 'data:': Allow data URIs for inline images
# 'https:': Allow images from any HTTPS source
CSP_IMG_SRC = ("'self'", "data:", "https:")

# CSP_FONT_SRC: Control where fonts can be loaded from
# 'self': Only load fonts from same origin
CSP_FONT_SRC = ("'self'",)

# CSP_CONNECT_SRC: Control AJAX, WebSocket, and EventSource connections
# 'self': Only allow connections to same origin
# Prevents data exfiltration to external domains
CSP_CONNECT_SRC = ("'self'",)

# CSP_FRAME_ANCESTORS: Control who can embed this site in frames
# 'none': Prevent all framing (equivalent to X-Frame-Options: DENY)
# Protects against clickjacking
CSP_FRAME_ANCESTORS = ("'none'",)

# CSP_BASE_URI: Restrict URLs that can be used in <base> element
# 'self': Only allow base URLs from same origin
# Prevents attackers from changing base URL to hijack relative URLs
CSP_BASE_URI = ("'self'",)

# CSP_FORM_ACTION: Restrict where forms can submit data
# 'self': Only allow form submissions to same origin
# Prevents forms from submitting data to external sites
CSP_FORM_ACTION = ("'self'",)

# CSP_UPGRADE_INSECURE_REQUESTS: Automatically upgrade HTTP to HTTPS
# Instructs browser to upgrade all HTTP requests to HTTPS
# Provides additional layer of protection
CSP_UPGRADE_INSECURE_REQUESTS = True


# =====================================================
# LOGGING CONFIGURATION FOR SECURITY MONITORING
# =====================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


# =====================================================
# DEVELOPMENT OVERRIDES
# =====================================================

# In development, relax HTTPS requirements
# IMPORTANT: Remove or comment out this section in production
if DEBUG:
    # Disable HTTPS redirects for local development
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False

    # Disable HSTS for development
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

    # Allow all hosts in development
    ALLOWED_HOSTS = ['*']

    # Less strict CSP for development
    CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'")
    CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")


# =====================================================
# SECURITY CHECKLIST FOR PRODUCTION
# =====================================================

"""
Before deploying to production, verify:

1. Environment Variables:
   ✓ SECRET_KEY loaded from environment
   ✓ DEBUG = False
   ✓ Database credentials secured

2. HTTPS Configuration:
   ✓ Valid SSL/TLS certificate installed
   ✓ Web server configured for HTTPS
   ✓ SECURE_SSL_REDIRECT = True
   ✓ SECURE_HSTS_SECONDS = 31536000

3. Cookie Security:
   ✓ SESSION_COOKIE_SECURE = True
   ✓ CSRF_COOKIE_SECURE = True
   ✓ SESSION_COOKIE_HTTPONLY = True

4. Headers:
   ✓ X_FRAME_OPTIONS configured
   ✓ SECURE_CONTENT_TYPE_NOSNIFF = True
   ✓ SECURE_BROWSER_XSS_FILTER = True

5. Content Security Policy:
   ✓ CSP headers configured
   ✓ No 'unsafe-inline' or 'unsafe-eval' in production

6. Additional Checks:
   ✓ ALLOWED_HOSTS properly configured
   ✓ Static files collected (python manage.py collectstatic)
   ✓ Database migrations applied
   ✓ Admin interface secured with strong password
   ✓ Regular security updates applied

7. Testing:
   ✓ Run: python manage.py check --deploy
   ✓ Test all functionality over HTTPS
   ✓ Verify security headers with online tools
   ✓ Check SSL configuration with SSL Labs
"""