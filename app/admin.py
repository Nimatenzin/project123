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
# admin.site.register(UserProfile)
from django.contrib import admin
from .models import Schedule, TimeSlot

class TimeSlotInline(admin.TabularInline):
    model = TimeSlot

class ScheduleAdmin(admin.ModelAdmin):
    inlines = [TimeSlotInline]
    list_display = ['date']

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'total_adults_slots', 'total_child_slots', 'available_adults_slots', 'available_child_slots', 'booked_adults_slots', 'booked_child_slots', 'schedule']

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)


# admin.py
from django.contrib import admin
from .models import Payment, PaymentApproval

class PaymentApprovalInline(admin.TabularInline):
    model = PaymentApproval

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_number', 'email', 'phone_number', 'screenshot', 'created_at')
    inlines = [PaymentApprovalInline]

admin.site.register(Payment, PaymentAdmin)

class PaymentApprovalAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_account_number', 'payment_email', 'payment_phone_number', 'payment_screenshot', 'payment_created_at', 'approval_status',)

    def payment_account_number(self, obj):
        return obj.payment.account_number

    def payment_email(self, obj):
        return obj.payment.email

    def payment_phone_number(self, obj):
        return obj.payment.phone_number

    def payment_screenshot(self, obj):
        return obj.payment.screenshot

    def payment_created_at(self, obj):
        return obj.payment.created_at

    def approval_status(self, obj):
        return 'Approved' if obj.approved else 'Cancelled' if obj.cancelled else 'Pending'

admin.site.register(PaymentApproval, PaymentApprovalAdmin)



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






