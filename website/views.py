from django.shortcuts import render
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'list.html', {'category': category, 'categories': categories, 'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'detail.html', {'product': product, 'cart_product_form': cart_product_form})

def index(request):
    data=Product.objects.all()
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': 100,#hardcode value
        'item_name': 'book',#hardcode value
        'invoice': '98966',#hardcode value
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('index')),
        'return_url': 'http://{}{}'.format(host, reverse('index')),
        'cancel_return': 'http://{}{}'.format(host, reverse('index')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    p={'product':data,'form':form}

    return render(request,'index.html',p)