package reddittransformer

import org.apache.spark.sql.{SaveMode, SparkSession}
import java.sql.{Connection, DriverManager}
import java.util.Properties

object RedditTransformer {
  val spark = SparkSession
    .builder()
    .appName("BA Transformer")
    .getOrCreate()

  import spark.implicits._

  def connectToData(fileGlob: String) = spark.read
    .json(fileGlob)
    .select("created_utc", "body")

  def sparkStop() = spark.stop()
}
