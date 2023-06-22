import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


def render_age_statistic(app, data):
    age_df = data[data['Age'].notna()]
    age_value_counts = age_df['Age'].value_counts().sort_values(ascending=False).sort_index()
    age_items = []
    age_count = 0

    age_pie_labels = []
    age_pie_values = []

    for value, count in age_value_counts.items():
        age_count += count
        age_items.append(html.Tr([html.Td(value), html.Td(count)]))
        age_pie_labels.append(value)
        age_pie_values.append(count)

    age_items.append(html.Tr([
        html.Th('Sum'),
        html.Th(age_count),
    ]))

    fig = px.pie(names=age_pie_labels, values=age_pie_values)
    fig.update_layout(legend=dict(orientation="h"))

    @app.callback(
        Output('age-output-container', 'children'),
        [Input('age-display-options', 'value')]
    )
    def update_output(type):
        if type == 'text':
            return html.Table(age_items, className='table')
        return dcc.Graph(figure=fig)

    return html.Div([
            html.Div('Age:', className='card-header'),
            html.Div([
            ], className='card-body', id='age-output-container'),
            html.Div(
                dcc.RadioItems(
                options=[
                    {"label": "Text", "value": "text"},
                    {"label": "Graph", "value": "graph"},
                ],
                value="text",
                inline=True,
                id="age-display-options",
                className='btn-group btn-group-toggle',
                labelClassName='btn btn-secondary'
            ),
            className='card-footer text-muted')
        ], className='card col-sm')
