import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


def render_profit(data):
    df = data[data['LanguageHaveWorkedWith'].notna()]
    df = df[df['ConvertedCompYearly'].notna()]

    df['Language'] = df['LanguageHaveWorkedWith'].str.split(';')
    df = df.explode('Language')

    # Calculate the average yearly salary for each language
    language_salary = df.groupby('Language')['ConvertedCompYearly'].mean().reset_index()

    # Sort the languages based on the average yearly salary in descending order
    top_10_languages = language_salary.sort_values(by='ConvertedCompYearly', ascending=False).head(10)

    # Display the top 10 most profitable languages

    # Create a table to display the language data
    table = html.Table(
        [
            html.Thead(html.Tr([html.Th('#')] + [html.Th(col) for col in top_10_languages.columns]))
        ] +
        [
            html.Tr([
                html.Td(i+1)] +
                # [html.Td(top_10_languages.iloc[i][col]) for col in top_10_languages.columns
                [html.Td(top_10_languages.iloc[i][top_10_languages.columns[0]])]+
                [html.Td('${:,.2f}'.format(top_10_languages.iloc[i][top_10_languages.columns[1]]))
            ]) for i in range(len(top_10_languages))
        ]
    , className='table')

    # Set up the layout of the Dash application
    return html.Div([
          html.H2('Top 10 Most Profitable Languages'),
          table
      ], className='row')