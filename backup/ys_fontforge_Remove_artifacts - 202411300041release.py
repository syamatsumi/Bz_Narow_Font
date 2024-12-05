#!fontforge --lang=py -script

import fontforge
import math

# オンカーブ点のノード数が2より多い(つまり3以上)のパスをok_pathsに保存。
# 2点間の距離が一定数以上あるなら、カマボコ状の形を作ってる可能性がある。
# 問答無用で削除する場合はmin_distanceをクソデカに設定すること。

def ys_rm_little_line(glyph, min_distance=20):
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
                ok_paths.append(contour)  # 距離が長ければOK
        elif len(on_curve_points) > 2:
            # オンクルーブポイントが3点以上の場合は無条件でOK
            ok_paths.append(contour)

    # フォアグラウンドをクリアして、OKパス変数に入れてたコンターを書き戻す
    glyph.foreground = fontforge.layer() # フォアグラウンドをクリア
    for contour in ok_paths:  # OKパスの書き戻し
        glyph.foreground += contour



# バウンディングボックスで判定して、
# しきい値以下のオブジェクトは削除する。

def ys_rm_small_poly(width_threshold, height_threshold, glyph):
# これmainで使うと幅プロパティが逝くから関数内以外で使っちゃダメ。
# 指定された閾値より小さいものをNGパス変数に入れる
    ng_paths = []  # 空リストを初期化
    for contour in glyph.foreground:  # 各パス（輪郭）をループ
        contour.addExtrema("all")
        bbox = contour.boundingBox()
        xmin, ymin, xmax, ymax = bbox
        width = xmax - xmin
        height = ymax - ymin
        if width <= width_threshold and height <= height_threshold:  # 条件をチェック
            ng_paths.append(contour)  # 条件を満たすものをリストに追加
    # 問題のないパス(さっき保存できてないコンター)をOK変数にブチ込む
    ok_paths = [contour for contour in glyph.foreground if contour not in ng_paths]
    # フォアグラウンドをクリアして、OKパス変数に入れてたコンターを書き戻す
    glyph.foreground = fontforge.layer() # フォアグラウンドをクリア
    for contour in ok_paths:  # okパスの書き戻し
        glyph.foreground += contour



if __name__ == "__main__":
    ys_rm_littleline(glyph, 20)