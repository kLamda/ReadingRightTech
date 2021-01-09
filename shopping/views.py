from django.shortcuts import render, redirect
from .models import ShoppingItem
from django.contrib.auth import get_user_model
from itertools import groupby
import uuid
# Create your views here.
def key_func(k):
    return k['date']
def view_list(request):
    if request.user.id != None:
        if request.method == "POST":
            data = []
            # print("Filter request", request)
            for objects in ShoppingItem.objects.all().filter(userID=request.user.id, date = request.POST['date']):
                # print("Filtered objects", objects)
                data.append({"itemName": objects.itemName, "quantity": objects.quantityItem, "date": objects.date,
                                 "status": objects.status,
                                 "pending": True if objects.status == "0" else False,
                                 "bought": True if objects.status == "1" else False,
                                 "not_available": True if objects.status == "2" else False, "uniqueID": objects.id})
            INFO = sorted(data, key=key_func)
            data_1 = []
            for key, value in groupby(INFO, key_func):
                a = []
                a.append(str(key))
                a.append(list(value))
                data_1.append(a)
            return render(request, 'shopping/index.html', context={"data": data_1})
        data = []
        for objects in ShoppingItem.objects.all().filter(userID=request.user.id):
            date_item = objects.date
            data.append({"itemName" : objects.itemName,"quantity": objects.quantityItem,"date": str(date_item), "status": objects.status,
                             "pending" : True if objects.status=="0" else False, "bought" : True if objects.status == "1" else False,
                             "not_available" : True if objects.status=="2" else False, "uniqueID": objects.id})
        INFO = sorted(data, key=key_func)
        data_1 = []
        for key, value in groupby(INFO, key_func):
            a = []
            a.append(str(key))
            a.append(list(value))
            data_1.append(a)
        return render(request, 'shopping/index.html', context={"data" : data_1})
    else:
        return redirect('accounts:login')

def add_list(request):
    if request.user.id != None:
        if request.method == "POST":
            current_user = request.user.id
            name = request.POST['item_name']
            quantity = request.POST['item_quantity']
            select_flag = request.POST['select_flag']
            date = request.POST['date']
            if len(name) == 0 or len(quantity) == 0 or len(date) == 0:
                return render(request, 'shopping/add.html', context = {"error" : "Fill all the quantity of form"})
            ShoppingItem(id=uuid.uuid4(), userID= current_user,itemName = name, quantityItem = quantity, status = select_flag, date = date).save()
            return redirect('shopping:index')
        return render(request, 'shopping/add.html')
    else:
        return redirect("accounts:login")

def update_list(request):
    if request.user.id != None:
        if request.POST['submit_item'] == "Delete":
            ShoppingItem.objects.all().get(id=request.POST["uniqueID"]).delete()
            return redirect('shopping:index')
        elif request.POST['submit_item'] == "Update":
            item_id = request.POST['uniqueID']
            item_name = request.POST['itemName']
            itemQuantity = request.POST['itemQuantity']
            itemStatus = request.POST['itemStatus']
            itemDate = request.POST['itemDate']
            context = {'uniqueID' : item_id, 'item_name' : item_name, "item_quantity" : itemQuantity, "item_status" : itemStatus, "item_date" : itemDate}
            # print("index context", context)
            return render(request, 'shopping/update.html', context)
        elif request.POST['submit_item'] == "Update_list":
            # print(request.POST["uniqueID"])
            item = ShoppingItem.objects.all().get(userID=request.user.id, id=request.POST["uniqueID"])
            item.itemName = request.POST['itemNameUpdate']
            item.quantityItem = int(request.POST['itemQuantityUpdate'])
            item.status = request.POST['itemStatusUpdate']
            item.date = request.POST['itemDateUpdate']
            item.save()
            return redirect('shopping:index')
        return render(request, 'shopping/update.html')
    else:
        return redirect("accounts:login")