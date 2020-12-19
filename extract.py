from yahooquery import Ticker
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def port_dashboard():
    return render_template('home.html', pl='12', price='3232')

@app.route('/ticker')
def render_ticker():
    return 'Ticker page'

def get_indexes(ticker):
    port = Ticker(ticker)
    financial_data = port.financial_data[ticker]
    earnings = port.earnings[ticker]

    total_shares = financial_data['totalRevenue'] // financial_data['revenuePerShare']
    current_price = financial_data['currentPrice']
    earning_per_share = earnings['financialsChart']['yearly'][-1]['earnings']/total_shares
    price_earning = current_price/earning_per_share
    print(price_earning)

if __name__ == '__main__':
    #app.run()

    tickers = ['TAEE3.SA', 'BBSE3.SA', 'ENBR3.SA', 'KLBN3.SA', 'FLRY3.SA', 'EGIE3.SA', 'ITSA4.SA', 'WEGE3.SA', 'WIZS3.SA']

    for ticker in tickers:
        get_indexes(ticker)




