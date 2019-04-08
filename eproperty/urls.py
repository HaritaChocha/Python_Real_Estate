from django.urls import path

# Local Import
from . import views

app_name = "eproperty"


urlpatterns = [
    # Home Page
    path('', views.homePage, name='home'),

    # About Page
    path('about', views.aboutPage, name='about'),

    # Contact Page
    path('contact', views.contactPage, name='contact'),

    # Property Page
    path('property', views.viewProperty, name='property'),
    path('propertyDetail/<int:id>', views.propertyDetail, name="propertyDetail"),
    path('property/detail/delete/<int:id>', views.deleteProperty, name='deleteProperty'),
    path('property/detail/update/<int:id>', views.updateProperty, name='updateProperty'),
    path('property/detail/image/add/<int:id>', views.addPropertyImages, name='addImage'),
    path('myproperty', views.myProperty, name="myProperty"),

    # Search and Sort
    path('property/sort/<value>', views.sortProperty, name="sortProperty"),
    path('property/search', views.searchProperty, name="search"),
    path('property/filter', views.filterProperty, name="filter"),

    # Advertise
    path('advertise', views.advertiseProperty, name="advertise"),
]