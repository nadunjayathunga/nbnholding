import dash
import dash_bootstrap_components as dbc
from data import time_series_data, fin_tiles_values, company_info, graph_legends, months, pl_sort_order, \
    create_narration, related_parties, bs_sort_order, elimination_ledgers
from dash import dcc, html, callback, Output, Input, dash_table
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
from datetime import date
from datetime import timedelta
import plotly.express as px
import warnings



warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

dash.register_page(__name__,
                   path='/', external_stylesheets=[dbc.themes.PULSE, dbc.icons.BOOTSTRAP])

initial_active_cell = {'row': 0, 'column': 1,
                       'column_id': '01', 'row_id': 0}

pl_tab_content = html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    [
                        dcc.Dropdown(
                            options=[
                                {'label': key, 'value': value} for key, value in time_series_data.items()
                            ],
                            value='current_month',
                            id='time-series-fin',
                            className='mt-1',
                            optionHeight=35,
                            clearable=False
                        )
                    ], width={'size': 2}

                ),
                dbc.Col(
                    children=[
                        html.Div(
                            children=[], id='financial-matrics'
                        )
                    ], width={'size': 10}
                )
            ]
        ), dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H5('CATEGORY-WISE REVENUE',
                                className='text-center text-primary mb-4'),
                        dcc.Graph(id='cat-rev', figure={})
                    ], width={'size': 8}
                ),
                dbc.Col(
                    children=[
                        html.H5('YTD', className='text-center text-primary mb-4'),
                        dcc.Graph(id='cat-rev-ytd', figure={})
                    ], width={'size': 4}
                )
            ]
        ), dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H5('CATEGORY-WISE GROSS PROFIT',
                                className='text-center text-primary mb-4'),
                        dcc.Graph(id='cat-gp', figure={})
                    ], width={'size': 8}
                ),
                dbc.Col(
                    children=[
                        html.H5('YTD', className='text-center text-primary mb-4'),
                        dcc.Graph(id='cat-gp-ytd', figure={})
                    ], width={'size': 4}
                )
            ]
        ), dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H5('CATEGORY-WISE OVERHEAD',
                                className='text-center text-primary mb-4'),
                        dcc.Graph(id='cat-oh', figure={})
                    ], width={'size': 8}
                ),
                dbc.Col(
                    children=[
                        html.H5('YTD', className='text-center text-primary mb-4'),
                        dcc.Graph(id='cat-oh-ytd', figure={})
                    ], width={'size': 4}
                )
            ]
        ), dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H5('MAIN INDEXES',
                                className='text-center text-primary mb-4'),
                        dcc.Graph(id='main_index', figure={})
                    ], width={'size': 6}
                ),
                dbc.Col(
                    children=[
                        html.H5(
                            'SUMMARY', className='text-center text-primary mb-4'),
                        dash_table.DataTable(
                            id='monthly-pl',
                            style_cell=dict(textAlign='left'),
                            style_table={'fontSize': 10,
                                         'height': '500px', 'overflowY': 'scroll'},
                            style_header=dict(backgroundColor="paleturquoise",
                                              fontWeight='bold', border='1px solid black'),
                            style_data=dict(backgroundColor="lavender"),
                            fixed_rows={'headers': True, 'data': 0},
                            active_cell=initial_active_cell,
                            style_data_conditional=([
                                {
                                    'if': {'column_id': 'Total'},
                                    'fontWeight': 'bold',
                                    'textAlign': 'right',
                                },
                                {
                                    'if':
                                        {'filter_query': '{first_level} contains "Total"'},
                                    'fontWeight': 'bold',
                                    'border': '1px solid black'
                                },
                                {
                                    'if':
                                        {'filter_query': '{first_level} contains "Cost of Sales" || {first_level} contains "Direct Income" || {first_level} contains "Finance Cost" \
                 || {first_level} contains "Overhead" || {first_level} contains "Indirect Income"'},
                                    'fontWeight': 'bold',
                                    'border-top': '1px solid black'
                                }
                            ])
                        )
                    ], width={'size': 6}
                )
            ]
        ), dbc.Row(
            children=[
                html.H6('Reasons for variance:',
                        className='text-start text-primary mb-4'),
                html.Div(
                    children=[], id='explanations'
                )
            ]
        ), dbc.Row(
            children=[
                html.H5('PROFIT / (LOSS) RESULTS',
                        className='text-center text-primary mb-4'),
                html.Div(
                    children=[], id='pl_results')
            ]
        )

    ]
)

bs_tab_content = html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H6('Balance Sheet as of : ')
                    ], width={'size': 2}
                ),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='bs-date-picker',
                        date=dt.now().date(),
                        min_date_allowed=date(2020, 12, 31),
                        max_date_allowed=dt.now()
                    ), width={'size': 2}
                ),
                dbc.Col(
                    width={'size': 8}
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H6('Key Ratios', className="text-center"),
                        html.Hr(),
                        html.Div(id='bs-main-kpi')

                    ], width={'size': 4}
                ),
                dbc.Col(
                    children=[
                        html.H6(children=[], id='bs-date'),
                        html.Div(
                            children=[], id='balance-sheet'
                        )
                    ], width={'size': 8}
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H6('Total Assets', className="text-center"),
                        dcc.Graph(id='ta-pie-chart', figure={})
                    ], width={'size': 6}
                ),
                dbc.Col(
                    children=[
                        html.H6('Total Liabilities', className="text-center"),
                        dcc.Graph(id='tl-pie', figure={})
                    ], width={'size': 6}
                )
            ]
        )
    ]
)
cf_tab_content = html.Div(
    children=[
        html.H1('Coming Soon')
    ]
)
ci_tab_content = html.Div(
    children=[
        html.H1('Coming Soon')
    ]
)

tabs = dbc.Tabs(
    [
        dbc.Tab(pl_tab_content, label="Profit/(Loss)"),
        dbc.Tab(bs_tab_content, label="Balance Sheet"),
        dbc.Tab(cf_tab_content, label="Cash Flow"),
        dbc.Tab(ci_tab_content, label="Change in Equity")
    ]
)

layout = html.Div(
    dcc.Loading(children=[tabs],
                color='#119DFF', type='graph', fullscreen=True)
)

first_level = pd.DataFrame(
    {'Description': [i for i in pl_sort_order.keys()]})


@callback(
    [
        Output(component_id='financial-matrics',component_property='children'),
        Output(component_id='cat-rev', component_property='figure'),
        Output(component_id='cat-rev-ytd', component_property='figure'),
        Output(component_id='cat-gp', component_property='figure'),
        Output(component_id='cat-gp-ytd', component_property='figure'),
        Output(component_id='cat-oh', component_property='figure'),
        Output(component_id='cat-oh-ytd', component_property='figure'),
        Output(component_id='main_index', component_property='figure'),
        Output(component_id='pl_results', component_property='children'),
        Output(component_id='monthly-pl', component_property='columns'),
        Output(component_id='monthly-pl', component_property='data'),
        Output(component_id='explanations', component_property='children'),
        Output(component_id='balance-sheet', component_property='children'),
        Output(component_id='bs-date', component_property='children'),
        Output(component_id='bs-main-kpi', component_property='children'),
        Output(component_id='tl-pie', component_property='figure'),
        Output(component_id='ta-pie-chart', component_property='figure'),
    ],
    [
        Input(component_id='start-date', component_property='data'),
        Input(component_id='end-date', component_property='data'),
        Input(component_id='time-series-fin', component_property='value'),
        Input(component_id='monthly-pl', component_property='active_cell'),
        Input(component_id='bs-date-picker', component_property='date'),
        Input(component_id='dCoAAdler', component_property='data'),
        Input(component_id='fGL', component_property='data'),
        Input(component_id='fBudget', component_property='data'),
        Input(component_id='database', component_property='data'),
    ],
    prevent_initial_call=True
)
def data_output(start_date, end_date, time_freq, active_cell, bs_date, dCoAAdler, fGL, fBudget,database):

        df_dCoAAdler = pd.DataFrame.from_dict(dCoAAdler)
        df_fGl = pd.DataFrame.from_dict(fGL)
        df_fGl['voucher_date'] = pd.to_datetime(df_fGl['voucher_date'])
        df_fGl['period'] = df_fGl['voucher_date'].dt.strftime(
            date_format='%m')  # return date as 01-12 i.e 2023-07-24 --> 07
        df_fGl_combined = pd.merge(
            left=df_fGl, right=df_dCoAAdler, on='ledger_code', how='left')
        df_fGl_combined['net'] = df_fGl_combined['credit'] - \
                                 df_fGl_combined['debit']  # Revenue will be positive and Expenses will be in negative.

        df_budget = pd.DataFrame.from_dict(fBudget)

        # start_date coming from app.py [DatepickerRange] format like 2023-04-07 i.e 2023-07-01
        cm_begin_date = dt.strptime(start_date, '%Y-%m-%d')
        cm_end_date = dt.strptime(end_date, '%Y-%m-%d')  # 2023-07-31
        pm_end_date = cm_begin_date - timedelta(days=1)  # 2023-06-30
        pm_begin_date = pm_end_date.replace(day=1)  # 2023-06-01
        cy_begin_date = cm_begin_date.replace(month=1)  # 2023-01-01
        py_end_date = cm_end_date - relativedelta(years=1)  # 2022-07-31
        py_m_begin_date = py_end_date.replace(day=1)  # 2022-07-01
        py_begin_date = py_m_begin_date.replace(month=1)  # 2022-01-01

        tile_data_value = {'matric': '', 'value': '', 'change': '',
                           'colour': '', 'icon': '',
                           'comparative': ''}  # this is the structure of each finacial matric tile
        # this is to store tile data for all matrics i.e Revenue/NP/GP etc...
        tile_data_value_all = []

        time_series = [
            {'freq': 'Current Month',
             'value': 'current_month',
             'start_date': cm_begin_date,  # 2023-07-01
             'end_date': cm_end_date,  # 2023-07-31
             'comparative_start': pm_begin_date,  # 2023-06-01
             'comparative_end': pm_end_date},  # 2023-06-30
            {'freq': 'Previous Year Same Month',
             'value': 'previous_year_same_month',
             'start_date': py_m_begin_date,  # 2022-07-01
             'end_date': py_end_date,  # 2022-07-31
             'comparative_start': cm_begin_date,  # 2023-07-01
             'comparative_end': cm_end_date},  # 2023-07-31
            {'freq': 'YTD Current Year',
             'value': 'ytd_current_year',
             'start_date': cy_begin_date,  # 2023-01-01
             'end_date': cm_end_date,  # 2023-07-31
             'comparative_start': py_begin_date,  # 2022-01-01
             'comparative_end': py_end_date}  # 2022-07-31
        ]
        # to get start_date,end_date, comparative_start and comparative_end values from time_series list upon selection
        # of 'time-series-fin'
        st_date = \
            [i['start_date']
             # Selection of 'key'-'Current Month' for the 'value' - 'value' in dictioneries in time_series list
             for i in time_series if i['value'] == time_freq][
                0]  # where 'value' equal to output value of 'time-series-fin'

        en_date = [i['end_date']
                   for i in time_series if i['value'] == time_freq][0]

        comparative_start = [i['comparative_start']
                             for i in time_series if i['value'] == time_freq][0]

        comparative_end = [i['comparative_end']
                           for i in time_series if i['value'] == time_freq][0]

        for matric in fin_tiles_values:  # matrics are GP/NP/EBITDA/REV etc...
            filt_current = (df_fGl_combined['voucher_date'] >= st_date) & (
                    df_fGl_combined['voucher_date'] <= en_date) & (df_fGl_combined['first_level'].isin(
                matric['filt']))  # 'filt' has a list of first_level account groups to get the required matric
            filt_comparative = (df_fGl_combined['voucher_date'] >= comparative_start) & (
                    df_fGl_combined['voucher_date'] <= comparative_end) & (
                                   df_fGl_combined['first_level'].isin(matric['filt']))
            # for each loop create an empty copy of the tile structure
            new_tile_data = tile_data_value.copy()
            new_tile_data['matric'] = matric['value']  # i.e Revenue/GP/NP etc..
            # current period sum of the selected matric i.e Revenue/GP
            new_tile_data['value']: float = df_fGl_combined.loc[filt_current]['net'].sum()
            '''SELECT SUM("fGL".credit - "fGL".debit) AS net FROM "fGL" LEFT JOIN "dCoAAdler" ON "fGL".ledger_code = 
            "dCoAAdler".ledger_code WHERE "dCoAAdler".first_level IN ('Logistics Revenue', 'Manpower Revenue', 
            'Projects Revenue', 'Services Revenue') AND "fGL".voucher_date BETWEEN '2023-08-01' AND '2023-08-31';'''
            new_tile_data['comparative']: float = df_fGl_combined.loc[filt_comparative]['net'].sum(
            )  # comparative period sum of the selected matric i.e Revenue/GP
            try:
                new_tile_data['change']: float = (
                                                         new_tile_data['value'] - new_tile_data['comparative']) / \
                                                 new_tile_data[
                                                     'comparative'] * 100  # Percentage change from previous to current period
            except ZeroDivisionError:
                new_tile_data['change']: float = 0

            if matric['value'] != 'Overhead' and new_tile_data['comparative'] < 0:
                new_tile_data['colour'] = 'success'
            elif matric['value'] != 'Overhead' and new_tile_data['comparative'] > 0:
                new_tile_data['colour'] = 'danger'
            elif matric['value'] == 'Overhead' and new_tile_data['comparative'] > 0:
                new_tile_data['colour'] = 'success'
            else:
                new_tile_data['colour'] = 'danger'
            # new_tile_data['colour'] = 'danger' if new_tile_data['change'] < 0 else 'success' # red if pct change is
            # negative, else green up and down arrow
            new_tile_data['icon'] = "bi bi-arrow-down" if new_tile_data['change'] < 0 else "bi bi-arrow-up"
            # append the current instance of loop to a list
            tile_data_value_all.append(new_tile_data)

        financial_matrics = []  # create an emplty list to store cards filled with matric values
        for i in tile_data_value_all:  # loop over all the matrics i.e Revenue/NP/GP
            card = dbc.Card(  # create a card for each matric
                html.Div(children=[
                    html.H4(
                        i['matric']  # Header i.e Revenue/GP/NP
                    ),
                    html.Hr(),
                    html.H4(f'QR: {i["value"]:,.0f}'),  # Current period value
                    html.H5
                        (
                        [
                            # percentage change from previous period to current period
                            f"{round(i['change'], 2)} %",
                            html.I(className=i['icon']),  # !!! this is not working
                        ], className=f"text-{i['colour']}"
                    ),
                    # comparative period value
                    html.H6(f"QR: {i['comparative']:,.0f}")
                ], className=f"border-{i['colour']} border-start border-5"),
                className='text-center text-nowrap my-2 p-2'

            )

            financial_matrics.append(card)

            card_layout = [
                dbc.Row(
                    [
                        dbc.Col(card, md=3) for card in financial_matrics
                    ]
                )
            ]

        filt_rev = (df_fGl_combined['voucher_date'] >= cy_begin_date) & (
                df_fGl_combined['voucher_date'] <= cm_end_date) & (df_fGl_combined['first_level'].isin(
            values=[i['filt'] for i in fin_tiles_values if i['value'] == 'Revenue'][0]))  # 2023-01-01 to 2023-07-31
        df_ref = df_fGl_combined.loc[filt_rev, ['period', 'ledger_name', 'net']]
        revenue_df = df_ref.groupby(by=['period', 'ledger_name'],
                                    as_index=False)['net'].sum()
        bar_chart_rev_monthwise_cat = px.bar(
            data_frame=revenue_df,
            x='period',
            y='net',
            barmode='group',
            color='ledger_name',
            labels={'period': 'Months', 'net': 'QAR Value',
                    'ledger_name': 'Revenue Type'},
        )
        bar_chart_rev_monthwise_cat.for_each_trace(
            lambda t: t.update(
                name=graph_legends[t.name]))  # to change the legend labels as per the 'graph_legends' dictionery

        bar_chart_rev_monthwise_cat.update_xaxes(
            labelalias=months)  # 01->Jan,02->Feb

        ytd_revenue_df = df_ref.groupby(by=['ledger_name'],
                                        as_index=False)['net'].sum()
        pie_chart_rev_ytd_cat = px.pie(
            data_frame=ytd_revenue_df,
            names=revenue_df['ledger_name'],
            values=revenue_df['net'],
            hole=0.3,
        )
        # to change the legend labels as per the 'graph_legends' dictionery
        pie_chart_rev_ytd_cat.update_traces(
            labels=[graph_legends[label] for label in pie_chart_rev_ytd_cat.data[0]['labels']])

        filt_gp = (df_fGl_combined['voucher_date'] >= cy_begin_date) & (
                df_fGl_combined['voucher_date'] <= cm_end_date) & (
                      df_fGl_combined['first_level'].isin(
                          [i['filt'] for i in fin_tiles_values if i['value'] == 'GP'][0]))
        rev_cat = [i['data'].get(
            'rev_cat') for i in company_info if i['data']['database'] == database][
            0]  # to get the revenue categories listed in company_info dictionery

        # dataframe consist only with Revenue and COGS ledgers
        df_gp = df_fGl_combined.loc[filt_gp, ['ledger_name', 'period', 'net']]
        for cat in rev_cat:
            df_gp.loc[df_gp['ledger_name'].str.contains(
                cat, case=False), 'ledger_name'] = cat
        df_gp_grp = df_gp.groupby(by=['period', 'ledger_name'], as_index=False)[
            'net'].sum()

        bar_chart_gp_monthwise = px.bar(
            data_frame=df_gp_grp,
            x='period',
            y='net',
            barmode='group',
            color='ledger_name',
            labels={'period': 'Months', 'net': 'QAR Value',
                    'ledger_name': 'Segment'}
        )
        bar_chart_gp_monthwise.update_xaxes(labelalias=months)

        ytd_gp_df = df_gp.groupby(by=['ledger_name'],
                                  as_index=False)['net'].sum()
        pie_chart_gp_ytd_cat = px.pie(
            data_frame=ytd_gp_df,
            names=ytd_gp_df['ledger_name'],
            values=ytd_gp_df['net'],
            hole=0.3,
        )

        filt_oh = (df_fGl_combined['voucher_date'] >= cy_begin_date) & (
                df_fGl_combined['voucher_date'] <= cm_end_date) & (df_fGl_combined['first_level'].isin(
            [i['filt'] for i in fin_tiles_values if i['value'] == 'Overhead'][0]))
        df_overhead = df_fGl_combined.loc[filt_oh, [
            'period', 'net', 'first_level']]
        df_overhead['net'] = df_overhead['net'] * -1
        df_overhead_final = df_overhead.groupby(
            by=['first_level', 'period'], as_index=False)['net'].sum()
        bar_chart_oh_monthwise = px.bar(
            data_frame=df_overhead_final,
            x='period',
            y='net',
            barmode='stack',
            color='first_level',
            labels={'period': 'Months', 'net': 'QAR Value',
                    'first_level': 'Exp Heading'}
        )
        bar_chart_oh_monthwise.update_xaxes(labelalias=months)

        df_overhead_final = df_overhead.groupby(
            by=['first_level'], as_index=False)['net'].sum()
        pie_chart_oh_ytd = px.pie(
            data_frame=df_overhead_final,
            names=df_overhead_final['first_level'],
            values=df_overhead_final['net'],
            hole=0.3
        )

        rev_line = df_ref.groupby(by=['period'], as_index=False)['net'].sum()

        rev_profit_indexes = px.line(data_frame=rev_line,
                                     x=rev_line['period'],
                                     y=rev_line['net'],
                                     markers='x',
                                     labels={'period': 'Months',
                                             'net': 'QAR Value'}
                                     )
        rev_profit_indexes.update_xaxes(labelalias=months)
        gp_line = df_gp_grp = df_gp.groupby(
            by=['period'], as_index=False)['net'].sum()

        rev_profit_indexes.add_scatter(x=gp_line['period'],
                                       y=gp_line['net'],
                                       name='Gross Profit'
                                       )

        filt_np = (df_fGl_combined['voucher_date'] >= cy_begin_date) & (
                df_fGl_combined['voucher_date'] <= cm_end_date) & (
                      df_fGl_combined['first_level'].isin(
                          [i['filt'] for i in fin_tiles_values if i['value'] == 'NP'][0]))
        df_np = df_fGl_combined.loc[filt_np, ['period', 'net', 'first_level']]

        np_line = df_np.groupby(by=['period'], as_index=False)['net'].sum()

        rev_profit_indexes.add_scatter(x=np_line['period'],
                                       y=np_line['net'],
                                       name='Net Profit'
                                       )
        filt_ebitda = (df_fGl_combined['voucher_date'] >= cy_begin_date) & (
                df_fGl_combined['voucher_date'] <= cm_end_date) & (df_fGl_combined['first_level'].isin(
            [i['filt'] for i in fin_tiles_values if i['value'] == 'EBITDA'][0]))
        df_ebitda = df_fGl_combined.loc[filt_ebitda, ['period', 'net']]

        ebitda_line = df_ebitda.groupby(by=['period'], as_index=False)['net'].sum()

        rev_profit_indexes.add_scatter(x=ebitda_line['period'],
                                       y=ebitda_line['net'],
                                       name='EBITDA'
                                       )

        df_report = df_np.copy()
        df_first_level_group = df_dCoAAdler.drop_duplicates(
            subset=['first_level', 'third_level'])

        df_report_merged = pd.merge(left=df_report, right=df_first_level_group[[
            'first_level', 'third_level']], on='first_level', how='left')

        for period in df_report_merged['period'].unique():
            filt_period = df_report_merged['period'] == period
            filt_period_df = df_report_merged.loc[filt_period]
            filt_period_df = filt_period_df.groupby(
                by=['period', 'third_level'], as_index=False)['net'].sum()
            filt_period_df.rename(
                columns={'third_level': 'first_level'}, inplace=True)
            filt_period_df.set_index(keys='first_level', inplace=True)
            revenue = filt_period_df.loc['Direct Income', 'net']
            cogs = filt_period_df.loc['Cost of Sales', 'net']
            gp = revenue + cogs
            np = filt_period_df['net'].sum()
            try:
                gp_pct = gp / revenue * 100
                np_pct = np / revenue * 100
            except ZeroDivisionError:
                gp_pct = 0
                np_pct = 0
            filt_period_df.reset_index(inplace=True)
            gp_amt_row = {'period': period,
                          'first_level': 'Gross Proft / Loss', 'net': gp}
            gp_pct_row = {'period': period,
                          'first_level': 'Gross Proft / Loss %', 'net': gp_pct}
            np_amt_row = {'period': period,
                          'first_level': 'Net Profit / Loss', 'net': np}
            np_pct_row = {'period': period,
                          'first_level': 'Net Profit / Loss %', 'net': np_pct}
            filt_period_df = filt_period_df._append(gp_amt_row, ignore_index=True)
            filt_period_df = filt_period_df._append(gp_pct_row, ignore_index=True)
            filt_period_df = filt_period_df._append(np_amt_row, ignore_index=True)
            filt_period_df = filt_period_df._append(np_pct_row, ignore_index=True)
            df_report = pd.concat([df_report, filt_period_df])

        df_report = pd.pivot_table(data=df_report, index=[
            'first_level'], columns='period', aggfunc='sum', margins=False, values='net')
        df_report.reset_index(inplace=True)
        # This is the row_id for the column header @ active_cell
        row = active_cell['row_id']

        def custom_sort_key(value):
            return pl_sort_order.get(value, 0)

        df_report = df_report.sort_values(
            by='first_level', key=lambda x: x.map(custom_sort_key))
        df_report['id'] = df_report.index
        df_report_cols = list(df_report.columns)
        df_report_cols.remove('id')

        first_level_header = df_report.at[row, 'first_level']
        # This is the column_id for the row @ active_cell
        col = active_cell['column_id']

        narration_filter = (df_fGl_combined['voucher_date'] >= cy_begin_date) & (
                df_fGl_combined['voucher_date'] <= cm_end_date) & (
                                       df_fGl_combined['first_level'] == first_level_header) & (
                                   df_fGl_combined['period'] == col)

        narration_df = df_fGl_combined.loc[narration_filter, [
            'ledger_name', 'narration', 'net']]
        narration_df['narration'] = narration_df['narration'].apply(
            create_narration)
        narration_df = narration_df[narration_df['narration'].notna()]
        narration_df.sort_values(by='ledger_name', inplace=True)

        narrations = dash_table.DataTable(
            columns=[
                {'name': 'Account Name', 'id': 'ledger_name', 'deletable': False, 'selectable': True, 'type': 'text'},
                {'name': 'Narration', 'id': 'narration',
                 'deletable': False, 'selectable': True, 'type': 'text'},
                {'name': 'Amount', 'id': 'net', 'deletable': False, 'selectable': True, 'type': 'numeric',
                 'format': {'specifier': ',.0f'}}],
            data=narration_df.to_dict('records'),
            id='narrations-tbl',
            style_cell=dict(textAlign='left'),
            style_table={'fontSize': 10,
                         'height': '100px', 'overflowY': 'scroll'},
            style_header=dict(backgroundColor="paleturquoise",
                              fontWeight='bold', border='1px solid black'),
            style_data=dict(backgroundColor="lavender"),
            fixed_rows={'headers': True, 'data': 0},
            active_cell=initial_active_cell,
        )

        column_list = ['CY CM', 'CY CM BUD', 'PY CM',
                       'CY PM', 'CY YTD', 'CY YTD BUD', 'PY YTD']

        time_period = [{'column': 'CY CM', 'start': cm_begin_date, 'end': cm_end_date},
                       {'column': 'CY CM BUD', 'start': cm_begin_date, 'end': cm_end_date},
                       {'column': 'PY CM', 'start': py_m_begin_date, 'end': py_end_date},
                       {'column': 'CY PM', 'start': pm_begin_date, 'end': pm_end_date},
                       {'column': 'CY YTD', 'start': cy_begin_date, 'end': cm_end_date},
                       {'column': 'CY YTD BUD', 'start': cy_begin_date, 'end': cm_end_date},
                       {'column': 'PY YTD', 'start': py_begin_date, 'end': py_end_date}]

        filtered_budget = df_budget.set_index(['ledger_code', 'fy'])
        filtered_budget = filtered_budget.stack().reset_index()
        filtered_budget.rename(
            columns={'level_2': 'month', 0: 'net'}, inplace=True)
        filtered_budget = pd.merge(right=filtered_budget, left=df_dCoAAdler[[
            'ledger_code', 'forth_level', 'first_level']], on='ledger_code', how='inner')
        filtered_budget['net'] = filtered_budget.apply(
            lambda row: row['net'] * -1 if row['forth_level'] == 'Expenses' else row['net'], axis=1)
        filtered_budget['voucher_date'] = pd.to_datetime(
            filtered_budget['fy'].astype(str) + '-' + filtered_budget['month'] + '-01')
        filtered_budget = filtered_budget.loc[filtered_budget['net'] != 0]
        filtered_budget = filtered_budget[['first_level', 'net', 'voucher_date']]

        for i in column_list:
            datasource = filtered_budget if i == 'CY CM BUD' or i == 'CY YTD BUD' else df_fGl_combined
            period_start = [k['start'] for k in time_period if k['column'] == i][0]
            period_end = [k['end'] for k in time_period if k['column'] == i][0]
            df_filter = (datasource['voucher_date'] >= period_start) & (datasource['voucher_date'] <= period_end) & (
                datasource['first_level'].isin(values=[j['filt'] for j in fin_tiles_values if j['value'] == 'NP'][0]))
            period_df = datasource.loc[df_filter, ['first_level', 'net']]
            period_df = period_df.groupby(
                by=['first_level'], as_index=False)['net'].sum()
            np = period_df['net'].sum()
            trd_level = pd.merge(left=period_df, right=df_first_level_group[[
                'first_level', 'third_level']], on='first_level', how='left')
            trd_level = trd_level.groupby(
                by=['third_level'], as_index=False)['net'].sum()
            trd_level.rename(columns={'third_level': 'first_level'}, inplace=True)
            period_df = pd.concat([period_df, trd_level])
            period_df.rename(
                columns={'first_level': 'Description', 'net': f'{i}'}, inplace=True)
            period_df.set_index(keys='Description', inplace=True)
            revenue = period_df.loc['Direct Income', f'{i}']
            cogs = period_df.loc['Cost of Sales', f'{i}']
            gp = revenue + cogs

            try:
                gp_pct = gp / revenue * 100
                np_pct = np / revenue * 100
            except ZeroDivisionError:
                gp_pct = 0
                np_pct = 0
            period_df.reset_index(inplace=True)
            gp_amt_row = {
                'Description': 'Gross Proft / Loss', f'{i}': gp}
            gp_pct_row = {
                'Description': 'Gross Proft / Loss %', f'{i}': gp_pct}
            np_amt_row = {
                'Description': 'Net Profit / Loss', f'{i}': np}
            np_pct_row = {
                'Description': 'Net Profit / Loss %', f'{i}': np_pct}
            period_df = period_df._append(gp_amt_row, ignore_index=True)
            period_df = period_df._append(gp_pct_row, ignore_index=True)
            period_df = period_df._append(np_amt_row, ignore_index=True)
            period_df = period_df._append(np_pct_row, ignore_index=True)

            merged_pl = pd.merge(left=first_level if i == 'CY CM' else merged_pl,
                                 right=period_df, on='Description', how='left')

        merged_pl = merged_pl.sort_values(
            by='Description', key=lambda x: x.map(custom_sort_key))
        merged_pl = merged_pl.loc[(merged_pl[column_list] != 0).any(axis=1)]

        inc_first_level = df_dCoAAdler[['forth_level', 'first_level']]
        inc_first_level: list = df_dCoAAdler.loc[inc_first_level['forth_level']
                                                 == 'Income', 'first_level'].unique().tolist()

        exp_first_level = df_dCoAAdler[['forth_level', 'first_level']]
        exp_first_level: list = df_dCoAAdler.loc[exp_first_level['forth_level']
                                                 == 'Expenses', 'first_level'].unique().tolist()

        pl_results = dash_table.DataTable(
            id='pl_results_table',
            columns=[
                {'name': 'Description', 'id': 'Description',
                 'type': 'text', 'deletable': False, 'selectable': True},
                {'name': 'CY CM', 'id': 'CY CM', 'type': 'numeric', 'deletable': True,
                 'selectable': True, 'format': {'specifier': ',.0f'}},
                {'name': 'CY CM BUD', 'id': 'CY CM BUD', 'type': 'numeric',
                 'deletable': True, 'selectable': True, 'format': {'specifier': ',.0f'}},
                {'name': 'PY CM', 'id': 'PY CM', 'type': 'numeric', 'deletable': True,
                 'selectable': True, 'format': {'specifier': ',.0f'}},
                {'name': 'CY PM', 'id': 'CY PM', 'type': 'numeric', 'deletable': True,
                 'selectable': True, 'format': {'specifier': ',.0f'}},
                {'name': ' ', 'id': ' ', 'type': 'text',
                 'deletable': False, 'selectable': True},
                {'name': 'CY YTD', 'id': 'CY YTD', 'type': 'numeric', 'deletable': True,
                 'selectable': True, 'format': {'specifier': ',.0f'}},
                {'name': 'CY YTD BUD', 'id': 'CY YTD BUD', 'type': 'numeric',
                 'deletable': True, 'selectable': True, 'format': {'specifier': ',.0f'}},
                {'name': 'PY YTD', 'id': 'PY YTD', 'type': 'numeric', 'deletable': True,
                 'selectable': True, 'format': {'specifier': ',.0f'}}
            ],
            data=merged_pl.to_dict(orient='records'),
            style_cell=dict(textAlign='left'),
            style_table={'fontSize': 10, 'height': '500px', 'overflowY': 'scroll'},
            style_header=dict(backgroundColor="paleturquoise",
                              fontWeight='bold', border='1px solid black'),
            style_data=dict(backgroundColor="lavender"),
            style_cell_conditional=(
                    [
                        {
                            'if': {'column_id': 'Description'},
                            'width': '30px'
                        },
                        {
                            'if': {'column_id': ' '},
                            'width': '75px'
                        }
                    ] +
                    [
                        {
                            'if': {'column_id': k},
                            'width': '30px'
                        } for k in ['CY CM', 'CY CM BUD', 'PY CM', 'CY PM', 'CY YTD', 'CY YTD BUD', 'PY YTD']
                    ]
            ),
            fixed_rows={'headers': True, 'data': 0},
            tooltip_data=[
                {
                    column: {
                        'value': f'The variance between {"CY CM" if column in ["CY CM BUD", "PY CM", "CY PM"] else "CY YTD"} \
                            and {column} is **{abs((row["CY CM"] if column in ["CY CM BUD", "PY CM", "CY PM"] else row["CY YTD"]) - row[column]):,.0f}**',
                        'type': 'markdown'
                    }
                    for column in row.keys() if column in ['CY CM BUD', 'PY CM', 'CY PM', 'CY YTD BUD', 'PY YTD']
                }
                for row in merged_pl.to_dict('records')
            ],

            tooltip_header={
                'CY CM': 'Current Year Current Month',
                'CY CM BUD': 'Current Year Current Month Budget',
                'PY CM': 'Previous Year Same Month',
                'CY PM': 'Current Year Previous Month',
                'CY YTD': 'Current Year Year-to-Date',
                'CY YTD BUD': 'Current Year Year-to-Date Budget',
                'PY YTD': 'Previous Year Year-to-Date'},
            css=[
                {
                    'selector': '.dash-table-tooltip',
                    'rule': 'background-color:white;color:black;font-size: 10px;font-family: "Times New Roman";'
                }
            ],
            style_data_conditional=([
                {
                    'if':
                        {
                            'filter_query': '{Description} contains "Cost of Sales" || {Description} contains "Direct '
                                            'Income" || {Description} contains "Finance Cost"  || {Description} contains '
                                            '"Overhead" || {Description} contains "Indirect Income"'},
                    'fontWeight': 'bold',
                    'border-top': '1px solid black'
                }
            ])

        )

        bs_date = dt.strptime(bs_date, '%Y-%m-%d')  # this is the current date by default
        bs_date_py = bs_date - relativedelta(years=1)
        ######################################## BALANCE SHEET CALCULATIONS STARTS FROM HERE ##############################a
        bs_combined = pd.DataFrame({'second_level': [], 'net': [], 'as_of': []})
        for fy in [bs_date_py, bs_date]:  # as we need as of current date and period one year ago
            # initializing the exclude ledgers list - currently this list contains inter-company receivable/payable ledgers
            exclude_list = [i for j in related_parties.values() for i in j]

            # #### RULE NUMBER ONE - INTER-COMPANY PAYABLE AND RECEIVABLE ADJUSTMENT ####### we are separating related
            # party receivable and payable balances from the gl. Same related party having more than one ledger account (
            # Receivable/Payable/ Wrongly created duplicate ledgers will be clubbed together. Total of positive related
            # party balances will be due from related parties and negative will be due to related parties.
            rp_filt = (df_fGl_combined['ledger_name'].isin(exclude_list)) & (df_fGl_combined[
                                                                                 'voucher_date'] <= fy)
            # j returns a list, i assigns such list items to a master list which
            # consist of all the ledger names of related parties
            df_rp = df_fGl_combined.loc[rp_filt, ['ledger_name', 'net']]

            df_rp['ledger_name'] = df_rp['ledger_name'].apply(
                lambda ledger_name: [i for i, j in related_parties.items() if ledger_name in j][
                    0])  # same related party has multiple ledgers i.e for payable and receivable. To get the total for
            # each related party need to assign a single value to each ledger which mentioned in related parties list.
            df_rp = df_rp.groupby(by=['ledger_name'], as_index=False)['net'].sum()  # this will group inter-company
            # ledgers having multiple ledger names

            rpp: float = df_rp.loc[df_rp['net'] >= 0, 'net'].sum()  # sum of related-parties which has negative values

            rpr: float = df_rp.loc[df_rp['net'] < 0, 'net'].sum()  # sum of related-parties which has positive values

            ##### RULE NUMBER TWO - NOMINAL LEDGER ACCOUNT ELIMINATION #######
            # PDC receivable / payable/ security cheque / guarantee cheque account sum total should be zero. Having them
            # in the second level total will unnecessarily increase the second level total

            elimination_filt = (df_fGl_combined['ledger_name'].isin(elimination_ledgers)) & (
                    df_fGl_combined['voucher_date'] <= fy)
            elimanated_total: float = df_fGl_combined.loc[elimination_filt, 'net'].sum()  # + if credit balance , - if
            # debit balance, credit - debit
            exclude_list = exclude_list + elimination_ledgers

            ##### RULE NUMBER THREE - HANDLING DEBIT/CREDIT BALANCES IN AP/AR  #######
            ap_filt = (df_fGl_combined['second_level'].isin(['Accounts Payables'])) & (
                ~df_fGl_combined['ledger_name'].isin(exclude_list)) & (df_fGl_combined['voucher_date'] <= fy)
            df_dr_ap = df_fGl_combined.loc[ap_filt].groupby(by=['ledger_name'], as_index=False)['net'].sum()
            dr_ap_list: list = df_dr_ap.loc[df_dr_ap['net'] < 0, 'ledger_name'].tolist()
            dr_ap_amt: float = df_dr_ap.loc[df_dr_ap['net'] < 0, 'net'].sum()  # return a - figure

            ar_filt = (df_fGl_combined['second_level'].isin(['Trade Receivables'])) & (
                ~df_fGl_combined['ledger_name'].isin(exclude_list)) & (df_fGl_combined['voucher_date'] <= fy)
            df_cr_ar = df_fGl_combined.loc[ar_filt].groupby(by=['ledger_name'], as_index=False)['net'].sum()
            cr_ar_list: list = df_cr_ar.loc[df_cr_ar['net'] > 0, 'ledger_name'].tolist()
            cr_ar_amt: float = df_cr_ar.loc[df_cr_ar['net'] > 0, 'net'].sum()  # return a + figure
            exclude_list = exclude_list + dr_ap_list + cr_ar_list
            # below will take all the balance sheet ledger accounts which are not related party receivable or payable.
            bs_second_level_filt = (~df_fGl_combined['ledger_name'].isin(exclude_list)) & (
                    df_fGl_combined['voucher_date'] <= fy) & df_fGl_combined['forth_level'].isin(
                ['Assets', 'Liabilities', 'Equity'])
            bs_second_level = df_fGl_combined.loc[bs_second_level_filt, ['net', 'second_level']]
            # this will create a root level table for balance sheet
            bs_second_level = bs_second_level.groupby(by=['second_level'], as_index=False)['net'].sum()

            bs_second_level.set_index('second_level', inplace=True)
            bs_second_level.loc['Accruals & Other Payables', 'net'] = bs_second_level.loc[
                                                                          'Accruals & Other Payables', 'net'] + cr_ar_amt + (
                                                                          elimanated_total if elimanated_total > 0 else 0)

            bs_second_level.loc['Other Receivable', 'net'] = bs_second_level.loc[
                                                                 'Other Receivable', 'net'] + dr_ap_amt + (
                                                                 elimanated_total if elimanated_total < 0 else 0)
            bs_second_level.reset_index(inplace=True)
            # creating a row for related party payable
            rpp_row = {'second_level': 'Due to Related Parties', 'net': rpp}
            bs_second_level = bs_second_level._append(rpp_row, ignore_index=True)
            # creating a row for related party receivable
            rpr_row = {'second_level': 'Due from Related Parties', 'net': rpr}
            bs_second_level = bs_second_level._append(rpr_row, ignore_index=True)

            pl_period_filt = (df_fGl_combined['forth_level'].isin(['Expenses', 'Income'])) & (
                    df_fGl_combined['voucher_date'] <= fy)
            # this will provide overall profit/loss figure for the period 2021-01-01 till current date
            pl_period: float = df_fGl_combined.loc[pl_period_filt, 'net'].sum()

            # below will add whole period pl figure to the opening retained earnings will return retuned earning as of
            # selected date
            bs_second_level.set_index('second_level', inplace=True)
            bs_second_level.loc['Retained Earnings', 'net'] = bs_second_level.loc[
                                                                  'Retained Earnings', 'net'] + pl_period
            bs_second_level.reset_index(inplace=True)

            for i in ['Assets', 'Equity', 'Liabilities']:
                e_l_row = {'second_level': '', 'net': 0}
                forth_level_total: float = 0
                for j in df_fGl_combined.loc[df_fGl_combined['forth_level'] == i, 'third_level'].unique().tolist():
                    third_level_total: float = 0
                    bs_second_level.set_index('second_level', inplace=True)
                    for k in df_fGl_combined.loc[df_fGl_combined['third_level'] == j, 'second_level'].unique().tolist():
                        try:
                            third_level_total = third_level_total + bs_second_level.loc[k, 'net']
                        except KeyError:
                            third_level_row = third_level_row
                    third_level_row = {'second_level': j, 'net': third_level_total}
                    bs_second_level.reset_index(inplace=True)
                    bs_second_level = bs_second_level._append(third_level_row, ignore_index=True)
                    bs_second_level.set_index('second_level', inplace=True)
                    try:
                        forth_level_total = forth_level_total + bs_second_level.loc[j, 'net']
                    except KeyError:
                        forth_level_total = forth_level_total
                    forth_level_row = {'second_level': i, 'net': forth_level_total}
                    bs_second_level.reset_index(inplace=True)

                bs_second_level = bs_second_level._append(forth_level_row, ignore_index=True)
                bs_second_level.set_index('second_level', inplace=True)
                try:
                    e_l_row = {'second_level': 'Liability & Equity',
                               'net': bs_second_level.loc['Equity', 'net'] + bs_second_level.loc['Liabilities', 'net']}
                except KeyError:
                    pass
                bs_second_level.reset_index(inplace=True)
                bs_second_level = bs_second_level._append(e_l_row, ignore_index=True)
                bs_second_level['as_of'] = f'As of {fy.date()}'  # 01

            bs_combined = pd.concat([bs_second_level, bs_combined])

        bs_combined_filt = (~bs_combined['second_level'].isin(
            ['Liabilities', 'Statutory Reserve', 'Capital', 'Current Accounts', 'Retained Earning', '']))

        bs_combined = bs_combined.loc[bs_combined_filt]

        bs_combined.set_index('second_level', inplace=True)

        bs_combined = pd.pivot_table(data=bs_combined, index=['second_level'], columns='as_of',
                                     values='net')  # this will pivot from |second_level|net|as_of --> |second_level|As
        # of 2023-12-20|As of 2022-12-20
        asset_headings: list = ['Assets'] + df_fGl_combined.loc[
            df_fGl_combined['forth_level'] == 'Assets', 'third_level'].unique().tolist() + df_fGl_combined.loc[
                                   df_fGl_combined['forth_level'] == 'Assets', 'second_level'].unique().tolist()
        bs_combined.reset_index(inplace=True)

        second_level_asset_list: list = df_fGl_combined.loc[
            df_fGl_combined['forth_level'] == 'Assets', 'second_level'].unique().tolist()
        pie_chart_assets_df = bs_combined.loc[
            bs_combined['second_level'].isin(second_level_asset_list) & bs_combined[f'As of {bs_date.date()}'] != 0, [
                'second_level', f'As of {bs_date.date()}']]
        pie_chart_assets_df[f'As of {bs_date.date()}'] = pie_chart_assets_df[f'As of {bs_date.date()}'].apply(
            lambda x: x * -1)

        pie_chart_assets = px.pie(
            data_frame=pie_chart_assets_df,
            names=pie_chart_assets_df['second_level'],
            values=pie_chart_assets_df[f'As of {bs_date.date()}'],
            hole=0.3,
        )
        pie_chart_assets.update_traces(
            pull=[i * 0 if i != max(pie_chart_assets_df[f'As of {bs_date.date()}'].tolist()) else 0.1 for i in
                  pie_chart_assets_df[f'As of {bs_date.date()}'].tolist()],
            opacity=0.8)

        second_level_liabilities_list: list = df_fGl_combined.loc[
            df_fGl_combined['forth_level'] == 'Liabilities', 'second_level'].unique().tolist()
        pie_chart_liabilities_df = bs_combined.loc[
            bs_combined['second_level'].isin(second_level_liabilities_list) & bs_combined[
                f'As of {bs_date.date()}'] != 0, [
                'second_level', f'As of {bs_date.date()}']]

        pie_chart_liabilities = px.pie(
            data_frame=pie_chart_liabilities_df,
            names=pie_chart_liabilities_df['second_level'],
            values=pie_chart_liabilities_df[f'As of {bs_date.date()}'],
            hole=0.3
        )
        pie_chart_liabilities.update_traces(
            pull=[i * 0 if i != max(pie_chart_liabilities_df[f'As of {bs_date.date()}'].tolist()) else 0.1 for i in
                  pie_chart_liabilities_df[f'As of {bs_date.date()}'].tolist()],
            opacity=0.8)

        def assets_positive(x):
            if x['second_level'] in asset_headings:
                return x[[f'As of {bs_date.date()}', f'As of {bs_date_py.date()}']] * -1
            else:
                return x[[f'As of {bs_date.date()}', f'As of {bs_date_py.date()}']]

        bs_combined[[f'As of {bs_date.date()}', f'As of {bs_date_py.date()}']] = bs_combined.apply(
            lambda x: assets_positive(x), axis=1)
        bs_combined.set_index('second_level', inplace=True)

        bs_combined['Variance'] = bs_combined[f'As of {bs_date.date()}'] - bs_combined[f'As of {bs_date_py.date()}']
        try:
            bs_combined['% Var'] = (bs_combined[f'As of {bs_date.date()}'] / bs_combined[
                f'As of {bs_date_py.date()}'] - 1) * 100
        except ZeroDivisionError:  # as in some cases prior year figure may be zero
            bs_combined['% Var'] = 0
        # as the initial table does not have CY / PY format
        bs_combined = bs_combined.reindex(
            columns=[f'As of {bs_date.date()}', f'As of {bs_date_py.date()}', 'Variance', '% Var'])

        def custom_sort_key_bs(value):
            return bs_sort_order.get(value, 0)

        # sorting as per the custom sort order
        bs_combined = bs_combined.sort_values(
            by='second_level', key=lambda x: x.map(custom_sort_key_bs))
        # otherwise dataTable will not show the second_level(Description)
        bs_combined.reset_index(inplace=True)

        ######BALANCE SHEET KPI###############

        bs_main_kpi = {'working_capital': {'long_name': 'Working Capital', 'cy': 0, 'py': 0,
                                           'url': 'https://www.investopedia.com/terms/w/workingcapital.asp'},
                       'debt_to_equity': {'long_name': 'Debt-to-Equity', 'cy': 0, 'py': 0,
                                          'url': 'https://www.investopedia.com/terms/d/debtequityratio.asp'},
                       'current_ratio': {'long_name': 'Current Ratio', 'cy': 0, 'py': 0,
                                         'url': 'https://www.investopedia.com/terms/c/currentratio.asp'},
                       'dso': {'long_name': 'Days Sales Outstanding', 'cy': 0, 'py': 0,
                               'url': 'https://www.investopedia.com/terms/d/dso.asp'},
                       'dpo': {'long_name': 'Days Payable Outstanding', 'cy': 0, 'py': 0,
                               'url': 'https://www.investopedia.com/terms/d/dpo.asp'},
                       'ccr': {'long_name': 'Cash Conversion Ratio', 'cy': 0, 'py': 0,
                               'url': 'https://www.investopedia.com/terms/c/cashconversioncycle.asp'},
                       'asset_turnover': {'long_name': 'Asset Turnover Ratio', 'cy': 0, 'py': 0,
                                          'url': 'https://www.investopedia.com/terms/a/assetturnover.asp'},
                       'roe': {'long_name': 'Return on Equity', 'cy': 0, 'py': 0, 'var': 0, 'var_pct': 0,
                               'url': 'https://www.investopedia.com/terms/r/returnonequity.asp'}}

        bs_combined.set_index('second_level', inplace=True)
        for fy in [bs_date, bs_date_py]:
            fy_year = 'cy' if fy == bs_date else 'py'
            bs_main_kpi['working_capital'][fy_year] = bs_combined.loc['Current Assets', f'As of {fy.date()}'] - \
                                                      bs_combined.loc[
                                                          'Current Liabilities', f'As of {fy.date()}']
            try:
                bs_main_kpi['debt_to_equity'][fy_year] = (bs_combined.loc['Current Liabilities', f'As of {fy.date()}'] +
                                                          bs_combined.loc[
                                                              'Non Current Liabilities', f'As of {fy.date()}']) / \
                                                         bs_combined.loc['Equity', f'As of {fy.date()}']
                bs_main_kpi['current_ratio'][fy_year] = bs_combined.loc['Current Assets', f'As of {fy.date()}'] / \
                                                        bs_combined.loc[
                                                            'Current Liabilities', f'As of {fy.date()}']
                dso = (bs_combined.loc['Trade Receivables', f'As of {fy.date()}'] - bs_combined.loc[
                    'Due from Related Parties', f'As of {fy.date()}']) / df_fGl_combined.loc[
                          df_fGl_combined['third_level'].isin(['Direct Income']) & (
                                  df_fGl_combined['voucher_date'] >= fy.replace(month=1, day=1)) & (
                                  df_fGl_combined['voucher_date'] <= fy), 'net'].sum() * 365
                bs_main_kpi['dso'][fy_year] = dso
                dpo = bs_combined.loc['Accounts Payables', f'As of {fy.date()}'] / df_fGl_combined.loc[
                    df_fGl_combined['third_level'].isin(['Cost of Sales']) & (
                            df_fGl_combined['voucher_date'] >= fy.replace(month=1, day=1)) & (
                            df_fGl_combined['voucher_date'] <= fy), 'net'].sum() * 365
                bs_main_kpi['dpo'][fy_year] = dpo
                bs_main_kpi['ccr'][fy_year] = dso - dpo
                bs_main_kpi['asset_turnover'][fy_year] = df_fGl_combined.loc[
                                                             df_fGl_combined['third_level'].isin(['Direct Income']) & (
                                                                     df_fGl_combined['voucher_date'] >= fy.replace(
                                                                 month=1,
                                                                 day=1)) & (
                                                                     df_fGl_combined[
                                                                         'voucher_date'] <= fy), 'net'].sum() / \
                                                         bs_combined.loc['Assets', f'As of {fy.date()}']
                bs_main_kpi['roe'][fy_year] = df_fGl_combined.loc[
                                                  df_fGl_combined['forth_level'].isin(['Expenses', 'Income']) & (
                                                          df_fGl_combined['voucher_date'] >= fy.replace(month=1,
                                                                                                        day=1)) & (
                                                          df_fGl_combined['voucher_date'] <= fy), 'net'].sum() / \
                                              bs_combined.loc[
                                                  'Equity', f'As of {fy.date()}']
            except ZeroDivisionError:
                bs_main_kpi['debt_to_equity'][fy_year] = 0
                bs_main_kpi['current_ratio'][fy_year] = 0
                bs_main_kpi['dso'][fy_year] = 0
                bs_main_kpi['dpo'][fy_year] = 0
                bs_main_kpi['ccr'][fy_year] = 0
                bs_main_kpi['asset_turnover'][fy_year] = 0
                bs_main_kpi['roe'][fy_year] = 0
        for i in bs_main_kpi:
            bs_main_kpi[i]['var'] = bs_main_kpi[i]['cy'] - bs_main_kpi[i]['py']
            try:
                bs_main_kpi[i]['var_pct'] = bs_main_kpi[i]['var'] / bs_main_kpi[i]['py']
            except ZeroDivisionError:
                bs_main_kpi[i]['var_pct'] = 0

        bs_combined.reset_index(inplace=True)

        no_of_rows = 4
        no_of_columns = 2

        cards = []
        tile_number = -1
        for i in range(no_of_rows):
            row_cards = []
            for j in range(no_of_columns):
                tile_number = tile_number + 1
                card = dbc.Card(
                    html.Div(
                        children=[
                            dbc.CardHeader(dbc.CardLink(
                                [v["long_name"] for i, (k, v) in enumerate(bs_main_kpi.items()) if i == tile_number][0],
                                target="_blank",
                                href=[v["url"] for i, (k, v) in enumerate(bs_main_kpi.items()) if i == tile_number][0]),
                                className="text-center fw-bold"),
                            dbc.CardBody([html.P(
                                f'CY: {[v["cy"] for i, (k, v) in enumerate(bs_main_kpi.items()) if i == tile_number][0]:,.0f}',
                                className="text-center fw-bold fs-3 text mt-0 mb-0"),
                                html.P(
                                    f'PY: {[v["py"] for i, (k, v) in enumerate(bs_main_kpi.items()) if i == tile_number][0]:,.0f}',
                                    className="text-center fs-4 text mt-0 mb-0"),
                                # html.Div(
                                #     [
                                #         html.P(
                                #             f'VAR: {[v["var"] for i, (k, v) in enumerate(bs_main_kpi.items()) if i == tile_number][0]:,.0f}',
                                #             className="text-center fs-6 text mt-0 mb-0"),
                                #         html.P('----', className="text-center fs-6 text mt-0 mb-0"),
                                #         html.P(
                                #             f'VAR: {[v["var_pct"] for i, (k, v) in enumerate(bs_main_kpi.items()) if i == tile_number][0]:,.0f}%',
                                #             className="text-center fs-6 text mt-0 mb-0")
                                #     ], className="d-xxl-inline-flex mt-0 mb-0"
                                # )
                            ])
                        ],
                        className='border-start border-5 border-warning' if
                        [v["cy"] for i, (k, v) in enumerate(bs_main_kpi.items()) if i == tile_number][0] <
                        [v["py"] for i, (k, v) in enumerate(bs_main_kpi.items()) if i == tile_number][
                            0] else 'border-start border-5 border-success'
                    )
                )
                row_cards.append(card)

            row = dbc.CardGroup(row_cards)
            cards.append(row)
            cards.append(html.Hr())

        if cards:
            cards.pop()

        balance_sheet = dash_table.DataTable(
            data=bs_combined.to_dict(orient='records'),
            columns=[
                {'name': 'Description', 'id': 'second_level', 'deletable': False, 'selectable': True, 'type': 'text'},
                {'name': f'As of {bs_date.date()}', 'id': f'As of {bs_date.date()}', 'deletable': False,
                 'selectable': True, 'type': 'numeric', 'format': {'specifier': ',.0f'}},
                {'name': f'As of {bs_date_py.date()}', 'id': f'As of {bs_date_py.date()}', 'deletable': False,
                 'selectable': True, 'type': 'numeric', 'format': {'specifier': ',.0f'}},
                {'name': 'Variance', 'id': 'Variance', 'deletable': False, 'selectable': True, 'type': 'numeric',
                 'format': {'specifier': ',.0f'}},
                {'name': '% Var', 'id': '% Var', 'deletable': False, 'selectable': True, 'type': 'numeric',
                 'format': {'specifier': ',.0f'}}, ],
            id='balance-sheet-tbl',
            style_cell=dict(textAlign='left'),
            style_table={'fontSize': 10,
                         },
            style_header=dict(backgroundColor="paleturquoise",
                              fontWeight='bold', border='1px solid black'),
            style_data=dict(backgroundColor="lavender"),
            # fixed_rows={'headers': True, 'data': 0},
            style_data_conditional=([
                {
                    'if':
                        {
                            'filter_query': '{second_level} eq "Non Current Assets" || {second_level} eq "Current Assets" '
                                            ' || {second_level} eq "Assets"  || {second_level} eq "Non Current '
                                            'Liabilities" || {second_level} eq "Current Liabilities" || {second_level} eq '
                                            '"Liability & Equity" || {second_level} eq "Equity"'},
                    'fontWeight': 'bold',
                    'border-top': '1px solid black'
                }

            ])

        )

        return [card_layout,
                bar_chart_rev_monthwise_cat,
                pie_chart_rev_ytd_cat,
                bar_chart_gp_monthwise,
                pie_chart_gp_ytd_cat,
                bar_chart_oh_monthwise,
                pie_chart_oh_ytd,
                rev_profit_indexes,
                pl_results,
                [{"name": months[i],
                  "id": i, "deletable": True, "selectable": True, 'type': 'numeric',
                  'format': {'specifier': ',.0f'}} if i not in ['first_level'] else {"name": months[i], "id": i,
                                                                                     "deletable": True,
                                                                                     "selectable": True,
                                                                                     'type': 'text'}
                 for
                 i in df_report_cols],
                # set the properties for first_level column and other column headers of the df_report.columns
                df_report.to_dict(orient='records'),
                narrations,
                balance_sheet,
                f'Balance Sheet As of {bs_date.date()}',
                cards,
                pie_chart_liabilities,
                pie_chart_assets,
                ]
