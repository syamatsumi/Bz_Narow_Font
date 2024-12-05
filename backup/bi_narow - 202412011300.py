#!fontforge --lang=py -script
import configparser
import logging
import os
import sys

import fontforge
import psMat

from utils import ys_repair_Self_Insec, ys_rm_little_line, ys_rm_small_poly
from utils import ys_closepath, ys_simplify, ys_rescale_chain, ys_widestroke
from bi_narow_set import shorten_style_rd, write_property

# コマンドライン引数の処理
if len(sys.argv) < 4:
    print("Usage: script.py <input_fontstyles> <output_name> <vshrink_ratio>", flush=True)
    sys.exit(1)    
try:
    INPUT_FONTSTYLES = sys.argv[1]  # 入力ファイル
    OUTPUT_NAME = sys.argv[2]  # 出力ファイル
    # OUTPUT_NAME = f"{OUTPUT_NAME}"  # 出力ファイルの形式 ゴミかも？　あとで消す。
    VSHRINK_RATIO = float(sys.argv[3])  # 横に縮める比率（数値に変換）
except ValueError:
    print("Error: <stroke_width> and <VSHRINK_RATIO> must be numbers.", flush=True)
    sys.exit(1)

# カレントディレクトリを保存する
current_dir = os.getcwd()

# 一旦、情報収集のためにスクリプトの場所をカレントディレクトリに設定する。
this_script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_script_dir)

# 設定ファイルの名前は自分の名前の拡張子違い
this_script_name = os.path.basename(__file__)  # 現在のスクリプト名を取得
ini_name = os.path.splitext(this_script_name)[0] + ".ini"  # 拡張子を .ini に変更
ini_path = os.path.join(this_script_dir, ini_name)

# 設定ファイルを読み込む
settings = configparser.ConfigParser()
settings.read(ini_path, encoding="utf-8")

SOURCE_FONTS_DIR = settings.get("DEFAULT", "Source_Fonts_Dir")
BUILD_FONTS_DIR  = settings.get("DEFAULT", "Build_Fonts_Dir")
STROKE_WIDTH_SF  = float(settings.get("DEFAULT", "Stroke_Width_SF"))
STROKE_WIDTH_MIN = float(settings.get("DEFAULT", "Stroke_Width_Min"))
STOROKE_HEIGHT   = float(settings.get("DEFAULT", "Storoke_Height"))
STRWR_WEIGHT_HI  = float(settings.get("DEFAULT", "StrWR_Weight_Hi"))
STRWR_WEIGHT_LO  = float(settings.get("DEFAULT", "StrWR_Weight_Lo"))
STRWR_POINTS_HI  = float(settings.get("DEFAULT", "StrWR_Points_Hi"))
STRWR_POINTS_LO  = float(settings.get("DEFAULT", "StrWR_Points_Lo"))
REDUCE_RATIO_HI  = float(settings.get("DEFAULT", "Reduce_Ratio_Hi"))
REDUCE_RATIO_LO  = float(settings.get("DEFAULT", "Reduce_Ratio_Lo"))

PRESAVE_INTERVAL = int(settings.get("DEFAULT", "Presave_Interval"))
IS_PROPORTIONAL_CUTOFF_VARIANCE = int(settings.get("DEFAULT", "is_proportional_cutoff_variance"))
PROPOTIONAL_SIDEBEARING_DIVISOR  = float(settings.get("DEFAULT", "propotional_sidebearing_divisor"))

# main関数内でlocal_setup_logger(OUTPUT_NAME) 使って設定。
logger = logging.getLogger()



######################################################################
#                             メイン関数                             #
######################################################################
def main():
    logger = local_setup_logger(OUTPUT_NAME)  # ログ出力の設定

    # 作業用のディレクトリを作成
    os.makedirs(BUILD_FONTS_DIR, exist_ok=True)

# 読み込むフォントのディレクトリまで確定させる
     # 必要なのは最初の値だけ。
    input_fontname = shorten_style_rd(INPUT_FONTSTYLES)[0]
    input_fontfile = os.path.join(SOURCE_FONTS_DIR, input_fontname)
    print (input_fontfile)
    font = fontforge.open(input_fontfile)  # フォントを開く

    #一通り情報を集め終わったので元のカレントディレクトリに戻る
    os.chdir(current_dir)

# SFDに変換して一旦TTFを閉じる
    temp_file = f"{OUTPUT_NAME}_temp_0.sfd"
    temp_file_path = os.path.join(BUILD_FONTS_DIR, temp_file)
    
    del_file = temp_file  # あとで消す時用
    font.save(temp_file_path)
    print(f"SFDに変更して再開する。file: {temp_file_path}", flush=True)
    font.close() # TTFフォントを閉じる

# SFDで保存した一時ファイルを開き直す
    font = fontforge.open(temp_file_path)
    print(f"SFDを開きなおした。 file: {temp_file_path}", flush=True)

# この時点でフォントのプロパティを書き換えておく
    write_property(ini_name, INPUT_FONTSTYLES, VSHRINK_RATIO, font)

# 標準出力が狂うかもなので一応初期化。
    sys.stdout = sys.__stdout__

# ASCII範囲に基づいてフォントがプロポーショナルかを判定
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

# メインのループ前にフォントの元情報を把握
    font_weight = font.os2_weight
    em_size = font.em

# ストローク幅のセッティング
    base_stroke_width = STROKE_WIDTH_MIN + STROKE_WIDTH_SF * (1 - VSHRINK_RATIO)

# カウンタをセット
    proc_cnt: int = 0



######################################################################
#                    ここから各グリフをループ処理                    #
######################################################################

    # 全グリフに変形処理を適用
    for glyph in font.glyphs():
        if not glyph.isWorthOutputting():
            continue  # 出力しないグリフはスキップ
        if len(glyph.references) > 0:
            print(f"合成グリフをスキップ： {glyph.glyphname}", flush=True)
            continue  # コンポジットグリフはスキップ
    
        proc_cnt += 1
        del_file = Local_snapshot_sfd(PRESAVE_INTERVAL, proc_cnt, del_file, OUTPUT_NAME, font, glyph)
        sys.stdout = sys.__stdout__  # 念の為標準出力をリセットしておく
            
    # グリフ幅がジャスト半分ならそのことを覚えておく
        if glyph.width ==  em_size / 2:
            halfwidth_glyph_flag = True
        else :
            halfwidth_glyph_flag = False
    
    # フォントウエイトと確認中グリフのポイント数を勘案してストロークの幅を変える
        point_count = sum(len(contour) for contour in glyph.layers[glyph.activeLayer])
        if point_count > STRWR_POINTS_HI or font_weight > STRWR_WEIGHT_HI:
            stroke_width = round(base_stroke_width * REDUCE_RATIO_HI)
        elif point_count > STRWR_POINTS_LO and font_weight > STRWR_WEIGHT_LO:
            stroke_width = round(base_stroke_width * REDUCE_RATIO_LO)
        else :
            stroke_width = base_stroke_width

    # 元のグリフを背面で保護(デバッグ用)
        # glyph.background = glyph.foreground

    # 縦に拡大する
        glyph.transform((1, 0, 0, 16, 0, 0))  # 縦に伸ばす
        glyph.addExtrema("all") # 極点を追加

    # 拡幅処理
        ys_widestroke(stroke_width, STOROKE_HEIGHT, glyph)

    # 幅を縮小＆最初に縦に伸ばした奴を元に戻す
        glyph.transform((1, 0, 0, 0.0625, 0, 0))
        glyph.addExtrema("all") # 極点を追加

    # 修復を試みる
        glyph.round()  # 整数化
        glyph.addExtrema("all") # 極点を追加
        glyph.removeOverlap()  # 結合
        glyph.addExtrema("all") # 極点を追加
        if glyph.validate(1) & 0x01:  # 開いたパスがある場合
            ys_closepath(glyph)
        if glyph.validate(1) != 0:  # どれか一つでも引っかかった場合
            glyph.simplify(0.01) # 単純化
        glyph.round()  # 整数化
        glyph.addExtrema("all") # 極点を追加
        glyph.removeOverlap()  # 結合
        glyph.addExtrema("all") # 極点を追加

    # 変形、精度劣化を伴う修復試行を行う。
        if glyph.validate(1) != 0:  # どれか一つでも引っかかった場合
            ys_rescale_chain(glyph)

    # 幅のストロークで太ったアウトラインを引き締める。
    # サイドベアリングを弄りたくないので拡大縮小の原点はグリフの中心にする。
    # グリフの幅まで変わると困るのでレイヤー単位で操作
        glyph.addExtrema("all") # 極点を追加
        bbox = glyph.boundingBox()
        xmin, ymin, xmax, ymax = bbox
        xcenter = xmin + (xmax - xmin) / 2
        stroke_shrink = 1 - (stroke_width / em_size)
        glyph.foreground.transform((1, 0, 0, 1, -xcenter, 0))
        glyph.foreground.transform((stroke_shrink, 0, 0, 1, 0, 0))
        glyph.foreground.transform((1, 0, 0, 1, xcenter, 0))

    # 指定の縮小率に従って縦横比変更
        glyph.transform((VSHRINK_RATIO, 0, 0, 1, 0, 0))
        glyph.addExtrema("all") # 極点を追加

    # 等幅フォントのグリフ幅を設定する
        if halfwidth_glyph_flag and not style_is_prop:
            glyph.width = round(em_size / 2 * VSHRINK_RATIO)
        else:
            glyph.width = round(em_size * VSHRINK_RATIO)
    
    # プロポーショナルフォント幅を設定する。
    # サイドベアリングがemサイズの1/SIDEBEARING_DIVISOR以上なら、それ以下に縮める。
    # スペースみたいなコンターの無いグリフは元に戻す。
        if style_is_prop:
            glyph.round()  # 整数化
            originalwidth = glyph.width  # スペースとかのために縮める前の幅を確保
            glyph.addExtrema("all") # 極点を追加
            glyph.removeOverlap()  # 結合
            glyph.addExtrema("all") # 極点を追加
            bbox = glyph.boundingBox()
            xmin, ymin, xmax, ymax = bbox
            maxbear = em_size / PROPOTIONAL_SIDEBEARING_DIVISOR
            if xmin < maxbear:
                glyph.transform(psMat.translate(maxbear - xmin, 0))
            glyph.addExtrema("all") # 極点を追加
            bbox = glyph.boundingBox()
            xmin, ymin, xmax, ymax = bbox
            glyph.width = round(xmax + maxbear) # グリフ幅を拡縮
            
            if glyph.width == maxbear * 2:
                glyph.width = originalwidth

    # 最後にTTFの仕様に合わせた最適化を実施
        if glyph.validate(1) != 0:  # どれか一つでも引っかかった場合
            glyph.simplify(0.01) # 単純化
        glyph.addExtrema("all") # 極点を追加
        if glyph.validate(1) & 0x01:  # 開いたパスがある場合
            ys_closepath(glyph)
        glyph.round()  # 整数化
        if glyph.validate(1) & 0x20:  # 自己交差がある場合
            ys_repair_Self_Insec(glyph, 2)
        glyph.addExtrema("all") # 極点を追加
        glyph.removeOverlap()  # 結合
        glyph.round()  # 整数化
        glyph.addExtrema("all") # 極点を追加
        glyph.background = fontforge.layer()  # デバッグの時はコメントアウト

        # 仕上げ後の検査(デバッグ用)
        Local_validate_notice("仕上げ処理後", "warning", glyph)
        print(f"\r done:{proc_cnt:<5}:{glyph.glyphname:<15}", end=" ", flush=True)

######################################################################
#                    各グリフのループ処理ここまで                    #
######################################################################

    try:
        # SFDファイルの保存
        output_sfd = f"{OUTPUT_NAME}.sfd"
        output_sfd_path = os.path.join(BUILD_FONTS_DIR, output_sfd)
        print(f"完成したフォントを保存： {output_sfd_path}", flush=True)
        font.save(output_sfd_path)  # SFD形式で保存
        
        # TTFファイルの保存
        output_ttf = f"{OUTPUT_NAME}.ttf"
        output_ttf_path = os.path.join(BUILD_FONTS_DIR, output_ttf)
        print(f"完成したフォントを保存： {output_ttf_path}", flush=True)
        font.generate(output_ttf_path)  # TTF形式で保存

        # TTFファイルを開き直し
        print(f"TTFに変更して再開する。file:{output_ttf_path}", flush=True)
        font.close() # SFDフォントを閉じる
        import time  # 書き込みが完了するまで少し待つ
        time.sleep(0.1)
        font = fontforge.open(output_ttf_path) # TTFを開きなおす
        print(f"TTFを開きなおした。 file: {output_ttf_path}", flush=True)
        sys.stdout = sys.__stdout__

        # 最後に全グリフを一斉に見直し
        for glyph in font.glyphs():
            if not glyph.isWorthOutputting():
                continue  # 出力しないグリフはスキップ
            if len(glyph.references) > 0:
                print(f"合成グリフをスキップ： {glyph.glyphname}", flush=True)
                continue  # コンポジットグリフはスキップ
            Local_validate_notice("最終チェック", "warning", glyph)

    except IOError as e:
        print(f"保存に失敗しました: {e}")
    else:
        if del_file != f"temp_0_{OUTPUT_NAME}.sfd":
            del_file_path = os.path.join(BUILD_FONTS_DIR, del_file)
            print(f"前の一時ファイルを削除： {del_file_path}", flush=True)
            os.remove(del_file_path)
    
    font.close()
    #print("処理が完了しました。Enterを押して待機状態を終了しましょう。")
    #input()  # ユーザーがEnterを押すまで待機

# def main():ここまで。



######################################################################
#                                                                    #
#                         以降はローカル関数                         #
#                                                                    #
######################################################################

def Local_snapshot_sfd (savefreq, proc_cnt, del_file, OUTPUT_NAME, font, glyph):
# savefreq個処理してたら一旦保存
    if proc_cnt % savefreq == 1:
        print(f"作業前保存中のグリフ： {glyph.glyphname}", flush=True)
        temp_file = f"{OUTPUT_NAME}_temp_{proc_cnt}.sfd"
        temp_file_path = os.path.join(BUILD_FONTS_DIR, temp_file)
        font.save(temp_file_path)
    # 前回の仮保存ファイルを削除
        print(f"前の一時ファイルを削除： {del_file}", flush=True)
        del_file_path = os.path.join(BUILD_FONTS_DIR, del_file)
        os.remove(del_file_path)
    # 次の削除対象ファイル名を保存
        del_file = temp_file
    # ついでにログもフラッシュしておく。
        for handler in logging.getLogger().handlers:
            if hasattr(handler, 'flush'):
                handler.flush()
    return del_file



def Local_validate_notice(note, loglevel, glyph):
    log_func = getattr(logger, loglevel, None)  # 動的にログレベルを取得

    if glyph.validate(1) & 0x01:  # 開いたパスがある場合
        log_func(f"{note}のグリフ '{glyph.glyphname}' に開いたパスがあります。")
    if glyph.validate(1) & 0x02:  # 時計回りじゃないパスがある
        logger.info(f"{note}のグリフ '{glyph.glyphname}' の外側に時計回りのパスがあるそうよ。")
    if glyph.validate(1) & 0x04:  # 交差がある場合
        logger.info(f"{note}のグリフ '{glyph.glyphname}' に交差があるそうよ。")
    if glyph.validate(1) & 0x08:  # 参照が不正
        logger.info(f"{note}のグリフ '{glyph.glyphname}' の参照が不正ですって。")
    if glyph.validate(1) & 0x10:  # ヒントが不正
        logger.info(f"{note}のグリフ '{glyph.glyphname}' のヒントが不正らしいわ。")
    if glyph.validate(1) & 0x20:  # 自己交差がある場合
        log_func(f"{note}のグリフ '{glyph.glyphname}' に自己交差があるらしいわ。")
    if glyph.validate(1) & 0x40:  # 交差がある場合
        log_func(f"{note}後のグリフ '{glyph.glyphname}' にその他のエラーだって。")   



def local_setup_logger(OUTPUT_NAME):
    global logger  # グローバルでロガーの設定をする。

    logger = logging.getLogger("custom_logger")
    logger.setLevel(logging.DEBUG)  # 全てのログを記録対象にする

    # ログファイルの記録先
    Log_file_path = os.path.join(BUILD_FONTS_DIR, f"{OUTPUT_NAME}.log")

    # ファイルハンドラ: WARNING以上をファイルに記録
    file_handler = logging.FileHandler(Log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
    logger.addHandler(file_handler)

    # コンソールハンドラ: INFO以下を通常出力（標準出力）
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.addFilter(lambda record: record.levelno < logging.WARNING)
    stdout_handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
    logger.addHandler(stdout_handler)

    # コンソールハンドラ: WARNING以上をエラー出力（標準エラー出力）
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
    logger.addHandler(stderr_handler)

    return logger



if __name__ == "__main__":
    main()
