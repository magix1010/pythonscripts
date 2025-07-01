import yfinance as yf

def get_fair_value_peterl(ticker):
    # Fetch stock data
    stock = yf.Ticker(ticker)
    
    # Get the latest EPS
    eps = stock.info.get('trailingEps', None)
    if eps is None:
        print(f"Could not fetch EPS for {ticker}.")
        return None

    # Get the expected growth rate (use analysts' projections)
    growth_rate = stock.info.get('earningsGrowth', None)
    if growth_rate is None:
        print(f"Could not fetch Growth Rate for {ticker}.")
        return None
    
    # Get the current PE Ratio
    pe_ratio = stock.info.get('trailingPE', None)
    if pe_ratio is None:
        print(f"Could not fetch PE Ratio for {ticker}.")
        return None

    # Peter Lynch's Fair Value Formula
    fair_value = eps * (1 + growth_rate) * pe_ratio
    
    return fair_value

# Example Usage
# ticker = input("Enter stock ticker: ").upper()
# fair_value = get_fair_value_peterl(ticker)

# if fair_value:
#     print(f"The estimated fair value of {ticker} is: ${fair_value:.2f}")