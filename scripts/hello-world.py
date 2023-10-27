from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

df = spark.read.options(header='True', inferSchema='True').csv('/resources/Data/*.csv')

df.write.format('com.databricks.spark.csv') \
  .mode('overwrite').option("header", "true").save("/resultado/result1")

producto = df.select('product_id').filter(df['event_type'] == 'cart').first()

product_id = producto['product_id']

sessiones = df.select('user_session').filter((df['event_type'] == 'purchase') & (df['product_id'] == product_id)).distinct()