import mysql.connector
class DAO:
	def connection(self):
		self.cnx = mysql.connector.connect(user='root', password='gis123',host='220.130.149.149',database='gis_db')
		return self.cnx

	def close(self):
		self.cnx.close()
