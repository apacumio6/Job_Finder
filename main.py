# This script will 
from updateCV import updateCV
from scrapeData import scrapeData
from updateSpreadsheet import updateSpreadsheet


def main():
	print("Step 1: Scrape the data")

	# get inputs from user
	job_title = input("Job title: ")
	location = input("Enter a location (city, state):")
	radius = input("Distance from location: ")

	# scrape indeed's website for jobs
	scrapeData(job_title, location, radius)

	# update the google sheet with the jobs found
	updateSpreadsheet()

	# create a folder and cover letter for each job found
	updateCV()
	
	print("Done!")

if __name__ == '__main__':
    main()

