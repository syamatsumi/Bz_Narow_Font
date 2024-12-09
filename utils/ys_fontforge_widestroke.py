#!fontforge --lang=py -script

import fontforge
import psMat
import math

from .ys_fontforge_Remove_artifacts import ys_closepath, ys_rm_spikecontours, ys_rm_little_line, ys_rm_small_poly
from .ys_fontforge_Repair_Self_Intersections import ys_repair_Self_Insec
from .ys_fontforge_tryfix import  ys_repair_si_chain, ys_rescale_chain, ys_simplify

# 幅ストロークを加える
def ys_widestroke(glyph, stroke_width, storoke_height, counter=1):
    glyph_backup = [contour.dup() for contour in glyph.foreground]
    #全てのストロークが反時計回りの場合フラグ立て
    is_all_ccw = True
    for contour in glyph.foreground:  # 各パス（輪郭）をループ
        if contour.isClockwise():
            is_all_ccw = False
            break  # 1つでも時計回りなら確認を終了

    glyph.stroke("calligraphic", stroke_width, storoke_height, 0, "round", "miterclip",
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

    # スパイク状の独立したコンターを削除する。
    ys_rm_spikecontours(glyph, 0.01, 10)
    # 自己交差の修復試行。直らなくても2度のツノは折る。
    ys_repair_si_chain(glyph, counter)
    ys_rm_little_line(glyph)  # 2点で構成されたパス(ゴミ)を削除
    ys_rm_small_poly(glyph, 20, 20)  # 小さなゴミを削除

    # 元のグリフと合成
    for contour in glyph_backup:  # 保存していたパスの書き戻し
        glyph.foreground += contour
    if is_all_ccw:  # 元々通常パス(CCW)しか無いグリフの場合
        for contour in glyph.foreground:
            if contour.isClockwise():  # 反転パス(CW)の場合
                contour.reverseDirection()  # パスを反転させる
    glyph.removeOverlap()  # 結合

    ys_repair_si_chain(glyph, counter) # 結合後の修復試行

    # ゴミ掃除
    print(f"\r now:{glyph.glyphname:<15} Cleaning small pieces.         ", end=" ", flush=True)
    ys_rm_spikecontours(glyph, 0.01, 10)
    ys_rm_little_line(glyph)  # 2点で構成されたパス(ゴミ)を削除
    ys_rm_small_poly(glyph, 20, 20)  # 小さなゴミを削除
    glyph.addExtrema("all") # 極点を追加



if __name__ == "__main__":
    main()
