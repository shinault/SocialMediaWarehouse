package transformer

import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}
import org.apache.spark.sql.functions.{
  col,
  from_unixtime,
  lit,
  length,
  monotonically_increasing_id}
import org.apache.spark.sql.types._
import com.databricks.spark.xml._
import java.sql.{Connection, DriverManager}
import java.util.Properties

object Transformer {
  val spark = SparkSession
    .builder()
    .appName("BA Transformer")
    .getOrCreate()

  import spark.implicits._

  def connectToJsonData(fileGlob: String): DataFrame = spark.read.json(fileGlob)

  def cleanRedditDF(df: DataFrame): DataFrame = df.filter(length(col("body")) > 80)
    .select(
      ($"created_utc").cast("long").cast("timestamp").alias("datetime"),
      $"body".alias("text"))
    .withColumn("source", lit("reddit"))
    .withColumn("id", monotonically_increasing_id())

  def connectToXmlData(fileGlob: String): DataFrame = {
    val customSchema = StructType(Array(
      StructField("_CreationDate", StringType),
      StructField("_Id", LongType),
      StructField("_PostId", LongType),
      StructField("_Score", LongType),
      StructField("_Text", StringType),
      StructField("_UserId", LongType),
      StructField("_UserDisplayName", StringType)
    ))
    spark.read
      .option("rowTag", "row")
      .schema(customSchema)
      .xml(fileGlob)
  }

  def cleanStackExchangeDF(df: DataFrame): DataFrame = df
    .filter(length(col("_Text")) > 80)
    .select(
      $"_CreationDate".cast("timestamp").alias("datetime"),
      $"_Text".alias("text"))
    .withColumn("source", lit("stackexchange"))
    .withColumn("id", monotonically_increasing_id())

  def cleanHNDF(df: DataFrame): DataFrame = df
    .filter(length(col("body.text")) > 80)
    .select(
      $"body.time".cast("timestamp").alias("datetime"),
      $"body.text".alias("text")
    )
    .withColumn("source", lit("hackernews"))
    .withColumn("id", monotonically_increasing_id())

  def addToDB(commentsDF: DataFrame, dbName: String, tblName: String) = {
    
    val jdbcHostname = System.getenv("DB_HOSTNAME")
    val jdbcPort = System.getenv("DB_PORT")
    val jdbcDatabase = dbName
    val jdbcUsername = System.getenv("DB_USERNAME")
    val jdbcPassword = System.getenv("DB_PASSWORD")
    val jdbcUrl = s"jdbc:postgresql://${jdbcHostname}:${jdbcPort}/${jdbcDatabase}"

    val connectionProperties = new Properties()
    connectionProperties.put("user", jdbcUsername)
    connectionProperties.put("password", jdbcPassword)

    val connection = DriverManager.getConnection(jdbcUrl, jdbcUsername, jdbcPassword)

    commentsDF.write
      .mode(SaveMode.Append)
      .jdbc(jdbcUrl, tblName, connectionProperties)
  }

  def sparkStop() = spark.stop()
}
