import sqlite3
import plotly.graph_objs as go
import plotly.offline as pyo
import time
import webbrowser

def fetch_opportunities(db_name):
    """
    Fetch arbitrage opportunities from the database.

    Parameters:
        db_name (str): The name of the database.

    Returns:
        list: A list of arbitrage opportunities.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute('''SELECT symbol, base_currency, quote_currency, source_exchange, target_exchange, 
                                 source_price, target_price, source_fee, target_fee, volume, timestamp 
                          FROM arbitrage_opportunities''')
        opportunities = cursor.fetchall()
    except sqlite3.OperationalError as e:
        if 'no such table' in str(e):
            opportunities = []
        else:
            raise
    finally:
        conn.close()
    
    return opportunities

def visualize_opportunities(db_name):
    """
    Visualize arbitrage opportunities stored in the database using Plotly.

    Parameters:
        db_name (str): The name of the database.
    """
    html_file = 'arbitrage_opportunities.html'
    first_run = True

    while True:
        opportunities = fetch_opportunities(db_name)

        if opportunities:
            symbols = []
            source_exchanges = []
            target_exchanges = []
            source_prices = []
            target_prices = []

            for opportunity in opportunities:
                symbols.append(opportunity[0])
                source_exchanges.append(opportunity[3])
                target_exchanges.append(opportunity[4])
                source_prices.append(opportunity[5])
                target_prices.append(opportunity[6])

            # Create a bar chart to visualize the prices
            fig = go.Figure()

            fig.add_trace(go.Bar(
                name='Source Price',
                x=symbols,
                y=source_prices,
                text=source_exchanges,
                textposition='auto'
            ))

            fig.add_trace(go.Bar(
                name='Target Price',
                x=symbols,
                y=target_prices,
                text=target_exchanges,
                textposition='auto'
            ))

            # Update the layout
            fig.update_layout(
                title='Arbitrage Opportunities',
                xaxis_title='Symbol',
                yaxis_title='Price',
                barmode='group'
            )

            # Save the plot to an HTML file
            pyo.plot(fig, filename=html_file, auto_open=False)

            # Open or refresh the plot in the browser
            if first_run:
                webbrowser.open_new_tab(html_file)
                first_run = False
            else:
                webbrowser.open(html_file, new=0)

        else:
            print("No arbitrage opportunities found.")

        # Fetch fresh data every minute
        time.sleep(60)

if __name__ == "__main__":
    visualize_opportunities('arbitrage.db')
