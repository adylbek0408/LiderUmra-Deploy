import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost", "liderumra.kg", "www.liderumra.kg"])

# ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["liderumra.kg", "www.liderumra.kg"])

INSTALLED_APPS = [
    'modeltranslation',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'ckeditor',
    'django_filters',
    'phonenumber_field',
    'corsheaders',
    'drf_yasg',

    'apps.tour',
    'apps.crm',
    'apps.blog',
]

SITE_ID = 1  # Добавлено для корректной работы

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'UMRA.middleware.LanguageHeaderMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'UMRA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'UMRA.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ky'
TIME_ZONE = "Asia/Bishkek"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('ky', 'Kyrgyz'),
    ('ru', 'Russian'),
)

DEFAULT_LANGUAGE = 'ky'
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ky'

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_GROUP_IDS = {
    'Bishkek': os.getenv('TELEGRAM_GROUP_BISHKEK'),
    'Osh': os.getenv('TELEGRAM_GROUP_OSH'),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
}

CSRF_TRUSTED_ORIGINS = [
    "https://www.liderumra.kg",
    "https://liderumra.kg",
]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://liderumra.kg",
    "https://www.liderumra.kg"
]

CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type', 'dnt',
    'origin', 'user-agent', 'x-csrftoken', 'x-requested-with'
]
CORS_EXPOSE_HEADERS = ['Content-Length', 'X-CSRFToken', 'Access-Control-Allow-Origin']
CORS_ALLOW_CREDENTIALS = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'OPERATIONS_SORTER': 'alpha',
}

JAZZMIN_SETTINGS = {
    "site_title": "Lider Umra",
    "site_header": "Lider Umra",
    "site_brand": "Lider Umra",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Добро пожаловать в администратора Lider Umra",
    "copyright": "Lider Umra © 2023-2025",
    "user_avatar": None,
    "show_sidebar": True,
    "navigation_expanded": True,
    "sidebar_fixed": True,
    "sidebar_collapsible": True,
    "custom_links": {
        "tour": [{
            "name": "Панель мониторинга",
            "url": "admin:index",
            "icon": "fas fa-tachometer-alt",
        }],
    },
    "icons": {
        # Auth
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",

        # CRM
        "crm.Client": "fas fa-user-tag",
        "crm.Manager": "fas fa-user-tie",

        # Blog
        "blog": "fas fa-blog",  # Иконка для всего приложения "blog"
        "blog.Post": "fas fa-blog",  # Блоги (иконка блога)
        "blog.Blog": "fas fa-newspaper",  # Блоги
        "blog.Lesson": "fas fa-video",  # Уроки (видеоуроки)
        "blog.Gallery": "fas fa-camera-retro",  # Фотогалерея (камера)
        "blog.Photo": "fas fa-images",  # Фотогалерея (раньше было "Gallery", но модели такой нет)
        "blog.FAQ": "fas fa-question-circle",  # Часто задаваемые вопросы

        # Tour
        "tour": "fas fa-route",  # Общая иконка для приложения "tour"
        "tour.Ajy": "fas fa-user-friends",  # Ажы (группа людей / лидер)
        "tour.PackageDetail": "fas fa-box",  # Детали пакетов
        "tour.PackageCategory": "fas fa-layer-group",  # Категории пакетов (группировка)
        "tour.CategoryPackage": "fas fa-tags",  # Категория пакетов (исправлено)
        "tour.Hotel": "fas fa-hotel",  # Отели
        "tour.Package": "fas fa-box-open",  # Пакеты
        "tour.TourDate": "fas fa-calendar-alt",  # Туры даты (время/дата)
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "related_modal_back": False,
    "hide_apps": [],
    "hide_models": [],
    "changeform_format": "horizontal_tabs",
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
}
