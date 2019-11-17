# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import pymongo
#
# my_client = pymongo.MongoClient('mongodb://localhost:27017/')
# db = my_client['cardb']
# cars_collection = db['cars']
# sold_collection = db['sold']
#
# avg_price_query = cars_collection.aggregate([
#     {"$match" : {"Marka": "Volvo", "Model": "XC90"}},
#     {"$unwind": "$istorija"},
#     {"$project": {"istorijski_podaci": {"$objectToArray": "$istorija"}}},
#     {"$unwind": "$istorijski_podaci"},
#     {"$match" : {
#             "istorijski_podaci.v": {"$gt":0},
#             "istorijski_podaci.k": {"$ne":'2019-11-17'},
#         }
#     },
#     {"$group": {"_id": "$istorijski_podaci.k", "avg_price": {"$avg": "$istorijski_podaci.v"}, "max": { "$max" : "$istorijski_podaci.v" }, "min": { "$min" : "$istorijski_podaci.v" }}},
#     {"$sort": {"_id": 1}}
#
# ])
#
# sold_price_sum = sold_collection.aggregate([
#     {"$group": {"_id": "$sold_date", "total_price": {"$sum": "$cena"}, "total_cars": {"$sum": 1}, "avg_price": {"$avg": "$cena"}}},
# ])
#
#
#
# #[{'_id': '2019-11-16', 'avg_price': 7794.275741710297}, {'_id': '2019-11-14', 'avg_price': 6569.122324159021}, {'_id': '2019-11-15', 'avg_price': 8107.412331406551}, {'_id': '2019-11-17', 'avg_price': 8679.398713826367}]
# #[{'_id': '2019-11-17', 'avg_price': 8850.160655737705}, {'_id': '2019-11-14', 'avg_price': 6884.99358974359}, {'_id': '2019-11-15', 'avg_price': 8365.333996023857}, {'_id': '2019-11-16', 'avg_price': 8061.62274368231}]
#
#
# res = list(avg_price_query)
# print(res)
# res_sold = list(sold_price_sum)
# print(res_sold)
#
# basic_info_price = list(cars_collection.aggregate([
#     {"$match" : {"Marka": "Volvo", "Model": "XC90", "cena": {"$gte": 0} }},
#     { "$group" : { "_id": "null", "max": { "$max" : "$cena" }, "min": { "$min" : "$cena" }, "avg_price": {"$avg": "$cena"}}}
# ]))
#
# # min_price = list(cars_collection.aggregate([
# #     {"$match" : {"Marka": "Volvo", "Model": "XC90", "cena": {"$gte": 0}}},
# #     { "$group" : { "_id": "null", "min": { "$min" : "$cena" }}}
# # ]))
#
#
#
# # min_price = list(cars_collection.find().sort({'cena': 1}).limit(1))
#
# print(basic_info_price)
# # print(min_price)
# # print(min_price)
#
#
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),
#
#     html.Div(children='''
#         Dash: A web application framework for Python.
#     '''),
#
#     dcc.Graph(
#         id='general-by-day',
#         figure={
#             'data': [
#                 {'x': list(map(lambda x: x['_id'], res)), 'y': list(map(lambda x: x['avg_price'], res)), 'type': 'line', 'name': 'avg price per day'},
#                 {'x': list(map(lambda x: x['_id'], res)), 'y': list(map(lambda x: x['max'], res)), 'type': 'lines', 'name': 'max price per day'},
#                 {'x': list(map(lambda x: x['_id'], res)), 'y': list(map(lambda x: x['min'], res)), 'type': 'lines', 'name': 'min price per day'},
#
#
#
#             ],
#             'layout': {
#                 'title': 'Volvo XC90'
#             }
#         }
#     ),
#
#     dcc.Graph(
#         id='sold-by-day',
#         figure={
#             'data': [
#                 {'x': list(map(lambda x: x['_id'], res_sold)), 'y': list(map(lambda x: x['total_price'], res_sold)),
#                     'type': 'bar', 'name': 'SF'}
#
#             ],
#             'layout': {
#                 'title': 'Dash Data Visualization'
#             }
#         }
#     )
# ])
#
# if __name__ == '__main__':
#     app.run_server(debug=True)

# -*- coding: utf-8 -*-
from client.query_executor import executor
from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        dcc.Input(id="marka", type="text", placeholder="Marka"),
        dcc.Input(id="model", type="text", placeholder="Model"),
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=dt(1900, 1, 1),
            max_date_allowed=dt.now(),
            initial_visible_month=dt(2019, 11, 1),

        ),
        html.Div(id="output")

    ],

)

@app.callback(
    Output("output", "children"),
    [Input("marka", "value"), Input("model", "value"),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')
     ],
)
def update_output(input1, input2, start_date, end_date):

    if input1 is not None and input2 is not None and start_date is not None and end_date is not None:
        match_obj = {'Marka': input1, 'Model': input2}
        res = executor.price_history(match_obj, start_date, end_date, 'cars')
        print('from dash')
        print(res)
        gph = dcc.Graph(
                id='general-by-day',
                figure={
                    'data': [
                        {'x': res['dates'], 'y': res['prices'], 'type': 'line', 'name': 'avg price per day'},
                        # {'x': list(map(lambda x: x['_id'], res)), 'y': list(map(lambda x: x['max'], res)), 'type': 'lines', 'name': 'max price per day'},
                        # {'x': list(map(lambda x: x['_id'], res)), 'y': list(map(lambda x: x['min'], res)), 'type': 'lines', 'name': 'min price per day'},



                    ],
                    'layout': {
                        'title': input1 + ' ' + input2
                    }
                }
            )
        return gph
    else :
        return ''


if __name__ == "__main__":
    app.run_server(debug=True)