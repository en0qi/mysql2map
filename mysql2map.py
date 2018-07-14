import folium #map 

from urllib.parse import urlparse #urlparse
import mysql.connector #mysql

url=urlparse('mysql://[username]:[password]@[hostname]:[port]/[table name]')

conn = mysql.connector.connect(
	host = url.hostname or 'localhost',
	port = url.port or 3306,
	user = url.username or 'root',
	password = url.password or 'password',
	database = url.path[1:],
	)

#print(conn.is_connected())

try:
	cur = conn.cursor()
	cur.execute('SELECT x.latitude, x.longitude, x.markerID FROM AccessLog as x')
	data = cur.fetchall()
	#Count the numbers of row
	query = "SELECT COUNT(*) from AccessLog"
	cur.execute(query)             #execute query separately
	res = cur.fetchone()
	total_rows = res[0] 
	#draw map
	m = folium.Map(location=[36.0821307,140.1114102], zoom_start=14) #つくば駅の緯度経度
	for i in range(total_rows):
		folium.Marker(
		    location=[data[i][0], data[i][1]],
		    popup=data[i][2],
		    icon=folium.Icon(icon='cloud')
		).add_to(m)
	m.save('map.html')

except Exception as e:
	raise e