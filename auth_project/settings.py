import os
from pathlib import Path
import environ
import pymysql

pymysql.install_as_MySQLdb()

# ===============================================================
# BASE DIR
# ===============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===============================================================
# ENV CONFIG
# ===============================================================
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
)

# Read .env (local only, Azure uses App Settings)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ===============================================================
# CORE SETTINGS
# ===============================================================
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)

# ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(",")
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=["*"]  # temporary safe fallback for Azure
)

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ===============================================================
# API KEYS
# ===============================================================
NEWS_API_KEY = env("NEWS_API_KEY", default="")

AZURE_OPENAI_API_KEY = env("AZURE_OPENAI_API_KEY", default="")
AZURE_OPENAI_ENDPOINT = env("AZURE_OPENAI_ENDPOINT", default="")
AZURE_OPENAI_API_VERSION = env("AZURE_OPENAI_API_VERSION", default="")
AZURE_OPENAI_DEPLOYMENT = env("AZURE_OPENAI_DEPLOYMENT", default="")
AZURE_OPENAI_DEPLOYMENT_NAME = env("AZURE_OPENAI_DEPLOYMENT_NAME", default="")

# ===============================================================
# DATABASE (MYSQL / AZURE MYSQL)
# ===============================================================
USE_AZURE_MYSQL = env("USE_AZURE_MYSQL", default="false").lower() == "true"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}

if USE_AZURE_MYSQL:
    DATABASES["default"]["OPTIONS"]["ssl"] = {
        "ca": str(BASE_DIR / "certificate" / "DigiCertGlobalRootG2.crt.pem")
    }

# ===============================================================
# EMAIL (PRODUCTION SAFE)
# ===============================================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = "ZeroRiskTrader <zerorisktrader.app@gmail.com>"
EMAIL_TIMEOUT = 10
# ===============================================================
# AUTH
# ===============================================================
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"

# ===============================================================
# APPS
# ===============================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "auth_app",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# ===============================================================
# MIDDLEWARE
# ===============================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ===============================================================
# URLS / WSGI
# ===============================================================
ROOT_URLCONF = "auth_project.urls"
WSGI_APPLICATION = "auth_project.wsgi.application"

# ===============================================================
# TEMPLATES
# ===============================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ===============================================================
# PASSWORD VALIDATION
# ===============================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===============================================================
# I18N
# ===============================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ===============================================================
# STATIC / MEDIA
# ===============================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

MEDIA_ROOT = BASE_DIR / "media"

# ===============================================================
# DEFAULT PK
# ===============================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===============================================================
# SECURITY (PRODUCTION)
# ===============================================================
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
