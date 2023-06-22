import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


def render_gender_statistic(app, data):
    gender_df = data[data['Gender'].notna()]
    gender_df['Gender'] = gender_df['Gender'].str.split(';')
    gender_df = gender_df.explode('Gender')
    gender_value_counts = gender_df['Gender'].value_counts().sort_values(ascending=False).sort_index()
    gender_items = []
    gender_count = 0

    gender_pie_labels = []
    gender_pie_values = []

    for value, count in gender_value_counts.items():
        gender_count += count
        gender_items.append(html.Tr([html.Td(value), html.Td(count)]))
        gender_pie_labels.append(value)
        gender_pie_values.append(count)

    gender_items.append(html.Tr([
        html.Th('Sum'),
        html.Th(gender_count),
    ]))

    fig = px.pie(names=gender_pie_labels, values=gender_pie_values)
    fig.update_layout(legend=dict(orientation="h"))

    @app.callback(
        Output('gender-output-container', 'children'),
        [Input('gender-display-options', 'value')]
    )
    def update_output(type):
        if type == 'text':
            return html.Table(gender_items, className='table')
        return dcc.Graph(figure=fig)
    
    return html.Div([
            html.Div('Gender:', className='card-header'),
            html.Div([
            ], className='card-body', id='gender-output-container'),
            html.Div(
                dcc.RadioItems(
                options=[
                    {"label": "Text", "value": "text"},
                    {"label": "Graph", "value": "graph"},
                ],
                value="text",
                inline=True,
                id="gender-display-options",
                className='btn-group btn-group-toggle',
                labelClassName='btn btn-secondary'
            ),
            className='card-footer text-muted')
        ], className='card col-sm')