"""Mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# 路由是浏览器输入url，在Django服务器响应url的转发中心。
# 路由都写在urls文件里，它将浏览器输入的url映射到相应的业务处理逻辑也就是视图

from django.contrib import admin
from django.urls import path,include
from login import views as login_views
from home import views as home_views
from register import views as register_views
from station_data_overview import views as overviews
from share_resource import views as share_overviews
from require import views as require_views
from manager_perf import views as manager_views
from . import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('share/', share_overviews.share),
    path('share/<file_name>/', share_overviews.download),
    path('login/', cache_page(60)(login_views.login)),
    path('home/', home_views.home_page),
    path('', home_views.home_page),
    path('overview/', include('station_data_overview.urls')),
    path('register/', cache_page(60)(register_views.register)),
    path('require/',require_views.require),
    path('managerperf/',include('manager_perf.urls'))
]
