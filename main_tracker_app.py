import datetime
import yfinance as yf
import pandas as pd
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from yahoo_fin import stock_info as si
from tkinter import ttk
  
dt = datetime.datetime.now()
dt = datetime.datetime(dt.year, dt.month, dt.day)
dt_1yr_ago = datetime.datetime.now() - relativedelta(years=1)
dt_1yr_ago  = datetime.datetime(dt_1yr_ago.year, dt_1yr_ago.month, dt_1yr_ago.day)

symbollist = ["AAPL", "MSFT", "GOOG", "TSLA", "GME"]

def extract_from_api(stock_symbol):
    yahoo_stock_data = yf.download(stock_symbol,period='max')
    stock_data = yf.Ticker(stock_symbol)

    latest_col = stock_data.quarterly_financials.columns[0]
    d1 = latest_col.date()
    d2 = dt.date()

    def days_between(d1, d2):
        d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)

    diff_count = days_between(str(d1),str(d2)) 
    
    # Number of days since the quarter ended ^
    # If it exceeds by 40 days then let's say that the latest quarter results aren't out yet ? 

    latest_col_prev_q = stock_data.quarterly_financials.columns[1]
    latest_col, latest_col_prev_q

    # Quarter ended x, Quarter ended y ^ 

    dt_1yr_ago_l1 = latest_col - relativedelta(years=1)
    dt_1yr_ago_l2  = latest_col_prev_q - relativedelta(years=1)

    dt_1yr_ago_l1, dt_1yr_ago_l2

    # Quarter ended x, Quarter ended y : but 1 year before ^

    yahoo_stock_data_past = yahoo_stock_data.loc[yahoo_stock_data.index >= dt_1yr_ago_l2]
    yahoo_stock_data_past = yahoo_stock_data_past.loc[yahoo_stock_data_past.index <= dt_1yr_ago_l1]
    yahoo_stock_data_past['Adj Close'].plot()

    yahoo_stock_data_present = yahoo_stock_data.loc[yahoo_stock_data.index >= latest_col_prev_q]
    yahoo_stock_data_present = yahoo_stock_data_present.loc[yahoo_stock_data_present.index <= latest_col]
    yahoo_stock_data_present['Adj Close'].plot()

    data_rec = stock_data.recommendations
    data_rec = data_rec.loc[data_rec.index >= latest_col]
    recommendation = data_rec['To Grade'].value_counts().index[0]

    def human_format(num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])



    vallist = []
    vallist.append(latest_col.date())
    vallist.append('$'+human_format(stock_data.quarterly_financials[latest_col]['Total Revenue']))
    vallist.append('$'+human_format(stock_data.quarterly_financials[latest_col]['Total Operating Expenses']))
    vallist.append('$'+human_format(stock_data.quarterly_financials[latest_col]['Gross Profit']))
    vallist.append('$'+human_format(stock_data.quarterly_financials[latest_col]['Net Income']))
    vallist.append('$'+human_format(stock_data.quarterly_financials[latest_col]['Ebit']))
    vallist.append(str(stock_data.info['returnOnEquity']*100)+'%')
    vallist.append('$' + str(stock_data.info['forwardEps']))
    vallist.append('$' + str(stock_data.info['trailingEps']))
    vallist.append(str(stock_data.info['earningsGrowth'])+'%')
    vallist.append('$' + str(stock_data.info['revenuePerShare']))
    vallist.append('$'+human_format(stock_data.info['enterpriseValue']))
    vallist.append(recommendation)
    vallist

    info_df = pd.DataFrame([vallist],columns=['Quarter_Ended_On','Total_Revenue','Total_Operating_Expenses',
                                              'Gross_Profit', 'Net_Income', 'EBIT',
                                              'Return_On_Equity', 'Forward_EPS', 'Trailing_EPS',
                                              'Earnings_Growth', 'Revenue_Per_Share', 'Enterprise_Value',
                                              'Analyst_Recommendation'])
    info_df_transposed = info_df.T.copy()
    info_df_transposed.columns = ["value"]
    info_df_transposed["index"] = info_df_transposed.index.astype(str)
    info_df_transposed = info_df_transposed[["index", "value"]]
    info_df_transposed['Combined'] = info_df_transposed[info_df_transposed.columns[0:]].apply(
            lambda x: ':'.join(x.dropna().astype(str)),
            axis=1
        )

    return info_df_transposed, yahoo_stock_data_past, yahoo_stock_data_present

    



 
# AAPL
aapl_results, aapl_past, aapl_present = extract_from_api(symbollist[0])    
# MSFT
msft_results, msft_past, msft_present = extract_from_api(symbollist[1])    
# GOOG
goog_results, goog_past, goog_present = extract_from_api(symbollist[2])    



# Tkinter design and layout

plt.style.use('seaborn-darkgrid')
root = tk.Tk()
root.geometry("1200x1000")


# To make whole window scrollable:
# =============================================================================
# Create a main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH,expand=1)

# Create frame for x scrollbar
sec = tk.Frame(main_frame)
sec.pack(fill=tk.X,side=tk.BOTTOM)

# Create a canvas
my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

# Add scrollbars to canvas
x_scrollbar = ttk.Scrollbar(sec,orient=tk.HORIZONTAL,command=my_canvas.xview)
x_scrollbar.pack(side=tk.BOTTOM,fill=tk.X)
y_scrollbar = ttk.Scrollbar(main_frame,orient=tk.VERTICAL,command=my_canvas.yview)
y_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

# Configure the canvas
my_canvas.configure(xscrollcommand=x_scrollbar.set)
my_canvas.configure(yscrollcommand=y_scrollbar.set)
my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(tk.ALL))) 

# Create another frame INSIDE the canvas
second_frame = tk.Frame(my_canvas)

# Add that new Frame to a window in the canvas
my_canvas.create_window((0,0),window= second_frame, anchor="nw")
# =============================================================================


stock1results = tk.StringVar()
stock2results = tk.StringVar()
stock3results = tk.StringVar()

# Initialize the stocks
stock1 = yf.Ticker(symbollist[0])
stock2 = yf.Ticker(symbollist[1])
stock3 = yf.Ticker(symbollist[2])
stock4 = yf.Ticker(symbollist[3])
stock5 = yf.Ticker(symbollist[4])

stock1labelholder = tk.StringVar()
stock2labelholder = tk.StringVar()
stock3labelholder = tk.StringVar()

symbol1 = tk.StringVar()
symbol1.set(symbollist[0])
symbol2 = tk.StringVar()
symbol2.set(symbollist[1])
symbol3 = tk.StringVar()
symbol3.set(symbollist[2])


# Labels for stock data
tk.Label(second_frame, textvariable=stock1labelholder, font=("Roboto", 20)).grid(row=0, column=1, sticky='WENS')
#tk.Label(second_frame, textvariable=symbol1, font=("Roboto", 20)).grid(row=0, column=1, sticky='WENS')

tk.Label(second_frame, textvariable=stock2labelholder, font=("Roboto", 20)).grid(row=2, column=1, sticky='WENS')
#tk.Label(second_frame, textvariable=symbol2, font=("Roboto", 20)).grid(row=2, column=1, sticky='WENS')

tk.Label(second_frame, textvariable=stock3labelholder, font=("Roboto", 20)).grid(row=4, column=1, sticky='WENS')
#tk.Label(second_frame, textvariable=symbol3, font=("Roboto", 20)).grid(row=4, column=1, sticky='WENS')



stock1labelholder.set(symbol1.get()+", "+"Current Share Price: " +"$"+ (str(round(float(si.get_live_price(symbol1.get())), 2))))
stock2labelholder.set(symbol2.get()+", "+"Current Share Price: " +"$"+ (str(round(float(si.get_live_price(symbol2.get())), 2))))
stock3labelholder.set(symbol3.get()+", "+"Current Share Price: " +"$"+ (str(round(float(si.get_live_price(symbol3.get())), 2))))



# First
tk.Label(second_frame, text="Latest Quarterly Results ↓", font=("Roboto", 20)).grid(row=0, column=3, sticky='WENS')
stock1box = tk.Listbox(second_frame, listvariable=stock1results, font=("Roboto", 12), bd=7, width=35)
stock1box.grid(row=1, column=3, sticky='WENS')
# Second
tk.Label(second_frame, text="Latest Quarterly Results ↓", font=("Roboto", 20)).grid(row=2, column=3, sticky='WENS')
stock2box = tk.Listbox(second_frame, listvariable=stock2results, font=("Roboto", 12), bd=7, width=35)
stock2box.grid(row=3, column=3, sticky='WENS')
# Third
tk.Label(second_frame, text="Latest Quarterly Results ↓", font=("Roboto", 20)).grid(row=4, column=3, sticky='WENS')
stock3box = tk.Listbox(second_frame, listvariable=stock3results, font=("Roboto", 12), bd=7, width=35)
stock3box.grid(row=5, column=3, sticky='WENS')


stock1results.set('\n'.join(aapl_results['Combined']))
stock2results.set('\n'.join(msft_results["Combined"]))
stock3results.set('\n'.join(goog_results['Combined']))


# Figure one data
df1 = None
figure1 = plt.Figure(figsize=(4, 3.5), dpi=100)
ax1 = figure1.add_subplot(111)
canvas1 = FigureCanvasTkAgg(figure1, second_frame)
canvas1.get_tk_widget().grid(row=1, column=1, sticky='WENS')

# Figure two data
df2 = None
figure2 = plt.Figure(figsize=(4, 3.5), dpi=100)
ax2 = figure2.add_subplot(111)
canvas2 = FigureCanvasTkAgg(figure2, second_frame)
canvas2.get_tk_widget().grid(row=1, column=2, sticky='WENS')

# Figure three data
df3 = None
figure3 = plt.Figure(figsize=(4, 3.5), dpi=100)
ax3 = figure3.add_subplot(111)
canvas3 = FigureCanvasTkAgg(figure3, second_frame)
canvas3.get_tk_widget().grid(row=3, column=1, sticky='WENS')

# Figure four data
df4 = None
figure4 = plt.Figure(figsize=(4, 3.5), dpi=100)
ax4 = figure4.add_subplot(111)
canvas4 = FigureCanvasTkAgg(figure4, second_frame)
canvas4.get_tk_widget().grid(row=3, column=2, sticky='WENS')

# Figure five data
df5 = None
figure5 = plt.Figure(figsize=(4, 3.5), dpi=100)
ax5 = figure5.add_subplot(111)
canvas5 = FigureCanvasTkAgg(figure5, second_frame)
canvas5.get_tk_widget().grid(row=5, column=1, sticky='WENS')

# Figure six data
df6 = None
figure6 = plt.Figure(figsize=(4, 3.5), dpi=100)
ax6 = figure6.add_subplot(111)
canvas6 = FigureCanvasTkAgg(figure6, second_frame)
canvas6.get_tk_widget().grid(row=5, column=2, sticky='WENS')


def startup():
    plotgraph1()
    plotgraph3()
    plotgraph2()
    plotgraph4()
    plotgraph5()
    plotgraph6()



def plotgraph1():
    global df1, figure1, ax1, root, canvas1
    data = aapl_past['Adj Close']
    data.index = data.index.strftime("%m/%d/%y")
    ax1.clear()
    df1 = None
    df1 = data
    df1.plot(kind='line', legend=False, ax=ax1, grid=True, x=df1.index,y='Adj Close', title="Last Year's Stock Performance (Same Quarter)")
    figure1.autofmt_xdate()
    canvas1.draw_idle()


def plotgraph2():
    global df2, figure2, ax2, root, canvas2
    data = aapl_present['Adj Close']
    data.index = data.index.strftime("%m/%d/%y")
    ax2.clear()
    df2 = None
    df2 = data
    df2.plot(kind='line', legend=False, ax=ax2, grid=True, x=df2.index,y='Adj Close', title="Latest Quarter Stock Performance")
    figure2.autofmt_xdate()
    canvas2.draw_idle()


def plotgraph3():
    global df3, figure3, ax3, root, canvas3
    data = msft_past['Adj Close']
    data.index = data.index.strftime("%m/%d/%y")
    ax3.clear()
    df3 = None
    df3 = data
    df3.plot(kind='line', legend=False, ax=ax3, grid=True, x=df3.index,y='Adj Close', title="Last Year's Stock Performance (Same Quarter)")
    figure3.autofmt_xdate()
    canvas3.draw_idle()


def plotgraph4():
    global df4, figure4, ax4, root, canvas4
    data = msft_present['Adj Close']
    data.index = data.index.strftime("%m/%d/%y")
    ax4.clear()
    df4 = None
    df4 = data
    df4.plot(kind='line', legend=False, ax=ax4, grid=True, x=df4.index,y='Adj Close', title="Latest Quarter Stock Performance")
    figure4.autofmt_xdate()
    canvas4.draw_idle()
    
    
def plotgraph5():
    global df5, figure5, ax5, root, canvas5
    data = goog_past['Adj Close']
    data.index = data.index.strftime("%m/%d/%y")
    ax5.clear()
    df5 = None
    df5 = data
    df5.plot(kind='line', legend=False, ax=ax5, grid=True, x=df5.index,y='Adj Close', title="Last Year's Stock Performance (Same Quarter)")
    figure5.autofmt_xdate()
    canvas5.draw_idle()
    
    
def plotgraph6():
    global df6, figure6, ax6, root, canvas6
    data = goog_present['Adj Close']
    data.index = data.index.strftime("%m/%d/%y")
    ax6.clear()
    df6 = None
    df6 = data
    df6.plot(kind='line', legend=False, ax=ax6, grid=True, x=df6.index,y='Adj Close', title="Latest Quarter Stock Performance")
    figure6.autofmt_xdate()
    canvas6.draw_idle()



plt.show()
root.wm_title("Earnings Tracker")
startup()
root.mainloop()
