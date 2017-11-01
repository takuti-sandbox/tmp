## 2. 基本的な書き方を身につける

- 修飾子
	- `transient`
		- フィールドをシリアライズ対象から除外
		- オブジェクトのファイル保存、ネットワーク送受信時などに不要になる一時データをシリアライズしなくて済む
	- `volatile`
		- マルチスレッドからアクセスされるフィールドに対して、スレッドごとに値がキャッシュされないようにする
		- スレッドセーフのため
	- `synchronized`
		- メソッドまたはブロックの同期
		- 同時に1つのスレッドからしかアクセスされないことが保証される
	- `native`
		- メソッドがネイティブコード（C/C++で書かれたDLL, 共有ライブラリなど）を呼び出す
	- `strictfp`
		- クラス、インタフェース、メソッドで浮動小数点数をIEEE 754規格で厳密に処理する
		- 厳密な浮動小数点演算によって、プラットフォーム間の移植性向上
- 変数名の後ろに `_` をつけるのはもはや不要
	- IDEで書くのが当たり前なので、フィールドとローカル変数の名前が一緒でも区別がつく
	- フレームワークによっては末尾の `_` によって変数のバインドに失敗するものもある
- 変数は名詞、メソッドは動詞で命名
	- booleanの変数名に `isXxx` とつけるのは違う
	- 変数名は `xxx` で、問い合わせるメソッドが `isXxx` と命名されるべき

## 3. 型を極める

- プリミティブ型
	- 桁数の多い数字はアンダースコアで区切りを表現できる：`long amount = 123_456_789L;`
	- Widening（ワイドニング；型のデータサイズが大きくなるような自動変換）は整合性が保たれる
		- e.g., short -> int
	- 逆に Narrowing（ナローイング）はコンパイルエラー (e.g., int -> short)
		- キャストすればコンパイルは通るけど、値はおかしくなる：`short shortNum = (short) intNum`
- 参照型
	- Wrapper Class：プリミティブ型を内包し、そのプリミティブ型の値を操作する機能を備えたもの
		- int <-> Integer, double <-> Double, ...
		- `Integer.MAX_VALUE`, `Float.MIN_VALUE`, ...
	- プリミティブ型からラッパークラスへの変換は、`valueOf`を使うと-127~128の範囲では事前に生成されたオブジェクトが利用できるので、メモリに優しい
	- プリミティブ型のintの初期値は0だが、ラッパークラスではNULL
		- ゼロとNULLを区別したいときはラッパークラスを使う
			- HTTP通信で取得した値やファイルから読み込んだ値のストアなど
	- Autoboxing: Primitive -> Wrapper Classへの変換 `Integer numInt = 10`
	- Unboxing: Wrapper Class -> Primitiveへの変換 `10 + Integer.valueOf(10)`
		- 依存しすぎると、ラッパークラスを誤って `==` で比較してしまってFalseになる、といったミスが発生する
			- -128 ~ 127の値をautoboxingしたオブジェクトだけは、事前に生成されたオブジェクトを使うので例外的に一致する
		- というわけで
			1. 原則としてautoboxing, unboxingは使用せず、明示的に変換
			2. ファイル、DB、HTTPリクエストなどの結果得られる値を保持する場合はラッパークラス
			3. 数値計算はプリミティブ型
			4. 記述量の削減（型変換を明記しないこと）が効果的な場合に限り、autoboxing, unboxingを利用
- クラス
	- 慣例として、他者が提供するライブラリやフレームワークなどとパッケージ名が重複してしまわないよう、自分が所有しているドメイン名を逆にしたものからパッケージ名を始める
	- フィールド、メソッドの修飾子は指定しないとパッケージプライベート（同一パッケージ内のクラスからのみ参照可能；`protected`はそれに加えて子クラスからも参照可能）
	- インタフェース
		- 絶対publicになるが、著者は省略せずに `public interface` とかく
		- メソッド定義のみで、処理は記述できない
			- が、Java8からは処理内容を定義する `default` メソッドが追加された
		- 匿名クラス
			- `public interface TaskHandler { ... }` -> `TaskHandler taskHandler = new TaskHandler() { ... };`
			- クラスを特定の一箇所で使うだけなら、 `implement` した名前のあるクラスを定義するよりもかんたん
	- nested class の使い方はEffective Java参照
- オブジェクトの等価性
	- `public boolean equals(Object obj)`
		- フィールドの値に基づく比較（値を1つずつ比較するので時間がかかる）
	- `public int hashCode()`
		- 同じオブジェクトなら同じハッシュ値を返す
		- ハッシュ値が異なれば異なるオブジェクト
		- 異なるオブジェクトでもハッシュ値が異なることはある
		- （intの値の比較だけなので高速）
	- `HashMap` や `HashSet` では、
		1. 最初にハッシュ値でオブジェクトを比較
		2. ハッシュ値が一致した場合に限り、`equals()`で厳密に値の一致判定
	- `equals()` と `hashCode()` の両方で等価だと判断されないと、オブジェクトはイコールにならない
		- 両メソッドはEclipseだとフィールドに基づいて自動生成される
		- `Objects.hash(v1, v2, ...)` を使えばハッシュ値生成簡単
- `enum`
	- `public static final` による定数は型安全ではない
		- `String COLOR_RED`, `String COLOR_GREEN`, `String COLOR_BLUE` のいずれかを取りたいメソッドを書くとき、引数の型はただの `String` になるので、 `"aaa"` のような意図しない入力も受け付けてしまう
		- 定数をコンパイルした結果はただの値； `String s = COLOR_RED` でも、コンパイル結果は `String s = "red"`
	- なので、`enum`型でいくつかの定数の集まりを表現する
		```
		public enum Color {
			RED, GREEN, BLUE
		};
		```
		- すると、`setColor(Color c)` のような、想定した値以外は受け付けない型安全な定数利用が可能
	- フィールドやメソッドの定義も可能
		```
		public enum HttpStatus {
			OK(200), NOT_FOUND(404), INTERNAL_SERVER_ERROR(500);

			private final int value;

			private HttpStatus(int value) { // enum のコンストラクタは private
				this.value = value;
			}
			public int getValue() {
				return value;
			}
		}
		```
- ジェネリクスで様々な型を受け付ける汎用的なクラス・メソッド定義

## 4. 配列とコレクションを極める

### List

- Listを for-each と iterator のどちらで探索するか？
	- 要素に対する操作（削除、更新）も行いたい時は iterator
- ArrayList
	- **forなどをつかった全体的な繰り返し処理向き**
	- 内部に配列を保持していて、そのサイズは何も指定しないと10
	- このサイズを超えるとき、「よりサイズの大きい配列を新たに生成して、元の配列から全要素をコピーする」処理が発生して非効率
	- 要素数の目安が事前についているのなら、コンストラクタでそれを設定したほうが無駄な配列生成＆コピー処理が削減できる
- LinkedList
	- **配列をiterateしつつ、途中で要素の追加/削除を行うとき**
- CopyOnWriteArray
	- **複数のスレッドから同時にアクセスしても正しく処理される** ArrayList の拡張

### Map

- HashMap
	- キーの `hasCode` メソッドでハッシュ値計算→ハッシュテーブルのサイズで割った余りをインデックスにする
	- 値を取り出すとき、同一インデックスに複数のEntryがあれば先頭から順に `equals` で比較しながら一致するkey-valueペアをlookup
	- ハッシュテーブルの初期サイズは16で、要素数がその75％に達するとサイズを自動で拡張する
		- サイズ <<< 要素数 だとハッシュ値の競合が増えてloopupに時間がかかるようになるため　
- ConcurrentHashMap
	- ハッシュテーブルの拡張と要素の追加が同時に起こると無限ループになりうるので、atomicに複数スレッドからの処理をさばく
	- `synchronized` を使うのも手
- LinkedHashMap
	- 要素の追加順序を保持したいとき
- TreeMap
	- キーの大小を意識するとき

### Set

- 内部的にはMapを持っていて、キーだけを使っているのがSet
	- 値は null 以外ならなんでもいいけど、通常は true
- なのでインタフェース、使い分けはMapと同じ
	- HashSet
	- LinkedHashSet
	- TreeSet
- ConcurrentHashSet は存在しない
	- `Collections.newSetFromMap()` で ConcurrentHashMap からセットが作れるので


### Stream

- Lambda
- メソッド参照
	- `list.forEach(System.out::println)` は `list.forEach(s -> System.out,.println(s))` と同じ
	- 引数の数と型が一致していれば、処理の内容としてメソッドそのものを代入できる
- streamの作成は `list.stream()` など
	- Mapの場合はEntrySetを取得してから、そのSetのStreamメソッドを呼び出すことで生成
		- `map.entrySet().stream().forEach(e -> /* something for e.getKey() and e.getValue() */)`