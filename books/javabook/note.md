### hashCode

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