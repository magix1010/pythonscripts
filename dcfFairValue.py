import yfinance as yf

def get_fair_value_dcf(ticker, years=5, discount_rate=0.10, terminal_growth=0.02):
    stock = yf.Ticker(ticker)

    # Get Free Cash Flow (FCF)
    cash_flow_stmt = stock.cashflow
    try:
        free_cash_flow = cash_flow_stmt.loc["Operating Cash Flow"] - cash_flow_stmt.loc["Capital Expenditure"]
        latest_fcf = free_cash_flow.iloc[0]  # Latest FCF value
    except:
        print("Could not retrieve Free Cash Flow data.")
        return None

    # Get growth rate (using analysts' projections or historical growth)
    growth_rate = stock.info.get("earningsGrowth", 0.05)  # Default to 5% if not available

    # Discount future cash flows
    discounted_fcf = 0
    for year in range(1, years + 1):
        future_fcf = latest_fcf * ((1 + growth_rate) ** year)
        discounted_fcf += future_fcf / ((1 + discount_rate) ** year)

    # Terminal Value Calculation
    terminal_value = (latest_fcf * (1 + terminal_growth)) / (discount_rate - terminal_growth)
    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** years)

    # Total present value of cash flows
    total_fair_value = discounted_fcf + discounted_terminal_value

    # Get number of outstanding shares
    shares_outstanding = stock.info.get("sharesOutstanding", None)
    if shares_outstanding is None:
        print("Could not retrieve shares outstanding.")
        return None

    # Fair value per share
    fair_value_per_share = total_fair_value / shares_outstanding

    return round(fair_value_per_share, 2)

# Example Usage
# ticker = input("Enter stock ticker: ").upper()
# fair_value = get_fair_value_dcf(ticker)

# if fair_value:
#     print(f"The estimated fair value of {ticker} is: ${fair_value}")
