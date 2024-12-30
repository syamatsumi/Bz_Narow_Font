#!fontforge --lang=py -script

import fontforge
import math

# 開いたパスを閉じるだけの関数。
def ys_closepath(glyph):
    close_paths = []
    open_paths = []
    # 無事なパスと問題のあるパスの選り分け
    for contour in glyph.foreground:
        if contour.closed:
            close_paths.append(contour.dup())
        else:
            open_paths.append(contour.dup())

    # 空いたパスの処置
    for contour in open_paths:
        # 繋いでもゴミにしかならない直線のみのパスは無視。
        if len(contour) > 2:
            start_point = contour[0]
            end_point = contour[-1]
            # 始点と終点が異なる位置にある場合は線を追加。
            if start_point.x != end_point.x or start_point.y != end_point.y:
                contour.lineTo(start_point.x, start_point.y)
            # コンターを閉じる
            contour.closed = True
            close_paths.append(contour.dup())

    # フォアグラウンドをクリアして、OKパス変数に入れてたコンターを書き戻す
    glyph.foreground = fontforge.layer()
    for contour in close_paths:
        glyph.foreground += contour
    return



# 面積を簡易的に計算する関数
# 当初はオンカーブポイントだけ計測してたけど、よく考えたら周長に関しては
# 全てのポイントを線分近似させた方がより正確なので変更。
def contour_area_and_points(contour):
    try:
        on_pts = []
        for i in range(len(contour)):
            if contour[i].on_curve:
                on_pts.append(contour[i])
        if len(on_pts) < 3:
            return 0.0, len(on_pts)
        x = [p.x for p in on_pts]
        y = [p.y for p in on_pts]
        area = 0.0
        for i in range(len(on_pts)):
            j = (i + 1) % len(on_pts)
            area += x[i]*y[j] - y[i]*x[j]
    except AttributeError as e:  # 属性の問題がある場合
        print(f"AttributeError: {e}")
        return 0.0, 0
    except Exception as e:  # それ以外の予期せぬエラー
        print(f"Unexpected error: {e}")
        return 0.0, 0
    return abs(area)*0.5, len(on_pts)

# コンターの周長を簡易的に計算する関数
def contour_length_and_points(contour):
    try:
        all_pts = []
        for i in range(len(contour)):
            all_pts.append(contour[i])
        length = 0.0
        for i in range(len(all_pts)):
            j = (i + 1) % len(all_pts)
            dx = all_pts[j].x - all_pts[i].x
            dy = all_pts[j].y - all_pts[i].y
            length += math.sqrt(dx*dx + dy*dy)
    except AttributeError as e:  # 属性の問題がある場合
        print(f"AttributeError: {e}")
        return 0.0, 0
    except Exception as e:  # それ以外の予期せぬエラー
        print(f"Unexpected error: {e}")
        return 0.0, 0
    return length, len(all_pts)

# 周長に対して極端に面積の小さなコンターを削除する関数
def ys_rm_spikecontours(glyph, c_thresh=0.1, g_thresh=0.001, p_thresh=10):
    ok_paths = []  # 有効なパスを保存するリスト
    # グリフ全体の面積を取得
    gbbox = glyph.boundingBox()
    gxmin, gymin, gxmax, gymax = gbbox
    gmax_area = (gxmax - gxmin) * (gymax - gymin)

    if glyph.validate(1) & 0x01:  # 空いたパスが存在する場合
        ys_closepath(glyph)  # 空いたパスを強制的に閉じる関数

    for contour in glyph.foreground:
        length, points = contour_length_and_points(contour)
        # 長さがないなら面積比も0で確定。
        if length == 0:
            c_ratio = 0.0
            g_ratio = 0.0

        # 入り組んだコンター（＊など）は、外周長に対する面積が
        # 極端に低く出るため、頂点数が多く、かつコンターの外周長が
        # BBOXの外周長を超える場合のみ、BBOXの面積と比較する。
        else:
            if points > p_thresh:  # 点の数が多い時
                cbbox = contour.boundingBox()
                cxmin, cymin, cxmax, cymax = cbbox
                bbox_pe = 2 * ((cxmax - cxmin) + (cymax - cymin))

                # BBOXの周長より長いときはBBOXの面積が比較対象
                if length > bbox_pe:
                    cmax_area = (cxmax - cxmin) * (cymax - cymin)
                else:
                    cmax_area = (length/4)**2
            else:  # 上記のどちらの条件にも当てはまらない場合は外周長基準。
                cmax_area = (length/4)**2

            # コンターの概算面積を求めてcmax_areaと比較する。
            area, _ = contour_area_and_points(contour)
            c_ratio = area/cmax_area if cmax_area > 0 else 0.0
            # 全体に比しての面積比も比較する。
            g_ratio = area/gmax_area if gmax_area > 0 else 0.0

        # どちらかの基準より面積比が大きければOK
        if c_ratio > c_thresh or g_ratio > g_thresh:
            ok_paths.append(contour.dup())  # 合格パスに追加

    # フォアグラウンドをクリアして、OKパス変数に入れてたコンターを書き戻す
    glyph.foreground = fontforge.layer()
    for contour in ok_paths:
        glyph.foreground += contour
    return



# オンカーブ点のノード数が2より多い(つまり3以上)のパスをok_pathsに保存。
# 2点間の距離が一定数以上あるなら、カマボコ状の形を作ってる可能性がある。
# 問答無用で削除する場合はmin_distanceをクソデカに設定すること。
# 何故かメイン関数に入れるとグリフが消える問題、たぶん参照渡しが原因。
# おそらくこれで解決したハズ……
def ys_rm_isolatepath(glyph, min_distance=20):
    ok_paths = []  # 有効なパスを保存するリスト
    for contour in glyph.foreground:
        # オンクルーブポイントを抽出
        on_curve_points = [point for point in contour if point.on_curve]

        # オンクルーブポイントが2点の場合に距離を計算
        if len(on_curve_points) == 2:
            distance = math.sqrt(
                (on_curve_points[0].x - on_curve_points[1].x)**2
                +(on_curve_points[0].y - on_curve_points[1].y)**2
                )
            if distance > min_distance:
                ok_paths.append(contour.dup())  # 距離が長ければOK
        elif len(on_curve_points) > 2:
            # オンクルーブポイントが3点以上の場合は無条件でOK
            ok_paths.append(contour.dup())

    # フォアグラウンドをクリアして、OKパス変数に入れてたコンターを書き戻す
    glyph.foreground = fontforge.layer()
    for contour in ok_paths:
        glyph.foreground += contour
    return



# バウンディングボックスで判定して、
# しきい値以下のオブジェクトは削除する。
def ys_rm_small_poly(glyph, width_threshold, height_threshold):
    ng_paths = []  # 空リストを初期化
    for contour in glyph.foreground:  # 各パス（輪郭）をループ
        contour.addExtrema("all")
        bbox = contour.boundingBox()
        xmin, ymin, xmax, ymax = bbox
        width = xmax - xmin
        height = ymax - ymin
        if width <= width_threshold and height <= height_threshold:  # 条件をチェック
            ng_paths.append(contour.dup())  # 条件を満たすものをリストに追加
    # 問題のないパス(さっき保存できてないコンター)をOK変数にブチ込む
    ok_paths = [contour.dup() for contour in glyph.foreground if contour not in ng_paths]

    # フォアグラウンドをクリアして、OKパス変数に入れてたコンターを書き戻す
    glyph.foreground = fontforge.layer()
    for contour in ok_paths:
        glyph.foreground += contour
    return



if __name__ == "__main__":
    ys_rm_littleline(glyph, 20)