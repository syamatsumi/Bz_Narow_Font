#!fontforge --lang=py -script

import fontforge
import psMat
import math

# 鋭角ノードを残り2点間に動かす関数。
# 許容される最小角度はデフォルトで2°
def ys_trim_spikes(glyph, angle_threshold=2):
    angle_threshold_rad = math.radians(angle_threshold)  # 角度をラジアンに変換
    for contour in glyph.foreground:
        i = 0
        while i < len(contour):
            # ノードの前後を取得（ループを考慮して）
            current_point = contour[i]
            # オンクルーブポイントのみを対象とする
            if not current_point.on_curve:
                i += 1
                continue
            # 前後のオンクルーブポイントを取得
            prev_index = i - 1
            while not contour[prev_index % len(contour)].on_curve:
                prev_index -= 1
            next_index = i + 1
            while not contour[next_index % len(contour)].on_curve:
                next_index += 1
            prev_point = contour[prev_index % len(contour)]
            next_point = contour[next_index % len(contour)]
            
            # 座標を取得
            prev_coords = (prev_point.x, prev_point.y)
            current_coords = (current_point.x, current_point.y)
            next_coords = (next_point.x, next_point.y)
            
            # ベクトルを計算
            vector1 = (prev_coords[0] - current_coords[0], prev_coords[1] - current_coords[1])
            vector2 = (next_coords[0] - current_coords[0], next_coords[1] - current_coords[1])
            
            # ベクトルの大きさと内積を計算
            mag1 = math.hypot(*vector1)
            mag2 = math.hypot(*vector2)
            dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
            
            # 角度を計算
            if mag1 > 0 and mag2 > 0:  # ゼロ除算回避
                cos_angle = dot_product / (mag1 * mag2)
                cos_angle = max(-1, min(1, cos_angle))  # 浮動小数点誤差の補正
                angle = math.acos(cos_angle)
                # 角度が閾値未満なら修正
                if angle < angle_threshold_rad:
                    # 中間点を計算して移動
                    midpoint = ((prev_coords[0] + next_coords[0]) / 2,
                                (prev_coords[1] + next_coords[1]) / 2)
                    current_point.x, current_point.y = midpoint
            i += 1

if __name__ == "__main__":
    ys_trim_spikes(glyph, angle_threshold=2)
