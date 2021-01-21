import argparse
import requests
import configparser
import time

parser = argparse.ArgumentParser()
parser.add_argument("-l", help="Lock your vehicle", action="store_true")
parser.add_argument("-u", help="Unlock your vehicle", action="store_true")
parser.add_argument("-s", help="Start your vehicle", action="store_true")
parser.add_argument("-k", help="Turn your vehicle off", action="store_true")
parser.add_argument("-r", help="Returns your vehicle's range", action="store_true")
parser.add_argument("-m", help="Returns your vehicle's mileage", action="store_true")
parser.add_argument("-o", help="Returns your vehicle's oil life", action="store_true")
parser.add_argument("-c", help="Returns your vehicle's coordinates", action="store_true")
parser.add_argument("-g", help="Returns a link to your vehicle's location on Google Maps", action="store_true")
parser.add_argument("-t", help="Returns your vehicle's tire pressure status", action="store_true")
parser.add_argument("-d", help="Returns your vehicle's door status", action="store_true")
parser.add_argument("-w", help="Returns your vehicle's window status", action="store_true")
parser.add_argument("-n", help="Returns vehicle's raw status", action="store_true")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read("fordpass.conf")

def main():
    if args.l:
        print(lockVehicle())
    if args.u:
        print(unlockVehicle())
    if args.s:
        print(startVehicle())
    if args.k:
        print(turnOffVehicle())
    if args.r:
        print(rangeVehicle())
    if args.m:
        print(mileageVehicle())
    if args.o:
        print(oilLifeVehicle())
    if args.c:
        print(coordinatesVehicle())
    if args.g:
        print(mapVehicle())
    if args.t:
        print(tireStatusVehicle())
    if args.d:
        print(doorStatusVehicle())
    if args.w:
        print(windowStatusVehicle())
    if args.n:
        print(getStatus())

def getToken():
    tokenHeader = {
    "Accept": "*/*",
    "Accept-Language": "en-US",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "fordpass-na/353 CFNetwork/1121.2.2 Darwin/19.3.0",
    "Accept-Encoding": "gzip, deflate, br"
    }

    body = {
    "client_id": "9fb503e0-715b-47e8-adfd-ad4b7770f73b",
    "grant_type": "password",
    "password": config["config"]["passwd"],
    "username": config["config"]["user"]
    }

    return requests.post("https://fcis.ice.ibmcloud.com/v1.0/endpoint/default/token", headers = tokenHeader, data = body).json()["access_token"]

header = {
    "auth-token": getToken(),
    "Accept": "*/*",
    "Accept-Language": "en-US",
    "Content-Type": "application/json",
    "User-Agent": "fordpass-na/353 CFNetwork/1121.2.2 Darwin/19.3.0",
    "Accept-Encoding": "gzip, deflate, br",
    "Application-Id": "71A3AD0A-CF46-4CCF-B473-FC7FE5BC4592"
}

def getStatus():
    return requests.get(f"https://usapi.cv.ford.com/api/vehicles/v4/{config['config']['vin']}/status", headers = header).json()

def lockVehicle():
    vehicleStatus = requests.put(f"https://usapi.cv.ford.com/api/vehicles/v2/{config['config']['vin']}/doors/lock", headers = header).json()
    time.sleep(int(config["config"]["timer"]))
    if vehicleStatus["status"] == 200 and getStatus()["vehiclestatus"]["lockStatus"]["value"] == "LOCKED":
        return "Vehicle Locked"
    else:
        return f"Vehicle Lock Command Failed:\n{vehicleStatus}\n" + str(getStatus()["vehiclestatus"]["lockStatus"])

def unlockVehicle():
    vehicleStatus = requests.delete(f"https://usapi.cv.ford.com/api/vehicles/v2/{config['config']['vin']}/doors/lock", headers = header).json()
    time.sleep(int(config["config"]["timer"]))
    if vehicleStatus["status"] == 200 and getStatus()["vehiclestatus"]["lockStatus"]["value"] == "UNLOCKED":
        return "Vehicle Unlocked"
    else:
        return f"Vehicle Unlock Command Failed:\n{vehicleStatus}" + str(getStatus()["vehiclestatus"]["lockStatus"])

def startVehicle():
    vehicleStatus = requests.put(f"https://usapi.cv.ford.com/api/vehicles/v2/{config['config']['vin']}/engine/start", headers = header).json()
    time.sleep(int(config["config"]["timer"]))
    if vehicleStatus["status"] == 200 and getStatus()["vehiclestatus"]["remoteStartStatus"]["value"] == 1:
        return "Engine Started"
    else:
        return f"Engine Start Command Failed:\n{vehicleStatus}" + str(getStatus()["vehiclestatus"]["remoteStartStatus"])
    
def turnOffVehicle():
    vehicleStatus = requests.delete(f"https://usapi.cv.ford.com/api/vehicles/v2/{config['config']['vin']}/engine/start", headers = header).json()
    time.sleep(int(config["config"]["timer"]))
    if vehicleStatus["status"] == 200 and getStatus()["vehiclestatus"]["remoteStartStatus"]["value"] == 0:
        return "Engine Stopped"
    else:
        return f"Engine Stop Command Failed:\n{vehicleStatus}" + str(getStatus()["vehiclestatus"]["remoteStartStatus"])

def rangeVehicle():
    return "Range: {} miles".format(int(requests.get(f"https://usapi.cv.ford.com/api/vehicles/v4/{config['config']['vin']}/status", headers = header).json()["vehiclestatus"]["fuel"]["distanceToEmpty"]))

def mileageVehicle():
    return "Vehicle Mileage: {} mi".format(int(requests.get(f"https://usapi.cv.ford.com/api/vehicles/v4/{config['config']['vin']}/status", headers = header).json()["vehiclestatus"]["odometer"]["value"]))

def oilLifeVehicle():
    return "Oil Life: {}%".format(int(requests.get(f"https://usapi.cv.ford.com/api/vehicles/v4/{config['config']['vin']}/status", headers = header).json()["vehiclestatus"]["oil"]["oilLifeActual"]))

def coordinatesVehicle():
    r = requests.get(f"https://usapi.cv.ford.com/api/vehicles/v4/{config['config']['vin']}/status", headers = header).json()["vehiclestatus"]["gps"]
    return "{} {}".format(r["latitude"], r["longitude"])

def mapVehicle():
    r = requests.get(f"https://usapi.cv.ford.com/api/vehicles/v4/{config['config']['vin']}/status", headers = header).json()["vehiclestatus"]["gps"]
    return "https://www.google.com/maps/search/?api=1&query={},{}".format(r["latitude"], r["longitude"])

def tireStatusVehicle():
    r = requests.get(f"https://usapi.cv.ford.com/api/vehicles/v4/{config['config']['vin']}/status", headers = header).json()["vehiclestatus"]["TPMS"]
    return "Tire Status:\n  Front Left: {}\n  Front Right: {}\n  Rear Left: {}\n  Rear Right: {}".format(r["leftFrontTireStatus"]["value"], r["rightFrontTireStatus"]["value"], r["outerLeftRearTireStatus"]["value"], r["outerRightRearTireStatus"]["value"])

def doorStatusVehicle():
    r = requests.get(f"https://usapi.cv.ford.com/api/vehicles/v4/{config['config']['vin']}/status", headers = header).json()["vehiclestatus"]["doorStatus"]
    return "Door Status:\n  Hood: {}\n  Front Left: {}\n  Front Right: {}\n  Rear Left: {}\n  Rear Right: {}\n  Trunk: {}".format(r["hoodDoor"]["value"], r["driverDoor"]["value"], r["passengerDoor"]["value"], r["leftRearDoor"]["value"], r["rightRearDoor"]["value"], r["tailgateDoor"]["value"])   

def windowStatusVehicle():
    r = requests.get(f"https://usapi.cv.ford.com/api/vehicles/v4/{config['config']['vin']}/status", headers = header).json()["vehiclestatus"]["windowPosition"]
    return "Window Status:\n  Front Left: {}\n  Front Right: {}\n  Rear Left: {}\n  Rear Right: {}".format(r["driverWindowPosition"]["value"], r["passWindowPosition"]["value"], r["rearDriverWindowPos"]["value"], r["rearPassWindowPos"]["value"]).replace("_"," ")

main()