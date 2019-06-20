import dictionary.DictBuilder
import connector.Connector

import org.apache.spark.sql.DataFrame

object App {

  def main(args: Array[String]) {
    val command = args(0)
    val dataSource = args(1)

    (command, dataSource) match {
      case ("dictionary", "reddit") => {
        val objectIterator = Connector.getAllObjects()
        while (objectIterator.hasNext) {
          val fileStatus = objectIterator.next
          val dataLoc = fileStatus.getPath
          val fileName = dataLoc.getName

          if (dataLoc.getParent.getName == "reddit") {
            println(s"Getting files from reddit")
            val fullDF: DataFrame = DictBuilder.connectToJson(dataLoc.toString)
            val dictDF: DataFrame = DictBuilder.createDictDF(fullDF)
            println(s"Writing to database")
            val tblName = fileName.replaceAll("-", "_")
            DictBuilder.addToDB(dictDF, "dictionaries", tblName)
          }
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
