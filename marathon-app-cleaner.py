# Application Name	: marathon-app-cleaner.py
# Author			: Vivek Juneja
# Created			: 11th December 2015
# Last Modified	:
# Version			: 1.0


# Description		: Removes Old applications deployed on Apache Marathon. This is used to create ephemeral applications that are removed after a configurable duration


from sys import argv
import re
from sets import Set
import random
import json
import requests
import datetime
from pytz import timezone
import argparse

only_use_groups=True    # Only delete Applicaton Groups
avoid_label_key=None    # The Marathon Label Key to be used to ignore application groups
avoid_label_value=None  # The Marathon Label Value for the Key to be used to ignore application groups
backup_directory=None

'''
Get all the app groups with their version timestamps

marathon_endpoint - http endpoint of marathon with port number
avoid_label_key - marathon application label "key" that is used to filter out the results
avoid_label_value - value of the "key" that is used to filter out the results
'''

def get_apps_version_time_dict(marathon_endpoint):
	r = requests.get("http://" + marathon_endpoint + "/v2/groups")
	#r = requests.get("http://localhost:8000/sample1.json")
	data = json.loads(r.content) 
	group_collection = []

 	''' 
 	# To consider Marathon Applications as well
 	if(only_use_groups==False):
		for app in data["apps"]:
			used_ports.append(app["ports"][0])
	'''

	for group in data["groups"]: # For each Group of Application Groups
			group_def = {}
			group_name = group["id"] 
			print "group : " + str(group_name)

			for each_group in group["groups"]: # Each Application Group 
				if (len(each_group["apps"])>0): # If there are apps in the Group
					group_version = each_group["apps"][0]["version"] # Get the latest version of the App
					group_label = each_group["apps"][0]["labels"] # Get the Labels declared fo the App
					if len(group_label) > 0: # If there are indeed any labels
						group_label_env = str(group_label[avoid_label_key]) # Get the Label Value for the key that needs to be ignored
						if(group_label_env == avoid_label_value): # If the value of the Key matches with the one that needs to be ignored
							continue # Don't add it to the removal list
					
					print 'group_version : ' + str(group_version)
					group_def[group_name] = group_version  # Add the Group Name and the Version (Time stamp) to the removal list
			
			if(len(group_def)!=0):
				group_collection.append(group_def) # Add to the collection of all Groups that are deployed on Marathon, except the ones which are to be ignored
						

	return group_collection


'''
Find Old apps on which actions can be taken (removed, archived, marked for deletion etc.)
Only checks for non-PROD applications and application groups. 
'''

def is_old_app(date, days_filter=None, hours_filter=None):

	marked_for_deletion = True
	not_marked_for_deletion = False

	
	format = "%Y-%m-%dT%H:%M:%S.%fZ" 
	d = datetime.datetime.strptime(date, format) # Format the Version timestamp in the Marathon Application JSON

	current_day_UTC = datetime.datetime.now(timezone('UTC')) # # Get the current Time in UTC Format
	
	d_utc = d.replace(tzinfo=timezone('UTC')) # Get the Version timestamp in the UTC Format
		
	date_diff = current_day_UTC - d_utc # Find the difference in time 

	
	if(days_filter != None): # Check if the Days filter is set in the command line args
		if(date_diff.days>=days_filter):  		#If the difference in dates exceeds the day filter value
			return marked_for_deletion
	elif(hours_filter != None): # Check if the Hours filter is set in the command line args
		# Find difference in number of hours
		total_difference_in_hours = date_diff.days * 24 + (date_diff.seconds / 60 / 60)
	
		if(total_difference_in_hours>=hours_filter): # If the difference in dates exceeds the hour filter value'''
			return marked_for_deletion

	# If it does not match with days or hour filter, then its NOT marked for deletion
	return not_marked_for_deletion



'''
Delete Old Applications that are marked for deletion based on the filter
conditions - Days or Hours
'''

def delete_old_apps(marathon_endpoint, days_filter=None, hours_filter=None):
	# Get list of all app groups on Marathon except the ones that are configured to be ignored
	apps_map = get_apps_version_time_dict(marathon_endpoint) 
	for item in apps_map:
		app_grp_name = item.keys()[0]
		app_grp_version_timestamp = item[app_grp_name]
		print "\n" + app_grp_name + " : " + app_grp_version_timestamp + "=>" 
		
		if (is_old_app(app_grp_version_timestamp, days_filter, hours_filter)==True):
			print "Old App. Marked for Deletion"
			save_app(marathon_endpoint, app_grp_name)
			print send_appgrp_delete_request(marathon_endpoint, app_grp_name)
		else:
			print "Old App. NOT Marked for Deletion"


'''
Save the Marathon Application deployment manifest for a given
application group Name
'''

def save_app(marathon_endpoint, app_grp_name):
	r = requests.get("http://" + marathon_endpoint + "/v2/groups/"+ app_grp_name)
	#print r.content
	fileName = backup_directory + str(app_grp_name[1:])+".json"
	print 'Saving to directory : ' + str(fileName)
	app_file = open(fileName, 'w')
	app_file.write(r.content)
	app_file.close()
	return r.content


'''
Issue delete request to Marathon endpoint for a given application group
'''

def send_appgrp_delete_request(marathon_endpoint, appgrp):
	delete_url = "http://" + str(marathon_endpoint) + "/v2/groups"+ appgrp
	r = requests.delete(delete_url)
	return r.content



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Removes old Applications on Marathon to save Capacity')
	parser.add_argument('--marathon', metavar='M', type=str,
                   help='The Marathon endpoint (eg: 10.53.15.219:18080)')
	parser.add_argument('--days', metavar='D', type=int,
                   help='Number of days old')
	parser.add_argument('--hours', metavar='H', type=int, 
                   help='Number of hours old')
	parser.add_argument('--filterkey', type=str, 
                   help='Key for the application label that needs to be filtered out')
	parser.add_argument('--filterkeyval',  type=str, 
                   help='Value of the Key for application label that needs to be filtered out')
	parser.add_argument('--backupdir',  type=str, 
                   help='Location of the Backup Directory where Old Deployment manifests would be stored')
	'''parser.add_argument('--ignoreapps',metavar='IGNORE', type=bool,
                   help='ignore Applications, and only consider Application Groups')'''
		
	args = parser.parse_args()

	only_use_groups = True
	avoid_label_key = args.filterkey
	avoid_label_value = args.filterkeyval
	backup_directory =  args.backupdir

	delete_old_apps(args.marathon, args.days, args.hours)

