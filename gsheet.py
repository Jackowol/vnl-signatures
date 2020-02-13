import gspread
import google.auth
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    '/path/to/key.json')

scoped_credentials = credentials.with_scopes(
    ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'])

client = gspread.authorize(scoped_credentials)

# Remplacer l'ID par le vrai
sheet = client.open_by_key('1GNSsDSjD7tVinR8fQXLI3PxWcxk90dNWYSskO7vzKB8').sheet1

DEBUG = False

# For testing purposes only
def findUser(email):
    print('BEGIN findUser()')
    cell = sheet.find(email)
    print(email + " repéré à " + "row : " + str(cell.row) + " col : " + str(cell.col))
    print('END findUser()')

    
def getInfo(email):
    refreshed = False

    # try block that authorizes client again if an error is detected
    try:
        cell = sheet.find(email)
    except:
        refreshed = True
        client.login()
    
    if(refreshed):
        cell = sheet.find(email)
        
    values = sheet.row_values(cell.row)

    if(DEBUG):
        print(values)
        print(len(values))

    return values
   
