from django.urls import path ,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[

    path('',views.User_Login.as_view(),name='user-login'),
    path('user-registration/',views.UserRegistration.as_view(),name='user-registration'),
    path('user-dashboard/',views.UserDashboard.as_view(),name='user-dashboard'),
    path('change-user-password/',views.Change_password.as_view(),name='change-user-password'),
    # path('edit-user-profile/<int:id>',views.Edit_Users_Profile.as_view(),name='edit-users-profile'),
    # path('add-restaurant-details/',views.Add_Restaurant_Deltails.as_view(),name='add-restaurant-details'),
  
    
    path('restaurant-details/',views.Restaurant_details.as_view(),name='restaurant-details'),
 
    path('subscription/',views.User_Subscription.as_view(),name='subscription'),
    path('Payment/',views.Payment.as_view(),name='Payment'),
    path('user-logout/',views.userlogout,name='user-logout'),
    # path('user-forgot-password/',views.Forget_password.as_view(),name='user-forgot-password'),
    

#############################Categorties######################
    path('add-category/',views.Add_Category.as_view(),name='add-category'),
    path('show-category/',views.Show_Category.as_view(),name='show-category'),
    path('edit-category/<int:id>',views.Edit_Category.as_view(),name='edit-category'),
    path('delete-category/<int:id>',views.delete_category,name='delete-category'),
    path('show-category-image/',views.Show_cat_image.as_view()),


############################Add Food item #################
    path('add-item/<int:id>',views.Add_Item.as_view(),name='add-item'),
    path('add-once/<int:id>',views.Add_Once.as_view(),name='add-once'),
    path('delete-add-once/<int:id>',views.Delete_Add_Once.as_view(),name='delete-add-once'),
    path('show-item/<int:id>',views.Show_Item.as_view(),name='show-item'),
    path('edit-item/<int:id>',views.Edit_Item.as_view(),name='edit-item'),
    path('delete-item/',views.Delete_item.as_view(),name='delete-item'),
    path('show-all-item/',views.Show_all_items.as_view(),name='show-all-item'),
    path('add-items/',views.Add_Item_all.as_view(),name='add-all-item'),
    # path('menu/<str:id>',views.Restaurant_Menu.as_view(),name='restaurant-menu'),
    # path('food-item/<int:id>',views.Food_Items.as_view(),name='food-item')

    path('receive-notification/',views.Receive_Notification.as_view(),name='receive-notification'),
    path('delete-receive-notification/<int:id>',views.delete_notification,name='delete-receive-notification'),

    path('generate-pdf/', views.generate_pdf, name='generate-pdf'),
    path('TermandConditions', views.TermandConditions.as_view(), name='TermandConditions'),
    path('Privacyandpolicies', views.Privacyandpolicies.as_view(), name='privacyandpolicies'),

    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='restaurent_admin/password_reset.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='restaurent_admin/password_reset_done.html'),name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='restaurent_admin\password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='restaurent_admin/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='restaurent_admin/password_reset_complete.html'),name='password_reset_complete'),
#####mobile View ####
    path('mobile-home/<int:id>',views.Mobile_home.as_view(),name='mobile_home'),
    path('mobile-items/<int:id>',views.Mobile_items.as_view(),name='mobile_items'),
]   