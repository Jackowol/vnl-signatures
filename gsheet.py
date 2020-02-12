import gspread
from oauth2client.service_account import ServiceAccountCredentials



# API Credentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('projet-signatures-90b29f9573cc.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1GNSsDSjD7tVinR8fQXLI3PxWcxk90dNWYSskO7vzKB8').sheet1

DEBUG = False

#asasd


def findUser(email):
    """
    For testing purposes only.
    """
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
    
    # adresse du bureau 1
    values[9] = values[9].split('\n')
    
    if(values[10]):
        values[10] = values[10].split('\n')

    if(DEBUG):
        print(values)
        print(len(values))
    return values
   
