#!fontforge --lang=py -script

import fontforge
import psMat
import math

from .ys_fontforge_Remove_artifacts import ys_closepath, ys_rm_spikecontours, ys_rm_isolatepath, ys_rm_small_poly
from .ys_fontforge_Repair_Self_Intersections import ys_repair_Self_Insec
from .ys_fontforge_tryfix import  ys_repair_si_chain, ys_rescale_chain, ys_simplify

# 幅ストロークを加える
def ys_widestroke(glyph, stroke_width, storoke_height, vshrink_ratio, counter=1):
    #全てのストロークが反時計回りの場合フラグ立て
    is_all_ccw = True
    for contour in glyph.foreground:  # 各パス（輪郭）をループ
        if contour.isClockwise():
            is_all_ccw = False
            break

    # グリフのバックアップを取得
    glyph_backup = [contour.dup() for contour in glyph.foreground]

    # 濁点グリフなら右の濁点をずらす。
    if ys_dakutenlist(glyph):
        ys_dakuten_move(glyph, stroke_width / vshrink_ratio, -100)

    # 白抜きカッコは白抜きの大きさを確保し、削った分だけストローク幅を増やす。
    if ys_cwhogolist(glyph):
        stroke_width = stroke_width * 2
        ys_cwhogo_expantion(glyph, stroke_width)

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
    # 変化が無くなるまで繰り返す。
    stroke_prev = [contour.dup() for contour in glyph.foreground]
    ys_repair_Self_Insec(glyph, 3)
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    stroke_aftr = [contour.dup() for contour in glyph.foreground]
    if stroke_prev != stroke_aftr:
        stroke_prev = [contour.dup() for contour in glyph.foreground]
        ys_repair_Self_Insec(glyph, 3)
        ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
        stroke_aftr = [contour.dup() for contour in glyph.foreground]
        if stroke_prev != stroke_aftr:
            stroke_prev = [contour.dup() for contour in glyph.foreground]
            ys_repair_Self_Insec(glyph, 3)
            ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
            stroke_aftr = [contour.dup() for contour in glyph.foreground]
            if stroke_prev != stroke_aftr:
                stroke_prev = [contour.dup() for contour in glyph.foreground]
                ys_repair_Self_Insec(glyph, 3)
                ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
                stroke_aftr = [contour.dup() for contour in glyph.foreground]
                if stroke_prev != stroke_aftr:
                    ys_repair_Self_Insec(glyph, 3)
                    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)

    # 修復チェインの繰り返し実行。変化がなくなるか悪化するまで繰り返し。
    ys_anomality_repair(glyph, counter)

    # 元のグリフと合成
    for contour in glyph_backup:  # 保存していたパスの書き戻し
        glyph.foreground += contour
    if is_all_ccw:  # 元々通常パス(CCW)しか無いグリフの場合
        for contour in glyph.foreground:
            if contour.isClockwise():  # 反転パス(CW)の場合
                contour.reverseDirection()  # パスを反転させる
    glyph.removeOverlap()  # 結合

    # 修復チェインの繰り返し実行。変化がなくなるか悪化するまで繰り返し。
    ys_anomality_repair(glyph, counter)
    return



# 修復チェインの繰り返し実行。変化がなくなるか悪化するなら終了。
def ys_anomality_repair(glyph, counter):
    if (glyph.validate(1) & 0x0FF) != 0 and (glyph.validate(1) & 0x0FF) != 0x04:
        previous_flags = glyph.validate(1) & 0x0FF
        ys_repair_si_chain(glyph, counter)
        current_flags = glyph.validate(1) & 0x0FF
        if (previous_flags & ~current_flags) != 0 and current_flags != 0:
            previous_flags = glyph.validate(1) & 0x0FF
            ys_repair_si_chain(glyph, counter)
            current_flags = glyph.validate(1) & 0x0FF
            if (previous_flags & ~current_flags) != 0 and current_flags != 0:
                previous_flags = glyph.validate(1) & 0x0FF
                ys_repair_si_chain(glyph, counter)
                current_flags = glyph.validate(1) & 0x0FF
                if (previous_flags & ~current_flags) != 0 and current_flags != 0:
                    previous_flags = glyph.validate(1) & 0x0FF
                    ys_repair_si_chain(glyph, counter)
                    current_flags = glyph.validate(1) & 0x0FF
                    if (previous_flags & ~current_flags) != 0 and current_flags != 0:
                        ys_repair_si_chain(glyph, counter)
    return



# 空隙を絶対に残さないと字形が崩れるグリフのリスト。
# 空隙を増やした分だけ大きく太らせることになるので、
# ここに入れて良い条件は結構限られる。
# グリフを渡したら対象かどうか判定して返す。
def ys_cwhogolist(glyph):
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
    }
    # グリフ名がリストにあるかチェック
    if glyph.glyphname in cwhogolist_set:
        return True
    else:
        return False

# 時計回りのコンターを、拡大幅で削られる分だけ
# 各コンターの中心から拡大する。
def ys_cwhogo_expantion(glyph, stroke_width):
    for contour in glyph.foreground:
        # 時計回りのコンターのみ処理
        if contour.isClockwise():
            # コンターの境界ボックスを取得
            bbox = contour.boundingBox()
            x_min, y_min, x_max, y_max = bbox
            # コンターの幅を計算
            width = x_max - x_min
            # 拡大率を計算
            if width == 0:
                continue  # 幅が0の場合スキップ
            scale_factor = (width + stroke_width) / width
            # コンターの中心を計算
            center_x = (x_min + x_max) / 2
            center_y = (y_min + y_max) / 2
            # コンターを原点に移動
            contour.transform(psMat.translate(-center_x, -center_y))
            # コンターを拡大
            contour.transform(psMat.scale(scale_factor, scale_factor))
            # 元の位置に戻す
            contour.transform(psMat.translate(center_x, center_y))
    return
"""
この辺の計算がワケ分からん。
とりあえずは左側だけで考えて見る。
幅2のストロークはパス内部に食われてしまうので、
方向違いのパスで往復しても両側で2しか増えない。
さらに上の関数のこの処理を加えると、
あらかじめ1削られているので1しか増えない。
じゃあその分を埋め合わせするために幅1.5にすると、
今度は広げた幅以上に食ってしまう。

ではストローク幅を4にする
あらかじめ2削られるけどそのかわり4増えるから、
最初の狙いどおり、元の太さに2を足した太さにできる。

この辺の釣り合いの取り方はなんかの数式で表現出来るんだろうけど、
今そういうトコまで頭まわらない。
どうやら、ぼくの頭は算数で止まっていると思われる。
まぁ、わけがわからなくても結果が得られるなら、という納得で茶を濁す。
"""



# 濁点を移動させたい対象グリフの一覧。
# グリフを渡したら対象かどうか判定して返す。
def ys_dakutenlist(glyph):
    dakutenlist_set = {
        "uni0022",  # "
        "uni00A8",  # ¨
        "uni00AB",  # «
        "uni00BB",  # »
        "uni02DD",  # ˝
        "uni0308",  # ̈
        "uni030B",  # ̋
        "uni030F",  # ̏
        "uni201C",  # “
        "uni201D",  # "
        "uni201E",  # „
        "uni2033",  # ″
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
        contour_to_move = glyph.foreground[rightmost_contour_index]
        contour_to_move.transform(psMat.translate(move_width, 0))
    return

if __name__ == "__main__":
    main()
