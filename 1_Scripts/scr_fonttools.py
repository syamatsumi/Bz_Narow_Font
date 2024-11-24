#!fontforge --lang=py -script

# 2つのフォントを合成する
# このスクリプトの元ネタはUDEVゴシックです。感謝……

import configparser
import math
import os
import shutil
import sys
import uuid
from decimal import ROUND_HALF_UP, Decimal

import fontforge
import psMat

# iniファイルを読み込む
settings = configparser.ConfigParser()
settings.read("scr_build.ini", encoding="utf-8")

VERSION = settings.get("DEFAULT", "VERSION")
FONT_NAME = settings.get("DEFAULT", "FONT_NAME")
JP_FONT = settings.get("DEFAULT", "JP_FONT")
SOURCE_FONTS_DIR = settings.get("DEFAULT", "SOURCE_FONTS_DIR")
BUILD_FONTS_DIR = settings.get("DEFAULT", "BUILD_FONTS_DIR")
VENDER_NAME = settings.get("DEFAULT", "VENDER_NAME")
FONTFORGE_PREFIX = settings.get("DEFAULT", "FONTFORGE_PREFIX")
ITALIC_ANGLE = int(settings.get("DEFAULT", "ITALIC_ANGLE"))

COPYRIGHT = """[BIZ UDGothic]
Copyright 2022 The BIZ UDGothic Project Authors (https://github.com/googlefonts/morisawa-biz-ud-gothic)

[BIZ UDMincho]
Copyright 2022 The BIZ UDMincho Project Authors (https://github.com/googlefonts/morisawa-biz-ud-mincho)

[Bi Hanbunko/Waribiki]
Modified by Saki Yamatsumi (2024)
"""  # noqa: E501

def main():
# オプション判定
    get_options()
    if options.get("unknown-option"):
        usage()
        return

# buildディレクトリを作成する
    if os.path.exists(BUILD_FONTS_DIR) and not options.get("do-not-delete-build-dir"):
        shutil.rmtree(BUILD_FONTS_DIR)
        os.mkdir(BUILD_FONTS_DIR)
    if not os.path.exists(BUILD_FONTS_DIR):
        os.mkdir(BUILD_FONTS_DIR)

    generate_font(
        jp_style="Regular",
        merged_style="Regular",
    )
    generate_font(
        jp_style="Bold",
        merged_style="Bold",
    )
    generate_font(
        jp_style="Regular",
        merged_style="Italic",
    )
    generate_font(
        jp_style="Bold",
        merged_style="BoldItalic",
    )
# オプション毎の修飾子を追加する
    variant = ""


def generate_font(jp_style, merged_style):
    print(f"=== Generate {merged_style} ===")

# 合成するフォントを開く
    jp_font = open_fonts(jp_style)

# 日本語グリフの斜体を生成する
    if "Italic" in merged_style:
        transform_italic_glyphs(jp_font)

# GSUBテーブルを削除する (ひらがな等の全角文字が含まれる行でリガチャが解除される対策)
    remove_lookups(jp_font, remove_gsub=False, remove_gpos=True)

# macOSでのpostテーブルの使用性エラー対策
# 重複するグリフ名を持つグリフをリネームする
    delete_glyphs_with_duplicate_glyph_names(jp_font)

# メタデータを編集する

    edit_meta_data(jp_font, merged_style, variant, cap_height, x_height)

# ttfファイルに保存
# ヒンティングが残っていると不具合に繋がりがちなので外す。
# ヒンティングはあとで ttfautohint で行う。
# flags=("no-hints", "omit-instructions") を使うとヒンティングだけでなく GPOS や GSUB も削除されてしまうので使わない
    jp_font.generate(
        f"{BUILD_FONTS_DIR}/{FONTFORGE_PREFIX}{FONT_NAME}{variant}-{merged_style}-jp.ttf",
    )

    # ttfを閉じる
    jp_font.close()


def open_fonts(jp_style: str):
    """フォントを開く"""
    jp_font = fontforge.open(
        SOURCE_FONTS_DIR + "/" + JP_FONT.replace("{style}", jp_style)
    )
# fonttools merge エラー対処
    jp_font = altuni_to_entity(jp_font)

# フォント参照を解除する
    for glyph in jp_font.glyphs():
        if glyph.isWorthOutputting():
            jp_font.selection.select(("more", None), glyph)
    jp_font.unlinkReferences()
    jp_font.selection.none()

    return jp_font


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


def transform_italic_glyphs(font):
    # 傾きを設定する
    font.italicangle = -ITALIC_ANGLE
    # 全グリフを斜体に変換
    for glyph in font.glyphs():
        orig_width = glyph.width
        glyph.transform(psMat.skew(ITALIC_ANGLE * math.pi / 180))
        glyph.transform(psMat.translate(-94, 0))
        glyph.width = orig_width


def edit_meta_data(font, weight: str, variant: str, cap_height: int, x_height: int):
    """フォント内のメタデータを編集する"""
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
    font.familyname = f"{FONT_NAME} {variant}".strip()
    font.fontname = f"{FONT_NAME}{variant}-{weight}".replace(" ", "").strip()
    font.fullname = f"{FONT_NAME} {variant}".strip() + f" {weight}"
    font.os2_vendor = VENDER_NAME
    font.copyright = COPYRIGHT


if __name__ == "__main__":
    main()
