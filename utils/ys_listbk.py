#!fontforge --lang=py -script

import fontforge

def ys_blacklist(glyph, flag):
    blacklist_set = {
        "uni2187",  # ↇ
        "uni2188",  # ↈ
        "uni25A0",  # ■
        "uni25B2",  # ▲
        "uni25B6",  # ▶
        "uni25BC",  # ▼
        "uni25C0",  # ◀
        "uni25C6",  # ◆
        "uni25CF",  # ●
        "uni25D9",  # ◙
        "uni2600",  # ☀
        "uni2601",  # ☁
        "uni2602",  # ☂
        "uni2605",  # ★
        "uni260E",  # ☎
        "uni2617",  # ☗
        "uni261A",  # ☚
        "uni261B",  # ☛
        "uni263B",  # ☻
        "uni265A",  # ♚
        "uni265B",  # ♛
        "uni265C",  # ♜
        "uni265D",  # ♝
        "uni265E",  # ♞
        "uni265F",  # ♟
        "uni2660",  # ♠
        "uni2663",  # ♣
        "uni2665",  # ♥
        "uni2666",  # ♦
        "uni267C",  # ♼
        "uni26C2",  # ⛂
        "uni26C3",  # ⛃
        "uni26C7",  # ⛇
        "uni26D6",  # ⛖
        "uni26DF",  # ⛟
        "uni26FE",  # ⛾
        "uni270E",  # ✎
        "uni2710",  # ✐
        "uni2719",  # ✙
        "uni271B",  # ✛
        "uni271C",  # ✜
        "uni271F",  # ✟
        "uni272A",  # ✪
        "uni272C",  # ✬
        "uni272D",  # ✭
        "uni272E",  # ✮
        "uni2735",  # ✵
        "uni2741",  # ❁
        "uni2742",  # ❂
        "uni2743",  # ❃
        "uni2756",  # ❖
        "uni27A0",  # ➠
        "uni27A1",  # ➡
        "uni27A4",  # ➤
        "uni27A5",  # ➥
        "uni27A6",  # ➦
        "uni27A7",  # ➧
        "uni27A8",  # ➨
        "uni27B4",  # ➴
        "uni27B6",  # ➶
        "uni27B7",  # ➷
        "uni27B8",  # ➸
        "uni27B9",  # ➹
        "uni27BA",  # ➺
        "uni27BB",  # ➻
        "uni27BC",  # ➼
        "uni27BD",  # ➽
        "uni2B05",  # ⬅
        "uni2B06",  # ⬆
        "uni2B07",  # ⬇
        "uni2B1B",  # ⬛
        "uni2B95",  # ⮕
        "uni3013",  # 〓
        "uni3020",  # 〠
        "uniFFFD",  # �
        "uni1F10C",  # 🄌
    }

    # リストのコードポイント範囲。
    # 範囲は終点が無視されるため指定範囲は終点+1
    blacklist_ranges = [
        range(0x24EB, 0x24FF + 1),
        range(0x2776, 0x277F + 1),
        range(0x278A, 0x2794 + 1),
        range(0x1F150, 0x1F169 + 1),
        range(0x1F170, 0x1F18F + 1),
    ]

    # コードポイントが範囲内かチェック
    if glyph.unicode != -1:  # コードポイントを持つ場合のみチェック
        for r in blacklist_ranges:
            if glyph.unicode in r:
                return False  # リストに該当する場合はFalseを返す

    # グリフ名がリストにあるかチェック
    if glyph.glyphname in blacklist_set:
        return False

    # 条件にマッチしなければフラグをそのまま返す
    return flag

if __name__ == "__main__":
    main()
