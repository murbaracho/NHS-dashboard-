import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import os

# Register page
dash.register_page(__name__, path="/utilisation", name="Utilisation")

# Load data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "../data/appointments_regional.csv")
df = pd.read_csv(file_path)
df['appointment_month'] = pd.to_datetime(df['appointment_month'])

# Monthly appointments trend
monthly = df.groupby(df['appointment_month'].dt.to_period('M'))['count_of_appointments'].sum().reset_index()
monthly['appointment_month'] = monthly['appointment_month'].dt.to_timestamp()
fig_monthly = px.line(monthly, x='appointment_month', y='count_of_appointments',
                      title="Monthly Appointment Trends",
                      labels={"appointment_month": "Month", "count_of_appointments": "Appointments"})

# Appointment modes over time
mode_monthly = df.groupby(['appointment_month', 'appointment_mode'])['count_of_appointments'].sum().reset_index()
fig_mode = px.line(mode_monthly, x='appointment_month', y='count_of_appointments', color='appointment_mode',
                   title="Appointments by Mode Over Time",
                   labels={"appointment_month": "Month", "count_of_appointments": "Appointments"})

# Seasonal distribution
df['season'] = df['appointment_month'].dt.month % 12 // 3 + 1
season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Autumn'}
df['season_name'] = df['season'].map(season_map)
seasonal = df.groupby('season_name')['count_of_appointments'].sum().reset_index()
fig_season = px.bar(seasonal.sort_values('count_of_appointments', ascending=False),
                    x='season_name', y='count_of_appointments',
                    title="Total Appointments by Season",
                    labels={"season_name": "Season", "count_of_appointments": "Appointments"})

# Layout
layout = html.Div([
    html.H2("Utilisation Overview"),
    dcc.Graph(figure=fig_monthly),
    dcc.Graph(figure=fig_mode),
    dcc.Graph(figure=fig_season)
])
 
