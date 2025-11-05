from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get('cart', {})

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        self.cart[product_id] = self.cart.get(product_id, 0) + quantity
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def items(self):
        from .models import Product
        products = Product.objects.filter(id__in=self.cart.keys())
        return [
            {
                'product': product,
                'quantity': self.cart[str(product.id)],
                'total': product.price * self.cart[str(product.id)]
            }
            for product in products
        ]

    def total_price(self):
        return sum(item['total'] for item in self.items())
    
    def get_items(self):
        items = []
        for product_id, quantity in self.cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                items.append({
                    "product": product,
                    "quantity": quantity,
                    "total": product.price * quantity
                })
            except Product.DoesNotExist:
                continue
        return items

    def get_total_price(self):
        return sum(
            Product.objects.get(id=int(pid)).price * qty
            for pid, qty in self.cart.items()
            if Product.objects.filter(id=int(pid)).exists()
        )
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            product_id = str(product.id)
            quantity = self.cart[product_id]  # Directly an int
            yield {
                'product': product,
                'quantity': quantity
            }


