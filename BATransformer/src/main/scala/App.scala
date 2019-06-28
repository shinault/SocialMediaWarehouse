import transformer.{Transformer => T}
import helpers.{RedditHelper => RH, StackExchangeHelper => SEH}

object App {
  def main(args: Array[String]) {
    val command = args(0)
    command match {
      case "stackexchange" => {
        val seDoms = SEH.getAllDomains()
        for (dom <- seDoms) {
          val fileName = dom ++ "/Comments.xml"
          println(s"Connecting to files from the glob ${fileName}...")
          val fileLoc = "s3a://saywhat-warehouse/raw/stack_exchange/" ++ fileName
          val df = T.connectToXmlData(fileLoc)
          val cleanedDF = T.cleanStackExchangeDF(df)
          println(s"Reading and writing files to database...")
          T.addToDB(df, "comments", "stackexchange")
        }
        T.sparkStop()
      }

      case "reddit" => {
        val redditFiles = RH.fileGenerator(2016, 1, 2016, 12)
        for (fileName <- redditFiles) {
          println(s"Connecting to files from the glob ${fileName}...")
          val fileLoc = "s3a://saywhat-warehouse/raw/reddit/" ++ fileName
          val df = T.connectToJsonData(fileLoc)
          val cleanedDF = T.cleanRedditDF(df)
          println(s"Reading and writing files to database...")
          T.addToDB(cleanedDF, "comments", "reddit")
        }
        T.sparkStop()
      }

      case "hackernews" => {
        println("This is a valid command, but not yet implemented")
      }

      case _ => {
        println("Not a valid command.")
        println("Please choose 'stackexchange', 'reddit', or 'hackernews'.")
      }
    }
  }
}
