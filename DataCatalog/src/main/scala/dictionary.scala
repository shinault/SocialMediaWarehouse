package dictionary

import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}
import org.apache.spark.sql.functions.typedLit
import com.databricks.spark.xml._
import java.sql.{Connection, DriverManager}
import java.util.Properties

object DictBuilder {
  val spark = SparkSession
    .builder()
    .appName("Data Dictionary Builder")
    .getOrCreate()

  import spark.implicits._

  def connectToJson(fileGlob: String) = spark.read.json(fileGlob)

  def connectToXml(fileGlob: String) = spark.read
    .option("rowTag", "row")
    .xml(fileGlob)

  def createDictDF(df: DataFrame): DataFrame = {
    val variables: Array[String] = df.columns
    val dataTypes: Array[String] = df.schema.fields.map(field => field.dataType.toString)
    spark.createDataset(variables zip dataTypes)
      .toDF("variable", "type")
      .withColumn("description", typedLit(""))
  }

  def addToDB(df: DataFrame, dbName: String, tblName: String) = {
    
    val jdbcHostname = System.getenv("DATADICT_DB_HOSTNAME")
    val jdbcPort = System.getenv("DATADICT_DB_PORT")
    val jdbcDatabase = dbName
    val jdbcUsername = System.getenv("DATADICT_DB_USERNAME")
    val jdbcPassword = System.getenv("DATADICT_DB_PASSWORD")
    val jdbcUrl = s"jdbc:postgresql://${jdbcHostname}:${jdbcPort}/${jdbcDatabase}"

    val connectionProperties = new Properties()
    connectionProperties.put("user", jdbcUsername)
    connectionProperties.put("password", jdbcPassword)

    val connection = DriverManager.getConnection(jdbcUrl, jdbcUsername, jdbcPassword)

    df.write
      .mode(SaveMode.Append)
      .jdbc(jdbcUrl, tblName, connectionProperties)
  }

  def sparkStop() = spark.stop()
}
