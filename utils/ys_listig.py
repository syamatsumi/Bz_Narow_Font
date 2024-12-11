#!fontforge --lang=py -script

def ys_ignorlist(glyphname):
    ignorlist_set = {
        "exclam.vert",
        "numbersign.vert",
        "dollar.vert",
        "percent.vert",
        "ampersand.vert",
        "parenleft.vert",
        "parenright.vert",
        "asterisk.vert",
        "plus.vert",
        "comma.vert",
        "minus.vert",
        "period.vert",
        "slash.vert",
        "zero.vert",
        "one.vert",
        "two.vert",
        "three.vert",
        "four.vert",
        "five.vert",
        "six.vert",
        "seven.vert",
        "eight.vert",
        "nine.vert",
        "colon.vert",
        "semicolon.vert",
        "less.vert",
        "equal.vert",
        "greater.vert",
        "question.vert",
        "at.vert",
        "A.vert",
        "B.vert",
        "C.vert",
        "D.vert",
        "E.vert",
        "F.vert",
        "G.vert",
        "H.vert",
        "I.vert",
        "J.vert",
        "K.vert",
        "L.vert",
        "M.vert",
        "N.vert",
        "O.vert",
        "P.vert",
        "Q.vert",
        "R.vert",
        "S.vert",
        "T.vert",
        "U.vert",
        "V.vert",
        "W.vert",
        "X.vert",
        "Y.vert",
        "Z.vert",
        "bracketleft.vert",
        "yen.vert",
        "bracketright.vert",
        "asciicircum.vert",
        "underscore.vert",
        "a.vert",
        "b.vert",
        "c.vert",
        "d.vert",
        "e.vert",
        "f.vert",
        "g.vert",
        "h.vert",
        "i.vert",
        "j.vert",
        "k.vert",
        "l.vert",
        "m.vert",
        "n.vert",
        "o.vert",
        "p.vert",
        "q.vert",
        "r.vert",
        "s.vert",
        "t.vert",
        "u.vert",
        "v.vert",
        "w.vert",
        "x.vert",
        "y.vert",
        "z.vert",
        "braceleft.vert",
        "bar.vert",
        "braceright.vert",
        "uni203E.vert",
        "gravecomb.vert",
        "acutecomb.vert",
        "uni0308.vert",
        "Adieresis.aalt",
        "ugrave.aalt",
        "eacute.aalt",
        "iacute.aalt",
        "germandbls.aalt",
        "ccedilla.aalt",
        "Ccedilla.aalt",
        "Ntilde.aalt",
        "ntilde.aalt",
        "cent.vert",
        "sterling.vert",
        "oacute.aalt",
        "uacute.aalt",
        "exclamdown.aalt",
        "questiondown.aalt",
        "Odieresis.aalt",
        "Udieresis.aalt",
        "adieresis.aalt",
        "edieresis.aalt",
        "idieresis.aalt",
        "odieresis.aalt",
        "udieresis.aalt",
        "acircumflex.aalt",
        "ecircumflex.aalt",
        "icircumflex.aalt",
        "ocircumflex.aalt",
        "ucircumflex.aalt",
        "agrave.aalt",
        "egrave.aalt",
        "aacute.aalt",
        "Oslash.vert",
        "logicalnot.vert",
        "uniFF61.vert",  # ｡
        "uniFF62.vert",  # ｢
        "uniFF63.vert",  # ｣
        "uniFF64.vert",  # ､
        "uniFF65.vert",  # ･
        "uniFF66.vert",  # ｦ
        "uniFF67.vert",  # ｧ
        "uniFF68.vert",  # ｨ
        "uniFF69.vert",  # ｩ
        "uniFF6A.vert",  # ｪ
        "uniFF6B.vert",  # ｫ
        "uniFF6C.vert",  # ｬ
        "uniFF6D.vert",  # ｭ
        "uniFF6E.vert",  # ｮ
        "uniFF6F.vert",  # ｯ
        "uniFF70.vert",  # ｰ
        "uniFF71.vert",  # ｱ
        "uniFF72.vert",  # ｲ
        "uniFF73.vert",  # ｳ
        "uniFF74.vert",  # ｴ
        "uniFF75.vert",  # ｵ
        "uniFF76.vert",  # ｶ
        "uniFF77.vert",  # ｷ
        "uniFF78.vert",  # ｸ
        "uniFF79.vert",  # ｹ
        "uniFF7A.vert",  # ｺ
        "uniFF7B.vert",  # ｻ
        "uniFF7C.vert",  # ｼ
        "uniFF7D.vert",  # ｽ
        "uniFF7E.vert",  # ｾ
        "uniFF7F.vert",  # ｿ
        "uniFF80.vert",  # ﾀ
        "uniFF81.vert",  # ﾁ
        "uniFF82.vert",  # ﾂ
        "uniFF83.vert",  # ﾃ
        "uniFF84.vert",  # ﾄ
        "uniFF85.vert",  # ﾅ
        "uniFF86.vert",  # ﾆ
        "uniFF87.vert",  # ﾇ
        "uniFF88.vert",  # ﾈ
        "uniFF89.vert",  # ﾉ
        "uniFF8A.vert",  # ﾊ
        "uniFF8B.vert",  # ﾋ
        "uniFF8C.vert",  # ﾌ
        "uniFF8D.vert",  # ﾍ
        "uniFF8E.vert",  # ﾎ
        "uniFF8F.vert",  # ﾏ
        "uniFF90.vert",  # ﾐ
        "uniFF91.vert",  # ﾑ
        "uniFF92.vert",  # ﾒ
        "uniFF93.vert",  # ﾓ
        "uniFF94.vert",  # ﾔ
        "uniFF95.vert",  # ﾕ
        "uniFF96.vert",  # ﾖ
        "uniFF97.vert",  # ﾗ
        "uniFF98.vert",  # ﾘ
        "uniFF99.vert",  # ﾙ
        "uniFF9A.vert",  # ﾚ
        "uniFF9B.vert",  # ﾛ
        "uniFF9C.vert",  # ﾜ
        "uniFF9D.vert",  # ﾝ
        "uniFF9E.vert",  # ﾞ
        "uniFF9F.vert",  # ﾟ
    }

    # グリフ名が無視リストにあるかチェック
    if glyphname in ignorlist_set:
        return True
    else:
        return False

if __name__ == "__main__":
    main()
