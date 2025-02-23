# we create cart.py cause what we do with carts are heavy for view, and it may get things dirty

cart_session_id='cart'
# what I did was because each session must be specified by name
class Cart:
    def __init__(self, request):
        self.session=request.session
        cart=self.session.get(cart_session_id)
        # but what if our user is new and has no ordering which leads to no session ?
        if not cart:
            cart =self.session[cart_session_id]={}
        self.cart =cart

    def add(self, product, quantity):
        product_id=str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]={'quantity':0, 'price':str(product.price)}
        self.cart[product_id]['quantity']+=quantity


    def save(self):
        self.session.modified=True
