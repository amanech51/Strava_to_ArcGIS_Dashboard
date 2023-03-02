import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import polyline
import pandas as pd

# Request Strava token
auth_url = "https://www.strava.com/oauth/token"
payload = {
    'client_id': "XXXXXX", 
    'client_secret': 'XXXXXX',
    'refresh_token': 'XXXXXX',
    'grant_type': "refresh_token",
    'f': 'json'
}
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

# Get athlete stats
athlete_id = 'XXXXXX'#Strava athlete id
my_stats_url = f"https://www.strava.com/api/v3/athletes/{athlete_id}/stats"
header = {'Authorization': 'Bearer ' + access_token}
my_stats = requests.get(my_stats_url, headers=header).json()

# Get all activities
activities_url = "https://www.strava.com/api/v3/athlete/activities"
total_act = my_stats['all_ride_totals']['count']
NumberPages = -(-total_act // 200)
list_activities = []
for i in range(1, NumberPages+1):
    param = {'per_page': 200, 'page': i}
    my_dataset = requests.get(activities_url, headers=header, params=param).json()
    list_activities += my_dataset

# Convert activities to dataframe
activities = pd.json_normalize(list_activities)

# Add decoded summary polylines (Converting Google coded polylines to coordinates)
activities['map.polyline'] = activities['map.summary_polyline'].apply(polyline.decode)

# Convert some values in the dataframe 
activities[['distance']] /= 1000 # Convert distance to Km.
activities[['average_speed', 'max_speed']] *= 3.6 #Convert speed from m/s to Km/h.
activities[['moving_time', 'elapsed_time']] /= 3600 #Convert time from s to hr.

# Extract coordinates vertices to csv file, to create polylines with arcpy (You might want to consider other options: arcpy.da.InsertCursor, Spatially Enable DataFrame and simplify the code)
coord = activities[['id','map.polyline','gear_id']].explode('map.polyline') # More columns can be added as wanted to obtain feature class with more attributes
coord[['Lat', 'Long']] = pd.DataFrame(coord['map.polyline'].tolist(), index=coord.index)
Vertices = coord.reset_index(drop=True).reset_index().rename(columns={'index': 'PT_ORDER', 'map.polyline': 'PAIR'})[['PT_ORDER','id', 'PAIR', 'Lat', 'Long','gear_id']]
csv_path = r'C:\your_path\vertices_pts.csv' # Replace with path to folder where you want to save it.
Vertices.to_csv(csv_path, index=False)

# Export activities to csv file
activities.drop(columns=['resource_state', 'location_city', 'location_state', 'location_country', 'manual', 'private', 'visibility', 'flagged', 'utc_offset', 'start_latlng', 'end_latlng', 'device_watts', 'has_heartrate', 'heartrate_opt_out', 'display_hide_heartrate_option', 'upload_id', 'upload_id_str', 'external_id', 'from_accepted_tag', 'photo_count', 'total_photo_count', 'has_kudoed', 'athlete.id', 'athlete.resource_state', 'map.id', 'map.summary_polyline', 'map.resource_state', 'map.polyline'], inplace=True)
activities['start_date'] = pd.to_datetime(activities['start_date']).dt.tz_localize(None)
activities['start_date_local'] = pd.to_datetime(activities['start_date_local']).dt.tz_localize(None)

### Assign a name to gear: modify as you need (You can use Strava API to get the gear_id https://www.strava.com/api/v3/gear/id)
def Bike (row):
   if row['gear_id'] == 'XXXXXX' :
      return 'Name 1'
   elif row['gear_id'] == 'XXXXXX' :
      return 'Name 2'
   elif row['gear_id'] == 'XXXXXXX' :
      return 'Name 3'
   elif row['gear_id'] == 'XXXXXXXXX' :
      return 'Name 4'
   else:
      return 'No gear specified'
activities['bike'] = activities.apply(Bike, axis=1)

activities.to_csv(r'C:\path_to_\activities.csv',index=False) #Replace with path to folder where you want to save csv file

#Create point feature class and then convert to lines
arcpy.env.overwriteOutput = True
point_fc = r'C:\path_to_FGDB\vertices' #Replace with path to Geodatabase where you want to store the points Feature Class
crs = arcpy.SpatialReference(4326)
arcpy.management.XYTableToPoint(in_table=csv_path, out_feature_class=point_fc, x_field="Long", y_field="Lat", coordinate_system=crs)

#Create routes with points (works with ArcGIS PRO 3.1, for previous versions remove transfer fields, as that functionality is not supported)
Input_Features = point_fc
Output_Feature_Class = r'C:\path_to_FGDB\routes' #Replace with path to Geodatabase where you want to store the line Feature Class
Line_Field = "id"
Sort_Field = "PT_ORDER"
transFields = "gear_id" #Consider adding more fields here as columns added in coord fataframe
arcpy.management.PointsToLine(Input_Features, Output_Feature_Class, Line_Field, Sort_Field, "NO_CLOSE", "CONTINUOUS", "START", transFields)