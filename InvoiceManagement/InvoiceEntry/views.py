from django.shortcuts import render
from .form import InvoiceForm
from .models import Invoice
from graphos.renderers.gchart import LineChart
from graphos.sources.simple import SimpleDataSource
# Create your views here.

def create(request):
    if request.method == 'POST':
        form=InvoiceForm(request.POST)
        if form.is_valid():
            f= form.save(commit=False)
            f.GSTAmount=f.InvoiceAmount*18/100
            f.TotalAmount=f.GSTAmount+f.InvoiceAmount
            f.save()
            return render(request, 'invoice.html', {'f': f})

    else:
        form=InvoiceForm()
    return render(request,'create.html',{'form':form})
def analyse(request):

    queryset = Invoice.objects.all()
    dataInvoice=[['Invoice Number','Invoice Sum']]
    dataGST=[['Invoice Number','GST Sum']]
    dataTotalAmount=[['Invoice Number','Total Amount Sum']]
    sumInvoiceAmount=0
    sumGST=0
    sumtotalAmount=0

    k=1
    for i in queryset:
        sumInvoiceAmount=i.InvoiceAmount+sumInvoiceAmount
        sumGST=i.GSTAmount+sumGST
        sumtotalAmount=i.TotalAmount+sumtotalAmount
        dataInvoice.insert(k,[k,sumInvoiceAmount])
        dataGST.insert(k,[k,sumGST])
        dataTotalAmount.insert(k,[k,sumtotalAmount])
        k=k+1

    line_chart_invoice=LineChart(SimpleDataSource(data=dataInvoice))
    line_chart_GST=LineChart(SimpleDataSource(data=dataGST))
    line_chart_Total_Amount=LineChart(SimpleDataSource(data=dataTotalAmount))
    return render(request, 'analyse.html', {'InvoiceChart': line_chart_invoice,'GSTChart':line_chart_GST,'TotalAmount':line_chart_Total_Amount})

