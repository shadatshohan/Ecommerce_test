from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from EcomApp.models import Setting,ContactForm,ContactMessage
from Product.models import Product,Images,Category
from EcomApp.forms import SearchForm
from OrderApp.models import ShopCart
# Create your views here.
def home(request):
    current_user=request.user
    cart_product=ShopCart.objects.filter(user_id=current_user.id)
    total_amount=0
    for p in cart_product:
        total_amount+=p.product.new_price*p.quantity
    total_quan=0
    for p in cart_product:
        total_quan+=p.quantity
    setting=Setting.objects.get(id=1)
    category=Category.objects.all()
    slide_images=Product.objects.all().order_by('id')[:3]
    latest_product=Product.objects.all().order_by('-id')
    featured_product=Product.objects.all().order_by('id')
    context={'setting':setting,
        'slide_images':slide_images,
        'latest_product':latest_product,
        'featured_product':featured_product,
        'category':category,
        'cart_product': cart_product,
        'total_amount': total_amount,
        'total_quan': total_quan
        }
    return render(request,'EcomApp/home.html',context)
def product_single(request,id):
    setting=Setting.objects.get(id=1)
    category=Category.objects.all()
    single_product=Product.objects.get(id=id)
    images=Images.objects.filter(product_id=id)
    product=Product.objects.all().order_by('id')[:4]
    context={'setting':setting,'single_product':single_product,'images':images,'product':product,'category':category}
    return render(request,'EcomApp/product_single.html',context)
def category_product(request, id, slug):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    sliding_images = Product.objects.all().order_by('id')[:2]
    product_cat = Product.objects.filter(category_id=id)
    context = {
        'category': category,
        'setting': setting,
        'product_cat': product_cat,
        'sliding_images': sliding_images,
    }
    return render(request, 'EcomApp/category_products.html', context)


def about(request):
    category=Category.objects.all()
    context={'category':category}
    return render(request,'EcomApp/about.html',context)

def contact(request):
    category=Category.objects.all()
    setting=Setting.objects.get(id=1)
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            data=ContactMessage()
            data.name=form.cleaned_data['name']
            data.email=form.cleaned_data['email']
            data.subject=form.cleaned_data['subject']
            data.message=form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            return redirect('contact_dat')
    form=ContactForm
    print(form)
    context={
    'form':form,
    'category':category,
    'setting':setting
    }
    return render(request,'EcomApp/contact_form.html',context)


def SearchView(request):
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            query=form.cleaned_data['query']
            cat_id=form.cleaned_data['cat_id']
            if cat_id==0:
                products=Product.objects.filter(title__icontains=query)
            else:
                products=Product.objects.filter(title__icontains=query,category_id=cat_id)
            category=Category.objects.all()
            sliding_images=Product.objects.all().order_by('id')[:2]
            setting=Setting.objects.get(pk=1)
            context = {
                'category': category,
                'query': query,
                'product_cat': products,
                'sliding_images': sliding_images,
                'setting': setting,
            }
            return render(request,'EcomApp/category_products.html',context)
    return HttpResponseRedirect('category_product')

