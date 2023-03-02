import pandas as pd
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime

auth_url = "https://www.strava.com/oauth/token"

payload = {
    'client_id': "XXXXXX",
    'client_secret': 'XXXXXX',
    'refresh_token': 'XXXXXX', 
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

# reading CSV file with activities
activities = pd.read_csv(r"C:\your_path_to_csv_file\activities.csv") #Provide path to csv file
activities = activities[activities['distance'] != 0] # Keep only activities with distance not equal to 0

#Converting column data to list
activities_ids = activities['id'].tolist()

#Variables to include in the request
variables = ['distance','time','altitude','heartrate','cadence','grade_smooth','velocity_smooth']

#Create an empty array with the response of the API request
All_variables = []

header = {'Authorization': 'Bearer ' + access_token}

for act_id in activities_ids[]: #You might want to slice the activities here to avoid exceeding Strava API request limits
    print(act_id)
    #Create an empty dictionary to hold the values for this activity
    activity_data = {}

    #Iterate through the variables, request the values and assign to the activity_data dictionary
    for variable in variables:
        param1 = {'keys': variable, 'key_by_type': True}
        my_streams_url = "https://www.strava.com/api/v3/activities/"+str(act_id)+"/streams"
        my_streams = requests.get(my_streams_url, headers=header, params=param1).json()
                
        # Check if the key exists in my_streams dictionary, if so add the data to dictionary
        if variable in my_streams.keys():
            activity_data[variable] = my_streams[variable]['data']
                        
        else:
            print(f"Variable '{variable}' not found for activity {act_id}.")
            continue
    
    # Add the activity id to the activity
    activity_data['activity_id'] = act_id
    
    #Add the activity_data dictionary to the All_variables list
    All_variables.append(activity_data)

data = []

# Create dataframe with streams data and export to csv file
for d in All_variables:
    n = len(d['distance']) 
    for i in range(n):
        row = {
            'activity_id': d['activity_id'],
            'distance': d['distance'][i] if 'distance' in d else None,
            'time': d['time'][i] if 'time' in d else None,
            'altitude': d['altitude'][i] if 'altitude' in d else None,
            'heartrate': d['heartrate'][i] if 'heartrate' in d else None,
            'cadence': d['cadence'][i] if 'cadence' in d else None,
            'grade_smooth': d['grade_smooth'][i] if 'grade_smooth' in d else None,
            'velocity_smooth': d['velocity_smooth'][i] if 'velocity_smooth' in d else None
        }
        
        data.append(row)

df = pd.DataFrame(data)

Fecha = datetime.now()

streams = r"C:\path_to_csv_file\Stream" + str(Fecha.strftime("%Y%m%d-%H_%M_%S")+".csv") #Provide path to csv file with stream data. You will need to combine all the csv files or
                                                                                        #change code and append to single file.
print(streams)
df.to_csv(streams,index=False)