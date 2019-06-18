package transformer

import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}
import java.sql.{Connection, DriverManager}
import java.util.Properties

object Transformer {
  val spark = SparkSession
    .builder()
    .appName("BA Transformer")
    .getOrCreate()

  import spark.implicits._

  def connectToJsonData(fileGlob: String) = spark.read
    .json(fileGlob)
    .select("created_utc", "body")

  def addToDB(commentsDF: DataFrame, dbName: String, tblName: String) = {
    
    val jdbcHostname = System.getenv("COMMENTS_DB_HOSTNAME")
    val jdbcPort = System.getenv("COMMENTS_DB_PORT")
    val jdbcDatabase = dbName
    val jdbcUsername = System.getenv("COMMENTS_DB_USERNAME")
    val jdbcPassword = System.getenv("COMMENTS_DB_PASSWORD")
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
