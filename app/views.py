from app import app
from datetime import datetime
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import request
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, ZillowError
from pymongo import MongoClient


VALID_ZAZ_ERR = "please post with valid 'zwsid' 'address' 'zipcode' "
VALID_R_ID_ERR = "please post with valid 'r_id'"
VALID_ZWSID_ERR = "Missing 'zwsid'"
VALID_ADDRESS_ERR = "Missing 'address'"
VALID_ZIPCODE_ERR = "missing 'zipcode'"

@app.route('/zillow_data', methods=('GET', 'POST'))
def get_data():
    """
    Returns zestimate_amount with a valid r_id
    if a user enters an invalid r_id or dosen't post
    return VALID_R_ID_ERR error message
    """
    if request.method == 'POST':
        if request.values.get('r_id'):
            try:
                r_id = request.values.get('r_id')
                client = MongoClient()
                db = client.zillow
                coll = db.zillow
                res = coll.find_one({"_id": ObjectId(r_id)})

                print 'r_id:', r_id
                if res:
                    return res['zillow_responce'].get('zestimate_amount')
            except InvalidId:
                pass

    return VALID_R_ID_ERR


@app.route('/', methods=('GET', 'POST'))
@app.route('/zillow', methods=('GET', 'POST'))
def zillow():
    """
    returns r_id with a valid search
    returns VALID_ZAZ_ERR with invalid search
    returns VALID_ZWSID_ERR with missing zwsid
    returns VALID_ADDRESS_ERR with missing address
    returns VALID_ZIPCODE_ERR with missing zipcode
    """
    if request.method == 'POST':
        if request.values.get('zwsid'):
            zwsid = request.values.get('zwsid')
        else:
            return VALID_ZWSID_ERR
        if request.values.get('address'):
            address = request.values.get('address')
        else:
            return VALID_ADDRESS_ERR
        if request.values.get('zipcode'):
            zipcode = request.values.get('zipcode')
        else:
            return VALID_ZIPCODE_ERR
        try:
            zillow_data = ZillowWrapper(zwsid)
            deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
            result = GetDeepSearchResults(deep_search_response)
        except ZillowError:
            return VALID_ZAZ_ERR

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
    return VALID_ZAZ_ERR
