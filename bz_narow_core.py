#!fontforge --lang=py -script
import configparser
import logging
import os
import sys
import gc

import fontforge
import psMat
import math

from utils import ys_closepath, ys_repair_spikes, ys_rm_spikecontours
from utils import ys_rm_isolatepath, ys_rm_small_poly
from utils import ys_widestroke
from utils import ys_blacklist, ys_whitelist, ys_ignorlist, ys_sparselist, ys_swaplist, ys_pswaplist, ys_mswaplist
from utils import ys_repair_si_chain, ys_rescale_chain, ys_simplify

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
PRESAVE_INTERVAL = int(settings.get("DEFAULT", "Presave_Interval"))

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

# savefreq個処理してたら一旦保存。
def Local_snapshot_sfd (font, glyph, proc_cnt, del_file, force=False):
    try:
        if proc_cnt % PRESAVE_INTERVAL == 1 or force:
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

# 大きく縮める際、元から半分サイズのグリフがあるなら交換してしまう。
def swap_hwglyph(glyph, swlayer_backup, stroke_flag, base_stroke_width):
    # 元のグリフ幅を控えておく
    orig_width = glyph.width

    #バックアップにターゲットのグリフが存在するならレイヤを書換え
    tgtname = glyph.glyphname
    if tgtname in swlayer_backup:
        glyph.foreground = fontforge.layer()
        glyph.width = swlayer_backup[tgtname]["width"]
        for contour in swlayer_backup[tgtname]["layer"]:
            glyph.foreground += contour
        swap_flag = True
    else:
        swap_flag = False

    # 交換が成立していた場合、拡幅処理の影響を減らすため
    if swap_flag:
        swap_width = swlayer_backup[tgtname]["width"]
        # 念の為0除算対策
        if swap_width == 0:
             return False
        # 最初から縮小目標とほぼ近い幅のグリフはストロークの対象外にする。
        # ストロークの影響を最小限に留めるために元の幅にまで広げる
        elif (swap_width / orig_width) <= VSHRINK_RATIO * 1.05:
            expratio = orig_width / swap_width
            stroke_flag = False
        elif (swap_width / orig_width) > 1:
            expratio = 1
            stroke_flag = True
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

# 強制的に全グリフの幅を揃えるパターン専用の処理
def force_width_norm(glyph, em_size, stroke_flag):
    # 幅が極端に狭いグリフにはなにもしない
    if glyph.width < em_size / 3:
         return False
    # 最初から縮小目標とほぼ近い幅のグリフはストロークの対象外にする。
    elif (glyph.width / em_size) <= VSHRINK_RATIO * 1.05:
        stroke_flag = False
        expratio = em_size / glyph.width
    # その他は幅をみんな同じに揃える
    else:
        expratio = em_size / glyph.width
    # 幅統一用の拡幅処理
    glyph.transform(psMat.scale(expratio, 1),"partialRefs")
    glyph.addExtrema("all")
    return stroke_flag

# 太りすぎたグリフを上手くフィットさせる。
# グリフの幅まで変わると困るのでレイヤー単位で操作
def wsize_fitting(glyph, obbox):
    # 現在のbboxと各種値を取得
    cbbox = glyph.boundingBox()
    cxmin, cymin, cxmax, cymax = cbbox
    cwidth = cxmax - cxmin

    # グリフに幅がないならこの関数終了。
    if cwidth == 0:
        return

    # 現在の幅を出す
    gwidth = glyph.width

    # 現状で枠内に収まってるならこの関数終了。
    if cxmin >=0 and cxmax <= gwidth:
        return

    # 元のBBOXを扱いやすくする
    oxmin, oymin, oxmax, oymax = obbox
    owidth = oxmax - oxmin

    glyph_foretemp = glyph.foreground

    # 元々左からはみ出していた場合
    if oxmin < 0:
        # さらに元々右からもはみ出していた場合は元の幅基準で縮小幅を決める
        if oxmax > gwidth:
            sh_ratio = owidth / cwidth
        # 左のはみ出し幅＋送り幅よりでかい場合はそっち合わせで縮小
        elif gwidth - oxmin < cwidth:
            sh_ratio = (gwidth - oxmin) / cwidth
        else:
            sh_ratio = 1
        # 左端に寄せて縮小かけて、元の左サイドベアリングに移動
        glyph_foretemp.transform(psMat.translate(-cxmin, 0))
        glyph_foretemp.transform(psMat.scale(sh_ratio, 1))
        glyph_foretemp.transform(psMat.translate(oxmin, 0))

    # 元々右からはみ出していた場合
    elif oxmax > gwidth:
        # はみ出し分よりなお現在のグリフがでかいなら縮小
        if oxmax < cwidth:
            sh_ratio = oxmax / cwidth
            # 左端に寄せて縮小かけたら元のはみ出し幅のハズ。
            glyph_foretemp.transform(psMat.translate(-cxmin, 0))
            glyph_foretemp.transform(psMat.scale(sh_ratio, 1))
        else:
            # 元のはみ出し幅に合わせる。元のomaxのが右にあるなら＋になって右に行く。
            # 現在のcmaxのが右にあったのなら-になって左に行くはず。
            x_shift = oxmax - cxmax
            glyph_foretemp.transform(psMat.translate(x_shift, 0))

    # 元々のはみ出しがなく現在左からはみ出している場合
    elif cxmin < 0:
        # 現在の幅がグリフ幅を超えるなら左端に寄せて縮小
        # 右端からも飛び出して居る場合も同じ条件と処理になるので判定省略
        if cwidth > gwidth:
            sh_ratio = gwidth / cwidth
            glyph_foretemp.transform(psMat.translate(-cxmin, 0))
            glyph_foretemp.transform(psMat.scale(sh_ratio, 1))
        # 超えないなら左端に寄せるだけ
        else:
            glyph_foretemp.transform(psMat.translate(-cxmin, 0))

    # 元々のはみ出しが無く現在右からはみ出している場合
    elif cxmax > gwidth:
        # 現在の幅がグリフ幅を超えるなら左端に寄せて縮小
        if cwidth > gwidth:
            sh_ratio = gwidth / cwidth
            glyph_foretemp.transform(psMat.translate(-cxmin, 0))
            glyph_foretemp.transform(psMat.scale(sh_ratio, 1))
        # 超えないなら右端に寄せるだけ
        else:
            x_shift = gwidth - cxmax
            glyph_foretemp.transform(psMat.translate(x_shift, 0))

    glyph.foreground = fontforge.layer()
    glyph.foreground = glyph_foretemp
    return

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

# 変形、精度劣化を伴う修復試行を行う。
# 幅を細めてからの適用は禁止。
def anomality_repair2(glyph):
    if (glyph.validate(1) & 0x0FF) != 0 and (glyph.validate(1) & 0x0FF) != 0x04:
        previous_flags = glyph.validate(1) & 0x0FF
        ys_rescale_chain(glyph)
        current_flags = glyph.validate(1) & 0x0FF
        if (previous_flags & ~current_flags) != 0 and current_flags != 0:
            # フラグが下りたけどまだなんかあるなら続行。
            # フラグに変化が無いなら繰り返す意味無いから終了。
            previous_flags = glyph.validate(1) & 0x0FF
            ys_rescale_chain(glyph)
            current_flags = glyph.validate(1) & 0x0FF
            if (previous_flags & ~current_flags) != 0 and current_flags != 0:
                previous_flags = glyph.validate(1) & 0x0FF
                ys_rescale_chain(glyph)
                current_flags = glyph.validate(1) & 0x0FF
                if (previous_flags & ~current_flags) != 0 and current_flags != 0:
                    previous_flags = glyph.validate(1) & 0x0FF
                    ys_rescale_chain(glyph)
                    current_flags = glyph.validate(1) & 0x0FF
                    if (previous_flags & ~current_flags) != 0 and current_flags != 0:
                        ys_rescale_chain(glyph)
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
    log_suffix = "sfd_verify"
    mkdir_path = os.path.join(BUILD_FONTS_DIR, f"{log_suffix}_log")
    os.makedirs(mkdir_path, exist_ok=True)

    # ログ出力の設定
    logger = local_setup_logger(OUTPUT_NAME, log_suffix)

    # 読み込むファイルとパス確認
    source_file = shorten_style_rd(INPUT_FONTSTYLES)[0]
    source_file_path = os.path.join(SOURCE_FONTS_DIR, source_file)
    print (f"source:{source_file_path} \r", end=" ", flush=True)
    # フォントを開く
    font = fontforge.open(source_file_path)

    # 一時ファイル名を付けてパスを確認
    temp_filename = f"{OUTPUT_NAME}_temp_0.sfd"
    temp_filepath = os.path.join(BUILD_FONTS_DIR, temp_filename)
    del_file = temp_filename  # あとで消す時用

    # フォントファイルの保存
    print(f"フォントの形式を変更して再開する。file:{temp_filepath} \r", end=" ", flush=True)
    font.save(temp_filepath)

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

    # フォントの元情報を把握
    font_weight = font.os2_weight
    em_size = font.em

    # 全部モノスペースのフラグを管理。
    mono_all = INPUT_FONTSTYLES.startswith("M")
    is_propotional = INPUT_FONTSTYLES.startswith("P")

    # テストの際はあらかじめリファレンスを解除
    if TGTGRYPHNAME:
        print("testmode : Now delete the glyphs that are not to be tested.", flush=True)
        # 先に参照解除処理を実行
        for glyph in font.glyphs():
            if glyph.glyphname in TGTGRYPHNAME:
                glyph.unlinkRef()

    # 交換対象のグリフを確保
    if VSHRINK_RATIO < 0.66:
        if is_propotional:
            swlayer_backup = ys_pswaplist(font)
        else:
            swlayer_backup = ys_swaplist(font)
    elif mono_all:
        swlayer_backup = ys_mswaplist(font)

    # githubベースで作ると円記号がバックスラッシュになる問題対策
    font.selection.select("yen")
    font.copy()
    font.selection.select("backslash")
    font.clear()
    font.paste()
    font.selection.none()

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
        if TGTGRYPHNAME:
            if glyph.glyphname not in TGTGRYPHNAME:
                # テスト対象外のグリフを削除する
                font.removeGlyph(glyph)
                continue
        # コンポジットグリフはなにもしないでスキップ
        if len(glyph.references) > 0:
            print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Composite glyphs are ignored...':<48}\r", end=" ", flush=True)
            continue
        # 無視リストにあるグリフは修正試行と仕上げだけしてスキップ
        if ys_ignorlist(glyph):
            print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Glyphs on ignore list...':<48}\r", end=" ", flush=True)
            anomality_repair1(glyph, proc_cnt)
            continue

        # 処理中グリフカウントのインクリメント
        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Start processing':<48}\r", end=" ", flush=True)
        proc_cnt += 1

        # 中途保存
        del_file = Local_snapshot_sfd(font, glyph, proc_cnt, del_file)

        # 基本ストローク幅のセッティング
        base_stroke_width = STROKE_WIDTH_MIN + STROKE_WIDTH_SF * (1 - VSHRINK_RATIO)
        # 基本ストローク幅は整数かつ偶数に設定する
        base_stroke_width = (base_stroke_width // 2) * 2
        # ウエイトによって拡幅上限を設定
        if font_weight > 500:
            if base_stroke_width > 80:
                base_stroke_width = 80
                stroke_width = 50
            elif base_stroke_width > 50:
                stroke_width = 50
            else:
                stroke_width = base_stroke_width
        elif base_stroke_width > 110:
            base_stroke_width = 110
            stroke_width = 80
        elif base_stroke_width > 80:
            stroke_width = 80
        else:
            stroke_width = base_stroke_width

        # 一部のウエイトと縮小率の組み合わせは基本的にストロークを避ける
        if VSHRINK_RATIO >= 0.5:
            stroke_flag = True
        elif VSHRINK_RATIO < 0.5 and font_weight < 700:
            stroke_flag = True
        elif VSHRINK_RATIO >= 0.3 and font_weight < 500:
            stroke_flag = True
        else:
            stroke_flag = False

        #例外処理群
        # ホワイトリスト登録グリフはストロークを許可(おおざっぱ)
        stroke_flag = ys_whitelist(glyph, stroke_flag)
        # ストロークを加えると破綻するグリフはブラックリストで除外処理。
        stroke_flag = ys_blacklist(glyph, stroke_flag)
        # スパースリスト登録グリフはストロークの太さを強める
        if ys_sparselist(glyph):
            stroke_width = base_stroke_width
            stroke_flag = True

        # グリフの入替えでイイ感じに調整できそうな対象は入替えてしまいましょう。
        if VSHRINK_RATIO < 0.66:
            stroke_flag ,base_stroke_width = swap_hwglyph(glyph, swlayer_backup, stroke_flag, base_stroke_width)
        elif mono_all:
            stroke_flag ,base_stroke_width = swap_hwglyph(glyph, swlayer_backup, stroke_flag, base_stroke_width)

        # 完全等幅版専用の処理
        if mono_all:
            stroke_flag = force_width_norm(glyph, em_size, stroke_flag)

        if stroke_flag and stroke_width > 10:
            # 元のBBOXを控えておく。
            obbox = glyph.boundingBox()

            # 縦に拡大する
            glyph.transform(psMat.scale(1,8),"partialRefs")
            glyph.addExtrema("all")

            # glyph.background = glyph.foreground
            print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Wider stroke':<48}\r", end=" ", flush=True)
            # ストロークによる拡幅処理を実行する。
            ys_widestroke(glyph, stroke_width, STOROKE_HEIGHT, VSHRINK_RATIO, proc_cnt)

            # 幅を縮小＆最初に縦に伸ばした奴を元に戻す
            glyph.transform(psMat.scale(1, 0.125),"partialRefs")
            glyph.addExtrema("all")

            # はみ出したグリフを元の状態を勘案して移動・縮小する
            wsize_fitting(glyph, obbox)

            print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Anomality Repair':<48}\r", end=" ", flush=True)
            anomality_repair1(glyph, proc_cnt)

            print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Anomality Repair Plus':<48}\r", end=" ", flush=True)
            anomality_repair2(glyph)

        # 指定の縮小率に従って縦横比変更
        glyph.transform(psMat.scale(VSHRINK_RATIO, 1),"partialRefs")
        glyph.addExtrema("all")

        # 仕上げ前の検査
        Local_validate_notice(glyph, "仕上げ前", "warning")

        # 仕上げ処理
        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Finish optimization':<48}\r", end=" ", flush=True)
        anomality_repair1(glyph, proc_cnt)
        glyph.addExtrema("all")

        # 仕上げ後の検査
        Local_validate_notice(glyph, "仕上げ処理後", "warning")
        print(f"now:{proc_cnt:<5}:{glyph.glyphname:<15} {'Process Completed!':<48}\r", end=" ", flush=True)
    ######################################################################
    #                    各グリフのループ処理ここまで                    #
    ######################################################################
    try:
        # 保存ファイル名を付けてパスを確認
        output_file = f"{OUTPUT_NAME}.sfd"
        output_filepath = os.path.join(BUILD_FONTS_DIR, output_file)
        print(f"作業完了したファイルを保存： {output_filepath} \r", end=" ", flush=True)
        font.save(output_filepath)  # SFD形式で保存

    except IOError as e:
        print(f"保存に失敗しました: {e}")

    else:
        del_file_path = os.path.join(BUILD_FONTS_DIR, del_file)
        print(f"前の一時ファイルを削除： {del_file_path} \r", end=" ", flush=True)
        os.remove(del_file_path)

    font.close()

if __name__ == "__main__":
    main()
