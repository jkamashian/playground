from app import app
from flask import request
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
from pymongo import MongoClient
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/zillow', methods=('GET', 'POST'))
def zillow():
    client = MongoClient()
    db = client.zillow
    coll = db.zillow_set
    if request.method == 'POST':
        #print 'request:',request
        #print 'headers:', request.headers
        #print 'values:',request.values
        #print 'args:',request.args
        #print 'form:',request.form
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
        #print "here"
        result = GetDeepSearchResults(deep_search_response)
        #print result
        #print 'z:',result.zestimate_amount
        result = db.zillow.insert_one(
            {
                "request_time":datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
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
        print result
        return "Zillow pOSTER for life!!{} {} {}".format(zwsid,address,zipcode)

    else:
        return "Zillow getter"