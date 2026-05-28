---
title: omikuji
category: web
genre: path-traversal
difficulty: medium
tags:
  - arbitrary-file-read
  - path-traversal
  - file-content-template
source: alpacahack:omikuji
solved_at: 2026-05-29
---

# omikuji

## 問題の要点

- POST body の `type` からコンテンツを取り、結果 HTML に埋め込む。
- `getResultContent(type)` がファイルパスとして `type` を扱う。
- `../flag` のような traversal が通る。

## 解き方

```bash
curl "$BASE/save" \
  -H 'Content-Type: text/plain' \
  --data-raw '../flag'
```

返ってきた result HTML に flag の内容が入る。

## 知見

- テンプレート出力先がランダムでも、埋め込む content の取得元が path traversal なら読み出せる。
- ファイル名として受け取る値は allowlist に寄せる。denylist だと `../`, symlink, URL decode で崩れやすい。

## 連携する知見

- [Web](../../../insights/web.md)
- [Web relations](../../../relations/web.md)
