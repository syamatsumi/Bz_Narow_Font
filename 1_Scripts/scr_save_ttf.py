#!fontforge --lang=py -script

import os
import sys
import fontforge
import uuid

# コマンドライン引数の処理
if len(sys.argv) < 5:
    sys.exit(1)
try:
    input_fontfile = sys.argv[1]
    FONT_NAME = sys.argv[2]
    FONT_NAME_JP =sys.argv[3]
    variant = sys.argv[4]  # ウエイト以外の値
    clswitch = sys.argv[5]  # COPYLIGHTの切り替え

except ValueError:
    print("Error: 引数に問題がある", flush=True)
    sys.exit(1)

# SFDファイルを開く
jp_font = fontforge.open(input_fontfile)

VERSION = "0.0.1"
VENDER_NAME = "YSAK"
weight = ""
BUILD_FONTS_DIR = "5_build"


COPYRIGHT = """[BIZ UDGothic]
Copyright 2022 The BIZ UDGothic Project Authors (https://github.com/googlefonts/morisawa-biz-ud-gothic)

[BIZ UDMincho]
Copyright 2022 The BIZ UDMincho Project Authors (https://github.com/googlefonts/morisawa-biz-ud-mincho)

[Bi Hanbunko/Waribiki]
Modified by Saki Yamatsumi (2024)
"""  # noqa: E501



def main():
    # コピーライト表記の切り替え
    sw_cprt(clswitch)

    # ファイル名からウエイト値の取得
    weight = get_weight(input_fontfile)
    print(f"Extracted weight: {weight}")

    # フォントを開く
    open_fonts(weight)
    jp_font = fontforge.open(input_fontfile)

    # GSUBテーブルを削除する
#    remove_lookups(jp_font, remove_gsub=False, remove_gpos=True)

    # メタデータの編集
    write_meta(jp_font, weight)

    # 書き出し
    jp_font.generate(f"{BUILD_FONTS_DIR}/{FONT_NAME}{variant}-{weight}.ttf")


# ウェイト名の抽出
def get_weight(fontfile):
    """ファイル名からウェイトを抽出する"""
    filename = os.path.splitext(os.path.basename(fontfile))[0]
    weight = filename.split("-")[-1] if "-" in filename else ""
    if not weight:
        print(f"Warning: Could not extract weight from filename: {filename}")
    return weight


# メタデータの書き込み
def write_meta(font, weight):
    if "Regular" == weight or "Italic" == weight:
        font.os2_weight = 400
    elif "Bold" in weight:
        font.os2_weight = 700

    font.sfnt_names = (
        (
            "English (US)",
            "License",
            """This Font Software is licensed under the SIL Open Font License,
Version 1.1. This license is available with a FAQ
at: http://scripts.sil.org/OFL""",
        ),
        ("English (US)", "License URL", "http://scripts.sil.org/OFL"),
        ("English (US)", "Version", VERSION),
    )
    font.familyname = f"{FONT_NAME} {variant}"
    font.fontname = f"{FONT_NAME}_{variant}-{weight}"
    font.fullname = f"{FONT_NAME_JP} {variant} {weight}"
    font.os2_vendor = VENDER_NAME
    font.copyright = COPYRIGHT
    font.uniqueid = -1


# 
def sw_cprt(clswitch):
    global COPYRIGHT
    if clswitch == "はんぶんゴシック":
        COPYRIGHT = """[BIZ UDGothic]
Copyright 2022 The BIZ UDGothic Project Authors (https://github.com/googlefonts/morisawa-biz-ud-gothic)

[Bi Hanbun Gothic]
Modified by Saki Yamatsumi (2024)
"""  # noqa: E501

    elif clswitch == "わりびきゴシック":
        COPYRIGHT = """[BIZ UDGothic]
Copyright 2022 The BIZ UDGothic Project Authors (https://github.com/googlefonts/morisawa-biz-ud-gothic)

[Bi Waribiki Gothic]
Modified by Saki Yamatsumi (2024)
"""  # noqa: E501(

    elif clswitch == "ほそめゴシック":
        COPYRIGHT = """[BIZ UDGothic]
Copyright 2022 The BIZ UDGothic Project Authors (https://github.com/googlefonts/morisawa-biz-ud-gothic)

[Bi Choihoso Gothic]
Modified by Saki Yamatsumi (2024)
"""  # noqa: E501

    elif clswitch == "はんぶん明朝":
        COPYRIGHT = """[BIZ UDMincho]
Copyright 2022 The BIZ UDMincho Project Authors (https://github.com/googlefonts/morisawa-biz-ud-mincho)

[Bi Hanbunko Mincho]
Modified by Saki Yamatsumi (2024)
"""  # noqa: E501

    elif clswitch == "わりびき明朝":
        COPYRIGHT = """[BIZ UDMincho]
Copyright 2022 The BIZ UDMincho Project Authors (https://github.com/googlefonts/morisawa-biz-ud-mincho)

[Bi Waribiki Mincho]
Modified by Saki Yamatsumi (2024)
"""  # noqa: E501

    elif clswitch == "ほそめ明朝":
        COPYRIGHT = """[BIZ UDMincho]
Copyright 2022 The BIZ UDMincho Project Authors (https://github.com/googlefonts/morisawa-biz-ud-mincho)

[Bi Hosome Mincho]
Modified by Saki Yamatsumi (2024)
"""  # noqa: E501




def altuni_to_entity(jp_font):
    """Alternate Unicodeで透過的に参照して表示している箇所を実体のあるグリフに変換する"""
    for glyph in jp_font.glyphs():
        if glyph.altuni is not None:
            # 以下形式のタプルで返ってくる
            # (unicode-value, variation-selector, reserved-field)
            # 第3フィールドは常に0なので無視
            altunis = glyph.altuni

            # variation-selectorがなく (-1)、透過的にグリフを参照しているものは実体のグリフに変換する
            before_altuni = ""
            for altuni in altunis:
                # 直前のaltuniと同じ場合はスキップ
                if altuni[1] == -1 and before_altuni != ",".join(map(str, altuni)):
                    glyph.altuni = None
                    copy_target_unicode = altuni[0]
                    try:
                        copy_target_glyph = jp_font.createChar(
                            copy_target_unicode,
                            f"uni{hex(copy_target_unicode).replace('0x', '').upper()}copy",
                        )
                    except Exception:
                        copy_target_glyph = jp_font[copy_target_unicode]
                    copy_target_glyph.clear()
                    copy_target_glyph.width = glyph.width
                    # copy_target_glyph.addReference(glyph.glyphname)
                    jp_font.selection.select(glyph.glyphname)
                    jp_font.copy()
                    jp_font.selection.select(copy_target_glyph.glyphname)
                    jp_font.paste()
                before_altuni = ",".join(map(str, altuni))
    # エンコーディングの整理のため、開き直す
    font_path = f"{BUILD_FONTS_DIR}/{jp_font.fullname}_{uuid.uuid4()}.ttf"
    jp_font.generate(font_path)
    jp_font.close()
    reopen_jp_font = fontforge.open(font_path)
    # 一時ファイルを削除
    os.remove(font_path)
    return reopen_jp_font


def remove_lookups(font, remove_gsub=True, remove_gpos=True):
    """GSUB, GPOSテーブルを削除する"""
    if remove_gsub:
        for lookup in font.gsub_lookups:
            font.removeLookup(lookup)
    if remove_gpos:
        for lookup in font.gpos_lookups:
            font.removeLookup(lookup)


def open_fonts(jp_style: str):
    """フォントを開く"""
    jp_font = fontforge.open(input_fontfile)

    # fonttools merge エラー対処
    jp_font = altuni_to_entity(jp_font)

    # フォント参照を解除する
    for glyph in jp_font.glyphs():
        if glyph.isWorthOutputting():
            jp_font.selection.select(("more", None), glyph)
    jp_font.unlinkReferences()
    jp_font.selection.none()

    return jp_font

if __name__ == "__main__":
    main()
