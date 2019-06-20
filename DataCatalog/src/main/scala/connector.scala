package connector

import com.databricks.spark.xml._
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.hadoop.conf.Configuration
import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}
import java.net.URI
import java.sql.{Connection, DriverManager}
import java.util.Properties

object Connector {
  val spark = SparkSession
    .builder()
    .appName("Data Dictionary Builder")
    .getOrCreate()

  import spark.implicits._

  def connectToJson(fileGlob: String) = spark.read.json(fileGlob)

  def connectToXml(fileGlob: String) = spark.read
    .option("rowTag", "row")
    .xml(fileGlob)

  def addToDB(df: DataFrame, dbName: String, tblName: String) = {
    
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

    df.write
      .mode(SaveMode.Overwrite)
      .jdbc(jdbcUrl, tblName, connectionProperties)
  }

  // Inspired by this answer:
  // https://stackoverflow.com/questions/54060265/how-to-list-files-in-s3-bucket-using-spark-session
  def getAllObjects() = {
    spark.sparkContext.hadoopConfiguration.set("fs.s3n.awsAccessKeyId",
      System.getenv("AWS_ACCESS_KEY_ID"))
    spark.sparkContext.hadoopConfiguration.set("fs.s3n.awsSecretAccessKey",
      System.getenv("AWS_SECRET_ACCESS_KEY"))
    val rootPath = "s3a://saywhat-warehouse/raw"
    val fs = FileSystem.get(URI.create(rootPath), new Configuration(true))
    fs.listFiles(new Path(rootPath), true)
  }

  def sparkStop() = spark.stop()
}
