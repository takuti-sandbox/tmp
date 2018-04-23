import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

class Foo {
  private static void refHashMapElement() {
    Map<String, float[]> m = new HashMap<String, float[]>();
    m.put("a", new float[] {1.f, 2.f});
    float[] a = m.get("a");
    Arrays.fill(a, 0.f);
    a[0] = 100;
    System.out.println(m.get("a")[0] + " " + m.get("a")[1]);
  }

  private static void ref2dArrayElement() {
    float[][] aa = new float[2][3];
    float[] aaa = aa[0];
    aaa[0] = 100;
    System.out.println(aa[0][0] + " " + aa[0][1]);
  }

  private static void refListElement() {
    List<float[]> lst = new ArrayList<float[]>();
    float[] arr = new float[] { 1, 2, 3 };
    lst.add(arr);
    arr[0] = 100;
    System.out.println(lst.get(0)[0]);
  }

  private static void copyList() {
    List<float[]> lst = new ArrayList<float[]>();
    float[] arr = new float[] { 1, 2, 3 };
    lst.add(arr);

    System.out.println("=== addAll() (shallow copy) test");
    List<float[]> lst2 = new ArrayList<float[]>();
    lst2.addAll(lst);
    System.out.println(lst.get(0)[0] + " " + lst2.get(0)[0]);
    arr[0] = 1000;
    System.out.println(lst.get(0)[0] + " " + lst2.get(0)[0]);

    System.out.println("=== clone() (deep copy) test");
    List<float[]> lst3 = new ArrayList<float[]>();
    lst2.addAll(lst);
    for (float[] elem : lst) {
      lst3.add(elem.clone());
    }
    System.out.println(lst.get(0)[0] + " " + lst3.get(0)[0]);
    arr[0] = 0;
    System.out.println(lst.get(0)[0] + " " + lst3.get(0)[0]);
  }

  private static void normalize() {
    float[] ary = new float[] {0.99999f, 1e-32f};
    System.out.println("Original: " + ary[0] + " " + ary[1]);
    double sum = 0.d;
    for (int i = 0; i < 2; i++) {
      sum += ary[i];
    }
    for (int i = 0; i < 2; i++) {
      ary[i] /= sum;
    }
    System.out.println("Normalized: " + ary[0] + " " + ary[1]);
  }

  private static void compareString() {
    String s = "did";
    System.out.println(s == "did");
  }

  private static void checkMaxAndInfinity() {
    System.out.println(Double.MAX_VALUE + " " + Math.sqrt(Double.MAX_VALUE));
    System.out.println(Double.POSITIVE_INFINITY + " " + Math.sqrt(Double.POSITIVE_INFINITY));
  }

  private static void multibytes () {
    String ss = "xž";
    System.out.println(ss.length());
    System.out.println(ss.getBytes().length);
    System.out.println(new String(ss.getBytes()));
  }

  private static void parseDouble () {
    System.out.println((Double.parseDouble("1.619520626263693E-4") + 1.d));
  }

  public static void main(String[] args) {
    refHashMapElement();

    System.out.println("---");

    ref2dArrayElement();
    refListElement();

    copyList();

    normalize();

    compareString();

    checkMaxAndInfinity();

    multibytes();

    parseDouble();
  }
}
