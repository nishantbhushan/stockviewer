from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse


##more plugins
import gzip
import pandas
from datetime import datetime

# Create your views here.

from .forms.portfolioForm import portfolioForm
from .forms.sampleform import normalform,normalModelForm
from .models import portfolioModel
from .data_processing.stockvalue import *
from .data_processing.dates import  chartTimeOptions, get_relative_date

def normalview(request):
    if request.method=='GET':
        context={}
        form = normalModelForm()
        print(form)
        context['form'] = form
        return render(request, "normalform.html", context)
    elif request.method=='POST':
        formdata = normalModelForm(request.POST)
        print(type(formdata.data.get('dateInput')))
        print(formdata.is_valid())
        print(formdata.cleaned_data)
        # print(request.POST)
        return HttpResponse('<h1>Hello HttpResponse</h1>')

def portfolioView(request, *args, **kwargs):
    
    print( chartTimeOptions)
    timeOption="Forever"
    context={}
    if request.method == 'GET':
        if not request.GET.get('timeOption') is None:
            timeOption=request.GET.get('timeOption')
        
        print(f"timeoption is {timeOption}")
        timeOptionDateFilter = get_relative_date(timeOption)
        print(f"timeoptiondate is {timeOptionDateFilter}")

        
        
        if 'tickerName' in kwargs:
            tickerName = kwargs.get('tickerName')
            myportfolio = myportfolio.filter(ticker__iexact=tickerName).filter(datePurchased__gt=timeOptionDateFilter).values()
        else:            
            myportfolio = portfolioModel.objects.all().values()
        
        if args:
            print(f'Positional arguments: {args}')
        if kwargs:
            print(f'Keyword arguments: {kwargs}')
        
        context["chartTimeOptions"] = chartTimeOptions
        

        if myportfolio.exists():
            portfolioValue = getHistoricalStockValue(pandas.DataFrame(myportfolio))
            if not timeOptionDateFilter is None:
                myportfolio= portfolioModel.objects.filter(datePurchased__gt=timeOptionDateFilter).values()
                portfolioValue = portfolioValue[portfolioValue['date']>=datetime(timeOptionDateFilter.year, timeOptionDateFilter.month, timeOptionDateFilter.day)].to_dict('records')    
            else:
                portfolioValue = portfolioValue[portfolioValue['date'].notnull()].to_dict('records')  
            context["portfolioData"]=myportfolio
            context["chartdata"] = portfolioValue            
            context['nulldata']=0
        else:
            context['nulldata']=1
        # print(portfolioValue.columns)
        # print(ticker)
        # compressed_portfolioValue = gzip.compress(pandas.DataFrame.to_pickle(portfolioValue))
        
        # context["datawithValue"] =portfolioValue
        
        # print(context["chartdata"])
        # context["chart_html"] = stockChart(portfolioValue.loc[portfolioValue["date"].notnull()])
        # print(context)
        return render(request, "portfolioView.html", context)
    elif request.POST.get('newstock') =='yes' :
        form = portfolioForm()
        context['form']=form        
        return render(request, "portfolioAdd.html",context)
    elif request.method == 'POST':
        stockform=portfolioForm(request.POST)
        stockform.save()
        if stockform.is_valid():
            print(stockform.cleaned_data)
            stockform.save()
        else:
            print("error with formdata")
            print(stockform.data)
            print(stockform.cleaned_data)
        return HttpResponse('<h1>Hello HttpResponse</h1>')    
    else:
        print("nothing to print")

def portfolioAdd(request):
    
    print(request.POST)

    # stockEntry.save()
    return HttpResponseRedirect('portfolioView')