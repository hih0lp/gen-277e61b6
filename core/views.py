from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Order, OrderItem
from .forms import RegistrationForm, CheckoutForm
from .cart import Cart

def home(request):
    featured_products = Product.objects.filter(available=True)[:6]
    categories = Category.objects.all()[:4]
    return render(request, 'core/home.html', {'featured_products': featured_products, 'categories': categories})

def catalog(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'core/catalog.html', {'category': category, 'categories': categories, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'core/product_detail.html', {'product': product})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'core/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity)
    messages.success(request, f'{product.name} добавлен в корзину')
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'{product.name} удалён из корзины')
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart:
        return redirect('cart_detail')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            messages.success(request, 'Заказ оформлен успешно!')
            return redirect('order_detail', order_id=order.id)
    else:
        initial = {'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email, 'phone': request.user.phone, 'address': request.user.address}
        form = CheckoutForm(initial=initial)
    return render(request, 'core/checkout.html', {'cart': cart, 'form': form})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'core/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация успешна! Войдите в аккаунт.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})
