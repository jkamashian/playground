# playground
please note this was built in a Unix environment and has not yet been tested for ios or windows environment
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
Setup a python virtual environment for playground repo on Unix
Please note that the following steps can be used to set up a pyenv for any repo that requires one.
This example will focus on the zillow playground repo.
1. Go to playground directory and install pyenv:
    * cd /opt/qa-test/playground
    * brew install pyenv
    * brew install pyenv-virtualenv
    * vim ~/.bash_profile
2. paste the following into the file:
    * export PATH=$PATH:/url/local/bin
    * export PYENV_ROOT="/opt/qa-test/pyenv"
    * export PATH="$PYENV_ROOT/bin:$PATH"
    * eval "$(pyenv init -)"
    * eval "$(pyenv virtualenv-init -)"
3.  save and quit:
    * shift + zz
    * source ~/.bash_profile
4. Reload the shell completely:
    * exec $SHELL
5. Install the desired version of python for the virtual environment
    * cd /opt/qa-test/playground
    * pyenv install 2.7.10
    * pyenv virtualenv 2.7.10 playground
    * check the github site for more info: https://github.com/yyuu/pyenv
6. Setup automatic initialization
    * vim /opt/qa-test/pyenv/versions/playground/lib/python2.7/site-packages/playground.pth
    * insert "/opt/qa-test/playground"  (without quotes)
    * shift + zz
7. Initialize pyenv
    * cd /opt/qa-test/playground
    * pyenv local playground

#Installation
1. The following are required to successfully install and/or run:
    * pip (https://pip.pypa.io/en/stable/installing/)
    * Mongo db required (https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)

2. run this command from the root of the project
    * cd /opt/qa-test/playground
    * pip install -U -r requirements.txt
    * the requirements contains all the external python libs for the project

#Running and operating project
1. use the following commands
    * sudo mkdir /data/db
    * sudo chmod -R 777 /data/db
    * mongod
    * this is to ensure that mongodb is running

2. to start the web service execute the following
    * python run.py

#Posting Options
You are now ready to start posting you can use any posting tool
You can post using any tool I used httprequester (https://addons.mozilla.org/en-us/firefox/addon/httprequester/) an addon for firefox for its simplicity and ease of use

1. make sure to post with the following:
    * zwsid (your zillow id)
    * address (the address you're looking for)
    * zipcode (the zipcode you're looking in)

2. Below is an example of a valid post string:
    * http://127.0.0.1:5000/?zwsid=X1-ZWz19r2ha52oej_5ywzw&address=2570%20Wildcat%20Ln&zipcode=92503
    * note that if there is an error with your post you will receive an error message

    this will return an Id for the property that you can use to post to the second endpoint
    * 572bc8646e69690fa98abc1a (this is an example)



#UnitTest
This section will discuss how to run the unittest for playground
1. Before running any unittest you must make sure that the api is running
    * cd /opt/qa-test/playground
    * python run.py
2. In order to run all the unittests run the following
    * cd /opt/qa-test/playground
    * python -m unittest discover
- There are two tests in total:
    * test_views_zillow: will test getting data from zillow and insert into mongodb
        * In this method there are two fixtures that you can use, a fail and a success, please make sure to test both fixtures.
    * test_views_get_data: will test getting zillow_estimated price from mongodb
        * Please make sure to test this with both fail and success fixtures from test_views_zillow.


#Original requirement

1. Build a small RESTFUL Api that consists of 2 endpoints.
    * Build an endpoint that'll accept parameters such as a home address to extract property data from the Zillow API. Store the Zillow response data in a NoSQL or file based Database. (Bonus point for NoSQL)
    * The application should initialize with Zillow credentials. (we will use our own credentials)
    * The second endpoint should return the Zillow estimated price given a property id.

2. Helpful Zillow links
    * http://www.zillow.com/howto/api/APIOverview.htm
    * https://pypi.python.org/pypi/pyzillow
3. Deliverables
    * Source Code
    * Deployment Instructions
    * ReadMe doc
4. Things to consider for your 'README' doc
    * Use the technologies of your choice but please leave a small paragraph explaining why you choose that technology
    * Explain how to execute your code


