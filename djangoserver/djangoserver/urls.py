"""djangoserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework.documentation import include_docs_urls

from djangoserver.session import SessionAuthentication

urlpatterns = [
    path('admin/', admin.site.urls),
    path('poetry/', include('miniprogram.urls')),
    url(r'api-auth', include("rest_framework.urls", namespace="reset_framework")),
    url(r'docs/', include_docs_urls(title='接口文档', authentication_classes=[], permission_classes=[])),
]
