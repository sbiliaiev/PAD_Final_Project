import dash_html_components as html
from .age import render_age_statistic
from .gender import render_gender_statistic
from .salary import render_salary_statistic

def render_general_statistic(app, data):
    return  html.Div([

        render_age_statistic(app, data),

        render_gender_statistic(app, data)

    ], className='row')
