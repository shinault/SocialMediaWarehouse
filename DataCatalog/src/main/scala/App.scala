import dictionary.DictBuilder
import org.apache.spark.sql.DataFrame

object App {
  def main(args: Array[String]) {
    val command = args(0)
    val dataSource = args(1)
    val fileName = args(2)

    (command, dataSource) match {
      case ("dictionary", "reddit") => {
        val dataLoc = s"s3a://saywhat-warehouse/raw/reddit/${fileName}"
        println(s"Getting files from $dataSource")
        val fullDF: DataFrame = DictBuilder.connectToJson(dataLoc)
        val dictDF: DataFrame = DictBuilder.createDictDF(fullDF)
        println(s"Writing to database")
        DictBuilder.addToDB(dictDF, "dictionaries", fileName)
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
