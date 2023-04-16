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
    
    html.Div([html.H3(children='Vitoria - Informacoes de Mercado Imobiliario'),]),

    # html.Div(children='''
    #     This is Dash running on Azure App Service.
    # '''),
    
    dbc.Row([
        dbc.Col(html.H6("Selecione o Bairro"),),
        dbc.Col(html.H6("Selecione Quartos"),),
        dbc.Col(html.H6("Numero de imoveis"),),
    ]),
    
    
    dbc.Row([dbc.Col(
        html.Div([
        dcc.Dropdown(id='my-input',
                    options=df['bairro'].unique(),
                    multi=False,
                    ),

        ]),),
        dbc.Col(    dcc.Dropdown(id='my-input2',
                    options=df['bedrooms'].unique(),
                    multi=False,
                    ),),
        dbc.Col(html.Div(id='my-output'),),
        ]),
    
    dbc.Row(html.H1(' ')),
    
    dbc.Row(dbc.Col(html.Div(dcc.Graph(id='box1'),))),
    dbc.Row(html.H1('')),
    dbc.Row(dbc.Col(html.Div(dcc.Graph(id='box2'),))),
        dbc.Row(html.H1('')),
    dbc.Row(dbc.Col(html.Div(dcc.Graph(id='box3'),))),
], style={"padding": "15px"})



# @app.callback(
#     dash.dependencies.Output(component_id='my-output', component_property='children'),
#     [dash.dependencies.Input(component_id='my-input', component_property='value')]
# )
# def update_output_div(input_value):
#     return 'Saída: {}'.format(input_value)

@app.callback(
    dash.dependencies.Output('box1', 'figure'),
    dash.dependencies.Output('box2', 'figure'),
    dash.dependencies.Output('box3', 'figure'),
    dash.dependencies. Output('my-output', 'children'),
    [dash.dependencies.Input('my-input', 'value'),
     dash.dependencies.Input('my-input2', 'value'),])
def update_figure(bairro, bedrooms):
    
    if bairro==None and bedrooms==None:
        filtered_df = df
        n_imoveis = filtered_df.shape[0]
    elif bairro==None and bedrooms!=None:
        filtered_df = df[df['bedrooms'] == bedrooms]
        n_imoveis = filtered_df.shape[0]
    elif bairro!=None and bedrooms==None:
        filtered_df = df[df['bairro'] == bairro]
        n_imoveis = filtered_df.shape[0]
    elif bairro!=None and bedrooms!=None:
        filtered_df = df[(df['bairro'] == bairro) & (df['bedrooms'] == bedrooms)]
        n_imoveis = filtered_df.shape[0]
    
    fig = px.box(filtered_df, y='price', x='bedrooms',)
    fig.update(layout_yaxis_range = [0,10e6])
    fig.update(layout_xaxis_range = [0,6.5])
    fig.update_layout(
        title='Numero de Quartos',
        xaxis_title="Quartos",
        yaxis_title="Preço (R$)",
        paper_bgcolor="LightSteelBlue",
        font=dict(size=18,),
        transition_duration=500
    )
    

    fig2 = px.box(filtered_df, y='price', x='vacancies',)
    fig2.update(layout_yaxis_range = [0,15e6],)
    fig2.update(layout_xaxis_range = [0,5.5])
    fig2.update_layout(
        title='Vagas de Garagem',
        xaxis_title="Vagas de Garagem",
        yaxis_title="Preço (R$)",
        paper_bgcolor="LightSteelBlue",
        font=dict(size=18,),
        transition_duration=500
    )
    
    fig3 = px.box(filtered_df, y='condo_fee', x='bedrooms',)
    fig3.update(layout_yaxis_range = [0,5e3],)
    fig3.update(layout_xaxis_range = [0,5.5])
    fig3.update_layout(
        title='Condoominio',
        xaxis_title="Quartos",
        yaxis_title="Condominio (R$)",
        paper_bgcolor="LightSteelBlue",
        font=dict(size=18,),
        transition_duration=500
    )

    # fig.update_layout(transition_duration=500)

    return fig, fig2, fig3, n_imoveis

#%%
server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)
    
    