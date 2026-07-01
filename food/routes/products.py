from flask import Blueprint

products = Blueprint("products", __name__)

@products.route("/products")
def get_products():
    return "Список продуктов"