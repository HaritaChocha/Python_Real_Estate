from django.db import models
from datetime import date
from django.utils import timezone
from enum import Enum
from S2G4RealEstate.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL

# Helper Class
class CategoryChoice(Enum):
    SingleHouse = 'Single House'
    AttachedHouse = 'Attached House'
    TownHouse = 'Town House'
    Apartment = 'Apartment'
    Store = 'Store'
    Farm = 'Farm'
    Factory = 'Factory'
    Mall = 'Mall'
    Building = 'Building'
    Other = 'Other'

class SectorChoice(Enum):
    Private = 'Private'
    Residential = 'Residential'
    Commercial = 'Commercial'
    Government = 'Government'
    Rural = 'Rural'
    Other = 'Other'

class DirectionChoice(Enum):
    North = 'North'
    South = 'South'
    East = 'East'
    West = 'West'
class DealingChoice(Enum):
    Buy = 'Buy'
    Sell = 'Sell'
    Rent = 'Rent'

# Selectional Models
class PropertyDirection(models.Model):
    propertyDirection = models.CharField(
      max_length=5,
      choices=[(tag.name, tag.value) for tag in DirectionChoice],
      default=DirectionChoice.North,
      unique=True,
      verbose_name='Property Direction'
    )

    def __str__(self):
        return self.propertyDirection

class PropertyCategory(models.Model):
    propertyCategory = models.CharField(
      max_length=15,
      choices=[(tag.name, tag.value) for tag in CategoryChoice],
      default=CategoryChoice.SingleHouse,
      unique=True,
      verbose_name='Property Category'
    )

    def __str__(self):
        return self.propertyCategory
class PropertySector(models.Model):
    propertySector = models.CharField(
      max_length=15,
      choices=[(tag.name, tag.value) for tag in SectorChoice],
      default=SectorChoice.Private,
      unique=True,
      verbose_name='Property Sector'
    )

    def __str__(self):
        return self.propertySector

# Address Models
class Country(models.Model):
    countryName = models.CharField(max_length = 50, unique=True)

    def __str__(self):
        return self.countryName

class Province(models.Model):
    countryName = models.ForeignKey(Country, on_delete=models.CASCADE)
    provinceName = models.CharField(max_length = 50, unique=True)

    def __str__(self):
        return self.provinceName

class City(models.Model):

    countryName = models.ForeignKey(Country, on_delete=models.CASCADE)
    provinceName = models.ForeignKey(Province, on_delete=models.CASCADE)
    cityName = models.CharField(max_length = 50, unique=True)

    def __str__(self):
        return self.cityName

# Property Models
class Property(models.Model):
    user = models.ForeignKey(User, null=False, blank = False, on_delete=models.CASCADE)

    propertyID = models.AutoField(unique=True, primary_key=True, verbose_name='Property ID')
    propertyName = models.CharField(max_length=50, blank=False, null=False, verbose_name='Title')
    propertyDescription = models.TextField(default='Not Available', verbose_name='Description')

    propertyCategory = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE, verbose_name='Category')
    propertySector = models.ForeignKey(PropertySector, on_delete=models.CASCADE, verbose_name='Sector')
    PropertyDirection = models.ForeignKey(PropertyDirection, on_delete=models.CASCADE, verbose_name='Direction')
    
    propertyCountry = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Country')
    propertyProvince = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='Province')
    propertyCity = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='City')
    propertyStreet = models.CharField(max_length=100, verbose_name='Street Name')
    propertyPostalCode = models.CharField(max_length=6, verbose_name='Postal Code')
    propertyStreetNumber = models.PositiveIntegerField(verbose_name='Street Number')
    
    propertyConstructionDate = models.DateField(default=date.today, verbose_name='Construction Date')
    propertyPostedDate = models.DateTimeField(auto_now=True, verbose_name='Date Posted')
    
    propertyNoOfHalls = models.PositiveIntegerField(verbose_name='Halls')
    propertyNoOfRooms = models.PositiveIntegerField(verbose_name='Rooms')
    propertyNoOfBathrooms = models.PositiveIntegerField(verbose_name='Bathrooms')
    propertyNoOfFloors = models.PositiveIntegerField(verbose_name='Floors')
    propertyTotalArea = models.PositiveIntegerField(verbose_name='Total Area')
    
    propertySellingPrice = models.PositiveIntegerField(verbose_name='Price')
    propertySellingType = models.CharField(max_length=5, default=DealingChoice.Buy, choices=[(tag.name,tag.value) for tag in DealingChoice], verbose_name='Type')
    
    def __str__(self):
        return self.propertyName

    def get_user(self):
        return self.user

## Property Images
class PropertyImages(models.Model):
    propertyImageID = models.AutoField(unique=True, primary_key=True)
    propertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
    propertyImage = models.ImageField(verbose_name='Image', null=True, blank=True, upload_to='property/', default='/home/tarang/Workspace/S2G4RealEstate/eproperty/static/images/no-image.png')
    
    def __str__(self):
        return str(self.propertyImageID)