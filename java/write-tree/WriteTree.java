import java.util.*;

class WriteTree {
  public static void write(int n) {
    int bottom_n = (int) Math.pow(2, n);
    int digits = String.valueOf(bottom_n).length();

    int w = bottom_n * digits - 1;
    int p = 0;
    String v = "1";

    String[] line = new String[w];

    List<Integer> prev_pos = new ArrayList<Integer>();
    prev_pos.add(0);
    prev_pos.add(w);

    for (int i = 0; i < n; i++) {
      v = String.valueOf((int) Math.pow(2, i));

      // reset line
      for (int j = 0; j < w; j++) line[j] = "_";

      List<Integer> pos = new ArrayList<Integer>();
      pos.add(0);

      for (int j = 0; j < prev_pos.size() - 1; j++) {
        p = prev_pos.get(j) + (prev_pos.get(j + 1) - prev_pos.get(j)) / 2;
        pos.add(p);
        pos.add(prev_pos.get(j + 1));
        for (int k = 0; k < v.length(); k ++) line[p + k] = String.valueOf(v.charAt(k));
      }

      for (int j = 0; j < w; j++) System.out.print(line[j]);
      System.out.println();

      // buckup current pos
      prev_pos = new ArrayList<Integer>();
      for (int j = 0; j < pos.size(); j++) prev_pos.add(pos.get(j));
    }
  }

  public static void main(String[] args) {
    write(5);
  }
}
