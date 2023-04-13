from flask import Flask
import folium
import pandas as pd
import math

# Define the bucket size: 1 would be every longitude/latitude (ca. 110km); 10 is 1/10th (ca. 11km); 20 is 1/20th (5.5km)
bucket_length = 20

# Maximal distance of accidents from route in kilometers
max_distance = 0.05


# Read the dataframe with the accident locations -> has only columns ID, Start_Lat, and Start_Lng
raw_data = pd.read_csv('accident_locations.csv')

# Functions to generate latitude and longitude IDs for the bucketing
def get_lat_id(lat):
    return int(lat*bucket_length)
def get_lng_id(lng):
    return int(lng*bucket_length)

# Assign bucketing IDs to each accident
raw_data["lat_id"] = raw_data["Start_Lat"].apply(get_lat_id)
raw_data["lng_id"] = raw_data["Start_Lng"].apply(get_lng_id)

# Group by bucketing IDs
groups = raw_data.groupby(['lat_id', 'lng_id'])

# Iterate over the groups and create individual dataframes
for name, group in groups:
    # Create the dataframe name
    df_name = f"accidents_{name[0]}_{name[1]}"
    
    # Create the dataframe
    vars()[df_name] = group.copy()

# Get a copy of all global variables
global_vars = globals().copy()


# Define a function to calculate the distance between two points
def distance(point1, point2):
    lat1, lon1 = point1
    lat2, lon2 = point2
    km_per_lat = 110.574 # km per degree latitude
    km_per_lon = 111.320 # km per degree longitude at the equator
    dx = (lon2 - lon1) * km_per_lon * math.cos((lat1 + lat2) / 2)
    dy = (lat2 - lat1) * km_per_lat
    return math.sqrt(dx**2 + dy**2)

# Define a function to calculate the distance between a point and a line segment
def distance_to_segment(point, segment_start, segment_end):
    px, py = point
    x1, y1 = segment_start
    x2, y2 = segment_end
    dx, dy = x2 - x1, y2 - y1
    segment_length_squared = dx*dx + dy*dy
    if segment_length_squared == 0:
        return distance(point, segment_start)
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / segment_length_squared))
    x = x1 + t * dx
    y = y1 + t * dy
    return distance(point, (x, y))

# Define a function to find accidents on a given route within a maximum distance
def find_accidents_on_route(start_point, end_point, max_distance):
    # Create a mask for accidents that are within the maximum distance from the route
    mask = data.apply(lambda row: distance_to_segment((row['Start_Lat'], row['Start_Lng']), start_point, end_point) <= max_distance, axis=1)

    # Return the accidents that match the mask
    return data.loc[mask]



# Route start and end point
start_point = (33.77299, -84.39020)
end_point = (33.790347, -84.391530)



# Extract the integer values of the start point lat and lng
start_lat = int(start_point[0]*bucket_length)
start_lng = int(start_point[1]*bucket_length)

# Get the dataframes that match the criteria
dfs_to_use = []
for lat_offset in [-1, 0, 1]:
    for lng_offset in [-1, 0, 1]:
        lat_id = start_lat + lat_offset
        lng_id = start_lng + lng_offset
        df_name = f"accidents_{lat_id}_{lng_id}"
        if df_name in global_vars and isinstance(global_vars[df_name], pd.DataFrame):
            dfs_to_use.append(global_vars[df_name])

# Concatenate the dataframes and reset the index
combined_df = pd.concat(dfs_to_use)
data = combined_df.reset_index(drop=True)

# Run after entering the accident, route, and distance data
accidents = find_accidents_on_route(start_point, end_point, max_distance)



app = Flask(__name__)

# Load your accidents data into a pandas dataframe here

# Set your start and end points here

@app.route('/map')
def map_view():
    # create a map object centered at the mean latitude and longitude of the accidents
    map_accidents = folium.Map(location=[accidents.Start_Lat.mean(), accidents.Start_Lng.mean()], zoom_start=15)

    # add markers for each accident to the map
    for index, row in accidents.iterrows():
        # create a tooltip with the lat/long coordinates
        tooltip = "ID: {}<br>Latitude: {}<br>Longitude: {}".format(row['ID'], round(row['Start_Lat'],5), round(row['Start_Lng'],5))
        folium.Marker(location=[row['Start_Lat'], row['Start_Lng']],
                      tooltip=tooltip
                     ).add_to(map_accidents)

    # add start point marker to the map
    start_tooltip = "Start Point"
    folium.Marker(location=[start_point[0], start_point[1]],
                  icon=folium.Icon(color='green', icon='glyphicon-home'),
                  tooltip=start_tooltip
                 ).add_to(map_accidents)
    
    # add end point marker to the map
    end_tooltip = "End Point"
    folium.Marker(location=[end_point[0], end_point[1]],
                  icon=folium.Icon(color='red', icon='glyphicon-flag'),
                  tooltip=end_tooltip
                 ).add_to(map_accidents)

    # Return the map HTML
    return map_accidents._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)