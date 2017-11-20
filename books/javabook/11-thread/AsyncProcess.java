public class AsyncProcess implements Runnable {
  private AsyncCallback callback;

  public AsyncProcess(AsyncCallback callback) {
    this.callback = callback;
  }

  public void run() {
    try {
      Thread.sleep(1000L);
      this.callback.notify("Finished.");
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
    System.out.println("AsyncProcess is finished.");
  }
}
