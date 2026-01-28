# Django Security Implementation Documentation

## Overview
This document details all security measures implemented in the Bookshelf Django application to protect against common web vulnerabilities.

---

## 1. Secure Settings Configuration

### DEBUG Mode
```python
DEBUG = False  # In production
```
**Why**: Prevents sensitive information disclosure like stack traces, settings, and SQL queries.

### Browser Security Headers

#### SECURE_BROWSER_XSS_FILTER = True
**Purpose**: Enables browser's built-in XSS filter  
**Protection**: Prevents reflected XSS attacks  
**How it works**: Browser detects and blocks page if XSS attack detected

#### X_FRAME_OPTIONS = 'DENY'
**Purpose**: Prevents clickjacking attacks  
**Protection**: Prevents site from being embedded in iframes  
**Alternative**: Use 'SAMEORIGIN' to allow same-domain framing

#### SECURE_CONTENT_TYPE_NOSNIFF = True
**Purpose**: Prevents MIME-type sniffing  
**Protection**: Forces browser to respect declared content-type  
**Why**: Prevents malicious file uploads from being executed

### HTTPS/SSL Security

#### CSRF_COOKIE_SECURE = True
**Purpose**: CSRF cookie only sent over HTTPS  
**Protection**: Prevents CSRF token interception  
**Requirement**: Must have HTTPS enabled

#### SESSION_COOKIE_SECURE = True
**Purpose**: Session cookie only sent over HTTPS  
**Protection**: Prevents session hijacking  
**Requirement**: Must have HTTPS enabled

#### SECURE_SSL_REDIRECT = True
**Purpose**: Redirects all HTTP to HTTPS  
**Protection**: Ensures all traffic is encrypted  
**Note**: Configure after HTTPS is set up

#### SECURE_HSTS_SECONDS = 31536000
**Purpose**: HTTP Strict Transport Security  
**Protection**: Forces HTTPS for 1 year  
**Benefit**: Prevents protocol downgrade attacks

### Cookie Security

#### SESSION_COOKIE_HTTPONLY = True
**Purpose**: JavaScript cannot access session cookie  
**Protection**: Prevents XSS from stealing sessions  
**Critical**: Essential XSS mitigation

#### SESSION_COOKIE_SAMESITE = 'Strict'
**Purpose**: Cookie sent only to same-site requests  
**Protection**: Prevents CSRF attacks  
**Options**: 'Strict', 'Lax', or 'None'

---

## 2. Content Security Policy (CSP)

### CSP Configuration
```python
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
```

**Purpose**: Controls which resources can be loaded  
**Protection**: Primary defense against XSS attacks  
**How it works**: Browser only loads content from approved sources

### CSP Directives Explained:
- **default-src**: Fallback for all resource types
- **script-src**: Controls JavaScript sources
- **style-src**: Controls CSS sources
- **img-src**: Controls image sources
- **frame-ancestors**: Controls embedding (clickjacking prevention)

---

## 3. CSRF Protection

### Implementation
All POST forms include: `{% csrf_token %}`

### How CSRF Protection Works:
1. Django generates unique token per session
2. Token embedded in form as hidden field
3. Server validates token on POST request
4. Request rejected if token missing/invalid

### Code Example:
```html
<form method="post">
    {% csrf_token %}  <!-- Required! -->
    <input type="text" name="username">
    <button type="submit">Submit</button>
</form>
```

### Decorators:
```python
from django.views.decorators.csrf import csrf_protect

@csrf_protect  # Explicitly enforce CSRF
def my_view(request):
    pass
```

---

## 4. SQL Injection Prevention

### Django ORM Usage
**SECURE (Use Django ORM):**
```python
# Parameterized query - safe
users = User.objects.filter(username=user_input)

# Q objects for complex queries - safe
users = User.objects.filter(
    Q(username__icontains=search) |
    Q(email__icontains=search)
)
```

**INSECURE (Never do this):**
```python
# String formatting - VULNERABLE!
query = f"SELECT * FROM users WHERE username = '{user_input}'"
cursor.execute(query)
```

### Why ORM is Safe:
- Automatically parameterizes queries
- Escapes special characters
- Prevents SQL injection by design

### Input Validation:
```python
# Validate length
if len(username) > 150:
    return error_response

# Sanitize input
username = username.strip()[:150]
```

---

## 5. XSS Prevention

### Django Auto-Escaping
Django templates automatically escape variables:
```html
<!-- Automatic escaping -->
<p>{{ user_input }}</p>

<!-- Explicit escaping (optional) -->
<p>{{ user_input|escape }}</p>
```

### What Gets Escaped:
- `<` becomes `&lt;`
- `>` becomes `&gt;`
- `'` becomes `&#x27;`
- `"` becomes `&quot;`
- `&` becomes `&amp;`

### Manual Escaping in Views:
```python
from django.utils.html import escape

safe_output = escape(user_input)
```

### CSP as Additional Layer:
Even if XSS payload gets through, CSP prevents execution by blocking inline scripts.

---

## 6. Secure Password Handling

### Using create_user():
```python
# SECURE - Password automatically hashed
User.objects.create_user(
    username=username,
    email=email,
    password=password  # Hashed with PBKDF2
)
```

**Never store plain text passwords!**

### Password Validators:
```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'UserAttributeSimilarityValidator'},  # Not similar to username
    {'NAME': 'MinimumLengthValidator'},            # Min 8 characters
    {'NAME': 'CommonPasswordValidator'},           # Not in common list
    {'NAME': 'NumericPasswordValidator'},          # Not all numeric
]
```

---

## 7. Authorization & Permissions

### View Protection:
```python
@login_required  # Must be authenticated
@permission_required('bookshelf.can_view', raise_exception=True)
def secure_view(request):
    pass
```

### Prevents:
- Unauthorized access
- Privilege escalation
- Information disclosure

---

## 8. Logging & Monitoring

### Security Logging:
```python
import logging
logger = logging.getLogger(__name__)

# Log security events
logger.info(f"User {user.username} accessed sensitive data")
logger.warning(f"Failed login attempt for {username}")
logger.error(f"Potential attack detected: {attack_pattern}")
```

### What to Log:
- Authentication attempts (success/failure)
- Permission denials
- Data modifications
- Suspicious patterns

---

## 9. Input Validation Best Practices

### Always Validate:
1. **Length**: Prevent buffer overflow/DoS
2. **Type**: Ensure correct data type
3. **Format**: Email, phone, etc.
4. **Range**: Numbers within acceptable bounds

### Example:
```python
# Validate email
if '@' not in email or len(email) > 254:
    return error_response

# Validate numeric range
if not 1 <= age <= 120:
    return error_response
```

---

## 10. Testing Security Measures

### Manual Tests:

#### Test CSRF Protection:
1. Remove `{% csrf_token %}` from form
2. Submit form
3. Should receive 403 Forbidden

#### Test XSS Prevention:
1. Input: `<script>alert('XSS')</script>`
2. Should display as text, not execute
3. Check page source - should be escaped

#### Test SQL Injection:
1. Input: `' OR '1'='1`
2. Should return no results or error
3. Should not expose data

#### Test Permission Enforcement:
1. Login as user without permission
2. Try to access restricted view
3. Should receive 403 Forbidden

### Automated Testing:
```python
from django.test import TestCase

class SecurityTestCase(TestCase):
    def test_csrf_protection(self):
        response = self.client.post('/create/', {})
        self.assertEqual(response.status_code, 403)
    
    def test_xss_prevention(self):
        response = self.client.get('/?q=<script>alert(1)</script>')
        self.assertNotContains(response, '<script>')
```

---

## 11. Production Checklist

Before deploying to production:

- [ ] DEBUG = False
- [ ] SECRET_KEY from environment variable
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] All security headers enabled
- [ ] CSP configured
- [ ] Database backups enabled
- [ ] Logging configured
- [ ] Security updates applied
- [ ] Dependency audit completed

---

## 12. Common Vulnerabilities & Mitigations

| Vulnerability | Mitigation | Implementation |
|---------------|------------|----------------|
| SQL Injection | Use Django ORM | ✓ Implemented |
| XSS | Auto-escaping + CSP | ✓ Implemented |
| CSRF | CSRF tokens | ✓ Implemented |
| Clickjacking | X-Frame-Options | ✓ Implemented |
| Session Hijacking | Secure cookies + HTTPS | ✓ Implemented |
| MITM Attacks | HTTPS + HSTS | ✓ Implemented |

---

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)