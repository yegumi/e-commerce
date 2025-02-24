from home.models import Product
# we create cart.py cause what we do with carts are heavy for view, and it may get things dirty

cart_session_id='cart'
# what I did was because each session must be specified by name
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart', {})
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def __iter__(self):
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        cart=self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"]=product.name
    #       we added a key as product and assigned product's name to it
            print(product.id)
        for item in cart.values():
            item["total_price"]=int(item["price"]) * item["quantity"]
            yield item

    # for our context_processor
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())



    def save(self):
        self.session.modified=True

    def get_total_price(self):
        return sum(int(item["total_price"])for item in self.cart.values())
