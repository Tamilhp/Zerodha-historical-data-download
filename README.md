# Zerodha-historical-data-download
This repository contains code to download historical data for more than 2000 days and intraday data for more than 100 days.
Download the framework and customize accordingly.
The language used is python.



The changes you need to make.

Set your working directory where you want your data to be downloaded.

Enter your API key.

Enter youy API secret.

Generate request_token.

Set the Access token.

In the 'tickers' variable write all the stock names you want(write the names exactly as in zerodha app).

in the fetchOHLC func, enter the number of days.

Note: If you want F&O data, change the instruments('NSE') to instruments('NFO').
