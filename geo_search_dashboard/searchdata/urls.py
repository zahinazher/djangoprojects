from django.urls import path, include

from . import views

app_name = 'clickad'
urlpatterns = [
    path(r'index.*', views.index, name="index.html"),
    path(r'get_topics_ajax', views.get_topics_ajax, name="get_topics_ajax"),
    path('', views.IndexView.as_view(), name='index'),
    path('index.html', views.IndexView.as_view(), name='index'),
    path('filter/', views.DataFilterView.as_view(), name='filter'),
    path('details/<int:id>/', views.DataDetailsView.as_view(), name='data_detail'),
    # path('get /clickad/adsclick', views.IndexView.as_view(), name = "index"),
    # path(r'^upload/csv/$', views.upload_csv, name='upload_csv'),
    # path('tables', views.datatable, name='tables'),
]
