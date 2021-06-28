#first Ask user what org they would want to use

import requests
import json
import csv
import subprocess

url = "https://api.meraki.com/api/v1/"

payload={}
headers = {
  'Accept': '*/*',
  'X-Cisco-Meraki-API-Key': 'd65a0f983403c6c57c480617abdee047ee1d8144',
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




def updatedevices():
	Net_ID = get_network()
	with open("devices.csv") as data:
		reader = csv.reader(data)
		count = 0
		for row in reader:
			url = "https://api.meraki.com/api/v1/networks/"+Net_ID+"/devices/"+row[0]
			payload = json.dumps({
      "name": row[1] + " " + row[2],
      "notes": row[3],
      "lanIp": row[4]
      })
      response = requests.request("PUT", url, headers=headers, data=payload)
      print(response.text)
			if count > 500:
				break
			count += 1
	



updatedevices()




