from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Local Import
from .models import PropertyCategory, PropertySector, Property, PropertyImages, PropertySector
from .forms import PropertyForm, PropertyImageForm

# Global Variable
properties = Property.objects.all()
categories = PropertyCategory.objects.all()
sectors = PropertySector.objects.all()

# Helper Functions
def save_image(image_form, single_property):
    image_form.propertyID = single_property
    image_form.save()

def get_address(single_property):
    street_num = single_property.propertyStreetNumber
    street_name = single_property.propertyStreet
    street_postal = single_property.propertyPostalCode
    city = single_property.propertyCity.cityName
    province = single_property.propertyProvince.provinceName

    return '{} {}, {}, {}, {}'.format(street_num, street_name, street_postal, city, province) 

def tagPropertyWithImage(properties):
    for single_property in properties:
        images = PropertyImages.objects.filter(propertyID=single_property)
        if images:
            single_property.propertyImage = images[0].propertyImage

# Home View
def homePage(request):
    
    context= {
        'categories': categories,
        'sector': sectors
    }
    return render(request, "eproperty/home.html", context)

# About View
def aboutPage(request):
    return render(request, 'eproperty/about.html')

# Contact Page
def contactPage(request):
    return render(request, 'eproperty/contact.html')

# Property CRUD Operations
def viewProperty(request):
    properties = Property.objects.all().order_by('propertyPostedDate')
    tagPropertyWithImage(properties)

    paginate = Paginator(properties, 10)
    page = request.GET.get('page')
    property_list = paginate.get_page(page)

    context = {
        'properties': property_list,
        'categories': categories,
        'sectors': sectors
    }
    return render(request, "eproperty/property.html", context)

def propertyDetail(request, id):
    single_property = Property.objects.get(propertyID=id)
    property_images = PropertyImages.objects.filter(propertyID=single_property)

    single_property.address = get_address(single_property)

    context = {
        'property': single_property,
        'property_images': property_images
    }
    return render(request, 'eproperty/propertyDetail.html', context)

@login_required
def deleteProperty(request, id):
    user = request.user
    single_property = get_object_or_404(Property, propertyID=id)
    if  user.is_authenticated and user.is_active and single_property.user==user:
        single_property.delete()
    else:
        print("Authentication Error")  
    return redirect('eproperty:property')

@login_required
def updateProperty(request, id):
    single_property = get_object_or_404(Property, propertyID=id)
    user = request.user

    if request.method == 'POST':
        property_form = PropertyForm(request.POST or None, instance=single_property)
        if property_form.is_valid() and user.is_authenticated and user.is_active and single_property.user==user:
            property_form.save()
            return redirect('eproperty:propertyDetail', id=id)
        else:
            print('error')
    else:
        property_form = PropertyForm(instance=single_property)
    context = {
        'form': property_form,
        'source': 'Update Property'
    }
    return render(request, 'eproperty/form.html', context)

# Add Property Image
def addPropertyImages(request, id):
    single_property = get_object_or_404(Property, propertyID=id)

    if request.method == 'POST':
        property_image_form = PropertyImageForm(request.POST, request.FILES)

        if property_image_form.is_valid():
            image_form = property_image_form.save(commit=False)
            save_image(image_form, single_property)
            return redirect('eproperty:propertyDetail', id=id)
    else:
        property_image_form = PropertyImageForm()
    context = {
        'property_image_form':property_image_form,
        'source': 'Add Image'
    }
    return render(request, 'eproperty/form.html', context) 

# Advertise New Property
@login_required
def advertiseProperty(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        property_image_form = PropertyImageForm(request.POST, request.FILES)
        if property_form.is_valid() and property_image_form.is_valid():
            if request.user.is_authenticated  and request.user.is_active:
                prop_form = property_form.save(commit=False)
                prop_form.user = request.user
                prop_form.save()
                image_form = property_image_form.save(commit=False)
                save_image(image_form, prop_form)
                return redirect('eproperty:property')
            else:
                raise ValueError('User Authentication Error')
        else:
            print('error')
    else:
        property_form = PropertyForm()
        property_image_form = PropertyImageForm()

    context ={
        'form':property_form,
        'property_image_form': property_image_form,
        'source': 'Add New Property'
    }

    return render(request, 'eproperty/form.html', context)

@login_required
def myProperty(request):
    user = request.user
    if user.is_authenticated  and user.is_active:
        properties = Property.objects.filter(user=user)
    if properties:
        tagPropertyWithImage(properties)

    print(properties)
    paginate = Paginator(properties, 10)
    page = request.GET.get('page')
    property_list = paginate.get_page(page)

    context = {
        'properties': property_list,
        'categories': categories,
        'sectors': sectors,
    }
    return render(request, "eproperty/property.html", context)

# Search and Sort
def sortProperty(request, value):
    
    if value == 'name':
        properties = Property.objects.order_by('propertyName')
    elif value == 'price':
        properties = Property.objects.order_by('propertySellingPrice')
    else:
        properties = Property.objects.order_by('-propertyPostedDate')
    
    tagPropertyWithImage(properties)

    paginate = Paginator(properties, 10)
    page = request.GET.get('page')
    property_list = paginate.get_page(page)

    context = {
        'properties': property_list,
        'categories': categories,
        'sectors': sectors
    }
    return render(request, "eproperty/property.html", context)

def searchProperty(request):
    query = request.GET.get('q')
    print(query)
    properties = Property.objects.filter(Q(pk__icontains=query) |
                                     Q(propertyName__icontains=query) |
                                     Q(propertyDescription__icontains=query) |
                                     Q(propertyCategory__propertyCategory__icontains=query) |
                                     Q(propertySector__propertySector__icontains=query) |
                                     Q(PropertyDirection__propertyDirection__icontains=query) |
                                     Q(propertyCountry__countryName__icontains=query) |
                                     Q(propertyProvince__provinceName__icontains=query) |
                                     Q(propertyCity__cityName__icontains=query) |
                                     Q(propertyStreet__icontains=query)
                                     )
    
    tagPropertyWithImage(properties)

    paginate = Paginator(properties, 10)
    page = request.GET.get('page')
    property_list = paginate.get_page(page)

    context = {
        'properties': property_list,
        'categories': categories,
        'sectors': sectors
    }
    return render(request, "eproperty/property.html", context)

def filterProperty(request):
    category = request.GET.getlist('category')
    sector = request.GET.getlist('sector')
    location = request.GET.get('location')
    room = request.GET.getlist('room')
    hall = request.GET.getlist('hall')
    bathroom = request.GET.getlist('bathroom')
    minprice = request.GET.get('minprice')
    maxprice = request.GET.get('maxprice')
    
    properties = Property.objects.all()

    if category:
        properties = properties.filter(propertyCategory__propertyCategory__in=category)
    
    if sector:
        properties = properties.filter(propertySector__propertySector__in=sector)

    if location:
        properties = properties.filter(
                                     Q(propertyCountry__countryName__icontains=location) |
                                     Q(propertyProvince__provinceName__icontains=location) |
                                     Q(propertyCity__cityName__icontains=location) |
                                     Q(propertyStreet__icontains=location) |
                                     Q(propertyPostalCode__icontains=location)
                                     )

    if room:
        properties = properties.filter(propertyNoOfRooms__in=room)
    
    if hall:
        properties = properties.filter(propertyNoOfHalls__in=hall)
    
    if bathroom:
        properties = properties.filter(propertyNoOfBathrooms__in=bathroom)

    if minprice:
        properties = properties.filter(propertySellingPrice__gte=minprice)

    if maxprice:
        properties = properties.filter(propertySellingPrice__lte=maxprice)
    
    print(properties)
    
    tagPropertyWithImage(properties)

    paginate = Paginator(properties, 10)
    page = request.GET.get('page')
    property_list = paginate.get_page(page)

    context = {
        'properties': property_list,
        'categories': categories,
        'sectors': sectors
    }
    return render(request, "eproperty/property.html", context)

