from django.contrib import admin
from .models import PropertyDirection, PropertyCategory, PropertySector, Country, Province, City, Property, PropertyImages

# Property Registrations
admin.site.register(PropertyDirection)
admin.site.register(PropertyCategory)
admin.site.register(PropertySector)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Property)
admin.site.register(PropertyImages)