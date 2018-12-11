from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns=[
    path('form/',views.View_city, name="form"),
    path('matching/',views.matching,name='matching'),
    url(r'^sendr/$',views.sendr,name='sendr'),
    url(r'^acceptr/$',views.acceptr,name='acceptr'),
    url(r'^decliner/$',views.decliner,name='decliner'),

]
