from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
        url(r'^$', views.display_login),
        url(r'^reg_process$', views.reg_process),
        url(r'^login_process$', views.login_process),
        url(r'^user/(?P<user_id>\d+)$', views.user_dashboard),
        url(r'^logout_process$', views.logout_process),
        url(r'^books$', views.display_books),
        url(r'^create_book$', views.book_form),
        url(r'^process_book$', views.process_book),
        url(r'^books/(?P<book_id>\d+)$', views.display_book),
]