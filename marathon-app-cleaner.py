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

'''
Get all the app groups with their version timestamps
'''
def get_apps_version_time_dict(marathon_endpoint):
	r = requests.get("http://" + marathon_endpoint + "/v2/groups")
	#json_file = open(fileName)
	data = json.loads(r.content) 
	group_collection = []

 	'''
 	if(only_use_groups==False):
		for app in data["apps"]:
			used_ports.append(app["ports"][0])
	'''

	for group in data["groups"]:
			#print "group:" + str(group["id"])
			group_def = {}
			group_name = group["id"]
			for each_group in group["groups"]:
				if (len(each_group["apps"])>0):
					group_version = each_group["apps"][0]["version"]
					


			group_def[group_name] = group_version
			group_collection.append(group_def)
						

	#print used_ports
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
	#print ' current_day_UTC ' + str(current_day_UTC)
	#print current_day
	#print type(current_day)
	d_utc = d.replace(tzinfo=timezone('UTC'))
	#print '\n Subtracting current_day ' + str(current_day_UTC) + ' with given date ' + str(d_utc)
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
		print 'hours_filter : ' + str(hours_filter)
		print 'total_difference_in_hours : ' + str(total_difference_in_hours)
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
			print send_appgrp_delete_request(marathon_endpoint, app_grp_name)
		

def send_appgrp_delete_request(marathon_endpoint, appgrp):
	delete_url = "http://" + str(marathon_endpoint) + "/v2/groups"+ appgrp
	print delete_url
	r = requests.delete(delete_url)
	#data = json.loads(r.content) 
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
	'''parser.add_argument('--ignoreapps',metavar='IGNORE', type=bool,
                   help='ignore Applications, and only consider Application Groups')'''
		
	args = parser.parse_args()

	

	only_use_groups = True

	delete_old_apps(args.marathon, args.days, args.hours)

