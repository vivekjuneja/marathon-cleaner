from sys import argv
import re
from sets import Set
import random
import json
import requests
import datetime
from pytz import timezone
import argparse

only_use_groups=True
avoid_label_key=None
avoid_label_value=None

'''
Get all the app groups with their version timestamps

marathon_endpoint - http endpoint of marathon with port number
avoid_label_key - marathon application label "key" that is used to filter out the results
avoid_label_value - value of the "key" that is used to filter out the results

'''
def get_apps_version_time_dict(marathon_endpoint):
	#r = requests.get("http://" + marathon_endpoint + "/v2/groups")
	r = requests.get("http://localhost:8000/sample1.json")
	data = json.loads(r.content) 
	group_collection = []

 	'''
 	if(only_use_groups==False):
		for app in data["apps"]:
			used_ports.append(app["ports"][0])
	'''
	for group in data["groups"]:
			group_def = {}
			group_name = group["id"]
			print "group : " + str(group_name)
			for each_group in group["groups"]:
				if (len(each_group["apps"])>0):
					group_version = each_group["apps"][0]["version"]
					group_label = each_group["apps"][0]["labels"]
					if len(group_label) > 0:
						group_label_env = str(group_label[avoid_label_key])
						if(group_label_env == avoid_label_value):
							continue
					
					print 'group_version : ' + str(group_version)
					group_def[group_name] = group_version
			
			if(len(group_def)!=0):
				group_collection.append(group_def)
						

	return group_collection


'''
Find Old apps on which actions can be taken (removed, archived, marked for deletion etc.)
Only checks for non-PROD applications and application groups. 
'''
def is_old_app(date, days_filter=None, hours_filter=None):

	marked_for_deletion = True
	not_marked_for_deletion = False

	
	format = "%Y-%m-%dT%H:%M:%S.%fZ" #2015-12-10T02:41:59.588Z - sample time
	d = datetime.datetime.strptime(date, format)
	current_day = datetime.datetime.today()
	current_day_UTC = datetime.datetime.now(timezone('UTC'))
	d_utc = d.replace(tzinfo=timezone('UTC'))
		
	date_diff = current_day_UTC - d_utc

	'''Check Filter'''
	if(days_filter != None):
		'''If the difference in dates exceeds the day filter value'''
		if(date_diff.days>=days_filter): 
			return marked_for_deletion
	elif(hours_filter != None):
		'''Find difference in number of hours'''
		total_difference_in_hours = date_diff.days * 24 + (date_diff.seconds / 60 / 60)
		'''If the difference in dates exceeds the hour filter value'''
		if(total_difference_in_hours>=hours_filter):
			return marked_for_deletion

	return not_marked_for_deletion


def delete_old_apps(marathon_endpoint, days_filter=None, hours_filter=None):
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


def save_app(marathon_endpoint, app_grp_name):
	r = requests.get("http://" + marathon_endpoint + "/v2/groups/"+ app_grp_name)
	#print r.content
	app_file = open(app_grp_name[1:]+".json", 'w')
	app_file.write(r.content)
	app_file.close()
	return r.content



def send_appgrp_delete_request(marathon_endpoint, appgrp):
	delete_url = "http://" + str(marathon_endpoint) + "/v2/groups"+ appgrp
	r = requests.delete(delete_url)
	return r.content

'''
For decorating the output as per needs of Bash Script
'''
def render_bash_output(array):
	bash_array=""
	for item in array:
		bash_array += str(item) + " "
	return (bash_array.strip())


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
	'''parser.add_argument('--ignoreapps',metavar='IGNORE', type=bool,
                   help='ignore Applications, and only consider Application Groups')'''
		
	args = parser.parse_args()

	

	only_use_groups = True
	avoid_label_key = args.filterkey
	avoid_label_value = args.filterkeyval

	delete_old_apps(args.marathon, args.days, args.hours)

