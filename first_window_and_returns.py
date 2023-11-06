import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import datetime
from dateutil.relativedelta import relativedelta

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x100')
        self.title('New window (full tracker app)')

        ttk.Button(self,
                text='Close',
                command=self.destroy).pack(expand=True)



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('500x500')
        self.title('Earnings Tracker')
        
        label1 = Label(self, text='Welcome to the Earnings Tracker!')
        label1.pack(ipadx=1, ipady=7)
        
        label2 = Label(self, text='Track the quarterly performance of your favorite public companies with this app!')
        label2.pack(ipadx=1, ipady=7)
        
        label3 = Label(self, text='Start by entering the company names or their stock symbols below:')
        label3.pack(ipadx=1, ipady=7)
        
        
        signin = ttk.Frame(self)
        signin.pack(padx=100, pady=5, fill='x', expand=True)
        
        
        company1 = tk.StringVar()
        company2 = tk.StringVar()
        company3 = tk.StringVar()
        
        # Company entries
        text_label1 = ttk.Label(signin, text="Company 1 :")
        text_label1.pack(fill='x', expand=True)
        
        text_entry1 = ttk.Entry(signin, textvariable=company1)
        text_entry1.pack(fill='x', expand=True)
        text_entry1.focus()
        
        text_label2 = ttk.Label(signin, text="Company 2 :")
        text_label2.pack(fill='x', expand=True)
        
        text_entry2 = ttk.Entry(signin, textvariable=company2)
        text_entry2.pack(fill='x', expand=True)
        text_entry2.focus()
        
        text_label3 = ttk.Label(signin, text="Company 3 :")
        text_label3.pack(fill='x', expand=True)
        
        text_entry3 = ttk.Entry(signin, textvariable=company3)
        text_entry3.pack(fill='x', expand=True)
        text_entry3.focus()
        
        
        # Place a button on the root window
        generate_button_results = ttk.Button(self,text='View results',command=self.open_window)
        generate_button_results.pack(expand=True)
        
        
        generate_button_returns = ttk.Button(self, text="See historical returns", command=self.plot_graph)
        generate_button_returns.pack(expand=True)
        
        
    def plot_graph(self):
        
        dt = datetime.datetime.now()
        dt = datetime.datetime(dt.year, dt.month, dt.day)
        dt_1yr_ago = datetime.datetime.now() - relativedelta(years=1)
        dt_1yr_ago  = datetime.datetime(dt_1yr_ago.year, dt_1yr_ago.month, dt_1yr_ago.day)
        
        symbollist = ["AAPL", "MSFT", "GOOG"]
        data = yf.download(symbollist,dt_1yr_ago)['Adj Close']
        ((data.pct_change()+1).cumprod()).plot(figsize=(10, 7))
        
        plt.legend()
        plt.title("Historical performance", fontsize=16)
        plt.ylabel('Cumulative Returns', fontsize=14)
        plt.xlabel('Year', fontsize=14)
        
        plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
        plt.show()

        
        # Automate company entries with dynamic inputs   
# =============================================================================
#         def addBox():
#             
#             frame = ttk.Frame(self)
#             frame.pack()
#             comp_name = "Company "+str(len(all_entries)+1)
#             Label(frame, text=comp_name).grid(row=0, column=0)
#             ent1 = ttk.Entry(frame)
#             ent1.grid(row=1, column=0)
#             all_entries.append(ent1)
# =============================================================================
                

# =============================================================================
#         all_entries = [] 
#         addboxButton = ttk.Button(self, text='Add company', command=addBox)
#         addboxButton.pack()
# =============================================================================

        
# =============================================================================
#         # Place a button on the root window
#         ttk.Button(self,
#                 text='Open another window',
#                 command=self.open_window).pack(expand=True)
# =============================================================================

    def open_window(self):
        window = Window(self)
        window.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()
