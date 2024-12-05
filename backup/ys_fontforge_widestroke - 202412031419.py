#!fontforge --lang=py -script

import fontforge
import psMat

from .ys_fontforge_Remove_artifacts import ys_rm_little_line, ys_rm_small_poly
from .ys_fontforge_Repair_Self_Intersections import ys_repair_Self_Insec
from .ys_fontforge_tryfix import ys_closepath, ys_repair_si_chain, ys_rescale_chain, ys_simplify



# 横にずらして幅を広げる
def ys_widepaste(rwidth, rheight, glyph):

    # 元のグリフをバックアップ
    glyph_backup = [contour for contour in glyph.foreground]

    for i in range(rwidth)
        

    # ずらしたグリフを保存
    glyph.transform(psMat.translate(rwidth14, 0))
    glyph_tscopy1 = [contour for contour in glyph.foreground]
    glyph.transform(psMat.translate(rwidth14, 0))
    glyph_tscopy2 = [contour for contour in glyph.foreground]
    glyph.transform(psMat.translate(rwidth14, 0))
    glyph_tscopy3 = [contour for contour in glyph.foreground]
    glyph.transform(psMat.translate(rwidth14, 0))
    glyph_tscopy4 = [contour for contour in glyph.foreground]
    glyph.foreground = fontforge.layer()
    
    # 保存していたパスの書き戻し
    for contour in glyph_backup:
        glyph.foreground += contour

    # 長方形のサイズを定義
    rect_width = rwidth
    rect_height = rheight + rwidth / 2

    for contour in glyph.foreground:
        # コンターの方向をチェック（時計回りはスキップ）
        if contour.isClockwise():
            continue

        ymax = None
        ymin = None

        # ymaxとyminの値を初期化
        max_y = float('-inf')
        min_y = float('inf')

        # オンカーブポイントを探す
        for point in contour:
            if not point.on_curve:
                continue
            if point.y > max_y:
                max_y = point.y
                ymax = point
            if point.y < min_y:
                min_y = point.y
                ymin = point

        # ymaxのオンカーブポイントが存在する場合
        if ymax:
            # 左上を原点とする長方形を追加
            pen = glyph.glyphPen(replace=False)

            # ポイントを追加
            pen.moveTo(0, 0)
            pen.lineTo(rect_width, 0)
            pen.lineTo(rect_width, rect_height)
            pen.lineTo(0, rect_height)
            pen.closePath()
            pen = None
            glyph.changed = True

            # 新しく追加したコンターを取得
            rect_contour = glyph.foreground[-1]

            # 長方形を配置（移動）
            rect_contour.transform(psMat.translate( ymax.x, ymax.y - rect_height))
            print(f"\r now:{glyph.glyphname:<15} kaketa        \r", end=" ", flush=True)

        # yminのオンカーブポイントが存在する場合
        if ymin:
            # 左下を原点とする長方形を追加
            pen = glyph.glyphPen(replace=False)

            # ポイントを追加
            pen.moveTo(0, 0)
            pen.lineTo(rect_width, 0)
            pen.lineTo(rect_width, rect_height)
            pen.lineTo(0, rect_height)
            pen.closePath()
            pen = None
            glyph.changed = True

            # 新しく追加したコンターを取得
            rect_contour = glyph.foreground[-1]

            # 長方形を配置（移動）
            rect_contour.transform(psMat.translate( ymin.x, ymin.y))
            print(f"\r now:{glyph.glyphname:<15} kaketa        \r", end=" ", flush=True)


    # ずらしたグリフと合成
    for contour in glyph_tscopy1:
        glyph.foreground += contour
    for contour in glyph_tscopy2:
        glyph.foreground += contour
    for contour in glyph_tscopy3:
        glyph.foreground += contour
    for contour in glyph_tscopy4:
        glyph.foreground += contour

    glyph.round()  # 整数化
    glyph.removeOverlap()  # 結合

    # 右に広げた分だけ中心がズレるので左にずらす
    glyph.transform(psMat.translate( - rwidth12 , 0))

    # ゴミ掃除
    print(f"\r now:{glyph.glyphname:<15} Cleaning small pieces.         ", end=" ", flush=True)
    ys_rm_little_line(glyph)  # 合成時に発生した2点で構成されたパス(ゴミ)を削除
    ys_rm_small_poly(20, 20, glyph)  # 小さなゴミを削除
    glyph.addExtrema("all") # 極点を追加



# 幅ストロークを加える
def ys_widestroke(stroke_width, storoke_height, glyph):
    glyph_backup = [contour for contour in glyph.foreground]

    #全てのストロークが反時計回りの場合フラグ立て
    is_all_ccw = True
    for contour in glyph.foreground:  # 各パス（輪郭）をループ
        if contour.isClockwise():
            is_all_ccw = False
            break  # 1つでも時計回りなら確認を終了

    glyph.stroke("elliptical", stroke_width, storoke_height, 0, "round", "miterclip",
        # "circular", width[, CAP, JOIN, ANGLE, KEYWORD],
        # "elliptical", width, minor_width[, ANGLE, CAP, JOIN, KEYWORD],
        # "calligraphic", width, height[, ANGLE, CAP, JOIN, KEYWORD],
        # "convex", contour[, ANGLE, CAP, JOIN, KEYWORD],
        removeinternal=False,  # Default=False (太らせ処理)
        removeexternal=False,  # Default=False (細らせ処理)
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

    # 自己交差の修復試行。直らなくても2度のツノは折る。
    ys_repair_si_chain(glyph)

    # 元のグリフと合成
    ys_rm_small_poly(20, 20, glyph) # 小さなゴミを除去
    for contour in glyph_backup:  # 保存していたパスの書き戻し
        glyph.foreground += contour
    if is_all_ccw:  # 元々通常パス(CCW)しか無いグリフの場合
        for contour in glyph.foreground:
            if contour.isClockwise():  # 反転パス(CW)の場合
                contour.reverseDirection()  # パスを反転させる
    glyph.removeOverlap()  # 結合

    ys_repair_si_chain(glyph) # 結合後の修復試行

    # ゴミ掃除
    print(f"\r now:{glyph.glyphname:<15} Cleaning small pieces.         ", end=" ", flush=True)
    ys_rm_little_line(glyph)  # 2点で構成されたパス(ゴミ)を削除
    ys_rm_small_poly(20, 20, glyph)  # 小さなゴミを削除
    glyph.addExtrema("all") # 極点を追加



if __name__ == "__main__":
    main()
