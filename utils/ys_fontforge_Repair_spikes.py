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
# 3次ベジエで実行すると狂うので2次ベジエに変更して作業し、元に戻すようにした。
# 任意のタイミングで実施するようにしてください。
# できればこれを実行した直後がよろしいかと思いますよ。（´∀｀ ）


# 前後のポイントを取得（オフカーブポイントをスキップ）
def ys_getpoint_oncurve(contour, idx):
    # 渡されたコンターの配列長さをチェック
    num_points = len(contour)
    # 手前のオンカーブポイントを取得
    prev_idx = (idx - 1) % num_points
    while not contour[prev_idx].on_curve:
        prev_idx = (prev_idx - 1) % num_points
        if prev_idx == idx:
            break  # 無限ループ防止
    next_idx = (idx + 1) % num_points
    # 次のオンカーブポイントを取得
    while not contour[next_idx].on_curve:
        next_idx = (next_idx + 1) % num_points
        if next_idx == idx:
            break  # 無限ループ防止
    prev_point = contour[prev_idx]
    next_point = contour[next_idx]
    return prev_point, next_point, prev_idx, next_idx

# ベクトルと角度を出す。
def ys_fig_anglegap(ptA, ptB, ptC):
    # ベクトルを計算
    vec1 = ( ptB.x - ptA.x, ptB.y - ptA.y,)
    vec2 = ( ptB.x - ptC.x, ptB.y - ptC.y,)
    vec3 = ( ptA.x - ptC.x, ptA.y - ptC.y,)
    # 角度を計算
    angle1 = math.atan2(vec1[1], vec1[0])
    angle2 = math.atan2(vec2[1], vec2[0])
    # 二つのベクトルの間の角度差を計算
    angle_gap = (angle2 - angle1)
    return angle_gap, vec1, vec2, vec3

# 問題のあるポイントの連続を検出
def ys_find_problem_clusters(contour, thresh_rad, input_idx):
    # 渡されたコンターの配列長さをチェック
    num_points = len(contour)
    problem_pts_oncurve = 0  # オンカーブ点を数える
    visited = set([input_idx])  # 訪問済みポイントを記録
    idx = input_idx
    end_idx = input_idx  # ループ前に初期化

    while True:
        # 確認中のポイント
        current_point = contour[idx]
        prev_point, next_point, _, next_idx = ys_getpoint_oncurve(contour, idx)
        angle_diff, _, _, _ = ys_fig_anglegap(prev_point, current_point, next_point)

        # 次のポイントが記録済みの場合はループ終了。
        if next_idx in visited:
            end_idx = idx
            break
        # 角度がNG判定のときはオンカーブ点を追記して次のループへ
        elif -thresh_rad < angle_diff < thresh_rad:
            problem_pts_oncurve += 1
            end_idx = next_idx
            idx = next_idx
            visited.add(idx)
        # 角度OK、再訪無しなら現在のポイントを終了範囲として戻り値に。
        else:
            end_idx = idx
            break

    return end_idx, problem_pts_oncurve


def ys_gather_and_shift_ng_points(contour, start_idx, end_idx, use_ng_points_for_average):
    # 渡されたコンターの配列長さをチェック
    num_points = len(contour)

    # 問題点の直前直後の点
    start_point = contour[start_idx]
    end_point = contour[end_idx]

    # 問題点のインデックスを収集
    if start_idx <= end_idx:
        # 始点の次から、レンジ終点まで(Pythonではレンジ終端は除外)
        indices_range = range(start_idx + 1 , end_idx)
    else:
        # 輪郭が閉じててループ部を挟む場合
        indices_range = (
            list(range(start_idx +1, num_points)) +
            list(range(0, end_idx))
            )

    # 実際の問題となる点をオンカーブのみと全部入りに別けて保存
    problem_points = []
    problem_all_points = []
    for i in indices_range:
        if contour[i].on_curve:
            problem_points.append(i)
            problem_all_points.append(i)
        else:
            problem_all_points.append(i)

    # 問題点を含む平均座標を使う場合
    if use_ng_points_for_average:
        total_x = sum(contour[p_idx].x for p_idx in problem_points)
        total_y = sum(contour[p_idx].y for p_idx in problem_points)
        total_points = len(problem_points)
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
        if not all([x_in_range, y_in_range]):
            new_x = (start_point.x + end_point.x) / 2
            new_y = (start_point.y + end_point.y) / 2

        # そうでない場合、平均座標を使用
        else:
            new_x = avg_x
            new_y = avg_y

    # 奇数個とかオフカーブポイントだけが移動対象の場合、始点と終点の中間点を使用
    else:
        new_x = (start_point.x + end_point.x) / 2
        new_y = (start_point.y + end_point.y) / 2

    # 問題のある全てのポイントを新しい位置に移動
    for p_idx in problem_all_points:
        contour[p_idx].x = new_x
        contour[p_idx].y = new_y

    return contour



# コンター間のループ
def ys_rmSpike(contour, thresh_rad):
    # 全てのポイントのインデックスを取得
    num_points = len(contour)
    for i in range(num_points):
        idx = i
        current_point = contour[idx]

        # 前後のオンカーブポイントを取得
        prev_point, next_point, prev_idx, next_idx = ys_getpoint_oncurve(contour, idx)

        # 二つのベクトルの間の角度差を計算
        angle_diff, vec_cp, vec_cn, vec_pn = ys_fig_anglegap(prev_point, current_point, next_point)

        # 角度が閾値の範囲内であるなら対処
        if -thresh_rad < angle_diff < thresh_rad:
            # オンカーブポイントなら連続点の判定に進む
            if current_point.on_curve:
                start_idx = prev_idx
                end_idx, problem_pts_oncurve = ys_find_problem_clusters(contour, thresh_rad, prev_idx)

                # 上のループ処理でトチった時用の保険……
                if end_idx == start_idx:
                    end_idx = next_idx
                    problem_pts_oncurve = 1

                # オンカーブポイントが偶数ならNGポイント座標の平均へ移動のフラグを立てる
                if problem_pts_oncurve % 2 == 0:
                    use_ng_points_for_average = True
                else:
                    use_ng_points_for_average = False

                # 問題点の座標を集めて一箇所に移動させる
                ys_gather_and_shift_ng_points(contour, start_idx, end_idx, use_ng_points_for_average)

            # オフカーブポイントなら、長さ比較で判定・対応。
            # オンカーブポイント同士のベクトルと比較して3倍以上の大きさがあるならアウト
            else:
                len_cp = vec_cp[0]**2 + vec_cp[1]**2
                len_cn = vec_cn[0]**2 + vec_cn[1]**2
                len_pn = vec_pn[0]**2 + vec_pn[1]**2
                # どちらかのベクトルがprev-next間のベクトルより3倍以上大きいなら、
                # オフカーブポイントはprevとnextの中間点にに強制移動。
                if len_cp > (3**2) * len_pn or len_cn > (3**2) * len_pn:
                    start_idx = prev_idx
                    end_idx = next_idx
                    use_ng_points_for_average = False

                    # 問題点の座標を集めて一箇所に移動させる
                    ys_gather_and_shift_ng_points(contour, start_idx, end_idx, use_ng_points_for_average)
    return contour



# グリフオブジェクトをコンター単位にバラして実行。通常はコレを呼べばOK。
def ys_repair_spikes(glyph, angle_threshold=2):
    proc_paths = []
    # 角度しきい値をラジアン角に変更
    thresh_rad = math.radians(angle_threshold)
    for contour in glyph.foreground:
        # 3次ベジエのコンターは一度2次に変換してから処理
        if contour.is_quadratic:
            proc_path = ys_rmSpike(contour.dup(), thresh_rad)
        else:
            contour.is_quadratic = True
            proc_path = ys_rmSpike(contour.dup(), thresh_rad)
            proc_path.is_quadratic = False
        # 加工後のパスを保存
        proc_paths.append(proc_path)

    # レイヤを消去して加工したパスを書き戻す
    glyph.foreground = fontforge.layer()
    for contour in proc_paths:
        glyph.foreground += contour

    return glyph

if __name__ == "__main__":
    ys_repair_spikes(glyph, angle_threshold=2)
