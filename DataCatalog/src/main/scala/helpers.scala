package helpers

import scala.xml._

/** Ad hoc helper functions to generate useful collections for
  * navigating the reddit folder in the main S3 bucket.
  */
object RedditHelper {
  def fileGenerator(fromYear: Int, fromMonth: Int,
    toYear: Int, toMonth: Int): Array[String] = {
    var curYear = fromYear
    var curMonth = fromMonth
    var redditFiles = Array[String]()
    while (curYear < toYear) {
      while (curMonth <= 12) {
        redditFiles = redditFiles :+ (s"RC_${curYear}-" ++ "%02d".format(curMonth))
        curMonth += 1
      }
      curMonth = 1
      curYear += 1
    }
    while (curMonth <= toMonth) {
      redditFiles = redditFiles :+ (s"RC_${curYear}-" ++ "%02d".format(curMonth))
      curMonth += 1
    }
    redditFiles
  }
}

/** Ad hoc helper functions to generate useful collections for
  * navigating the stack_exchange folder in the main S3 bucket.
  */
object StackExchangeHelper {

  /** Gets all top-level domain names that are part of the Stack
    * Exchange network.  This includes the meta domain names.
    */
  def getAllDomains(): Seq[String] = {
    val seXML = XML.load("https://archive.org/download/stackexchange/Sites.xml")
    (seXML \ "row").map(x => (x \"@Url").toString.drop(8))
  }

  /** For a given top-level domain, generates of sequence of resources
    * contained within the corresponding S3 folder.
    */
  def fileGenerator(domain: String): Seq[String] = {
    val files: Seq[String] = Seq(
      "Badges.xml",
      "Comments.xml",
      "PostHistory.xml",
      "PostLinks.xml",
      "Posts.xml",
      "Tags.xml",
      "Users.xml",
      "Votes.xml")
    files.map(file => s"${domain}/$file")
  }
}
