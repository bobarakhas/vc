"""
URL configuration for head project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signin, name='signin'),
    path('wallet/', views.wallet, name='wallet'),
    path('history/', views.history, name='history'),
    path('send/', views.send, name='send'),
    path('sendto/<str:sendto>/', views.sendto, name='sendto'),
    path('receive/', views.receive, name='receive'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('connect/<str:connect>/', views.connect, name='connect'),
    path('transaction/', views.transaction, name='transaction'),
    path('transaction/<str:transaction>/', views.transactiondetail, name='transactiondetail'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
]

urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)