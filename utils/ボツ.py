
# 輪郭の右辺だけを引き延ばします。
# 逆方向の輪郭は左辺が縮小します。
# ys_expand_Xweight(glyph, offset)
from .ys_fontforge_widestroke import ys_expand_Xweight

# 各スタイルを表すブール値を受け取り、fsSelectionの値を計算する関数。
# この関数では引数の順序がビットの並びと異なるので注意すること。
# (利用する気の無いパラメーターが多くてね……)
def build_fsSelection(
    wws=True,           # WWSファミリー（Weight-Width-Slope）
    regular=False,      # レギュラースタイル
    bold=False,         # ボールドスタイル
    italic=False,       # イタリックスタイル
    underscore=False,   # 下線入りスタイル
    negative=False,     # 地黒白抜きのスタイル
    outlined=False,     # ワイヤーフレーム的なスタイル
    strikeout=False,    # 打消し線スタイル
    use_metrics=False,  # OS/2テーブルのTypo Metricsを使用する
    oblique=False       # 疑似イタリック体スタイル
):

    # 各ビットの定義
    ITALIC =      0b0000000000000001
    UNDERSCORE =  0b0000000000000010
    NEGATIVE =    0b0000000000000100
    OUTLINED =    0b0000000000001000
    STRIKEOUT =   0b0000000000010000
    BOLD =        0b0000000000100000
    REGULAR =     0b0000000001000000
    USE_METRICS = 0b0000000010000000
    WWS =         0b0000000100000000
    OBLIQUE =     0b0000001000000000

    # 各ビットを組み立てる。
    fs_selection = 0b0000000000000000
    if italic:
        fs_selection |= ITALIC
    if underscore:
        fs_selection |= UNDERSCORE
    if negative:
        fs_selection |= NEGATIVE
    if outlined:
        fs_selection |= OUTLINED
    if strikeout:
        fs_selection |= STRIKEOUT
    if bold:
        fs_selection |= BOLD
    if regular:
        fs_selection |= REGULAR
    if use_typo_metrics:
        fs_selection |= USE_TYPO_METRICS
    if wws:
        fs_selection |= WWS
    if oblique:
        fs_selection |= OBLIQUE

    return fs_selection





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


# ASCII範囲にコンポジットグリフが居たら解除
def decomposit_asc(font):
    for codepoint in range(0x20, 0x7F):
        if codepoint in font:
            glyph = font[codepoint]
            if not glyph.isWorthOutputting():
                continue  # 出力しないグリフはスキップ
            if len(glyph.references) > 0:
                glyph.unlinkRef() #コンポジットグリフの参照を解除


# ASCII範囲に基づいてフォントがプロポーショナルかを判定
def isprop(font):
    widths = set()  # 空のセットを初期化
    for i in range(32, 127):  # ASCII範囲をループ
        char = chr(i)
        if char in font:  # グリフが存在するか確認
            glyph = font[char]
            if hasattr(glyph, "width"):  # 幅の属性があるか検証
                widths.add(glyph.width)  # 幅をセットに追加
    # 幅のバリエーション数が閾値以上ならプロポーショナル
    if len(widths) >= IS_PROPORTIONAL_CUTOFF_VARIANCE:
        style_is_prop = True
    else:
        style_is_prop = False
    return style_is_prop

# 縮小率で
    if VSHRINK_RATIO >= 0.7:
        stroke_flag = True
    elif VSHRINK_RATIO < 0.7 and font_weight < 700:
        stroke_flag = True
    elif VSHRINK_RATIO >= 0.5 and font_weight < 500:
        stroke_flag = True
    else:  # 狭め方が5割越えてたり、そこに近い値な上でウェイトが重いグリフは基本的にストロークから除外。
        stroke_flag = False



        # グリフのウェイトや複雑さを勘案してストロークの幅を弱める
        # これやるとグリフの太さがガタガタになって見た目がおかしくなるから一旦封印。
        # point_count, stroke_width, stroke_flag = custom_stroke_width(glyph, font_weight, base_stroke_width, stroke_flag)
        # print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Point Count'f'{point_count:<6}':<48}\r", end=" ", flush=True)


# フォントウエイトと確認中グリフのポイント数を勘案してストロークの幅を変える
def custom_stroke_width(glyph, font_weight, base_stroke_width, stroke_flag):
    point_count = sum(len(contour) for contour in glyph.layers["Fore"])
    # 幅の縮小率が高いほど発動条件をシビアになる。
    sleshpt = STRWR_POINTS * VSHRINK_RATIO

    # 点の数が規定値を上回るか、ウエイトが高いとナーフ発動。
    if point_count > sleshpt or font_weight > STRWR_WEIGHT:

        # 点の数が多いほどストロークが細くなる
        stroke_ratio = sleshpt / point_count

        # 縮小率が高いほどストロークが細くなる
        stroke_ratio = stroke_ratio * VSHRINK_RATIO

        # REDUCE RATIOを反映させる
        stroke_ratio = stroke_ratio * REDUCE_RATIO

        # 偶数にするために半分に割って整数化して倍にする。
        stroke_width = round((base_stroke_width * stroke_ratio)/2)*2
    else:  # 条件に一致しないならなにもしない
        stroke_width = base_stroke_width

    # ストローク幅が10を切るならstroke_flagをFalseにする
    if stroke_width < 10:
        stroke_flag = False
    return point_count, stroke_width, stroke_flag


# 最後にTTFの仕様に合わせた最適化を実施
def finish_optimise(glyph, counter):
    anomality_repair1(glyph, counter)
    anomality_repair1(glyph, counter)
    anomality_repair1(glyph, counter)

    ys_repair_Self_Insec(glyph, 3)
    glyph.round()
    glyph.removeOverlap()
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    ys_rm_small_poly(glyph, 25, 25)

    ys_repair_Self_Insec(glyph, 3)
    glyph.round()
    glyph.removeOverlap()
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    ys_rm_small_poly(glyph, 25, 25)

    if (glyph.validate(1) & 0x0FF) != 0 and (glyph.validate(1) & 0x0FF) != 0x04:
        ys_repair_si_chain(glyph, counter)
    if (glyph.validate(1) & 0x0FF) != 0 and (glyph.validate(1) & 0x0FF) != 0x04:
        ys_repair_si_chain(glyph, counter)
    glyph.addExtrema("all")


    # オフカーブポイントの処理
    # オフカーブポイントだけがどえらく暴れるパターンが発見されたため追加
    num_points = len(contour)
    i = 0
    while i < num_points:
        idx = i
        current_point = contour[idx]

        # 循環を考慮して前後のインデックスと座標を取得
        prev_idx = (idx - 1) % num_points
        next_idx = (idx + 1) % num_points
        prev_point = contour[prev_idx]
        next_point = contour[next_idx]

        # 二つのベクトルの間の角度差を計算
        angle_diff, vector1, vector2 = ys_fig_anglegap(prev_point, current_point, next_point)

        # 角度が閾値未満または(2π - 閾値)を超える場合を評価
        if not thresh_rad < angle_diff < (two_pi - thresh_rad):
            new_x = (prev_point.x + next_point.x) / 2
            new_y = (prev_point.y + next_point.y) / 2
            # 問題のあるポイントを新しい位置に移動
            contour[idx].x = new_x
            contour[idx].y = new_y
        i += 1

    # マージを用いて上の工程で集合させた点を整理
    contour.merge()


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




# 時計回りのコンターを、拡大幅で削られる分だけ
# 各コンターの中心から拡大する。
def ys_cwhogo_expantion(glyph, stroke_width):
    proc_paths = []
    for contour in glyph.foreground:
        # 時計回りのコンターのみ処理
        if not contour.isClockwise():
            # コンターの境界ボックスを取得
            bbox = contour.boundingBox()
            x_min, y_min, x_max, y_max = bbox
            # コンターの幅を計算
            gwidth = x_max - x_min
            # 拡大率を計算
            if gwidth == 0:
                continue  # 幅が0の場合スキップ
            scale_factor = (gwidth + stroke_width *2) / gwidth
            print(scale_factor)
            # コンターの中心を計算
            center_x = (x_min + x_max) / 2
            # コンターを原点に移動
            contour.transform(psMat.translate(-center_x, 0))
            # コンターを拡大
            contour.transform(psMat.scale(scale_factor, 1))
            # 元の位置に戻す
            contour.transform(psMat.translate(center_x, 0))
        # どちら周りにしてもパスを保存
        proc_paths.append(contour.dup())
    # レイヤを消去して加工したパスを書き戻す
    glyph.foreground = fontforge.layer()
    for contour in proc_paths:
        glyph.foreground += contour
        glyph.background += contour

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



    # オフカーブポイントの処理
    # (オフカーブポイントだけが暴れてるときがあるため)
    i = 0
    while i < num_points:
        idx = i
        current_point = contour[idx]

        # ここではオンカーブポイントを処理しない
        if current_point.on_curve:
            i += 1; continue

        # 前後のポイントを取得（オフカーブポイントをスキップ）
        prev_point, next_point = ys_getpoint_oncurve(contour, idx, num_points)

        # 二つのベクトルの間の角度差を計算
        angle_diff, vector1, vector2 = ys_fig_anglegap(prev_point, current_point, next_point)

        # 始点と終点の座標範囲を取得
        under_x = min(prev_point.x, next_point.x) - 200
        upper_x = max(prev_point.x, next_point.x) + 200
        under_y = min(prev_point.y, next_point.y) - 200
        upper_y = max(prev_point.y, next_point.y) + 200

        # この座標が範囲内にあるかのチェック
        x_in_range = under_x <= current_point.x <= upper_x
        y_in_range = under_y <= current_point.y <= upper_y

        # 角度が閾値未満または(2π - 閾値)を超える場合は加工。
        if (
            angle_diff > 0.01 and
            angle_diff < (two_pi - 0.01) and
            not x_in_range and
            not y_in_range
            ):
            # このオフカーブポイントは前後のポイントの中間に移動
            new_x = (prev_point.x + next_point.x) / 2
            new_y = (prev_point.y + next_point.y) / 2
            current_point.x = new_x
            current_point.y = new_y
        i += 1




# オンカーブポイントの条件式がおかしくて全部拾ってた頃の名残。
# 本来の姿を取り戻したら強くなり過ぎてこんな処理してたらボロボロになる。
    # スパイク状の独立したコンターを削除する。
    # 変化が無くなるまで繰り返す。
    stroke_prev = [contour.dup() for contour in glyph.foreground]
    ys_repair_spikes(glyph, 3)
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    stroke_aftr = [contour.dup() for contour in glyph.foreground]
    if stroke_prev != stroke_aftr:
        stroke_prev = [contour.dup() for contour in glyph.foreground]
        ys_repair_spikes(glyph, 3)
        ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
        stroke_aftr = [contour.dup() for contour in glyph.foreground]
        if stroke_prev != stroke_aftr:
            stroke_prev = [contour.dup() for contour in glyph.foreground]
            ys_repair_spikes(glyph, 3)
            ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
            stroke_aftr = [contour.dup() for contour in glyph.foreground]
            if stroke_prev != stroke_aftr:
                stroke_prev = [contour.dup() for contour in glyph.foreground]
                ys_repair_spikes(glyph, 3)
                ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
                stroke_aftr = [contour.dup() for contour in glyph.foreground]
                if stroke_prev != stroke_aftr:
                    ys_repair_spikes(glyph, 3)
                    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)



# 修復チェインの繰り返し実行。変化がなくなるか悪化するなら終了。
def ys_anomality_repair(glyph, counter):
    ys_repair_si_chain(glyph, counter)
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




    # スパイク状の独立したコンターを削除する。
    # 変化が無くなるまで繰り返す。
    stroke_prev = [contour.dup() for contour in glyph.foreground]
    ys_repair_spikes(glyph, 3)
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    stroke_aftr = [contour.dup() for contour in glyph.foreground]
    if stroke_prev != stroke_aftr:
        stroke_prev = [contour.dup() for contour in glyph.foreground]
        ys_repair_spikes(glyph, 3)
        ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
        stroke_aftr = [contour.dup() for contour in glyph.foreground]
        if stroke_prev != stroke_aftr:
            stroke_prev = [contour.dup() for contour in glyph.foreground]
            ys_repair_spikes(glyph, 3)
            ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
            stroke_aftr = [contour.dup() for contour in glyph.foreground]
            if stroke_prev != stroke_aftr:
                stroke_prev = [contour.dup() for contour in glyph.foreground]
                ys_repair_spikes(glyph, 3)
                ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
                stroke_aftr = [contour.dup() for contour in glyph.foreground]
                if stroke_prev != stroke_aftr:
                    ys_repair_spikes(glyph, 3)
                    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)

         テスト対象外のグリフを事前にピックアップ
        tst_delete_glyphs = [glyph for glyph in font.glyphs() if glyph.glyphname not in TGTGRYPHNAME]
         テスト対象外のグリフを削除
        print("testmode : Delete untested glyphs.", flush=True)
        for glyph in tst_delete_glyphs:
            font.removeGlyph(glyph)





# 大きく縮める際、元から半分サイズのグリフがあるなら交換してしまう。
def swap_hwglyph(font, glyph, is_propotional, stroke_flag, base_stroke_width):
    # 元のグリフ幅を控えておく
    orig_width = glyph.width

    #スワップ処理
    if is_propotional:
        swap_flag = ys_pswaplist(font, glyph)
    else:
        swap_flag = ys_swaplist(font, glyph)

    # 交換が成立していた場合、拡幅処理の影響を減らすため
    if swap_flag:
        swap_width = glyph.width
        # 念の為0除算対策
        if swap_width == 0:
             return False
        # 最初から縮小目標とほぼ近い幅のグリフはストロークの対象外にする。
        # ストロークの影響を最小限に留めるために元の幅にまで広げる
        elif (swap_width / orig_width) <= VSHRINK_RATIO * 1.05:
            expratio = orig_width / swap_width
            stroke_flag = False
        else:
            expratio = orig_width / swap_width
        # 基本ストローク幅のセッティング
        base_stroke_width = STROKE_WIDTH_MIN + STROKE_WIDTH_SF * (1 - (VSHRINK_RATIO / expratio))
        # 基本ストローク幅は整数かつ偶数に設定する
        base_stroke_width = (base_stroke_width // 2) * 2
        if base_stroke_width <= 10:
            stroke_flag = False

        glyph.transform(psMat.scale(expratio, 1),"partialRefs")
        glyph.addExtrema("all")
    return stroke_flag, base_stroke_width



