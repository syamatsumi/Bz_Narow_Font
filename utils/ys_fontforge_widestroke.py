#!fontforge --lang=py -script

import fontforge
import psMat
import math

from .ys_fontforge_Remove_artifacts import ys_rm_little_line, ys_rm_small_poly
from .ys_fontforge_Repair_Self_Intersections import ys_repair_Self_Insec
from .ys_fontforge_tryfix import ys_closepath, ys_repair_si_chain, ys_rescale_chain, ys_simplify



# ベクトルが上方向にあるパスを右にオフセットする
def ys_expand_Xweight(glyph, offset):
    # 0除算回避のため整数化、重複削除を実施
    glyph.round()
    glyph.removeOverlap()

    # 作業面を保存してレイヤをカラに
    glyph_backup = [contour.dup() for contour in glyph.foreground]
    glyph.foreground = fontforge.layer()

    # コンターを加工して吐き出す。
    wroking_contour = fontforge.contour(True)
    contour_processe = []
    for contour in glyph_backup:
        working_contour = contour.dup()
        # ベクトルの向きが変わる箇所に点を追加
        ys_insert_point_on_turn(working_contour)
        glyph.foreground += working_contour
        # 上向きのベクトル(CCWパスの右側)をオフセット処理
        # ys_upper_vector_offsetter(working_contour, offset)
        # 処理が済んだパスを保存。
        # contour_processe += working_contour
        
    return



# 上下方向ベクトルの向きが変わる箇所に点を追加
def ys_insert_point_on_turn(contour):
    new_contour = fontforge.contour(True)
    current_point = fontforge.contour(True)
    num_points = len(contour)

    # 全てのポイントのインデックスを取得
    point_indices = list(range(num_points))
    i = 0
    while i < num_points:
        idx = i
        current_point = contour[idx]

        # ポイントの属性を取得
        # 'move', 'line', 'curve', 'qcurve', 'offcurve'など
        point_type = current_point.type

        # オフカーブポイントは保存だけして次へ
        if point_type == 'offcurve':
            new_contour += current_point.dup()
            i += 1
            continue

        # 前後のポイントを取得（オフカーブポイントをスキップ）
        prev_idx = (idx - 1) % num_points
        while contour[prev_idx].type == 'offcurve':
            prev_idx = (prev_idx - 1) % num_points
            if prev_idx == idx:
                break  # 無限ループ防止

        next_idx = (idx + 1) % num_points
        while contour[next_idx].type == 'offcurve':
            next_idx = (next_idx + 1) % num_points
            if next_idx == idx:
                break  # 無限ループ防止

        prev_point = contour[prev_idx]
        next_point = contour[next_idx]

        # ベクトルを計算
        vector1 = (
            current_point.x - prev_point.x,
            current_point.y - prev_point.y,
        )
        vector2 = (
            next_point.x - current_point.x,
            next_point.y - current_point.y,
        )
        # 折り返し、折れ曲がりがあるポイント
        if is_direction_changed(vector1, vector2):
            new_contour += current_point.dup()
            new_contour += current_point.dup()

        else:
            # 通常の点として1回取得
            new_contour += current_point.dup()
        i += 1  # 次のポイントへ進む

    # コンターを閉じる処理、最初と最後のポイントが異なる場合
    if new_contour[0] != new_contour[-1]:
        # 最初の点をコピーして末尾に追加することで実質クローズ。
        new_contour += new_contour[0].dup()

    contour = new_contour

    return 



# ベクトルのY方向が変化したかどうかを判定
def is_direction_changed(vector1, vector2):
    # 通常の反転は単純に正負の掛け算では必ず負になる性質を利用。
    # 水平線から斜線、斜線から水平線の時も拾いたいので、
    # どちらかが水平線で0の時(=乗算で0になる)
    # かつ、足し算して0じゃないなら向きの変更と見做します。
    y1, y2 = vector1[1], vector2[1]
    return (y1 * y2 < 0) or (y1 * y2 == 0 and y1 + y2 != 0)



def ys_upper_vector_offsetter(contour, offset):
    points_target = []  # 動かす対象ポイントの格納場所
    num_points = len(contour)
    point_indices = list(range(num_points))  # インデックス取得

    i = 0
    while i < num_points:
        idx = i
        current_point = contour[idx]
        point_type = current_point.type  # ポイントの属性を取得

        # 前後のポイントを取得（オフカーブポイントをスキップ）
        prev_idx = (idx - 1) % num_points
        while contour[prev_idx].type == 'offcurve':
            prev_idx = (prev_idx - 1) % num_points
            if prev_idx == idx:
                break  # 無限ループ防止

        next_idx = (idx + 1) % num_points
        while contour[next_idx].type == 'offcurve':
            next_idx = (next_idx + 1) % num_points
            if next_idx == idx:
                break  # 無限ループ防止

        prev_point = contour[prev_idx]
        next_point = contour[next_idx]

        # ベクトルを計算
        vector1 = (
            current_point.x - prev_point.x,
            current_point.y - prev_point.y,
        )
        vector2 = (
            next_point.x - current_point.x,
            next_point.y - current_point.y,
        )

        # yが増加するか、してたポイントは全て対象。
        # このあと操作する対象をピックアップする処理なので、
        # ここは敢えての参照渡し。
        if vector1[1] > 0 or vector2[1] > 0:
            points_target.append(current_point)

        i += 1  # 次のポイントへ進む

    # 動かす対象のポイントをオフセット
    for point in points_target:
        point.x += offset  # X軸方向に移動

    return






# 幅ストロークを加える
def ys_widestroke(glyph, stroke_width, storoke_height):
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

    # 自己交差の修復試行。直らなくても2度のツノは折る。
    ys_repair_si_chain(glyph, 777)

    # 元のグリフと合成
    ys_rm_small_poly(glyph, 20, 20) # 小さなゴミを除去
    for contour in glyph_backup:  # 保存していたパスの書き戻し
        glyph.foreground += contour
    if is_all_ccw:  # 元々通常パス(CCW)しか無いグリフの場合
        for contour in glyph.foreground:
            if contour.isClockwise():  # 反転パス(CW)の場合
                contour.reverseDirection()  # パスを反転させる
    glyph.removeOverlap()  # 結合

    ys_repair_si_chain(glyph, 777) # 結合後の修復試行

    # ゴミ掃除
    print(f"\r now:{glyph.glyphname:<15} Cleaning small pieces.         ", end=" ", flush=True)
    ys_rm_little_line(glyph)  # 2点で構成されたパス(ゴミ)を削除
    ys_rm_small_poly(glyph, 20, 20)  # 小さなゴミを削除
    glyph.addExtrema("all") # 極点を追加



if __name__ == "__main__":
    main()
