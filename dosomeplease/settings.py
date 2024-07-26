"""
Django settings for dosomeplease project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-35vn5@1i1bu%*0=j7_ej6v8tp(nik$p(&#oo(gl^zjghrf9f)c"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mentalhealth",  #我們的應用程式
    'hitcount',
    'django_filters', # 新增搜尋的部分
    'mdeditor',
]

#filters
REST_FRAMEWORK = {
  'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
#USER保留，新增欄位
AUTH_USER_MODEL = 'mentalhealth.Profile'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dosomeplease.urls"
import os
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "dosomeplease.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "zh-hant"

TIME_ZONE = "Asia/Taipei"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_FINDERS = [
#      'django.contrib.staticfiles.finders.FileSystemFinder',
#      'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
#      'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#  ]

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# django-mdeditor 设置
MDEDITOR_CONFIGS = {
    'default':{
        'width': '100%',  # Custom edit box width
        'height': 500,  # Custom edit box height
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
                    "emoji", "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar 
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # image upload format type
        'image_folder': 'editor',  # 图片保存路径
        'theme': 'dark',  # 工具栏显示主题, dark / default
        'preview_theme': 'default',  # 预览区显示主题, dark / default
        'editor_theme': 'default',  # 编辑区显示主题, pastel-on-dark / default
        'toolbar_autofixed': True,  # 工具栏是否固定在顶部
        'search_replace': True,  # 是否打开搜索替换 
        'emoji': True,  # 是否打开表情显示
        'tex': True,  # 是否打开 tex 图表显示
        'flow_chart': True,  # 是否打开流程图显示
        'sequence': True, # 是否打开时序图显示
        'watch': True,  # 实时预览
        'lineWrapping': True,  # 是否换行
        'lineNumbers': True,  # 是否显示行数
        'language': 'zh'  # 语言
    }
}
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#SMTP Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com" #SMTP伺服器
EMAIL_PORT = 587  #TLS通訊埠號
EMAIL_USE_TLS = True #開啟TLS(傳輸層安全性)
EMAIL_HOST_USER = "dusum1129@gmail.com" #寄件者電子郵件
EMAIL_HOST_PASSWORD = "riau ddso vhtb ckgu" #Gmail應用程式的密碼

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

X_FRAME_OPTIONS = 'SAMEORIGIN'  # 针对django3.0+修改 frame 配置 + 默认为 deny