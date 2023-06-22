import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


def render_salary_statistic(app, data):
    @app.callback(
        Output('salary-output-container', 'children'),
        [Input('salary-display-options', 'value'), Input('salary-threshold-input', 'value')]
    )
    def update_output(type, threshold):
        sal_df = data[data['ConvertedCompYearly'].notna()]
        sal_df['ConvertedCompYearly'] = sal_df['ConvertedCompYearly'].astype(float)
        value_counts = sal_df['ConvertedCompYearly'].value_counts()
        if (threshold and int(threshold) and int(threshold) > 1):
            sal_df = sal_df[sal_df['ConvertedCompYearly'].isin(value_counts[value_counts > int(threshold)].index)]

        salary_table = html.Table([
                    html.Tr([
                        html.Td('Min'),
                        html.Td(sal_df['ConvertedCompYearly'].min()),
                    ]),
                    html.Tr([
                        html.Td('Max'),
                        html.Td(sal_df['ConvertedCompYearly'].max()),
                    ]),
                    html.Tr([
                        html.Td('Average'),
                        html.Td((sal_df['ConvertedCompYearly'].min() + sal_df['ConvertedCompYearly'].max()) / 2),
                    ]),
                ], className='table')
    
        fig = px.histogram(sal_df, x='ConvertedCompYearly')

        if type == 'text':
            return salary_table
        return dcc.Graph(figure=fig)

    return html.Div(
        html.Div([
            html.Div('Salary:', className='card-header'),
            html.Div(
                dcc.Input(className='form-control', placeholder='Enter threshold', id='salary-threshold-input'), 
                className='card-body'
            ),
            html.Div([
            ], className='card-body', id='salary-output-container'),
            html.Div(
                dcc.RadioItems(
                options=[
                    {"label": "Text", "value": "text"},
                    {"label": "Graph", "value": "graph"},
                ],
                value="text",
                inline=True,
                id="salary-display-options",
                className='btn-group btn-group-toggle',
                labelClassName='btn btn-secondary'
            ),
            className='card-footer text-muted')
        ], className='card col-sm')
    , className='row')