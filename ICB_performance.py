import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import os

# Register this as a Dash page
dash.register_page(__name__, path="/icb-performance", name="ICB Performance")

# Get absolute path to the data file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "appointments_regional.csv")
lookup_path = os.path.join(BASE_DIR, "data", "NHS_England_Regions_July_2022_EN_BFC.csv")

# Load appointment data
appointments = pd.read_csv(file_path)
appointments['appointment_month'] = pd.to_datetime(appointments['appointment_month'])

# Aggregate total appointments per ICB
icb_summary = (
    appointments.groupby('icb_ons_code')['count_of_appointments']
    .sum()
    .reset_index()
    .sort_values(by='count_of_appointments', ascending=False)
)

# Try to match ICB codes with names
if os.path.exists(lookup_path):
    icb_lookup = pd.read_csv(lookup_path)
    if 'ICB Code' in icb_lookup.columns and 'ICB Name' in icb_lookup.columns:
        icb_summary = icb_summary.merge(
            icb_lookup[['ICB Code', 'ICB Name']], 
            left_on='icb_ons_code', 
            right_on='ICB Code', 
            how='left'
        )
        icb_summary['Region'] = icb_summary['ICB Name'].fillna(icb_summary['icb_ons_code'])
    else:
        icb_summary['Region'] = icb_summary['icb_ons_code']
else:
    icb_summary['Region'] = icb_summary['icb_ons_code']

# Top 20 bar plot
fig = px.bar(
    icb_summary.head(20),
    x='count_of_appointments',
    y='Region',
    orientation='h',
    title='Top 20 ICBs by Appointment Volume',
    labels={
        'count_of_appointments': 'Total Appointments',
        'Region': 'ICB Region'
    },
    height=600
)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})

# Layout
layout = html.Div([
    html.H2("📍 ICB Performance Benchmarking", className='my-4'),
    html.P("This section ranks Integrated Care Boards (ICBs) by the total number of appointments over the analysis period."),
    dcc.Graph(figure=fig),
    html.P("📝 This helps planners and regional managers understand where demand is highest across the NHS.")
])
