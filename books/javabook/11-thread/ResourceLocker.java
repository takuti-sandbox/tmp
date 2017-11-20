import java.util.List;

public class ResourceLocker implements Runnable {
  private String name;
  private List<String> fromList;
  private List<String> toList;

  public ResourceLocker(String name, List<String> fromList, List<String> toList) {
    this.name = name;
    this.fromList = fromList;
    this.toList = toList;
  }

  public void run() {
    String str = null;
    try {
      System.out.printf("[%s] started.\n", name);

      Thread.sleep(500L);

      System.out.printf("[%s] attempt to lock fromList(%s).\n", name, fromList);
      synchronized (fromList) {
        System.out.printf("[%s] fromList(%s) was locked.\n", name, fromList);

        str = fromList.get(0);
        System.out.printf("[%s] %s <- fromList(%s).\n", name, str, fromList);

        Thread.sleep(500L);

        System.out.printf("[%s] attempt to lock toList(%s).\n", name, toList);
        synchronized (toList) {
          System.out.printf("[%s] toList(%s) was locked.\n", name, toList);

          toList.add(str);
          System.out.printf("[%s] %s -> toList(%s).\n", name, str, toList);
        }
      }
    } catch (InterruptedException e) {
      e.printStackTrace();
    } finally {
      System.out.printf("[%s] finished.\n", name);
    }
  }
}
