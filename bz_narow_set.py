#!fontforge --lang=py -script
import configparser
import fontforge

# フォント固有の値を書き込んだりする方のスクリプト。
# 改造元が異なるフォントを扱う際は、これとiniを弄れば済むようにしたつもり……

def shorten_style_rd(input_fontstyles):
    font_styles = {
        "MゴシR": {"spacing_type": "Monospace", "serif_type": "sans", "weight": "Regular"},
        "MゴシB": {"spacing_type": "Monospace", "serif_type": "sans", "weight": "Bold"},
        "PゴシR": {"spacing_type": "Propotional", "serif_type": "sans", "weight": "Regular"},
        "PゴシB": {"spacing_type": "Propotional", "serif_type": "sans", "weight": "Bold"},
        "MミンR": {"spacing_type": "Monospace", "serif_type": "serif", "weight": "Regular"},
        "MミンB": {"spacing_type": "Monospace", "serif_type": "serif", "weight": "Bold"},
        "PミンR": {"spacing_type": "Propotional", "serif_type": "serif", "weight": "Regular"},
        "PミンB": {"spacing_type": "Propotional", "serif_type": "serif", "weight": "Bold"},
    }

    style_data = font_styles.get(input_fontstyles)
    spacing_type = style_data["spacing_type"]
    serif_type = style_data["serif_type"]
    weight = style_data["weight"]

    type_p = "P" if spacing_type == "Propotional" else ""
    serif_type_e = "Gothic" if serif_type == "sans" else "Mincho" if serif_type == "serif" else ""
    serif_type_j = "ゴシック" if serif_type == "sans" else "明朝" if serif_type == "serif" else ""

    source_font_name = (f"BIZUD{type_p}{serif_type_e}-{weight}.ttf")

    return source_font_name, spacing_type, serif_type, weight, type_p, serif_type_e, serif_type_j



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
    type_p,
    serif_type_e,
    serif_type_j
    ) = shorten_style_rd(input_fontstyles)

    settings = configparser.ConfigParser()
    settings.read(ini_name, encoding="utf-8")

    VERSION = settings.get("DEFAULT", "Version")
    FONT_FAMILY = settings.get("DEFAULT", "Font_Family")
    FONT_FAMILY_JP = settings.get("DEFAULT", "Font_Family_JP")
    VENDOR_NAME = settings.get("DEFAULT", "Vendor_Name")

    COPYRIGHT = set_copyright_str(serif_type)
    ratio = str(round(vshrink_ratio * 100))

# 実際に書き込みを始める
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

    font.familyname = f"{FONT_FAMILY} {serif_type_e}{ratio}"
    font.fontname = f"{FONT_FAMILY}{type_p}{serif_type_e}{ratio}-{weight}".replace(" ", "").strip()
    font.fullname = f"{FONT_FAMILY_JP}{type_p}{serif_type_j}{ratio} {weight}"
    font.os2_vendor = VENDOR_NAME
    font.uniqueid = -1
    font.copyright = COPYRIGHT

    font.appendSFNTName("Japanese", "Family", f"{FONT_FAMILY_JP}{type_p}{serif_type_j}{ratio}")
    font.appendSFNTName("Japanese", "SubFamily", f"{weight}")
    # font.appendSFNTName("Japanese", "UniqueID", )
    font.appendSFNTName("Japanese", "Fullname", font.fullname)
    font.appendSFNTName("Japanese", "Version", VERSION)
    # font.appendSFNTName("Japanese", "PostScriptName", f"")
    # font.appendSFNTName("Japanese", "Trademark", f"")
    # font.appendSFNTName("Japanese", "Manufacturer", f"")
    # font.appendSFNTName("Japanese", "Designer", f"")
    # font.appendSFNTName("Japanese", "Description", f"")
    # font.appendSFNTName("Japanese", "Vendor URL", f"")
    # font.appendSFNTName("Japanese", "Designer URL", f"")
    font.appendSFNTName("Japanese", "License", "This Font Software is licensed under the SIL Open Font License, Version 1.1.")
    font.appendSFNTName("Japanese", "License URL", "http://scripts.sil.org/OFL")
    font.appendSFNTName("Japanese", "Preferred Family", f"{FONT_FAMILY_JP}{type_p}{serif_type_j}")
    font.appendSFNTName("Japanese", "Preferred Styles", f"{ratio} {weight}")
    # font.appendSFNTName("Japanese", "Compatible Full", f"")
    # font.appendSFNTName("Japanese", "Sample Text", f"")
    # font.appendSFNTName("Japanese", "WWS Family", f"")
    # font.appendSFNTName("Japanese", "WWS Subfamily", f"")


if __name__ == "__main__":
    main()
