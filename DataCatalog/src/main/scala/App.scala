import dictionary.DictBuilder
import helpers.{RedditHelper => RH}

import org.apache.spark.sql.DataFrame

object App {

  def main(args: Array[String]) {
    val command = args(0)
    val dataSource = args(1)

    (command, dataSource) match {
      case ("dictionary", "reddit") => {
        val redditFiles = RH.fileGenerator(2005, 12, 2017, 9)
        for (fileName <- redditFiles) {
          val fileLoc = "s3a://saywhat-warehouse/raw/reddit/" ++ fileName
          println(s"Getting files from $fileLoc")
          val fullDF: DataFrame = DictBuilder.connectToJson(fileLoc)
          val dictDF: DataFrame = DictBuilder.createDictDF(fullDF)
          println(s"Writing to database")
          val tblName = fileName.replaceAll("-", "_")
          DictBuilder.addToDB(dictDF, "dictionaries", tblName)
        }
      }

      case ("dictionary", "stackexchange") => {
        println(s"Valid command, but feature not yet implemented.")
      }

      case ("dictionary", "hackernews") => {
        println(s"Valid command, but feature not yet implemented.")
      }

      case ("stats", "reddit") => {
        println(s"Valid command, but feature not yet implemented.")
      }

      case ("stats", "stackexchange") => {
        println(s"Valid command, but feature not yet implemented.")
      }

      case ("stats", "hackernews") => {
        println(s"Valid command, but feature not yet implemented.")
      }

      case _ => {
        println("Not a valid command, or data source not valid.")
        println("Please enter 'dictionary' or 'stats' for the command,")
        println("followed by 'reddit', 'stackexchange', or 'hackernews'.")
      }
    }
  }
}
