"""WanCiZhan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

import users.views
import vocabularies.views

urlpatterns = [
                  path('', users.views.home, name="login"),
                  path('admin/', admin.site.urls),
                  path('back/', users.views.back, name="back"),
                  path('login/', users.views.home, name="login"),
                  path('logout/', users.views.logout, name="logout"),
                  path('login/<slug:kind>', users.views.login, name="login"),
                  path('register/<slug:kind>', users.views.register, name='register'),
                  path('home/', users.views.users_home, name='main_page'),
                  path('home/recite', vocabularies.views.recite_home, name='recite'),
                  path('home/recite/begin', vocabularies.views.recite, name='begin_recite'),
                  path('home/recite/vocabulary', vocabularies.views.recite_vocabulary, name='vocabulary'),
                  path('home/recite/vocabulary/detail/<slug:is_remembered>', vocabularies.views.recite_detail,
                       name='vocabulary_detail'),
                  path('home/recite/finish', vocabularies.views.finish_recite, name='finish_recite'),
                  path('home/display_book', vocabularies.views.display_book, name='display_book'),
                  path('home/display_personal', vocabularies.views.display_personal, name='display_personal'),
                  path('home/display_star', vocabularies.views.display_star, name='display_star'),
                  path('home/recite/vocabulary/star/<slug:condition>', vocabularies.views.star, name='star'),
                  path('home/recite/vocabulary/detail', vocabularies.views.recite_detail_noarg,
                       name='vocabulary_detail'),
                  path('home/display_r_line', vocabularies.views.display_r_line, name='display_r_line'),
                  path('home/test', vocabularies.views.test, name='test'),
                  path('home/test/begin', vocabularies.views.begin_test_noarg, name='begin_test'),
                  path('home/test/begin/<slug:is_correct>', vocabularies.views.begin_test, name='begin_test'),
                  path('home/test/finish_test', vocabularies.views.finish_test, name='finish_test'),
                  path('home/add_vocabulary', vocabularies.views.add_vocabulary_admin, name='add_vocabulary'),
                  path('home/distribute_vocabulary', vocabularies.views.distribute_vocabulary_admin,
                       name='distribute_vocabulary'),
                  path('home/delete_user', users.views.delete_user, name='delete_user'),
                  path('home/detail/<slug:vocabulary>', vocabularies.views.vocabulary_detail,
                       name='vocabulary_detail_extra')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
