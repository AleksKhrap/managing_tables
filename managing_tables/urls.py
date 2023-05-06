from django.urls import path
from . import views


app_name = 'managing_tables'
urlpatterns = [
    path('', views.index, name='index'),
    path('tables/', views.tables, name='tables'),
    path('tables/<int:table_id>/', views.table, name='table'),
    path('new_table/', views.new_table, name='new_table'),
    path('edit_table/<int:participant_id>/', views.edit_table, name='edit_table'),
    path('new_participant/<int:table_id>/', views.new_participant, name='new_participant'),
    path('delete_table/<int:table_id>/', views.delete_table, name='delete_table'),
    path('delete_participant/<int:participant_id>/', views.delete_participant, name='delete_participant'),
    path('all_users_tables/', views.all_users_tables, name='all_users_tables'),
]


