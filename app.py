#%%

import dash
import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

import os
import pandas as pd

import plotly.express as px

#%%
dir_path = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(os.path.join(dir_path, 'data', 'df_real_state.csv'))


fig = px.box(df, y='price', x='bedrooms',)
fig.update(layout_yaxis_range = [0,10e6])
fig.update(layout_xaxis_range = [0,6.5])
fig.update_layout(
    # height=1000,
    paper_bgcolor="LightSteelBlue",
)
#%%


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
application = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)


app.layout = html.Div(children=[
    navbar,
    
    html.H1(children='Vitoria - Real State'),

    html.Div(children='''ß
        This is Dash running on Azure App Service.
    '''),
    

    dcc.Graph(figure=fig),
])



#%%
server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)
    
    