import requests
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockForm
from .models import Stock


def home(request):
    if request.method == "POST":
        api_request = requests.get(
            'https://cloud.iexapis.com/stable/stock/' + request.POST['ticker'] + 
            '/batch?types=quote&token=pk_150fca9899514fca939170a4dd09c20b')

        try:
            api = json.loads(api_request.content)
        except Exception:
            api = 'Error...'

        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'ticker': 'Enter Stock Ticker Right Above...'})


def about(request):
   return render(request, 'about.html', {})


def add_delete_stock(request):
    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added!!"))
            return redirect('add_delete_stock')

    else:
        tickers = Stock.objects.all() 
        symbols = ','.join([str(ticker) for ticker in tickers])
        req = json.loads(requests.get('https://cloud.iexapis.com/stable/stock/market/batch?'
            f'symbols={symbols}&types=quote&token=pk_150fca9899514fca939170a4dd09c20b').content)
        apis = [quote for quote in req.values()]
        
        return render(request, 'add_delete_stock.html', {'output': zip(tickers, apis)})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)  # pk = primay key
    item.delete()
    messages.success(request, ("Stock Has Been Deleted!!"))
    return redirect('add_delete_stock')
