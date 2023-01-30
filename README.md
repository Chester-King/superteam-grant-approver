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

### parseText

Function prototype - `def parseText(message)`

It takes one inputs

* `message` - message from Grant Bot to be parsed to figure out the record ID

### rejectGrant

Function prototype - `def rejectGrant(message)`

It takes one inputs

* `message` - mark the grant as rejected by identifying the record ID from message

### acceptGrant

Function prototype - `def acceptGrant(message)`

It takes one inputs

* `message` - mark the grant as accepted by identifying the record ID from message

## GrantApprovalBot.py

GrantApprovalBot contains the functions which watch and act depending on the operations taking place in discord with the help of deployed discrod bot and use helper functions of `airfile.py` to communicate with Airtable.
It picks up bot token from `.env` file.

### Add Approver - command function

Function Prototype - `async def add_approver(ctx, channelID: str, userID: str)`

It takes 3 inputs 

* `ctx` - bot context
* `channelID` - channel ID on which approver needs to be added by superadmin
* `userID` - ID of the user to be added

### Add Channel - command function

Function Prototype - `async def add_channel(ctx, channelID: str,*, name: str)`

It takes 3 inputs

* `ctx` - bot context
* `channelID` - channel ID which needs to be monitored by the bot
* `name` - name of the channel for airtable which makes it easier to identify the channel.

### On Reaction Add - event function

Function Prototype - `async def on_reaction_add(reaction, user)`

It takes 2 inputs

* `reaction` - This is a complex object which gives us data about in which channel the reaction was done and the reaction details
* `user` - which user reacted to the message. 
