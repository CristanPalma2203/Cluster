from pyspark.sql import SparkSession
spark=SparkSession.builder.getOrCreate()

df=spark.read.options(header='True',inferShema='True').csv('/resources/Data/*.csv')

products.mode.write('overwrite').csv("/resultado/result1")

producto = df.select(['product_id']).filter("event_type='cart'").first()

sessiones = df.select(['user_session']).filter("event_type='purchase' and product_id = "+producto).distinc()
