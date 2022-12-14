import argparse
import pyspark
from pyspark import SparkContext
from pyspark.sql.functions import desc
from pyspark.sql.types import *
from pyspark.sql import SparkSession


def get_args():
    parser = argparse.ArgumentParser(description='A spark job saving the partitioned cell-towers data in the hdfs and putting it into a MySQL database.')
    parser.add_argument('--hdfs_source_dir', help='HDFS source directory', required=True, type=str)
    parser.add_argument('--hdfs_target_dir', help='HDFS target directory', required=True, type=str)
    parser.add_argument('--hdfs_target_format', help='HDFS target format', required=True, type=str)
    parser.add_argument('--full_or_diff', help='Wether full or diff table is used', required=True, type=str)
    return parser.parse_args()

# --- Main program ---
if __name__ == '__main__':

    args = get_args()

    sc = pyspark.SparkContext()

    spark = SparkSession(sc)

    schema = StructType(
        [
            StructField("radio", StringType(), True),
            StructField("mcc", IntegerType(), True),
            StructField("net", IntegerType(), True),
            StructField("area", IntegerType(), True),
            StructField("cell", IntegerType(), True),
            StructField("unit", IntegerType(), True),
            StructField("lon", DoubleType(), True),
            StructField("lat", DoubleType(), True),
            StructField("range", IntegerType(), True),
            StructField("samples", IntegerType(), True),
            StructField("changeable", IntegerType(), True),
            StructField("created", IntegerType(), True),
            StructField("updated", IntegerType(), True),
            StructField("averageSignal", IntegerType(), True)
        ])

    if(args.full_or_diff == "full"):
        fileName = "/cell_towers_full.csv"
        writeMode = "overwrite"
    else:
        fileName = "/cell_towers_diff.csv"
        writeMode = "append"

    cell_tower_dataframe = spark.read.format('csv')\
        .options(header='true', delimiter=',', nullValue='null', inferschema='true')\
        .schema(schema)\
        .load(args.hdfs_source_dir + fileName)
        
    cell_tower_dataframe = cell_tower_dataframe\
        .dropna()\
        .dropDuplicates()\
        .select("radio", "lat", "lon", "range")\
        .repartition('radio')\
    
    cell_tower_dataframe\
        .write.format("parquet")\
        .mode(writeMode).option("path", args.hdfs_target_dir)\
        .partitionBy("radio")\
        .saveAsTable("default")\

    df_lte = spark.read.parquet(args.hdfs_target_dir + "/radio=LTE")
    df_cdma = spark.read.parquet(args.hdfs_target_dir + "/radio=CDMA")
    df_gsm = spark.read.parquet(args.hdfs_target_dir + "/radio=GSM")
    df_umts = spark.read.parquet(args.hdfs_target_dir + "/radio=UMTS")

    df_partioned_by_radio = [[df_lte, "LTE"], [df_cdma, "CDMA"], [df_gsm, "GSM"], [df_umts,"UMTS"]]

    for df_radio in df_partioned_by_radio:
        df_radio[0].write.format('jdbc').options(
            url='jdbc:mysql://ocid:3306/cell_towers',
            driver='com.mysql.cj.jdbc.Driver',
            dbtable='towers_' + df_radio[1],
            user='root',
            password='ocidBigData').partitionBy("radio").mode(writeMode).save()