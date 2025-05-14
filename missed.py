import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import os

# Register this as a Dash page
dash.register_page(__name__, path="/missed", name="Missed Appointments")

# Resolve data paths relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "appointments_regional.csv")
lookup_path = os.path.join(BASE_DIR, "data", "icb_locations.csv")

# Load data
df = pd.read_csv(file_path)
df['appointment_month'] = pd.to_datetime(df['appointment_month'])

# Filter for DNA (Did Not Attend) records
missed = df[df['appointment_status'] == 'DNA']

# --- Trend Over Time ---
missed_monthly = (
    missed.groupby(missed['appointment_month'].dt.to_period('M'))['count_of_appointments']
    .sum()
    .reset_index()
)
missed_monthly['appointment_month'] = missed_monthly['appointment_month'].dt.to_timestamp()

fig_missed = px.line(
    missed_monthly,
    x='appointment_month',
    y='count_of_appointments',
    title="📉 Missed Appointments Over Time",
    labels={"appointment_month": "Month", "count_of_appointments": "Missed Appointments"},
    markers=True
)

fig_missed.update_layout(
    xaxis_title="Month",
    yaxis_title="Missed Appointments",
    margin=dict(t=50, l=40, r=40, b=40)
)

# --- Missed Appointments by Region ---
missed_by_region = (
    missed.groupby('icb_ons_code')['count_of_appointments']
    .sum()
    .reset_index()
    .sort_values(by='count_of_appointments', ascending=False)
    .head(10)
)

# Optional: Merge with region names if available
if os.path.exists(lookup_path):
    icb_lookup = pd.read_csv(lookup_path)
    if 'ICB Code' in icb_lookup.columns and 'ICB Name' in icb_lookup.columns:
        missed_by_region = missed_by_region.merge(
            icb_lookup[['ICB Code', 'ICB Name']],
            left_on='icb_ons_code',
            right_on='ICB Code',
            how='left'
        )
        missed_by_region['Region'] = missed_by_region['ICB Name'].fillna(missed_by_region['icb_ons_code'])
    else:
        missed_by_region['Region'] = missed_by_region['icb_ons_code']
else:
    missed_by_region['Region'] = missed_by_region['icb_ons_code']

fig_region = px.bar(
    missed_by_region,
    x='count_of_appointments',
    y='Region',
    orientation='h',
    title="🏥 Top 10 ICBs by Missed Appointments",
    labels={"count_of_appointments": "Missed Appointments", "Region": "ICB Region"},
    text='count_of_appointments'
)

fig_region.update_layout(
    yaxis_title="ICB Region",
    xaxis_title="Missed Appointments",
    margin=dict(t=50, l=80, r=40, b=40)
)

# --- Page Layout ---
layout = html.Div([
    html.H2("Missed Appointments Overview", className='my-4'),
    html.P("Missed appointments (DNA) contribute to wasted resources and delayed care. This page highlights the volume and patterns of missed appointments over time and by region."),
    dcc.Graph(figure=fig_missed),
    dcc.Graph(figure=fig_region),
])


