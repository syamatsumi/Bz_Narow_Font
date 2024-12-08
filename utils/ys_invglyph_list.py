#!fontforge --lang=py -script

def ys_list_invglyph(input_str):
    invglyph_set = {
        "uni2187",  # ↇ
        "uni2188",  # ↈ
        "uni24EB",  # ⓫
        "uni24EC",  # ⓬
        "uni24ED",  # ⓭
        "uni24EE",  # ⓮
        "uni24EF",  # ⓯
        "uni24F0",  # ⓰
        "uni24F1",  # ⓱
        "uni24F2",  # ⓲
        "uni24F3",  # ⓳
        "uni24F4",  # ⓴
        "uni24F5",  # ⓵
        "uni24F6",  # ⓶
        "uni24F7",  # ⓷
        "uni24F8",  # ⓸
        "uni24F9",  # ⓹
        "uni24FA",  # ⓺
        "uni24FB",  # ⓻
        "uni24FC",  # ⓼
        "uni24FD",  # ⓽
        "uni24FE",  # ⓾
        "uni24FF",  # ⓿
        "uni25D9",  # ◙
        "uni261A",  # ☚
        "uni261B",  # ☛
        "uni263B",  # ☻
        "uni265A",  # ♚
        "uni265B",  # ♛
        "uni265C",  # ♜
        "uni265D",  # ♝
        "uni265E",  # ♞
        "uni265F",  # ♟
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
        "uni2776",  # ❶
        "uni2777",  # ❷
        "uni2778",  # ❸
        "uni2779",  # ❹
        "uni277A",  # ❺
        "uni277B",  # ❻
        "uni277C",  # ❼
        "uni277D",  # ❽
        "uni277E",  # ❾
        "uni277F",  # ❿
        "uni27B4",  # ➴
        "uni27B6",  # ➶
        "uniFFFD",  # �
        "uni1F10C",  # 🄌
        "uni1F150",  # 🅐
        "uni1F151",  # 🅑
        "uni1F152",  # 🅒
        "uni1F153",  # 🅓
        "uni1F154",  # 🅔
        "uni1F155",  # 🅕
        "uni1F156",  # 🅖
        "uni1F157",  # 🅗
        "uni1F158",  # 🅘
        "uni1F159",  # 🅙
        "uni1F15A",  # 🅚
        "uni1F15B",  # 🅛
        "uni1F15C",  # 🅜
        "uni1F15D",  # 🅝
        "uni1F15E",  # 🅞
        "uni1F15F",  # 🅟
        "uni1F160",  # 🅠
        "uni1F161",  # 🅡
        "uni1F162",  # 🅢
        "uni1F163",  # 🅣
        "uni1F164",  # 🅤
        "uni1F165",  # 🅥
        "uni1F166",  # 🅦
        "uni1F167",  # 🅧
        "uni1F168",  # 🅨
        "uni1F169",  # 🅩
        "uni1F170",  # 🅰
        "uni1F171",  # 🅱
        "uni1F172",  # 🅲
        "uni1F173",  # 🅳
        "uni1F174",  # 🅴
        "uni1F175",  # 🅵
        "uni1F176",  # 🅶
        "uni1F177",  # 🅷
        "uni1F178",  # 🅸
        "uni1F179",  # 🅹
        "uni1F17A",  # 🅺
        "uni1F17B",  # 🅻
        "uni1F17C",  # 🅼
        "uni1F17D",  # 🅽
        "uni1F17E",  # 🅾
        "uni1F17F",  # 🅿
        "uni1F180",  # 🆀
        "uni1F181",  # 🆁
        "uni1F182",  # 🆂
        "uni1F183",  # 🆃
        "uni1F184",  # 🆄
        "uni1F185",  # 🆅
        "uni1F186",  # 🆆
        "uni1F187",  # 🆇
        "uni1F188",  # 🆈
        "uni1F189",  # 🆉
        "uni1F18A",  # 🆊
        "uni1F18B",  # 🆋
        "uni1F18C",  # 🆌
        "uni1F18D",  # 🆍
        "uni1F18F",  # 🆏
    }
    # 引数の文字列が配列に含まれているか確認
    if input_str in invglyph_set:
        # フラグをFalseに更新
        flag = False
    else:
        flag = True
    
    # フラグを返す
    return flag


if __name__ == "__main__":
    main()
