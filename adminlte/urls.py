from django.urls import path

from .views import *
from .views import (admin_order_views, admin_payment_views, admin_category_views, admin_product_views,
                    admin_rating_views, admin_article_views,
                    admin_report_views, admin_profile_views, admin_coupon_views)
from django.contrib.admin.views.decorators import staff_member_required



urlpatterns = [
    path('', admin_order_views.index, name="seller_dashboard"),
    # path('order/list/', admin_order_views.OrderList.as_view(), name="order_list"),
    # path('order/<int:id>/delete', admin_order_views.delete_order, name="delete_order"),
    # path('order/<int:id>', admin_order_views.order_detail, name="edit_order"),
    # path('order/change_in_order', admin_order_views.change_in_order, name="change_in_order"),
    #
    # path('payment/list/', admin_payment_views.PaymentList.as_view(), name="payment_list"),
    # path('payment/<int:id>/', admin_payment_views.edit_payment, name="edit_payment"),
    # path('payment/<int:id>/delete', admin_payment_views.delete_payment, name="delete_payment"),
    #
    # path('category/list/', admin_category_views.CategoryList.as_view(), name="category_list"),
    # path('category/add/', admin_category_views.add_new_category, name="category_add"),
    # path('category/<int:id>/', admin_category_views.edit_category, name="edit_category"),
    # path('category/<int:id>/delete', admin_category_views.delete_category, name="delete_category"),
    #
    # path('product/list/', admin_product_views.ProductList.as_view(), name="product_list"),
    # path('product/add/', admin_product_views.add_new_product, name="product_add"),
    # path('product/<int:id>/delete', admin_product_views.delete_product, name="delete_product"),
    # path('product/<int:id>', admin_product_views.edit_product, name="edit_product"),
    # path('product/colors/<int:product_id>', admin_product_views.product_colors, name="product_colors"),
    # path('product/sizes/<int:product_id>', admin_product_views.product_sizes, name="product_sizes"),
    # path('product/v/delete/', admin_product_views.delete_variation, name="variation_delete"),
    # path('product/v/update/', admin_product_views.update_variation, name="variation_update"),
    #
    # path('rating/list/', admin_rating_views.RatingList.as_view(), name="rating_list"),
    # path('rating/<int:id>/delete', admin_rating_views.delete_review, name="delete_rating"),
    # path('rating/<int:id>', admin_rating_views.edit_review, name="edit_rating"),
    #
    # path('article/list/', admin_article_views.ArticleList.as_view(), name="article_list"),
    # path('article/<int:id>/delete', admin_article_views.delete_article, name="delete_article"),
    # path('article/add/', admin_article_views.add_new_article, name="article_add"),
    # path('article/<int:id>', admin_article_views.edit_article, name="edit_article"),
    #
    # path('coupon/list/', admin_coupon_views.CouponList.as_view(), name="coupon_list"),
    # path('coupon/<int:id>/delete', admin_coupon_views.delete_coupon, name="delete_coupon"),
    # path('coupon/add/', admin_coupon_views.add_new_coupon, name="coupon_add"),
    # path('coupon/<int:id>', admin_coupon_views.edit_coupon, name="edit_coupon"),
    #
    # path('sales/year/<int:year>', admin_order_views.get_sales_chart, name="report_by_year"),
    # path('report/<int:year>', admin_report_views.report, name='report_by_year'),
    #
    # path('profile/list/', admin_profile_views.ProfileList.as_view(), name="profile_list"),
    # path('profile/<int:id>', admin_profile_views.view_profile, name="view_profile"),

    path('settings/<int:id>', store_settings, name='store_settings'),
    path('settings/profile', profile_settings, name="profile_settings"),
    path('settings/password', password_settings, name="password_settings"),

    path('login/', login, name="seller_login"),
    path('logout/', logout_user, name="seller_logout"),

    # path('signup/', signup, name="signup"),

    # path('password_change/', auth_views.PasswordChangeView.as_view(template_name="dashboard/password_change.html"), name="password_change"),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="dashboard/password_change_done.html"), name="password_change_done"),
    #
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name="dashboard/password_reset_form.html"), name="password_reset"),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="dashboard/password_reset_done.html"), name="password_reset_done"),
    #
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="dashboard/password_reset_confirm.html"), name="password_reset_confirm"),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="dashboard/password_reset_complete.html"), name="password_reset_complete"),
]
