from django.urls import path
from . import views

urlpatterns=[
    path('admin-login/',views.login,name='admin-login'),
    path('admin-dashboard/',views.AdminDashboard.as_view(),name='admin-dashboard'),
    path('admin-logout/',views.Admin_logout,name='admin-logout'),
    path('forgot-password/',views.Forget_password.as_view(),name='forgot-password'),
    path('change-password/',views.Change_password.as_view(),name='change-password'),
################################   Users Show   ########################
    path('add-users/',views.Add_Users.as_view(),name='add-users'),
    path('edit-users/<int:id>',views.Edit_Users.as_view(),name='edit-users'),
    path('show-users/',views.Show_Users.as_view(),name='show-users'),
    path('delete-users/<int:id>',views.Delete_Users,name='delete-users'),
    path('show-profile/<int:id>',views.Show_Profile,name='show-profile'),
    path('active-inactive/',views.Active_inActive.as_view(),name='active-inactive'),
    path('edit-admin/<int:id>',views.Edit_Admin.as_view(),name='edit-admin'),
   
#######################  Restaurants Show #################

    path('add-restaurant/',views.Add_Rastaurant.as_view(),name='add-restaurant'),
    path('show-restaurant/',views.Show_Restaurant.as_view(),name='show-restaurant'),
    path('detail-restaurant/<int:id>',views.Restaurant_detail.as_view(),name='detail-restaurant'),
    path('payament_details',views.User_Payment.as_view(),name='payament_details'),
    path('delete-restaurant/<int:id>',views.Delete_Restaurant,name='delete-restaurant'),
    path('restaurant-active-inactive/',views.Restaurant_Active_inActive.as_view(),name='restaurant-active-inactive'),

    

    path('add-subscription',views.Add_SubscriptionsDetails.as_view(),name='add-subscription'),
    path('show-subscription',views.Show_SubscriptionsDetails.as_view(),name='show-subscription'),
    path('edit-subscription/<int:id>',views.Edit_SubscriptionsDetails.as_view(),name='edit-subscription'),
    path('delete-subscription/<int:id>',views.delete_subscriptionsdetails,name='delete-subscription'),


    path('sent-notification/',views.Add_Notifiactions.as_view(),name='sent-notification'),
    path('show-notification/',views.Notifiactions_show.as_view(),name='show-notification'),
    path('delete-notification/<int:id>',views.delete_notifications,name='delete-notification'),
    path('delete-all-notification/',views.delete_all_notifications,name='delete-all-notification'),
    path('404/', views.handler404, name='handler404'),
]
