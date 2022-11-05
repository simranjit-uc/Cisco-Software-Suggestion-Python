# ****** Import relevant libraries ******
import json, requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from tabulate import tabulate


# ****** Declare and initialize variables ******

API_TOKEN_CLIENT_ID = "<< Use the Client ID from Cisco's API Registration Output >>"
API_TOKEN_CLIENT_PASS = "<< Use the Client Password from Cisco's API Registration Output >>"
TOKEN_URL = "https://cloudsso.cisco.com/as/token.oauth2"
SFW_URL = "https://api.cisco.com/software/suggestion/v2/suggestions/software/productIds/ISR4431-SEC/K9-RF"


# ****** Use this module to ignore any SSL certificate exchange related warnings ******

disable_warnings(InsecureRequestWarning)


lst = []
tbl = []
tbl.insert(0, "IOS Name")
tbl.insert(1, "IOS Image")
tbl.insert(2, 'Release Date')
lst.insert(0, tbl)


# ****** Send a request to Cisco's Authorization Server for a new token ******

def get_Token():
    resp = requests.post(TOKEN_URL, verify=False, data={"grant_type": "client_credentials"},
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             params={"client_id": API_TOKEN_CLIENT_ID, "client_secret": API_TOKEN_CLIENT_PASS})

    json_Output = json.loads(resp.text)
    access_token = json_Output["access_token"]
    return access_token


# ****** Send a request to the Cisco's Software Suggestion API and manipulate its response ******

def get_Data():
    AUTH = "Bearer " + get_Token()
    HEADERS = {"Authorization": AUTH}
    SFW_REQUEST = requests.get(SFW_URL, headers=HEADERS, verify=False)
    resp = json.loads(SFW_REQUEST.text)
    tot_Records = resp['paginationResponseRecord']['totalRecords']

    tot_Sugg = len(resp['productList'][0]['suggestions'])


    if tot_Sugg != 0:
        for i in range(tot_Sugg):
            lst.append([])
            disp_Name = resp['productList'][0]['suggestions'][i]['relDispName']
            lst[i+1].insert(i,disp_Name)
            img_Name = resp['productList'][0]['suggestions'][i]['images'][1]['imageName']
            lst[i+1].insert(i+1, img_Name)
            rel_Date = resp['productList'][0]['suggestions'][i]['releaseDate']
            lst[i+1].insert(i+2, rel_Date)


    disp_Data = tabulate(lst, headers='firstrow', tablefmt='fancy_grid')
    print(disp_Data)


# ****** Call both functions one by one ******

get_Token()
get_Data()


