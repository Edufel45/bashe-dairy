import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
ON_VERCEL = bool(os.environ.get("VERCEL"))
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
DEBUG = os.environ.get("DEBUG", "0" if ON_VERCEL else "1") == "1"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", ".vercel.app,bashedairy.co.tz,www.bashedairy.co.tz,localhost,127.0.0.1").split(",")
CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app", "https://bashedairy.co.tz", "https://www.bashedairy.co.tz"]
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "django.contrib.sitemaps", "shop"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True,
    "OPTIONS": {"context_processors": ["django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
if os.environ.get("DATABASE_URL"):  # Neon / Supabase Postgres (required on Vercel)
    import dj_database_url
    DATABASES["default"] = dj_database_url.parse(os.environ["DATABASE_URL"], conn_max_age=0, ssl_require=True)
AUTH_PASSWORD_VALIDATORS = []
TIME_ZONE = "Africa/Dar_es_Salaam"; USE_TZ = True
STATIC_URL = "/static/"; STATIC_ROOT = BASE_DIR / "staticfiles"
WHITENOISE_USE_FINDERS = True; WHITENOISE_MAX_AGE = 31536000   # no collectstatic needed on Vercel
STORAGES = {"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}
MEDIA_URL = "/media/"; MEDIA_ROOT = BASE_DIR / "media"
USE_CLOUD_MEDIA = bool(os.environ.get("CLOUDINARY_URL"))  # Vercel disk is read-only: uploads go to Cloudinary
if USE_CLOUD_MEDIA:
    INSTALLED_APPS = ["cloudinary_storage"] + INSTALLED_APPS + ["cloudinary"]
    STORAGES["default"] = {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
if not DEBUG:
    SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
