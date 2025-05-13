import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import os

# Register page
dash.register_page(__name__, path="/missed", name="Missed Appointments")

# Load data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "../data/appointments_regional.csv")
df = pd.read_csv(file_path)
df['appointment_month'] = pd.to_datetime(df['appointment_month'])

# Filter for missed appointments
missed = df[df['appointment_status'] == 'DNA']

# Missed over time
missed_monthly = missed.groupby(missed['appointment_month'].dt.to_period('M'))['count_of_appointments'].sum().reset_index()
missed_monthly['appointment_month'] = missed_monthly['appointment_month'].dt.to_timestamp()
fig_missed = px.line(missed_monthly, x='appointment_month', y='count_of_appointments',
                     title="Missed Appointments Over Time",
                     labels={"appointment_month": "Month", "count_of_appointments": "Missed Appointments"})

# Missed by region
missed_by_region = missed.groupby('icb_ons_code')['count_of_appointments'].sum().reset_index().sort_values(by='count_of_appointments', ascending=False).head(10)
fig_region = px.bar(missed_by_region, x='count_of_appointments', y='icb_ons_code', orientation='h',
                    title="Top 10 Regions by Missed Appointments",
                    labels={"count_of_appointments": "Missed Appointments", "icb_ons_code": "ICB Region Code"})

# Layout
layout = html.Div([
    html.H2("Missed Appointments Overview"),
    dcc.Graph(figure=fig_missed),
    dcc.Graph(figure=fig_region)
])

