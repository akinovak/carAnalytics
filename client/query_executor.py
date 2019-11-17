from conf import ctx


class QueryExecutor:

    def __init__(self):
        self.db = ctx.db

    def price_history(self, match_object, date_begin, date_end, collection):
        avg_price_query = self.db[collection].aggregate([
                {"$match" : match_object},
                {"$unwind": "$istorija"},
                {"$project": {"istorijski_podaci": {"$objectToArray": "$istorija"}}},
                {"$unwind": "$istorijski_podaci"},
                {"$match" : {
                        "istorijski_podaci.v": {"$gt":0},
                        "istorijski_podaci.k": {"$gte": date_begin, "$lte": date_end},
                    }
                },
                {"$group": {"_id": "$istorijski_podaci.k", "avg_price": {"$avg": "$istorijski_podaci.v"}, "max": { "$max" : "$istorijski_podaci.v" }, "min": { "$min" : "$istorijski_podaci.v" }}},
                {"$sort": {"_id": 1}}

            ])

        query_res = list(avg_price_query)
        dates = list(map(lambda x: x['_id'], query_res))
        prices = list(map(lambda x: x['avg_price'], query_res))
        max_prices = list(map(lambda x: x['max'], query_res))
        min_prices = list(map(lambda x: x['min'], query_res))

        res = {'dates': dates, 'prices': prices, 'max_prices': max_prices, 'min_prices': min_prices}
        print(res)

        return res


executor = QueryExecutor()

# executor.price_history({"Marka": "Volvo", "Model": "XC90"}, "2019-11-15", "2019-11-16", "cars")