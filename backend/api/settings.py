"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os, json, datetime
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

APPEND_SLASH = False # 추가 안해줄시 기본값이 True인데 그 경우 urls.py에서 경로설정시 주소 끝에 /를 붙이고 
#해당경로로 /를 붙이지 않고 접속시 페이지를 찾을 수 없기때문에 리다이렉트를 시켜 자동으로 /를 붙여서 경로를 찾는다.
#이 경우 문제가 될 수 있기때문에 false로 값을 지정해줬다.

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user', # 추가
    'rest_framework', # 추가
    'rest_framework_jwt', # 추가
    'corsheaders', # 추가
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',     # 추가
    'django.middleware.common.CommonMiddleware', # 추가
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = ['http://localhost:3000'] #아까 설치한 corsheaders로 해당 서버와 연결할 서버의 url을 작성해준모습

REST_FRAMEWORK = { # 추가
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  #인증된 회원만 액세스 허용
        'rest_framework.permissions.AllowAny',         #모든 회원 액세스 허용
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': ( #api가 실행됬을 때 인증할 클래스를 정의해주는데 우리는 JWT를 쓰기로 했으니
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication', #이와 같이 추가해준 모습이다.
    ),
}

JWT_AUTH = { # 추가
   'JWT_SECRET_KEY': SECRET_KEY,
   'JWT_ALGORITHM': 'HS256',
   'JWT_VERIFY_EXPIRATION' : True, #토큰검증
   'JWT_ALLOW_REFRESH': True, #유효기간이 지나면 새로운 토큰반환의 refresh
   'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=30),  # Access Token의 만료 시간
   'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=3), # Refresh Token의 만료 시간
   'JWT_RESPONSE_PAYLOAD_HANDLER': 'api.custom_responses.my_jwt_response_handler'
}





ROOT_URLCONF = 'api.urls'

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

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]






# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul' # 후에 작성한 게시물에 날짜를 표현하기 위해서 
USE_TZ = False  #Use_TZ를 false로 설정해서 우리나라 시간을 가져온 모습이다.

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static') #개발자가 관리하는 파일들 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') #사용자가 업로드한 파일 관리

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
