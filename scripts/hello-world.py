print("Hola Lil Josue;")

spark=SparkSession.builder.getOrCreate()
df=spark.read.options(header='True',inferShema='True').csv(/resources/Data/*.csv)
df.count()