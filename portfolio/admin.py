from django.contrib import admin

# Register your models here.
from .models import portfolioModel

class portfolioAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticker']
    search_fields = ['ticker','datePurchased']


admin.site.register(portfolioModel,portfolioAdmin)
