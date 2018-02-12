# Dependencies
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import requests
import json
import datetime
import os

def scrapeData(_job_title, _location, _radius):
	# URL of page to be scraped
	base_url = 'https://www.indeed.com/jobs?'

	# job search criteria (advanced search)
	with_all_words = ''
	with_exact_phrase = _job_title
	with_at_least_one = ''
	with_none = ''
	with_words_in_title = ''
	from_this_company = ''
	job_types = 'all'        #[fulltime, parttime, contract, internship, temporary]
	show_jobs_from = ''      #[(blank is all), jobsite, employer]
	job_source = ''          #[(blank means include staffing agencies, directhire (exclude staffing agencies)]
	salary = ''
	radius = _radius  #'5'             #[5,10,15,25,50,100 in miles]            
	location = _location #"San Mateo, CA"
	age_of_post = 'any'      #[any is default, 15, 7, 3, 1 (yesterday), last (since last visit)]
	limit = '10'               #[50, 30, 20, 10 results per page]
	sort = 'date'            #[relevance, date]
	preferred_search = 'advsrch'


	#build the query url
	query_url = base_url + "as_and=" + with_all_words + \
	            "&as_phr=" + with_exact_phrase.replace(" ", "+") + \
	            "&as_any=" + with_at_least_one + \
	            "&as_not=" + with_none + \
	            "&as_ttl=" + with_words_in_title + \
	            "&as_cmp=" + from_this_company + \
	            "&jt=" + job_types + \
	            "&st=" + show_jobs_from + \
	            "&sr=" + job_source + \
	            "&salary=" + salary + \
	            "&radius=" + radius + \
	            "&l=" + (location.replace(" ", "+")).replace(",", "%2C") + \
	            "&fromage=" + age_of_post + \
	            "&limit=" + limit + \
	            "&sort=" + sort + \
	            "&psf=" + preferred_search

	# Retrieve page with the requests module
	response = requests.get(query_url)

	# Create BeautifulSoup object; parse with 'html.parser'
	soup = BeautifulSoup(response.text, 'html.parser')


	# Get the number of jobs returned from the search
	searchCount = soup.find(id="searchCount").string
	index_of_first_blank = searchCount.find("of ")
	index_of_second_blank = searchCount.find(" job")
	len_of_searchCount = len(searchCount)
	resultCount = searchCount[(index_of_first_blank + 3):index_of_second_blank]
	print(resultCount)
	print(int(resultCount)/int(limit))
	print(query_url)

	#keep track of the page we're on (for testing purposes only)
	page_num = 0
	api_key = 'AIzaSyCo4JSr1s1WKsdMcH8sBoGNA3zDmqAlsQE'

	#create a list to store the data
	job_list = []
	job_title = ''
	job_link = ''
	company = ''
	company_location = ''
	company_lat = ''
	company_long = ''
	quick_apply = ''
	address = ''

	#modify the query url to get all of the pages
	query_url = query_url + "&start="
	for page in np.arange(0, int(resultCount), int(limit)):
	    #print(query_url + str(page))
	    
	    page_num += 1
	    # Retrieve page with the requests module
	    response = requests.get(query_url + str(page))

	    # Create BeautifulSoup object; parse with 'html.parser'
	    soup = BeautifulSoup(response.text, 'html.parser')
	    
	    # results are returned as an iterable list
	    results = soup.find_all('div', class_="result")
	    
	    for result in results:
	        #job title
	        try:
	            job_title = result.find('a', class_="jobtitle turnstileLink").text
	            print(result.find('a', class_="jobtitle turnstileLink").text)
	        except Exception as e:
	            job_title = result.find('a', class_="turnstileLink")["title"]
	            print(result.find('a', class_="turnstileLink")["title"])
	        try:
	            #company name
	            company = result.find('span', class_="company").find('a', class_="turnstileLink").text.lstrip()
	            print(result.find('span', class_="company").find('a', class_="turnstileLink").text.lstrip())
	        except Exception as e:
	            company = result.find('span', class_="company").text.lstrip()
	            print(result.find('span', class_="company").text.lstrip())

	        #location
	        company_location = result.find('span', class_="location").text
	        print(result.find('span', class_="location").text)

	        try:
	            quick_apply = result.find('span', class_="iaLabel").text
	            print(result.find('span', class_="iaLabel").text)
	        except Exception as e:
	            quick_apply = "No easy apply"
	            print("No easy apply")
	        
	        #job_link = result
	        job_link = "http://indeed.com/" + result.find('a', class_="turnstileLink")['href']

	       
	        company_name = company.replace(" ", "+")
	        company_location_name = company_location.replace(" ", "+").replace(",", "%2C")
	        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s+%s&key=%s' % (company_name, company_location_name,api_key)
	        response = requests.get(url).json()
	        
	        try:
	        	lat = response['results'][0]['geometry']['location']['lat']
	        except Exception as e:
	        	lat = ''

	        try:
	        	lng = response['results'][0]['geometry']['location']['lng']
	        except Exception as e:
	        	lng = ''

	        try:
	        	address = response['results'][0]['formatted_address']
	        except Exception as e:
	        	address = ''

	        print(lat)
	        print(lng)
	        
	        job_list.append({"job_title": job_title, "company":company, "company_location": company_location, "address" : address, "lat": lat, "lng": lng, "quick_apply":quick_apply, "job_link": job_link})

	        #print (result.find('a').get('href'))
	        print(str(page_num) + "=========================================\n")


	# export the dataframe to a csv
	jobList_df = pd.DataFrame(job_list)

	filename = 'jobList.csv'

	if (os.path.isfile(filename)):
		os.remove(filename)
	jobList_df.to_csv(filename, encoding='utf-8')        