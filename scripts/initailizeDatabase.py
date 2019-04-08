# Python script to populate all the requisite model data for actual property to add

import os, sys

os.chdir('..')
project_path = os.getcwd()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "S2G4RealEstate.settings")
sys.path.append(project_path)

os.chdir(project_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from eproperty.models import *

# PropertyDirection
for tag in [(tag.name) for tag in DirectionChoice]:
    try:
        instance = PropertyDirection(propertyDirection=tag)
        instance.save()
    except:
        pass 

print('Property Directions Created:')
print(PropertyDirection.objects.all())

# # PropertyCategory
for tag in [(tag.name) for tag in CategoryChoice]:
    try:
        instance = PropertyCategory(propertyCategory=tag)
        instance.save()
    except:
        pass 

print('Property Category Created:')
print(PropertyCategory.objects.all())

# # PropertySector
for tag in [(tag.name) for tag in SectorChoice]:
    try:
        instance = PropertySector(propertySector=tag)
        instance.save()
    except:
        pass 

print('Property Sectors Created:')
print(PropertySector.objects.all())

# Country
try:
    country1 = Country(countryName='Canada')
    country2 = Country(countryName='United States of America')
    country1.save()
    country2.save()
except:
    pass

print('Countries Created:')
print(Country.objects.all())

# Province
country1 = Country.objects.get(countryName='Canada')
country2 = Country.objects.get(countryName='United States of America')
try:
    province = Province(countryName=country1, provinceName='Quebec')
    province.save()
    province = Province(countryName=country1, provinceName='Ontario')
    province.save()
    province = Province(countryName=country2, provinceName='Michigan')
    province.save()
except:
    pass
print('Province Created:')
print(Province.objects.all())

# Cities
province1 = Province.objects.get(provinceName='Quebec')
province2 = Province.objects.get(provinceName='Ontario')
province3 = Province.objects.get(provinceName='Michigan')
try:
    city = City(countryName=country1, provinceName=province1, cityName='Montreal')
    city.save()
    city = City(countryName=country1, provinceName=province1, cityName='Quebec City')
    city.save()
    city = City(countryName=country1, provinceName=province2, cityName='Toronto')
    city.save()
    city = City(countryName=country1, provinceName=province2, cityName='Windsor')
    city.save()
    city = City(countryName=country2, provinceName=province3, cityName='Detroit')
    city.save()
except:
    pass

print('Cities Created:')
print(City.objects.all())

