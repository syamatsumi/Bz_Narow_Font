#!fontforge --lang=py -script

import fontforge

from .ys_fontforge_Remove_artifacts import ys_closepath, ys_rm_spikecontours, ys_rm_isolatepath, ys_rm_small_poly
from .ys_fontforge_Repair_Self_Intersections import ys_repair_Self_Insec

def ys_repair_si_chain(glyph, proc_cnt):
    if glyph.validate(1) & 0x01:  # 開いたパスを検出
        print(f"now:{glyph.glyphname:<15} {'Anomality Repair cntclose':<48}\r", end=" ", flush=True)
        ys_closepath(glyph)  # パスを閉じる＆その他処理
    ys_rm_isolatepath(glyph)  # 孤立したゴミパスを削除
    
    mode = f"{glyph.validate(1):x}"

    # 処理戻し用のバックアップを取得
    glyph.round()  # 整数化
    stroke_backup = [contour.dup() for contour in glyph.foreground]

    if (glyph.validate(1) & 0x0FF) != 0 and (glyph.validate(1) & 0x0FF) != 0x04:
        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Anomality Repair 1 mode'f'{mode}':<48}\r", end=" ", flush=True)
        previous_flags = glyph.validate(1) & 0x0FF
        ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
        ys_repair_Self_Insec(glyph, 1)
        glyph.round()
        glyph.removeOverlap()
        glyph.addExtrema("all")
        ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
        ys_repair_Self_Insec(glyph, 1)
        glyph.round()
        glyph.removeOverlap()
        glyph.addExtrema("all")
        ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
        ys_rm_small_poly(glyph, 25, 25)
        glyph.addExtrema("all")
        current_flags = glyph.validate(1) & 0x0FF
        if ((previous_flags & ~current_flags) == 0 or
            (~previous_flags & current_flags) != 0):  # フラグが降りてないか、むしろ立ってる時
            print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Anomality Repair 2 mode'f'{mode}':<48}\r", end=" ", flush=True)
            previous_flags = glyph.validate(1) & 0x0FF
            glyph.foreground = fontforge.layer()
            for contour in stroke_backup:
                glyph.foreground += contour
            ys_rm_spikecontours(glyph, 0.11, 0.001, 10)
            ys_repair_Self_Insec(glyph, 3)
            glyph.round()
            glyph.removeOverlap()
            glyph.addExtrema("all")
            ys_rm_spikecontours(glyph, 0.11, 0.001, 10)
            ys_repair_Self_Insec(glyph, 3)
            glyph.round()
            glyph.removeOverlap()
            glyph.addExtrema("all")
            ys_rm_spikecontours(glyph, 0.11, 0.001, 10)
            ys_rm_small_poly(glyph, 25, 25)
            glyph.addExtrema("all")
            current_flags = glyph.validate(1) & 0x0FF
            if ((previous_flags & ~current_flags) == 0 or
                (~previous_flags & current_flags) != 0):  # フラグが降りてないか、むしろ立ってる時
                print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Anomality Repair 3 mode'f'{mode}':<48}\r", end=" ", flush=True)
                previous_flags = glyph.validate(1) & 0x0FF
                glyph.foreground = fontforge.layer()
                for contour in stroke_backup:
                    glyph.foreground += contour
                ys_rm_spikecontours(glyph, 0.12, 0.001, 10)
                ys_repair_Self_Insec(glyph, 4)
                glyph.round()
                glyph.removeOverlap()
                glyph.addExtrema("all")
                ys_rm_spikecontours(glyph, 0.12, 0.001, 10)
                ys_repair_Self_Insec(glyph, 4)
                glyph.round()
                glyph.removeOverlap()
                glyph.addExtrema("all")
                ys_rm_spikecontours(glyph, 0.12, 0.001, 10)
                ys_rm_small_poly(glyph, 25, 25)
                glyph.addExtrema("all")
                current_flags = glyph.validate(1) & 0x0FF
                if ((previous_flags & ~current_flags) == 0 or
                    (~previous_flags & current_flags) != 0):  # フラグが降りてないか、むしろ立ってる時
                    print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Anomality Repair 4 mode'f'{mode}':<48}\r", end=" ", flush=True)
                    previous_flags = glyph.validate(1) & 0x0FF
                    glyph.foreground = fontforge.layer()
                    for contour in stroke_backup:
                        glyph.foreground += contour
                    ys_rm_spikecontours(glyph, 0.13, 0.001, 10)
                    ys_repair_Self_Insec(glyph, 5)
                    glyph.round()
                    glyph.removeOverlap()
                    glyph.addExtrema("all")
                    ys_rm_spikecontours(glyph, 0.13, 0.001, 10)
                    ys_repair_Self_Insec(glyph, 5)
                    glyph.round()
                    glyph.removeOverlap()
                    glyph.addExtrema("all")
                    ys_rm_spikecontours(glyph, 0.13, 0.001, 10)
                    ys_rm_small_poly(glyph, 25, 25)
                    glyph.addExtrema("all")
                    current_flags = glyph.validate(1) & 0x0FF
                    if ((previous_flags & ~current_flags) == 0 or
                        (~previous_flags & current_flags) != 0):  # フラグが降りてないか、むしろ立ってる時
                        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Anomality Repair 5 mode'f'{mode}':<48}\r", end=" ", flush=True)
                        previous_flags = glyph.validate(1) & 0x0FF
                        glyph.foreground = fontforge.layer()
                        for contour in stroke_backup:
                            glyph.foreground += contour
                        ys_rm_spikecontours(glyph, 0.14, 0.001, 10)
                        ys_repair_Self_Insec(glyph, 6)
                        glyph.round()
                        glyph.removeOverlap()
                        glyph.addExtrema("all")
                        ys_rm_spikecontours(glyph, 0.14, 0.001, 10)
                        ys_repair_Self_Insec(glyph, 6)
                        glyph.round()
                        glyph.removeOverlap()
                        glyph.addExtrema("all")
                        ys_rm_spikecontours(glyph, 0.14, 0.001, 10)
                        ys_rm_small_poly(glyph, 25, 25)
                        glyph.addExtrema("all")
                        current_flags = glyph.validate(1) & 0x0FF
                        if ((previous_flags & ~current_flags) == 0 or
                            (~previous_flags & current_flags) != 0):  # フラグが降りてないか、むしろ立ってる時
                            print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Repair failure, rollback.':<48}\r", end=" ", flush=True)
                            glyph.foreground = fontforge.layer() # フォアグラウンドをクリア
                            for contour in stroke_backup:  # 保存していたパスの書き戻し
                                glyph.foreground += contour  # 修復試行前に戻す
                            ys_rm_spikecontours(glyph, 0.15, 0.001, 10)
                            ys_repair_Self_Insec(glyph, 2)
                            glyph.round()
                            glyph.removeOverlap()
                            glyph.addExtrema("all")
                            ys_rm_spikecontours(glyph, 0.15, 0.001, 10)
                            ys_repair_Self_Insec(glyph, 2)
                            glyph.round()
                            glyph.removeOverlap()
                            glyph.addExtrema("all")
                            ys_rm_spikecontours(glyph, 0.15, 0.001, 10)
                            ys_rm_small_poly(glyph, 25, 25)
                            glyph.addExtrema("all")
    # 異常がなければ何もおきないハズの処理。
    else:
        ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
        ys_repair_Self_Insec(glyph, 2)
        glyph.round()
        glyph.removeOverlap()
        glyph.addExtrema("all")
        ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
        ys_repair_Self_Insec(glyph, 2)
        glyph.round()
        glyph.removeOverlap()
        glyph.addExtrema("all")
        ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
        ys_rm_small_poly(glyph, 25, 25)
        glyph.addExtrema("all")



# 拡大縮小に伴う誤差でなおせないか試行錯誤してた頃のやつ
def ys_rescale_chain(glyph):
    glyph_backup = [contour.dup() for contour in glyph.foreground]

    if (glyph.validate(1) & 0x0FF) != 0 and (glyph.validate(1) & 0x0FF) != 0x04:
        previous_flags = glyph.validate(1) & 0x0FF
        glyph.transform((0.2, 0, 0, 1, 0, 0))
        glyph.round()  # 整数化
        glyph.addExtrema("all") # 極点を追加
        glyph.removeOverlap()  # 結合
        glyph.transform((5, 0, 0, 0.2, 0, 0))
        glyph.round()  # 整数化
        glyph.addExtrema("all") # 極点を追加
        glyph.removeOverlap()  # 結合
        glyph.transform((0.2, 0, 0, 1, 0, 0))
        glyph.round()  # 整数化
        glyph.addExtrema("all") # 極点を追加
        glyph.removeOverlap()  # 結合
        glyph.transform((5, 0, 0, 5, 0, 0))
        ys_repair_Self_Insec(glyph, 2)
        glyph.removeOverlap()  # 結合
        ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
        ys_rm_isolatepath(glyph)
        ys_rm_small_poly(glyph, 25, 25)
        glyph.addExtrema("all")
        current_flags = glyph.validate(1) & 0x0FF
        if ((previous_flags & ~current_flags) == 0 or
            (~previous_flags & current_flags) != 0):
            # フラグが降りてないか、むしろ立ってる時は次の悪足掻き
            glyph.foreground = fontforge.layer() # フォアグラウンドをクリア
            for contour in glyph_backup:  # 保存していたパスの書き戻し
                glyph.foreground += contour  # 修復試行前に戻す
            previous_flags = glyph.validate(1) & 0x0FF
            glyph.transform((1, 0, 0, 12.5, 0, 0))
            ys_simplify(glyph)  # 単純化試行
            ys_closepath(glyph)  # 開いたパスの修正
            glyph.round()  # 整数化
            glyph.addExtrema("all") # 極点を追加
            glyph.removeOverlap()  # 結合
            glyph.transform((12.5, 0, 0, 0.08, 0, 0))
            ys_simplify(glyph)  # 単純化試行
            ys_closepath(glyph)  # 開いたパスの修正
            glyph.round()  # 整数化
            glyph.addExtrema("all") # 極点を追加
            glyph.removeOverlap()  # 結合
            glyph.transform((1, 0, 0, 12.5, 0, 0))
            ys_closepath(glyph)  # 開いたパスの修正
            glyph.round()  # 整数化
            glyph.addExtrema("all") # 極点を追加
            glyph.removeOverlap()  # 結合
            glyph.transform((0.08, 0, 0, 0.08, 0, 0))
            ys_repair_Self_Insec(glyph, 2)
            glyph.removeOverlap()  # 結合
            ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
            ys_rm_isolatepath(glyph)
            ys_rm_small_poly(glyph, 25, 25)
            glyph.addExtrema("all")
            current_flags = glyph.validate(1) & 0x0FF
            if ((previous_flags & ~current_flags) == 0 or
                (~previous_flags & current_flags) != 0):
                # フラグが降りてないか、むしろ立ってる時はさらに次の悪足掻き
                glyph.foreground = fontforge.layer() # フォアグラウンドをクリア
                for contour in glyph_backup:  # 保存していたパスの書き戻し
                    glyph.foreground += contour  # 修復試行前に戻す
                previous_flags = glyph.validate(1) & 0x0FF
                glyph.transform((0.25, 0, 0, 1, 0, 0))
                glyph.round()  # 整数化
                glyph.addExtrema("all") # 極点を追加
                glyph.removeOverlap()  # 結合
                glyph.transform((4, 0, 0, 0.25, 0, 0))
                glyph.round()  # 整数化
                glyph.addExtrema("all") # 極点を追加
                glyph.removeOverlap()  # 結合
                glyph.transform((0.25, 0, 0, 1, 0, 0))
                glyph.round()  # 整数化
                glyph.addExtrema("all") # 極点を追加
                glyph.removeOverlap()  # 結合
                glyph.transform((4, 0, 0, 32, 0, 0))
                ys_simplify(glyph)  # 単純化試行
                ys_closepath(glyph)  # 開いたパスの修正
                glyph.round()  # 整数化
                glyph.addExtrema("all") # 極点を追加
                glyph.removeOverlap()  # 結合
                glyph.transform((8, 0, 0, 1, 0, 0))
                ys_simplify(glyph)  # 単純化試行
                ys_closepath(glyph)  # 開いたパスの修正
                glyph.round()  # 整数化
                glyph.addExtrema("all") # 極点を追加
                glyph.removeOverlap()  # 結合
                glyph.transform((1, 0, 0, 0.125, 0, 0))
                ys_simplify(glyph)  # 単純化試行
                ys_closepath(glyph)  # 開いたパスの修正
                glyph.round()  # 整数化
                glyph.addExtrema("all") # 極点を追加
                glyph.removeOverlap()  # 結合
                glyph.transform((0.125, 0, 0, 1, 0, 0))
                ys_repair_Self_Insec(glyph, 2)
                glyph.removeOverlap()  # 結合
                ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
                ys_rm_isolatepath(glyph)
                ys_rm_small_poly(glyph, 25, 25)
                glyph.addExtrema("all")
                current_flags = glyph.validate(1) & 0x0FF
                if ((previous_flags & ~current_flags) == 0 or
                    (~previous_flags & current_flags) != 0):
                    # フラグが降りてないか、むしろ立ってる時はあきらめる
                    glyph.foreground = fontforge.layer() # フォアグラウンドをクリア
                    for contour in glyph_backup:  # 保存していたパスの書き戻し
                        glyph.foreground += contour  # 修復試行前に戻す



# 単純化による自己交差の除去試行
def ys_simplify(glyph):
    # 単純化の設定。ignoreextrema と setstarttoextremum を有効化
    flags = ["ignoreextrema", "setstarttoextremum", "smoothcurves", "mergelines", "removesingletonpoints"]  

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
    glyph.simplify(0.05, flags)  # 単純化で治ればいいな
    ys_rm_small_poly(glyph, 25, 25) # ごみ掃除関数
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    
    for contour in glyph.foreground:# この操作で開いたパスを閉じる操作
        if not contour.closed:  # 開いたパスかどうかを確認
            contour.addExtrema("all")
            contour.closed = True  # 強制的に閉じる

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
