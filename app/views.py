from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import TimeSlot


# Restrict the unknown from accessing the customer page
def check_role_unknown(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the unkown page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied



def about(request):
    return render(request, 'about.html')

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # form.save()

            #create the user using create_user method
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, phone_number=phone_number, password=password)
            user.role = User.CUSTOMER
            user.save()
            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Account registered successfully.Please check your email to activate your account!')
            return redirect('/registerUser/')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'registerUser.html', context)

def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
        
   

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_unknown)
def unknownDashboard(request):
    return render(request, 'unknownDashboard.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')
    


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request, 'Password did not match!')
            return redirect('reset_password')
    return render(request, 'reset_password.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def check_availability(request):
    return render(request, 'check_availability.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Schedule
from django.shortcuts import redirect

@login_required(login_url='login/')
def show_available_time_slots(request):
    if request.method == 'POST':
        date = request.POST['date']
        schedule = Schedule.objects.filter(date=date).first()
        if schedule:
            time_slots = schedule.get_available_time_slots()
            return render(request, 'availability.html', {'time_slots': time_slots})
        else:
            messages.error(request, 'No schedule found for the selected date.')
            return redirect('/#book-a-table')
    else:
        return redirect('login')
    
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PaymentForm
from .models import Payment, TimeSlot

@login_required
def payment(request, time_slot_id):
    print("Reached payment view")  # Add this line to check if the view is accessed

    time_slot = TimeSlot.objects.get(pk=time_slot_id)

    if request.method == 'POST':
        print("Inside POST condition")  # Add this line to check if the request is a POST request

        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")  # Add this line to check if the form is valid

            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()

            # Update the time slot availability
            if (
                payment.num_adults <= time_slot.available_adults_slots and
                payment.num_children <= time_slot.available_child_slots
            ):
                time_slot.available_adults_slots -= payment.num_adults
                time_slot.available_child_slots -= payment.num_children
                time_slot.booked_adults_slots += payment.num_adults
                time_slot.booked_child_slots += payment.num_children
                time_slot.save()

            messages.success(request, 'Payment successful!')
            return redirect('index')

    else:
        print("Inside GET condition")  # Add this line to check if the request is a GET request

        form = PaymentForm()

    return render(request, 'payment.html', {'form': form, 'time_slot_id': time_slot_id, 'time_slot': time_slot})


from django.shortcuts import render

def payment_success(request):
    return render(request, 'payment_success.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Payment, PaymentApproval
from .models import User

@login_required
def payment_approval(request):
    user = request.user
    payments = Payment.objects.filter(user=user)
    approvals = PaymentApproval.objects.filter(payment__in=payments)

    context = {
        'payments': payments,
        'approvals': approvals,
    }

    return render(request, 'payment_approval.html', context)



@login_required
def approve_payment(request, email):
    user = get_object_or_404(User, email=email)

    if request.user.is_staff:
        try:
            payment = get_object_or_404(Payment, user=user)
            approval = get_object_or_404(PaymentApproval, payment=payment)
            if not approval.approved and not approval.cancelled:  # Check if already approved or cancelled
                approval.approve(request.user)
                messages.success(request, f'Payment for {email} has been approved.')
            else:
                messages.warning(request, f'Payment for {email} has already been approved or cancelled.')
        except Payment.DoesNotExist:
            messages.error(request, f'No payment found for {email}.')
        except PaymentApproval.DoesNotExist:
            messages.error(request, f'Payment for {email} has not been submitted for approval.')
    else:
        messages.error(request, 'You do not have permission to approve payments.')

    return redirect('payment-approval')


@login_required
def cancel_payment(request, email):
    user = get_object_or_404(User, email=email)

    if request.user.is_staff:
        try:
            payment = get_object_or_404(Payment, user=user)
            approval = get_object_or_404(PaymentApproval, payment=payment)
            if not approval.approved and not approval.cancelled:  # Check if already approved or cancelled
                approval.cancel(request.user)
                messages.success(request, f'Payment for {email} has been cancelled.')
            else:
                messages.warning(request, f'Payment for {email} has already been approved or cancelled.')
        except Payment.DoesNotExist:
            messages.error(request, f'No payment found for {email}.')
        except PaymentApproval.DoesNotExist:
            messages.error(request, f'Payment for {email} has not been submitted for approval.')
    else:
        messages.error(request, 'You do not have permission to cancel payments.')

    return redirect('payment-approval')


from django.shortcuts import render
from .models import Image

def index(request):
    images = Image.objects.all()
    context = {'images': images}
    return render(request, 'index.html', context)


from django.shortcuts import render, redirect
from app.models import Contact

from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        occupation = request.POST.get('occupation')
        message = request.POST.get('message')
        contact = Contact(name=name, occupation=occupation, message=message)
        contact.save()
        messages.success(request, 'Your message has been sent!')
        return redirect('contact')
    return render(request, 'contact.html')


def cust_availability(request):
    user = request.user
    payments = Payment.objects.filter(user=user)
    approvals = PaymentApproval.objects.filter(payment__in=payments)

    context = {
        'payments': payments,
        'approvals': approvals,
    }


    return render(request, 'cust_availability.html', context)








