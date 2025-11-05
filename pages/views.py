from django.shortcuts import render
from shop.models import Product
from .models import Testimonial

def home(request):
    testimonials = Testimonial.objects.filter(featured=True)
    featured_products = Product.objects.filter(featured=True)
    return render(request, "pages/home.html", {
        "featured_products": featured_products,
        "testimonials": testimonials,
    })

def contact(request):
    return render(request, 'pages/contact.html')

def terms(request):
    return render(request, 'pages/terms.html')

def privacy(request):
    return render(request, 'pages/privacy.html')

def shipping(request):
    return render(request, 'pages/shipping.html')

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

def contact_send(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject", "New Contact Form Submission")
        message = request.POST.get("message")

        full_message = f"From: {name} <{email}>\n\n{message}"

        send_mail(
            subject,
            full_message,
            email,  # from email
            ["myuntoldstory.contact@gmail.com"],  # to email
            fail_silently=False,
        )

        messages.success(request, "Thanks for reaching out! We'll be in touch soon.")
        return redirect("contact")

    return render(request, "contact.html")

def about(request):
    team = [
        {
            "name": "Nathan",
            "role": "Co-Founder & COO",
            "bio": "Nathan blends immersive storytelling with modern web architecture to build unforgettable digital experiences.",
            "image": "img/nathan.jpg"
        },
        {
            "name": "Daniel",
            "role": "Co-Founder & CMO",
            "bio": "Daniel forges new stories and opportunities for letting customers discover storytelling.",
            "image": "img/daniel.png"
        },
        {
            "name": "Kristy",
            "role": "Co-Founder & CPO",
            "bio": "Kristy works to bring every story to life with meaningful product solutions and development opportunities.",
            "image": "img/kristy.jpeg"
        },
    ]
    return render(request, "pages/about.html", {"team": team})




