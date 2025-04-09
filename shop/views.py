from django.shortcuts import render
from django.http import HttpResponse, response
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json

# Create your views here.


def index(request):
    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "shop/index.html", params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        Name = request.POST.get('name', '')
        Email = request.POST.get('email', '')
        Phone = request.POST.get('phone', '')
        Desc = request.POST.get('desc', '')

        contact = Contact(name=Name, email=Email, phone=Phone, desc=Desc)
        print(type(contact))
        contact.save()
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get('orderId', '')
        Email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderid, email=Email)
            if len(order) > 0:
                Update = OrderUpdate.objects.filter(order_id=orderid)
                updates = []
                for item in Update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates,order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, 'shop/tracker.html')

def searchMatch(query,item):
    if query.lower() in ((item.desc.lower()) or (item.product_name.lower()) or  (item.category.lower()) or (item.subcategory.lower())):
        print("Item is", item)
        return True
    else:    
        return False

def search(request):
    query=request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        print("prod is",prod) 
        print(query) 
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if n != 0:
            allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "shop/index.html", params)
    # return render(request, 'shop/search.html')


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'Vproduct': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + \
            " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        checkout = Order(items_json=items_json, name=name, email=email,
                         address=address, city=city, state=state, zip_code=zip_code, phone=phone)
        checkout.save()
        update = OrderUpdate(order_id=checkout.order_id,
                             update_desc="The order has been placed")
        update.save()
        thank = True
        id = checkout.order_id
        print(type(checkout))
        return render(request, 'shop/checkout.html',{'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')
