import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class FileIoTest {
  public static void main(String... args) {
    Path path = Paths.get("userlist.txt");
    try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
      reader.lines()
            .map(s -> s.split(" ")[0]).distinct()
            .forEach(System.out::println);
    } catch (IOException e) {
      System.err.println(e);
    }
  }
}
