
import requests
import json
import csv
import subprocess
import os

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


#Create New CSV FIle
def createcsv():
	filename = input("What do you want to name your file?\n")
	filename = filename + ".csv"
	subprocess.call('powershell.exe New-Item -Name ' + filename + " " + '-ItemType "file"', shell=True)
	return filename

#get network devices and then export as CSV
def getNetworkDevices():
	
	payload={}
	devices = requests.request("GET", url + "networks/" + get_network() + "/devices", headers=headers, data=payload)
	devices = devices.json()
	deviceinfo = []
	file = createcsv()
	for val in range(len(devices)):
		deviceinfo.append(devices[val]["serial"])
		deviceinfo.append(devices[val]["name"])
		deviceinfo.append(devices[val]["model"])
		deviceinfo.append(devices[val]["mac"])
		with open(file, "a", newline= '') as data:
			csv_writer = csv.writer(data, quoting =csv.QUOTE_ALL) 
			csv_writer.writerow(deviceinfo)
		deviceinfo = []
	
getNetworkDevices()

