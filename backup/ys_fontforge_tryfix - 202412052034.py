#!fontforge --lang=py -script

import fontforge

from .ys_fontforge_Remove_artifacts import ys_rm_little_line, ys_rm_small_poly
from .ys_fontforge_Repair_Self_Intersections import ys_repair_Self_Insec

# 開いたパスを閉じて、閉じられないパスを捨てる関数
def ys_closepath(glyph):
    # パスが閉じられたコンターをOKパス変数にブチ込む、
    ok_paths = [contour.dup() for contour in glyph.foreground if contour.closed]
    # パスが開いたコンター(さっき保存できてないコンター)をNG変数にブチ込む
    ng_paths = [contour.dup() for contour in glyph.foreground if contour not in ok_paths]
    # フォアグラウンドをクリアして、NGパス変数に入れてたコンターを書き戻す
    glyph.foreground = fontforge.layer() # フォアグラウンドをクリア
    for contour in ng_paths:  # NGパスの書き戻し
        glyph.foreground += contour
    # 開いたパスを閉じる操作
    for contour in glyph.foreground:
        contour.addExtrema("all")
        contour.closed = True  # 強制的に閉じる

    # 強制的に閉じることができたパスをOKパス変数にブチ込む、
    ok_paths += [contour.dup() for contour in glyph.foreground if contour.closed]
    glyph.foreground = fontforge.layer()  # まだ残ってるゴミは諦めてポイ。
    for contour in ok_paths:  # OKパスを書き戻す
        glyph.foreground += contour
    
    glyph.addExtrema("all")



def ys_repair_si_chain(glyph, proc_cnt):
    if glyph.validate(1) & 0x01:  # 開いたパスを検出
        print(f"\r now:{glyph.glyphname:<15} Anomality Repair cntclose \r", end=" ", flush=True)
        ys_closepath(glyph)  # パスを閉じる＆その他処理
    ys_rm_little_line(glyph)  # 2点で構成されたパス(ゴミ)を削除

    # 処理戻し用のバックアップを取得
    glyph.round()  # 整数化
    stroke_backup = [contour.dup() for contour in glyph.foreground]

    if glyph.validate(1) & 0x20:  # 自己交差がある
        print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Anomality Repair 1        \r", end=" ", flush=True)
        ys_repair_Self_Insec(glyph, 1)
        glyph.round()
        glyph.removeOverlap()

        if glyph.validate(1) & 0x20:
            print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Anomality Repair 2        \r", end=" ", flush=True)
            glyph.foreground = fontforge.layer()
            for contour in stroke_backup:
                glyph.foreground += contour
            ys_repair_Self_Insec(glyph, 3)
            glyph.round()
            glyph.removeOverlap()

            if glyph.validate(1) & 0x20:
                print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Anomality Repair 3        \r", end=" ", flush=True)
                glyph.foreground = fontforge.layer()
                for contour in stroke_backup:
                    glyph.foreground += contour
                ys_repair_Self_Insec(glyph, 4)
                glyph.round()
                glyph.removeOverlap()

                if glyph.validate(1) & 0x20:
                    print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Anomality Repair 4        \r", end=" ", flush=True)
                    glyph.foreground = fontforge.layer()
                    for contour in stroke_backup:
                        glyph.foreground += contour
                    ys_repair_Self_Insec(glyph, 5)
                    glyph.round()
                    glyph.removeOverlap()

                    if glyph.validate(1) & 0x20:
                        print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Anomality Repair 5        \r", end=" ", flush=True)
                        glyph.foreground = fontforge.layer()
                        for contour in stroke_backup:
                            glyph.foreground += contour
                        ys_repair_Self_Insec(glyph, 6)
                        glyph.round()
                        glyph.removeOverlap()

                        if glyph.validate(1) & 0x20:
                            print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Repair failure, rollback. \r", end=" ", flush=True)
                            glyph.foreground = fontforge.layer() # フォアグラウンドをクリア
                            for contour in stroke_backup:  # 保存していたパスの書き戻し
                                glyph.foreground += contour  # 修復試行前に戻す
                            ys_repair_Self_Insec(glyph, 2)
                            glyph.round()
                            glyph.removeOverlap()
    else:
        ys_repair_Self_Insec(glyph, 2)
        glyph.round()
        glyph.removeOverlap()


# 拡大縮小に伴う誤差でなおせないか試行錯誤してた頃のやつ
def ys_rescale_chain(glyph):
    glyph_backup = [contour.dup() for contour in glyph.foreground]

    if glyph.validate(1) != 0:  # どれか一つでも引っかかった場合
        previous_flags = glyph.validate(1)
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
        current_flags = glyph.validate(1)
        if (previous_flags & ~current_flags) != 0:  # フラグが「落ちた」場合
            pass  # 何かしらの改善が見られたので終了。
        else:
            glyph.foreground = fontforge.layer() # フォアグラウンドをクリア
            for contour in glyph_backup:  # 保存していたパスの書き戻し
                glyph.foreground += contour  # 修復試行前に戻す

        # 次の悪足掻き
            previous_flags = glyph.validate(1)
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
            current_flags = glyph.validate(1)
            if (previous_flags & ~current_flags) != 0:  # フラグが「落ちた」場合
                pass  # 何かしらの改善が見られたので終了。
            else:
                glyph.foreground = fontforge.layer() # フォアグラウンドをクリア
                for contour in glyph_backup:  # 保存していたパスの書き戻し
                    glyph.foreground += contour  # 修復試行前に戻す
            # さらに次の悪足掻き
                previous_flags = glyph.validate(1)
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
                current_flags = glyph.validate(1)
                if (previous_flags & ~current_flags) != 0:  # フラグが「落ちた」場合
                    pass  # 何かしらの改善が見られたので終了。
                else:
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
    ys_rm_small_poly(glyph, 20, 20) # ごみ掃除関数
    
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
