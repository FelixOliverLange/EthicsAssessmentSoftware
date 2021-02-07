"""EthikBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

# For details about the include, see https://docs.djangoproject.com/en/3.1/topics/http/urls/#including-other-urlconfs
# If it makes problems, either include the urls.py directly and rework the view pointers, or attempt solving this.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('EthicAssessmentSoftware.urls'))
]
