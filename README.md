# Knowledge

このディレクトリは、CTF writeup から再利用可能な知見を育てるための知識ベースです。
個別 writeup をそのまま増やすだけでなく、抽象的な知見と具体的な参照関係を分けて蓄積します。

## 役割

- `writeup/` は個別の事例です。解いた問題、手順、観察、失敗、flag 取得までを残します。
- `insights/` は一般知識です。`rsa.md`、`pwn.md`、`web.md` のようなカテゴリ単位のファイルに、特定 writeup に依存しない見方や定石を書きます。
- `relations/` は接続層です。カテゴリ単位の relation で、関連 insight と具体 writeup の概要一覧を束ねます。

`insights`、`relations`、`writeup` は多対多でつながります。
1 つの relation が複数 insight を参照してよく、複数 writeup を参照してよいです。
1 つの insight も複数 relation から参照されます。

## 構成

```text
.knowledge/
├── README.md
├── SKILL.md
├── insights/
│   ├── rsa.md
│   ├── pwn.md
│   └── web.md
├── relations/
│   └── rsa.md
└── writeup/
    └── alphahack/2025-w49/1207_size-limit.md
```

## 運用ルール

- writeup を追加したら、関係する relation に追記します。
- relation には、関連する insight と確認元の writeup へのリンクを必ず入れます。
- 新しい一般知識が出たら `insights/{category}.md` を更新します。
- 具体例、例外、問題ごとの差分、offset、URL、制約などは writeup に置き、relation には index と比較観点を置きます。
- 1ファイルが1000行を超えて読みづらくなった場合だけ、サブフォルダや分割を検討します。
- 既存カテゴリで束ねにくい場合だけ、新しい relation/insight を作ります。

writeup は次の形式で置きます。

`writeup/{sponsor}/{year}-w{week}/mmdd_{title}.md`

例: [writeup/alphahack/2025-w49/1207_size-limit.md](writeup/alphahack/2025-w49/1207_size-limit.md)

## 使い分け

- insight: 「RSA では復号で得られる値は常に `m mod N` である」
- relation: 「この具体トピックは、どの insight とどの writeup を結ぶか」
- writeup: 「その問題で実際にどう手を動かしたか」
