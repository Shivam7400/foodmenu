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
    path('Delete-Profile/',views.DeleteImage.as_view(),name='deleteImage'),
 
    path('subscription/',views.User_Subscription.as_view(),name='subscription'),
    path('Payment/',views.Payment.as_view(),name='Payment'),
    path('user-logout/',views.userlogout,name='user-logout'),
    # path('user-forgot-password/',views.Forget_password.as_view(),name='user-forgot-password'),
    path('Transaction-History/',views.Transaction_History.as_view(),name='t_history'),
    path('Delete-Transaction-History/',views.Delete_Transaction_History.as_view(),name='delete_t_history'),
    

#############################Categorties######################
    path('add-category/',views.Add_Category.as_view(),name='add-category'),
    path('show-category/',views.Show_Category.as_view(),name='show-category'),
    path('edit-category/',views.Edit_Category.as_view(),name='edit-category'),
    path('delete-category/',views.delete_category,name='delete-category'),
    path('show-category-image/',views.Show_cat_image.as_view()),
    path('category-details/',views.caterogy_details.as_view()),


############################Add Food item #################
    path('add-item/<int:id>',views.Add_Item.as_view(),name='add-item'),
    path('add-once/<int:id>',views.Add_Once.as_view(),name='add-once'),
    path('delete-add-once/<int:id>',views.Delete_Add_Once.as_view(),name='delete-add-once'),
    path('show-item/<int:id>',views.Show_Item.as_view(),name='show-item'),
    path('edit-item/<int:id>',views.Edit_Item.as_view(),name='edit-item'),
    path('delete-item/',views.Delete_item.as_view(),name='delete-item'),
    path('show-all-item/',views.Show_all_items.as_view(),name='show-all-item'),
    path('show-all-Draft-item/',views.Show_all_draft_items.as_view(),name='show-all-draft-item'),
    path('add-items/',views.Add_Item_all.as_view(),name='add-all-item'),
    path('Order-History/',views.Order_history.as_view(),name='order_history'),
    path('complete-order/',views.Completeorder.as_view(),name='Completeorder'),
    # path('menu/<str:id>',views.Restaurant_Menu.as_view(),name='restaurant-menu'),
    # path('food-item/<int:id>',views.Food_Items.as_view(),name='food-item')

    path('receive-notification/',views.Receive_Notification.as_view(),name='receive-notification'),
    path('delete-receive-notification/<int:id>',views.delete_notification,name='delete-receive-notification'),

    path('generate-pdf/<int:id>', views.generate_pdf, name='generate-pdf'),
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
    # path('add-to-cart/<int:id>',views.Addtocarts.as_view(),name='Addtocarts'),
    path('add-to-cart-view/<int:id>',views.AddToCartView.as_view(),name='AddToCartView'),
    path('add-to-cart-remove/<int:id>',views.RemoveAddtocart.as_view(),name='RemoveAddtocart'),
    path('item-details/<int:id>',views.Mob_Item_details.as_view(),name='mob_Item_details'),
    path('Manage-quantity/',views.ManageQuantity.as_view(),name='manageQuantity'),
    path('Check-Out/<int:id>',views.Checkout.as_view(),name='checkout'),
    path('checkout/<int:id>',views.CheckOutSession.as_view(),name='checkout_page'),
    path('Success-Page/<int:id>',views.SuccessPage.as_view(),name='success-page'),
    path('Order_details/<int:id>',views.generate_order_pdf,name='order-Details'),
]   