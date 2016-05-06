# playground
please note this was built in a linux environment and has not yet been tested for ios or windows environment
# Tools and Reasoning
  The main tools used in this project were flask and Mongo DB.
  So I choose flask for a few reasons
 
1. Flask (http://flask.pocoo.org/)
  * It’s one me of my more familiar tools  
  * the framework is lightweight and very quick to set up with little to no fuss
  * Free and open sources
  * Popular and lots of community support
2. Mongo db (https://www.mongodb.com/)  
  * the number 1 nosql framework
  * easy to learn and start using
  * strong python support


#Recommendations
I recamend installing "Virtualenv" (https://virtualenv.pypa.io/en/latest/) its a nice way to keep python libs feom overwritting/conflicting with one another on seprate projects

#Installation
The following are required to successfully install and/or run:
* pip (https://pypi.python.org/pypi/pip)
* Mongo db required (https://www.mongodb.com/download-center#community)

run this command from the root of the project
* pip install -U -r requirements.txt
the requirements contains all the external python libs for the project

#Running and operating project
use the following commands
* mongod
this is to ensure that mongodb is running

to start the web service execute the following
* python run.py

you are now ready to start posting you can use any posting tool
you can post using any tool I used httprequester (https://addons.mozilla.org/en-us/firefox/addon/httprequester/) an addon for firefox for its simplicity and ease of use

make sure to post with the following:
* zwsid (your zillow id)
* address (the address you're looking for)
* zipcode (the zipcode you're looking in)

Below is an example of a valid post string:
* http://127.0.0.1:5000/?zwsid=X1-ZWz19r2ha52oej_5ywzw&address=2570%20Wildcat%20Ln&zipcode=92503
* note that if there is an error with your post you will receive an error message

this will return an Id for the property that you can use to post to the second endpoint
* 572bc8646e69690fa98abc1a (this is an example)
*



#ToDo

in order to be done this still requires unit testing however due to the time constraints(I told David 5/5/16) that will have to be added later.

#Original requirement

1. Build a small RESTFUL Api that consists of 2 endpoints.



•        Build an endpoint that'll accept parameters such as a home address to extract property data from the Zillow API. Store the Zillow response data in a NoSQL or file based Database. (Bonus point for NoSQL)

•        The application should initialize with Zillow credentials. (we will use our own credentials)

•        The second endpoint should return the Zillow estimated price given a property id.



- Helpful Zillow links

•       http://www.zillow.com/howto/api/APIOverview.htm

•       https://pypi.python.org/pypi/pyzillow
2. Deliverables

•       Source Code

•       Deployment Instructions

•       ReadMe doc

 

3. Things to consider for your 'README' doc

•       Use the technologies of your choice but please leave a small paragraph explaining why you choose that technology

•       Explain how to execute your code


