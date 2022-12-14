from airtable import airtable
from collections import OrderedDict
import os
import json
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

superAdminUserID = os.getenv('SUPER_ADMIN_USER_ID')
superAdminUserName = os.getenv('SUPER_ADMIN_USER_NAME')
grantBotUserID = os.getenv('GRANT_BOT_USER_ID')


airtableApiKey = os.getenv('API_KEY')
airtableBaseID = os.getenv('BASE_ID')
airtableChannelTableName = os.getenv('CHANNEL_TABLE_NAME')
airtableGrantTableName = os.getenv('GRANT_TABLE_NAME')
viewUndecided = os.getenv('UNDECIDED_VIEW')

at = airtable.Airtable( airtableBaseID, airtableApiKey )

def addApprover(channelID, userID, flag):
    table = at.get(airtableChannelTableName)
    records = table['records']

    #adding an approver
    for channel in records:
        fields = channel['fields']
        fieldDict = dict(fields)
        if(fieldDict['Channel ID'] == (channelID)):
            print("Found!")
            n={}
            n['Approvers'] = fieldDict['Approvers'] + ', ' + userID
            at.update(airtableChannelTableName, channel['id'], n)
            flag = True
            
    return flag           
            
def addChannel(channelID, name):
    #adding a channel
    newData = {'Channel ID': channelID, 'Approvers': superAdminUserID, 'Grant Program': name, 'Active': 'Open'}
    at.create(airtableChannelTableName, newData)
    

    
def isUserApproved(channelID, userID):
    table = at.get(airtableChannelTableName)
    records = table['records']

    for channel in records:
        fields = channel['fields']
        fieldDict = dict(fields)
        if(fieldDict['Channel ID'] == str(channelID)):
            approvers = fieldDict['Approvers']
            approverList = approvers.split(', ')
            if str(userID) in approverList:
                print('approved to react')
                return True
    
    print('user not approved')
    return False
    
def parseText(message):
    #print(message.content)
    splitText = message.content.split('\n')
    #print(splitText)
    for line in splitText:
        if line.startswith('Record:'):
            recNo = line.split(': ')
            print(recNo[1])
            return recNo[1]
    
def rejectGrant(message):
    messageRecordID = parseText(message)
    table = at.get(airtableGrantTableName,record_id=messageRecordID)
    # records = table['records']
    print(f'messageRecordID: {messageRecordID}')
    
    if(table['fields']['Status'] == 'Undecided'):
        n={}
        n['Status'] = 'Rejected'
        at.update(airtableGrantTableName, messageRecordID, n)
        print('Grant has been rejected!')
    else:
        print('Grant already handled!')


def acceptGrant(message):
    # write to airtable for grant approved!
    messageRecordID = parseText(message)
    table = at.get(airtableGrantTableName,record_id=messageRecordID)
    # records = table['records']
    print(f'messageRecordID: {messageRecordID}')
    
    if(table['fields']['Status'] == 'Undecided'):
        n={}
        n['Status'] = 'Accepted'
        at.update(airtableGrantTableName, messageRecordID, n)
        print('Grant has been accepted!')
    else:
        print('Grant already handled!')
    #print('Grant added to approved list!')