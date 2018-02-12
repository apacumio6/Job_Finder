# This script updates the cover letter template and creates a word document
from __future__ import print_function
from mailmerge import MailMerge
from datetime import date
import os
import pandas as pd

def updateCV():

	template = "Cover_Letter_Template.docx"

	

	#read the csv of jobs
	jobs_df = pd.read_csv('jobList.csv')
	jobs_df = jobs_df[['company', 'job_title']]
	jobs_df	= jobs_df.sort_values(['company', 'job_title'])

	jobID = 1
	for row in jobs_df.itertuples():
		print(row[1])
		print(row[2])
		print('================================')
		
		document = MailMerge(template)
		print(document.get_merge_fields())

		#create a folder for each job
		try:
			folder_name = row[1].replace("/", "") + ' - ' + row[2].replace("/", "")
			os.mkdir(folder_name)
		except Exception as e:
			company_name = row[1].replace("/", "")
			job_title = row[2].replace("/", "")
			folder_name = company_name[0:10] + ' - ' + job_title[0:10]
			try:
				os.mkdir(folder_name)
			except Exception as e:
				os.mkdir(folder_name + ' - ' +str(jobID))

		document.merge(
		    company=row[1],
		    position=row[2])
		
		try:
			document.write(folder_name + '\Cover Letter.docx')
		except Exception as e:
			# append a number in case there are duplicate folder names
			document.write(folder_name + ' - ' + str(jobID) + '\Cover Letter.docx')
		jobID += 1