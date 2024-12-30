#!fontforge --lang=py -script

import fontforge
import psMat
import math

from .ys_fontforge_Remove_artifacts import ys_closepath, ys_rm_spikecontours, ys_rm_isolatepath, ys_rm_small_poly
from .ys_fontforge_Repair_spikes import ys_repair_spikes
from .ys_fontforge_tryfix import  ys_repair_si_chain, ys_rescale_chain, ys_simplify

# 幅ストロークを加える
def ys_widestroke(glyph, stroke_width, storoke_height, vshrink_ratio, counter=1):
    # 濁点グリフなら右の濁点をずらす。
    if ys_dakutenlist(glyph):
        move_width = stroke_width
        ys_dakuten_move(glyph, move_width, -1000)

    # ストロークの方向性に関わる処理(兼バックアップ)
    cw_paths = []
    ccw_paths = []
    for contour in glyph.foreground:
        if contour.isClockwise():
            cw_paths.append(contour.dup())
        else:
            is_all_cw = False
            ccw_paths.append(contour.dup())
    # 全部CWだった場合用フラグ
    is_all_cw = ccw_paths == []

    # 特定のグリフは反時計回りのコンターを削除する
    if ys_ccwhogolist(glyph):
        # 内側ストロークが無いぶんストローク幅を増やす
        stroke_width = stroke_width * 2
        # レイヤを消去して時計回りのパスだけ書き戻す
        glyph.foreground = fontforge.layer()
        for contour in cw_paths:
            glyph.foreground += contour

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

    # ストロークで発生したノイズを除去する。
    # 本来のベクトルと水平・垂直の方向に発生したポイントのズレによって、
    # 所により線が行ったり来たりの繰り返しになって極端な鋭角の繰り返しが発生する。
    # この作業はアーティファクトの除去が目的というより、
    # 後にアーティファクトが発生するのを予防するためのもの。
    ys_closepath(glyph)
    ys_repair_spikes(glyph, 0.5)
    glyph.round()
    glyph.addExtrema("all")
    glyph.removeOverlap()
    # ゴミ掃除
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    ys_rm_isolatepath(glyph)
    ys_rm_small_poly(glyph, 20, 30)

    # 元の時計回りパスの書き戻し
    for contour in cw_paths:
        glyph.foreground += contour

    # 元々通常パス(CW)しか無いグリフの場合
    if is_all_cw:
        for contour in glyph.foreground:
            if not contour.isClockwise():  # 反転パス(CCW)の場合
                contour.reverseDirection()  # パスを反転させる
    else:
        # 反時計回りパスの書き戻し
        for contour in ccw_paths:
            glyph.foreground += contour

    glyph.round()
    glyph.addExtrema("all")
    glyph.removeOverlap()  # 結合
    glyph.addExtrema("all")

    return



# 空隙を絶対に残さないと字形が崩れるグリフのリスト。
# 空隙を増やした分だけ大きく太らせることになるので、
# ここに入れて良い条件は結構限られる。
# グリフを渡したら対象かどうか判定して返す。
def ys_ccwhogolist(glyph):
    cwhogolist_set = {
        "uni300E",  # 『
        "uni300F",  # 』
        "uni3016",  # 〖
        "uni3017",  # 〗
        "uni3018",  # 〘
        "uni3019",  # 〙
        "uni300E.vert",  # 『
        "uni300F.vert",  # 』
        "uni300E.hwid",  # 『
        "uni300F.hwid",  # 』
        "uniFE46",  # ﹆
    }
    # グリフ名がリストにあるかチェック
    if glyph.glyphname in cwhogolist_set:
        return True
    else:
        return False



# 濁点を移動させたい対象グリフの一覧。
# グリフを渡したら対象かどうか判定して返す。
def ys_dakutenlist(glyph):
    dakutenlist_set = {
    "quotedbl",  # "
    "dieresis",  # ¨
    "guillemotleft",  # «
    "guillemotright",  # »
    "hungarumlaut",  # ˝
    "uni0308",  # ̈
    "uni030B",  # ̋
    "uni030F",  # ̏
    "quotedblleft",  # “
    "quotedblright",  # "
    "quotedblbase",  # „
    "second",  # ″
    "uni226A",  # ≪
    "uni226B",  # ≫
    "uni3003",  # 〃
    "uni300A",  # 《
    "uni300B",  # 》
    "uni3034",  # 〴
    "uni304C",  # が
    "uni304E",  # ぎ
    "uni3050",  # ぐ
    "uni3052",  # げ
    "uni3054",  # ご
    "uni3056",  # ざ
    "uni3058",  # じ
    "uni305A",  # ず
    "uni305C",  # ぜ
    "uni305E",  # ぞ
    "uni3060",  # だ
    "uni3062",  # ぢ
    "uni3065",  # づ
    "uni3067",  # で
    "uni3069",  # ど
    "uni3070",  # ば
    "uni3073",  # び
    "uni3076",  # ぶ
    "uni3079",  # べ
    "uni307C",  # ぼ
    "uni3094",  # ゔ
    "uni3099",  # ゙
    "uni309B",  # ﾞ
    "uni309E",  # ゞ
    "uni30AC",  # ｶﾞ
    "uni30AE",  # ｷﾞ
    "uni30B0",  # ｸﾞ
    "uni30B2",  # ｹﾞ
    "uni30B4",  # ｺﾞ
    "uni30B6",  # ｻﾞ
    "uni30B8",  # ｼﾞ
    "uni30BA",  # ｽﾞ
    "uni30BC",  # ｾﾞ
    "uni30BE",  # ｿﾞ
    "uni30C0",  # ﾀﾞ
    "uni30C2",  # ﾁﾞ
    "uni30C5",  # ﾂﾞ
    "uni30C7",  # ﾃﾞ
    "uni30C9",  # ﾄﾞ
    "uni30D0",  # ﾊﾞ
    "uni30D3",  # ﾋﾞ
    "uni30D6",  # ﾌﾞ
    "uni30D9",  # ﾍﾞ
    "uni30DC",  # ﾎﾞ
    "uni30F4",  # ヴ
    "uni30F7",  # ヷ
    "uni30F8",  # ヸ
    "uni30F9",  # ヹ
    "uni30FA",  # ヺ
    "uni30FE",  # ヾ
    "uni30FC",  # ｰ
    "uni30FD",  # ヽ
    "uni30FE",  # ヾ
    "uni30FF",  # ヿ
    "uni3100",  # ㄀
    "uni3101",  # ㄁
    "uni3102",  # ㄂
    "uni3103",  # ㄃
    "uni3104",  # ㄄
    "uniFF02",  # "
    "uniFF9E",  # ﾞ
    "uni301D.vert",  # 〝
    "uni301F.vert",  # 〟
    "uni309B.vert",  # ﾞ
    "uni309E.vert",  # ゞ
    "uni30FE.vert",  # ヾ
    "quotedblright.hwid",  #
    "uni30F4.aalt",  # ヴ
    "uni30AC.aalt",  # ｶﾞ
    "uni30AE.aalt",  # ｷﾞ
    "uni30B0.aalt",  # ｸﾞ
    "uni30B2.aalt",  # ｹﾞ
    "uni30B4.aalt",  # ｺﾞ
    "uni30B6.aalt",  # ｻﾞ
    "uni30B8.aalt",  # ｼﾞ
    "uni30BA.aalt",  # ｽﾞ
    "uni30BC.aalt",  # ｾﾞ
    "uni30BE.aalt",  # ｿﾞ
    "uni30C0.aalt",  # ﾀﾞ
    "uni30C2.aalt",  # ﾁﾞ
    "uni30C5.aalt",  # ﾂﾞ
    "uni30C7.aalt",  # ﾃﾞ
    "uni30C9.aalt",  # ﾄﾞ
    "uni30D0.aalt",  # ﾊﾞ
    "uni30D3.aalt",  # ﾋﾞ
    "uni30D6.aalt",  # ﾌﾞ
    "uni30D9.aalt",  # ﾍﾞ
    "uni30DC.aalt",  # ﾎﾞ
    "uni304C.aalt",  # が
    "uni304E.aalt",  # ぎ
    "uni3050.aalt",  # ぐ
    "uni3052.aalt",  # げ
    "uni3054.aalt",  # ご
    "uni3056.aalt",  # ざ
    "uni3058.aalt",  # じ
    "uni305A.aalt",  # ず
    "uni305C.aalt",  # ぜ
    "uni305E.aalt",  # ぞ
    "uni3060.aalt",  # だ
    "uni3062.aalt",  # ぢ
    "uni3065.aalt",  # づ
    "uni3067.aalt",  # で
    "uni3069.aalt",  # ど
    "uni3070.aalt",  # ば
    "uni3073.aalt",  # び
    "uni3076.aalt",  # ぶ
    "uni3079.aalt",  # べ
    "uni307C.aalt",  # ぼ
    "uni5FC4"  # 忄
    }
    # グリフ名がリストにあるかチェック
    if glyph.glyphname in dakutenlist_set:
        return True
    else:
        return False

# 指定したグリフオブジェクトの一番右にあるコンターを右に移動させる。
# thresholdを指定しておくとthresholdより下にyminのあるコンターは移動させない。
# 一番右側にあるコンターが濁点以外のとき対策。今は利用予定なし。
def ys_dakuten_move(glyph, move_width, threshold=-1000):
    # コンターの数を確認し、1つだけの場合は何もしない
    if len(glyph.foreground) <= 1:
        return

    # 各パスのBoundingBoxを取得し、左下の始点が最も右にあるコンターを特定する
    rightmost_contour_index = None
    max_xmin = None
    max_ymin = None

    for i, contour in enumerate(glyph.foreground):
        xmin, ymin, xmax, ymax = contour.boundingBox()

        # xminの最大値を判定
        if max_xmin is None or xmin > max_xmin:
            max_xmin = xmin
            max_ymin = ymin
            rightmost_contour_index = i

    # 特定した一番右のコンターのyminがしきい値以上である場合にのみ移動
    if rightmost_contour_index is not None and max_ymin >= threshold:
        proc_paths = []
        for i, contour in enumerate(glyph.foreground):
            if i == rightmost_contour_index:
                contour.transform(psMat.translate(move_width, 0))
            proc_paths.append(contour.dup())
        # レイヤを消去して加工したパスを書き戻す
        glyph.foreground = fontforge.layer()
        for contour in proc_paths:
            glyph.foreground += contour
    return

if __name__ == "__main__":
    main()
