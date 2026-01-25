import pyodbc

server = 'DESKTOP-7L879NC\SQLEXPRESS'
usuario = 'Jefrino'
clave = '12345678'
conexion = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';UID='+usuario+';PWD='+clave+';autocommit=True')

print ("Conexion Exitosa ")

cursor= conexion.cursor()

conexion.close()