import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yfinance as yf
from peterLynchFairValue import get_fair_value_peterl
from dcfFairValue import get_fair_value_dcf

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate usinng JSON key file
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

batch_range = []

# Open the Google sheet
sheet = client.open("Stocks").sheet1

# Get all Tickers
tickers = sheet.col_values(24)

def average_of_fair_values(fv1,fv2):
    fair_value1 = fv1 if isinstance(fv1, (int, float)) and fv1 > 0 else 0
    fair_value2 = fv2 if isinstance(fv2, (int, float)) and fv2 > 0 else 0

    count = 1 if fair_value1 > 0 else 0
    count += 1 if fair_value2 > 0 else 0
    
    # Calculate average if there are valid values
    if count > 0:
        return (fair_value1 + fair_value2) / count
    else:
        return None  # Return None if no valid values

# Use correct keys to get Fair Value, Current ratio, Profit margin, Operating Margin, Operating cash flow, Overall Risk for each ticker
for i in range(1, len(tickers)):
    ticker = tickers[i]
    stock = yf.Ticker(ticker)
    #get fair value
    peterFairValue = get_fair_value_peterl(ticker)  # Get fair value using Peter Lynch's method
    dcfFairValue = get_fair_value_dcf(ticker)  # Get fair value using DCF method
    fair_value = average_of_fair_values(peterFairValue, dcfFairValue); # Calculate the average of positive values among the two fair values
    temp_values = [stock.info.get("currentRatio", "N/A"), round(stock.info.get("profitMargins", 0)*100,2),round(stock.info.get("operatingMargins", 0)*100,2),round(stock.info.get("operatingCashflow", 0)/1000000000,2),stock.info.get("overallRisk", "N/A"),fair_value]
    batch_range.append(temp_values)
    #print("'",ticker,"': ",temp_values)
# Update the Google sheet
sheet.batch_update([{ "range": "J2", "values": batch_range }])
print("Sheet updated successfully!")
