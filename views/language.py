import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


def render_language_view(app, data):
    lang_worked_df = data[data['LanguageHaveWorkedWith'].notna()]
    lang_want_df = data[data['LanguageWantToWorkWith'].notna()]

    work_language_counts = {}
    want_language_counts = {}

    for languages in lang_worked_df['LanguageHaveWorkedWith']:
        for language in languages.split(';'):
            if language != '':
                if language in work_language_counts:
                    work_language_counts[language] += 1
                else:
                    work_language_counts[language] = 1

    for languages in lang_want_df['LanguageWantToWorkWith']:
        for language in languages.split(';'):
            if language != '':
                if language in want_language_counts:
                    want_language_counts[language] += 1
                else:
                    want_language_counts[language] = 1


    # Create a DataFrame for work_language_counts
    work_df = pd.DataFrame({'Language': list(work_language_counts.keys()), 'Worked with': list(work_language_counts.values())})

    # Create a DataFrame for want_language_counts
    want_df = pd.DataFrame({'Language': list(want_language_counts.keys()), 'Want to work with': list(want_language_counts.values())})

    # Combine the DataFrames
    combined_df = pd.merge(work_df, want_df, on='Language', how='outer').fillna(0)

    @app.callback(
        Output('language-output-container', 'children'),
        [Input('language-dropdown', 'value')]
    )
    def update_output(type):
        if type == 'work':
            sorted_df = combined_df.sort_values(by='Worked with', ascending=False)
        else:
            sorted_df = combined_df.sort_values(by='Want to work with', ascending=False)
        
        fig = px.histogram(sorted_df, x='Language', y=['Worked with', 'Want to work with'],
                   barmode='group', title='Language Occurrences', width=1200)
    
        # fig.update_layout(xaxis={'categoryorder':'total descending'})

        return dcc.Graph(figure=fig)

    return html.Div([
        html.Div(id='language-output-container'),
        dcc.Dropdown(
            id='language-dropdown',
            options=[
                {'label': 'Language worked with', 'value': 'work'},
                {'label': 'Language want to work with', 'value': 'want'}
            ],
            value='work',
            clearable=False
        ),
    ], className='row')

    