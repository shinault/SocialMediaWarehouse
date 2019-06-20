package helpers

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
