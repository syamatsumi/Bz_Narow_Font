#!fontforge --lang=py -script
import configparser
import fontforge
import hashlib
import uuid
import re

# フォント固有の値を書き込んだりする方のスクリプト。
# 改造元が異なるフォントを扱う際は、これとiniを弄れば済むようにしたつもり……

def shorten_style_rd(input_fontstyles):
    font_styles = {
        "ゴシR": {"spacing_type": "Monospace", "serif_type": "sans", "weight": "Regular"},
        "ゴシB": {"spacing_type": "Monospace", "serif_type": "sans", "weight": "Bold"},
        "ミンR": {"spacing_type": "Monospace", "serif_type": "serif", "weight": "Regular"},
        "ミンB": {"spacing_type": "Monospace", "serif_type": "serif", "weight": "Bold"},
        "PゴシR": {"spacing_type": "Propotional", "serif_type": "sans", "weight": "Regular"},
        "PゴシB": {"spacing_type": "Propotional", "serif_type": "sans", "weight": "Bold"},
        "PミンR": {"spacing_type": "Propotional", "serif_type": "serif", "weight": "Regular"},
        "PミンB": {"spacing_type": "Propotional", "serif_type": "serif", "weight": "Bold"},
        "MゴシR": {"spacing_type": "AllMonospace", "serif_type": "sans", "weight": "Regular"},
        "MゴシB": {"spacing_type": "AllMonospace", "serif_type": "sans", "weight": "Bold"},
        "MミンR": {"spacing_type": "AllMonospace", "serif_type": "serif", "weight": "Regular"},
        "MミンB": {"spacing_type": "AllMonospace", "serif_type": "serif", "weight": "Bold"},
    }

    style_data = font_styles.get(input_fontstyles)
    spacing_type = style_data["spacing_type"]
    serif_type = style_data["serif_type"]
    weight = style_data["weight"]

    if spacing_type == "Propotional":
        MPtype = "P"
        p_type = "P"
    elif spacing_type == "AllMonospace":
        MPtype = "M"
        p_type = ""
    else:
        MPtype = ""
        p_type = ""

    serif_type_e = "Gothic" if serif_type == "sans" else "Mincho" if serif_type == "serif" else ""
    serif_type_j = "ゴシック" if serif_type == "sans" else "明朝" if serif_type == "serif" else ""

    source_font_name = (f"BIZUD{p_type}{serif_type_e}-{weight}.ttf")

    return source_font_name, spacing_type, serif_type, weight, MPtype, serif_type_e, serif_type_j



# 複数行にかかるコピーライト表記の選択、copyright_multiline_string
def set_copyright_mlstr(serif_type):
    if serif_type == "sans":
        COPYRIGHT = f"""[BIZ UDGothic]
Copyright 2022 The BIZ UDGothic Project Authors (https://github.com/googlefonts/morisawa-biz-ud-gothic)

[Bz Naro Gothic]
Modified by Yamatsumi Saki (2024)
"""  # noqa: E501

    elif serif_type == "serif":
        COPYRIGHT = f"""[BIZ UDMincho]
Copyright 2022 The BIZ UDMincho Project Authors (https://github.com/googlefonts/morisawa-biz-ud-mincho)

[Bz Naro Mincho]
Modified by Yamatsumi Saki (2024)
"""  # noqa: E501

    return COPYRIGHT



# ある意味コイツがこのスクリプトのメイン部分。
# フォントにプロパティを書きます。
def write_property(ini_name, input_fontstyles, vshrink_ratio, font):
    # 上にある関数を使って名前の断片を拾ってくる
    (
    source_font_name,
    spacing_type,
    serif_type,
    weight,
    MPtype,
    serif_type_e,
    serif_type_j
    ) = shorten_style_rd(input_fontstyles)

    settings = configparser.ConfigParser()
    settings.read(ini_name, encoding="utf-8")

    VERSION = settings.get("DEFAULT", "Version")
    FONT_FAMILY_EN = settings.get("DEFAULT", "Font_Family_EN")
    FONT_FAMILY_JP = settings.get("DEFAULT", "Font_Family_JP")
    DESCRIPTOR_EN = settings.get("DEFAULT", "Descriptor_EN")
    DESCRIPTOR_JP = settings.get("DEFAULT", "Descriptor_JP")
    VENDOR_NAME = settings.get("DEFAULT", "Vendor_Name")
    VENDOR_URL = settings.get("DEFAULT", "Vendor_URL")
    LICENSE_URL = settings.get("DEFAULT", "License_URL")
    COPYRIGHT_EN = settings.get("DEFAULT", "Copyright_EN")
    COPYRIGHT_JP = settings.get("DEFAULT", "Copyright_JP")

    copyright_ml = set_copyright_mlstr(serif_type)
    ratio = str(round(vshrink_ratio * 100))

    # ポストスクリプト名の設定(制限多し)
    ps_name = f"{FONT_FAMILY_EN}{MPtype}{serif_type_e}{ratio}-{weight}".replace(" ", "").strip()
    if len(ps_name) > 63:
        raise ValueError(f"PostScriptName '{ps_name}' exceeds 63 characters!")
    if not re.match(r"^[A-Za-z0-9\-]+$", ps_name):
        raise ValueError(f"Invalid character in PostScriptName '{ps_name}'!")

    # OS/2関係のフラグと同じ関係にある値は以降でセット
    font.os2_vendor = VENDOR_NAME
    font.os2_weight_width_slope_only =True

    # 林檎はフラグ立てが必要らしい。めんどくせえ。
    macstyle = 0

    # Panoseと近い属性の値をセット
    panose_family = 2  # Latin Text
    if serif_type == "sans":
        panose_serif = 11  # Normal Sans
        if weight == "Regular":
            panose_weight = 4  # Thin
            font.weight = "Regular"
            font.os2_weight = 400  # Regular
        elif weight == "Bold":
            panose_weight = 8  # Bold
            font.weight = "Bold"
            font.os2_weight = 700  # Bold
            macstyle |= (1 << 0)

    elif serif_type == "serif":
        panose_serif = 2  # Cove(凹面型セリフ)
        if weight == "Regular":
            panose_weight = 4  # Thin
            font.weight = "Regular"
            font.os2_weight = 400  # Regular
        elif weight == "Bold":
            panose_weight = 7  # Demi
            font.weight = "Bold"
            font.os2_weight = 700  # Bold
            macstyle |= (1 << 0)

    if vshrink_ratio <= 0.2:
        panose_propotion = 8  # Very Condensed
        font.os2_width = 1    # Ultra-Condensed
        uqid1 = 1
        macstyle |= (1 << 5)
    elif vshrink_ratio <= 0.3:
        panose_propotion = 8  # Very Condensed
        font.os2_width = 2    # Extra-Condensed
        uqid1 = 2
        macstyle |= (1 << 5)
    elif vshrink_ratio <= 0.4:
        panose_propotion = 6  # Condensed
        font.os2_width = 3    # Condensed
        uqid1 = 3
        macstyle |= (1 << 5)
    elif vshrink_ratio <= 0.5:
        panose_propotion = 6  # Condensed
        font.os2_width = 4    # Semi-Condensed
        uqid1 = 4
        macstyle |= (1 << 5)
    elif vshrink_ratio <= 0.6:
        panose_propotion = 0  # Any
        font.os2_width = 5    # Medium
        uqid1 = 5
    elif vshrink_ratio <= 0.7:
        panose_propotion = 5  # Extended
        font.os2_width = 6    # Semi-Expanded
        uqid1 = 6
        macstyle |= (1 << 6)
    elif vshrink_ratio <= 0.8:
        panose_propotion = 5  # Extended
        font.os2_width = 7    # Expanded
        uqid1 = 7
        macstyle |= (1 << 6)
    elif vshrink_ratio <= 0.9:
        panose_propotion = 7  # Very Extended
        font.os2_width = 8    # Extra-Expanded
        uqid1 = 8
        macstyle |= (1 << 6)
    else:
        panose_propotion = 7  # Very Extended
        font.os2_width = 9    # Ultra-Expanded
        uqid1 = 9
        macstyle |= (1 << 6)

    # Mac Styleの書き込み。
    font.macstyle = macstyle

    # Panoseの書き込み
    font.os2_panose = (panose_family, panose_serif, panose_weight, panose_propotion, 0, 0, 0, 0, 0, 0)

    # unique id周り
    uqid2_table = {
        "Regular": {"": 0, "P": 1, "M": 2},
        "Bold": {"": 3, "P": 4, "M": 5},
        "reserve": {"": 6, "P": 7, "M": 8, "R": 9},
    }
    uqid2 = uqid2_table[weight][MPtype]
    uqid57 = int(hashlib.md5(f"{FONT_FAMILY_EN}{VERSION}".encode()).hexdigest(), 16) % 10000000
    uniqid = (uqid57 * 100) + (uqid2 * 10) +(uqid1)

    # ユニークIDはAdobeに割当てが与えられてるでもなければ基本的に-1を設定
    font.uniqueid = -1

    # 実際に書き込みを始める
    font.fontname = ps_name
    font.familyname = f"{FONT_FAMILY_EN} {MPtype} {serif_type_e}{ratio}".replace("  ", " ").strip()
    font.fullname = f"{FONT_FAMILY_EN} {MPtype} {serif_type_e}{ratio} {weight}".replace("  ", " ").strip()
    font.fondname = f"{FONT_FAMILY_EN}{MPtype}{serif_type_e}{ratio}-{weight}".replace(" ", "").strip()
    font.copyright = copyright_ml
    font.version = VERSION

    font.sfnt_names = (
        ("English (US)", "License",
        """This Font Software is licensed under the SIL Open Font License,
Version 1.1. This license is available with a FAQ
at: https://openfontlicense.org/OFL"""),
        ("Japanese", "License",
        """このフォントはSIL Open Font License第1.1版に基づいて許諾されています。
このライセンスはFAQ（よくある質問）と共に以下のサイトで入手できます。
https://openfontlicense.org/OFL"""),
    )
    font.appendSFNTName("English (US)", "Family",       f"{FONT_FAMILY_EN}{MPtype}{serif_type_e}{ratio}")
    font.appendSFNTName("English (US)", "SubFamily",    f"{weight}")
    font.appendSFNTName("English (US)", "Fullname",     f"{FONT_FAMILY_EN} {MPtype} {serif_type_e}{ratio} {weight}")
    font.appendSFNTName("English (US)", "WWS Family",       f"{FONT_FAMILY_EN} {MPtype} {serif_type_e}")
    font.appendSFNTName("English (US)", "WWS Subfamily",    f"{ratio} {weight}")
    font.appendSFNTName("English (US)", "Preferred Family", f"{FONT_FAMILY_EN} {MPtype} {serif_type_e}")
    font.appendSFNTName("English (US)", "Preferred Styles", f"{ratio} {weight}")
    font.appendSFNTName("English (US)", "Compatible Full",  f"{FONT_FAMILY_EN} {MPtype} {serif_type_e}{ratio} {weight}")
    font.appendSFNTName("English (US)", "Copyright", str(COPYRIGHT_EN))
    font.appendSFNTName("English (US)", "Descriptor", str(DESCRIPTOR_EN))
    font.appendSFNTName("English (US)", "License URL", str(LICENSE_URL))
    font.appendSFNTName("English (US)", "PostScriptName", str(ps_name))
    font.appendSFNTName("English (US)", "Vendor URL", str(VENDOR_URL))
    font.appendSFNTName("English (US)", "Version", str(VERSION))
    font.appendSFNTName("English (US)", "UniqueID", f"{uniqid} {FONT_FAMILY_EN} {MPtype}{serif_type_e}{ratio} {weight} {VERSION}")

    font.appendSFNTName("Japanese", "Family",       f"{FONT_FAMILY_JP}{MPtype}{serif_type_j}{ratio}")
    font.appendSFNTName("Japanese", "SubFamily",    f"{weight}")
    font.appendSFNTName("Japanese", "Fullname",     f"{FONT_FAMILY_JP}{MPtype}{serif_type_j}{ratio} {weight}")
    font.appendSFNTName("Japanese", "WWS Family",       f"{FONT_FAMILY_JP}{MPtype}{serif_type_j}")
    font.appendSFNTName("Japanese", "WWS Subfamily",    f"{ratio} {weight}")
    font.appendSFNTName("Japanese", "Preferred Family", f"{FONT_FAMILY_JP}{MPtype}{serif_type_j}")
    font.appendSFNTName("Japanese", "Preferred Styles", f"{ratio} {weight}")
    font.appendSFNTName("Japanese", "Compatible Full",  f"{FONT_FAMILY_JP}{MPtype}{serif_type_j}{ratio} {weight}")
    font.appendSFNTName("Japanese", "Copyright", str(COPYRIGHT_JP))
    font.appendSFNTName("Japanese", "Descriptor", str(DESCRIPTOR_JP))
    font.appendSFNTName("Japanese", "License URL", str(LICENSE_URL))
    font.appendSFNTName("Japanese", "PostScriptName", str(ps_name))
    font.appendSFNTName("Japanese", "Vendor URL", str(VENDOR_URL))
    font.appendSFNTName("Japanese", "Version", str(VERSION))
    font.appendSFNTName("Japanese", "UniqueID", f"{uniqid} {FONT_FAMILY_JP}{MPtype}{serif_type_j}{ratio} {weight} {VERSION}")

    # font.appendSFNTName("Japanese", "Trademark", f"")
    # font.appendSFNTName("Japanese", "Manufacturer", f"")
    # font.appendSFNTName("Japanese", "Designer", f"")
    # font.appendSFNTName("Japanese", "Designer URL", f"")
    # font.appendSFNTName("Japanese", "Sample Text", f"")
    # font.appendSFNTName("Japanese", "CID findfont Name", f"")

if __name__ == "__main__":
    main()
