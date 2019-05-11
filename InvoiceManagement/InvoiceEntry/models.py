from django.db import models

# Create your models here.
class ClientName(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name
status=(
    ('to_be_sent','To Be Sent'),
    ('sent','Sent'),
    ('recieved_approval','Recieved Approval'),
    ('recieved_payment','Recieved Payment')
)
class Invoice(models.Model):
    ClientName =models.ForeignKey('ClientName',on_delete=models.CASCADE)
    ProjectName = models.CharField(max_length=20)
    InvoiceAmount=models.IntegerField()
    GSTAmount=models.IntegerField()
    TotalAmount=models.IntegerField()
    InvoiceSubmission=models.DateField()
    InvoiceDueDate=models.DateField()
    InvoiceStatus=models.CharField(choices=status,max_length=20)
