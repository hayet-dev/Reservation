from django.db import models

class Appointment(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.IntegerField()
    request = models.TextField()
    sent_date = models.DateField(auto_now_add=True)
    accepted= models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now_add=True,null=True,blank=True)



    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ['-sent_date']
    
# Create your models here.
