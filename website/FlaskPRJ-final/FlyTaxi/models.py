from FlyTaxi import cntStr
from datetime import datetime


def geoInfo():
    listSpot = list()
    with cntStr.connection.cursor() as cursor:
        timeNow = f'{datetime.now().time().hour}:00:00' if datetime.now().time().hour > 9 else f'0{datetime.now().time().hour}:00:00'
        timeWeekday = datetime.now().weekday() + 1
        sql = "SELECT DISTINCT clustersPos.Cluster_id, clusterspos.Latitude, clusterspos.Longitude, clusterspos.Radius,\
            clustersInfo.Pickup_count, clustersInfo.Trip_Total_level, clustersInfo.Profits_level, clustersInfo.Tips_yn,\
            clustersInfo.long_yn, clustersInfo.Trip_Miles, clustersInfo.outside_yn\
            FROM clustersPos LEFT JOIN clustersinfo \
            ON clustersPos.Cluster_id = clustersInfo.Cluster_id \
            WHERE clustersInfo.Time=%s AND clustersInfo.week=%s"
        cursor.execute(sql, (timeNow, timeWeekday))
        tmp = cursor.fetchall()
        for i in tmp:
            listSpot.append(i)
    return listSpot

def clusterInfo():
    listInfo = list()
    with cntStr.connection.cursor() as cursor:
        timeWeekday = datetime.now().weekday() + 1
        sql = "SELECT `Cluster_id`, `Time`, `Week`, `Pickup_count`, `Trip_Total`, `Trip_Miles`, `Trip_Seconds` FROM `clustersinfo` WHERE `Week`=%s"
        cursor.execute(sql, timeWeekday)
        tmp = cursor.fetchall()
        for i in tmp:
            listInfo.append(i)
    return listInfo
