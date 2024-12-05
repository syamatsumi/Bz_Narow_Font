#!fontforge --lang=py -script

import fontforge
import math

# 鋭角のノードを均す関数です。
# アイデア出しだけやってあとはChatGPT o1-previewに書いて貰ったまんまで、
# 正直なところ、ちゃんと動いてるのかよくわからんちん。

# 見た目にわからないほど小さな自己交差は凄い鋭角を持っています。
# 垂直方向にとびだせばツノになりますし、
# 水平方向に飛び出していてもやはり飛び出して居るポイントは鋭角なのです。
# そこで、本スクリプトでは鋭角を作っているポイントを一箇所に寄せ集めてしまいます。
# あとはglyph.removeOverlap()で重複したポイントを削除すればいいのですが、
# パスの向きがおかしな状態でglyph.removeOverlap()をやると
# そのままグリフがメチャクチャになっちゃうので、
# あえてglyph.removeOverlap()をかけていません。
# 任意のタイミングで実施するようにしてください。
# できればこれを実行した直後がよろしいかと思いますよ。（´∀｀ ）

def ys_repair_Self_Insec(glyph, angle_threshold=2):
    import math
    angle_threshold_rad = math.radians(angle_threshold)

    for contour in glyph.foreground:
        num_points = len(contour)

        # コンター内にオンカーブポイントが存在するか確認
        on_curve_exists = any(p.on_curve for p in contour)
        if not on_curve_exists:
            continue  # 次のコンターへ

        i = 0
        while i < num_points:
            current_point = contour[i]

            # 角度の計算
            if not current_point.on_curve:
                i += 1
                continue  # オフカーブポイントはスキップ

            # 次のオンカーブポイントを探す
            j = (i + 1) % num_points
            found_next_oncurve = False
            while True:
                if contour[j].on_curve:
                    found_next_oncurve = True
                    break
                j = (j + 1) % num_points
                if j == i:
                    break  # 一周してしまった場合

            if not found_next_oncurve:
                i += 1
                continue  # オンカーブポイントが見つからない場合、次へ

            next_point = contour[j]

            # 前のオンカーブポイントを探す
            k = (i - 1) % num_points
            found_prev_oncurve = False
            while True:
                if contour[k].on_curve:
                    found_prev_oncurve = True
                    break
                k = (k - 1) % num_points
                if k == i:
                    break  # 一周してしまった場合

            if not found_prev_oncurve:
                i += 1
                continue  # オンカーブポイントが見つからない場合、次へ

            prev_point = contour[k]

            # ベクトルを計算
            vector1 = (current_point.x - prev_point.x, current_point.y - prev_point.y)
            vector2 = (next_point.x - current_point.x, next_point.y - current_point.y)

            # 内積と外積を計算
            dot_product = vector1[0]*vector2[0] + vector1[1]*vector2[1]
            cross_product = vector1[0]*vector2[1] - vector1[1]*vector2[0]

            # ベクトルの大きさを計算
            mag1 = math.hypot(*vector1)
            mag2 = math.hypot(*vector2)

            if mag1 > 0 and mag2 > 0:
                # 内積と角度を計算
                angle = math.atan2(cross_product, dot_product)
                if angle < 0:
                    angle += 2 * math.pi
            else:
                angle = 0.0  # ベクトルの大きさがゼロの場合

            # 角度が問題のある場合の処理
            if angle_threshold_rad < angle < (2 * math.pi - angle_threshold_rad):
                # 問題のない角度の場合
                i += 1
                continue
            else:
                # 問題のある角度の場合
                # 問題のあるポイントの連続を処理
                problem_points = []
                start_idx = i
                max_iterations = num_points  # 無限ループ防止のため
                iterations = 0

                while iterations < max_iterations:
                    problem_points.append(i)
                    i = (i + 1) % num_points
                    iterations += 1

                    if i == start_idx:
                        break  # 一周した場合

                    current_point = contour[i]
                    if not current_point.on_curve:
                        continue
                    # 次のオンカーブポイントを探す
                    j = (i + 1) % num_points
                    found_next_oncurve = False
                    while True:
                        if contour[j].on_curve:
                            found_next_oncurve = True
                            break
                        j = (j + 1) % num_points
                        if j == i:
                            break  # 一周してしまった場合
        
                    if not found_next_oncurve:
                        i += 1
                        continue  # オンカーブポイントが見つからない場合、次へ
        
                    next_point = contour[j]
        
                    # 前のオンカーブポイントを探す
                    k = (i - 1) % num_points
                    found_prev_oncurve = False
                    while True:
                        if contour[k].on_curve:
                            found_prev_oncurve = True
                            break
                        k = (k - 1) % num_points
                        if k == i:
                            break  # 一周してしまった場合
        
                    if not found_prev_oncurve:
                        i += 1
                        continue  # オンカーブポイントが見つからない場合、次へ
        
                    prev_point = contour[k]
                    # ベクトルを再計算
                    vector1 = (current_point.x - prev_point.x, current_point.y - prev_point.y)
                    vector2 = (next_point.x - current_point.x, next_point.y - current_point.y)

                    dot_product = vector1[0]*vector2[0] + vector1[1]*vector2[1]
                    cross_product = vector1[0]*vector2[1] - vector1[1]*vector2[0]

                    mag1 = math.hypot(*vector1)
                    mag2 = math.hypot(*vector2)

                    if mag1 > 0 and mag2 > 0:
                        angle = math.atan2(cross_product, dot_product)
                        if angle < 0:
                            angle += 2 * math.pi
                    else:
                        angle = 0.0

                    # 角度の評価
                    if angle_threshold_rad < angle < (2 * math.pi - angle_threshold_rad):
                        # 問題のない角度が現れたら終了
                        break

                if iterations >= max_iterations:
                    print("Warning: Potential infinite loop detected in contour processing.")
                    break  # 無限ループを防止

                # 問題のあるポイントの処理
                num_problems = len(problem_points)

                # 始点と終点を取得
                start_idx = (problem_points[0] - 1) % num_points
                end_idx = (problem_points[-1] + 1) % num_points
                start_point = contour[start_idx]
                end_point = contour[end_idx]

                if num_problems % 2 == 0:
                    # 偶数個の場合、問題点の平均座標を計算
                    total_x = sum(contour[p_idx].x for p_idx in problem_points)
                    total_y = sum(contour[p_idx].y for p_idx in problem_points)
                    total_points = num_problems  # 問題オンカーブポイント数
                    avg_x = total_x / total_points
                    avg_y = total_y / total_points

                    # 始点と終点の座標範囲を取得
                    min_x = min(start_point.x, end_point.x)
                    max_x = max(start_point.x, end_point.x)
                    min_y = min(start_point.y, end_point.y)
                    max_y = max(start_point.y, end_point.y)

                    # 平均座標が範囲内にあるかのチェック
                    x_in_range = min_x <= avg_x <= max_x
                    y_in_range = min_y <= avg_y <= max_y

                    if not x_in_range and not y_in_range:
                        # x軸とy軸の両方で範囲外の場合、始点と終点の中間点を使用
                        new_x = (start_point.x + end_point.x) / 2
                        new_y = (start_point.y + end_point.y) / 2
                    else:
                        # そうでない場合、平均座標を使用
                        new_x = avg_x
                        new_y = avg_y

                else:
                    # 奇数個の場合、始点と終点の中間点を使用
                    new_x = (start_point.x + end_point.x) / 2
                    new_y = (start_point.y + end_point.y) / 2

                # 始点と終点に隣接するオフカーブポイントを移動対象から除外
                # 始点に隣接するオフカーブポイント
                start_adjacent_idx = (start_idx + 1) % num_points
                if not contour[start_adjacent_idx].on_curve and start_adjacent_idx in problem_points:
                    problem_points.remove(start_adjacent_idx)

                # 終点に隣接するオフカーブポイント
                end_adjacent_idx = (end_idx - 1) % num_points
                if not contour[end_adjacent_idx].on_curve and end_adjacent_idx in problem_points:
                    problem_points.remove(end_adjacent_idx)

                # 問題のある全てのポイント（オフカーブポイント含む）を新しい位置に移動
                for p_idx in problem_points:
                    contour[p_idx].x = new_x
                    contour[p_idx].y = new_y
            print(f"\r now:{glyph.glyphname:<15} {i} {p_idx}", end=" ", flush=True)
            i += 1  # 次のポイントへ進む

if __name__ == "__main__":
    ys_rmSelfInsec(glyph, 2)
