from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, ContactForm
from .models import SignUp
# Create your views here.

def home(request):
    title = 'Sign Up Now'
    #if request.user.is_authenticated():
    #    title = "Logged in as  %s" %(request.user)

    #add a form
    #if request.method == "POST":
    #    print request.POST
    form = SignUpForm(request.POST or None)

    context = {
        "title": title,
        "form": form,
    }

    if form.is_valid():
        instance = form.save(commit=False)


       # full_name = form.cleaned_data.get("full_name")
       # if not full_name:
       #     full_name = "Anonymous"
       # instance.full_name = full_name        #This one and the below is same

        if not instance.full_name:
            instance.full_name = "Anonymous"
        instance.save()
        context = {
            "title": "Thank you",
         }
        
        
        
    if request.user.is_authenticated() and request.user.is_staff:
        #print(SignUp.objects.all())
   
        queryset = SignUp.objects.all().order_by('-timestamp')
        context = {
            "queryset" : queryset
                
        }
        

    return render(request, "home.html", context)


def contact(request):
    title = 'Contact Us'
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        #for key, value in form.cleaned_data.iteritems():
        #    print key, value     #use this if you have many fields
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
       # print email, message, full_name
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
       
        to_email = [from_email, 'support@chrysaour.com']
        contact_message = "%s: %s via %s"%(
            form_full_name,
            form_message,
            form_email)
        some_html_message = """
        <h1>Hello</h1>
        """

        send_mail(subject,
                  contact_message,
                  from_email,
                  to_email,
                  fail_silently=False)


    context = {
        "form": form,
        "title": title,
        "title_align_center" : title_align_center,
    }

    return render(request, "forms.html", context)