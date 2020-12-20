from yahooquery import Ticker
from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///port.db'
db = SQLAlchemy(app)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return f'<Ticker {self.id}'

@app.route('/', methods=['POST', 'GET'])
def port_dashboard():
    if request.method == 'POST':
        form_content = request.form['ticker']
        new_ticker = Portfolio(ticker=form_content)
        
        try:
            db.session.add(new_ticker)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your ticker'
    else:
        tickers = Portfolio.query.order_by(Portfolio.id).all()
        return render_template('home.html', tickers=tickers)

@app.route('/ticker/<string:ticker>')
def render_ticker(ticker):
    pl, price = get_indexes(f'{ticker}.SA')
    return render_template('ticker.html', pl=pl, price=price)

@app.route('/delete/<int:id>')
def delete(id):
    ticker_to_delete = Portfolio.query.get_or_404(id)
    try:
        db.session.delete(ticker_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting this record'

def get_indexes(ticker):
    port = Ticker(ticker)
    financial_data = port.financial_data[ticker]
    earnings = port.earnings[ticker]

    total_shares = financial_data['totalRevenue'] // financial_data['revenuePerShare']
    current_price = financial_data['currentPrice']
    earning_per_share = earnings['financialsChart']['yearly'][-1]['earnings']/total_shares
    price_earning = current_price/earning_per_share
    return price_earning, current_price

if __name__ == '__main__':
    # tickers = ['TAEE3.SA', 'BBSE3.SA', 'ENBR3.SA', 'KLBN3.SA', 'FLRY3.SA', 'EGIE3.SA', 'ITSA4.SA', 'WEGE3.SA', 'WIZS3.SA']
    app.run(debug=True)





