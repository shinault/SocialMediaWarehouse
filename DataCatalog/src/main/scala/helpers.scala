package helpers

import scala.xml._

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

object StackExchangeHelper {
  def getAllDomains(): Seq[String] = {
    val seXML = XML.load("https://archive.org/download/stackexchange/Sites.xml")
    (seXML \ "row").map(x => (x \"@Url").toString)
  }

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
