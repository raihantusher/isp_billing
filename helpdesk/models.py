from django.db import models

# Create your models here.


class Ticket(models.Model):
    STATUS = (
        ('Unassigned', 'Unasigned'),
        ('Assigned', 'Assigned'),
        ('Completed', 'Completed'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default="Unassigned")
    datetime = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment = models.TextField()
    ticket  = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    #by = models
