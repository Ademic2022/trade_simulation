import plotly.express as px
import datetime

def generate_profit_loss_graph(db, trader_name):
    data = db[trader_name].find()

    """Process the data"""
    timestamps = []
    balances = []

    for record in data:
        timestamp_seconds = record["timestamp"]
        timestamp_datetime = datetime.datetime.fromtimestamp(timestamp_seconds)
        formatted_timestamp = timestamp_datetime.strftime('%Y-%m-%d %H:%M:%S')

        timestamps.append(formatted_timestamp)
        balances.append(record["balance"])

    """Create the Plotly graph"""
    fig = px.line(x=timestamps, y=balances, labels={'x': 'Timestamp', 'y': 'Balance'}, title='Profit/Loss vs. Time')

    """Convert the Plotly graph to an HTML div"""
    plot_div = fig.to_html(full_html=False)

    return plot_div

    
