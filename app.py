import yfinance as yf
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

def fetch_stock_data(tickers, start_date, end_date):
    """Fetch stock data from Yahoo Finance"""
    return yf.download(tickers, start=start_date, end=end_date)['Adj Close']

def calculate_cumulative_gains(data):
    """Calculate cumulative daily gains"""
    return data.pct_change().add(1).cumprod().subtract(1).multiply(100)

def create_line_plot(data, ticker1, ticker2):
    """Create a line plot for cumulative gains"""
    plt.figure(figsize=(10, 6))
    data.plot()
    plt.title(f'Cumulative YTD Stock Gains for {ticker1} and {ticker2}')
    plt.ylabel('Gain %')
    plt.xlabel('Date')
    plt.grid(True)
    filename = 'images/ytd_stock_gains.png'
    plt.savefig('static/' + filename)
    return filename

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ticker1 = request.form.get("first")
        ticker2 = request.form.get("second")
        tickers = [ticker1, ticker2]
        start_date = '2024-01-01'
        end_date = '2024-06-16'

        data = fetch_stock_data(tickers, start_date, end_date)
        daily_gains = calculate_cumulative_gains(data)
        filename = create_line_plot(daily_gains, ticker1, ticker2)
        return render_template("graph.html", graph=filename)
    else:
        return render_template("index.html")
