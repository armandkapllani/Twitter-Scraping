#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 18:05:37 2018

@author:        Armand Kapllani
@department:    Economics 
@institute:     University of Florida
"""

#=============================================================================#
#+++++++++++++++++++ Scraping Specific Tweeter Hashtags ++++++++++++++++++++++#
#=============================================================================#
#______________________________________________________________________________
#                                                                             
# Twitter search using latitude and longitude                                 
#       + Perform a search for tweets close to latitude and longitude         
#       + Save the results to a CSV file                                      
#______________________________________________________________________________

# Identify the latitude and longtitude of a given city
from geopy import geocoders 
gn = geocoders.GeoNames(username='akapllani')
loc = gn.geocode("Tirana, Albania", exactly_one = False)[0]
loc[1]


latitude  = float(input('Enter the latitude:'))
longitude = float(input('Enter the longitude:'))
print('The latitude and longitude are', latitude, 'and', longitude, 
      'respectively', '.') 

#______________________________________________________________________________

# Create a dictionary 
credentials = {}  


# Provide your credentials [obtain credentials from Twitter app]
credentials['CONSUMER_KEY']    = '***'  
credentials['CONSUMER_SECRET'] = '***'
credentials['ACCESS_TOKEN']    = '***' 
credentials['ACCESS_SECRET']   = '***'


# Save the credentials object to file
with open("twitter_credentials.json", "w") as file:  
    json.dump(credentials, file)


# Load credentials from the json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)
    
# Instantiate an object 
twitter = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
                        creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

#______________________________________________________________________________

# Open a .csv file and create a csv writer object
import csv
output     = "output.csv"
open_csv   = open(output, "w")
csv_writer = csv.writer(open_csv)


# Headings to the csv file
row = [ "user", "text", "latitude", "longitude" ]
csv_writer.writerow(row)

#______________________________________________________________________________

# Twitter API only allows us to query up to 100 tweets at a time

search_range = 1            # Set the range of search in kilometers 
num_results  = 50           # Minimum number of results to obtain
tweet_count  = 0            # Count the results    
last_id      = None              

while tweet_count <  num_results:
    
    tweets = twitter.search(q = "Gainesville", 
                           geocode      = "%f,%f,%dkm" % (latitude, longitude, 
                                                          search_range), 
                           count        = 100, 
                           max_id       = last_id, 
                           result_type  ='mixed')

    for tweet in tweets["statuses"]:
        
        # Keep only users that provide geo data
        if tweet["geo"]:
            
            user_name   = tweet["user"]["screen_name"]
            text        = tweet["text"]
            text        = text.encode('ascii', 'replace')
            latitude    = tweet["geo"]["coordinates"][0]
            longitude   = tweet["geo"]["coordinates"][1]
            
            # Column names
            row = [user_name, text, latitude, longitude]
            # Write each row 
            csv_writer.writerow(row)
            
            tweet_count += 1
            
        last_id = tweet["id"]
    print("got %d results" % tweet_count)
#______________________________________________________________________________

# Close and save the .csv file
open_csv.close()
print("written to %s" % output)






