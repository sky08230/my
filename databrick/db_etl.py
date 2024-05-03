from pyspark.sql.functions import *
from pyspark.sql import Window

#function load data from raw layer to bronze layer
def raw_to_bronze(raw_path,bronze_path):
    #read data from json file 
    df=spark.read.option("multiline","true").json(raw_path).select(explode('movie'))
    #extract fields from movie column
    df_bronze=df.select('col',
                  "col.Id",
                    "col.Title",
                    "col.Overview",
                    "col.Tagline",
                    "col.Budget",
                    "col.Revenue",
                    "col.ImdbUrl",
                    "col.TmdbUrl",
                    "col.PosterUrl",
                    "col.Price",
                    "col.BackdropUrl",
                    "col.OriginalLanguage",
                    "col.ReleaseDate",
                    "col.RunTime",
                    "col.CreatedDate",
                    "col.UpdatedDate",
                    "col.UpdatedBy",
                    "col.CreatedBy",
                    "col.genres")
    #extracrt all genres mapping values
    df_genres=df_bronze.select('genres',explode('genres').alias('genres_value')).select('genres_value.id','genres_value.name').filter(length(col('name'))>0).distinct().orderBy('id')
    #convert the genres dataframe to dictionary
    df_g = df_genres.toPandas() 
    dict_genres={i:j for i,j in zip(df_g['id'],df_g['name'])}
    
    #function used to fill the null value for genres
    @udf(ArrayType(StringType())) 
    def fill_null_genres(a,b):
        return [dict_genres[i] for i in a]
      
    # use window function to mark the duplicate record 
    win = Window.partitionBy("Id").orderBy("Id")
    # perform transformation for genres,budget,and add mark column for quarantined value
    df_bronze_trans=df_bronze.selectExpr( "*",'genres.id as genres_id ','genres.name as genres_name',"EXISTS(genres,i-> len(i.name) <1)null_genres","runtime<0 as quarantine").withColumn('genres_name', when(col('null_genres')==True,fill_null_genres('genres_id','genres_name')).otherwise(col('genres_name'))).withColumn('Budget',when(col('Budget')<1000000,1000000).otherwise(col('Budget'))).withColumn('movie_num', row_number().over(win))

    df_bronze_trans.write.format("delta").mode("overwrite").save(bronze_path)


#function load data from bronze layer to silver layer
def bronze_to_silver(bronze_path,silver_path):
    #load data from bronze, and filter out the duplicate record
    df_bronze=spark.read.format("delta").load(bronze_path).filter(col('movie_num')==1)
    #seperate clean data 
    df_clean=df_bronze.where(col('quarantine')==False)
    #save clean data to silver
    df_clean.write.format("delta").mode("append").save(silver_path+"/moive")
    #transform quarantine data and save to sliver
    df_quarantine=df_bronze.where(col('quarantine')==True).withColumn("RunTime",abs("RunTime"))
    df_quarantine.write.format("delta").mode("append").save(silver_path+"/moive")
    
    #extract genres and OriginalLanguage table and save to silver
    w = Window.orderBy(col('OriginalLanguage').desc())
    df_OriginalLanguage=df_bronze.select('OriginalLanguage').distinct().withColumn('id', row_number().over(w))
    df_genres=df_bronze.select('genres',explode('genres').alias('genres_value')).select('genres_value.id','genres_value.name').filter(length(col('name'))>0).distinct().orderBy('id')
    df_OriginalLanguage.write.format("delta").mode("overwrite").save(silver_path+"/OriginalLanguage")
    df_genres.write.format("delta").mode("overwrite").save(silver_path+"/genres")

if __name__=="__main__":
    raw_path="dbfs:/mnt/raw"
    bronze_path="dbfs:/mnt/bronze"
    silver_path="dbfs:/mnt/silver"
    raw_to_bronze(raw_path,bronze_path)
    bronze_to_silver(bronze_path,silver_path)

    


             

