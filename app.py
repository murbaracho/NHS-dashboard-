import dash
from dash import html
import dash_bootstrap_components as dbc

# Initialize the app with page support and LUX Bootstrap theme
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

app.title = "NHS Appointments Intelligence Hub"

# Navbar
navbar = dbc.NavbarSimple(
    brand="NHS Appointments Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Utilisation", href="/utilisation")),
        dbc.NavItem(dbc.NavLink("Missed", href="/missed")),
        dbc.NavItem(dbc.NavLink("ICB Performance", href="/icb-performance")),
        dbc.NavItem(dbc.NavLink("Twitter", href="/twitter")),

    ],
    className="mb-4"
)

# Layout
app.layout = dbc.Container([
    navbar,
    dash.page_container,
    html.Hr(),
    html.Footer("Created for NHS Stakeholders | LSE Data Analytics", className="text-center text-muted my-3")
], fluid=True)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

