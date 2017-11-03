public class ExceptionTest {
  public static void handleApplicationException(ApplicationException e) {
    String id = e.getId();
    Object[] params = e.getParams();

    System.out.println("ApplicationException due to " + id + " at line:" + params[0] + " written by " + params[1]);
  }

  public static double divideBy(int n) throws ApplicationException {
    if (n == 0) {
      throw new ApplicationException("BUG", 3, "Mike");
    }
    return 10.0 / n;
  }

  public static void main(String... args) {
    try {
      divideBy(0);
    } catch (ApplicationException e) {
      handleApplicationException(e);
    }
  }
}
