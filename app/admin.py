from django.contrib import admin
from .models import User, UserProfile, Schedule, TimeSlot, Payment, PaymentApproval, Image, Contact
from django.contrib.auth.admin import UserAdmin, Group
from django.contrib import messages
from django.core.exceptions import ValidationError


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
    list_display = ['start_time', 'end_time', 'total_adults_slots', 'total_child_slots', 'available_adults_slots', 'available_child_slots', 'booked_adults_slots', 'booked_child_slots']

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)

class PaymentApprovalInline(admin.TabularInline):
    model = PaymentApproval

class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id','account_number', 'email', 'phone_number',
        'screenshot', 'display_created_date', 'num_adults', 'num_children', 'total_amount'
    )
    inlines = [PaymentApprovalInline]
    search_fields = ('email', 'phone_number')
    
    
    def display_created_date(self, obj):
        return obj.created_at.date()

    display_created_date.short_description = 'Created Date'

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return super().get_fieldsets(request, obj)
        else:
            # Remove the "General" tab for existing objects
            return []
        
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['role'] = ''
        return initial

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_delete'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

admin.site.register(Payment, PaymentAdmin)

class PaymentApprovalAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'payment_account_number', 'payment_email', 'payment_phone_number',
        'payment_screenshot', 'display_created_date', 'get_num_adults',
        'get_num_children', 'get_total_amount', 'approval_status',
    )

    def save_model(self, request, obj, form, change):
        if obj.approved and obj.cancelled:
            # If both checkboxes are selected, raise a validation error
            raise ValidationError("Cannot select both 'Approved' and 'Cancelled'")

        super().save_model(request, obj, form, change)

        if '_continue' not in request.POST and '_addanother' not in request.POST:
            # Customize the success message
            messages.success(request, 'Message saved successfully')

    def payment_account_number(self, obj):
        return obj.payment.account_number

    def payment_email(self, obj):
        return obj.payment.email

    def payment_phone_number(self, obj):
        return obj.payment.phone_number

    def payment_screenshot(self, obj):
        return obj.payment.screenshot

    def display_created_date(self, obj):
        return obj.payment.created_at.date()

    display_created_date.short_description = 'Payment Created Date'

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

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['has_change_permission'] = False
        extra_context['show_history'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

admin.site.register(Contact, ContactAdmin)

# Remove the add button from all classes except Schedule
for model, model_admin in admin.site._registry.items():
    if model not in [Schedule, Image]:
        model_admin.has_add_permission = lambda request: False

admin.site.site_header = "AquaBlue"
admin.site.site_title = "AquaBlue"
