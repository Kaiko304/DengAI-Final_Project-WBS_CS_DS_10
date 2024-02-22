# this will open a local streamlit tab
# with a basic map and a choice of locations

# ---------------------------------------------------------------#
# to run streamlit app locally:
# 1. download this py-file and data/san_juan_predictions_map.csv
# 2. open CLI (command line interface)
# 3. on CLI, navigate to folder with py-file (using cd, dir, cd..)
# then prompt  >streamlit run name_of_py_file.py
# this opens automatically a browser tab with the streamlit app
# (stop process: ctrl+c)
# ---------------------------------------------------------------#


def load_data():
    import pandas as pd
    
    sj_pred = pd.read_csv("data/san_juan_predictions_map.csv") # load
    sj_pred['week_start_date'] = pd.to_datetime(sj_pred['week_start_date']) # format

    # create time_data (one common df)
    time_data = sj_pred[['week_start_date','Latitude','Longitude','total_cases']]

    # create time_index and data seperately
    time_index = sj_pred['week_start_date']
    data = sj_pred[['Latitude','Longitude','total_cases']]
    return data


def make_map(center):
    import folium
    from folium.plugins import HeatMapWithTime
    
    # basic map
    data = load_data() # call data
    map = folium.Map(center, zoom_start=11)

    # # add heatmap
    heatmap = folium.plugins.HeatMap(data)
    # HeatMapWithTime needs more work (looping?)
    # heatmap = folium.plugins.HeatMapWithTime(data, index=time_index, auto_play=True)
    heatmap.add_to(map)
    
    map.save('sj_pred_map.html')


def main():
    import streamlit as st

    st.title("Dengue Hazard App")
    st.caption('The three Mosquiteers - charming Terror of the Dengue Virus.')

    # sidebar
    st.sidebar.header("Choose a Weather Station")
    center = [18.4496, -66.0772]
    map_center = st.sidebar.radio("", ["San Juan", "Iquitos", "Iman", "somewhere", "..and other"])
    if map_center == "San Juan":
        center = [18.4496, -66.0772]
    elif map_center == "Iquitos":
        center = [-3.783, -73.3]
    elif map_center == "Iman":
        center = [52.5331, 13.3831]
    elif map_center == "somewhere":
        center = [50.283, 10.983]
    elif map_center == "..and other": 
        center = [49.9681, 8.2117]
    else:
        result = "Invalid operation"
    
    # display map
    make_map(center) # call map
    with open('sj_pred_map.html', 'r') as foli:
        map = foli.read()
    st.components.v1.html(map, height=600)

    # results
    if center:
        st.write(f"You've chosen {map_center} as your location.")

if __name__ == "__main__":
    main()