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

# Function to fetch outliers from database
def fetch_outliers_grouped(cursor):
    try:
        cursor.execute('SELECT symbol, source_exchange, target_exchange, source_price, target_price, percentage, timestamp FROM outliers ORDER BY timestamp DESC')
        outliers = cursor.fetchall()

        # Group outliers by timestamp
        grouped_outliers = {}
        for out in outliers:
            symbol, source_exchange, target_exchange, source_price, target_price, percentage, timestamp = out
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

            # Round timestamp to nearest minute for clustering
            rounded_timestamp = timestamp.replace(second=0, microsecond=0)
            key = rounded_timestamp.strftime('%Y-%m-%d %H:%M:%S')

            if key in grouped_outliers:
                grouped_outliers[key].append(out)
            else:
                grouped_outliers[key] = [out]

        return grouped_outliers
    except Exception as e:
        logger.error(f"Error fetching grouped outliers: {e}")
        return {}

# Function to plot data from database
def plot_data(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    fig = go.FigureWidget()

    def update_table():
        try:
            grouped_opportunities = fetch_opportunities_grouped(cursor)
            grouped_outliers = fetch_outliers_grouped(cursor)

            fig.data = []

            if not grouped_opportunities and not grouped_outliers:
                logger.info("No data available to plot.")
                return

            # Limit to displaying up to 5 tables (clusters)
            num_clusters = min(len(grouped_opportunities) + len(grouped_outliers), 5)
            i = 0

            # Add opportunities to the plot
            for timestamp_str, opportunities in grouped_opportunities.items():
                if i >= num_clusters:
                    break
                try:
                    df_opp = pd.DataFrame(opportunities, columns=['symbol', 'source_exchange', 'target_exchange', 'source_price', 'target_price', 'percentage', 'timestamp'])
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    
                    fig.add_annotation(
                        text=f"<b>Opportunities at {timestamp}</b>",
                        xref="paper", yref="paper",
                        x=0.5, y=1.05 - 0.2 * i,
                        showarrow=False,
                        font=dict(size=14),
                        align="center"
                    )

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
                    i += 1

                except Exception as e:
                    logger.error(f"Error processing opportunities: {e}", exc_info=True)

            # Add outliers to the plot
            for timestamp_str, outliers in grouped_outliers.items():
                if i >= num_clusters:
                    break
                try:
                    df_out = pd.DataFrame(outliers, columns=['symbol', 'source_exchange', 'target_exchange', 'source_price', 'target_price', 'percentage', 'timestamp'])
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    
                    fig.add_annotation(
                        text=f"<b>Outliers at {timestamp}</b>",
                        xref="paper", yref="paper",
                        x=0.5, y=1.05 - 0.2 * i,
                        showarrow=False,
                        font=dict(size=14),
                        align="center"
                    )

                    fig.add_trace(
                        go.Table(
                            header=dict(values=["Symbol", "Exchange", "Source Price", "Target Price", "Percentage Difference"],
                                        fill_color='lightyellow',
                                        align='left',
                                        font=dict(size=14)),
                            cells=dict(values=[df_out.symbol, df_out.source_exchange, df_out.source_price, df_out.target_price, df_out.percentage],
                                        fill_color='lightgrey',
                                        align='left',
                                        font=dict(size=12)),
                            domain={'row': i, 'column': 0}
                        )
                    )
                    i += 1

                except Exception as e:
                    logger.error(f"Error processing outliers: {e}", exc_info=True)

            fig.update_layout(
                title='Clustered Arbitrage Opportunities and Outliers',
                margin=dict(l=10, r=10, t=40, b=10),
                grid={'rows': num_clusters, 'columns': 1}
            )

            fig.show()

        except Exception as e:
            logger.error(f"Error updating table: {e}", exc_info=True)  # Log full traceback for debugging

    update_table()

    while True:
        update_table()
        time.sleep(360)

if __name__ == '__main__':
    plot_data('arbitrage.db')
