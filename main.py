import pandas as pd
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from views import render_general_statistic, render_salary_statistic, render_language_view, render_profit

print("hello world")

# url = "https://drive.google.com/file/d/1mYWGZFfX5YdkIFpcCAUkrMsENQncq5RA/view?usp=drive_link"
url = "data/survey_results_public.csv"
data = pd.read_csv(url)

# filter values

# # sex section
# sex_df = data[data['Sexuality'].notna()]
# sex_df['Sexuality'] = sex_df['Sexuality'].str.split(';')
# sex_df = sex_df.explode('Sexuality')
# sex_value_counts = sex_df['Sexuality'].value_counts().sort_values(ascending=False).sort_index()
# sex_items = []
# sex_count = 0
# for value, count in sex_value_counts.items():
#     sex_count += count
#     sex_items.append(html.Tr([html.Td(value), html.Td(count)]))
# sex_items.append(html.Tr([
#     html.Th('Sum'),
#     html.Th(sex_count),
# ]))

app = dash.Dash(__name__)

# applayout section
app.layout = html.Div([
    html.H1("StackOverflow statistics"),

    html.Hr(),

    render_general_statistic(app, data),

    html.Hr(),

    render_salary_statistic(app, data),

    html.Hr(),

    render_language_view(app, data),

    html.Hr(),

    render_profit(data),

    html.Hr(),

], className='container')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)