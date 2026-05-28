# Rev

Rev は入力がどのように変換され、どこで正解と比較されるかを追う。
全部を完全に理解するより、比較点・データ定数・可逆変換・外部効果を先に押さえると速い。

## 初動

- `strings`, `file`, `checksec`, `objdump`, Ghidra/IDA で形式と比較関数を見る。
- `strcmp`, `memcmp`, `strncmp`, `printf`, `puts` の直前を確認する。
- static data 配列、S-box、key、出力列を探す。
- 入力長チェックを探す。

## 壊れやすい部分

- **平文比較**: 最後が `strcmp(input, expected)` なら breakpoint で expected を読む。
- **可逆な1文字変換**: `+ i`, `^ i`, key XOR は出力から戻せる。
- **関数ポインタ**: 候補関数が少なければ index ごとの呼び分け表にする。
- **難読化 script**: eval/Invoke-Expression の直前を表示する。
- **VM**: 命令セットが小さいなら emulator か Z3 で入力を解く。
- **IR/assembly**: レジスタや SSA を高級言語の変数へ写す。

## 考え方

1. 入力長と flag format を確認する。
2. 比較点を見つける。比較対象が平文か暗号文かを分ける。
3. 変換が可逆なら逆変換を書く。
4. 変換が複雑なら symbolic execution や Z3 へ寄せる。
5. 時間待ちや anti-debug が本質でなければ、patch/jump/hook で飛ばす。

## 実戦メモ

- 「複雑な処理」より「最後に何と比べるか」が重要。
- XOR は式を 0 条件から解く。`(input ^ a) ^ b == 0` なら `input = a ^ b`。
- VM は opcode 表を作った時点で半分解けている。状態が byte 配列なら BitVec(8) がよく合う。
