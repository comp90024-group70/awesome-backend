"""
URL configuration for couch_demo_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from .views import *

urlpatterns = [
    path('health', health_check, name='check connection status'),
    path('twitter/sentiment', sentiment_analysis, name="satisfactory"),
    path('ado/family', get_ado_family, name='get the ado family'),
    path('ado/job', get_ado_job, name='get the ado job'),
    path('sa4/family', get_sa4_family, name='get the sa4 family'),
    path('sa4/job', get_sa4_job, name='get the sa4 job'),
    path('twitter/topics', get_twitter_topics, name='get the twitter topics'),
    path('twitter/treemap', get_treemap, name='get the twitter treemap'),
    path('mastodon/recent', get_mas, name='get the twitter treemap'),
    path("mastodon/count", mastodon_count, name="get the mastodon count"),
    path("twitter/count", twitter_count, name="get the twitter clean count"),
]
