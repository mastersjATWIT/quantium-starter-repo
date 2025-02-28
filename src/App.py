import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from datetime import datetime
import numpy as np

# Load the processed data
df = pd.read_csv('pink_morsel_sales.csv')

# Convert date string to datetime object
df['date'] = pd.to_datetime(df['date'])

# Sort by date
df = df.sort_values('date')

# Create a new DataFrame with daily total sales
daily_sales = df.groupby('date')['sales'].sum().reset_index()

# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    # Header
    html.H1("Soul Foods Pink Morsel Sales Analysis", 
            style={'textAlign': 'center', 'color': '#E91E63', 'marginBottom': 30}),
    
    html.Div([
        # Description with price increase information
        html.Div([
            html.H3("Sales Before and After Price Increase (January 15, 2021)", 
                   style={'color': '#555', 'marginBottom': 20}),
            html.P("This dashboard visualizes Pink Morsel sales data to analyze the impact of the price increase.",
                  style={'marginBottom': 20})
        ], style={'marginBottom': 20}),
        
        # Line chart
        dcc.Graph(
            id='sales-line-chart',
            figure=px.line(
                daily_sales, 
                x='date', 
                y='sales',
                title='Daily Pink Morsel Sales',
                labels={'date': 'Date', 'sales': 'Sales ($)'},
                template='plotly_white'
            ).update_layout(
                # Add a vertical line to indicate the price increase date
                shapes=[
                    dict(
                        type="line",
                        xref="x",
                        yref="paper",
                        x0="2021-01-15",
                        y0=0,
                        x1="2021-01-15",
                        y1=1,
                        line=dict(
                            color="red",
                            width=2,
                            dash="dash",
                        )
                    )
                ],
                annotations=[
                    dict(
                        x="2021-01-15",
                        y=1.05,
                        xref="x",
                        yref="paper",
                        text="Price Increase",
                        showarrow=False,
                        font=dict(color="red")
                    )
                ]
            )
        ),
        
        # Additional insights section
        html.Div([
            html.H3("Analysis Insights", style={'marginTop': 30, 'marginBottom': 15}),
            
            # Calculate and display average sales before and after
            html.Div(id='sales-comparison')
        ])
    ], style={'width': '80%', 'margin': 'auto'})
])

# Add callback to compute and display insights
@app.callback(
    dash.dependencies.Output('sales-comparison', 'children'),
    dash.dependencies.Input('sales-line-chart', 'figure')
)
def update_sales_comparison(_):
    # Get the price increase date
    price_increase_date = pd.to_datetime('2021-01-15')
    
    # Calculate average daily sales before and after price increase
    sales_before = daily_sales[daily_sales['date'] < price_increase_date]['sales'].mean()
    sales_after = daily_sales[daily_sales['date'] >= price_increase_date]['sales'].mean()
    
    # Calculate percentage change
    pct_change = ((sales_after - sales_before) / sales_before) * 100
    
    # Determine if sales increased or decreased
    change_direction = "increased" if pct_change > 0 else "decreased"
    
    return [
        html.P([
            html.Strong("Average Daily Sales Before Price Increase: "), 
            f"${sales_before:.2f}"
        ]),
        html.P([
            html.Strong("Average Daily Sales After Price Increase: "), 
            f"${sales_after:.2f}"
        ]),
        html.P([
            html.Strong("Percentage Change: "), 
            f"{pct_change:.2f}% {change_direction}"
        ]),
        html.P([
            html.Strong("Conclusion: "), 
            f"Sales {'were higher' if sales_after > sales_before else 'were lower'} after the price increase on January 15, 2021."
        ], style={'marginTop': 15, 'fontSize': '18px', 'fontWeight': 'bold'})
    ]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)