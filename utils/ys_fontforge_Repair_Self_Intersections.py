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
    two_pi = 2 * math.pi

    for contour in glyph.foreground:
        num_points = len(contour)
        # 全てのポイントのインデックスを取得
        point_indices = list(range(num_points))
        i = 0
        while i < num_points:
            idx = i
            current_point = contour[idx]

            # ポイントの属性を取得
            point_type = current_point.type  # 'move', 'line', 'curve', 'qcurve', 'offcurve'など

            # オフカーブポイントは処理しない
            if point_type == 'offcurve':
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

            # 角度を計算
            angle1 = math.atan2(vector1[1], vector1[0])
            angle2 = math.atan2(vector2[1], vector2[0])

            # 二つのベクトルの間の角度差を計算
            angle_diff = (angle2 - angle1) % two_pi

            # 角度差が0から2πの範囲になるように調整
            if angle_diff < 0:
                angle_diff += two_pi

            # 角度差を0から2πの範囲に正規化
            angle_diff = angle_diff % two_pi

            # 角度が閾値未満または(2π - 閾値)を超える場合を評価
            if not angle_threshold_rad < angle_diff < (two_pi - angle_threshold_rad):
                # 問題のあるポイントの連続を検出
                problem_points = []
                start_idx = idx  # 開始インデックスを保存

                # 問題のあるポイントを収集
                initial_i = i  # 問題セグメントの開始位置を保存
                while True:
                    problem_points.append(idx)
                    i += 1
                    if i >= num_points:
                        break  # 輪郭の終端に到達

                    idx = i % num_points
                    current_point = contour[idx]

                    # オフカーブポイントはスキップ
                    if current_point.type == 'offcurve':
                        continue

                    # 次のポイントを取得
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

                    angle1 = math.atan2(vector1[1], vector1[0])
                    angle2 = math.atan2(vector2[1], vector2[0])

                    angle_diff = (angle2 - angle1) % two_pi
                    if angle_diff < 0:
                        angle_diff += two_pi
                    angle_diff = angle_diff % two_pi

                    if angle_threshold_rad < angle_diff < (two_pi - angle_threshold_rad):
                        # 問題のない角度が現れたら終了
                        break

                end_idx = idx

                # 問題のある全てのポイント（オフカーブポイント含む）を収集
                if start_idx <= end_idx:
                    indices_range = range(start_idx, end_idx + 1)
                else:
                    # 輪郭が閉じている場合
                    indices_range = list(range(start_idx, num_points)) + list(range(0, end_idx + 1))

                problem_all_points = []
                for j in indices_range:
                    problem_all_points.append(j)

                # 始点と終点のポイントを取得
                prev_idx = (initial_i - 1) % num_points
                while contour[prev_idx].type == 'offcurve':
                    prev_idx = (prev_idx - 1) % num_points
                    if prev_idx == initial_i:
                        break  # 無限ループ防止

                start_point = contour[prev_idx]
                end_point = contour[end_idx]

                num_problems = len(problem_points)

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

                    # 始点と終点に隣接するオフカーブポイントを移動対象から除外
                    # 始点に隣接するオフカーブポイント
                    start_adjacent_idx = (start_idx + 1) % num_points
                    if not contour[start_adjacent_idx].on_curve and start_adjacent_idx in problem_all_points:
                        problem_all_points.remove(start_adjacent_idx)

                    # 終点に隣接するオフカーブポイント
                    end_adjacent_idx = (end_idx - 1) % num_points
                    if not contour[end_adjacent_idx].on_curve and end_adjacent_idx in problem_all_points:
                        problem_all_points.remove(end_adjacent_idx)

                else:
                    # 奇数個の場合、始点と終点の中間点を使用
                    new_x = (start_point.x + end_point.x) / 2
                    new_y = (start_point.y + end_point.y) / 2

                # 問題のある全てのポイントを新しい位置に移動
                for p_idx in problem_all_points:
                    contour[p_idx].x = new_x
                    contour[p_idx].y = new_y
            else:
                i += 1  # 次のポイントへ進む





# ギザギザになってる部分を平らにならしたい。

def ys_sawtooth_reduction(glyph):
    import math

    for contour in glyph.foreground:
        num_points = len(contour)
        # 全てのポイントのインデックスを取得
        point_indices = list(range(num_points))
        i = 0
        while i < num_points:
            idx = i
            current_point = contour[idx]

            # ポイントの属性を取得
            point_type = current_point.type  # 'move', 'line', 'curve', 'qcurve', 'offcurve'など

            # オフカーブポイントは処理しない
            if point_type == 'offcurve':
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

            # 現在の点と前の点の距離を計算
            distance_prev = math.sqrt(
                (current_point.x - prev_point.x) ** 2 + (current_point.y - prev_point.y) ** 2
            )

            # 現在の点と次の点の距離を計算
            distance_next = math.sqrt(
                (next_point.x - current_point.x) ** 2 + (next_point.y - current_point.y) ** 2
            )

            # 角度が閾値未満または(2π - 閾値)を超える場合を評価
            if distance_prev < 2 or distance_next < 2:
                # 問題のあるポイントの連続を検出
                problem_points = []
                start_idx = idx  # 開始インデックスを保存

                # 問題のあるポイントを収集
                initial_i = i  # 問題セグメントの開始位置を保存
                while True:
                    problem_points.append(idx)
                    i += 1
                    if i >= num_points:
                        break  # 輪郭の終端に到達

                    idx = i % num_points
                    current_point = contour[idx]

                    # オフカーブポイントはスキップ
                    if current_point.type == 'offcurve':
                        continue

                    # 次のポイントを取得
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

                    # 現在の点と前の点の距離を計算
                    distance_prev = math.sqrt(
                        (current_point.x - prev_point.x) ** 2 + (current_point.y - prev_point.y) ** 2
                    )

                    # 現在の点と次の点の距離を計算
                    distance_next = math.sqrt(
                        (next_point.x - current_point.x) ** 2 + (next_point.y - current_point.y) ** 2
                    )

                    if distance_prev >= 2 and distance_next >= 2:
                        # 問題のない距離が現れたら終了
                        break

                end_idx = idx

                # 問題のある全てのポイント（オフカーブポイント含む）を収集
                if start_idx <= end_idx:
                    indices_range = range(start_idx, end_idx + 1)
                else:
                    # 輪郭が閉じている場合
                    indices_range = list(range(start_idx, num_points)) + list(range(0, end_idx + 1))

                problem_all_points = []
                for j in indices_range:
                    problem_all_points.append(j)

                # 始点と終点のポイントを取得
                prev_idx = (initial_i - 1) % num_points
                while contour[prev_idx].type == 'offcurve':
                    prev_idx = (prev_idx - 1) % num_points
                    if prev_idx == initial_i:
                        break  # 無限ループ防止

                start_point = contour[prev_idx]
                end_point = contour[end_idx]

                num_problems = len(problem_points)

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

                    # 始点と終点に隣接するオフカーブポイントを移動対象から除外
                    # 始点に隣接するオフカーブポイント
                    start_adjacent_idx = (start_idx + 1) % num_points
                    if not contour[start_adjacent_idx].on_curve and start_adjacent_idx in problem_all_points:
                        problem_all_points.remove(start_adjacent_idx)

                    # 終点に隣接するオフカーブポイント
                    end_adjacent_idx = (end_idx - 1) % num_points
                    if not contour[end_adjacent_idx].on_curve and end_adjacent_idx in problem_all_points:
                        problem_all_points.remove(end_adjacent_idx)

                else:
                    # 奇数個の場合、始点と終点の中間点を使用
                    new_x = (start_point.x + end_point.x) / 2
                    new_y = (start_point.y + end_point.y) / 2

                # 問題のある全てのポイントを新しい位置に移動
                for p_idx in problem_all_points:
                    contour[p_idx].x = new_x
                    contour[p_idx].y = new_y
            else:
                i += 1  # 次のポイントへ進む


if __name__ == "__main__":
    ys_rmSelfInsec(glyph, 2)
