import gspread
import requests
from google.oauth2.service_account import Credentials
# -------------------------------------------------------------------------------
YANDEX_API = "23ba9181-ab9f-4c7e-a209-346f4ef7c4a9"
GEOCODE_URL = "https://geocode-maps.yandex.ru/1.x"
# -------------------------------------------------------------------------------

#                                       </FUNCTIONS/>
def geocode(address):
    params = {
        'apikey': YANDEX_API,
        'geocode': address,
        'format': 'json'
    }

    response = requests.get(GEOCODE_URL, params=params)
    if response.status_code == 200:
        data = response.json()

        try:
                pos = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
                longitude, latitude = pos.split(" ")
                return float(latitude), float(longitude)
        except (KeyError, IndexError):
            print("No results found for this address")
            return None

    else:
        print(f"Error: {response.status_code}")
        return None


def address_to_coords(addr_mat):
    return [geocode(k) for k in addr_mat]

#                                   </>

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",

]

creds = Credentials.from_service_account_file("creds.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1__of0_NMbxIDXlKTkcEbV1stP4p7qEKUIDluGWXDEZc"
workbook = client.open_by_key(sheet_id)

sheets = workbook.worksheets()
moyka = sheets[0]


# Initializing matrix [Name, Address, Type, Phone Number, Web-Site, Telegram]
matrix = moyka.get_all_values()

# Getting coordinates of all addresses from a sheet
coords = address_to_coords(k[1] for k in matrix[3:])

# Getting names
names = [k[0] for k in matrix[3:]]

# Getting type
types = [k[2] for k in matrix[3:]]

# Getting numbers
numbers = [k[3] for k in matrix[3:]]

# Getting URL's

url = [k[4] for k in matrix[3:]]

# Getting average cheque

cheque = [k[5] for k in matrix[3:]]


# Resulting matrix with names and coordinates of every car wash
result = [[names[i], coords[i], types[i], numbers[i], url[i], cheque[i]] for i in range(len(coords))]

# Saving info to coord.txt file
with open("coord.txt", "w") as txt_file:
    for el in result:
        txt_file.write(f"{el[0]};{el[1][0]};{el[1][1]};{el[2]};{el[3]};{el[4]};{el[5]}\n")
