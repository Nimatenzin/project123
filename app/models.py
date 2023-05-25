from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import OneToOneField
class UserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, phone_number, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            phone_number=phone_number,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
    
class User(AbstractBaseUser):
    UNKNOWN = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (UNKNOWN, 'Unknown'),
        (CUSTOMER, 'Customer'),
    )

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'Unknown'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role

  
class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


from django.db import models

class TimeSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_adults_slots = models.PositiveIntegerField()
    total_child_slots = models.PositiveIntegerField()
    available_adults_slots = models.PositiveIntegerField()
    available_child_slots = models.PositiveIntegerField()
    booked_adults_slots = models.PositiveIntegerField()
    booked_child_slots = models.PositiveIntegerField()
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)

class Schedule(models.Model):
    date = models.DateField()

    def get_available_time_slots(self):
        return self.timeslot_set.filter(available_adults_slots__gt=0, available_child_slots__gt=0)

    def book_time_slot(self, time_slot, num_adults, num_children):
        if num_adults <= time_slot.available_adults_slots and num_children <= time_slot.available_child_slots:
            time_slot.available_adults_slots -= num_adults
            time_slot.available_child_slots -= num_children
            time_slot.booked_adults_slots += num_adults
            time_slot.booked_child_slots += num_children
            time_slot.save()
            return True
        else:
            return False
            
from django.db import models

class Payment(models.Model):
        account_number = models.PositiveIntegerField()
        total_amount = models.DecimalField(max_digits=10, decimal_places=2)
        journal_number = models.PositiveIntegerField()
        email = models.EmailField()
        phone_number = models.CharField(max_length=20)
        screenshot = models.ImageField(upload_to='screenshots/')
        created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.conf import settings
from .models import Payment
from django.utils import timezone

class PaymentApproval(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    approved_at = models.DateTimeField(null=True)
    cancelled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='canceller')
    cancelled_at = models.DateTimeField(null=True)

    def approve(self, user):
        self.approved = True
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save()

    def cancel(self, user):
        self.cancelled = True
        self.cancelled_by = user
        self.cancelled_at = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.payment.id} - Approval Status: {"Approved" if self.approved else "Cancelled" if self.cancelled else "Pending"}'

from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='images/', unique=True)

    def __str__(self):
        return self.image.name

from django.db import models
from django.utils import timezone

class Contact(models.Model):
    name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    




 