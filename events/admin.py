from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Event, Sponsor, Sponsorship, Category, Contact


class EventsAdmin(admin.ModelAdmin):
    list_display = ('id','title','time_create','photo','is_published')
    list_display_links = ('id','title')
    search_fields = ('title','description')
    list_editable=('is_published',)
    list_filter = ('is_published', 'time_create')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    search_fields = ('name',)


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('id','user','company_name','contact_name','email')
    list_display_links = ('id','company_name')
    search_fields = ('company_name',)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')

admin.site.register(Event, EventsAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Sponsorship)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact, ContactAdmin)