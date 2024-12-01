#!fontforge --lang=py -script

import fontforge

from .ys_fontforge_Repair_Self_Intersections import ys_repair_Self_Insec
from .ys_fontforge_Remove_artifacts import ys_rm_small_poly
from .ys_fontforge_Remove_artifacts import ys_rm_little_line
from .ys_fontforge_Remove_artifacts import ys_rm_small_poly
from .ys_fontforge_tryfix import ys_closepath
from .ys_fontforge_tryfix import ys_simplify
from .ys_fontforge_tryfix import ys_rescale_chain

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

    # 元のグリフと合成
    if glyph.validate(1) & 0x01:  # 開いたパスを検出
        ys_closepath(glyph)  # パスを閉じる＆その他処理
    ys_rm_little_line(glyph)  # 2点で構成されたパス(ゴミ)を削除
    ys_repair_Self_Insec(glyph, 1)  # 1度以下の角度の点を移動
    if glyph.validate(1) & 0x20:  # まだ自己交差がある
        ys_repair_Self_Insec(glyph, 2)  # 2度以下の角度の奴を潰す。
        if glyph.validate(1) & 0x20:
            ys_repair_Self_Insec(glyph, 3)
            if glyph.validate(1) & 0x20:
                ys_repair_Self_Insec(glyph, 4)
                if glyph.validate(1) & 0x20:
                    ys_repair_Self_Insec(glyph, 5)
                    if glyph.validate(1) & 0x20:
                        ys_repair_Self_Insec(glyph, 6)

    ys_rm_small_poly(20, 20, glyph) # 小さなゴミを除去
    for contour in glyph_backup:  # 保存していたパスの書き戻し
        glyph.foreground += contour
    if is_all_ccw:  # 元々通常パス(CCW)しか無いグリフの場合
        for contour in glyph.foreground:
            if contour.isClockwise():  # 反転パス(CW)の場合
                contour.reverseDirection()  # パスを反転させる
    glyph.removeOverlap()  # 結合

    # 修復試行
    if glyph.validate(1) & 0x01:
        ys_closepath(glyph)
    if glyph.validate(1) & 0x20:
        ys_repair_Self_Insec(glyph, 1) 
        if glyph.validate(1) & 0x20:
            ys_repair_Self_Insec(glyph, 2)
            if glyph.validate(1) & 0x20:
                ys_repair_Self_Insec(glyph, 3)
                if glyph.validate(1) & 0x20:
                    ys_repair_Self_Insec(glyph, 4)
                    if glyph.validate(1) & 0x20:
                        ys_repair_Self_Insec(glyph, 5)
                        if glyph.validate(1) & 0x20:
                            ys_repair_Self_Insec(glyph, 6)
        glyph.removeOverlap()  # 結合

    # ゴミ掃除
    ys_rm_little_line(glyph)  # 2点で構成されたパス(ゴミ)を削除
    ys_rm_small_poly(20, 20, glyph)
    glyph.addExtrema("all") # 極点を追加



if __name__ == "__main__":
    main()
