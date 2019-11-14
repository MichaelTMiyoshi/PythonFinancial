# Data Science
# Finance using Yahoo Finance API
# from:
#   https://learndatasci.com/tutorials/python-finance-part-yahoo-finance-api-pandas-matplotlib/
# NOTE:
#   Had to install pandas-datareader.  The dash (-) becomes an underscore(_)
#   in the program.
# fix in code (took out panel_data.to_frame().head(9) line) from:
#   https://longervision.github.io/2018/11/07/Finance/finance-data/
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# define the instruments to download.  Apple, Microsoft, S&P500 index.
tickers = ["AAPL", "MSFT", "^GSPC"]

# data from 01/01/2010 through 12/31/2016
start_date = "2010-01-01"
end_date = "2016-12-31"

# user pandas_reader.data.DataReader to load the desired data.  Simple.
#panel_data = data.DataReader("INPX", "yahoo", start_date, end_date)
panel_data = data.DataReader(tickers, "yahoo", start_date, end_date)
#panel_data = data.DataReader(tickers, data_source="google", start=start_date, end=end_date)
#panel_data.to_frame().head(9)
######################################
#print(panel_data)
######################################
# getting just the adjusted closing prices.  This will return a Pandas DataFrame
# The index in this DataFrame is the major index of the panel_data.
close = panel_data["Close"]

# Getting all the weekdays between 01/01/2010 and 12/31/2016
all_weekdays = pd.date_range(start=start_date, end=end_date, freq = "B")

# How do we align the existing prices in adj_close with our new set of dates?
# All we need to do is reindex close using all_weekdays as the new index
close = close.reindex(all_weekdays)

# Reindexing will insert missing values (NaN) for the dates that were not present
# in the original set.  To cope with this, we can fill the missing by replacing
# them with the latest price for each instrument.
close = close.fillna(method="ffill")
#print(all_weekdays)
close.head(10)
#print(close.head(10))
print(close)
#close.describe()
print(close.describe())

# Get the MSFT timeseries.  This now returns a Pandas Series object indexed by date.
msft = close.loc[:, "MSFT"]

# Calculate the 20 and 100 days moving averages of the closing  prices
short_rolling_msft = msft.rolling(window=20).mean()
long_rolling_msft = msft.rolling(window=100).mean()

# Plot everything by leveraging the very powerful matplotlib package
fig, ax = plt.subplots(figsize=(16,9))

ax.plot(msft.index, msft, label="MSFT")
ax.plot(short_rolling_msft.index, short_rolling_msft, label="20 days rolling")
ax.plot(long_rolling_msft.index, long_rolling_msft, label="100 days rolling")

ax.set_xlabel("Date")
ax.set_ylabel("Adjusted closing price ($)")
ax.legend()

# had to look at
#   https://matplotlib.org/3.1.1/tutorials/introductory/pyplot.html
# to show me how to show the plot
#   It is cool.  Worth the work to get plots out.
fig.show()
