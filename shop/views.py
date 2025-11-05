from django.shortcuts import render, get_object_or_404
from .models import Product
from django.shortcuts import redirect
from .cart import Cart
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST

def product_list(request):
    products = Product.objects.filter(available=True)
    cart = Cart(request)
    return render(request, 'shop/product_list.html', {
        'products': products,
        'cart_items': cart.items(),
        'total': cart.total_price()
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart_items': cart.items(), 'total': cart.total_price()})

@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    cart.add(product_id=pk)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'added'})
    return redirect(reverse('product_list'))

def cart_remove(request, pk):
    cart = Cart(request)
    cart.remove(product_id=pk)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'removed'})
    return redirect(reverse('product_list'))


def cart_fragment(request):
    try:
        cart = Cart(request)
        cart_items = cart.get_items()
        total = cart.get_total_price()
        html = render_to_string("shop/cart_detail.html", {
            "cart_items": cart_items,
            "total": total
        })
        return JsonResponse({
            "html": html,
            "count": sum([item["quantity"] for item in cart_items])
        })
    except Exception as e:
        print("Cart fragment error:", e)
        return JsonResponse({"error": str(e)}, status=500)

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Here you'd process payment and save order
        cart.clear()
        return render(request, 'shop/checkout_success.html')
    return render(request, 'shop/checkout.html', {'cart_items': cart.items(), 'total': cart.total_price()})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
import traceback

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    try:
        cart = Cart(request)
        line_items = []

        for item in cart:
            product = item['product']
            print("Using Stripe key:", settings.STRIPE_SECRET_KEY[:10])
            print("Price ID:", product.stripe_price_id)
            line_items.append({
                'price': product.stripe_price_id,
                'quantity': item['quantity'],
            })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='subscription',
            success_url='https://myuntoldstories.onrender.com/success/',
            cancel_url='https://myuntoldstories.onrender.com/cancel/',
        )
        print("Stripe secret:", settings.STRIPE_SECRET_KEY[:10])
        print("Session ID:", session.id)


        return JsonResponse({'id': session.id})

    except Exception as e:
        print("Stripe error:", str(e))
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

def cart_count(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    count = sum([item["quantity"] for item in cart_items])

    return JsonResponse({"count": count})
