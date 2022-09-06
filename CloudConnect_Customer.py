import requests


#Setting up credentials for Token Check

API_Key = 'blah'
username = 'blah'
password = 'blah'

payload = {
    'grant_type': 'password',
    'username': username,
    'password': password
}


#Receiving and saving token info
Find_Token = requests.post(url='https://cloud.wago.com/api/token',
                           headers= {'Content-Type': 'application/x-www-form-urlencoded'},
                           data=payload)


Auth_Token = Find_Token.json().get('access_token')



#Request Subscriptions
subscriptions = requests.get(url= 'https://cloud.wago.com/api/core/subscriptions?api-version=1.0',
                             headers= {'Authorization': 'Bearer ' + Auth_Token,'api-key': API_Key})
#print(subscriptions.json())



#Found subscriptions
#subscriptionId = subscriptions.json()[1].get('id') #Grab the ID value of a specific subscription

for i in range(0, len(subscriptions.json())):
    if subscriptions.json()[i].get('name') == 'WAGO':
        subscriptionId = subscriptions.json()[i].get('id')


#Creating a dictionary of Name/ID pairs
Workspaces = requests.get(url= 'https://cloud.wago.com/api/core/subscriptions/'
                               +subscriptionId+ '/workspaces?api-version=1.0',
                          headers= {'Authorization': 'Bearer ' + Auth_Token,'api-key': API_Key})

#print(Workspaces.json())



#Find The ID of the Profile you'd like to copy and the ID of the party you'd like to copy to
for i in range(0, len(Workspaces.json())):
    if Workspaces.json()[i].get('name') == 'Adam Reeve':
        AdamsID = Workspaces.json()[i].get('id')
        #print(AdamsID)
    if Workspaces.json()[i].get('name') == 'Joe Abdelmalak':
        JoesID = Workspaces.json()[i].get('id')
        #print(JoesID)




#Find the Alarm config and save it of the party you want to copy

AlarmConfig = requests.get(url= 'https://cloud.wago.com/api/alarmapp/alarmconfigurations?WorkspaceId='
                                +AdamsID +'&api-version=2.0',
                           headers= {'Authorization': 'Bearer ' + Auth_Token,'api-key': API_Key})
#print(AlarmConfig.json())


ValueBasedAlarms = []
ConnectionBasedAlarms = []
PlcStatusBasedAlarms = []
TimeIntervalBasedAlarms = []
TelemetryDataTimeoutBasedAlarms = []
AlarmFlagBasedAlarms = []

#Set Variables to Copy all the alarm configuration information

for i in range(0, len(AlarmConfig.json())):

    if AlarmConfig.json()[i].get('type')== 'ValueBased':
        if i == 0:
            ValueBasedAlarms = [AlarmConfig.json()[i]]
        if i > 0 :
            ValueBasedAlarms.append(AlarmConfig.json()[i])







        #print(ValueBasedAlarms[0])
#print(ValueBasedAlarms)



"""
    if AlarmConfig.json()[i].get('type')== 'ConnectionBased':
        ConnectionBasedAlarms = AlarmConfig.json()[i]
        del ConnectionBasedAlarms['id']
        ConnectionBasedAlarms['devices']['devices'] = '76445d7b-d61b-4ed5-ac1d-66e6e87c9ed3'
        print(ConnectionBasedAlarms)


    if AlarmConfig.json()[i].get('type')== 'PlcStatusBased':
        PlcStatusBasedAlarms = AlarmConfig.json()[i]

    if AlarmConfig.json()[i].get('type')== 'TimeIntervalBased':
        TimeIntervalBasedAlarms = AlarmConfig.json()[i]
        TimeIntervalBasedAlarms['devices']['devices'] = ['76445d7b-d61b-4ed5-ac1d-66e6e87c9ed3']

        print(TimeIntervalBasedAlarms)



    if AlarmConfig.json()[i].get('type') == 'TelemetryDataTimeout':
        TelemetryDataTimeoutBasedAlarms = AlarmConfig.json()[i]
        print(TelemetryDataTimeoutBasedAlarms)
        del TelemetryDataTimeoutBasedAlarms['id']
        TelemetryDataTimeoutBasedAlarms['devices']['devices'] = '76445d7b-d61b-4ed5-ac1d-66e6e87c9ed3'
        TelemetryDataTimeoutBasedAlarms['rule']['collectionKey'] = 1
        TelemetryDataTimeoutBasedAlarms['rule']['tagKey'] = 'Inlet_Pressure'
        print(TelemetryDataTimeoutBasedAlarms)

    if AlarmConfig.json()[i].get('type')== 'AlarmFlags':
        AlarmFlagBasedAlarms = AlarmConfig.json()[i]


#Copy over alarm data to other account
"""
AdamsDevices = requests.get(url= 'https://cloud.wago.com/api/deviceapp/devices?WorkspaceId='
                                +AdamsID +'&api-version=1.0',
                           headers= {'Authorization': 'Bearer ' + Auth_Token,'api-key': API_Key})

#print(AdamsDevices.json())
AdamsDeviceIDs= []
for i in range(0, len(AdamsDevices.json())):
    if i == 0:
        AdamsDeviceIDs = [AdamsDevices.json()[i].get('id')]
    if i > 0:
        AdamsDeviceIDs.append(AdamsDevices.json()[i].get('id'))

#print(AdamsDeviceIDs)

JoesDevices = requests.get(url= 'https://cloud.wago.com/api/deviceapp/devices?WorkspaceId='
                                +JoesID +'&api-version=1.0',
                           headers= {'Authorization': 'Bearer ' + Auth_Token,'api-key': API_Key})


JoesDeviceIDs = []
for i in range(0, len(JoesDevices.json())):
    if i == 0:
        JoesDeviceIDs = [JoesDevices.json()[i].get('id')]
    if i > 0:
        JoesDeviceIDs.append(JoesDevices.json()[i].get('id'))

print(JoesDeviceIDs)

#Change the rules JSON block
for i in range(0,len(ValueBasedAlarms)):

    del ValueBasedAlarms[i]['id']
    ValueBasedAlarms[i]['rules'][0]['tag']['deviceId'] = AlarmConfig.json()[i]['rules'][0]['tag']['deviceId']
    ValueBasedAlarms[i]['rules'][0]['tag']['collectionKey'] = AlarmConfig.json()[i]['rules'][0]['tag']['collectionKey']
    ValueBasedAlarms[i]['rules'][0]['tag']['tagKey'] = AlarmConfig.json()[i]['rules'][0]['tag']['tagKey']
    #print(ValueBasedAlarms[i])
    
    if ValueBasedAlarms:

        ValueBasedAlarmsPost = requests.post(url='https://cloud.wago.com/api/alarmapp/alarmconfigurations/valueBased?Workspace='
                                                 +JoesID+'&api-version=2.0',
                                     headers= {'Content-Type': 'application/json; charset=utf-8',
                                               'Accept': 'text/plain','Authorization': 'Bearer ' + Auth_Token,
                                               'api-key': API_Key},
                                     json= ValueBasedAlarms[i])
        print(ValueBasedAlarmsPost)






#if TimeIntervalBasedAlarms:

 #   TimeIntervalBasedAlarmsPost = requests.post(url='https://cloud.wago.com/api/alarmapp/alarmconfigurations/timeIntervalBased?Workspace='+JoesID+'&api-version=2.0',
  #                                   headers= {'Content-Type': 'application/json; charset=utf-8', 'Accept': 'text/plain','Authorization': 'Bearer ' + Auth_Token,'api-key': API_Key},
   #                                  json= TimeIntervalBasedAlarms)
    #print(TimeIntervalBasedAlarmsPost)
    #Seems to automatically adjust the alarm rule to all devices, even when not selected


#API path not available for Connection based alarms


#if ConnectionBasedAlarms:

 #   ConnectionBasedAlarmsPost = requests.post(url='https://cloud.wago.com/api/alarmapp/alarmconfigurations/timeoutBased?Workspace='+JoesID+'&api-version=2.0',
  #                                   headers= {'Content-Type': 'application/json; charset=utf-8', 'Accept': 'text/plain','Authorization': 'Bearer ' + Auth_Token,'api-key': API_Key},
   #                                  json= ConnectionBasedAlarms)
    #print(ConnectionBasedAlarmsPost)



#if TelemetryDataTimeoutBasedAlarms:

 #   TelemetryDataTimeoutBasedAlarmsPost= requests.post(url='https://cloud.wago.com/api/alarmapp/alarmconfigurations/timeoutBased?Workspace='+JoesID+'&api-version=2.0',
  #                                   headers= {'Content-Type': 'application/json; charset=utf-8', 'Accept': 'text/plain','Authorization': 'Bearer ' + Auth_Token,'api-key': API_Key},
   #                                  json= TelemetryDataTimeoutBasedAlarms)
    #print(TelemetryDataTimeoutBasedAlarmsPost)

#print(TelemetryDataTimeoutBasedAlarms)



