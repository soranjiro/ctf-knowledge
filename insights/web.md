# Web

Web 問は、入力がどの構文・どの状態・どの権限境界に入るかを見る。
SQL、URL、shell、awk、path、template、Cookie など、見た目は同じ文字列でも、解釈する側が変わると脆弱性の種類も変わる。

## 初動

- ルーティングと API を一覧化する。
- 入力値が入る先を分類する: DB query, subprocess, file path, URL parser, template, auth/session。
- 状態を確認する: Cookie, localStorage, sessionStorage, headers, generated file。
- role や user id を変える: self-transfer, target user, admin name, duplicate request。

## 壊れやすい部分

- **business logic**: 自己送金、負数、二重送信、同時実行、境界金額。
- **SQLi**: username に制限があっても password 側など別 field から条件を作れる。
- **path traversal**: denylist は `../`, symlink, `/dev/stdin`, `/proc/self/fd` で迂回されやすい。
- **command/program injection**: shell でなくても awk/sed/grep などの構文に入れば injection。
- **SSRF/parser gap**: WAF と実際の URL parser の解釈差を見る。
- **browser state leak**: Cookie や storage に flag がそのままあることがある。

## 考え方

1. 文字列が最終的に誰に解釈されるかを見る。
2. denylist より allowlist の有無を見る。denylist なら別名や別構文を探す。
3. 認証・権限は「ログインできるか」だけでなく「どの user の条件で処理されるか」を見る。
4. ファイル読みは path だけでなく fd と標準入力も見る。
5. 出力が HTML に保存されるなら、結果ページ経由で読めるか見る。

## 実戦メモ

- `subprocess.run([...])` は shell injection を避けるだけで、呼び出し先プログラムへの injection は防がない。
- Web easy/misc では DevTools の Application/Network タブが最短のことがある。
- 仕様上「ありえない操作」、例えば自分から自分への送金は最初に試す。
