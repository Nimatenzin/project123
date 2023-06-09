from django.contrib import admin
from .models import User, UserProfile, Schedule, TimeSlot, Payment, PaymentApproval, Image, Contact
from django.contrib.auth.admin import UserAdmin, Group

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'phone_number', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    icon = 'fas fa-user'
    search_fields = ('email', 'phone_number')

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)

class TimeSlotInline(admin.TabularInline):
    model = TimeSlot

class ScheduleAdmin(admin.ModelAdmin):
    inlines = [TimeSlotInline]
    list_display = ['date']

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'total_adults_slots', 'total_child_slots', 'available_adults_slots', 'available_child_slots', 'booked_adults_slots', 'booked_child_slots',]

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)

class PaymentApprovalInline(admin.TabularInline):
    model = PaymentApproval
    
from django.contrib import admin
from .models import Payment, PaymentApproval

class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'account_number', 'email', 'phone_number',
        'screenshot', 'created_at', 'num_adults', 'num_children', 'total_amount'
    )
    search_fields = ('email', 'phone_number')

admin.site.register(Payment, PaymentAdmin)


class PaymentApprovalAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'payment_account_number', 'payment_email', 'payment_phone_number',
        'payment_screenshot', 'payment_created_at', 'get_num_adults',
        'get_num_children', 'get_total_amount', 'approval_status',
    )

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

    def get_num_adults(self, obj):
        return obj.payment.num_adults

    def get_num_children(self, obj):
        return obj.payment.num_children

    def get_total_amount(self, obj):
        return obj.payment.total_amount

    def approval_status(self, obj):
        return 'Approved' if obj.approved else 'Cancelled' if obj.cancelled else 'Pending'

admin.site.register(PaymentApproval, PaymentApprovalAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image',)

admin.site.register(Image, ImageAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'occupation', 'created_at')

admin.site.register(Contact, ContactAdmin)

# Remove the add button from all classes except Schedule
for model, model_admin in admin.site._registry.items():
    if model not in [Schedule, Image]:
        model_admin.has_add_permission = lambda request: False

admin.site.site_header = "AquaBlue"
admin.site.site_title = "AquaBlue"
