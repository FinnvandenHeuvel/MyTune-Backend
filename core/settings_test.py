from . import settings as base

# --- start with all base settings ---
SECRET_KEY = base.SECRET_KEY
DEBUG = False
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = base.INSTALLED_APPS
MIDDLEWARE = base.MIDDLEWARE
TEMPLATES = base.TEMPLATES

# If you have these in base settings, keep them too
ROOT_URLCONF = getattr(base, "ROOT_URLCONF", None)
WSGI_APPLICATION = getattr(base, "WSGI_APPLICATION", None)
ASGI_APPLICATION = getattr(base, "ASGI_APPLICATION", None)

LANGUAGE_CODE = getattr(base, "LANGUAGE_CODE", "en-us")
TIME_ZONE = getattr(base, "TIME_ZONE", "UTC")
USE_I18N = getattr(base, "USE_I18N", True)
USE_TZ = getattr(base, "USE_TZ", True)

STATIC_URL = getattr(base, "STATIC_URL", "static/")
DEFAULT_AUTO_FIELD = getattr(
    base, "DEFAULT_AUTO_FIELD", "django.db.models.BigAutoField"
)

# --- override DB for tests (SQLite) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": base.BASE_DIR / "test_db.sqlite3",
    }
}

# --- speed up tests ---
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
