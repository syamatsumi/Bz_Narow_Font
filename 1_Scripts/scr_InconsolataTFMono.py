#!fontforge --lang=py -script

import fontforge
import psMat
import sys
import os

# BIZ UDゴシックの値に揃える
new_em_size = 2048
new_ascent = 1802
new_descent = 246
new_upos = -297
new_uwidth = 102

#余白を設定する
min_margin = 16

# コマンドライン引数の処理
if len(sys.argv) < 4:
    print("Usage: script.py <input_fontfile> <output_fontfile> <mono_width>", flush=True)
    sys.exit(1)

input_fontfile = sys.argv[1]  # 入力ファイル
output_fontfile = sys.argv[2]  # 出力ファイル
output_fontfile = f"{output_fontfile}.sfd"  # 出力ファイルの形式
mono_width = int(sys.argv[3])  # モノスペースとしての幅

# フォントを開く
font = fontforge.open(input_fontfile)

# SFDで一時保存
temp_file = f"temp{output_fontfile}"
font.save(temp_file)
print(f"Saved intermediate state to: {temp_file}", flush=True)

# TTFフォントを閉じる
font.close()

# SFDで保存した一時ファイルを開き直す
font = fontforge.open(temp_file)
print(f"Reopened temporary file: {temp_file}", flush=True)

# ASCII範囲にコンポジットグリフが居たら解除
for codepoint in range(0x20, 0x7F):
    if codepoint in font:
        glyph = font[codepoint]
        if not glyph.isWorthOutputting():
            continue  # 出力しないグリフはスキップ
        if len(glyph.references) > 0:
            glyph.unlinkRef() #コンポジットグリフの参照を解除

#EMサイズの変更
current_em_size = font.em #現在のEMサイズを取得
scale_factor = new_em_size / current_em_size #スケール割合を算出

font.em = new_em_size # font.transformの前にEMサイズを設定する
font.upos = new_upos  # 下線の位置（ベースラインより下に100単位）
font.uwidth = new_uwidth  # 下線の厚さ
font.transform(psMat.scale(scale_factor))

font.ascent = new_ascent #高さ
font.descent = new_descent #深さ

# 拡大率を計算
# EMの高さ
em_height = font.em

# 対象グリフ「(」
target_glyph_code = ord("(")

# 「(」のBoundingBoxを取得
glyph = font[target_glyph_code]
bbox = glyph.boundingBox()
ref_glyph_height = bbox[3] - bbox[1]  # 上端 - 下端

# 拡大率を計算（EM高さに収まる最大値）
scale_factor = em_height / ref_glyph_height

# 一律の拡大処理
for glyph in font.glyphs():
    if not glyph.isWorthOutputting():
        continue  # 出力しないグリフはスキップ
    if len(glyph.references) > 0:
        continue  # コンポジットグリフはスキップ
    
# 先に目星を付けたグリフの高さを基準に一律に拡大
    glyph.transform(psMat.scale(scale_factor))

# 特定の文字を高さ調整
font["parenleft"].transform(psMat.translate(0, 8))
font["parenright"].transform(psMat.translate(0, 8))
font["colon"].transform(psMat.translate(0, 275))
font["semicolon"].transform(psMat.translate(0, 275))
font["comma"].transform(psMat.translate(0, 166))
font["period"].transform(psMat.translate(0, 166))
font["bracketleft"].transform(psMat.translate(0, 75))
font["bracketright"].transform(psMat.translate(0, 75))
font["braceleft"].transform(psMat.translate(0, 45))
font["bar"].transform(psMat.translate(0, 166))
font["braceright"].transform(psMat.translate(0, 45))

# 個別の拡大処理
for glyph in font.glyphs():
    if not glyph.isWorthOutputting():
        continue  # 出力しないグリフはスキップ
    if len(glyph.references) > 0:
        continue  # コンポジットグリフはスキップ
# 下端のはみ出しを修正する処理
    bbox = glyph.boundingBox()
    xmin, ymin, xmax, ymax = bbox
# 下端が新しい深さを下回る場合、上辺を基準に縮小
    if ymin < -new_descent:
        height = ymax - ymin
        width = xmax - xmin
        magnific = (ymax + new_descent) / height
        glyph.transform(psMat.translate(0, -ymax))
        glyph.transform(psMat.scale(magnific, magnific))  # 縮小
        glyph.transform(psMat.translate(0, ymax))  # 先の移動を元に戻す

# 拡大縮小に伴う横スケールのバラツキを揃える
for glyph in font.glyphs():
    if not glyph.isWorthOutputting():
        continue  # 出力しないグリフはスキップ
    if len(glyph.references) > 0:
        continue  # コンポジットグリフはスキップ
    bbox = glyph.boundingBox()
    xmin, ymin, xmax, ymax = bbox
# グリフの幅を計算
    content_width = xmax - xmin
# 変数の初期化
    scale_x = 1.0  # 横方向のスケール
# 幅が基準を超える場合、縮小率を計算
    base_width = mono_width - min_margin * 2
    if content_width > base_width:
        scale_x = base_width / content_width
    # 変形適用
        glyph.transform(psMat.scale(scale_x, 1))

# グリフ幅の処理（モノスペース）
for glyph in font.glyphs():
    if not glyph.isWorthOutputting():
        continue  # 出力しないグリフはスキップ
    if len(glyph.references) > 0:
        continue  # コンポジットグリフはスキップ
# グリフのBoundingBoxを取得 (xmin, ymin, xmax, ymax)
    bbox = glyph.boundingBox()
    xmin, ymin, xmax, ymax = bbox
    rsbearing = glyph.width - xmax  # 右サイドベアリング
    content_width = xmax - xmin  # アウトラインの幅
    orig_width = glyph.width
# アウトライン両サイドのがグリフ幅-最小マージンx2より小さい時
    if content_width < glyph.width - min_margin * 2:
    # かつ左ベッタリだったときは左サイドベアリングを最小値まで移動
        if xmin < min_margin:
            glyph.transform(psMat.translate(min_margin - xmin , 0))
    # 右がべったりまたは飛び出して居る時は右マージンを最小マージンまで移動
        elif rsbearing < min_margin:
            glyph.transform(psMat.translate(rsbearing - min_margin , 0))
    # どっちつかずに狭いだけのグリフはなにもしない。
# アウトラインの幅が十分広くても右サイドベアリングが負になっている場合は寄せるだけ。
# 寄せたら左が飛び出すような場合については前工程にて補正済みのため考慮しない。
    elif rsbearing < min_margin:
        glyph.transform(psMat.translate(rsbearing - min_margin , 0))
# 念の為にグリフ幅をふたたび固定
    glyph.width = mono_width

# TTFに合わせた最適化処理
for glyph in font.glyphs():
    if not glyph.isWorthOutputting():
        continue  # 出力しないグリフはスキップ
    if len(glyph.references) > 0:
        continue  # コンポジットグリフはスキップ
    glyph.round()  # 最終的にTTFになるので、ここで整数化。
    glyph.removeOverlap()  # 整数化で重なったポイントを結合
    glyph.round()  # 結合処理で端数が出た時のために整数化
    glyph.addExtrema() # 極点を追加

# フォントを保存
font.save(output_fontfile)
os.remove(temp_file)
print(f"Font saved to: {output_fontfile}", flush=True)
