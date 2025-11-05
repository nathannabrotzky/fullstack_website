from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    quote = models.TextField()
    role = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="testimonials/", blank=True)
    featured = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} — {self.role}"