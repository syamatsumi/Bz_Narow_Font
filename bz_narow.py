#!fontforge --lang=py -script
import configparser
import logging
import os
import sys
import gc

import fontforge
import psMat
import math

from utils import ys_closepath, ys_repair_Self_Insec, ys_rm_spikecontours
from utils import ys_rm_little_line, ys_rm_small_poly
from utils import ys_repair_si_chain, ys_rescale_chain, ys_simplify
from utils import ys_widestroke, ys_blacklist, ys_whitelist, ys_ignorlist
from bz_narow_set import shorten_style_rd, write_property




# コマンドライン引数の処理
if len(sys.argv) < 4:
    print("Usage: script.py <input_fontstyles> <output_name> <vshrink_ratio>", flush=True)
    sys.exit(1)    
try:
    INPUT_FONTSTYLES = sys.argv[1]  # 入力ファイル
    OUTPUT_NAME = sys.argv[2]  # 出力ファイル
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

FFSCR = settings.get("DEFAULT", "ffscr")
SOURCE_FONTS_DIR = settings.get("DEFAULT", "Source_Fonts_Dir")
BUILD_FONTS_DIR  = settings.get("DEFAULT", "Build_Fonts_Dir")
STROKE_WIDTH_SF  = float(settings.get("DEFAULT", "Stroke_Width_SF"))
STROKE_WIDTH_MIN = float(settings.get("DEFAULT", "Stroke_Width_Min"))
STOROKE_HEIGHT   = float(settings.get("DEFAULT", "Storoke_Height"))
STRWR_WEIGHT = float(settings.get("DEFAULT", "StrWR_Weight"))
STRWR_POINTS = float(settings.get("DEFAULT", "StrWR_Points"))
REDUCE_RATIO = float(settings.get("DEFAULT", "Reduce_Ratio"))

PRESAVE_INTERVAL = int(settings.get("DEFAULT", "Presave_Interval"))
IS_PROPORTIONAL_CUTOFF_VARIANCE = int(settings.get("DEFAULT", "is_proportional_cutoff_variance"))
PROPOTIONAL_SIDEBEARING_DIVISOR  = float(settings.get("DEFAULT", "propotional_sidebearing_divisor"))

# main関数内でlocal_setup_logger(OUTPUT_NAME) 使って設定。
logger = logging.getLogger()

# 書き込みをロガーに転送するクラス。
class StreamToLogger:  
    def __init__(self, logger, log_level=logging.WARNING):
        self.logger = logger
        self.log_level = log_level
        self.buffer = ''
    # メッセージを行ごとに分割してロガーに送信
    def write(self, message):
        for line in message.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
    def flush(self):
        pass  # バッファのフラッシュは不要

def local_setup_logger(OUTPUT_NAME):
    global logger  # グローバルでロガーの設定をする。
    logger = logging.getLogger("custom_logger")
    logger.setLevel(logging.DEBUG)  # 全てのログを記録対象にする
    # ログファイルの記録先
    Log_file_path = os.path.join(BUILD_FONTS_DIR, f"{OUTPUT_NAME}_sercherr.log")
    # ファイルハンドラ: INFO以上をファイルに記録
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

def setup():
    os.makedirs(BUILD_FONTS_DIR, exist_ok=True)  # 作業用のディレクトリを作成
    logger = local_setup_logger(OUTPUT_NAME)  # ログ出力の設定
    # 読み込むフォントのディレクトリまで確定させる
    input_fontname = shorten_style_rd(INPUT_FONTSTYLES, VSHRINK_RATIO)[0]
    input_fontfile = os.path.join(SOURCE_FONTS_DIR, input_fontname)
    print (f"input_fontfile \r", end=" ", flush=True)
    font = fontforge.open(input_fontfile)  # フォントを開く
    #一通り情報を集め終わったので元のカレントディレクトリに戻る
    os.chdir(current_dir)
    # 一時ファイル名を付けてパスを確認
    temp_file = f"{OUTPUT_NAME}_temp_0.sfd"
    temp_file_path = os.path.join(BUILD_FONTS_DIR, temp_file)
    del_file = temp_file  # あとで消す時用
    return font, del_file, temp_file, temp_file_path

def save_and_open(font, filepath):
    print(f"保存して開きなおす。file: {filepath}\r", end=" ", flush=True)
    font.save(filepath)
    font.close()
    font = fontforge.open(filepath)
    print(f"開きなおした file: {filepath}\r", end=" ", flush=True)
    sys.stdout = sys.__stdout__  # 標準出力が狂うかもなので一応初期化。
    return font

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

# ASCII範囲にコンポジットグリフが居たら解除
def decomposit_asc(font):
    for codepoint in range(0x20, 0x7F):
        if codepoint in font:
            glyph = font[codepoint]
            if not glyph.isWorthOutputting():
                continue  # 出力しないグリフはスキップ
            if len(glyph.references) > 0:
                glyph.unlinkRef() #コンポジットグリフの参照を解除

# savefreq個処理してたら一旦保存。
def Local_snapshot_sfd (font, glyph, proc_cnt, del_file):
    try:
        if proc_cnt % PRESAVE_INTERVAL == 1:
            print(f"作業前保存中のグリフ： {glyph.glyphname} \r", end=" ", flush=True)
            temp_file = f"{OUTPUT_NAME}_temp_{proc_cnt}.sfd"
            temp_file_path = os.path.join(BUILD_FONTS_DIR, temp_file)
            font.save(temp_file_path)
            # 前回の仮保存ファイルを削除
            print(f"前の一時ファイルを削除： {del_file} \r", end=" ", flush=True)
            del_file_path = os.path.join(BUILD_FONTS_DIR, del_file)
            os.remove(del_file_path)
            # 次の削除対象ファイル名を保存
            del_file = temp_file
            # ついでにログもフラッシュしておく。
            for handler in logging.getLogger().handlers:
                if hasattr(handler, 'flush'):
                    handler.flush()
            gc.collect()  # ガベージコレクションの実行
    except IOError as e:
        print(f"保存か削除に失敗したかも？　多分削除に……： {del_file} \r", flush=True)
    return del_file

# 強制的に全グリフの幅を揃えるパターン専用の処理
def force_width_normalize_setting(glyph, em_size, stroke_flag):
    # 幅が極端に狭いグリフにはなにもしない
    if glyph.width < em_size / 3:
         stroke_flag = False
         wratio = 1
    # 最初から縮小目標とほぼ近い幅のグリフはストロークの対象外にする。
    elif (glyph.width / em_size) < VSHRINK_RATIO * 1.05:
        stroke_flag = False
        wratio = em_size / glyph.width
    # その他は幅をみんな同じに揃える
    else:
        wratio = em_size / glyph.width
    return wratio, stroke_flag

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

def upscale(glyph, wratio):
    glyph.transform((wratio, 0, 0, 8, 0, 0))
    glyph.addExtrema("all")

def downscale(glyph):
    glyph.transform((1, 0, 0, 0.125, 0, 0))
    glyph.addExtrema("all")

# 加工後は何かしらの異常が発生するので修復を試みる
def anomality_repair(glyph):
    glyph.round()  # 整数化
    glyph.removeOverlap()
    if glyph.validate(1) & 0x01:  # 開いたパスがある場合
        ys_closepath(glyph)
    glyph.simplify(0.1) # 単純化
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    ys_repair_Self_Insec(glyph, 3)  # 自己交差の修復試行&ツノ折り
    glyph.round()
    glyph.removeOverlap()
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
    if glyph.validate(1) & 0x20:
        ys_rescale_chain(glyph)  # 一度で取り切れなかった時対策
        glyph.round()
        glyph.removeOverlap()
    glyph.addExtrema("all")

# 幅のストロークで太ったアウトラインを引き締める。
# サイドベアリングを弄りたくないので拡大縮小の原点はグリフの中心にする。
# グリフの幅まで変わると困るのでレイヤー単位で操作
def shapeup_outline(glyph, em_size, stroke_width):
    bbox = glyph.boundingBox()
    xmin, ymin, xmax, ymax = bbox  # グリフの大きさを取得
    xcenter = xmin + (xmax - xmin) / 2
    stroke_shrink = 1 - (stroke_width / em_size)
    glyph.foreground.transform((1, 0, 0, 1, -xcenter, 0))
    glyph.foreground.transform((stroke_shrink, 0, 0, 1, 0, 0))
    glyph.foreground.transform((1, 0, 0, 1, xcenter, 0))
    glyph.addExtrema("all")

# 指定の縮小率に従って縦横比変更
def vshrink(glyph):
    glyph.transform((VSHRINK_RATIO, 0, 0, 1, 0, 0))
    glyph.addExtrema("all")

# 最後にTTFの仕様に合わせた最適化を実施
def finish_optimise(glyph, proc_cnt):
    if glyph.validate(1) & 0x01:  # 開いたパスがある場合
        # 自己交差の修復試行&ツノ折り(パスも閉じてくれるし)
        ys_repair_si_chain(glyph, proc_cnt, 0x20)
    glyph.round()
    glyph.simplify(0.1)
    ys_rm_spikecontours(glyph, 0.1, 0.001, 10)

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

    if glyph.validate(1) & 0x20:  # さらに自己交差がある場合
        ys_repair_si_chain(glyph, proc_cnt, 0x20)
    if glyph.validate(1) & 0x08:  # 参照が不正
        ys_repair_si_chain(glyph, proc_cnt, 0x08)
    glyph.addExtrema("all")

def Local_validate_notice(glyph, note, loglevel):
    log_func = getattr(logger, loglevel, None)  # 動的にログレベルを取得
    if glyph.validate(1) & 0x01:  # 開いたパスがある
        log_func(f"{note}のグリフ '{glyph.glyphname}' に開いたパス")
    if glyph.validate(1) & 0x02:  # 外側に時計回のパスがある
        logger.info(f"{note}のグリフ '{glyph.glyphname}' の外側に時計回りのパス")
    #if glyph.validate(1) & 0x04:  # 交差がある
    #    print(f"{note}のグリフ '{glyph.glyphname}' に交差がある")
    # logger.info(f"{note}のグリフ '{glyph.glyphname}' に交差がある")
    # 交差は見つけてもどーにもできないので記録から外す……
    if glyph.validate(1) & 0x08:  # 参照が不正
        logger.info(f"{note}のグリフ '{glyph.glyphname}' の参照が不正")
    if glyph.validate(1) & 0x10:  # ヒントが不正
        logger.info(f"{note}のグリフ '{glyph.glyphname}' のヒントが不正")
    if glyph.validate(1) & 0x20:  # 自己交差がある
        log_func(f"{note}のグリフ '{glyph.glyphname}' に自己交差がある")
    if glyph.validate(1) & 0x40:  # その他のエラーがある
        log_func(f"{note}後のグリフ '{glyph.glyphname}' にその他のエラー")



######################################################################
#                             メイン関数                             #
######################################################################
def main():
    font, del_file, temp_file, temp_file_path = setup()  # セットアップ
    font = save_and_open(font, temp_file_path)  # SFDに変えて開き直し
    style_is_prop = isprop(font)  # 元のフォントがプロポーショナルか判定
    font_weight = font.os2_weight  # フォントの元情報を把握
    em_size = font.em  # ↓基本ストローク幅のセッティング
    base_stroke_width = STROKE_WIDTH_MIN + STROKE_WIDTH_SF * (1 - VSHRINK_RATIO)
    proc_cnt: int = 0  # カウンタをセット
    # フォントのプロパティを書き換える
    write_property(ini_name, INPUT_FONTSTYLES, VSHRINK_RATIO, font)
    # 全部モノスペースのフラグを管理。
    mono_all = INPUT_FONTSTYLES.startswith("M")

    for glyph in font.glyphs():  # 全グリフをループ処理
        if not glyph.isWorthOutputting():
            print(f"出力しないグリフをスキップ： {glyph.glyphname}\r", end=" ", flush=True)
            continue
        if len(glyph.references) > 0:
            print(f"合成グリフをスキップ： {glyph.glyphname}\r", end=" ", flush=True)
            continue
        if ys_ignorlist(glyph.glyphname):
            print(f"無視リスト対象のグリフをスキップ： {glyph.glyphname}\r", end=" ", flush=True)
            continue

        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Start processing':<32}\r", end=" ", flush=True)
        proc_cnt += 1  # 処理中グリフカウントのインクリメント
        del_file = Local_snapshot_sfd(font, glyph, proc_cnt, del_file)  # 中途保存
        
        if VSHRINK_RATIO >= 0.7:
            stroke_flag = True
        elif VSHRINK_RATIO < 0.7 and font_weight < 700:
            stroke_flag = True
        elif VSHRINK_RATIO >= 0.5 and font_weight < 500:
            stroke_flag = True
        else:  # 狭め方が5割越えてたり、そこに近い値な上でウェイトが重いグリフは基本的にストロークから除外。
            stroke_flag = False

        # 強制的に全ての文字の幅を揃える設定を作る。
        if mono_all:
            wratio, stroke_flag = force_width_normalize_setting(glyph, em_size, stroke_flag)
        else:
            wratio = 1
        # グリフのウェイトや複雑さを勘案してストロークの幅を弱める
        point_count, stroke_width, stroke_flag = custom_stroke_width(glyph, font_weight, base_stroke_width, stroke_flag)
        
        # ホワイトリストとブラックリスト。除外した上でまぁかけても良さそうな奴が対象。
        # 巾基準だけで判断されると太さがガタガタになるので……
        stroke_flag = ys_whitelist(glyph, stroke_flag)
        stroke_flag = ys_blacklist(glyph, stroke_flag)
        
        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Point Count'f'{point_count:<6}':<32}\r", end=" ", flush=True)
        upscale(glyph, wratio)  # 縦に拡大する(強制モノスペース版はこの際に幅も広げる)

        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Wider stroke':<32}\r", end=" ", flush=True)
        # ストロークによる拡幅処理を実行する。
        if stroke_flag: ys_widestroke(glyph, stroke_width, STOROKE_HEIGHT, proc_cnt)

        # 幅を縮小＆最初に縦に伸ばした奴を元に戻す
        downscale(glyph)

        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Anomality Repair':<32}\r", end=" ", flush=True)
        if stroke_flag: anomality_repair(glyph)

        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Anomality Repair Plus':<32}\r", end=" ", flush=True)
        # 変形、精度劣化を伴う修復試行を行う。
        if glyph.validate(1) & 0x20: ys_rescale_chain(glyph)

        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Overflow treatment':<32}\r", end=" ", flush=True)
        # ストロークで太ったアウトラインのを引き締めてオリジナルの幅に近付ける
        if stroke_flag: shapeup_outline(glyph, em_size, stroke_width)

        vshrink(glyph)  # 指定の縮小率に従って縦横比変更
        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Finish optimization':<32}\r", end=" ", flush=True)

        finish_optimise(glyph, proc_cnt)
        # Local_validate_notice(glyph, "仕上げ処理後", "warning")  # 仕上げ後の検査(デバッグ用)
        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Process Completed!':<32}\r", end=" ", flush=True)
    ######################################################################
    #                    各グリフのループ処理ここまで                    #
    ######################################################################
    try:
        # SFDファイルの保存
        output_sfd = f"{OUTPUT_NAME}.sfd"
        output_sfd_path = os.path.join(BUILD_FONTS_DIR, output_sfd)
        print(f"完成したフォントを保存： {output_sfd_path} \r", end=" ", flush=True)
        font.save(output_sfd_path)  # SFD形式で保存
        
        # TTFファイルの保存
        output_ttf = f"{OUTPUT_NAME}.ttf"
        output_ttf_path = os.path.join(BUILD_FONTS_DIR, output_ttf)
        print(f"完成したフォントを保存： {output_ttf_path} \r", end=" ", flush=True)
        font.generate(output_ttf_path)  # TTF形式で保存

        # TTFファイルを開き直し
        print(f"TTFに変更して再開する。file:{output_ttf_path} \r", end=" ", flush=True)
        font.close() # SFDフォントを閉じる
        import time  # 書き込みが完了するまで少し待つ
        time.sleep(0.1)
        font = fontforge.open(output_ttf_path) # TTFを開きなおす
        print(f"TTFを開きなおした。 file: {output_ttf_path} \r", end=" ", flush=True)
        sys.stdout = sys.__stdout__

        # 最後に全グリフを一斉に見直し
        for glyph in font.glyphs():
            if not glyph.isWorthOutputting():
                continue  # 出力しないグリフはスキップ
            if len(glyph.references) > 0:
                print(f"合成グリフをスキップ： {glyph.glyphname} \r", end=" ", flush=True)
                continue  # コンポジットグリフはスキップ
            if ys_ignorlist(glyph.glyphname):
                print(f"無視リスト対象のグリフをスキップ： {glyph.glyphname}\r", end=" ", flush=True)
                continue
            Local_validate_notice(glyph, "最終チェック", "warning")

    except IOError as e:
        print(f"保存に失敗しました: {e}")

    else:
        if del_file != f"temp_0_{OUTPUT_NAME}.sfd":
            del_file_path = os.path.join(BUILD_FONTS_DIR, del_file)
            print(f"前の一時ファイルを削除： {del_file_path} \r", end=" ", flush=True)
            os.remove(del_file_path)
    
    font.close()

if __name__ == "__main__":
    main()
