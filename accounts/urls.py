from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [

    # path('users/',views.registeredUsersView,name="users"),
    # path('',views.indexView,name="home"),

    path('',views.registeredUsersView,name="users"),
    path('getbulksleepdata/',views.getbulksleepdata,name="getbulksleepdata"),
    path('login/',views.loginView,name="loginView"),
    path('access/',views.indexView,name="home"),
    path('viewdata/',views.redirectView,name="viewdata"),
    path('exportsleepdata/',views.exportsleepdata,name="exportsleepdata"),
    path('profiledashboard/',views.profiledashboard,name="profiledashboard"),
    path('getsleepdata/',views.getsleepdata,name="getsleepdata"),
   
    # path('dashboard/',views.dashboardView_sleep,name="dashboard1"),
]