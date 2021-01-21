# fordpass
A Python3 script to interact with and retrieve data about your FordPass enabled vehicle

## Requirements

The only dependencies are a Ford vehicle that suports FordPass, a valid FordPass account, the 'requests' Python library. 

## Install

First, you will need the username, password, and VIN for your Ford.  Store these values in fordpass.conf.  Remember to take proper security measures to protect this file. 

Next, make sure you have 'requests' installed:

`pip3 install requests`

## Usage

Once your config file is complete, run the script with one or more of these flags:

```
python3 fordpass.py [arguments]

arguments:
  -h, --help  show this help message and exit
  -l          Lock your vehicle
  -u          Unlock your vehicle
  -s          Start your vehicle
  -k          Turn your vehicle off
  -r          Returns your vehicle's range
  -m          Returns your vehicle's mileage
  -o          Returns your vehicle's oil life
  -c          Returns your vehicle's coordinates
  -g          Returns a link to your vehicle's location on Google Maps
  -t          Returns your vehicle's tire pressure status
  -d          Returns your vehicle's door status
  -w          Returns your vehicle's window status
  -n          Returns vehicle's raw status
  ```


When interacting with the vehicle (locking/unlocking, remote start, etc), there is a deliberate delay to give time for the vehicle to execute the commands and change status.  If you are seeing errors when interacting, you can modify the 'timer' value in fordpass.conf to a high number. 

Use cases from here are wide open.  You can trigger automations when you get home to automatically lock doors, kill the engine, and alert you if you left a window open.  You could monitor your tire pressure once per day and alert when one gets low.  

## Example Output

![alt text](https://raw.githubusercontent.com/p4lsec/fordpass/main/demo.png "Logo Title Text 1")
