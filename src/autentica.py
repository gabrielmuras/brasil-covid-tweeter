# -*- coding: utf-8 -*-
import os
import tweepy

class Autentica:

    def api(self, consumer_key, consumer_secret, access_token ,access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        return api

    def usuario(self, api):

        user = api.me()
        return user
