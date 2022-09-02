from django.urls import path
from . import views
urlpatterns = [

    # path('users/',views.registeredUsersView,name="users"),
    # path('',views.indexView,name="home"),

    path('users/',views.registeredUsersView,name="users"),
    path('getbulksleepdata/',views.getbulksleepdata,name="getbulksleepdata"),
    path('',views.loginView,name="loginView"),
    path('registrationView/',views.registrationView,name="registrationView"),
    path('access/',views.indexView,name="home"),
    path('viewdata/',views.redirectView,name="viewdata"),
    path('exportsleepdata/',views.exportsleepdata,name="exportsleepdata"),
    path('profiledashboard/',views.profiledashboard,name="profiledashboard"),
    path('getsleepdata/',views.getsleepdata,name="getsleepdata"),
    path('getindivsleepdata/',views.getindivsleepdata,name="getindivsleepdata"),

    # path('dashboard/',views.dashboardView_sleep,name="dashboard1"),
]