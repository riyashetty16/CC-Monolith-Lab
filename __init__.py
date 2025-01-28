import ast
from typing import List
import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> List[Product]:
    """Retrieve a user's cart and return a list of Product objects."""
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    try:
        # Parse and fetch products in a single comprehension
        items = [
            products.get_product(content)
            for cart_detail in cart_details
            for content in ast.literal_eval(cart_detail['contents'])
        ]
        return items
    except (ValueError, SyntaxError):
        # Log or handle errors if content parsing fails
        print("Error parsing cart contents.")
        return []


def add_to_cart(username: str, product_id: int) -> None:
    """Add a product to the user's cart."""
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """Remove a product from the user's cart."""
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """Delete the user's cart."""
    dao.delete_cart(username)
