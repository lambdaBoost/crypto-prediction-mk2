from binance.client import Client
import pandas as pd


def make_trading_pairs(currency_list):
    """
    
    Returns
    -------
    list of all possible trading pairs from the currencies list

    """
    
    pair_list = list()
    
    for i in range(len(currency_list)):
        for j in(range(len(currency_list))):
            if i != j:
                pair = currency_list[i] + currency_list[j]
                pair_list.append(pair)
                
    return pair_list

def get_biggest_trading_pair(api_key, api_secret):
    
    client = Client(api_key, api_secret)
    
    exchange_info = client.get_exchange_info()
    
    pair = exchange_info['symbols'][0]['symbol']
    
    return pair


def get_all_prices(api_key, api_secret):
    """
    return price of all traded pairs on binance

    Parameters
    ----------
    api_key : str
        DESCRIPTION.
    api_secret : str
        DESCRIPTION.

    Returns
    -------
    prices : dict
        prices of all trade pairs

    """
    client = Client(api_key, api_secret)
    prices = client.get_all_tickers()

    return prices
    
    

def get_recent_trades(sym, lim, api_key, api_secret):
    
    client = Client(api_key, api_secret)

    res = client.get_recent_trades(symbol=sym, limit=lim)
    

    return res


def get_max_time(trades, limit):
    """
    gets time of least recent trades from a retrieved json of recent trades

    Parameters
    ----------
    trades : list
        json from get_recent_trades.

    Returns
    -------
    None.

    """
    
    time = trades[limit]['time']
    
    return time

def filter_cutoff_time(trades, cut_time):
    
    """"
    filter out trades before the cutoff time
    
    """
    
    filtered = [d for d in trades if d['time'] < cut_time]
    
    return filtered


    
def get_qty_from_trades(trades):
    """
    return trade sizes from list of trades. uses isbuyermaker flag to define
    sells and buys using
    
    isBuyerMaker = true -> SELL
    isBuyerMaker = false -> BUY

    """
    
    qtys = [d['qty'] for d in trades]
    isBuyerMaker = [d['isBuyerMaker'] for d in trades]
    isBuyerMaker = [int(i) for i in isBuyerMaker]
    qtys = [float(i) for i in qtys]

    #multiply sells by -1 and buys by 1
    isBuyerMaker = [((-2*i)+1) for i in isBuyerMaker]  #convert to + and -1
    qtys = [a*b for a,b in zip(qtys,isBuyerMaker)]
    
    #probably dont need this if data is to be stored in a matrix
   # if(len(qtys) < limit):
        
    #    qtys += [0] * (limit - len(qtys))
    
    return qtys


def get_price_from_trades(trades):
    """
    returns the price of a given coin
    price is in units of the respective benchmark currency
    
    """
    
    coin_price = float(trades[0]['price'])
    
    return coin_price



def get_benchmark_currency_prices(benchmark_list, api_key, api_secret, usd='USDT'):
    """
    

    Parameters
    ----------
    benchmark_list : str
        list of benchmark currencies
    api_key : str
        api key object
    api_secret : str
        api secret object
    usd : str, optional
        stable coin to use for usd conversion. The default is 'USDT'.

    Returns
    -------
    dict

    """
    
    benchmark_prices = pd.DataFrame(columns = ['usd'], index=benchmark_list)
    
    for c in benchmark_list:
        
        pair = c + usd
        
        last_trade = get_recent_trades(pair, 1, api_key, api_secret)
        
        price = float(last_trade[0]['price'])
        
        benchmark_prices['usd'][c] = price
        
    return benchmark_prices
        
    

def get_available_symbols(api_key, api_secret):
    
    """
    get all available currency pairs from binance
    
    """
    pair_list = []
    
    client = Client(api_key, api_secret)
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
        pair_list.append(s['symbol'])
    
    return pair_list


def get_viable_currencies(currencies, pair_list):
    
    """
    takes availabel binance symbols and filters to get those available for
    trade against the benchmark currencies. Returns a list of all currencies 
    that can be traded against the benchmarks
    """

    pair_list = [ p for p in pair_list if any(c in p for c in currencies) ]
        
        
    currency_list = pair_list
    
    for c in currencies:
        
        currency_list  = [s.replace(c, "") for s in currency_list]
        
    #only include currencies that can be traded against all the benchmark currencies
    #currency_list=[c for c in currency_list if currency_list.count(c) != len(currencies)]
    
    currency_list = list(dict.fromkeys(currency_list))

        
    return currency_list


def filter_currency_list(currency_list, drops, limit):
    
    """
    takes list of viable currencies and drops preselected values
    limits to top n by market cap
    """
    
    #TODO - use CMC api for this
    
def make_pair_list(currency_list, benchmark_currencies):
    
    """
    takes full list of viable currencies after filtering and generates all
    pairs to fetch data for
    
    """
    
    pairs = []
    
    for b in benchmark_currencies:
        
        #append benchmark at both end and start to get both combos
        individual_list = [s + b for s in currency_list]
        pairs.append(individual_list)

        
    pairs = [pair for sublist in pairs for pair in sublist]
    
    
    return pairs


def get_coin_prices(currency_list):
    
    """
    return a dictionary of prices in usd
    """
    
    

    
    