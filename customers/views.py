from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime
from django.http import Http404  
from django.db.models import F, Q, CharField, Value
from django.db import connection
from django.urls import reverse
# Model
from customers.models import Customer

# Create your views here.

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'website', 'address']


@login_required
def datatable(request):
    if request.method == 'POST':


        ## Action Buttons ( Addtional Buttons )
        actionButton = ""
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("customers.show", kwargs={'pk': 0})+"' class='btn btn-sm btn-success btn-show'><i class='fa fa-search'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("customers.edit", kwargs={'pk': 0})+"' class='btn btn-sm btn-info btn-edit'><i class='fa fa-edit'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("customers.delete", kwargs={'pk': 0})+"' class='btn btn-sm btn-danger btn-delete'><i class='fa fa-trash'></i></a>"
      
        ## Read value
        draw =  int(request.POST.get("draw"))
        row =  int(request.POST.get("start"))
        rowperpage =  int(request.POST.get("length"))
        columnIndex =  request.POST.get("order[0][column]")
        columnName =   request.POST.get("columns["+columnIndex+"][name]")
        columnSortOrder =   request.POST.get("order[0][dir]")
        searchValue =  request.POST.get("search[value]")


        ## Total number of records without filtering
        getData = Customer.objects
        totalRecord = getData.count()

        ## Total number of records with filtering  
        ## Search
        getFilter = getData
        
        if(searchValue !=""):
            getFilter = getData.filter(Q(name__contains=searchValue) | Q(phone__contains=searchValue) | Q(email__contains=searchValue) | Q(website__contains=searchValue) | Q(address__contains=searchValue))
        
        totalRecordFilter = getFilter.count()
        getDataOrder =  getFilter

        if(columnSortOrder == "desc"):
            getDataOrder =  getFilter.order_by('-'+columnName)
        else:
            getDataOrder =  getFilter.order_by(columnName)

        aaData = getDataOrder[row:(row + rowperpage)].values(
            key_id = F('id'),
            customer_name = F('name'),
            customer_email = F('email'),
            customer_phone = F('phone'),
            customer_website = F('website'),
            customer_addresss = F('address'),
        ).annotate(action=Value(actionButton, output_field=CharField()))
       

        response = {
            "draw":draw,
            "iTotalRecords":int(totalRecord),
            "iTotalDisplayRecords":int(totalRecordFilter),
            "aaData":list(aaData)
        }

        #print(connection.queries)

        return JsonResponse(response)

    raise Http404         
    

@login_required
def index(request, template_name='app/customer/index.html'):
    return render(request, template_name)


@login_required
def create(request, template_name='app/customer/form.html'):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_at = datetime.now()
        obj.save()
        messages.success(request, 'Record created successfully')
        customer = Customer.objects.latest('id')
        return redirect('customers.show', pk=customer.id)
    return render(request, template_name, {'form':form, 'type': 'create', 'page_name' : 'Customer'})

@login_required
def show(request, pk, template_name='app/customer/show.html'):
    customer= get_object_or_404(Customer, pk=pk)
    return render(request, template_name, {'customer':customer})

@login_required
def edit(request, pk, template_name='app/customer/form.html'):
    customer= get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        messages.success(request, 'Record updated successfully')
        return redirect('customers.show', pk=pk)
    return render(request, template_name, {'form':form, 'type': 'edit', 'page_name' : 'Customer'})

@login_required
def delete(request, pk):
    customer= get_object_or_404(Customer, pk=pk)
    if customer:
        customer.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('customers.index')