import sqlite3
import pandas as pd
import time
import plotly.graph_objects as go
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to fetch opportunities from database
def fetch_opportunities_grouped(cursor):
    try:
        cursor.execute('SELECT symbol, source_exchange, target_exchange, source_price, target_price, percentage, timestamp FROM opportunities ORDER BY timestamp DESC')
        opportunities = cursor.fetchall()

        # Group opportunities by timestamp
        grouped_opportunities = {}
        for opp in opportunities:
            symbol, source_exchange, target_exchange, source_price, target_price, percentage, timestamp = opp
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

            # Round timestamp to nearest minute for clustering
            rounded_timestamp = timestamp.replace(second=0, microsecond=0)
            key = rounded_timestamp.strftime('%Y-%m-%d %H:%M:%S')

            if key in grouped_opportunities:
                grouped_opportunities[key].append(opp)
            else:
                grouped_opportunities[key] = [opp]

        return grouped_opportunities
    except Exception as e:
        logger.error(f"Error fetching grouped opportunities: {e}")
        return {}

# Function to plot data from database
def plot_data(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    fig = go.FigureWidget()

    def update_table():
        try:
            grouped_opportunities = fetch_opportunities_grouped(cursor)

            fig.data = []

            if not grouped_opportunities:
                logger.info("No data available to plot.")
                return

            # Limit to displaying up to 5 tables (clusters)
            num_clusters = min(len(grouped_opportunities), 5)
            for i, (timestamp_str, opportunities) in enumerate(grouped_opportunities.items()):
                try:
                    # Construct DataFrame with the correct columns
                    df_opp = pd.DataFrame(opportunities, columns=['symbol', 'source_exchange', 'target_exchange', 'source_price', 'target_price', 'percentage', 'timestamp'])

                    # Validate columns and adjust if necessary
                    expected_columns = ['symbol', 'source_exchange', 'target_exchange', 'source_price', 'target_price', 'percentage']
                    if not all(col in df_opp.columns for col in expected_columns):
                        logger.error(f"DataFrame columns do not match expected columns: {df_opp.columns}")
                        continue

                    # Format timestamp for display
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

                    # Add a text annotation above each table
                    fig.add_annotation(
                        text=f"<b>Opportunities found at {timestamp}</b>",
                        xref="paper", yref="paper",
                        x=0.5, y=1.05,
                        showarrow=False,
                        font=dict(size=14),
                        align="center"
                    )

                    # Add table trace
                    fig.add_trace(
                        go.Table(
                            header=dict(values=["Symbol", "Buy From", "Source Price", "Sell To", "Target Price", "Percentage Difference"],
                                        fill_color='paleturquoise',
                                        align='left',
                                        font=dict(size=14)),
                            cells=dict(values=[df_opp.symbol, df_opp.source_exchange, df_opp.source_price, df_opp.target_exchange, df_opp.target_price, df_opp.percentage],
                                        fill_color='lavender',
                                        align='left',
                                        font=dict(size=12)),
                            domain={'row': i, 'column': 0}
                        )
                    )

                    # Break if we've added 5 clusters
                    if i + 1 >= num_clusters:
                        break

                except Exception as e:
                    logger.error(f"Error processing opportunities: {e}", exc_info=True)

            fig.update_layout(
                title='Clustered Arbitrage Opportunities',
                margin=dict(l=10, r=10, t=40, b=10),
                grid={'rows': num_clusters, 'columns': 1}
            )

            fig.show()

        except Exception as e:
            logger.error(f"Error updating table: {e}", exc_info=True)  # Log full traceback for debugging

    update_table()

    while True:
        update_table()
        time.sleep(120)

if __name__ == '__main__':
    plot_data('arbitrage.db')
