#!fontforge --lang=py -script

import fontforge

def ys_ignorlist(glyph):
    # 除外キーワード
    ignore_keywords = {
        ".vert"
    }

    # 除外リスト（完全一致）
    ignore_list = {
        "glyph13576",
        "exclamdown.aalt",
        "currency.aalt",
        "questiondown.aalt",
        "uni0306.aalt",
        "cedilla.aalt",
        "uni030B.aalt",
        "uni030C.aalt",
        "AE.aalt",
        "ordfeminine.aalt",
        "Lslash.aalt",
        "Oslash.aalt",
        "OE.aalt",
        "ordmasculine.aalt",
        "ae.aalt",
        "lslash.aalt",
        "oslash.aalt",
        "oe.aalt",
        "germandbls.aalt",
        "threequarters.aalt",
        "Agrave.aalt",
        "Aacute.aalt",
        "Acircumflex.aalt",
        "Atilde.aalt",
        "Adieresis.aalt",
        "Aring.aalt",
        "Ccedilla.aalt",
        "Egrave.aalt",
        "Eacute.aalt",
        "Ecircumflex.aalt",
        "Edieresis.aalt",
        "Igrave.aalt",
        "Iacute.aalt",
        "Icircumflex.aalt",
        "Idieresis.aalt",
        "Eth.aalt",
        "Ntilde.aalt",
        "Ograve.aalt",
        "Oacute.aalt",
        "Ocircumflex.aalt",
        "Otilde.aalt",
        "Odieresis.aalt",
        "Ugrave.aalt",
        "Uacute.aalt",
        "Ucircumflex.aalt",
        "Udieresis.aalt",
        "Yacute.aalt",
        "Thorn.aalt",
        "agrave.aalt",
        "aacute.aalt",
        "acircumflex.aalt",
        "atilde.aalt",
        "adieresis.aalt",
        "aring.aalt",
        "ccedilla.aalt",
        "egrave.aalt",
        "eacute.aalt",
        "ecircumflex.aalt",
        "edieresis.aalt",
        "igrave.aalt",
        "iacute.aalt",
        "icircumflex.aalt",
        "idieresis.aalt",
        "eth.aalt",
        "ntilde.aalt",
        "ograve.aalt",
        "oacute.aalt",
        "ocircumflex.aalt",
        "otilde.aalt",
        "odieresis.aalt",
        "ugrave.aalt",
        "uacute.aalt",
        "ucircumflex.aalt",
        "udieresis.aalt",
        "yacute.aalt",
        "thorn.aalt",
        "ydieresis.aalt",
        "Scaron.aalt",
        "Zcaron.aalt",
        "scaron.aalt",
        "zcaron.aalt"
    }

    # 除外するコードポイント範囲
    # 範囲は終点が含まれない点に注意
    ignore_ranges = [
        range(12499, 12529),
        range(13188, 13201),
        range(13281, 13512),
        range(13577, 13671)
    ]

    # キーワード除外処理
    if any(keyword in glyph.glyphname for keyword in ignore_keywords):
        return True

    # グリフ名が "glyph" で始まり、数値部分が範囲内かをチェック
    if glyph.glyphname.startswith("glyph"):
        try:
            num = int(glyph.glyphname[5:])  # "glyph" の後ろを数値に変換
            for code_range in ignore_ranges:
                if num in code_range:  # 範囲内か確認
                    return True
        except ValueError:
            pass  # 数値変換できなかった場合はスルー

    # グリフ名がリストにあるかチェック
    if glyph.glyphname in ignore_list:
        return True
    else:
        return False

if __name__ == "__main__":
    main()
