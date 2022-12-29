from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


##more plugins
import gzip
import pandas
import copy
from datetime import datetime

# Create your views here.

from .forms.portfolioForm import portfolioForm
from .forms.sampleform import normalform,normalModelForm
from .models import portfolioModel
from .data_processing.stockvalue import *
from .data_processing.stockCharts import *
from .data_processing.dates import  chartTimeOptions, get_relative_date

@login_required
def portfolioView(request, *args, **kwargs):
    print(request.POST.dict())
    nvl_date = lambda dt: dt if dt else date.min
    
    print( chartTimeOptions)
    timeOption="Forever"
    context={}
    
    if not request.POST.get('timeOption') is None:
        timeOption=request.POST.get('timeOption')
    
    print(f"timeoption is {timeOption}")
    timeOptionDateFilter = get_relative_date(timeOption)
    print(f"timeoptiondate is {timeOptionDateFilter}")

    myportfolio= portfolioModel.objects.all().values()
    
    if args:
        print(f'Positional arguments: {args}')
    if kwargs:
        print(f'Keyword arguments: {kwargs}')
    
    
    if 'tickerName' in kwargs:
        tickerName = kwargs.get('tickerName')
        myportfolio = myportfolio.filter(ticker__iexact=tickerName).values()
        tickerData = stockChart(tickerName,chartTimeOptions,timeOptionDateFilter)
        context['tickerData']=tickerData.get('tickerData')
        context['min_price'] = tickerData.get('min_price')
        context['max_price'] = tickerData.get('max_price')
        context['var_price'] = round((tickerData.get('max_price')- tickerData.get('min_price'))*100/ tickerData.get('min_price'),2)
        context['tickerName'] = tickerName

    context["chartTimeOptions"] = chartTimeOptions
    

    if myportfolio.exists():
        portfolioValue = getHistoricalStockValue(pandas.DataFrame(myportfolio))


        if not timeOptionDateFilter is None:
            myportfolio= portfolioModel.objects.filter(datePurchased__gt=timeOptionDateFilter).values()
            portfolioValue = portfolioValue[portfolioValue['date']>=datetime(timeOptionDateFilter.year, timeOptionDateFilter.month, timeOptionDateFilter.day)]
            first_stock_date = nvl_date(portfolioModel.objects.filter(datePurchased__gt=timeOptionDateFilter).exclude(quantity=0).values_list('datePurchased', flat=True).first())
            print(first_stock_date)
            first_stock_date = datetime.combine(first_stock_date , datetime.min.time())
            min_date = max(portfolioValue['date'].min(),first_stock_date)
            print(min_date)
            max_date = portfolioValue['date'].max()
            min_value = portfolioValue.loc[portfolioValue['date']>=min_date,'cumValue'].values[0]
            min_cost = portfolioValue.loc[portfolioValue['date']>=min_date,'cumCost'].values[0]            
            max_value = portfolioValue.loc[portfolioValue['date']==max_date,'cumValue'].values[0]
            max_cost = portfolioValue.loc[portfolioValue['date']==max_date,'cumCost'].values[0]
            
            portfolioValue= portfolioValue.to_dict('records')    
        else:
            portfolioValue = portfolioValue[portfolioValue['date'].notnull()]
            first_stock_date =  nvl_date(myportfolio.exclude(quantity=0).values_list('datePurchased', flat=True).first())
            print(first_stock_date)
            first_stock_date = datetime.combine(first_stock_date, datetime.min.time())
            min_date = max(portfolioValue['date'].min(),first_stock_date)
            print(min_date)
            max_date = portfolioValue['date'].max()
            min_value = portfolioValue.loc[portfolioValue['date']>=min_date,'cumValue'].values[0]
            min_cost = portfolioValue.loc[portfolioValue['date']>=min_date,'cumCost'].values[0]            
            max_value = portfolioValue.loc[portfolioValue['date']==max_date,'cumValue'].values[0]
            max_cost = portfolioValue.loc[portfolioValue['date']==max_date,'cumCost'].values[0]
            portfolioValue= portfolioValue.to_dict('records')

        stockHistoryChartData= [
            {
            'Date' : row['datePurchased'],
            'Stock' : row['ticker'],
            'Quantity' : row['quantity'],
            'Cost' : row['costBasis'],
            }
            for row in myportfolio
        ]
        
        
        
        stockPerformanceChartData= [
            {
            'Date' : row['date'].date(),
            'Quantity' : row['cumQuantity'],
            'Cost' : row['cumCost'],
            'Value' : row['cumValue'],
            }
            for row in portfolioValue
        ]

        
        

        context["portfolioData"]=myportfolio
        context["stockHistoryChartData"] = stockHistoryChartData
        context['stockPerformanceChartData'] = stockPerformanceChartData
        context['nulldata']=0
    else:
        context['nulldata']=1
    
    context['timeOption'] = timeOption
    context['min_value'] = min_value
    context['max_value'] = max_value
    context['var_value'] = round((max_value-min_value)*100/min_value,2)
    context['min_cost'] = min_cost
    context['max_cost'] = max_cost
    context['var_cost'] = round((max_cost-min_cost)*100/min_cost,2)



    return render(request, "portfolioView.html", context)


    if request.POST.get('newstock') =='yes' :
        form = portfolioForm()
        context['form']=form        
        return render(request, "portfolioAdd.html",context)
    
    else:
        print("nothing to print")

def portfolioAdd(request):
    context = {}
    form = portfolioForm(request.POST or None)
    context['form'] = form
    if request.method=='POST':
        if stockform.is_valid():
            print(stockform.cleaned_data)
            stockform.save()
            return redirect('portfolio/')
        else:
            print("error with formdata")
            print(stockform.data)
            print(stockform.cleaned_data)
    return render(request, "portfolioAdd.html",context)