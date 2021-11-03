from django.shortcuts import render
from django.http import HttpResponse
from EcomApp.models import Setting
from Product.models import Product,Images,Category
# Create your views here.
def home(request):
	setting=Setting.objects.get(id=1)
	category=Category.objects.all()
	slide_images=Product.objects.all().order_by('id')[:3]
	latest_product=Product.objects.all().order_by('-id')
	featured_product=Product.objects.all().order_by('id')
	context={'setting':setting,
	    'slide_images':slide_images,
	    'latest_product':latest_product,
	    'featured_product':featured_product,
	    'category':category
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