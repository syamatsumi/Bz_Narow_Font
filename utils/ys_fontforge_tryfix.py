#!fontforge --lang=py -script

import fontforge
import psMat

from .ys_fontforge_Remove_artifacts import ys_closepath, ys_rm_spikecontours, ys_rm_isolatepath, ys_rm_small_poly
from .ys_fontforge_Repair_spikes import ys_repair_spikes


# スパイク状コンターの除去などの処理一式
def ys_repair_si(glyph, thdeg, thretio):
    ys_repair_spikes(glyph, thdeg)# コンター内スパイクの除去
    # スパイク状コンターの除去。
    ys_rm_spikecontours(glyph, thretio, 0.001, 10)
    glyph.round()  # 整数化
    glyph.addExtrema("all")  # 極点の追加
    glyph.removeOverlap()  # 重複の削除(コンターの合成)
    ys_rm_isolatepath(glyph)  # 孤立したパスの削除
    ys_rm_spikecontours(glyph, thretio, 0.001, 10)
    ys_repair_spikes(glyph, thdeg)
    glyph.round()
    glyph.addExtrema("all")
    glyph.removeOverlap()
    ys_rm_isolatepath(glyph)
    ys_rm_spikecontours(glyph, thretio, 0.001, 10)
    ys_rm_small_poly(glyph, 25, 25)
    glyph.addExtrema("all")

# 作業レイヤーを元に戻す
def ys_restore(glyph, backup):
    glyph.foreground = fontforge.layer()
    for contour in backup:
        glyph.foreground += contour



# 修復処理の強度を強めながら直るまで繰り返す
def ys_repair_si_chain(glyph, proc_cnt):
    if glyph.validate(1) & 0x01:  # 開いたパスを検出
        ys_closepath(glyph)  # パスを閉じる
    ys_rm_isolatepath(glyph)  # 孤立したゴミパスを削除
    ys_repair_spikes(glyph, 1)  # removeoverlapを絡めない所でやっとく必要ある。
    glyph.round()  # 整数化
    # 処理戻し用のバックアップを取得
    forebackup = [contour.dup() for contour in glyph.foreground]

    mode = f"{glyph.validate(1):x}"
    if (glyph.validate(1) & 0x0FF) != 0:
        previous_flags = glyph.validate(1) & 0x0FF
        for stronger in range(1, 6):  # 強度1から5を順番に試す
            print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Anomality Repair 'f'{stronger} mode'f'{mode}':<48}\r", end=" ", flush=True)
            ys_repair_si(glyph, stronger * 0.1, 0.1 + stronger * 0.01)  # 修復処理
            current_flags = glyph.validate(1) & 0x0FF
            if ((previous_flags & ~current_flags) != 0 and  # フラグが降りた上で
                (~previous_flags & current_flags) == 0):  # 新たに立ったフラグがない
                break  # 成功したからループ終了
            else:
                ys_restore(glyph, forebackup)  # リセットして次の周回へ

        else:  # breakされない = 修復失敗。
            print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Repair failure, rollback.':<48}\r", end=" ", flush=True)
            ys_repair_si(glyph, 2, 0.1)  # 最低限の処理を実施

    # そもそもバリデーションに問題が無かった時用の仕上げ処理
    else:
        ys_repair_si(glyph, 2, 0.1)



# 拡大縮小の繰り返しで丸まらないかな？
def ys_rescale(glyph, mag):
    glyph.transform(psMat.scale(mag, 1))
    glyph.round()  # 整数化
    glyph.addExtrema("all") # 極点を追加
    glyph.removeOverlap()  # 結合
    glyph.transform(psMat.scale(1/mag, mag))
    glyph.round()
    glyph.addExtrema("all")
    glyph.removeOverlap()
    glyph.transform(psMat.scale(mag, 1))
    glyph.round()
    glyph.addExtrema("all")
    glyph.removeOverlap()
    glyph.transform(psMat.scale(1/mag, 1/mag))
    ys_repair_spikes(glyph, 0.5)
    glyph.addExtrema("all")
    glyph.removeOverlap()
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    ys_rm_isolatepath(glyph)
    ys_rm_small_poly(glyph, 25, 25)
    glyph.addExtrema("all")

# 拡大縮小と単純化で丸まらないかな？
def ys_rescale_and_simplify(glyph, mag):
    glyph.transform(psMat.scale(1, mag))
    ys_simplify(glyph)  # 単純化試行
    ys_closepath(glyph)  # 開いたパスの修正
    ys_rm_spikecontours(glyph, 0.15, 0.001, 10)
    ys_repair_spikes(glyph, 0.5)
    glyph.round()  # 整数化
    glyph.addExtrema("all") # 極点を追加
    glyph.removeOverlap()  # 結合
    glyph.transform(psMat.scale(mag, 1/mag))
    ys_simplify(glyph)
    ys_closepath(glyph)
    ys_rm_spikecontours(glyph, 0.15, 0.001, 10)
    ys_repair_spikes(glyph, 0.5)
    glyph.round()
    glyph.addExtrema("all")
    glyph.removeOverlap()
    glyph.transform(psMat.scale(1, mag))
    ys_closepath(glyph)
    ys_rm_spikecontours(glyph, 0.15, 0.001, 10)
    ys_repair_spikes(glyph, 0.5)
    glyph.round()
    glyph.addExtrema("all")
    glyph.removeOverlap()
    glyph.transform(psMat.scale(1/mag, 1/mag))
    ys_closepath(glyph)
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    ys_repair_spikes(glyph, 0.5)
    glyph.round()
    glyph.addExtrema("all")
    glyph.removeOverlap()
    ys_rm_isolatepath(glyph)
    ys_rm_small_poly(glyph, 25, 25)
    glyph.addExtrema("all")



# 拡大縮小に伴う誤差でなおせないか試行錯誤してた頃のやつ
def ys_rescale_chain(glyph):
    forebackup = [contour.dup() for contour in glyph.foreground]

    if (glyph.validate(1) & 0x0FF) != 0:
        previous_flags = glyph.validate(1) & 0x0FF
        # 拡大方向に拡縮して直らないか
        ys_rescale(glyph, 12.5)
        current_flags = glyph.validate(1) & 0x0FF
        if ((previous_flags & ~current_flags) == 0 or  # フラグが降りてないか
            (~previous_flags & current_flags) != 0):  # むしろ新たに立ってる時
            ys_restore(glyph, forebackup)  # リセット

            # 拡大と単純化を組み合わせて直らないか
            ys_rescale_and_simplify(glyph, 12.5)
            current_flags = glyph.validate(1) & 0x0FF
            if ((previous_flags & ~current_flags) == 0 or
                (~previous_flags & current_flags) != 0):
                ys_restore(glyph, forebackup)  # リセット

                # 縮小を加えて直らないか
                ys_rescale(glyph, 0.2)
                current_flags = glyph.validate(1) & 0x0FF
                if ((previous_flags & ~current_flags) == 0 or
                    (~previous_flags & current_flags) != 0):
                    ys_restore(glyph, forebackup)  # リセット

                    # 縮小に拡大単純化加えて直らないか？
                    ys_rescale(glyph, 0.2)
                    ys_rescale_and_simplify(glyph, 8)
                    current_flags = glyph.validate(1) & 0x0FF
                    if ((previous_flags & ~current_flags) == 0 or
                        (~previous_flags & current_flags) != 0):

                        # 変化無しか、悪化する
                        ys_restore(glyph, forebackup)  # リセット



# 単純化による自己交差の除去試行
def ys_simplify(glyph):
    # 単純化の設定。ignoreextrema と setstarttoextremum を有効化
    flags = ["ignoreextrema", "setstarttoextremum", "removesingletonpoints"]  

    ys_rm_small_poly(glyph, 20, 20) # ごみ掃除関数
    # 自己交差したパスをNGパス変数にブチ込む(新規)
    ng_paths = [contour.dup() for contour in glyph.foreground if contour.selfIntersects()]
    # 自己交差してないパス(さっき保存できてないコンター)をOK変数にブチ込む(新規)
    ok_paths = [contour.dup() for contour in glyph.foreground if contour not in ng_paths]
    # フォアグラウンドをクリアして、NGパス変数に入れてたコンターを書き戻す
    glyph.foreground = fontforge.layer() # フォアグラウンドをクリア
    for contour in ng_paths:  # NGパスの書き戻し
        glyph.foreground += contour
        contour.addExtrema("all")
    glyph.foreground.simplify(0.05, flags)  # 単純化で治ればいいな
    ys_rm_small_poly(glyph, 25, 25) # ごみ掃除関数
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    ys_repair_spikes(glyph, 0.5)

    if glyph.validate(1) & 0x01:  # 開いたパスを検出
        ys_closepath(glyph)  # パスを閉じる

    # 自己交差したパスをNGパス変数にブチ込む(新規)
    ng_paths = [contour.dup() for contour in glyph.foreground if contour.selfIntersects()]
    # 自己交差してないパス(さっき保存できてないコンター)をOK変数にブチ込む(追記)
    ok_paths += [contour.dup() for contour in glyph.foreground if contour not in ng_paths]
    glyph.foreground = fontforge.layer() # まだ残ってるゴミはポイ。
    for contour in ok_paths:  # OKパスを書き戻す
        glyph.foreground += contour
        contour.addExtrema("all")
    
    # 単純化の参考。
    # [error_bound, flags, tan_bounds, linefixup, linelenmax]
    #"ignoreslopes",  # Allow slopes to change
    #"ignoreextrema",  # Allow removal of extrema
    #"smoothcurves",  # Allow curve smoothing
    #"choosehv",  # Snap to horizontal or vertical
    #"forcelines",  # flatten bumps on lines
    #"nearlyhvlines",  # Make nearly horizontal/vertical lines be so
    #"mergelines",  # Merge adjacent lines into one
    #"setstarttoextremum",  # Rotate the point list so that the start point is on an extremum
    #"removesingletonpoints",  # If the contour contains just one point then remove it



if __name__ == "__main__":
    main()
