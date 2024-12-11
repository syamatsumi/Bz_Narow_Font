#!fontforge --lang=py -script

def ys_whitelist(glyph, flag):
    whitelist_set = {
        "uni7532",  # 甲
        "uni4E59",  # 乙
        "uni4E19",  # 丙
        "uni4E01",  # 丁
        "uni4E00",  # 一
        "uni4E8C",  # 二
        "uni4E09",  # 三
        "uni56DB",  # 四
        "uni4E94",  # 五
        "uni516D",  # 六
        "uni4E03",  # 七
        "uni516B",  # 八
        "uni4E5D",  # 九
        "uni5341",  # 十
        "uni4ECA",  # 今
        "uni6614",  # 昔
        "uni4E86",  # 了
        "uni4EC1",  # 仁
        "uni4E59",  # 乙
        "uni4E2D",  # 中
        "uni4E0D",  # 不
        "uni5408",  # 合
        "uni5426",  # 否
        "uni4EBA",  # 人
        "uni5165",  # 入
        "uni76EE",  # 目
        "uni53E3",  # 口
        "uni65E5",  # 日
        "uni6708",  # 月
        "uni706B",  # 火
        "uni6C34",  # 水
        "uni6728",  # 木
        "uni571F",  # 土
        "uni58EB",  # 士
        "uni58EC",  # 壬
        "uni5927",  # 大
        "uni5C0F",  # 小
        "uni5915",  # 夕
        "uni5929",  # 天
        "uni592B",  # 夫
        "uni59BB",  # 妻
        "uni592E",  # 央
        "uni738B",  # 王
        "uni672C",  # 本
        "uni5B50",  # 子
        "uni5C11",  # 少
        "uni5DF1",  # 己
        "uni5DF3",  # 巳
        "uni5DE5",  # 工
        "uni5DE6",  # 左
        "uni53F3",  # 右
        "uni5DFE",  # 巾
        "uni5E72",  # 干
        "uni5E73",  # 平
        "uni5E74",  # 年
        "uni5E78",  # 幸
        "uni624B",  # 手
        "uni8DB3",  # 足
        "uni6238",  # 戸
        "uni6597",  # 斗
        "unifb01",  # ﬁ
        "unifb02",  # ﬂ
        "unife45",  # ﹅
        "unife46",  # ﹆
    }
    # ホワイトリストのコードポイント範囲
    whitelist_ranges = [
        range(0x21, 0x24EB),
        range(0x2500, 0x25FE),
        range(0x3001, 0x301F),
        range(0x3033, 0x31FF),
        range(0x4E00, 0x4E15),
        range(0xFF01, 0xFFEF),
    ]

    # コードポイントが範囲内かチェック
    if glyph.unicode != -1:  # コードポイントを持つ場合のみチェック
        for r in whitelist_ranges:
            if glyph.unicode in r:
                return True  # ホワイトリストに該当する場合はTrueを返す

    # グリフ名がホワイトリストにあるかチェック
    if glyph.glyphname in whitelist_set:
        return True

    # 条件にマッチしなければフラグをそのまま返す
    return flag


if __name__ == "__main__":
    main()
