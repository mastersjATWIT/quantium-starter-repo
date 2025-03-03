import pandas
from dash import Dash, html, dcc, Input, Output, callback
from plotly.express import line

# the path to the formatted data file
DATA_PATH = "./formatted_data.csv"

# load in data
data = pandas.read_csv(DATA_PATH)
data = data.sort_values(by="date")

# initialize dash with external stylesheets
dash_app = Dash(__name__)

# Define the app layout with added region filter
dash_app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "Pink Morsel Visualizer",
                    id="header"
                ),
                html.P(
                    "Explore sales performance across different regions",
                    className="subtitle"
                )
            ],
            className="header-container"
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Filter by Region"),
                        dcc.RadioItems(
                            id='region-filter',
                            options=[
                                {'label': 'All Regions', 'value': 'all'},
                                {'label': 'North', 'value': 'north'},
                                {'label': 'East', 'value': 'east'},
                                {'label': 'South', 'value': 'south'},
                                {'label': 'West', 'value': 'west'}
                            ],
                            value='all',
                            className="radio-items"
                        )
                    ],
                    className="filter-container"
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="visualization"
                        )
                    ],
                    className="chart-container"
                )
            ],
            className="content-container"
        )
    ],
    className="main-container"
)

# Callback to update the chart based on the selected region
@callback(
    Output('visualization', 'figure'),
    Input('region-filter', 'value')
)
def update_figure(selected_region):
    if selected_region == 'all':
        filtered_data = data
        title = "Pink Morsel Sales - All Regions"
    else:
        filtered_data = data[data['region'] == selected_region]
        title = f"Pink Morsel Sales - {selected_region.capitalize()} Region"
    
    fig = line(
        filtered_data, 
        x="date", 
        y="sales", 
        title=title,
        color_discrete_sequence=['#ff69b4'],  # Pink color for the line
        template="plotly_white"
    )
    
    # Customize the figure layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="#333333"
        ),
        title=dict(
            font=dict(
                size=20,
                color="#333333"
            )
        ),
        xaxis=dict(
            title="Date",
            tickfont=dict(size=12),
            gridcolor="#f0f0f0"
        ),
        yaxis=dict(
            title="Sales",
            tickfont=dict(size=12),
            gridcolor="#f0f0f0"
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="closest"
    )
    
    return fig

# Add custom CSS
dash_app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Pink Morsel Visualizer</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f9f1f5;
                color: #333333;
            }
            
            .main-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header-container {
                text-align: center;
                margin-bottom: 30px;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-bottom: 4px solid #ff69b4;
            }
            
            #header {
                margin: 0;
                color: #ff69b4;
                font-size: 36px;
                letter-spacing: 1px;
            }
            
            .subtitle {
                color: #888;
                font-size: 16px;
                margin-top: 5px;
            }
            
            .content-container {
                display: flex;
                flex-direction: row;
                flex-wrap: wrap;
                gap: 20px;
            }
            
            .filter-container {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                flex: 1;
                min-width: 200px;
            }
            
            .chart-container {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                flex: 3;
                min-width: 300px;
            }
            
            .radio-items {
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 15px;
            }
            
            .radio-items label {
                padding: 8px 12px;
                border-radius: 5px;
                transition: background-color 0.2s;
                cursor: pointer;
            }
            
            .radio-items label:hover {
                background-color: #ffe6f2;
            }
            
            h3 {
                margin-top: 0;
                color: #ff69b4;
                border-bottom: 2px solid #ffd1e6;
                padding-bottom: 10px;
            }
            
            @media (max-width: 768px) {
                .content-container {
                    flex-direction: column;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# this is only true if the module is executed as the program entrypoint
if __name__ == '__main__':
    dash_app.run_server(debug=True)