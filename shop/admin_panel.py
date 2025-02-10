from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "DASHBOARD_CALLBACK": "apps.dashboard.views.dashboard_callback",
    "ENVIRONMENT": "apps.dashboard.utils.environment_callback",
    # "COLORS": {
    #     "primary": {
    #         "50": "250 245 255",
    #         "100": "243 232 255",
    #         "200": "233 213 255",
    #         "300": "216 180 254",
    #         "400": "40 180 99",
    #         "500": "40 180 99",
    #         "600": "40 180 99",
    #         "700": "126 34 206",
    #         "800": "107 33 168",
    #         "900": "88 28 135",
    #         "950": "59 7 100",
    #     },
    # },
    # "SITE_ICON": {
    #     "light": lambda request: static("dashboard/images/icon.svg"),  # light mode
    #     "dark": lambda request: static("dashboard/images/icon.svg"),  # dark mode
    # },
    # # "SITE_LOGO": lambda request: static("dashboard/images/logo.svg"),  # both modes, optimise for 32px height
    # "SITE_LOGO": {
    #     "light": lambda request: static("dashboard/images/logo.svg"),  # light mode
    #     "dark": lambda request: static("dashboard/images/logo.svg"),  # dark mode
    # },
    # "SITE_SYMBOL": "speed",  # symbol from icon set
    # "SITE_FAVICONS": [
    #     {
    #         "rel": "icon",
    #         "sizes": "32x32",
    #         "type": "image/ico+xml",
    #         "href": lambda request: static("favicon.ico"),
    #     },
    # ],
    "TABS": [
        {
            "models": ["messaging.group", "messaging.groupuser"],
            "collapsible": True,
            "items": [
                {
                    "title": _("Groups"),
                    "icon": "article",
                    "link": reverse_lazy("admin:messaging_group_changelist"),
                },
                {
                    "title": _("Group Users"),
                    "icon": "article",
                    "link": reverse_lazy("admin:messaging_groupuser_changelist"),
                },
            ],
        },
        {
            "models": ["info.faqgroup", "info.faq"],
            "title": _("FAQ Management"),
            "collapsible": True,
            "items": [
                {
                    "title": _("FAQ Groups"),
                    "icon": "group",
                    "link": reverse_lazy("admin:info_faqgroup_changelist"),
                },
                {
                    "title": _("FAQs"),
                    "icon": "help",
                    "link": reverse_lazy("admin:info_faq_changelist"),
                },
            ],
        },
        # Contact Us Tab
        {
            "models": ["info.inquirycategory", "info.contactus"],
            "title": _("Contact Us Management"),
            "collapsible": True,
            "items": [
                {
                    "title": _("Categories"),
                    "icon": "category",
                    "link": reverse_lazy("admin:info_inquirycategory_changelist"),
                },
                {
                    "title": _("Contact Us"),
                    "icon": "contact_mail",
                    "link": reverse_lazy("admin:info_contactus_changelist"),
                },
            ],
        },
        # States Tab
        {
            "models": ["info.state", "info.city"],
            "title": _("Location Management"),
            "collapsible": True,
            "items": [
                {
                    "title": _("States"),
                    "icon": "map",
                    "link": reverse_lazy("admin:info_state_changelist"),
                },
                {
                    "title": _("Cities"),
                    "icon": "location_city",
                    "link": reverse_lazy("admin:info_city_changelist"),
                },
            ],
        },
        # Product Offer Tab
        {
            "models": ["cms.productoffer", "cms.productofferitem"],
            "title": _("Product Offer Management"),
            "collapsible": True,
            "items": [
                {
                    "title": _("Product Offers"),
                    "icon": "local_offer",  # Material icon for product offers
                    "link": reverse_lazy("admin:cms_productoffer_changelist"),
                },
                {
                    "title": _("Product Offer Items"),
                    "icon": "list",  # Material icon for product offer items
                    "link": reverse_lazy("admin:cms_productofferitem_changelist"),
                },
            ],
        },
        # Order Tab
        {
            "models": ["order.order", "order.orderitem", "order.ordershipment", "order.orderstatus"],
            "title": _("Order Management"),
            "collapsible": True,
            "items": [
                {
                    "title": _("Orders"),
                    "icon": "shopping_cart",
                    "link": reverse_lazy("admin:order_order_changelist"),
                },
                {
                    "title": _("Order Items"),
                    "icon": "inventory",
                    "link": reverse_lazy("admin:order_orderitem_changelist"),
                },
                {
                    "title": _("Order Shipments"),
                    "icon": "local_shipping",
                    "link": reverse_lazy("admin:order_ordershipment_changelist"),
                },
                {
                    "title": _("Order Statuses"),
                    "icon": "history",
                    "link": reverse_lazy("admin:order_orderstatus_changelist"),
                },
            ],
        },
        # Coupon Tab
        {
            "models": ["promotions.coupon", "promotions.couponconsume"],
            "title": _("Coupon Management"),
            "collapsible": True,
            "items": [
                {
                    "title": _("Coupons"),
                    "icon": "card_giftcard",
                    "link": reverse_lazy("admin:promotions_coupon_changelist"),
                },
                {
                    "title": _("Coupon Consumes"),
                    "icon": "history",
                    "link": reverse_lazy("admin:promotions_couponconsume_changelist"),
                },
            ],
        },
        # product Tab
        {
            "models": ["products.product", "products.productproperty", "products.productdiscount", "products.productimage"],
            "title": _("Product Management"),
            "collapsible": True,
            "items": [
                {
                    "title": _("Products"),
                    "icon": "inventory",
                    "link": reverse_lazy("admin:products_product_changelist"),
                },
                {
                    "title": _("Properties"),
                    "icon": "tune",
                    "link": reverse_lazy("admin:products_productproperty_changelist"),
                },
                {
                    "title": _("Discounts"),
                    "icon": "local_offer",
                    "link": reverse_lazy("admin:products_productdiscount_changelist"),
                },
                {
                    "title": _("Image"),
                    "icon": "image",
                    "link": reverse_lazy("admin:products_productimage_changelist"),
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,  # Top border
                "collapsible": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        # "badge": "sample_app.badge_callback",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("account management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Admin Users"),
                        "icon": "shield_person",
                        "link": reverse_lazy("admin:account_adminuserproxy_changelist"),
                    },
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:account_normaluserproxy_changelist"),
                    },
                    {
                        "title": _("New Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:account_newuserproxy_changelist"),
                        "badge": "apps.account.utils.new_user_badge_callback",
                    },
                    {
                        "title": _("Addresses"),
                        "icon": "home",
                        "link": reverse_lazy("admin:account_address_changelist"),
                    },
                ],
            },
            {
                "title": _("Product Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Products"),
                        "icon": "inventory",
                        "link": reverse_lazy("admin:products_product_changelist"),
                    },
                    {
                        "title": _("Categories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:products_productcategory_changelist"),
                    },
                    {
                        "title": _("Brands"),
                        "icon": "category",
                        "link": reverse_lazy("admin:products_productbrand_changelist"),
                    },
                    {
                        "title": _("Reviews"),
                        "icon": "rate_review",
                        "link": reverse_lazy("admin:products_productreview_changelist"),
                    },
                    {
                        "title": _("Wishlists"),
                        "icon": "favorite",
                        "link": reverse_lazy("admin:products_productwishlist_changelist"),
                    },
                ],
            },
            # Shipments Manangement Section
            {
                "title": _("Shipments Manangement"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Shipment Types"),
                        "icon": "local_shipping",
                        "link": reverse_lazy("admin:shipments_shipmenttype_changelist"),
                    },
                ],
            },
            {
                "title": _("Order Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Orders"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:order_order_changelist"),
                    },
                ],
            },
            # CMS Management section
            {
                "title": _("CMS Management"),
                "separator": True,  # No separator above this section
                "collapsible": True,
                "items": [
                    {
                        "title": _("Banners"),
                        "icon": "photo_library",  # Material icon for banners
                        "link": reverse_lazy("admin:cms_banner_changelist"),
                    },
                    {
                        "title": _("Sliders"),
                        "icon": "slideshow",  # Material icon for sliders
                        "link": reverse_lazy("admin:cms_slider_changelist"),
                    },
                    {
                        "title": _("Product Offers"),
                        "icon": "local_offer",  # Material icon for product offers
                        "link": reverse_lazy("admin:cms_productoffer_changelist"),
                    },
                ],
            },
            {
                "title": _("Promotions Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Coupons"),
                        "icon": "card_giftcard",
                        "link": reverse_lazy("admin:promotions_coupon_changelist"),
                    },
                ],
            },
            {
                "title": _("Wallet Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Wallets"),
                        "icon": "wallet",
                        "link": reverse_lazy("admin:wallet_wallet_changelist"),
                    },
                    {
                        "title": _("Transactions"),
                        "icon": "account_balance_wallet",
                        "link": reverse_lazy("admin:wallet_wallettransaction_changelist"),
                    },
                ],
            },
            {
                "title": _("Carts Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Carts"),
                        "icon": "wallet",
                        "link": reverse_lazy("admin:carts_cart_changelist"),
                    },
                ],
            },
            {
                "title": _("Messaging"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Groups"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:messaging_group_changelist"),
                    },
                    {
                        "title": _("Group Messages"),
                        "icon": "cell_tower",
                        "link": reverse_lazy("admin:messaging_groupmessage_changelist"),
                    },
                    {
                        "title": _("User Messages"),
                        "icon": "sms",
                        "link": reverse_lazy("admin:messaging_usermessage_changelist"),
                    },
                ],
            },
            # Blog Management section
            {
                "title": _("Blog Management"),
                "separator": True,  # No separator above this section
                "collapsible": True,
                "items": [
                    {
                        "title": _("Blog Posts"),
                        "icon": "article",
                        "link": reverse_lazy("admin:blogs_post_changelist"),
                    },
                    {
                        "title": _("Categories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:blogs_blogcategory_changelist"),
                    },
                    {
                        "title": _("Comments"),
                        "icon": "comment",
                        "link": reverse_lazy("admin:blogs_postcomment_changelist"),
                    },
                    {
                        "title": _("Bookmark"),
                        "icon": "bookmark",
                        "link": reverse_lazy("admin:blogs_blogbookmark_changelist"),
                    },
                ],
            },
            # Info App Section
            {
                "title": _("Information Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("About Us"),
                        "icon": "info",
                        "link": reverse_lazy("admin:info_aboutus_changelist"),
                    },
                    {
                        "title": _("FAQ Management"),
                        "icon": "help",
                        "link": reverse_lazy("admin:info_faq_changelist"),
                    },
                    {
                        "title": _("Privacy Policy"),
                        "icon": "security",
                        "link": reverse_lazy("admin:info_privacypolicy_changelist"),
                    },
                    {
                        "title": _("Shop Locations"),
                        "icon": "location_on",
                        "link": reverse_lazy("admin:info_shoplocation_changelist"),
                    },
                    {
                        "title": _("States"),
                        "icon": "map",
                        "link": reverse_lazy("admin:info_state_changelist"),
                    },
                    {
                        "title": _("Contact Us"),
                        "icon": "contact_mail",
                        "link": reverse_lazy("admin:info_contactus_changelist"),
                    },
                ],
            },
        ],
    },
    "STYLES": [],
    "SCRIPTS": [],
}
