import pymysql.cursors
import csv


# conntection infomation
connection = pymysql.connect(host='localhost',
                             user='ourAcc',
                             password='ourPW',
                             database='ourDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# using with => closing file/session while runing out of the block
def clustersData2DB():
    dt01 = list()
    dt02 = list()

    with open('clustersPos.csv', newline='') as csvfile:
        tmp = csv.reader(csvfile)
        for i in tmp:
            dt01.append(i)

    with open('clustersInfo.csv', newline='') as csvfile:
        tmp = csv.reader(csvfile)
        for i in tmp:
            dt02.append(i)

    with connection:
        with connection.cursor() as cursor:
            # Create talbe
            sqlTable01 = """CREATE TABLE IF NOT EXISTS `clusterspos` (
            `Cluster_id` INT NOT NULL,
            `Latitude` DOUBLE NOT NULL,
            `Longitude` DOUBLE NOT NULL,
            `Radius` FLOAT NOT NULL 
            ) CHARSET=utf8;"""
            cursor.execute(sqlTable01)

            # Create a new record
            sqlInsert01 = "INSERT INTO `clusterspos` (`Cluster_id`, `Latitude`, `Longitude`, `Radius`) VALUES (%s, %s, %s, %s)"

            for i in dt01:
                insert_tuple01 = (i[0], i[1], i[2], i[3])
                cursor.execute(sqlInsert01, insert_tuple01)


            # Create talbe
            sqlTable02 = """CREATE TABLE IF NOT EXISTS `clustersinfo` (
            `Cluster_id` INT NOT NULL,
            `Week` INT,
            `Time` VARCHAR(30),
            `Pickup_count` FLOAT,
            `Trip_Total` FLOAT,
            `Trip_Miles` FLOAT,
            `Trip_Seconds` FLOAT,
            `Tips_yn` FLOAT,
            `long_yn` FLOAT,
            `traffic_yn` FLOAT,
            `outside_yn` FLOAT,
            `Trip_Total_level` VARCHAR(30),
            `Profits_level` VARCHAR(30)
            ) CHARSET=utf8;"""
            cursor.execute(sqlTable02)

            # Create a new record
            sqlInsert02 = "INSERT INTO `clustersinfo` VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            for i in dt02:
                insert_list02 = list()
                num = len(i)
                for j in range(num):
                    insert_list02.append(i[j])
                cursor.execute(sqlInsert02, tuple(insert_list02))

        connection.commit()
    

if __name__ == "__main__":
    clustersData2DB()
