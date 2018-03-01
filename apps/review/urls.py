from django.conf.urls import url
from . import views 
urlpatterns = [
    url(r'^$', views.index),
    url(r'^regi', views.regi),
    url(r'^books', views.books),
    url(r'^login', views.login),
    url(r'^add_book', views.add),
    url(r'^logout', views.logout),
    url(r'^adding_book', views.adding_book),
    url(r'^add_review', views.add_review),
    url(r'^book/(?P<num>\d+)', views.reviewz),
    url(r'^users/(?P<num>\d+)', views.myspace),
]