from pathlib import Path
import environ
import os

# Set Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize Environment Variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))  # ✅ Always load .env

# Debug Settings
DEBUG = env.bool("DEBUG", default=True)

# Secret Key
SECRET_KEY = env("SECRET_KEY", default="django-insecure-default-key")

# Allowed Hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# Application Definition
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",  # Add WhiteNoise here
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your Apps
    'Leads',
    'agents',

    # Third-party Apps
    'crispy_forms',
    'crispy_tailwind',
]

# Middleware
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'DJCRM.urls'

# Templates
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

# WSGI
WSGI_APPLICATION = 'DJCRM.wsgi.application'

# Database Configuration (with default values)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DB_NAME", default="djcrm"),
        'USER': env("DB_USER", default="djcrmuser"),
        'PASSWORD': env("DB_PASSWORD", default="djcrm1234"),
        'HOST': env("DB_HOST", default="localhost"),
        'PORT': env("DB_PORT", default="5432"),
    }
}

# Authentication
AUTH_USER_MODEL = 'Leads.User'

# Email Backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Login & Logout
LOGIN_REDIRECT_URL = "/Leads"
LOGOUT_REDIRECT_URL = "/Leads"
LOGIN_URL = "/login"

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "static_root"
# for whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# these setting are used in production
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = "DENY"


ALLOWED_HOSTS = ["*"]
# run the command
# pip install gunicorn
# pip freeze > requirements.txt
# gunicorn DJCRM.wsgi:application