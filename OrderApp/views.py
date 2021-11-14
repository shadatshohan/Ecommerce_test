from django.shortcuts import render,HttpResponse,HttpResponseRedirect,HttpResponseRedirect
from Product.models import Category,Product,Images
from OrderApp.models import ShopCart,ShopCartForm,Order,OrderForm,OrderProduct
from UserApp.models import UserProfile
from EcomApp.models import Setting
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

# Create your views here.
@login_required(login_url='/user/user_login')
def Add_to_Shopping_cart(request,id):
    url=request.META.get('HTTP_REFERER')
    current_user=request.user 
    checking=ShopCart.objects.filter(product_id=id,user_id=current_user.id)
    if checking:
        control=1
    else:
        control=0

    if request.method=='POST':
        form=ShopCartForm(request.POST)
        if form.is_valid():
            if control==1:
                data=ShopCart.objects.filter(product_id=id,user_id=current_user.id)
                data.quantity+=form.cleaned_data['quantity']
                data.save()
            else:
                data=ShopCart()
                data.user_id=current_user.id
                data.product_id=id
                data.quantity=form.cleaned_data['quantity']
                data.save()
        messages.success(request,"Your Product has been added")
        return HttpResponseRedirect(url)
    else:
        if control==1:
            data=ShopCart.objects.filter(product_id=id,user_id=current_user.id)
            data.quantity+=1
            data.save()
        else:
            data=ShopCart()
            data.user_id=current_user.id
            data.product_id=id
            data.quantity=1
            data.save()
        messages.success(request,"Your Product has been added")
        return HttpResponseRedirect(url)


def cart_details(request):
    current_user=request.user
    setting=Setting.objects.get(id=1)
    category=Category.objects.all()
    cart_product=ShopCart.objects.filter(user_id=current_user.id)
    total_amount=0
    for p in cart_product:
        total_amount+=p.product.new_price*p.quantity
    context={
         'setting':setting,
         'category':category,
         'cart_product':cart_product,
         'total_amount':total_amount}
    return render(request,'EcomApp/cart_details.html',context)

def cart_delete(request,id):
    url=request.META.get('HTTP_REFERER')
    current_user=request.user
    cart_product=ShopCart.objects.filter(id=id,user_id=current_user.id)
    cart_product.delete()
    messages.warning(request, 'Your product has been deleted.')
    return HttpResponseRedirect(url)

@login_required(login_url='/user/user_login')
def OrderCart(request):
    current_user=request.user
    shoping_cart=ShopCart.objects.filter(user_id=current_user.id)
    total_amount=0
    for qs in shoping_cart:
        total_amount+=qs.quantity*qs.product.new_price
    if request.method=='POST':
        form=OrderForm(request.POST,request.FILES)
        if form.is_valid():
            dat=Order()
            dat.first_name = form.cleaned_data['first_name']
            dat.last_name = form.cleaned_data['last_name']
            dat.address = form.cleaned_data['address']
            dat.city = form.cleaned_data['city']
            dat.phone = form.cleaned_data['phone']
            dat.country = form.cleaned_data['country']
            dat.transaction_id = form.cleaned_data['transaction_id']
            dat.transaction_image = form.cleaned_data['transaction_image']
            dat.user_id=current_user.id
            dat.total=total_amount
            dat.ip=request.META.get('REMOTE_ADDR')
            ordercode=get_random_string(6).upper()
            dat.code=ordercode
            dat.save()

            for rs in shoping_cart:
                data=OrderProduct()
                data.order_id=dat.id
                data.product_id=rs.product_id
                data.user_id=current_user.id
                data.quantity=rs.quantity
                data.price=rs.product.new_price
                data.amount=rs.amount
                data.save()

                product=Product.objects.get(id=rs.product_id)
                product.amount-=rs.quantity
                product.save()
            ShopCart.objects.filter(user_id=current_user.id).delete()
            messages.success(request,'Your order has been completed')
            category=Category.objects.all()
            setting=Setting.objects.get(id=1)
            context={
                 'ordercode':ordercode,
                 'category':category,
                 'setting':setting
            }
            return render(request,'OrderApp/ordercompleted.html',context)
        else:
            messages.warning(request,form.errors)
    form=OrderForm()
    profile=UserProfile.objects.get(user_id=current_user.id)
    total_amount=0
    for p in shoping_cart:
        total_amount+=p.product.new_price*p.quantity
    category=Category.objects.all()
    setting=Setting.objects.get(id=1)
    context= {
         'shoping_cart':shoping_cart,
         'total_amount':total_amount,
         'profile':profile,
         'form':form,
         'category':category,
         'setting':setting,
    }
    return render(request,'OrderApp/order_form.html',context)


