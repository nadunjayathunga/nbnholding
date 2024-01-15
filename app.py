import dash
import dash_auth
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, dcc
from data import company_info
from creds import db_info,USER_MAPPING
from datetime import datetime, date
from sqlalchemy import create_engine
import pandas as pd
import sshtunnel


app = dash.Dash(name=__name__, external_stylesheets=[
    dbc.themes.PULSE], use_pages=True, title='Dashboard')
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

dash_auth.BasicAuth(app, USER_MAPPING)

header_row = dbc.Row(
    children=[
        html.H1('Corporate Dashboard', className='text-center text-primary')
    ],
    id='main-heading'
)

secondary_row = dbc.Row(
    children=[
        dbc.Col(
            [
                dcc.Dropdown(
                    options=[
                        {'label': i['data']['long_name'], 'value': i['data']['database']} for i in company_info
                    ],
                    value='nadunjayathunga$elite_security',
                    id='company-name',
                    className='mt-1',
                    optionHeight=35,
                    clearable=False
                )
            ], width={'size': 2}

        ),
        dbc.Col(
            [
                dcc.DatePickerRange(
                    id='dt-pkr-range',
                    min_date_allowed=None,
                    max_date_allowed=None,
                    updatemode='bothdates',
                    start_date=None,
                    end_date=None,  # dt(2023, 8, 31),
                    disabled=False,
                )
            ], width={'size': 3},
            style={'margin-top': 2},
        ),
        dbc.Tooltip('The date range need to be first day and last day of any given period',
                    target='dt-pkr-range',
                    placement='top'),
        dbc.Col(
            [
                dbc.Nav(
                    children=[], vertical=False, pills=True, justified=True, id='menu-items'
                )
            ], width={'size': 7},
        )
    ]
)


def check_date_format(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").date()
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format")


app.layout = html.Div(children=[
    dcc.Store(id='start-date', data={}),
    dcc.Store(id='end-date', data={}),
    dcc.Store(id='dCoAAdler', data={}),
    dcc.Store(id='fGL', data={}),
    dcc.Store(id='fBudget', data={}),
    dcc.Store(id='dEmployee', data={}),
    dcc.Store(id='dCustomers', data={}),
    dcc.Store(id='fGlJob', data={}),
    dcc.Store(id='exp_allocation', data={}),
    dcc.Store(id='dJobs', data={}),
    dcc.Store(id='database', data={}),
    header_row,
    secondary_row,
    html.Hr(),
    dash.page_container])


@app.callback(
    Output(component_id='menu-items', component_property='children'),
    [Input(component_id='company-name', component_property='value')]
)
def create_menu_item(item):
    # 'nav_links': ['Finance','Operations','Sales']
    menu_items = [i['data']['nav_links'] for i in company_info if i['data']['database'] == item]
    nav_links = []
    for item in menu_items[0]:  # Finance
        menu_item = dbc.NavLink(item.upper(),
                                href='/' if item == 'Finance' else f'/{item.lower()}',
                                active='exact', disabled=False)
        nav_links.append(menu_item)
    return nav_links


@app.callback(
    [Output(component_id='dt-pkr-range', component_property='min_date_allowed'),
     Output(component_id='dt-pkr-range',
            component_property='max_date_allowed'),
     Output(component_id='dt-pkr-range', component_property='end_date'),
     Output(component_id='dt-pkr-range', component_property='start_date')],
    [Input(component_id='company-name', component_property='value'), ]
)
def set_dates(company_db):
    with sshtunnel.SSHTunnelForwarder((db_info['SSHHOST'], 22),
                                      ssh_username=db_info['USERNAME'],
                                      ssh_password=db_info['PWDLOGIN'],
                                      remote_bind_address=(db_info['DBHOSTADDRESS'], 3306)) as tunnel:
        engine = create_engine(
            f'mysql+pymysql://{db_info["USERNAME"]}:{db_info["PWDDB"]}@{db_info["HOSTNAME"]}:{tunnel.local_bind_port}/{company_db}')
        query = 'SELECT voucher_date FROM fGL'
        df_fgl = pd.read_sql_query(query, engine)

        earliest_date = df_fgl['voucher_date'].min()
        closest_date = df_fgl['voucher_date'].max()
        current_year: str = str(date.today().year)
        cy_start_date = current_year + '-01-01'
        cy_start_date = datetime.strptime(cy_start_date, '%Y-%m-%d').date()

        return [earliest_date,
                closest_date,
                closest_date,
                cy_start_date]


@app.callback(
    [
        Output(component_id='start-date', component_property='data'),
        Output(component_id='end-date', component_property='data'),
        Output(component_id='dCoAAdler', component_property='data'),
        Output(component_id='fGL', component_property='data'),
        Output(component_id='fBudget', component_property='data'),
        Output(component_id='dEmployee', component_property='data'),
        Output(component_id='dCustomers', component_property='data'),
        Output(component_id='fGlJob', component_property='data'),
        Output(component_id='exp_allocation', component_property='data'),
        Output(component_id='dJobs', component_property='data'),
        Output(component_id='database', component_property='data')
    ],
    [
        Input(component_id='dt-pkr-range', component_property='start_date'),
        Input(component_id='dt-pkr-range', component_property='end_date'),
        Input(component_id='company-name', component_property='value')
    ], prevent_initial_call=True
)
def output_data(start_date, end_date, database):
    start_date = check_date_format(start_date)
    end_date = check_date_format(end_date)

    with sshtunnel.SSHTunnelForwarder((db_info['SSHHOST'], 22),
                                      ssh_username=db_info['USERNAME'],
                                      ssh_password=db_info['PWDLOGIN'],
                                      remote_bind_address=(db_info['DBHOSTADDRESS'], 3306)) as tunnel:
        engine = create_engine(
            f'mysql+pymysql://{db_info["USERNAME"]}:{db_info["PWDDB"]}@{db_info["HOSTNAME"]}:{tunnel.local_bind_port}/{database}')

        dCoAAdler = pd.read_sql('dCoAAdler', engine)
        fGL = pd.read_sql('fGL', engine)
        fBudget = pd.read_sql('fBudget', engine)
        dEmployee = pd.read_sql('dEmployee', engine)
        dCustomers = pd.read_sql('dCustomers', engine)
        fGlJob = pd.read_sql('fGlJob', engine)
        exp_allocation = pd.read_sql('exp_allocation', engine)
        dJobs = pd.read_sql('dJobs', engine)

        return [start_date,
                end_date,
                dCoAAdler.to_dict('records'),
                fGL.to_dict('records'),
                fBudget.to_dict('records'),
                dEmployee.to_dict('records'),
                dCustomers.to_dict('records'),
                fGlJob.to_dict('records'),
                exp_allocation.to_dict('records'),
                dJobs.to_dict('records'),
                database]


if __name__ == '__main__':
    app.run(debug=False, port=3050)
