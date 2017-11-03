import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class OptionalStack<E> {
  private List<E> stack;

  public OptionalStack() {
    this.stack = new ArrayList();
  }

  public boolean push(E elem) {
    return this.stack.add(elem);
  }

  public Optional<E> pop() {
    if (this.stack.isEmpty()) {
      return Optional.empty();
    }
    return Optional.of(this.stack.remove(this.stack.size() - 1));
  }
}
