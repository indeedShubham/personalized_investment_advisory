import requests

def get_mutual_fund_data(symbol, api_key):
    base_url = "https://www.alphavantage.co/query"
    function = "TIME_SERIES_DAILY"

    # Define the parameters for the request
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": "9MEZNVO5F7NAXERS"
    }

    # Send the request
    response = requests.get(base_url, params=params)

    # Parse the JSON response
    data = response.json()

    return data

# Replace 'YOUR_API_KEY' with your actual API key
# Replace 'MUTFUND_SYMBOL' with the symbol of the mutual fund you're interested in
data = get_mutual_fund_data('MUTFUND_SYMBOL', 'YOUR_API_KEY')

print(data)