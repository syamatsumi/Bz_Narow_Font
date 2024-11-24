#!fontforge --lang=py -script
import fontforge
import psMat
import sys
import os
import math

# コマンドライン引数の処理
if len(sys.argv) < 4:
    print("Usage: script.py <input_fontfile> <output_fontfile> <italic_angle>", flush=True)
    sys.exit(1)

try:
    input_fontfile = sys.argv[1]  # 入力ファイル
    output_fontfile = sys.argv[2]  # 出力ファイル
    output_fontfile = f"{output_fontfile}.sfd"  # 出力ファイルの形式
    ITALIC_ANGLE = float(sys.argv[3]) # イタリック体の傾き（数値に変換）
except ValueError:
    print("Error: <italic_angle> must be numbers.", flush=True)
    sys.exit(1)

# フォントを開く
font = fontforge.open(input_fontfile)

# 傾きを設定する
font.italicangle = -ITALIC_ANGLE
# 全グリフを斜体に変換
for glyph in font.glyphs():
    orig_width = glyph.width
    glyph.transform(psMat.skew(ITALIC_ANGLE * math.pi / 180))
    glyph.transform(psMat.translate(-94, 0))
    glyph.width = orig_width

font.save(output_fontfile)  # フォントを保存
