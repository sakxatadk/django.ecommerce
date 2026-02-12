from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from .forms import ProductForm , UserRegistrationForm
from django.shortcuts import get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q


# Create your views here.
def all_products(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()
    return render(request , 'myapp/all_products.html',{'products': products , 'query':query})

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST , request.FILES)
        if form.is_valid():
           product = form.save(commit = False)
           product.user = request.user
           product.save()
           return redirect('all_products')
    else:
        form = ProductForm()
    return render(request , 'products_form.html',{'form': form})

@login_required
def product_edit(request , product_id):
    product = get_object_or_404(Product, pk =product_id , user = request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST , request.FILES , instance= product)
        if form.is_valid():
           product = form.save(commit = False)
           product.user = request.user
           product.save()
           return redirect('all_products')
    else:
        form = ProductForm(instance = product)
        return render(request , 'products_form.html',{'form': form})

@login_required
def product_delete(request , product_id):
    product= get_object_or_404(Product , pk=product_id , user = request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('all_products')
    return render(request , 'products_confirm_delete.html',{'product': product})

    
def register(request):
    if request.method == 'POST':
        form= UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('all_products')
        
    else:
        form = UserRegistrationForm()
    return render(request , 'registration/register.html',{'form': form})
















