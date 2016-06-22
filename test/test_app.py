#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  test_app
# ------------------------------------------------------------------------------
from __future__ import unicode_literals, print_function, absolute_import
from unittest import TestCase
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from requests.exceptions import ConnectionError

base_url = "http://127.0.0.1:5000"

class TestApp(TestCase):
    @property
    def collection(self):
        """
        :return: Zillow mongoDB collection
        """
        client = MongoClient()
        return client.zillow.zillow

    def validate_id(self, _id):
        """
        Validates weather the id returned from api exists in mongodb
        :param _id: id from api response
        :return: boolean
        """
        try:
            res = self.collection.find_one({"_id": ObjectId(_id)})
            if res:
                return True
        except InvalidId:
            return False


    def test_views_zillow(self, clean=True):
        """
        Test getting info from zillow on a property and confirm that it get
        inserted into mongoDB successfully
        :param clean: Boolean to determine weather to clean up after it self
        :return: The mongo object id for the data inserted

        success fixture:
            fixture = dict(zwsid='X1-ZWz1f5677kiadn_6bk45',
                           address='16212 Haynes',
                           zipcode='91406')
        fail fixture:
            fixture = dict(zwsid='X1-ZWz1f5677kiadn_6bk45',
                           address='640 Clearwater Ln',
                           zipcode='83127')

        """
        url = base_url + "/zillow"
        fixture = dict(zwsid='X1-ZWz1f5677kiadn_6bk45',
                       address='16212 Haynes',
                       zipcode='91406')
        try:
            response = requests.request("POST", url, data=fixture)
        except ConnectionError as e:
            raise self.failureException("Test Failed because the app is not "
                                        "running, please run 'python run.py'"
                                        " from project root.")
        print(response.text)
        self.assertTrue(self.validate_id(response.text), "Failed to find "
                                                         "response ID in "
                                                         "MongoDB")
        if clean is True:
            self.collection.remove({"_id": ObjectId(response.text)})
        return response.text

    def test_views_get_data(self):
        """
        Test getting the zillow estimated price from our api
        * This test will use test_views_zillow inorder to get it's fixture data,
        if unittest test_views_zillow fails this test will also fail
        """
        url = base_url + "/zillow_data"
        fixture = dict(r_id=self.test_views_zillow(clean=False))
        try:
            response = requests.request("POST", url, data=fixture)
        except ConnectionError as e:
            raise self.failureException("Test Failed because the app is not "
                                        "running, please run 'python run.py'"
                                        " from project root.")
        print(fixture, response.text)
        self.assertEqual(response.text, '497076')
        self.collection.remove({"_id": ObjectId(fixture['r_id'])})