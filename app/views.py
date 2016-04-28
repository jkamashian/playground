from app import app
from flask import request
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/zillow', methods=('GET', 'POST'))
def zillow():
    if request.method == 'POST':
        print 'request:',request
        print 'headers:', request.headers
        print 'values:',request.values
        print 'args:',request.args
        print 'form:',request.form
        zwsid = request.args['zwsid']
        address = request.args['address']
        zipcode = request.args['zipcode']
        zillow_data = ZillowWrapper(zwsid)
        deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
        print "here"
        result = GetDeepSearchResults(deep_search_response)
        print 'z:',result.zestimate_amount


        return "Zillow pOSTER for life!!{} {} {}".format(zwsid,address,zipcode)
    else:
        return "Zillow getter"