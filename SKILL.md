# SKILL

このリポジトリでは、CTF の個別 writeup を材料にして topic ごとの知見を育てる。
writeup は事例、insights は一般知識、relations は insights と writeup をつなぐ接続層として扱う。

## ディレクトリ

- 個別事例は [writeup/](writeup) に置く。
- 一般知識は [insights/](insights) に置く。原則として `insights/rsa.md`、`insights/pwn.md`、`insights/web.md` のようにカテゴリ単位の1ファイルへ集約する。
- 具体参照と接続情報は [relations/](relations) に置く。

## 粒度

- `insights/{category}.md` は、特定の問題名や writeup に依存しない形で書く。計算方法、典型的な脆弱性、考え方、初動の見方をまとめる。
- `relations/{category}.md` は、複数の insight と複数の writeup を結び、具体例の概要一覧と writeup への index を置く。
- `insights`、`relations`、`writeup` は多対多で扱う。1:1 の対応表にしない。
- 1 つの writeup が複数 topic に関係する場合は、複数 relation から参照してよい。
- 1 つの relation が複数 insight に関係する場合は、`関連 insights` にすべて列挙する。
- 細かい topic ごとにファイルを増やしすぎない。1ファイルが1000行を超え、読みにくくなった場合だけサブフォルダや分割を検討する。
- `plaintext-size-limit` のような具体事例寄りの名前は、insight ではなく relation 側の具体例として扱う。insight では RSA 全体の見方や計算方法に吸収する。

## メタデータ

各 writeup には、`category`、`genre`、`difficulty`、`tags` を入れる。
LLM が拾う前提なので、短く揃えた表現を使う。

## 使い方

- 問題を解いたら `writeup/{source}/{year}-w{week}/mmdd_{title}.md` に追加する。
- その writeup から再利用できる見方を抽出し、カテゴリ別の relation に追記する。
- relation からカテゴリ別 insight を参照し、足りない一般知識がある場合だけ insight を追加または更新する。
- 具体的な観察、offset、URL、制約、例外、失敗などは writeup に置き、relation には概要と比較観点だけを置く。
- relation と insight は必ずしも同時に 1 ペアで作らない。
