import org.scalatest._
import helpers.{RedditHelper => RH, StackExchangeHelper => SEH}

class HelperSpecs extends FunSuite {
  test("RedditHelper generates files correctly") {
    assert(RH.fileGenerator(2015, 2, 2015, 2) === Array("RC_2015-02"))
    assert(RH.fileGenerator(2015, 12, 2016, 1) === Array("RC_2015-12", "RC_2016-01"))
    val correctVal = Array("RC_2015-12",
      "RC_2016-01",
      "RC_2016-02",
      "RC_2016-03",
      "RC_2016-04",
      "RC_2016-05",
      "RC_2016-06",
      "RC_2016-07",
      "RC_2016-08",
      "RC_2016-09",
      "RC_2016-10",
      "RC_2016-11",
      "RC_2016-12",
      "RC_2017-01")
    assert(RH.fileGenerator(2015, 12, 2017, 1) === correctVal)
  }

  test("StackExchangeHelper retrieves domains and formats correctly") {
    val seDoms = SEH.getAllDomains()
    assert(seDoms(0) == "softwareengineering.stackexchange.com")
    assert(seDoms(1) == "softwareengineering.meta.stackexchange.com")
    assert(seDoms(2) == "english.stackexchange.com")
    assert(seDoms.length == 346)
  }

  test("StackExchangeHelper joins file names with domains correctly") {
    val correct = Seq("domain/Badges.xml",
      "domain/Comments.xml",
      "domain/PostHistory.xml",
      "domain/PostLinks.xml",
      "domain/Posts.xml",
      "domain/Tags.xml",
      "domain/Users.xml",
      "domain/Votes.xml")
    assert(SEH.fileGenerator("domain") === correct)
  }
}
