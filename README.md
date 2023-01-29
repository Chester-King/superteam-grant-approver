# Superteam Grant Approver Bot

This discord bot is supposed to read the incoming messages in discord channel and based on the reaction from Whitelisted Approver
Using Airtable as DB as it is easier to manage for operations team

## AirFile.py

AirFile contains the functions which perform airtable operations.
The functions in `airfile.py` are as suppose 

### addApprover

Function prototype - `def addApprover(channelID, userID, flag)`

It takes three inputs 

* `channelID` - Existing whitelisted channelID to which approver needs to be added
* `userID` - The approver superadmin wants to whitelist
* `flag` - This confirms that the update happened

### addChannel

Function prototype - `def addChannel(channelID, name)`

It takes two inputs 

* `channelID` - Whitelist a new channel on which the bot should start keeping watch on
* `name` - Name of the channel to add in Airtable for easier identification

### isUserApproved

Function prototype - `def isUserApproved(channelID, userID)` 

It takes two inputs 

* `channelID` - channelID on which to check if user is approved
* `userID` - userID which needs to be checked