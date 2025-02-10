import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators import csrf
from django.views.decorators.http import require_POST
from jalali_date import date2jalali, datetime2jalali

from apps.account.forms import EditAddressForm, EditProfileForm

# --- Account App Queries ---
from apps.account.queries import get_user_address, get_user_by_email_or_username
from apps.account.utils import generate_reset_password_token, send_forget_password_mail

# --- Blogs App Queries ---
from apps.blogs.forms import CommentForm

# --- Blog App Queries ---
from apps.blogs.queries import (
    get_all_blog_categories,
    get_all_blog_posts,
    get_blog_category,
    get_post_comments,
    get_post_details_by_id,
    get_posts_by_category,
    has_bookmarked,
)

# --- Carts App Queries ---
from apps.carts.queries import (
    add_or_update_cart_item,
    get_cart,
    get_cart_item,
    get_cart_item_count,
    get_cart_items,
    get_cart_items_total_price,
    get_total_inside_cart,
    remove_from_cart_item,
    update_cart_items_quantities,
)

# --- Slider App Queries ---
from apps.cms.queries import get_first_banner, get_second_banner, get_sliders

# --- Info App Forms ---
from apps.info.forms import ContactUsForm

# --- Info App Queries ---
from apps.info.queries import get_about_us_data, get_faq_groups, get_privacy_policy, get_shop_location

# --- Order App Queries ---
from apps.messaging.queries import get_notification, get_notifications, seen_user_message
from apps.order.queries import get_orders_by_user, place_order

# --- Product App Queries ---
from apps.products.filters import ProductListFilter
from apps.products.queries import (
    add_or_remove_product_from_wishlist,
    create_product_review,
    get_all_products,
    get_best_offer,
    get_product,
    get_product_categories,
    get_product_category,
    get_product_details_by_id,
    get_product_reviews,
    get_products_by_category,
    get_products_by_subcategory,
    get_products_with_offers,
    get_related_products,
    get_subcategories_for_category,
    get_user_wishlist,
    is_product_in_wishlist,
    search_products,
)
from apps.promotions.queries import calculate_cart_discount, coupon_validate, get_coupon_by_code

# --- Shipments App Queries ---
from apps.shipments.queries import get_active_shipment_types
from core import choice
from core.http import get_session_key, get_user


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)  # Log out the user after password change
            return render(
                request,
                "front_shop/change-password-message.html",
                {
                    "message": _("Your Password Changed successfully. Please Login Again"),
                    "success": True,
                },
            )
        else:
            return render(request, "front_shop/change-password.html", {"form": form})
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "front_shop/change-password.html", {"form": form})


def forget_password_view(request: HttpRequest) -> HttpResponse:
    """
    Handles the forget password request. Sends a reset email if the user exists,
    or displays an error if the user is not found.
    """
    error = False  # Default error flag is False
    if request.method == "POST":
        email_or_username = request.POST.get("email", "").strip()
        # Get user by email or username
        user = get_user_by_email_or_username(email_or_username)

        if user:
            # Generate a secure reset token
            reset_token = generate_reset_password_token()
            user.reset_password_token = reset_token
            # Send the reset password email
            send_forget_password_mail(request, user.email, user.username, reset_token)

            # Redirect to the success page
            return redirect("forget-password-success")
        else:
            error = True
            # Pass an error message to the template
            return render(request, "front_shop/forget-password.html", {"error": error})

    return render(request, "front_shop/forget-password.html")


def forget_password_success_view(request: HttpRequest) -> HttpResponse:
    return render(request, "front_shop/forget-password-success.html")


# --- settings page Views ---
def settings_view(request: HttpRequest) -> HttpResponse:
    """
    Logs out the user and redirects them to the home page (or another page).
    """
    return render(request, "front_shop/settings.html")


# --- logout page Views ---
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logs out the user and redirects them to the home page (or another page).
    """
    logout(request)  # Log out the user
    return redirect("intro")  # Redirect to the home page or desired page


# --- intro page Views ---
def intro_view(request: HttpRequest) -> HttpResponse:
    return render(request, "front_shop/intro.html")


# --- Pages Views ---
def pages_view(request: HttpRequest) -> HttpResponse:
    return render(request, "front_shop/pages.html")


# --- offline Page Views ---
def offline_view(request: HttpRequest) -> HttpResponse:
    return render(request, "front_shop/offline.html")


# --- Login Page Views ---
class loginView(LoginView):
    template_name = "front_shop/login.html"
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy("home")

    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        messages.error(self.request, _("Invalid username or password"))
        return self.render_to_response(self.get_context_data(form=form))


# --- Info App Views ---
def about_us(request: HttpRequest) -> HttpResponse:
    """Renders the 'About Us' page with the first entry."""
    context: Dict[str, Any] = {"about_us_text": get_about_us_data()}
    return render(request, "front_shop/about-us.html", context)


def support_view(request: HttpRequest) -> HttpResponse:
    """Renders the 'Support' page with FAQ groups and related FAQs ordered by priority."""
    context: Dict[str, Any] = {"faq_groups": get_faq_groups()}
    return render(request, "front_shop/support.html", context)


def privacy_policy_view(request: HttpRequest) -> HttpResponse:
    """Renders the 'Privacy Policy' page with the first policy entry."""
    context: Dict[str, Any] = {"privacy_policy_text": get_privacy_policy()}
    return render(request, "front_shop/privacy-policy.html", context)


def contact_us_view(request: HttpRequest) -> HttpResponse:
    """Handles GET and POST requests for the 'Contact Us' page."""
    location = get_shop_location()
    # Initialize the form
    form = ContactUsForm(request.POST or None)
    success_message = None  # Initialize the success message variable

    if request.method == "POST" and form.is_valid():
        # If the form is valid, save the data
        form.save()

        # Set a success message to be displayed on the page
        success_message = _("Your inquiry has been successfully submitted. We will get back to you shortly.")

    # Prepare context to pass to the template
    context = {
        "form": form,
        "location": location,
        "success_message": success_message,  # Pass the success message to the template
    }

    return render(request, "front_shop/contact.html", context)


# --- Homepage View ---
def home_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the homepage with necessary data: active sliders,
    product categories, banners, products, and their ratings.
    """
    user = request.user if request.user.is_authenticated else None
    # Get all products
    products = get_all_products(user=user)
    # Filter products that have offers
    products_with_offers = get_products_with_offers(products)
    context: Dict[str, Any] = {
        "sliders": get_sliders(),
        "categories": get_product_categories(),
        "first_banner": get_first_banner(),
        "products": get_all_products(user=user),
        "second_banner": get_second_banner(),
        "products_with_offers": products_with_offers,
    }
    return render(request, "front_shop/home.html", context)


# --- Category page View ---
def category_view(request: HttpRequest, category_id) -> HttpResponse:
    user = get_user(request)
    category = get_product_category(category_id)
    products_in_category = get_products_by_category(category, user)
    # Fetch the subcategories for this category using the query function
    subcategories = get_subcategories_for_category(category)
    qs = ProductListFilter(data=request.GET, request=request, queryset=products_in_category)
    # print(subcategories)
    context = {
        "categories": subcategories,
        "products": qs.qs,
    }

    return render(request, "front_shop/category.html", context)


# --- Sub Category page View ---
def subcategory_view(request: HttpRequest, category_id) -> HttpResponse:
    # Fetch the products for the selected category
    products_in_category = get_products_by_subcategory(category_id)
    context = {
        "products": products_in_category,
    }

    return render(request, "front_shop/sub-category.html", context)


# --- Shop Grid page View ---
def shopgrid_view(request: HttpRequest) -> HttpResponse:
    user = get_user(request)
    categories = get_product_categories()
    products = get_all_products(user=user)
    filters = ProductListFilter(request=request, queryset=products, data=request.GET)

    context = {
        "categories": categories,
        "products": filters.qs,
        "filters": filters,
    }

    return render(request, "front_shop/shop-grid.html", context)


# --- Single Product review form ---
@login_required
def single_product_review_view(request: HttpRequest, product_id: int) -> HttpResponse:
    # Fetch product details using the query function
    if request.method != "POST":
        return JsonResponse({})

    product_details = get_product(product_id)
    if not product_details:
        return JsonResponse({}, status=404)

    data = json.loads(request.body)  # Parse the JSON payload
    star = int(data.get("star", 5))
    comment = data.get("comment", None)
    if not star or not comment:
        return JsonResponse({"error": _("Star and comment are required.")}, status=400)
    # Create a new review in the database
    # print(star, comment)
    _obj = create_product_review(user=request.user, product=product_details, star=star, comment=comment)
    return JsonResponse({"comment": comment, "star": star, "date": _("Now"), "user": request.user.full_name}, status=200)


# --- Single Product page View ---
def single_product_view(request: HttpRequest, product_id: int) -> HttpResponse:
    # Fetch product details using the query function
    session_key = get_session_key(request)
    user = get_user(request)
    product_details = get_product_details_by_id(product_id, user)

    if not product_details:
        # If the product is not found, render the not found page with 404 status
        return render(request, "front_shop/not_found.html", status=404)
    product = product_details["product"]

    # Get related products
    related_products = get_related_products(product_id)
    # Get reviews for the product from queries.py
    product_reviews = get_product_reviews(product)
    offer = get_best_offer(product)

    total_inside_cart = get_total_inside_cart(product, request.user, session_key)
    # print(product_reviews)
    # Pass the grouped properties to the context instead of ungrouped ones
    context = {
        "user": request.user,
        "product": product,
        "related_products": related_products,
        "product_images": product_details["product_images"],
        "grouped_product_properties": product_details["grouped_product_properties"],
        "discount_percent": product_details["discount_percent"],
        "discount_amount": product_details["discount_amount"],
        "final_price": product_details["final_price"],
        "product_reviews": product_reviews,
        "total_inside_cart": total_inside_cart,
        "offer_info": {
            "offer": offer,
            "offer_end_at": offer.product_offer.active_until.strftime("%Y/%m/%d %H:%M:%S"),
            "offer_sold": int((offer.sold_stock / offer.stock) * 100),
        }
        if offer
        else {},
    }

    return render(request, "front_shop/single-product.html", context)


@csrf.csrf_exempt
def add_product_to_cart_ajax(request: HttpRequest, product_id: int) -> HttpResponse:
    """Add or update a product in the user's cart via AJAX."""
    quantity = int(request.POST.get("quantity", 1))
    session_key = get_session_key(request)

    user = request.user if request.user.is_authenticated else None
    user_cart = get_cart(user, session_key)
    product = get_product(product_id)
    # print(quantity, request.POST, request.GET, request.content_params)
    if quantity < 1:
        remove_from_cart_item(product, user_cart)
    else:
        _cart_item = add_or_update_cart_item(
            product=product,
            quantity=quantity,
            cart=user_cart,
        )
    # Clear the coupon if product is removed
    remove_coupon(request)
    return HttpResponse(quantity)


@csrf.csrf_exempt
def quick_add_product_to_cart_ajax(request: HttpRequest, product_id: int) -> HttpResponse:
    """Add or update a product in the user's cart via AJAX."""

    session_key = get_session_key(request)

    user = request.user if request.user.is_authenticated else None
    user_cart = get_cart(user, session_key)
    product = get_product(product_id)
    item = get_cart_item(user_cart, product)
    quantity = item.quantity if item else 0
    new_quantity = quantity + 1

    _cart_item = add_or_update_cart_item(
        product=product,
        quantity=new_quantity,
        cart=user_cart,
    )

    return HttpResponse(quantity)


def get_cart_item_count_view(request: HttpRequest) -> HttpResponse:
    """
    Returns the current cart item count via HTMX request.
    """
    session_key = get_session_key(request)

    user_cart = get_cart(request.user, session_key)
    update_cart_items_quantities(user_cart)

    # Get the count of items in the cart
    cart_item_count = get_cart_item_count(user_cart)

    return HttpResponse(cart_item_count)


@csrf.csrf_exempt
def remove_product_from_cart_ajax(request: HttpRequest, product_id: int) -> HttpResponse:
    """Remove a product from the user's cart via AJAX."""
    session_key = get_session_key(request)

    user_cart = get_cart(request.user, session_key)
    product = get_product(product_id)
    remove_from_cart_item(product, user_cart)
    # Clear the coupon if product is removed
    remove_coupon(request)
    return HttpResponse()


def cart_view(request: HttpRequest) -> HttpResponse:
    """Render the cart page with items, total price, and apply coupon logic."""
    # Fetch cart items
    session_key = get_session_key(request)
    cart = get_cart(request.user, session_key)
    update_cart_items_quantities(cart)
    items = get_cart_items(cart)
    coupon_code = request.session.get("coupon_code")
    coupon_obj = get_coupon_by_code(coupon_code) if coupon_code else None

    # Fetch the total price of the items in the cart (after applying coupon if available)
    result = get_cart_items_total_price(cart, coupon_obj)
    # Access individual variables
    total_price = result["total_price"]

    has_coupon = result["coupon_id"]

    # Prepare context
    context = {
        "items": items,
        "total_price": total_price,
        "has_coupon": has_coupon,
        "coupon_code": coupon_code or "",
    }

    return render(request, "front_shop/cart.html", context)


def cart_total_price_ajax(request: HttpRequest) -> HttpResponse:
    """Returns the total price of items in the user's cart as a formatted string."""
    session_key = get_session_key(request)

    cart = get_cart(request.user, session_key)
    update_cart_items_quantities(cart)

    coupon_code = request.session.get("coupon_code")
    coupon_obj = get_coupon_by_code(coupon_code) if coupon_code else None

    total_price = int(get_cart_items_total_price(cart, coupon_obj)["total_price"])
    p = f"{total_price:,}"
    return HttpResponse(p)


@login_required
def checkout_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the checkout page with shipment types and user information.
    Ensures user profile is complete before proceeding.
    """
    user = request.user

    # Fetch user details
    address = get_user_address(user)
    shipment_types = get_active_shipment_types()
    coupon_code = request.session.get("coupon_code")
    session_key = get_session_key(request)
    cart = get_cart(user, session_key)
    coupon_obj = get_coupon_by_code(coupon_code) if coupon_code else None
    # Fetch the total price of the items in the cart (after applying coupon if available)
    result = get_cart_items_total_price(cart, coupon_obj)
    # Access individual variables
    total_price = result["total_price"]

    # Check if the profile is complete
    profile_incomplete = not all((user.get_full_name(), user.email, user.phone_number, address))

    # Prepare the context data
    context = {
        "full_name": user.get_full_name(),
        "email": user.email,
        "phone": user.phone_number,
        "address": address,
        "shipment_types": shipment_types,
        "profile_incomplete": profile_incomplete,  # Flag for incomplete profile
        "final_price": total_price,  # Final price (either discounted or total price)
    }

    return render(request, "front_shop/checkout.html", context)


@login_required
def choose_payment_method(request: HttpRequest) -> HttpResponse:
    """
    Renders the payment method selection page.
    """
    # You can add any logic here if you need to pass additional context to the template,
    # such as available payment methods, etc.
    # print(request.session.items())

    return render(request, "front_shop/checkout-payment.html")


@login_required
def payment_method_cash(request: HttpRequest) -> HttpResponse:
    """
    Handles the cash on delivery payment method selection during checkout.
    Renders the checkout-cash.html page.
    """
    # You can add any context or logic here if needed
    return render(request, "front_shop/checkout-cash.html")


@login_required
def payment_success(request: HttpRequest) -> HttpResponse:
    """
    Handle the successful payment and display a confirmation message to the user.
    """
    return render(request, "front_shop/payment-success.html")


@login_required
def payment_failed(request: HttpRequest) -> HttpResponse:
    """
    Handle the failed payment
    """
    return render(request, "front_shop/payment-failed.html")


def apply_coupon(request: HttpRequest) -> JsonResponse:
    """Apply coupon and update the total price of the cart."""
    session_key = get_session_key(request)

    if request.method == "POST":
        data = json.loads(request.body)  # Parse JSON data from the request
        coupon_code = data.get("coupon_code", "").strip()
        # Get the user's cart
        cart = get_cart(request.user, session_key)
        # print(f"{coupon_code=:}")
        try:
            # Get the total price with the coupon applied
            result = get_cart_items_total_price(cart)
            total_price = result["total_price"]

            if not coupon_code:
                return JsonResponse(
                    data={
                        "success": True,
                        "total_price": total_price,
                    },
                )

            coupon_obj = get_coupon_by_code(coupon_code)

            coupon_validate(cart.user, coupon_obj, total_price)

            # Save the coupon code in the session
            request.session["coupon_code"] = coupon_code

            # print(result, total_price)
            # Return the new price and success message
            return JsonResponse(
                data={
                    "success": True,
                    "total_price": calculate_cart_discount(total_price, coupon_obj),
                },
            )

        except ValidationError as e:
            # print(e)
            return JsonResponse(
                {
                    "success": False,
                    "error": e.message,
                }
            )

    return JsonResponse(
        {
            "success": False,
            "error": _("Invalid request"),
        }
    )


def remove_coupon(request: HttpRequest) -> None:
    # Remove the coupon code from session
    if "coupon_code" in request.session:
        del request.session["coupon_code"]


@csrf.csrf_exempt
def store_shipment_selection(request: HttpRequest) -> JsonResponse:
    """Store the selected shipment method in the session."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            shipment_id = data.get("shipment_id")

            if shipment_id:
                request.session["selected_shipment_id"] = shipment_id  # Store in session
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "No shipment ID provided"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method"})


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """
    View to display the user's profile information, including their username,
    full name, email, phone number, and address.

    The view fetches the user's address using the `get_user_address` function
    and prepares the necessary context data to be rendered in the profile template.
    """
    user = request.user

    # Fetch user details
    address = get_user_address(user)

    # Prepare the context data
    context = {
        "username": user.username,
        "full_name": user.get_full_name(),
        "email": user.email,
        "phone": user.phone_number,
        "address": address,
    }

    return render(request, "front_shop/profile.html", context)


@login_required
def edit_profile_view(request: HttpRequest) -> HttpResponse:
    """
    View to handle editing the user's profile and managing their addresses.
    """
    user = request.user

    if request.method == "POST":
        # Initialize the forms with data and files (for the profile) and addresses
        profile_form = EditProfileForm(request.POST, request.FILES, instance=user)
        address_form = EditAddressForm(request.POST, instance=user.addresses.first())  # Handle the first address or create

        # Check if the forms are valid
        profile_valid = profile_form.is_valid()
        address_valid = address_form.is_valid()

        if profile_valid or address_valid:  # Proceed if either form is valid
            # Save the profile form if valid
            if profile_valid:
                profile_form.save()

            # Save the address form if valid
            if address_valid:
                address = address_form.save(commit=False)
                address.user = user  # Ensure the address is associated with the logged-in user
                address.save()

            return redirect("profile-page")  # Redirect after saving the valid form(s)
    else:
        # Prefill the forms with existing data when the request is not a POST
        profile_form = EditProfileForm(instance=user)
        address_form = EditAddressForm(instance=user.addresses.first())  # Prefill with the first address

    context = {
        "profile_form": profile_form,
        "address_form": address_form,
    }
    return render(request, "front_shop/edit-profile.html", context)


@login_required
def my_orders_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    orders = get_orders_by_user(user)
    # Map order status type to display data
    ORDER_STATUS_MAP = {
        0: {"icon": "ti ti-basket"},
        1: {"icon": "ti ti-box"},
        2: {"icon": "ti ti-box"},
        3: {"icon": "ti ti-trolley"},
        4: {"icon": "ti ti-truck-delivery"},
        5: {"icon": "ti ti-building-store"},
        6: {"icon": "ti ti-heart-check"},
        7: {"icon": "ti ti-alert-circle"},
    }

    orders_data = []

    for order in orders:
        statuses = order.order_statuses.all().exclude(type=choice.ORDER_STATUS_PAYMENT_WAITING).order_by("type")
        status_data = []
        for status in statuses:
            status_info = ORDER_STATUS_MAP.get(status.type, {})
            estimated_time = status.estimated_time
            if not estimated_time:
                estimated_time = datetime.now() + timedelta(days=status.type)
            estimated_time = date2jalali(estimated_time).strftime("%d %b %Y")
            timestamp = datetime2jalali(status.timestamp).strftime("%d %b %Y - %I:%M %p") if status.timestamp else None

            data = {
                "icon": status_info.get("icon"),
                "label": status.get_type_display(),
                "timestamp": timestamp,
                "estimated_time": estimated_time,
                "active": order.current_status >= status.type,  # Mark the most recent status as active
            }
            status_data.append(data)

        orders_data.append(
            {
                "order": order,
                "current_status": order.current_status,
                "statuses": status_data,
            }
        )

    context = {
        "orders": orders_data,
        "user": user,
    }
    return render(request, "front_shop/my-orders.html", context)


@login_required
def create_order_view(request):
    """
    View to create an order by reading variables from the session and returning an HTTP response.
    """
    session_key = get_session_key(request)
    # Read required variables from the session
    user = request.user
    address = get_user_address(user)
    coupon_code = request.session.get("coupon_code")
    cart = get_cart(user, session_key)
    coupon_obj = get_coupon_by_code(coupon_code) if coupon_code else None
    cart_info = get_cart_items_total_price(cart, coupon_obj)

    cart_items: list[dict] = get_cart_items(cart)
    shipment_id: Optional[str] = request.session.get("selected_shipment_id")
    status_type: Optional[int] = 0  #  '0' payment waiting - need to change later

    # estimated_delivery_time: Optional[str] = request.session.get("estimated_delivery_time")
    # print(
    #     dict(
    #         user=user,
    #         address=address,
    #         coupon=coupon_obj,
    #         product_total_price=cart_info["product_total_price"],
    #         coupon_total_discount=cart_info["coupon_total_discount"],
    #         product_total_discount=cart_info["product_total_discount"],
    #         total_price=cart_info["total_price"],
    #         cart_items=cart_items,
    #         shipment_id=shipment_id,
    #         status_type=status_type,
    #         estimated_delivery_time=None,  # Optional, can be None
    #         note=None,
    #     )
    # )
    # Place the order
    try:
        place_order(
            user=user,
            address=address,
            coupon=coupon_obj,
            product_total_price=cart_info["product_total_price"],
            coupon_total_discount=cart_info["coupon_total_discount"],
            product_total_discount=cart_info["product_total_discount"],
            total_price=cart_info["total_price"],
            cart_items=cart_items,
            shipment_id=shipment_id,
            status_type=status_type,
            estimated_delivery_time=None,  # Optional, can be None
            note=None,
        )

        # Clean UP

        # Clear the cart and remove coupon
        cart.clear()
        remove_coupon(request)

        # Redirect to the payment success page with the order details
        return redirect("payment-success")

    except RuntimeError as e:
        # print(e)
        return render(request, "front_shop/payment-failed.html", {"error": str(e)}, status=500)


def shoplist_view(request: HttpRequest) -> HttpResponse:
    products = get_all_products()
    # Get all product categories
    categories = get_product_categories()
    category_id = request.GET.get("category_id")
    user = get_user(request)
    if category_id:
        category = get_product_category(category_id)
        products = get_products_by_category(category, user)

    # Prepare the context data
    context = {
        "categories": categories,
        "products": products,
    }

    # Render the template with the products context
    return render(request, "front_shop/shop-list.html", context)


def my_notification_view(request: HttpRequest) -> HttpResponse:
    notifications = get_notifications(request.user).order_by("is_seen", "-created_at") if request.user.is_authenticated else []
    # Prepare the context data
    context = {
        "notifs": notifications,
    }

    # Render the template with the products context
    return render(request, "front_shop/notifications.html", context)


@login_required
def notification_details_view(request: HttpRequest, notif_id: int) -> HttpResponse:
    notification = get_notification(request.user, notif_id)
    seen_user_message(notification)
    # Prepare the context data
    context = {
        "notif": notification,
    }

    # Render the template with the products context
    return render(request, "front_shop/notification-details.html", context)


@csrf.csrf_exempt
@login_required
@require_POST
def toggle_heart_wishlist_ajax(request: HttpRequest, product_id: int) -> HttpResponse:
    """Add or remove a product from the user's wishlist via AJAX."""
    user_id = request.user.id
    result = add_or_remove_product_from_wishlist(user_id, product_id)  # return 1 or 0
    return HttpResponse(result)


@login_required
def check_product_in_wishlist_ajax(request: HttpRequest, product_id: int) -> HttpResponse:
    """Check if a product is in the user's wishlist and return the heart icon HTML."""
    user = request.user
    product = get_product(product_id)
    if not product:
        return HttpRequest(0)

    product_in_wishlist = is_product_in_wishlist(user=user, product=product)

    return HttpResponse(product_in_wishlist)


@login_required
def user_wishlist_list_view(request: HttpRequest) -> HttpResponse:
    user = get_user(request)
    products = get_user_wishlist(user)

    # Prepare the context data
    context = {
        "products": products,
    }

    return render(request, "front_shop/wishlist-list.html", context)


@login_required
def user_wishlist_list_add_to_cart_view(request: HttpRequest) -> HttpResponse:
    user = get_user(request)
    products = get_user_wishlist(user)
    cart = get_cart(user)
    [add_or_update_cart_item(p, 1, cart) for p in products]

    # Prepare the context data
    context = {
        "products": products,
    }

    return render(request, "front_shop/wishlist-list.html", context)


def blog_list_view(request: HttpRequest) -> HttpResponse:
    """Render the blog list."""
    posts = get_all_blog_posts()
    categories = get_all_blog_categories()

    category_id = request.GET.get("category_id")
    # Fetch posts by category only if category_id is present and valid
    if category_id and (category_obj := get_blog_category(category_id)):
        posts = get_posts_by_category(category_obj)

    context = {
        "posts": posts,
        "categories": categories,
    }
    return render(request, "front_shop/blog-list.html", context)


def blog_grid_view(request: HttpRequest) -> HttpResponse:
    """Render the blog grid."""
    posts = get_all_blog_posts()
    categories = get_all_blog_categories()
    category_id = request.GET.get("category_id")
    # Fetch posts by category only if category_id is present and valid
    if category_id and (category_obj := get_blog_category(category_id)):
        posts = get_posts_by_category(category_obj)

    context = {
        "posts": posts,
        "categories": categories,
    }
    return render(request, "front_shop/blog-grid.html", context)


def blog_detail_view(request: HttpRequest, post_id: int) -> HttpResponse:
    """Render the blog detail."""
    post = get_post_details_by_id(post_id)
    comments = get_post_comments(post)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login-page")  # Redirect to login if not authenticated
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.sender = request.user  # Assuming the user is logged in
            comment.is_accepted = False  # New comments need admin approval
            comment.save()
            return redirect("blog-details", post_id=post_id)
    else:
        form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "has_bookmarked": has_bookmarked(request.user, post) if request.user.is_authenticated else False,
    }
    return render(request, "front_shop/blog-details.html", context)


# Search view that handles the search results
def search_view(request):
    query = request.GET.get("query", "").strip()  # Get query from GET request
    page_number = request.GET.get("page", 1)  # Default to page 1

    if not query:
        # If no query is provided, return empty results
        products = []
        total_pages = 1
    else:
        # Perform search based on the query
        products = search_products(query)

        # Paginate results
        paginator = Paginator(products, 9)  # Show 9 results per page
        try:
            page_products = paginator.page(page_number)
        except PageNotAnInteger:
            page_products = paginator.page(1)  # Return first page if invalid page number
        except EmptyPage:
            page_products = paginator.page(paginator.num_pages)  # Return last page if out of range

        total_pages = paginator.num_pages  # Get total number of pages

    return render(
        request,
        "front_shop/search_results.html",  # Render the search results page
        {
            "query": query,
            "products": page_products,
            "total_pages": total_pages,
        },
    )


# --- Flash Sale View ---
def flash_sale_view(request: HttpRequest) -> HttpResponse:
    user = request.user if request.user.is_authenticated else None
    # Get all products
    products = get_all_products(user=user)
    # Filter products that have offers
    products_with_offers = get_products_with_offers(products)
    context: Dict[str, Any] = {
        "products_with_offers": products_with_offers,
    }
    return render(request, "front_shop/flash-sale.html", context)
