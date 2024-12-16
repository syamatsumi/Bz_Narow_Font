#!fontforge --lang=py -script

import fontforge
import math
two_pi = 2 * math.pi

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
# contour.merge()はかけるようにしました。
# 任意のタイミングで実施するようにしてください。
# できればこれを実行した直後がよろしいかと思いますよ。（´∀｀ ）


# 前後のポイントを取得（オフカーブポイントをスキップ）
def ys_getpoint_oncurve(contour, idx, num_points):
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
    return prev_point, next_point

# ベクトルと角度を出す。
def ys_fig_anglegap(ptA, ptB, ptC):
    # ベクトルを計算
    vec1 = ( ptB.x - ptA.x, ptB.y - ptA.y,)
    vec2 = ( ptC.x - ptB.x, ptC.y - ptB.y,)
    # 角度を計算
    angle1 = math.atan2(vec1[1], vec1[0])
    angle2 = math.atan2(vec2[1], vec2[0])
    # 二つのベクトルの間の角度差を計算
    angle_diff = (angle2 - angle1) % two_pi
    # 角度差が0から2πの範囲になるように調整
    if angle_diff < 0:
        angle_diff += two_pi
    # 角度差を0から2πの範囲に正規化
    angle_gap = angle_diff % two_pi
    return angle_gap, vec1, vec2

# 問題のあるポイントの連続を検出
def ys_find_problem_clusters(contour, thresh_rad, i, idx, num_points):
    # 開始インデックスを保存
    start_idx = idx

    # 問題セグメントの開始位置を保存
    initial_i = i

    # 問題ポイントの格納枠
    problem_points = []

    while True:
        problem_points.append(idx)
        i += 1

        # 輪郭の終端に到達したら終了
        if i >= num_points:
            break

        idx = i % num_points
        current_point = contour[idx]
        if current_point.type == 'offcurve':
            continue

        prev_point, next_point = ys_getpoint_oncurve(contour, idx, num_points)
        angle_diff, vector1, vector2 = ys_fig_anglegap(prev_point, current_point, next_point)

        if thresh_rad < angle_diff < (two_pi - thresh_rad):
            break

    # 終了インデックスを保存
    end_idx = idx

    # 問題のある全てのポイント（オフカーブポイント含む）を収集
    if start_idx <= end_idx:
        indices_range = range(start_idx, end_idx + 1)

    # 輪郭が閉じている場合
    else:
        indices_range = (
            list(range(start_idx, num_points)) + 
            list(range(0, end_idx + 1))
        )

    problem_all_points = []
    for j in indices_range:
        problem_all_points.append(j)

    # 始点と終点のポイントを取得
    prev_idx = (initial_i - 1) % num_points
    while contour[prev_idx].type == 'offcurve':
        prev_idx = (prev_idx - 1) % num_points
        if prev_idx == initial_i:
            break  # 無限ループ防止

    # 問題となる点を一箇所に寄せ集める。
    start_point = contour[prev_idx]
    end_point = contour[end_idx]
    num_problems = len(problem_points)

    # 偶数個の場合、問題点の平均座標を計算
    if num_problems % 2 == 0:
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

        # x軸とy軸の両方で範囲外の場合、始点と終点の中間点を使用
        if not x_in_range and not y_in_range:
            new_x = (start_point.x + end_point.x) / 2
            new_y = (start_point.y + end_point.y) / 2

        # そうでない場合、平均座標を使用
        else:
            new_x = avg_x
            new_y = avg_y

        # 始点と終点に隣接するオフカーブポイントを移動対象から除外
        # 始点に隣接するオフカーブポイント
        start_adjacent_idx = (start_idx + 1) % num_points
        if (not contour[start_adjacent_idx].on_curve
            and start_adjacent_idx in problem_all_points):
            problem_all_points.remove(start_adjacent_idx)

        # 終点に隣接するオフカーブポイント
        end_adjacent_idx = (end_idx - 1) % num_points
        if (not contour[end_adjacent_idx].on_curve 
            and end_adjacent_idx in problem_all_points):
            problem_all_points.remove(end_adjacent_idx)

    # 奇数個の場合、始点と終点の中間点を使用
    else:
        new_x = (start_point.x + end_point.x) / 2
        new_y = (start_point.y + end_point.y) / 2

    # 問題のある全てのポイントを新しい位置に移動
    for p_idx in problem_all_points:
        contour[p_idx].x = new_x
        contour[p_idx].y = new_y

    return contour, i



# メイン関数。
def ys_rmSelfInsec(contour, thresh_rad):
    # 全てのポイントのインデックスを取得
    num_points = len(contour)
    i = 0
    while i < num_points:
        idx = i
        current_point = contour[idx]

        # ポイントの属性'move', 'line', 'curve', 'qcurve', 'offcurve'など
        point_type = current_point.type

        # オフカーブポイントは処理しない
        if point_type == 'offcurve':
            i += 1; continue

        # 前後のポイントを取得（オフカーブポイントをスキップ）
        prev_point, next_point = ys_getpoint_oncurve(contour, idx, num_points)

        # 二つのベクトルの間の角度差を計算
        angle_diff, vector1, vector2 = ys_fig_anglegap(prev_point, current_point, next_point)

        # 角度が閾値未満または(2π - 閾値)を超える場合を評価
        if not thresh_rad < angle_diff < (two_pi - thresh_rad):
            contour, i = ys_find_problem_clusters(contour, thresh_rad, i, idx, num_points)
        # 角度が閾値以上(合格)のため、何もせずに次のポイントへ進む
        else:
            i += 1

    # マージを用いて上の工程で集合させた点を整理
    contour.merge()

    # 戻り値はコンターで。
    return contour



# グリフオブジェクトをコンター単位にバラして実行。通常はコレを呼べばOK。
def ys_repair_Self_Insec(glyph, angle_threshold=2):
    # 角度しきい値をラジアン角に変更
    thresh_rad = math.radians(angle_threshold)
    for contour in glyph.foreground:
        # 2次ベジエのコンターは一度3次に変換してから処理
        if contour.is_quadratic:
            contour.is_quadratic = False
            contour = ys_rmSelfInsec(contour.dup(), thresh_rad)
            contour.is_quadratic = True
        else:
            contour = ys_rmSelfInsec(contour.dup(), thresh_rad)

if __name__ == "__main__":
    ys_rmSelfInsec(contour, thresh_rad)
