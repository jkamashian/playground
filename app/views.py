from app import app
from datetime import datetime
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import request
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, ZillowError
from pymongo import MongoClient
import logging
log = logging.getLogger('app')


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
    if request.method in ['POST', 'GET']:
        if request.values.get('r_id'):
            try:
                r_id = request.values.get('r_id')
                client = MongoClient()
                db = client.zillow
                coll = db.zillow
                res = coll.find_one({"_id": ObjectId(r_id)})

                log.debug('r_id: %s' % r_id)
                if res:
                    z_est = res['zillow_responce'].get('zestimate_amount')
                    return "$" + '{:20,}'.format(int(z_est)).strip()
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
    if request.method in ['POST', 'GET']:
        if request.values.get('zwsid'):
            zwsid = request.values.get('zwsid')
            log.debug(zwsid)
        else:
            return VALID_ZWSID_ERR
        if request.values.get('address'):
            address = request.values.get('address')
            log.debug(address)
        else:
            return VALID_ADDRESS_ERR
        if request.values.get('zipcode'):
            zipcode = request.values.get('zipcode')
            log.debug(request)
        else:
            return VALID_ZIPCODE_ERR
        try:
            zillow_data = ZillowWrapper(zwsid)
            deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
            result = GetDeepSearchResults(deep_search_response)
        except ZillowError as e:
            log.error(e)
            return VALID_ZAZ_ERR

        client = MongoClient()
        db = client.zillow
        mongo_result = db.zillow.insert_one(
            {
                "request_time":datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
                "zillow_responce": {
                    "zillow_id": getattr(result, "zillow_id"),
                    "home_type": getattr(result, "home_type"),
                    "home_detail_link": getattr(result, "home_detail_link"),
                    "graph_data_link": getattr(result, "graph_data_link"),
                    "map_this_home_link": getattr(result, "map_this_home_link"),
                    "latitude": getattr(result, "latitude"),
                    "longitude": getattr(result, "longitude"),
                    "tax_year": getattr(result, "tax_year"),
                    "tax_value": getattr(result, "tax_value"),
                    "year_built": getattr(result, "year_built"),
                    "property_size": getattr(result, "property_size"),
                    "home_size": getattr(result, "home_size"),
                    "bathrooms": getattr(result, "bathrooms"),
                    "bedrooms": getattr(result, "bedrooms"),
                    "last_sold_date": getattr(result, "last_sold_date"),
                    "last_sold_price_currency": getattr(result, "last_sold_price_currency"),
                    "last_sold_price": getattr(result, "last_sold_price"),
                    "zestimate_amount": getattr(result, "zestimate_amount"),
                    "zestimate_last_updated": getattr(result, "zestimate_last_updated"),
                    "zestimate_value_change": getattr(result, "zestimate_value_change"),
                    "zestimate_valuation_range_high": getattr(result, "zestimate_valuation_range_high"),
                    "zestimate_valuationRange_low": getattr(result, "zestimate_valuationRange_low"),
                    "zestimate_percentile": getattr(result, "zestimate_percentile")
                },
                "request_information": {
                    'zwsid':zwsid,
                    'address': address,
                    'zipcode': zipcode
                },
            }
        )
        return str(mongo_result.inserted_id)
    return VALID_ZAZ_ERR
