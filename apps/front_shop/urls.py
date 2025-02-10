from django.urls import path

from . import views

urlpatterns = [
    # Home and static pages
    path("", views.home_view, name="home"),
    path("about/", views.about_us, name="about-us"),
    path("support/", views.support_view, name="support"),
    path("privacy-policy/", views.privacy_policy_view, name="privacy-policy"),
    path("contact/", views.contact_us_view, name="contact"),
    path("offline/", views.offline_view, name="offline"),
    path("search/", views.search_view, name="search"),
    # User authentication
    path("login/", views.loginView.as_view(), name="login-page"),
    path("logout/", views.logout_view, name="logout"),
    path("password/forget/", views.forget_password_view, name="forget-password"),
    path("password/change/", views.change_password_view, name="change-password"),
    path("password/forget/success/", views.forget_password_success_view, name="forget-password-success"),
    # User profile
    path("profile/", views.profile_view, name="profile-page"),
    path("profile/edit/", views.edit_profile_view, name="edit-profile"),
    path("profile/my-orders/", views.my_orders_view, name="my-orders"),
    path("notification/", views.my_notification_view, name="notification"),
    path("notification/<int:notif_id>/", views.notification_details_view, name="notification-details"),
    # Pages
    path("settings/", views.settings_view, name="settings"),
    path("intro/", views.intro_view, name="intro"),
    path("pages/", views.pages_view, name="pages"),
    path("flash-sale/", views.flash_sale_view, name="flash-sale"),
    # Category and product-related pages
    path("category/<int:category_id>/", views.category_view, name="category"),
    path("subcategory/<int:category_id>/", views.subcategory_view, name="subcategory"),
    path("shop-grid/", views.shopgrid_view, name="shop-grid"),
    path("shop-list/", views.shoplist_view, name="shop-list"),
    path("product/<int:product_id>/", views.single_product_view, name="single_product"),
    path("product/<int:product_id>/review", views.single_product_review_view, name="single_product_review"),
    # Cart and checkout
    path("cart/", views.cart_view, name="cart"),
    path("cart/total-price-ajax", views.cart_total_price_ajax, name="cart_total_price_ajax"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("checkout/payment-method/", views.choose_payment_method, name="payment-method-select"),
    path("checkout/payment-method/cash/", views.payment_method_cash, name="payment-method-cash"),
    path("checkout/payment-success/", views.payment_success, name="payment-success"),
    path("checkout/payment-failed/", views.payment_success, name="payment-failed"),
    path("checkout/create-order/", views.create_order_view, name="create-order"),
    # Cart and wishlist actions (AJAX)
    path("product/<int:product_id>/add/", views.add_product_to_cart_ajax, name="add_product_to_cart_ajax"),
    path("product/<int:product_id>/add/quick/", views.quick_add_product_to_cart_ajax, name="quick_add_product_to_cart_ajax"),
    path("product/<int:product_id>/remove/", views.remove_product_from_cart_ajax, name="remove_product_from_cart_ajax"),
    path("apply-coupon/", views.apply_coupon, name="apply_coupon"),
    path("store-shipment-selection/", views.store_shipment_selection, name="store-shipment-selection"),
    path("cart_item_count-ajax/", views.get_cart_item_count_view, name="get_cart_item_count"),
    path("check_wishlist/<int:product_id>/", views.check_product_in_wishlist_ajax, name="check_wishlist"),
    path("toggle_wishlist/<int:product_id>/", views.toggle_heart_wishlist_ajax, name="toggle_wishlist"),
    # Wishlist page
    path("wishlist-list/", views.user_wishlist_list_view, name="wishlist-list"),
    path("wishlist-list/add-to-cart/", views.user_wishlist_list_add_to_cart_view, name="wishlist-list-add-to-cart"),
    # blog
    path("blog/list/", views.blog_list_view, name="blog-list"),
    path("blog/grid/", views.blog_grid_view, name="blog-grid"),
    path("blog/details/<int:post_id>/", views.blog_detail_view, name="blog-details"),
]
