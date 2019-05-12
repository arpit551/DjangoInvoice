from django.shortcuts import render
from .form import InvoiceForm,ClientForm
from .models import Invoice
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import BarChart
from django.contrib import messages

def create(request):
    if request.method == 'POST':
        formclient = ClientForm(request.POST)
        form=InvoiceForm(request.POST)
        if formclient.is_valid():
            formclient.save()
            messages.success(request, 'Client added Successful')

        if form.is_valid():
            f= form.save(commit=False)
            f.GSTAmount=f.InvoiceAmount*18/100
            f.TotalAmount=f.GSTAmount+f.InvoiceAmount
            f.save()
            return render(request, 'invoice.html', {'f': f})

    else:

        form=InvoiceForm()
    formclient = ClientForm()
    return render(request,'create.html',{'form':form,'formclient':formclient})
def analyse(request):
    StartDate=None
    EndDate=None
    if request.method=='POST':
        StartDate=request.POST['start']
        EndDate=request.POST['end']

        if EndDate is None or StartDate is None:
            queryset=Invoice.objects.all()
        else:
            queryset = Invoice.objects.filter(InvoiceSubmission__range=[StartDate, EndDate])
    else:
        queryset=Invoice.objects.all()
    querysetquarter=Invoice.objects.all()
    sumInvoiceAmount=0
    sumGST=0
    sumTotalAmount=0
    q1=0
    q2=0
    q3=0
    q4=0
    for i in queryset:
        sumInvoiceAmount=i.InvoiceAmount+sumInvoiceAmount
        sumGST=i.GSTAmount+sumGST
        sumTotalAmount=i.TotalAmount+sumTotalAmount
    for i in querysetquarter:
        if 1 <= i.InvoiceSubmission.month <= 3:
            q1 = q1 + i.InvoiceAmount
        if 4 <= i.InvoiceSubmission.month <= 6:
            q2 = q2 + i.InvoiceAmount
        if 7 <= i.InvoiceSubmission.month <= 9:
            q3 = q3 + i.InvoiceAmount
        if 10 <= i.InvoiceSubmission.month <= 12:
            q4 = q4 + i.InvoiceAmount



    bardata = [['Sum Amounts','RS'],['Invoice Sum',sumInvoiceAmount], ['GST Sum',sumGST],['Total Sum',sumTotalAmount]]
    quarterdata=[['Quarter','Invoice Amount'],['Quarter 1',q1],['Quarter 2',q2],['Quarter 3',q3],['Quarter 4',q4]]
    bar_chart=BarChart(SimpleDataSource(data=bardata),options={'title': 'Comparison between Invoice, GST and Total Amount'})
    bar_chart_quarter=BarChart(SimpleDataSource(data=quarterdata),options={'title': 'Quarter wise Invoice Amount'})
    return render(request, 'analyse.html', {'bar_chart':bar_chart,'quarter':bar_chart_quarter,'e':EndDate,'s':StartDate})
