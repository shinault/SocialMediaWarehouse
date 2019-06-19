import dictionary.DictBuilder
import datastats.StatsBuilder

object App {
  def main(args: Array[String]) {
    val command = args(0)
    val dataSource = args(1)

    (command, dataSource) match {
      case ("dictionary", "reddit") => {
        println(s"Valid command, but feature not yet implemented.")
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
