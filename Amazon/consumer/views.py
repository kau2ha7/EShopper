from django.shortcuts import render,redirect
from django.views import View
from .forms import CustomerForm,CustomerProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Customer,Product,Cart,OrderPlaced
from django.db.models import Q
from django.http import JsonResponse



# Create your views here.
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerForm()
        return render(request,'consumer/profile.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            fm = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            fm.save()
            return render(request,'consumer/profile.html',{'form':form,'active':'btn-primary'})
class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        sleepwear = Product.objects.filter(category='SW')
        shoes = Product.objects.filter(category = 'S')
        jackets = Product.objects.filter(category='J')
        blazzers = Product.objects.filter(category = 'B')
        shirts = Product.objects.filter(category = 'SS')
        jeans = Product.objects.filter(category='JS')
        return render(request,'consumer/index.html',{'topwears':topwears,'bottomwears':bottomwears,'sleepwear':sleepwear,'shoes':shoes,'jackets':jackets,'blazzers':blazzers,'shirts':shirts,'jeans':jeans})
    
class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_exists = False
        if request.user.is_authenticated:
            item_exists = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'consumer/productdetail.html',{'product':product,'item_exists':item_exists})
    
# Cart
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user 
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount +=tempamount
                totalamount = amount + shipping_amount
            return render(request,'consumer/addtocart.html',{'cart':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'consumer/emptycart.html')
   

def minus_cart(request):
  if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        # Get all cart items for the given product and user
        cart_items = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
        
        # Check if there's at least one cart item and then decrement the quantity of the first one.
        if cart_items.exists():
            cart_item = cart_items.first()
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                # Optionally, you could delete the item if quantity reaches zero
                cart_item.delete()
        else:
            return JsonResponse({"error": "Cart item not found."}, status=404)

        # Calculate amounts
        amount = 0.0
        shipping_amount = 70.0
        cart_products = Cart.objects.filter(user=request.user)
        
        for p in cart_products:
            temp_amount = p.quantity * p.product.discounted_price
            amount += temp_amount

        data = {
            'prod_id': prod_id,  # Including prod_id in the response for frontend targeting
            'quantity': cart_item.quantity if cart_items.exists() else 0,
            'amount': amount,
            'totalamount': amount + shipping_amount,
        }

        return JsonResponse(data)
    
def plus_cart(request):
 if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        # Get all cart items for the given product and user
        cart_items = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
        
        # Check if there's at least one cart item and then increment the quantity of the first one.
        if cart_items.exists():
            cart_item = cart_items.first()
            cart_item.quantity += 1
            cart_item.save()
        else:
            return JsonResponse({"error": "Cart item not found."}, status=404)

        # Calculate amounts
        amount = 0.0
        shipping_amount = 70.0
        cart_products = Cart.objects.filter(user=request.user)
        
        for p in cart_products:
            temp_amount = p.quantity * p.product.discounted_price
            amount += temp_amount

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }

        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        # Filter for all cart items for the given product and user and delete them
        Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).delete()
        
        # Calculate the new total amount
        amount = 0.0
        shipping_amount = 70.0
        cart_products = Cart.objects.filter(user=request.user)  # Fetch only the current user's cart items
        
        for p in cart_products:
            temp_amount = p.quantity * p.product.discounted_price
            amount += temp_amount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount,
        }

        return JsonResponse(data)
    

def topwears(request,data=None):
    if data is None:
        topwears = Product.objects.filter(category='TW')
    if data == 'Prada' or data == 'Polo' or data == 'Friends' or data == 'Puma' or data == 'Levis' or data == 'Lee_Cooper' or data == 'Lee' or data == 'Louis_Philippe':
        if data is not None:
            normalised_data = data.replace('_',' ')
        topwears = Product.objects.filter(category='TW').filter(brand=normalised_data)
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=5000)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=5000)
    return render(request,'consumer/topwears.html',{'topwears':topwears})
    

def bottomwears(request,data=None):
    if data is None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'Prada' or data == 'Fendi' or data == 'Adidas' or data == 'H_M' or data == 'Chanel' or data == 'Gucci' or data == 'Hermes' or data == 'Burberry' or data == 'Louis_Philippe' or data == 'Calvin_Klein' or data == 'Zara':
        if data is not None:
            normalised_data = data.replace('_',' ')
        bottomwears = Product.objects.filter(category='BW').filter(brand=normalised_data)
    elif data == 'below':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=5000)
    elif data == 'above':
        bottomwears = Product.objects.filter(category='TW').filter(discounted_price__gt=5000)
    return render(request,'consumer/bottomwears.html',{'bottomwears':bottomwears})

def sleepwears(request,data=None):
    if data is None:
        sleepwears = Product.objects.filter(category='SW')
    elif data == 'Natori' or data == 'Lanya' or data == 'Skin' or data == 'Pajamagram' or data == 'Barefoot_Dreams' or data == 'Calvin_Klein' or data == 'Victoria_Secret' or data == 'Eberjay':
        if data is not None:
            normalized_data = data.replace('_',' ')
        sleepwears = Product.objects.filter(category='SW').filter(brand=normalized_data)
    elif data == 'below':
        sleepwears = Product.objects.filter(category='SW').filter(discountef_price__lt=5000)
    elif data == 'above':
        sleepwears = Product.objects.filter(category='SW').filter(discounted_price__gt=5000)
    return render(request,'consumer/sleepwears.html',{'sleepwears':sleepwears})
def shoes(request,data=None):
    if data is None:
        shoes = Product.objects.filter(category='S')
    elif data == 'Prada' or data == 'Nike' or data == 'Adidas' or data == 'Bata' or data == 'Lee' or data == 'Gucci' or data == 'Oxford' or data == 'Clarks' or data == 'Levis':
        shoes = Product.objects.filter(category='S').filter(brand=data)
    elif data == 'below':
        shoes = Product.objects.filter(category='S').filter(discounted_price__lt=5000)
    elif data == 'above':
        shoes = Product.objects.filter(category='S').filter(discounted_price__gt=5000)
    return render(request,'consumer/shoes.html',{'shoes':shoes})

def jackets(request,data=None):
    if data is None:
        jackets = Product.objects.filter(category='J')
    elif data == 'Monte_Carlo' or data == 'Alley_Solley' or data == 'Woodland' or data == 'Gucci' or data == 'Parx' or data == 'Peter_England' or data == 'Royal_Enfield' or data == 'Levis':
        if data is not None:
            normalized_data = data.replace('_',' ')
        jackets = Product.objects.filter(category='J').filter(brand=normalized_data)
    elif data == 'below':
        jackets = Product.objects.filter(category='J').filter(discounted_price__lt=5000)
    elif data == 'above':
        jackets = Product.objects.filter(category='J').filter(discounted_price__gt=5000)
    return render(request,'consumer/jackets.html',{'jackets':jackets})

def blazzers(request,data=None):
    if data is None:
        blazzers = Product.objects.filter(category='B')
    elif data == 'Raymond' or data == 'Jack_and_Jones' or data == 'Arrow' or data == 'Louis_Philippe' or data == 'Alley_Solley' or data == 'Van_Heusen' or data == 'Gucci' or data == 'Peter_England' or data == 'Lee' or data == 'Tommy_Hielfiger' or data == 'Canary_London' or data == 'Parx':
        if data is not None:
            normalized_data = data.replace('_',' ')
        blazzers = Product.objects.filter(category='B').filter(brand=normalized_data)
    elif data == 'below':
        blazzers = Product.objects.filter(category='B').filter(discounted_price__lt=5000)
    elif data == 'above':
        blazzers = Product.objects.filter(category='B').filter(discounted_price__gt=5000)
    return render(request,'consumer/blazzers.html',{'blazzers':blazzers})

def shirts(request,data=None):
        if data is None:
            shirts = Product.objects.filter(category='SS')
        elif data == 'Louis_Philippe' or data == 'Prada' or data == 'Fendi' or data == 'Woodland' or data == 'Parx' or data == 'Oxford' or data == 'Lee':
            if data is not None:
                normalized_data = data.replace('_',' ')
            shirts = Product.objects.filter(category='SS').filter(brand=normalized_data)
        elif data == 'below':
            shirts = Product.objects.filter(category='SS').filter(discounted_price__lt=5000)
        elif data == 'above':
            shirst = Product.objects.filter(category='SS').filter(discounted_price__gt=5000)
        return render(request,'consumer/shirts.html',{'shirts':shirts})
  

def jeans(request,data=None):
    if data is None:
        jeans = Product.objects.filter(category='JS')
    elif data == 'Levis' or data == 'Alley_Solley' or data == 'Louis_Philippe' or data == 'Lee' or data == 'Puma' or data == 'Papa_Jeans' or data == 'Fendi' or data == "Peter_England" or data == 'Arrow' or data == 'Van_Heusen' or data == 'Prada':
        if data is not None:
            normalized_data = data.replace('_',' ')
        jeans = Product.objects.filter(category='JS').filter(brand=normalized_data)
    elif data == 'below':
        jeans = Product.objects.filter(category='JS').filter(discounted_price__lt=5000)
    elif data == 'above':
        jeans = Product.objects.filter(category='jS').filter(discounted_price__gt=5000)
    return render(request,'consumer/jeans.html',{'jeans':jeans})

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'consumer/address.html',{'add':add,'active':'btn-primary'})

@login_required
def order(request):
    print('dkakfka')
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request,'consumer/orders.html',{'order_placed':op})

@login_required
def checkout(request):
    user = request.user 
    add = Customer.objects.filter(user=request.user)
    cart_items = Cart.objects.filter(user=user)
    totalamount=0.0
    amount = 0.0
    shipping_amount = 70.0
    tempamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount +=tempamount
            totalamount = amount + shipping_amount
    return render(request,'consumer/checkout.html',{'add':add,'totalamount':totalamount,'tempamount':tempamount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user 
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

def search(request):
    query = request.GET.get('query')
    # q = Q(Q(brand__icontains=query) | Q(category__icontains=query))
    product = Product.objects.filter(brand__icontains=query)


    return render(request,'consumer/search.html',{'product':product})








