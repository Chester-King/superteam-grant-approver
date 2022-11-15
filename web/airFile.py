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
            fieldDict['Approvers'] += ', ' + userID
            at.update(airtableChannelTableName, channel['id'], fieldDict)
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
    table = at.get(airtableGrantTableName,view=viewUndecided)
    records = table['records']
    messageRecordID = parseText(message)
    print(f'messageRecordID: {messageRecordID}')
    
    for grant in records:
        #print(grant)
        fields = grant['fields']
        fieldDict = dict(fields)
        #print(f'\n\n{fieldDict}\n')
        recordID = fieldDict['RecordID']
        status = fieldDict['Status']
        submitter = fieldDict['Submitter']
        print(f'OG ID: {grant["id"]}, submitter: {submitter}, record ID: {recordID}, status: {status}')
        if messageRecordID == recordID:
            if status == 'Undecided':
                n={}
                n['Status'] = 'Rejected'
                fieldDict['Status'] = 'Rejected'
                at.update(airtableGrantTableName, grant['id'], n)
                print('Grant set as Rejected!')
            else:
                print('Grant already handled!')
            break


def acceptGrant(message):
    # write to airtable for grant approved!
    table = at.get(airtableGrantTableName,view=viewUndecided)
    records = table['records']
    messageRecordID = parseText(message)
    print(f'messageRecordID: {messageRecordID}')
    
    for grant in records:
        #print(grant)
        fields = grant['fields']
        fieldDict = dict(fields)
        #print(f'\n\n{fieldDict}\n')
        recordID = fieldDict['RecordID']
        status = fieldDict['Status']
        submitter = fieldDict['Submitter']
        print(f'OG ID: {grant["id"]}, submitter: {submitter}, record ID: {recordID}, status: {status}')
        if messageRecordID == recordID:
            if status == 'Undecided':
                n={}
                n['Status'] = 'Accepted'
                at.update(airtableGrantTableName, grant['id'], n)
                print('Grant set as Accepted!')
            else:
                print('Grant already handled!')
            break
    #print('Grant added to approved list!')