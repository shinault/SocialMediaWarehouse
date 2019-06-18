import transformer.{Transformer => T}

object App {
  def main(args: Array[String]) {
    val command = args(0)
    val fileGlob = args(1)
    command match {
      case "stackexchange" => {
        println(s"Connecting to files from the glob ${fileGlob}...")
        val df = T.connectToXmlData(fileGlob, "comments", "stackexchange")
        println(s"Reading and writing files to database...")
        T.addToDB(df)
        T.sparkStop()
      }

      case "reddit" => {
        println(s"Connecting to files from the glob ${fileGlob}...")
        val df = T.connectToJsonData(fileGlob, "comments", "reddit")
        println(s"Reading and writing files to database...")
        T.addToDB(df)
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
