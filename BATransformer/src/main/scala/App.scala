import reddittransformer.{RedditTransformer => RT}

object App {
  def main(args: Array[String]) {
    val command = args(0)
    val fileGlob = args(1)
    command match {
      case "stackexchange" => {
        println("This is a valid command, but not yet implemented")
      }
        
      case "reddit" => {
        val df = RT.connectToData(fileGlob)
        println(df.count())
        RT.sparkStop()
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
