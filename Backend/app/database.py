import sqlite3


### Make the connection
connection = sqlite3.connect("sqlite.db")

### Close the connection when done
connection.close()
