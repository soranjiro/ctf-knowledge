---
title: hit-and-miss
category: misc
genre: oracle
difficulty: easy
tags:
  - regex-oracle
  - prefix-leak
  - brute-force
source: alpacahack:hit-and-miss
solved_at: 2026-05-29
---

# hit-and-miss

## 問題の要点

- サーバーに regex を送ると、secret flag にマッチしたかどうかが `Hit!` / `Miss!` で返る。
- 試行回数の制限が実質ない。

## 解き方

`^Alpaca\{...` のように prefix 固定の正規表現を投げ、1文字ずつ候補を伸ばす。

```python
chars = string.ascii_letters + string.digits + "_}"
flag = r"Alpaca\{"

while True:
    for ch in chars:
        pattern = f"^{flag}{re.escape(ch)}"
        if is_hit(pattern):
            flag += r"\}" if ch == "}" else ch
            break
```

文字クラス `[...]` を使えば二分探索もできる。

## 得られた flag

```text
Alpaca{Reg3x_Crossw0rd}
```

## 知見

- yes/no oracle は、暗号でなくても secret extraction になる。
- regex を受け取るサービスでは、完全一致だけでなく prefix match や文字クラスによる探索が情報漏えいになる。

## 連携する知見

- [Misc](../../../insights/misc.md)
- [Misc relations](../../../relations/misc.md)
