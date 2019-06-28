name := "Data Catalog Builder"
version := "1.0"
scalaVersion := "2.11.12"


libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.4.3"
libraryDependencies += "com.databricks" % "spark-xml_2.11" % "0.5.0"
libraryDependencies += "org.postgresql" % "postgresql" % "9.4-1200-jdbc41"
libraryDependencies += "org.apache.hadoop" % "hadoop-aws" % "2.7.1"
libraryDependencies += "org.scalatest" % "scalatest_2.11" % "3.0.5" % "test"
libraryDependencies += "com.holdenkarau" %% "spark-testing-base" % "2.3.1_0.12.0" % "test"


parallelExecution in Test := false
