from pyspark.sql import functions as F
from pyspark.sql.functions import desc
from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession.builder.appName("CargarDatos").getOrCreate()

df = spark.read.csv('/content/2020-Feb.csv', header=True)

#Metodo para Buscar sesiones
def buscar_sesiones(df,producto):
  if producto.product_id is not  None:
      sesiones = df.select(['user_session']).filter("event_type='purchase' and product_id=" + producto.product_id).distinct()
      return sesiones, True
  else:
      return None, False

# Buscar los productos que se han comprado en esas sesiones de usuario
def buscar_producto_top5(df,producto):
  sesiones, validador =  buscar_sesiones(df,producto)
  if validador:
    productos_comprados = df.select(['product_id']).filter(df.user_session.isin(sesiones["user_session"]))
    conteo_productos = productos_comprados.groupby('product_id').count()
    conteo_productos_ordenado = conteo_productos.orderBy(desc("count"))
    return conteo_productos_ordenado.select(['product_id']).limit(5)
  else :
    print("No se encontarto sesiones")

producto = df.select(['product_id']).filter("event_type='cart'").first()
print(producto.product_id)
dfr = buscar_producto_top5(df,producto)

dfr.repartition(1).write.csv("/content/output_productos.csv", header=True, mode="overwrite")

print("app top 5 products")
print(dfr)