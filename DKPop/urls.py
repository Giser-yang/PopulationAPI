from django.urls import path
from DKPop import views
# from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # path('token/', views.get_token),
    # path('gettoken/', views.user_login),
    path('exampleinfo/', views.get_info),
    path('dkinfo/', views.dkdata),
    path('getjson/', views.query_cqrk)
]
