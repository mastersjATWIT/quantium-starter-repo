import pytest
from dash import Dash
from dash.testing.application_runners import RenderLocalRunner
from dash.testing.application_runners.runners import WebdriverRunner

# Import the main application
from App import dash_app  # Replace with the actual import path of your Dash app

# Fixture to set up the test runner
@pytest.fixture
def dash_duo(dash_duo):
    return dash_duo

# Test 1: Check if the header is present
def test_header_exists(dash_duo):
    # Serve the app
    dash_duo.start_server(dash_app)
    
    # Find the header element
    header = dash_duo.find_element("#header")
    
    # Assert that the header exists and has the correct text
    assert header is not None
    assert header.text == "Pink Morsel Visualizer"

# Test 2: Check if the visualization is present
def test_visualization_exists(dash_duo):
    # Serve the app
    dash_duo.start_server(dash_app)
    
    # Find the visualization graph element
    visualization = dash_duo.find_element("#visualization")
    
    # Assert that the visualization exists
    assert visualization is not None

# Test 3: Check if the region picker is present
def test_region_picker_exists(dash_duo):
    # Serve the app
    dash_duo.start_server(dash_app)
    
    # Find the region picker element
    region_picker = dash_duo.find_element("#region_picker")
    
    # Assert that the region picker exists
    assert region_picker is not None
    
    # Optional: Check if all expected radio items are present
    radio_items = dash_duo.find_elements("input[type='radio']")
    expected_regions = ["north", "east", "south", "west", "all"]
    assert len(radio_items) == len(expected_regions)