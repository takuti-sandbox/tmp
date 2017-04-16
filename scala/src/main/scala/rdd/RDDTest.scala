import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._

import org.apache.spark.rdd.RDD

import scala.util.Random

object RDDTest {
  val conf: SparkConf = new SparkConf().setMaster("local").setAppName("RDDTest")
  val sc: SparkContext = new SparkContext(conf)

  val rng: Random = new Random
  val randomList: List[Int] = (for (i <- 1 to 10000) yield rng.nextInt).toList

  def time[R](block: => R): R = {
    val t0 = System.nanoTime()
    val result = block
    val t1 = System.nanoTime()
    println("Elapsed time: " + ((t1 - t0) / 1000000000.0) + " sec")
    result
  }

  def f(v: Int): Int = {
    for (i <- 1 to 10000) {}
    v
  }

  def main(args: Array[String]) {
    val nIter = 1000

    for (i <- 1 to 3) { // try 3 times
      println("========")
      println("Uncached")
      println("========")
      time {
        val rdd: RDD[Int] = sc.parallelize(randomList).map(f)
        for (i <- 1 to nIter) rdd.count()
      }

      println("========")
      println("Cached")
      println("========")
      time {
        val rddCached: RDD[Int] = sc.parallelize(randomList).map(f).cache()
        for (i <- 1 to nIter) rddCached.count()
      }
    }

    sc.stop()
  }
}
