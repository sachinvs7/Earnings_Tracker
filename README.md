# Earnings_Tracker

### Python application to view and track the latest quarterly earnings of publicly listed companies and compare their stock performances. 

###  :point_right: App's opening window 
![Earnings tracker opening window](/SS_1.PNG "Opening window")
###  :point_right: App's tracker view 
![Earnings tracker tracker view](/SS_2.PNG "Tracker view")

### Problem: 

Developed as a simple hobby project, and whenever time permitted, I wanted a consolidated view of the latest quarterly results for some of my favorite companies. I routinely track their financial performance through [10-Qs and 10-Ks](https://www.investopedia.com/terms/1/10q.asp), as well as eagerly await the release of their earnings call transcript/webcast. Reading them gives me an idea of where the company's strategy is headed, and whether any of their businesses or services are particularly thriving or facing challenges. Sometimes, I choose to do this manually instead of searching online and reading news articles. This is because on some websites, I have to pay a fee to unlock the full story at website X or subscribe to a tool with a hefty monthly charge. I also often find that the results for one or two companies are not yet available. While there are a few websites that neatly present free results, they do not always cover the specific metrics I want to observe, nor do they provide a consolidated view. Hence, this alternative.


### Results:
1. Cumulative returns for stocks, from the past year until now. 
2. Current share price, latest and previous year stock performances (adjusted closing price), and several other financial metrics - all for the most recent quarter period.

### Tech stack:
Python, Tkinter, Tk, 2 APIs ([yfinance](https://github.com/ranaroussi/yfinance) and [yahoo_fin](http://theautomatic.net/yahoo_fin-documentation/)), and some common Python libraries (Pandas, NumPy, Matplotlib, dateutil, datetime).

### Files:
Fetching monetary data for the latest quarter was easy but getting the historical stock performance for the **exact same quarter** (Q1, Q2, Q3, or annual) was not. This is because what constitutes Q1 for company X may differ from that of company Y due to variations in the start and end times of their fiscal years. So the .ipynb notebook shows some experimentation with the APIs. Had to mix-match and format values from the yfinance pool of results and for what I wanted to show - calculate [time delta](https://docs.python.org/3/library/datetime.html#timedelta-objects) objects. The other two files are the main GUI files for the opening window and the tracker view (as per screenshots). 


This would not have been possible without Stack Overflow, many youtube tutorials for Tkinter, [this documentation](https://www.pythontutorial.net/tkinter/) and the 2 APIs ([yfinance](https://github.com/ranaroussi/yfinance) and [yahoo_fin](http://theautomatic.net/yahoo_fin-documentation/)). Without the APIs, I would have had to scrape data manually, which, although feasible, would have been very time-consuming.
