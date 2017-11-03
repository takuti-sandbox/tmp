import java.util.Optional;

public class OptionalStackTest {
  public static void main(String... args) {
    OptionalStack<String> optStack = new OptionalStack<>();

    Optional<String> opt = optStack.pop(); // this hsould be empty
    String elem = opt.orElse("empty");
    System.out.println(elem);

    optStack.push("Foo");
    optStack.push("Bar");
    optStack.push("Baz");

    opt = optStack.pop();
    if (opt.isPresent()) {
      System.out.println(opt.get()); // Baz
    }

    opt = optStack.pop();
    opt.ifPresent(System.out::println); // Bar
  }
}
