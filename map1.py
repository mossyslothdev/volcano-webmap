import folium
import pandas

volcano_data = pandas.read_csv("Files\\Volcanoes.txt")
# load latitude of volcanoes into a list
volcano_latitude = list(volcano_data["LAT"])
# load longitude of volcanoes into a list
volcano_longitude = list(volcano_data["LON"])
# load elevation of volcanoes into a list
volcano_elevation = list(volcano_data["ELEV"])


def color_picker(elevation):
    if elevation < 1000:
        return "green"
    elif elevation <= 1000 or elevation < 3000:
        return "orange"
    else:
        return "red"


map = folium.Map(
    location=[32.7778755224263, -96.79610465549673],
    zoom_start=6,
    tiles="Stamen Terrain",
)

feature_group_volcanoes = folium.FeatureGroup(name="Volcanoes")

for latitude, longitude, elevation in zip(volcano_latitude, volcano_longitude, volcano_elevation):
    feature_group_volcanoes.add_child(
        folium.CircleMarker(
            location=[latitude, longitude],
            popup=str(elevation) + " m",
            radius=7,
            fill=True,
            fill_opacity=0.7,
            fill_color=color_picker(elevation),
            color="grey",  # this last parameter controls the outline color
        )
    )

feature_group_population = folium.FeatureGroup(name="Population")

feature_group_population.add_child(
    folium.GeoJson(
        data=open("Files\\world.json", "r", encoding="utf-8-sig").read(),
        style_function=lambda x: {
            "fillColor": "green"
            if x["properties"]["POP2005"] < 10000000
            else "orange"
            if 10000000 <= x["properties"]["POP2005"] < 20000000
            else "red"
        },
    )
)

map.add_child(feature_group_volcanoes)
map.add_child(feature_group_population)
map.add_child(folium.LayerControl())

map.save("Map1.html")
