import sqlite3
import pandas as pd
import time
import plotly.graph_objects as go

def fetch_opportunities(cursor):
    # Fetch data from the opportunities table
    cursor.execute('SELECT symbol, source_exchange, target_exchange, source_price, target_price, percentage FROM opportunities')
    rows = cursor.fetchall()
    return rows

def plot_opportunities(db_name):
    # Connect to the database
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Initialize an empty figure widget
    fig = go.FigureWidget()

    # Function to update the table
    def update_table():
        rows = fetch_opportunities(cursor)

        if not rows:
            print("No data available to plot.")
            return

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=['symbol', 'source_exchange', 'target_exchange', 'source_price', 'target_price', 'percentage'])

        # Sort DataFrame by percentage and select top N opportunities
        top_n = 10  # Show top 10 opportunities
        df = df.sort_values('percentage', ascending=False).head(top_n)

        # Create a table
        fig.data = []

        fig.add_trace(
            go.Table(
                header=dict(
                    values=["Symbol", "Buy From", "Source Price", "Sell To", "Target Price", "Percentage Difference"],
                    fill_color='paleturquoise',
                    align='left',
                    font=dict(size=14)
                ),
                cells=dict(
                    values=[df.symbol, df.source_exchange, df.source_price, df.target_exchange, df.target_price, df.percentage],
                    fill_color='lavender',
                    align='left',
                    font=dict(size=12)
                )
            )
        )

        fig.update_layout(
            title='Top Arbitrage Opportunities',
            margin=dict(l=10, r=10, t=40, b=10)
        )

    # Initial table
    update_table()

    # Display the figure
    fig.show()

    # Continuous update every minute
    while True:
        time.sleep(60)
        update_table()

if __name__ == '__main__':
    plot_opportunities('arbitrage.db')
