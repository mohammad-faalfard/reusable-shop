# Import product-related models
from .product import Product  # Product model
from .product_brand import ProductBrand  #  Brands
from .product_category import ProductCategory  # Category for organizing products
from .product_discount import ProductDiscount  # Discounts for products
from .product_images import ProductImage  # Product Images
from .product_property import ProductProperty  # Product attributes (e.g., color, size)
from .product_review import ProductReview  # User reviews for products
from .product_tag import ProductTag  # Tags for products
from .product_wishlist import ProductWishlist  # User wishlists

# Public API for the module
__all__ = [
    "ProductCategory",
    "ProductTag",
    "ProductDiscount",
    "Product",
    "ProductImage",
    "ProductProperty",
    "ProductReview",
    "ProductWishlist",
    "ProductBrand",
]
