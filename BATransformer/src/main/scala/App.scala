object App {
  def main(args: Array[String]) {
    args(0) match {
      case "stackexchange" => {
        println("This is a valid command, but not yet implemented")
      }
      case "reddit" => {
        println("This is a valid command, but not yet implemented")
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
