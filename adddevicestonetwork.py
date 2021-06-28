#The purpose of this script is to help imoort devices into a specific network from a CSV


#first Ask user what org they would want to use

import requests
import json
import csv
import subprocess

url = "https://api.meraki.com/api/v1/"

payload={}
headers = {
  'Accept': '*/*',
  'X-Cisco-Meraki-API-Key': '',
  'Content-Type': 'application/json'

}


#First Get Organizations the user has Access To
def get_orgs():
	orgs = requests.request("GET", url + "organizations", headers=headers, data=payload)
	orgs = orgs.json()
	organizations = []
	for val in range(len(orgs)):
		organizations.append((orgs[val]["name"]))
	print(organizations)

	orgname = input("Above is the organizations you have access to. Which do you want to add devices to?\n")
	Org_id = ""
	if orgname in organizations:
		for val in range(len(orgs)):
			if((orgs[val]["name"])) == orgname:
				return ((orgs[val]["id"]))

		
# Get Network You Want to Add Devices
def get_network():
	networks = requests.request("GET", url + "organizations/" + get_orgs() + "/networks", headers=headers, data=payload)
	networks = networks.json()
	network_names = []
	for val in range(len(networks)):
		network_names.append((networks[val]["name"]))
	print(network_names)

	netname = input("Above is the networks you have access to. Which do you want to add devices to?\n")
	net_id = ""
	if netname in network_names:
		for val in range(len(networks)):
			if ((networks[val]["name"])) == netname:
				return ((networks[val]["id"]))
#Grab Serials From CSV
def get_serials():
	with open("serials.csv") as data:
		reader = csv.reader(data)
		count = 0
		serial_list = []
		for row in reader:
			serial_list.append(row[0])
			if count > 100:
				break
			count += 1
		return serial_list


# Add Devices from CSV into network specified above
def claim_devices():

	payload = json.dumps({
	  "serials": get_serials()
	})
	
	response = requests.request("POST", url + "networks/" + get_network() + "/devices/claim", headers=headers, data=payload)

	print(response.text)




print(get_serials())
claim_devices()	














