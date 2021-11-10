from django.shortcuts import render,HttpResponse,HttpResponseRedirect,HttpResponseRedirect
from Product.models import Category,Product,Images
from OrderApp.models import ShopCart,ShopCartForm
from EcomApp.models import Setting

# Create your views here.
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
    return HttpResponseRedirect(url)