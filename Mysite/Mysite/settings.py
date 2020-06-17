"""
Django settings for Mysite project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i+7y^1bsbb1ta04u!!4n*64dppqcmdd4f%h0by0b#i_v!+*%w5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'home',
    'station_data_overview',
    'register',
    'share_resource',
    'require',
    'manager_perf',
]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',  # redis缓存中间件
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware', # redis缓存中间件
]

CACHE_MIDDLEWARE_SECONDS = 24*60*60     # 每个页面缓存的时间(单位:秒)
CACHE_MIDDLEWARE_ALIAS= 'default'     # 缓存别名

ROOT_URLCONF = 'Mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['C:/Users/Administrator/PycharmProjects/web_0.0/Mysite/templates'],
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

WSGI_APPLICATION = 'Mysite.wsgi.application'


# Build Caches use redis

CACHES = {
    'default':{
        'BACKEND':'django_redis.cache.RedisCache',
        'LOCATION':'redis://192.168.8.247:6379',
        'OPTIONS':{
            'CLIENT_CLASS':'django_redis.client.DefaultClient',
            'PASSWORD':'chy910624',
        },
    },
}


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite',  #数据库名称
        'USER':'ramsey',         #数据库用户名
        'PASSWORD':'chy910624',  #数据库密码
        'HOST':'',               #数据库主机，留空默认为localhost
        'PORT':'3306',           #数据库端口
    },
    'ad_server':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'team_station',  # 广告组服务器数据库名称
        'USER': 'marmot',  # 数据库用户名
        'PASSWORD': '',  # 数据库密码
        'HOST': 'wuhan.yibai-it.com',  # 数据库主机，留空默认为localhost
        'PORT': '33061',  # 数据库端口
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    (os.path.join(BASE_DIR,'static')),
]

# set email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False   #是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性。)
EMAIL_USE_SSL = False    #是否使用SSL加密，qq企业邮箱不要求使用
EMAIL_HOST = 'smtp.qq.com'   #发送邮件的邮箱 的 SMTP服务器，这里用了163邮箱
EMAIL_PORT = 25     #发件箱的SMTP服务器端口
EMAIL_HOST_USER = '1579922399@qq.com'    #发送邮件的邮箱地址
EMAIL_HOST_PASSWORD = 'zpzwxdsuvksugjdc'         #发送邮件的邮箱密码(这里使用的是授权码)