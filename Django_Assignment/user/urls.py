from django.urls import path,include
from .views import *

urlpatterns = [
    # path('users/', views.create_user),
    # path('users/', views.get_users),
    # # path('users/getdata/', views.get_users),
    # path('users/update/<int:pk>/', views.update_user),
    # path('users/delete/<int:pk>/', views.delete_user),
    # path('users/getuser/<int:pk>/', views.get_user_by_id),
    path('users/<int:id>/', UserOperationsView.as_view(), name='user_detail'),
    path('users/', UserListCreateView.as_view(), name='user_list'),
    
]

