#!fontforge --lang=py -script
import configparser
import fontforge

# フォント固有の値を書き込んだりする方のスクリプト。
# 改造元が異なるフォントを扱う際は、これとiniを弄れば済むようにしたつもり……

def shorten_style_rd(input_fontstyles, ratio):
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
        if ratio > 0.5:
            p_type = "P"
        else: 
            p_type = ""
    else:
        MPtype = ""
        p_type = ""
    
    serif_type_e = "Gothic" if serif_type == "sans" else "Mincho" if serif_type == "serif" else ""
    serif_type_j = "ゴシック" if serif_type == "sans" else "明朝" if serif_type == "serif" else ""

    source_font_name = (f"BIZUD{p_type}{serif_type_e}-{weight}.ttf")

    return source_font_name, spacing_type, serif_type, weight, MPtype, serif_type_e, serif_type_j



# コピーライト表記の選択
def set_copyright_str(serif_type):
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
    ) = shorten_style_rd(input_fontstyles, vshrink_ratio)

    settings = configparser.ConfigParser()
    settings.read(ini_name, encoding="utf-8")

    VERSION = settings.get("DEFAULT", "Version")
    FONT_FAMILY = settings.get("DEFAULT", "Font_Family")
    FONT_FAMILY_JP = settings.get("DEFAULT", "Font_Family_JP")
    VENDOR_NAME = settings.get("DEFAULT", "Vendor_Name")

    COPYRIGHT = set_copyright_str(serif_type)
    ratio = str(round(vshrink_ratio * 100))



# 実際に書き込みを始める
    font.familyname = f"{FONT_FAMILY} {MPtype} {serif_type_e}{ratio}".replace("  ", " ").strip()
    font.fontname = f"{FONT_FAMILY}{MPtype}{serif_type_e}{ratio}-{weight}".replace(" ", "").strip()
    font.fullname = f"{FONT_FAMILY_JP}{MPtype}{serif_type_j}{ratio} {weight}"
    font.copyright = COPYRIGHT
    font.version = VERSION
    font.uniqueid = -1
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
    font.appendSFNTName("English (US)", "Preferred Family", f"{FONT_FAMILY} {MPtype} {serif_type_e}")
    font.appendSFNTName("English (US)", "Preferred Styles", f"{ratio} {weight}")
    font.appendSFNTName("Japanese", "Family", f"{FONT_FAMILY_JP}{MPtype}{serif_type_j}{ratio}")
    font.appendSFNTName("Japanese", "SubFamily", f"{weight}")
    font.appendSFNTName("Japanese", "Fullname", font.fullname)
    font.appendSFNTName("Japanese", "Version", VERSION)
    font.appendSFNTName("Japanese", "License", "This Font Software is licensed under the SIL Open Font License, Version 1.1.")
    font.appendSFNTName("Japanese", "License URL", "http://scripts.sil.org/OFL")
    font.appendSFNTName("Japanese", "Preferred Family", f"{FONT_FAMILY_JP}{MPtype}{serif_type_j}")
    font.appendSFNTName("Japanese", "Preferred Styles", f"{ratio} {weight}")
    # font.appendSFNTName("Japanese", "UniqueID", )
    # font.appendSFNTName("Japanese", "PostScriptName", f"")
    # font.appendSFNTName("Japanese", "Trademark", f"")
    # font.appendSFNTName("Japanese", "Manufacturer", f"")
    # font.appendSFNTName("Japanese", "Designer", f"")
    # font.appendSFNTName("Japanese", "Description", f"")
    # font.appendSFNTName("Japanese", "Vendor URL", f"")
    # font.appendSFNTName("Japanese", "Designer URL", f"")
    # font.appendSFNTName("Japanese", "Compatible Full", f"")
    # font.appendSFNTName("Japanese", "Sample Text", f"")
    # font.appendSFNTName("Japanese", "WWS Family", f"")
    # font.appendSFNTName("Japanese", "WWS Subfamily", f"")

    # OS/2関係のフラグと同じ関係にある値は以降でセット
    font.os2_vendor = VENDOR_NAME
    font.os2_weight_width_slope_only =True

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

    # 通常の日本語フォントは半角全角の違いを持つため
    # 通常使わない属性をここではセット……
    if MPtype == "M":
        panose_propotion = 9  # 等幅
        if vshrink_ratio <= 0.5:
            font.os2_width = 1    # Ultra-Condensed
        elif vshrink_ratio <= 0.625:
            font.os2_width = 2    # Extra-Condensed
        elif vshrink_ratio <= 0.75:
            font.os2_width = 3    # Condensed
        elif vshrink_ratio <= 0.875:
            font.os2_width = 4    # Semi-Condensed

    elif vshrink_ratio <= 0.5:
        panose_propotion = 8  # Very Condensed
        font.os2_width = 1    # Ultra-Condensed
    elif vshrink_ratio <= 0.625:
        panose_propotion = 8  # Very Condensed
        font.os2_width = 2    # Extra-Condensed
    elif vshrink_ratio <= 0.75:
        panose_propotion = 6  # Condensed
        font.os2_width = 3    # Condensed
    elif vshrink_ratio <= 0.875:
        panose_propotion = 6  # Condensed
        font.os2_width = 4    # Semi-Condensed

    elif vshrink_ratio >= 2:
        panose_propotion = 7  # Very Extended
        font.os2_width = 9    # Ultra-Expanded
    elif vshrink_ratio >= 1.5:
        panose_propotion = 7  # Very Extended
        font.os2_width = 8    # Extra-Expanded
    elif vshrink_ratio >= 1.25:
        panose_propotion = 5  # Extended
        font.os2_width = 7    # Expanded
    elif vshrink_ratio >= 1.125:
        panose_propotion = 5  # Extended
        font.os2_width = 6  # Semi-Expanded
    else:
        panose_propotion = 0  # 任意
        font.os2_width = 5  # Medium

    # Panoseの書き込み
    font.os2_panose = (panose_family, panose_serif, panose_weight, panose_propotion, 0, 0, 0, 0, 0, 0)



if __name__ == "__main__":
    main()
