from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from .forms import CreateProductForm, UpdateProductForm
from .models import Category, Product


def index(request):
    categories = Category.objects.all()

    return render(request, 'index.html',
                  {'categories': categories})


def products_list(request, slug):
    products = Product.objects.filter(category__slug=slug)
    return render(request, 'list.html',
                  {'products': products})


def product_detail(request, product_id):
    # product = Product.objects.get(pk=product_id)
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'detail.html', locals())



def product_create(request):
    if request.method == 'POST':
        print(request.POST)
        product_form = CreateProductForm(request.POST,
                                         request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            return redirect('detail', product.id)
    else:
        product_form = CreateProductForm()
    return render(request, 'create_product.html', locals())


def product_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_form = UpdateProductForm(request.POST or None,
                                     request.FILES or None,
                                     instance=product)
    if product_form.is_valid():
        product_form.save()
        return redirect('detail', product_id)
    return render(request, 'update_product.html', locals())


def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        slug = product.category.slug
        product.delete()
        return redirect('list', slug)
    return render(request, 'delete_product.html', locals())


""" Cart Views """


@login_required()
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required()
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required()
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required()
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required()
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required()
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')