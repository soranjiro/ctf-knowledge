# Web Relations

Web 関連 writeup の index。
入力がどの構文・状態に入ったかで分類する。

## 関連 insights

- [Web](../insights/web.md)

## 事例一覧

- [Emojify](../writeup/alphahack/2025-w49/1203_emojify.md): URL parser/WAF の解釈差で SSRF する。
- [Alpaca Bank](../writeup/alphahack/2025-w50/1211_alpaca-bank.md): 自己送金の business logic bug で残高を増やす。
- [cat](../writeup/alphahack/2025-w51/1216_cat.md): `/dev/stdin` で subprocess に渡された `flag.txt` を読む。
- [omikuji](../writeup/alphahack/2025-w51/1220_omikuji.md): `../flag` の path traversal で結果 HTML に flag を埋める。
- [Log Viewer](../writeup/alphahack/2025-w52/1222_log-viewer.md): `awk` の regex/program 文脈に注入し、`system()` を呼ぶ。
- [Xmas Login](../writeup/alphahack/2025-w52/1225_xmas-login.md): password 欄の SQLi で複数 user の flag 断片を取る。

## 比較観点

- parser gap / SSRF: `Emojify`
- business logic: `Alpaca Bank`
- file read: `cat`, `omikuji`
- program injection: `Log Viewer`
- SQLi: `Xmas Login`
