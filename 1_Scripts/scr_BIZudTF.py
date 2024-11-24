#!fontforge --lang=py -script
import fontforge
import psMat
import sys
import os

# コマンドライン引数の処理
if len(sys.argv) < 5:
    print("Usage: script.py <input_fontfile> <output_fontfile> <stroke_width> <vshrink_ratio>", flush=True)
    sys.exit(1)

try:
    input_fontfile = sys.argv[1]  # 入力ファイル
    output_fontfile = sys.argv[2]  # 出力ファイル
    output_fontfile = f"{output_fontfile}.sfd"  # 出力ファイルの形式
    str_width = float(sys.argv[3])  # 太らせる単位の大きさ（数値に変換）
    vshrink_ratio = float(sys.argv[4])  # 横に縮める比率（数値に変換）
except ValueError:
    print("Error: <stroke_width> and <vshrink_ratio> must be numbers.", flush=True)
    sys.exit(1)

# フォントを開く
font = fontforge.open(input_fontfile)

# SFDに変換する
temp_file = f"temp_0_{output_fontfile}"
font.save(temp_file)
print(f"SFDに変更して再開する。file:  {temp_file}", flush=True)
font.close() # TTFフォントを閉じる
import time  # 書き込みが完了するまで少し待つ
time.sleep(0.1)
font = fontforge.open(temp_file) # SFDで保存した一時ファイルを開き直す
print(f"SFDを開きなおした。 file: {temp_file}", flush=True)

# ループ前の変数宣言
proc_cnt: int = 0
del_aftr: int = 0

# ループ前にフォントの元情報を把握
font_weight = font.os2_weight
em_size = font.em

# 全グリフに変形処理を適用
for glyph in font.glyphs():
    if not glyph.isWorthOutputting():
        continue  # 出力しないグリフはスキップ
    if len(glyph.references) > 0:
        print(f"合成グリフをスキップ： {glyph.glyphname}", flush=True)
        continue  # コンポジットグリフはスキップ

# 1000個処理したら仮保存
    proc_cnt += 1
    if proc_cnt % 1000 == 1:
        print(f"作業前保存中のグリフ： {glyph.glyphname}", flush=True)
        temp_file = f"temp_{proc_cnt}_{output_fontfile}"
        font.save(temp_file)
        del_aftr = proc_cnt #ファイル作成時点の番号を控える
    # 前回の仮保存ファイルを削除
        print(f"前の一時ファイルを削除： {del_file}", flush=True)
        del_file = f"temp_{del_aftr}_{output_fontfile}"
        os.remove(del_file)

# 本グリフが半角グリフかチェックする
    if glyph.width ==  em_size / 2:
        halfwidth_glyph_flag = True
    else :
        halfwidth_glyph_flag = False

# グリフのウエイトとポイント数を勘案してストロークの幅を変える
    point_count = sum(len(contour) for contour in glyph.layers[glyph.activeLayer])
    if point_count < 300 or font_weight > 700:
        stroke_width = round(str_width * 0.5)
    elif point_count < 150 and font_weight > 500:
        stroke_width = round(str_width * 0.8)
    else :
        stroke_width = str_width
# 縦に拡大する
    glyph.transform((1, 0, 0, 16, 0, 0))  # 縦に伸ばす
    glyph.addExtrema() # 極点を追加
    glyph.layers["Back"] = glyph.layers["Fore"]
# 前面全体をストローク処理
    glyph.stroke("elliptical", stroke_width, 10, 0, "round", "miterclip",
        # "circular", width[, CAP, JOIN, ANGLE, KEYWORD],
        # "elliptical", width, minor_width[, ANGLE, CAP, JOIN, KEYWORD],
        # "calligraphic", width, height[, ANGLE, CAP, JOIN, KEYWORD],
        # "convex", contour[, ANGLE, CAP, JOIN, KEYWORD],
        removeinternal=False,  # Default=False
        removeexternal=False,  # Default=False
        extrema=False,  # Default=True
        simplify=False,  # Default=True
        removeoverlap="none",  # Default="layer" "contour" "none"
        accuracy=0.5,  # default=0.25
        jlrelative=False,  # Default=True
        joinlimit=0.05,  # Default=20
        ecrelative=True,  # Default=True
        extendcap=0.1,  # Default=0
        arcsclip="ratio"  # Default="auto" "arcs" "svg2" "ratio"
    )

# 閉じたパスを背面で保護
    closed_paths = [contour for contour in glyph.foreground if contour.closed]
    for contour in closed_paths:
        glyph.background += contour  # 輪郭を1つずつ追加
# 正常なパスを前面から削除    
    remaining_paths = [contour for contour in glyph.foreground if contour not in closed_paths]
    glyph.clear()  # フォアグラウンドをクリア
    for contour in remaining_paths:
        glyph.foreground += contour  # 必要な輪郭を再追加
# 開いたパスを閉じる
    for contour in glyph.foreground:
        if not contour.closed:  # 開いたパスかどうかを確認
            contour.closed = True  # 強制的に閉じる
# 強制的に閉じたパスを背面で保護
    closed_paths = [contour for contour in glyph.foreground if contour.closed]
    for contour in closed_paths:
        glyph.background += contour
# 閉じたパスを前面から削除    
    remaining_paths = [contour for contour in glyph.foreground if contour not in closed_paths]
    glyph.clear()
    for contour in remaining_paths:
        glyph.foreground += contour
# なおも開いたパスを強く単純化して安全狙いのストローク
    if glyph.foreground:
        glyph.simplify()
        glyph.stroke("circular", 15, 0, 0, "round", "round")
# 各レイヤの合成
    glyph.layers["Fore"] += glyph.layers["Back"]
    glyph.layers["Back"] = fontforge.layer()  # 背面をクリア
# 結合
    glyph.removeOverlap()  # 結合
        # glyph.exclude()  # くり抜き
        # glyph.intersect()  # 重なりの抽出
# 最初に縦に伸ばした奴を元に戻す＆幅を縮小
    glyph.transform((vshrink_ratio, 0, 0, 0.0625, 0, 0))
# 幅のストロークで太ったアウトラインを引き締める。
# グリフの幅まで変わると困るのでレイヤー単位で操作
    stroke_shrink = 1 - (stroke_width / em_size)
    glyph.layers["Fore"].transform((stroke_shrink, 0, 0, 1, 0, 0))
# 半角グリフの幅を再設定する
    if halfwidth_glyph_flag:
        glyph.width = round(em_size / 2 * vshrink_ratio)    
# グリフ左端が0より左にある場合を補正
    bbox = glyph.boundingBox()  # (xmin, ymin, xmax, ymax)
    if bbox[0] < 0:
        glyph.layers["Fore"].transform(psMat.translate(-bbox[0], 0))  # X軸方向に右へ移動
# 実際の幅が glyph.width より大きい場合、横方向に縮める
    bbox_width = bbox[2] - bbox[0]  # xmax - xmin
    if bbox_width > glyph.width:
        shrink_ratio = glyph.width / bbox_width  # 縮小率を計算
        glyph.transform(psMat.scale(shrink_ratio, 1))  # 横方向に縮小
# グリフ右端がグリフ幅より右にある場合を補正
    bbox = glyph.boundingBox()  # (xmin, ymin, xmax, ymax)
    if bbox[2] > glyph.width:
        glyph.layers["Fore"].transform(psMat.translate(bbox[2]-glyph.width, 0))  # X軸方向に左へ移動
# 最後にTTFの仕様に合わせた最適化を実施
    glyph.simplify()# 単純化
        # 参考。
        # [error_bound, flags, tan_bounds, linefixup, linelenmax]
        #"ignoreslopes",  # Allow slopes to change
        #"ignoreextrema",  # Allow removal of extrema
        #"smoothcurves",  # Allow curve smoothing
        #"choosehv",  # Snap to horizontal or vertical
        #"forcelines",  # flatten bumps on lines
        #"nearlyhvlines",  # Make nearly horizontal/vertical lines be so
        #"mergelines",  # Merge adjacent lines into one
        #"setstarttoextremum",  # Rotate the point list so that the start point is on an extremum
        #"removesingletonpoints",  # If the contour contains just one point then remove it
    glyph.round()  # 整数化
    glyph.removeOverlap()  # 結合
    glyph.round()  # 整数化
    glyph.addExtrema() # 極点を追加
    print(f"done:{proc_cnt}:{glyph.glyphname}", flush=True)

try:
    print(f"完成したフォントを保存： {output_fontfile}", flush=True)
    font.save(output_fontfile)  # フォントを保存
except IOError as e:
    print(f"保存に失敗しました: {e}")
else:
    print(f"前の一時ファイルを削除： {del_file}", flush=True)
    del_file = f"temp_{del_aftr}_{output_fontfile}"
    os.remove(del_file)

print("処理が完了しました。Enterを押して待機状態を終了しましょう。")
input()  # ユーザーがEnterを押すまで待機
