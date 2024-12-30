#!fontforge --lang=py -script
import configparser
import logging
import os
import sys
import gc

import fontforge

from utils import ys_repair_si_chain, ys_repair_spikes, ys_rescale_chain
from utils import ys_rm_isolatepath, ys_rm_spikecontours, ys_rm_isolatepath, ys_rm_small_poly

# ファイル名変えたらここも要書換え
from bz_narow_property import shorten_style_rd, write_property

# コマンドライン引数の処理
if len(sys.argv) < 4:
    print("Usage: script.py <input_fontstyles> <output_name> <vshrink_ratio> <tgtgryphname>...", flush=True)
    sys.exit(1)
try:
    INPUT_FONTSTYLES = sys.argv[1]  # 入力ファイル
    OUTPUT_NAME = sys.argv[2]  # 出力ファイル
    VSHRINK_RATIO = float(sys.argv[3])  # 横に縮める比率（数値に変換）
    # 4番目以降の引数をリストとして格納
    TGTGRYPHNAME = sys.argv[4:]  # 可変長のグリフ名リスト
except ValueError:
    print("Error: <stroke_width> and <VSHRINK_RATIO> must be numbers.", flush=True)
    sys.exit(1)

# スクリプトの場所をカレントディレクトリに設定する。
this_script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_script_dir)

# 設定ファイルのパス設定、現在のスクリプト名を取得
this_script_name = os.path.basename(__file__)
# 拡張子を除外する
base_name = os.path.splitext(this_script_name)[0]

# 名前にアンダーバーがある場合
if "_" in base_name:
    # hoge_hoge.pyならhoge_settings.iniに。
    prefix, _, _ = base_name.rpartition("_")
    ini_name = f"{prefix}_settings.ini"
# 名前にアンダーバーがない場合は
else:
    # hogehoge.pyからhogehoge.iniに。
    ini_name = f"{base_name}.ini"
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

def local_setup_logger(OUTPUT_NAME, suffix):
    global logger  # グローバルでロガーの設定をする。
    logger = logging.getLogger("custom_logger")
    logger.setLevel(logging.DEBUG)  # 全てのログを記録対象にする
    # ログファイルの記録先
    Log_file_path = os.path.join(BUILD_FONTS_DIR, f"{suffix}_log", f"{OUTPUT_NAME}_{suffix}.log")
    # ファイルハンドラ: WARNING以上をファイルに記録
    file_handler = logging.FileHandler(Log_file_path)
    file_handler.setLevel(logging.WARNING)
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

# 加工後は何かしらの異常が発生するので修復を試みる
def anomality_repair1(glyph, counter):
    if (glyph.validate(1) & 0x0FF) != 0 and (glyph.validate(1) & 0x0FF) != 0x04:
        previous_flags = glyph.validate(1) & 0x0FF
        ys_repair_si_chain(glyph, counter)
        current_flags = glyph.validate(1) & 0x0FF
        if (previous_flags & ~current_flags) != 0 and current_flags != 0:
            # フラグが下りたけどまだなんかあるなら続行。
            # フラグに変化が無いなら繰り返す意味無いから終了。
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

def Local_validate_notice(glyph, note, loglevel):
    log_func = getattr(logger, loglevel, None)  # 動的にログレベルを取得
    if glyph.validate(1) & 0x01:  # 開いたパスがある
        log_func(f"{INPUT_FONTSTYLES}:{note}のグリフ '{glyph.glyphname}' に開いたパス")
    if glyph.validate(1) & 0x02:  # 外側に時計回のパスがある
        log_func(f"{INPUT_FONTSTYLES}:{note}のグリフ '{glyph.glyphname}' の外側に時計回りのパス")
    if glyph.validate(1) & 0x04:  # 交差がある
        # logger.info(f"{INPUT_FONTSTYLES}:{note}のグリフ '{glyph.glyphname}' に交差がある")
        print(f"{INPUT_FONTSTYLES}:{note}のグリフ '{glyph.glyphname}' に交差がある \r", end=" ", flush=True)
    if glyph.validate(1) & 0x08:  # 参照が不正
        log_func(f"{INPUT_FONTSTYLES}:{note}のグリフ '{glyph.glyphname}' の参照が不正")
    if glyph.validate(1) & 0x10:  # ヒントが不正
        log_func(f"{INPUT_FONTSTYLES}:{note}のグリフ '{glyph.glyphname}' のヒントが不正")
    if glyph.validate(1) & 0x20:  # 自己交差がある
        log_func(f"{INPUT_FONTSTYLES}:{note}のグリフ '{glyph.glyphname}' に自己交差がある")
    if glyph.validate(1) & 0x40:  # その他のエラーがある
        log_func(f"{INPUT_FONTSTYLES}:{note}後のグリフ '{glyph.glyphname}' にその他のエラー")



######################################################################
#                             メイン関数                             #
######################################################################
def main():
    # 作業用のディレクトリを作成とログ出力の設定
    log_suffix = "ttf_verify"
    mkdir_path = os.path.join(BUILD_FONTS_DIR, f"{log_suffix}_log")
    os.makedirs(mkdir_path, exist_ok=True)

    # ログ出力の設定
    logger = local_setup_logger(OUTPUT_NAME, log_suffix)

    # 読み込むファイルとパス確認
    source_file = f"{OUTPUT_NAME}.sfd"
    source_file_path = os.path.join(BUILD_FONTS_DIR, source_file)
    print (f"source:{source_file_path} \r", end=" ", flush=True)
    # フォントを開く
    font = fontforge.open(source_file_path)

    # 一時ファイル名を付けてパスを確認
    temp_filename = f"{OUTPUT_NAME}_temp.ttf"
    temp_filepath = os.path.join(BUILD_FONTS_DIR, temp_filename)
    del_file = temp_filename  # あとで消す時用

    # フォントファイルの保存
    print(f"フォントの形式を変更して再開する。file:{temp_filepath} \r", end=" ", flush=True)
    font.generate(temp_filepath)

    # フォントを閉じる
    font.close()
    import time  # 書き込みが完了するまで少し待つ
    time.sleep(0.1)

    # フォントファイルを開き直し
    font = fontforge.open(temp_filepath)
    print(f"変換後のファイルを開きなおした。 file: {temp_filepath} \r", end=" ", flush=True)
    # 標準出力が狂うかもなので一応初期化。
    sys.stdout = sys.__stdout__

    # フォントのプロパティを書き換える
    write_property(ini_name, INPUT_FONTSTYLES, VSHRINK_RATIO, font)



    ######################################################################
    #　　　　　　　　　　　　　　　ループ 1　　　　　　　　　　　　　　　#
    ######################################################################
    # カウンタをセット
    proc_cnt: int = 0

    # 全グリフをループ処理
    for glyph in font.glyphs():
        # 出力に値しない(カラのグリフ)は無視
        if not glyph.isWorthOutputting():
            continue
        # 処理中グリフカウントのインクリメント
        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Start processing':<48}\r", end=" ", flush=True)
        proc_cnt += 1

        # 仕上げ前の検査
        Local_validate_notice(glyph, "仕上げ前", "warning")

        # 仕上げ処理
        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Finish optimization':<48}\r", end=" ", flush=True)

        if VSHRINK_RATIO >= 1.0:
            ys_rescale_chain

        ys_repair_spikes(glyph, 0.3)
        glyph.round()
        glyph.removeOverlap()
        ys_rm_isolatepath(glyph)
        ys_rm_spikecontours(glyph, 0.1, 0.001, 10)
        ys_rm_small_poly(glyph, 25, 25)

        anomality_repair1(glyph, proc_cnt)

        # 仕上げ後の検査
        Local_validate_notice(glyph, "仕上げ処理後", "warning")
        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Process Completed!':<48}\r", end=" ", flush=True)
    ######################################################################
    #                    各グリフのループ処理ここまで                    #
    ######################################################################
    try:
        # 保存ファイル名を付けてパスを確認
        output_file = f"{OUTPUT_NAME}.ttf"
        output_filepath = os.path.join(BUILD_FONTS_DIR, output_file)
        print(f"作業完了したファイルを保存： {output_filepath} \r", end=" ", flush=True)
        font.generate(output_filepath)  # 拡張子の形式で保存

    except IOError as e:
        print(f"保存に失敗しました: {e}")

    else:
        del_file_path = os.path.join(BUILD_FONTS_DIR, del_file)
        print(f"前の一時ファイルを削除： {del_file_path} \r", end=" ", flush=True)
        os.remove(del_file_path)

    font.close()

if __name__ == "__main__":
    main()
