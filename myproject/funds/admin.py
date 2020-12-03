from django.contrib import admin

# Register your models here.

from .models import Fund

class FundAdmin(admin.ModelAdmin):
    list_display = ('fund_name','fund_ISIN','pub_date')

admin.site.register(Fund, FundAdmin)
