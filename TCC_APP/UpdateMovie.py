import os
from sqlalchemy import create_engine
import base64
from PIL import Image
from io import BytesIO

my_conn = create_engine("mysql+pymysql://tccapp:yE2KGUn7!Nqchvd@watchlist.mysql.database.azure.com/app_db")

id = 51662

pathimg = 'C:/Posters/51662.png'
pathtxt = 'C:/Posters/51662.txt'


with open(pathimg,'rb') as image_file:
    base64_bytes = base64.b64encode(image_file.read())
    base64_string = base64_bytes.decode()
fob = base64_string

query="UPDATE movies SET poster=%s WHERE movieId=%s"
data=(fob,id)

my_cursor=my_conn.execute(query,data)
print("Rows updated = ",my_cursor.rowcount)


file = open(pathtxt, 'r')
fob1 = file.read()

query="UPDATE movies SET description=%s WHERE movieId=%s"
data=(fob1,id)

my_cursor=my_conn.execute(query,data)
print("Rows updated = ",my_cursor.rowcount)
