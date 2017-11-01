import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;

public class StreamTest {
  public static void testRange() {
    IntStream.rangeClosed(1, 3).forEach(System.out::println);
  }

  public static void testFilterForEach() {
    List<Student> students = Arrays.asList(new Student("Ken", 100), new Student("Shin", 60), new Student("Takuya", 80));
    students.stream()
            .filter(s -> s.getScore() >= 70)
            .forEach(System.out::println);
  }

  public static void testSort() {
    List<Student> students = Arrays.asList(new Student("Ken", 100), new Student("Shin", 60), new Student("Takuya", 80));
    Collections.sort(students, (s1, s2) -> Integer.compare(s1.getScore(), s2.getScore()));
    students.forEach(System.out::println);
  }

  public static void testMapStream() {
    Map<String, Integer> studentMap = new HashMap<>();
    studentMap.put("Ken", 100);
    studentMap.put("Shin", 60);
    studentMap.put("Takuya", 80);
    studentMap.entrySet().stream() // Stream<Entry<String, Integer>>
              .map(e -> new Student(e.getKey(), e.getValue().intValue()))
              .map(Student::getScore)
              .sorted((s1, s2) -> {
                 if (s1 > s2) {
                   return -1;
                 } else if (s1 < s2) {
                   return 1;
                 }
                 return 0;
               })
              .forEach(System.out::println);
  }

  public static void testSum() {
    double sum = DoubleStream.of(0.1, 0.2, 0.3).sum();
    System.out.println(sum);
  }

  public static void testGroupingBy() {
    Arrays.asList(new Student("Ken", 100), new Student("Shin", 60), new Student("Takuya", 80), new Student("Satoshi", 80))
      .stream()
      .collect(Collectors.groupingBy(Student::getScore))
      .entrySet()
      .stream() // Stream<Map<Integer, List<Student>>>
      .forEach(e -> System.out.println(e.getKey() + ": " + e.getValue().size()));
  }

  public static void testRepeat() {
    System.out.println(IntStream.range(0, 10).mapToObj(i -> "?").collect(Collectors.joining(", ")));
  }

  public static void main(String... agrs) {
    System.out.println("> testFilterForEach");
    testFilterForEach();

    System.out.println("> testSort");
    testSort();

    System.out.println("> testRange");
    testRange();

    System.out.println("> testMapStream");
    testMapStream();

    System.out.println("> testSum");
    testSum();

    System.out.println("> testGroupingBy");
    testGroupingBy();

    System.out.println("> testRepeat");
    testRepeat();
  }
}
