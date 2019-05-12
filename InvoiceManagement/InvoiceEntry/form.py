from django import forms
from django.forms import ModelForm
from .models import Invoice,ClientName


class InvoiceForm(ModelForm):
    # ClientName = forms.ModelChoiceField(
    #     queryset=ClientName.objects.all(),to_field_name='name')

    class Meta:
        model=Invoice
        fields=['ClientName','ProjectName','InvoiceAmount','InvoiceSubmission','InvoiceDueDate','InvoiceStatus']
        widgets = {
            'InvoiceSubmission': forms.DateInput(format=('%d/%m/%Y'),
                                             attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                    'type': 'date'}),
            'InvoiceDueDate': forms.DateInput(format=(' % d / % m / % Y'),
                attrs = {'class': 'form-control', 'placeholder': 'Select a date',
                         'type': 'date'}),
        }
        labels = {
            "ClientName": "Client Name",
            'ProjectName':'Project Name',
            'InvoiceAmount':'Invoice Amount',
            'InvoiceSubmission':'Invoice Submission',
            'InvoiceDueDate':'Invoice Due Date',
            'InvoiceStatus': 'Invoice Status'

        }

class ClientForm(ModelForm):
    class Meta:
        model=ClientName
        fields=['name']