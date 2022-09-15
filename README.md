# Earnings_Tracker

### Python application that allows one to view and track the latest quarterly earnings and compare stock performances of publicly listed companies. Full details and insights are below. 

### Screenshot 1 - App's opening window 
![Earnings tracker opening window](/SS_1.PNG "Opening window")
### Screenshot 2 - App's tracker view 
![Earnings tracker tracker view](/SS_2.PNG "Tracker view")

### :point_right: The problem?
Developed as a passion project and when time permitted to complete a version; I wanted a consolidated view of some of my favorite companies' latest quarterly results. I don't own any shares of blue-chip stocks like AAPL, MSFT, GOOG, TSLA, etc. But I regularly follow their monetary performance and wait for their respective quarter's [10-Q](https://www.investopedia.com/terms/1/10q.asp), as well as an [earnings call](https://www.investopedia.com/terms/e/earnings-call.asp) transcript/webcast to be released. Reading them gives me an idea of where the company's strategy is headed, what their current focus is, and if any of their businesses are particularly soaring or choking. And I manually do this at times as opposed to searching online and reading news articles - where I have to pay a fee to unlock the full story at website X or find that the results aren't out yet for 1 or 2 companies. Few websites exist that neatly present free results but they do not always cover the metrics that I personally want to observe nor do they show a consolidated view. Why consolidated view? Possible rookie talk, but if I had N dollars that I wanted to invest in the market, I could look at the latest [EPS](https://www.investopedia.com/terms/e/eps.asp) of AAPL and MSFT for example and choose to buy more shares of one company and that's enough. ***But*** if I was presented with their EPS, EBITDA margins, Net Incomes, Acquisition costs etc., I can then possibly see something that can help me make a more informed decision.   

#### Hence the entire intuition for this project was based on the premise - Can I make something that fetched, read, and showed the results for me instead? Not just a "results", but the results that I want to see.

### :point_right: Results? 
1. Cumulative returns for your stocks, from the past year until now. 
2. Current share price, latest and previous year stock performances, financial metrics like ROE, EPS, Net Income, etc - all for the most recent quarter period.
3. Why compare stock performances? (adjusted closing price in this case) Because the movement after earnings results reflects investor sentiment. Took inspiration from company reports where it is common to find comparisons that say "figures as of X date", and next to it "figures as of Y date".  

### :point_right: Tech stack? 
Python, Tkinter, Tk, 2 APIs ([yfinance](https://github.com/ranaroussi/yfinance) and [yahoo_fin](http://theautomatic.net/yahoo_fin-documentation/)), and some common Python libraries (Pandas, NumPy, Matplotlib, dateutil, datetime).

### :point_right: Files? 
The ipynb notebook shows some experimentation with the APIs. Had to mix-match and format values from the pool of results from yfinance and for what I wanted to show - calculate some [**time delta**](https://docs.python.org/3/library/datetime.html#timedelta-objects) objects. Fetching monetary data for the latest quarter is easy but getting the historical stock performance for the **exact same quarter** (could be Q1, Q2, Q3, or Annual) is tricky. More details below. The other two files are the main GUI files for the opening window and the tracker view (as per screenshots). 

### :point_right: Quarter disparity problem and a fix: 
#### What is Q1 for company X could be different for company Y because of the difference in the start and end times of their fiscal years, so a fixed definition of a quarter wouldn't be possible for all companies and I had to get creative.

<ol>
  <li>One particular result from the yfinance API (stock_ticker.quarterly_financials) shows a table-like breakdown of some monetary results for each quarter where the column names represent the quarter-ending date and the rows represent the results for the quarter that ended on said date.</li>
  <li>Fetch the current date, time, and year to get a timestamp.</li>
  <li>To recap, the first column name from the result in #1 is the date that represents the latest quarter-ending date, and hence likewise, the second column name represents the previous quarter-ending date. The time in between is the most recent quarter and it is for that period, that I need stock performance (apart from what's shown in stock_ticker.quarterly_financials).</li>
  <li>Fetch a year-1 timestamp for both the above 2 dates and now the time difference between these 2 can be used to fetch me the data for the same quarter but for the previous year.</li>
  <li>If the difference between the current timestamp and that of the first/latest column from the result in #1 exceeds by let's say 40 days (to account for delay in the quarter-ending date and publishment of results a.k.a "earnings season"), then I can say the "latest", latest quarterly results aren't out yet and that we are into a newer quarter where results would arrive in the future. As per this definition, the latest would mean whatever is last or out at the moment.</li> 
</ol>

### :point_right: Things left to do:
<ol>
  <li><strong>DONE</strong> - Make the whole tracker view scrollable so that you can see for n tickers/companies - took some effort but it's complete. </li> 
  <li>Connect the button from the opening window to the tracker view; need to pass inputs with it.</li>
  <li>Dynamically add more companies in the opening window (3 for now because the increase in space is causing the buttons to move a lot), another button for this? - those with some front-end expertise can suggest.</li>
  <li>A few Tkinter display elements are currently static in the tracker view. Put them all in a loop and make it generate based on n stock inputs. This should be easy.</li>
  <li>Use API again or do web scraping to fetch ticker symbol from company name. Makes sense for inputs to prefer names more.</li>
  <li><strong>DONE</strong> - Test automatic fetching of data for different tickers with the APIs.</li> 
  <li>Choose the best displaying elements in the tracker view. Tkinter is super quick to pick up and develop POCs, but I haven't explored the depth of what it has to offer. I'm also aware that popular front-end frameworks will be best alternatives but this is a desktop app for now.</li>
  <li>Choose a different set of plots to show maybe?</li>
  <li>And many more iterations of features...</li> 
</ol>

#### This would not have been possible without Stack Overflow, many youtube tutorials for Tkinter, [this documentation](https://www.pythontutorial.net/tkinter/) and the 2 APIs ([yfinance](https://github.com/ranaroussi/yfinance) and [yahoo_fin](http://theautomatic.net/yahoo_fin-documentation/)). Without the APIs, I would have to scrape data manually, which I guess would make things work but it will be very time-consuming. 
