from app import app
from datetime import datetime
from bson.objectid import ObjectId
from flask import request
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
from pymongo import MongoClient


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/zillow_data', methods=('GET', 'POST'))
def get_data():
    if request.method == 'POST':
        if request.values.get('r_id'):
            r_id = request.values.get('r_id')
            client = MongoClient()
            db = client.zillow
            res = db.find_one({"_id": r_id})
            return 'working', r_id

    return "please post with valid 'r_id"


@app.route('/zillow', methods=('GET', 'POST'))
def zillow():
    if request.method == 'POST':
        if request.values.get('zwsid'):
            zwsid = request.values.get('zwsid')
        else:
            return "Missing zwsid"
        if request.values.get('address'):
            address = request.values.get('address')
        else:
            return "Missing address"
        if request.values.get('zipcode'):
            zipcode = request.values.get('zipcode')
        else:
            return "missing zipcode"
        zillow_data = ZillowWrapper(zwsid)
        deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
        result = GetDeepSearchResults(deep_search_response)

        client = MongoClient()
        db = client.zillow
        result = db.zillow.insert_one(
            {
                "request_time":datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
                "zillow_responce": {
                    "zillow_id": result.zillow_id,
                    "home_type": result.home_type,
                    "home_detail_link": result.home_detail_link,
                    "graph_data_link": result.graph_data_link,
                    "map_this_home_link": result.map_this_home_link,
                    "latitude": result.latitude,
                    "longitude": result.longitude,
                    "tax_year": result.tax_year,
                    "tax_value": result.tax_value,
                    "year_built": result.year_built,
                    "property_size": result.property_size,
                    "home_size": result.home_size,
                    "bathrooms": result.bathrooms,
                    "bedrooms": result.bedrooms,
                    "last_sold_date": result.last_sold_date,
                    "last_sold_price_currency": result.last_sold_price_currency,
                    "last_sold_price": result.last_sold_price,
                    "zestimate_amount": result.zestimate_amount,
                    "zestimate_last_updated": result.zestimate_last_updated,
                    "zestimate_value_change": result.zestimate_value_change,
                    "zestimate_valuation_range_high": result.zestimate_valuation_range_high,
                    "zestimate_valuationRange_low": result.zestimate_valuationRange_low,
                    "zestimate_percentile": result.zestimate_percentile
                },
                "request_information": {
                    'zwsid':zwsid,
                    'address': address,
                    'zipcode': zipcode
                },
            }
        )
        return str(result.inserted_id)
    return "please post with valid 'zwsid' 'address' 'zipcode' "