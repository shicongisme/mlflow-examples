import click
import mlflow
import mlflow.spark
from pyspark.sql import SparkSession
from common import *

spark = SparkSession.builder.appName("Predict").getOrCreate()
show_versions(spark)

@click.command()
@click.option("--model_uri", help="Model URI", required=True, type=str)
@click.option("--data_path", help="Data path", default=default_data_path, type=str)

def main(model_uri, data_path):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")

    data_path = data_path or default_data_path
    data = read_data(spark, data_path)
    print("Data Schema:")
    data.printSchema()

    print("model_uri:", model_uri)
    model = mlflow.spark.load_model(model_uri)
    print("model.type:", type(model))
    predictions = model.transform(data)
    print("predictions.type:", type(predictions))
    df = predictions.select(colPrediction, colLabel, colFeatures)
    df.show(5, False)

if __name__ == "__main__":
    main()
