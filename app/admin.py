from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'phone_number','role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User,  CustomUserAdmin)
admin.site.register(UserProfile)

from django.contrib import admin
from .models import Schedule, TimeSlot

class TimeSlotInline(admin.TabularInline):
    model = TimeSlot

class ScheduleAdmin(admin.ModelAdmin):
    inlines = [TimeSlotInline]

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(TimeSlot)

# admin.py

from django.contrib import admin
from .models import Payment, PaymentApproval

class PaymentApprovalInline(admin.TabularInline):
    model = PaymentApproval

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_number', 'total_amount', 'journal_number', 'email', 'phone_number', 'screenshot', 'created_at')
    inlines = [PaymentApprovalInline]

    def journal_number(self, obj):
        return obj.journal_number

admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentApproval)

from django.contrib import admin
from .models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image',)
    
admin.site.register(Image, ImageAdmin)


from django.contrib import admin
from app.models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'occupation', 'created_at')

admin.site.register(Contact, ContactAdmin)






