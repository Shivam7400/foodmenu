from django.urls import path
from . import views

urlpatterns=[
    path('user-login/',views.User_Login.as_view(),name='user-login'),
    path('user-registration/',views.UserRegistration.as_view(),name='user-registration'),
    path('home/',views.HomePage.as_view(),name='home'),
    path('user-dashboard/',views.UserDashboard.as_view(),name='user-dashboard'),
    path('change-user-password/',views.Change_password.as_view(),name='change-user-password'),
    path('edit-user-profile/<int:id>',views.Edit_Users_Profile.as_view(),name='edit-users-profile'),
    path('add-restaurant-details/',views.Add_Restaurant_Deltails.as_view(),name='add-restaurant-details'),
    path('show-restaurant-details/',views.Show_Restaurant_Details.as_view(),name='show-restaurant-details'),
    path('edit-restaurant-details/<int:id>',views.Edit_Restaurant_Details.as_view(),name='edit-restaurant-details'),
    path('restaurant-details/<int:id>',views.Restaurant_details.as_view(),name='restaurant-details'),
    path('delete-restaurant-details/<int:id>',views.delete_restaurant_details,name='delete-restaurant-details'),
    path('subscription',views.User_Subscription.as_view(),name='subscription'),
    path('user-logout/',views.userlogout,name='user-logout'),
    

#############################Categorties######################
    path('add-category/<int:id>',views.Add_Category.as_view(),name='add-category'),
    path('show-category/',views.Show_Category.as_view(),name='show-category'),
    path('edit-category/<int:id>',views.Edit_Category.as_view(),name='edit-category'),
    path('delete-category/<int:id>',views.delete_category,name='delete-category'),


############################Add Food item #################
    path('add-item/<int:id>',views.Add_Item.as_view(),name='add-item'),
    path('show-item/<int:id>',views.Show_Item.as_view(),name='show-item'),
    path('edit-item/<int:id>',views.Edit_Item.as_view(),name='edit-item'),
    path('delete-item/<int:id>',views.delete_item,name='delete-item'),



    path('menu/<str:menu>',views.Restaurant_Menu.as_view(),name='restaurant-menu'),
    # path('food-item/<int:id>',views.Food_Items.as_view(),name='food-item')



    path('receive-notification/',views.Receive_Notification.as_view(),name='receive-notification'),
    path('delete-receive-notification/<int:id>',views.delete_notification,name='delete-receive-notification'),



     path('generate-pdf/<int:id>', views.generate_pdf, name='generate-pdf'),
]