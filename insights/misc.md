# Misc

Misc はジャンル横断の観察問題が多い。
暗号・Pwn・Web の定石だけでなく、UI、Cookie、正規表現、shell の短い構文、問題文の含みを拾う。

## 初動

- 配布物、ページ、Cookie、headers、保存状態、metadata を見る。
- 問題文の単語を素直に受け取る。数字、日付、伝統、静かさ、制限などがヒントになる。
- 入力制限があるときは、その制限内で使える構文を列挙する。

## 壊れやすい部分

- **oracle**: `Hit/Miss` のような1 bit 応答でも、prefix を伸ばせば secret が漏れる。
- **regex**: `^prefix`, character class, alternation で探索できる。
- **short shell payload**: `|sh` のように環境や標準入出力を利用する。
- **browser state**: Cookie/localStorage に flag や token がある。
- **calendar/date**: 問題の月・日・曜日がそのまま key になることがある。

## 考え方

1. 「計算する問題」か「観察する問題」かをまず分ける。
2. 返ってくる情報が少なくても、繰り返し問い合わせられるなら oracle 化する。
3. 入力制限が短いほど、既存の実行環境に乗る payload を探す。
4. Web 的な Misc では DevTools と HTTP raw response を見る。

## 実戦メモ

- Easy Misc はソースや本文より Cookie が答え、ということも普通にある。
- 正規表現 oracle は線形探索でも解けるが、文字クラスで二分探索できることが多い。
