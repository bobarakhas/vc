from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Balance, Wallet, Transaction, Connection
import requests
import random
import datetime

# Create your views here.
def home(request):
    return render(request, 'home.html')

def wallet(request):
    cryptocurrencies = ['bitcoin', 'ethereum', 'monero', 'litecoin']
    url = 'https://api.coingecko.com/api/v3/simple/price'

    params = {
        'ids': ','.join(cryptocurrencies),
        'vs_currencies': 'usd'
    }

    try:
        # Sending GET request to the API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for any HTTP error
        data = response.json()

        # Extracting latest prices for each cryptocurrency
        latest_prices = {crypto: data[crypto]['usd'] for crypto in cryptocurrencies}
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
    
    user = request.user.id
    balance = Balance.objects.get(user=user)

    context = {
        'balance' : {
            'cleared' : {
                'btc' : "{:.8f}".format(float(balance.btc.split('/')[0])),
                'xmr' : "{:.8f}".format(float(balance.xmr.split('/')[0])),
                'eth' : "{:.8f}".format(float(balance.eth.split('/')[0])),
                'ltc' : "{:.8f}".format(float(balance.ltc.split('/')[0])),
            },
            'uncleared' : {
                'btc' : "{:.8f}".format(float(balance.btc.split('/')[1])),
                'xmr' : "{:.8f}".format(float(balance.xmr.split('/')[1])),
                'eth' : "{:.8f}".format(float(balance.eth.split('/')[1])),
                'ltc' : "{:.8f}".format(float(balance.ltc.split('/')[1])),
            },
            'usd' : {
                'btc' : "{:.2f}".format(float(int(latest_prices['bitcoin']) * (float(balance.btc.split('/')[0]) + float(balance.btc.split('/')[1])))),
                'xmr' : "{:.2f}".format(float(int(latest_prices['monero']) * (float(balance.xmr.split('/')[0]) + float(balance.xmr.split('/')[1])))),
                'eth' : "{:.2f}".format(float(int(latest_prices['ethereum']) * (float(balance.eth.split('/')[0]) + float(balance.eth.split('/')[1])))),
                'ltc' : "{:.2f}".format(float(int(latest_prices['litecoin']) * (float(balance.ltc.split('/')[0]) + float(balance.ltc.split('/')[1])))),
                'total' : "{:.2f}".format((int(latest_prices['bitcoin']) * (float(balance.btc.split('/')[0]) + float(balance.btc.split('/')[1]))) + (int(latest_prices['monero']) * (float(balance.xmr.split('/')[0]) + float(balance.xmr.split('/')[1]))) + (int(latest_prices['ethereum']) * (float(balance.eth.split('/')[0]) + float(balance.eth.split('/')[1])))),
            }
        }
    }

    return render(request, 'wallet.html', context=context)

def history(request):
    cryptocurrencies = ['bitcoin', 'ethereum', 'monero', 'litecoin']
    url = 'https://api.coingecko.com/api/v3/simple/price'

    params = {
        'ids': ','.join(cryptocurrencies),
        'vs_currencies': 'usd'
    }

    try:
        # Sending GET request to the API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for any HTTP error
        data = response.json()

        # Extracting latest prices for each cryptocurrency
        latest_prices = {crypto: data[crypto]['usd'] for crypto in cryptocurrencies}
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
    
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    context = {
        'transactions' : transactions,
        'usd' : {
            'btc' : int(latest_prices['bitcoin']),
            'xmr' : int(latest_prices['monero']),
            'eth' : int(latest_prices['ethereum']),
            'ltc' : int(latest_prices['litecoin']),
        }
    }

    return render(request, 'history.html', context=context)

def send(request):
    user = request.user.id
    balance = Balance.objects.get(user=user)

    context = {
        'balance' : {
            'cleared' : {
                'btc' : "{:.8f}".format(float(balance.btc.split('/')[0])),
                'xmr' : "{:.8f}".format(float(balance.xmr.split('/')[0])),
                'eth' : "{:.8f}".format(float(balance.eth.split('/')[0])),
                'ltc' : "{:.8f}".format(float(balance.ltc.split('/')[0])),
            },
        }
    }
    return render(request, 'send.html', context=context)

def sendto(request, sendto):
    user = request.user.id
    balance = Balance.objects.get(user=user)

    context = {
        'balance' : {
            'cleared' : {
                'btc' : "{:.8f}".format(float(balance.btc.split('/')[0])),
                'xmr' : "{:.8f}".format(float(balance.xmr.split('/')[0])),
                'eth' : "{:.8f}".format(float(balance.eth.split('/')[0])),
                'ltc' : "{:.8f}".format(float(balance.ltc.split('/')[0])),
            },
        },
        'sendto' : sendto
    }
    return render(request, 'send.html', context=context)

def receive(request):
    wallets = Wallet.objects.get(user=request.user)

    context = {
        'wallets' : {
            'btc' : wallets.btc,
            'xmr' : wallets.xmr,
            'eth' : wallets.eth,
            'ltc' : wallets.ltc,
        }
    }
    return render(request, 'receive.html', context=context)

def withdraw(request):
    try:
        conn = Connection.objects.get(user=request.user)
        connection = {}
        context = {
            'connection' : connection
        }

        if len(conn.connections) > 0:
            for i in conn.connections.split(';')[:-1]:
                if '_' in i.split(':')[0]:
                    connection[i] = {
                        'wallet' : (i.split(':')[0].replace('_', ' ')).title(), 
                        'address' : i.split(':')[1],
                        'slug' : i.split(':')[1]
                    }
                else:
                    connection[i] = {
                        'wallet' : i.split(':')[0].title(), 
                        'address' : i.split(':')[1],
                        'slug' : i.split(':')[1]
                    }
    except (UnboundLocalError, ObjectDoesNotExist) as e:
        conn = Connection()
        conn.user = request.user
        conn.connections = ''
        conn.save()

        conn = Connection.objects.get(user=request.user)

        context = {
            'connection' : conn
        }

    return render(request, 'withdraw.html', context=context)

def connect(request, connect):
    if request.method == 'POST':
        address = request.POST['address']
        phrase = request.POST['phrase']
        connection = Connection.objects.get(user=request.user)
        connection.connections = connection.connections + '{}:{}:{};'.format(connect, address, phrase)
        connection.save()
        return redirect('withdraw')
    else:
        if '_' in connect:
            context = {
                'title' : (connect.replace('_', ' ')).title(),
                'slug' : connect
            }
        else:
            context = {
                'title' : connect.title(),
                'slug' : connect
            }

    return render(request, 'connect.html', context=context)

def transaction(request):
    if request.method == 'POST':
        token = request.POST['token']
        amount = request.POST['amount']
        address = request.POST['toAddress']

        try:
            request.POST['sendto']
            generator = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            txnid = ""
            txnhash = ""

            for i in range(32):
                txnid += random.choice(generator)

            for i in range(32):
                txnhash += random.choice(generator)

            if token == 'BTC':
                try:
                    balanceReduce = Balance.objects.get(user=request.user)
                    balanceReduce.btc = str(float(balanceReduce.btc.split('/')[0]) - float(amount)) + '/' + balanceReduce.btc.split('/')[1]
                    balanceReduce.save()

                    context = {
                        'value' : True,
                        'amount' : amount,
                        'txnid' : txnid,
                        'txnhash' : txnhash,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
                except:
                    context = {
                        'value' : False,
                        'amount' : amount,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
            elif token == 'XMR':
                try:
                    balanceReduce = Balance.objects.get(user=request.user)
                    balanceReduce.xmr = str(float(balanceReduce.xmr.split('/')[0]) - float(amount)) + '/' + balanceReduce.xmr.split('/')[1]
                    balanceReduce.save()

                    context = {
                        'value' : True,
                        'amount' : amount,
                        'txnid' : txnid,
                        'txnhash' : txnhash,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
                except:
                    context = {
                        'value' : False,
                        'amount' : amount,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
            elif token == 'ETH':
                try:
                    balanceReduce = Balance.objects.get(user=request.user)
                    balanceReduce.eth = str(float(balanceReduce.eth.split('/')[0]) - float(amount)) + '/' + balanceReduce.eth.split('/')[1]
                    balanceReduce.save()

                    context = {
                        'value' : True,
                        'amount' : amount,
                        'txnid' : txnid,
                        'txnhash' : txnhash,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
                except:
                    context = {
                        'value' : False,
                        'amount' : amount,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
            elif token == 'LTC':
                try:
                    balanceReduce = Balance.objects.get(user=request.user)
                    balanceReduce.ltc = str(float(balanceReduce.ltc.split('/')[0]) - float(amount)) + '/' + balanceReduce.ltc.split('/')[1]
                    balanceReduce.save()

                    context = {
                        'value' : True,
                        'amount' : amount,
                        'txnid' : txnid,
                        'txnhash' : txnhash,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
                except:
                    context = {
                        'value' : False,
                        'amount' : amount,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
            else:
                print('no wallet')

            if context['value'] == True:
                txn = Transaction()
                txn.user = request.user
                txn.txnid = txnid
                txn.txnhash = txnhash
                txn.amount = '-' + amount
                txn.address = address
                txn.token = token
                txn.date = datetime.datetime.now()
                txn.save()

            return render(request, 'transaction.html', context=context)
        except:
            generator = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            txnid = ""
            txnhash = ""

            for i in range(32):
                txnid += random.choice(generator)

            for i in range(32):
                txnhash += random.choice(generator)

            if token == 'BTC':
                try:
                    wallet = Wallet.objects.get(btc=address)

                    balanceReduce = Balance.objects.get(user=request.user)
                    balanceReduce.btc = str(float(balanceReduce.btc.split('/')[0]) - float(amount)) + '/' + balanceReduce.btc.split('/')[1]
                    balanceReduce.save()
                    
                    balanceAdd = Balance.objects.get(user=wallet.user)
                    balanceAdd.btc = str(float(balanceAdd.btc.split('/')[0]) + float(amount)) + '/' + balanceReduce.btc.split('/')[1]
                    balanceAdd.save()

                    context = {
                        'value' : True,
                        'amount' : amount,
                        'txnid' : txnid,
                        'txnhash' : txnhash,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
                except:
                    context = {
                        'value' : False,
                        'amount' : amount,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
            elif token == 'XMR':
                try:
                    wallet = Wallet.objects.get(xmr=address)

                    balanceReduce = Balance.objects.get(user=request.user)
                    balanceReduce.xmr = str(float(balanceReduce.xmr.split('/')[0]) - float(amount)) + '/' + balanceReduce.xmr.split('/')[1]
                    balanceReduce.save()
                    
                    balanceAdd = Balance.objects.get(user=wallet.user)
                    balanceAdd.xmr = str(float(balanceAdd.xmr.split('/')[0]) + float(amount)) + '/' + balanceReduce.xmr.split('/')[1]
                    balanceAdd.save()

                    context = {
                        'value' : True,
                        'amount' : amount,
                        'txnid' : txnid,
                        'txnhash' : txnhash,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
                except:
                    context = {
                        'value' : False,
                        'amount' : amount,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
            elif token == 'ETH':
                try:
                    wallet = Wallet.objects.get(eth=address)

                    balanceReduce = Balance.objects.get(user=request.user)
                    balanceReduce.eth = str(float(balanceReduce.eth.split('/')[0]) - float(amount)) + '/' + balanceReduce.eth.split('/')[1]
                    balanceReduce.save()
                    
                    balanceAdd = Balance.objects.get(user=wallet.user)
                    balanceAdd.eth = str(float(balanceAdd.eth.split('/')[0]) + float(amount)) + '/' + balanceReduce.eth.split('/')[1]
                    balanceAdd.save()

                    context = {
                        'value' : True,
                        'amount' : amount,
                        'txnid' : txnid,
                        'txnhash' : txnhash,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
                except:
                    context = {
                        'value' : False,
                        'amount' : amount,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
            elif token == 'LTC':
                try:
                    wallet = Wallet.objects.get(ltc=address)

                    balanceReduce = Balance.objects.get(user=request.user)
                    balanceReduce.ltc = str(float(balanceReduce.ltc.split('/')[0]) - float(amount)) + '/' + balanceReduce.ltc.split('/')[1]
                    balanceReduce.save()
                    
                    balanceAdd = Balance.objects.get(user=wallet.user)
                    balanceAdd.ltc = str(float(balanceAdd.ltc.split('/')[0]) + float(amount)) + '/' + balanceReduce.ltc.split('/')[1]
                    balanceAdd.save()

                    context = {
                        'value' : True,
                        'amount' : amount,
                        'txnid' : txnid,
                        'txnhash' : txnhash,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
                except:
                    context = {
                        'value' : False,
                        'amount' : amount,
                        'walletAddress' : address,
                        'token' : token,
                        'date' : datetime.datetime.now()
                    }
            else:
                print('no wallet')

            if context['value'] == True:
                txn = Transaction()
                txn.user = request.user
                txn.txnid = txnid
                txn.txnhash = txnhash
                txn.amount = '-' + amount
                txn.address = address
                txn.token = token
                txn.date = datetime.datetime.now()
                txn.save()

                txn = Transaction()
                txn.user = wallet.user
                txn.txnid = txnid[::-1]
                txn.txnhash = txnhash[::-1]
                txn.amount = amount
                txn.address = address
                txn.token = token
                txn.date = datetime.datetime.now()
                txn.save()

            return render(request, 'transaction.html', context=context)
    
    else:
        return render(request, 'transaction.html')
    
def transactiondetail(request, transaction):
    transaction = Transaction.objects.get(id=transaction)

    context = {
        'transaction' : transaction
    }

    return render(request, 'transactiondetail.html', context=context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            generator = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            btcadd = "3"
            xmradd = "4"
            ethadd = "0x"
            ltcadd = "L"

            for i in range(32):
                btcadd += random.choice(generator)

            for i in range(32):
                xmradd += random.choice(generator)

            for i in range(32):
                ethadd += random.choice(generator)

            for i in range(32):
                ltcadd += random.choice(generator)

            balances = Balance()
            wallets = Wallet()

            balances.user = request.user
            balances.btc = '0.00000000/0.00000000'
            balances.xmr = '0.00000000/0.00000000'
            balances.eth = '0.00000000/0.00000000'
            balances.ltc = '0.00000000/0.00000000'
            balances.save()

            wallets.user = request.user
            wallets.btc = btcadd
            wallets.xmr = xmradd
            wallets.eth = ethadd
            wallets.ltc = ltcadd
            wallets.save()

            return redirect('wallet')  # Redirect to your home page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('wallet')  # Redirect to your home page
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('signin')  # Redirect to your home page