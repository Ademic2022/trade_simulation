from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import uuid, json, pymongo
from .conn import db
from .trader import Trader
from .graph import generate_profit_loss_graph


def user_colection(trader_name, db):
    """Select the collection"""
    collection = db[trader_name]

    """Query to get the last document based on timestamp in descending order"""
    last_document = collection.find_one(sort=[("timestamp", -1)])
    profit = round(last_document['balance'] - 100, 2)

    """Access the fields in the last document"""
    if last_document:
        user_datas = {
            "balance": round(last_document['balance'],2),
            "total_trades": last_document['total_trades'],
            "timestamp": last_document['timestamp'],
            "trader_name": trader_name,
            "trades": last_document['total_trades'],
            "profit": profit
        }
        return user_datas
    else:
        return None


def simulate_trading(request, trader_name):

    if request.method == 'POST':
        action = request.POST.get('action')
        user_trader_name = trader_name

        trader = Trader(user_trader_name)
        if action == 'start':
            if user_trader_name in db.list_collection_names():
                """Check the user's simulation state in the database"""
                simulation_state = trader.get_simulation_state(db)

                if simulation_state == 'running':
                    messages.success(request, 'Trading in Progress')

                """Update the simulation state to 'running' in the database"""
                trader.set_simulation_state('running', db)

                simulation_duration_minutes = 10
                trader.simulate(db, simulation_duration_minutes)
                messages.success(request, 'Trading in progress...')
                return HttpResponseRedirect(reverse('simulate_trading', args=[trader_name]))
            else:
                messages.success(request, 'User not found')

        elif action == 'stop':
            """Set the simulation state to 'stopped' in the database"""
            trader.set_simulation_state('stopped', db)
            messages.success(request, 'Trade activities stopped, enter your account name to see trade activities ')
            return redirect('dashboard')
    """get user collection from database"""
    user_data = user_colection(trader_name, db)
    return render(request, 'simulate_trading.html', 
                  {"trader_name": trader_name, "user_data": user_data})


def index(request):

    return render(request, 'index.html')

def lucky_trader(request):
    if request.method == 'POST':
        form_data = request.POST
        username = form_data['username']

        """Check if the username is already used by an existing trader"""
        existing_traders = db.list_collection_names()
        for trader in existing_traders:
            if username.lower() in trader:
                messages.error(request, 'Username already taken, try again')
                return redirect('dashboard')

        """If the username is available, create a new trader"""
        num_traders = len(existing_traders)
        if num_traders < 10:
            trader_name = f"trader_{username}_{str(uuid.uuid4())[:4]}".lower()
            trader = Trader(trader_name)
            try:
                trader.store_data(db)
                messages.success(request, f"Congratulations {username}, you have been given free $100 to Trade")
                return redirect('account', trader_name=trader_name)

            except pymongo.errors.ConnectionFailure as e:
                """Handle any connection errors"""
                
                print(f"Connection to MongoDB failed: {e}")
        else:
            messages.error(request, 'Sorry, the maximum number of sponsored users has been reached')
            return redirect('home')

    return render(request, 'lucky_trader.html')

def account(request, trader_name):
    user_datas = user_colection(trader_name, db)
    if user_datas:
        return render(request, 'account.html', 
                      {"user_datas": user_datas, "trader_name": trader_name})
    else:
        messages.error(request, 'User not found')
        return redirect('home')


def dashboard(request):
    if request.method == 'POST':
        form_data = request.POST
        account_name = form_data['account_name'].lower()

        """Check if the trader's collection exists in the database"""
        if account_name in db.list_collection_names():
            user_datas = user_colection(account_name, db)
            messages.success(request, f"Welcome {account_name}")

            """Check if there's data to plot"""
            if db[account_name].count_documents({}) > 0:
                """pass the graph to html template"""
                graph = generate_profit_loss_graph(db, account_name)
                return render(request, 'dashboard.html', 
                              {"account_name": account_name, 
                               "user_datas": user_datas,
                               "graph": graph,})
            else:
                messages.error(request, 'No data to plot.')

        else:
            messages.error(request, 'User not Found.')
    
    return render(request, "dashboard.html")


