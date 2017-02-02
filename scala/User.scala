class User(val name: String, val age: Int)

object User {
  def printUser(user: User) = println(user.name + " " + user.age)
}
