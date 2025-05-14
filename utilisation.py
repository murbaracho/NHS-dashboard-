import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import os

# Register page
dash.register_page(__name__, path="/utilisation", name="Utilisation")

# Load data using project-relative path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "appointments_regional.csv")

# Read and format data
df = pd.read_csv(file_path)
df['appointment_month'] = pd.to_datetime(df['appointment_month'])

# ----- Appointments by Mode -----
appointments_by_mode = df.groupby(['appointment_month', 'appointment_mode'])['count_of_appointments'].sum().reset_index()
mode_plot = px.line(
    appointments_by_mode,
    x='appointment_month',
    y='count_of_appointments',
    color='appointment_mode',
    title="📞 Appointments Over Time by Mode",
    labels={'appointment_month': 'Month', 'count_of_appointments': 'Appointments'}
)
mode_plot.update_layout(margin=dict(t=50, l=40, r=40, b=40))

# ----- Appointment Status Over Time -----
status_trend = df.groupby(['appointment_month', 'appointment_status'])['count_of_appointments'].sum().reset_index()
status_plot = px.line(
    status_trend,
    x='appointment_month',
    y='count_of_appointments',
    color='appointment_status',
    title='✅ Appointments Over Time by Status',
    labels={'appointment_month': 'Month', 'count_of_appointments': 'Appointments'}
)
status_plot.update_layout(margin=dict(t=50, l=40, r=40, b=40))

# ----- Appointments by Healthcare Professional Type -----
hcp_trend = df.groupby(['appointment_month', 'hcp_type'])['count_of_appointments'].sum().reset_index()
hcp_plot = px.line(
    hcp_trend,
    x='appointment_month',
    y='count_of_appointments',
    color='hcp_type',
    title='🩺 Appointments by Healthcare Professional Type',
    labels={'appointment_month': 'Month', 'count_of_appointments': 'Appointments'}
)
hcp_plot.update_layout(margin=dict(t=50, l=40, r=40, b=40))

# ----- Appointments by Lead Time -----
lead_time = df.groupby(['appointment_month', 'time_between_book_and_appointment'])['count_of_appointments'].sum().reset_index()
lead_plot = px.line(
    lead_time,
    x='appointment_month',
    y='count_of_appointments',
    color='time_between_book_and_appointment',
    title='⏱ Appointments by Time Between Booking and Appointment',
    labels={'appointment_month': 'Month', 'count_of_appointments': 'Appointments'}
)
lead_plot.update_layout(margin=dict(t=50, l=40, r=40, b=40))

# ----- Layout -----
layout = html.Div([
    html.H2("📈 Utilisation Trends", className='my-4'),
    html.P("This section explores how NHS appointments were delivered over time, segmented by mode of delivery, staff type, attendance status, and booking lead time."),
    
    dcc.Graph(figure=mode_plot),
    dcc.Graph(figure=status_plot),
    dcc.Graph(figure=hcp_plot),
    dcc.Graph(figure=lead_plot)
])

