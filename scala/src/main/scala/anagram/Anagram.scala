object Anagram {
  def isAnagram(s1: String, s2: String): Boolean =
    if (s1.length != s2.length) false
    else if (s1 == s2) true
    else s1.groupBy(c => c) == s2.groupBy(c => c)

  def main(args: Array[String]): Unit = {
    assert(args.length == 2, "You need to pass 2 words")
    println(isAnagram(args(0).toLowerCase(), args(1).toLowerCase()))
  }
}
