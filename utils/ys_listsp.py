#!fontforge --lang=py -script

import fontforge

def ys_sparselist(glyph):
    sparselist_set = {
        "uni4E00",  # 一
        "uni4E01",  # 丁
        "uni4E09",  # 三
        "uni4E5A",  # 乚
        "uni4E85",  # 亅
        "uni4E86",  # 了
        "uni4E8C",  # 二
        "uni4EA0",  # 亠
        "uni4EA1",  # 亡
        "uni4EBA",  # 人
        "uni4EC1",  # 仁
        "uni5165",  # 入
        "uni516B",  # 八
        "uni516D",  # 六
        "uni5200",  # 刀
        "uni529B",  # 力
        "uni52F9",  # 勹
        "uni5315",  # 匕
        "uni531A",  # 匚
        "uni5338",  # 匸
        "uni5341",  # 十
        "uni535C",  # 卜
        "uni53E3",  # 口
        "uni571F",  # 土
        "uni58EB",  # 士
        "uni58EC",  # 壬
        "uni5927",  # 大
        "uni5929",  # 天
        "uni592B",  # 夫
        "uni592E",  # 央
        "uni5B50",  # 子
        "uni5DE5",  # 工
        "uni5DF1",  # 己
        "uni5DF3",  # 巳
        "uni5E72",  # 干
        "uni6238",  # 戸
        "uni624B",  # 手
        "uni624C",  # 扌
        "uni65E5",  # 日
        "uni6708",  # 月
        "uni738B",  # 王
        "uni76EE",  # 目
        "uniFB01",  # ﬁ
        "uniFB02",  # ﬂ
        "uniFE45",  # ﹅
        "uniFE46",  # ﹆
        "uni4EDD",  # 仝
        "uni5182",  # 冂
        "uni5183",  # 冃
        "uni5184",  # 冄
        "uni5196",  # 冖
        "uni5199",  # 写
        "uni51AB",  # 冫
        "uni51AE",  # 冮
        "uni5369",  # 卩
        "uni536B",  # 卫
        "uni5382",  # 厂
        "uni5385",  # 厅
        "uni5388",  # 厈
        "uni53B6",  # 厶
        "uni53E3",  # 口
        "uni53E4",  # 古
        "uni53EA",  # 只
        "uni53F0",  # 台
        "uni56D7",  # 囗
        "uni572D",  # 圭
        "uni5B51",  # 孑
        "uni5B52",  # 孒
        "uni5B57",  # 字
        "uni5BF8",  # 寸
        "uni5C38",  # 尸
        "uni5DE8",  # 巨
        "uni5DF2",  # 已
        "uni5E75",  # 幵
        "uni5E76",  # 并
        "uni5E77",  # 幷
        "uni5E7F",  # 广
        "uni5EFE",  # 廾
        "uni5EFF",  # 廿
        "uni5F00",  # 开
        "uni5F13",  # 弓
        "uni5F16",  # 弖
        "uni5F73",  # 彳
        "uni5FC4",  # 忄
        "uni624B",  # 手
        "uni624C",  # 扌
        "uni6597",  # 斗
        "uni65B9",  # 方
        "uni65E5",  # 日
        "uni65E6",  # 旦
        "uni65E8",  # 旨
        "uni65E9",  # 早
        "uni65F1",  # 旱
        "uni660A",  # 昊
        "uni66F0",  # 曰
        "uni6708",  # 月
        "uni6728",  # 木
        "uni672A",  # 未
        "uni672B",  # 末
        "uni672C",  # 本
        "uni6C14",  # 气
        "uni6C35",  # 氵
        "uni7592",  # 疒
        "uni767D",  # 白
        "uni767E",  # 百
        "uni7681",  # 皁
        "uni7687",  # 皇
        "uni77E2",  # 矢
        "uni77F3",  # 石
        "uni793A",  # 示
        "uni793B",  # 礻
        "uni793C",  # 礼
        "uni7A74",  # 穴
        "uni7C73",  # 米
        "uni7F8A",  # 羊
        "uni7F8E",  # 美
        "uni8002",  # 耂
        "uni81FC",  # 臼
        "uni820C",  # 舌
        "uni820D",  # 舍
        "uni820E",  # 舎
        "uni8C55",  # 豕
        "uni8C9D",  # 貝
        "uni8C9E",  # 貞
        "uni8C9F",  # 貟
        "uni8CA0",  # 負
        "uni8CA2",  # 貢
        "uni8CAC",  # 責
        "uni8CB4",  # 貴
        "uni8CB5",  # 貵
        "uni8FB6",  # 辶
        "uni8FB7",  # 辷
        "uni8FBB",  # 辻
        "uni8FBD",  # 辽
        "uni8FC0",  # 迀
        "uni8FC1",  # 迁
        "uni8FC2",  # 迂
        "uni9577",  # 長
        "uni9578",  # 镸
        "uni961C",  # 阜
        "uni961D",  # 阝
        "uni9752",  # 青
        "uniFA5C",  # 臭
        "uniFA66",  # 辶
        "uniFFEE",  # ￮
        "uni20089",  # 𠂉
        "uni200A4",  # 𠂤
        "uni201A2",  # 𠆢
        "uni20628",  # 𠘨
        "uni20AD3",  # 𠫓
        "uni2123D",  # 𡈽
        "uni215D7",  # 𡗗
        "uni219C3",  # 𡧃
        "uni2634C",  # 𦍌
        "uni27FB7",  # 𧾷
        "uni2840C",  # 𨐌
        "uni28455",  # 𨑕
        "uni2967F",  # 𩙿
        "uni300E",  # 『（特別処理が入るためリスト入り）
        "uni300F",  # 』
        "uni3016",  # 〖
        "uni3017",  # 〗
        "uni3018",  # 〘
        "uni3019",  # 〙
        "uni300E.vert",  # 『
        "uni300F.vert",  # 』
        "uni300E.hwid",  # 『
        "uni300F.hwid",  # 』
        "uniFE46",  # ﹆
        "uni0022",  # "
        "uni00A8",  # ¨
        "uni00AB",  # «
        "uni00BB",  # »
        "uni02DD",  # ˝
        "uni0308",  # ̈
        "uni030B",  # ̋
        "uni030F",  # ̏
        "uni201C",  # “
        "uni201D",  # "
        "uni201E",  # „
        "uni2033",  # ″
        "uni226A",  # ≪
        "uni226B",  # ≫
        "uni3003",  # 〃
        "uni300A",  # 《
        "uni300B",  # 》
        "uni3034",  # 〴
        "uni3099",  # ゙
        "uni309B",  # ﾞ
        "uni309E",  # ゞ
        "uni30FE",  # ヾ
        "uni30FC",  # ｰ
        "uni30FD",  # ヽ
        "uni30FE",  # ヾ
        "uni30FF",  # ヿ
        "uni3100",  # ㄀
        "uni3101",  # ㄁
        "uni3102",  # ㄂
        "uni3103",  # ㄃
        "uni3104",  # ㄄
        "uniFF02",  # "
        "uniFF9E",  # ﾞ
        "uni301D.vert",  # 〝
        "uni301F.vert",  # 〟
        "uni309B.vert",  # ﾞ
        "uni309E.vert",  # ゞ
        "uni30FE.vert",  # ヾ
        "uni0021",  # !
        "uni0028",  # (
        "uni0029",  # )
        "uni002B",  # +
        "uni002F",  # /
        "uni0031",  # 1
        "uni003A",  # :
        "uni003B",  # ;
        "uni003C",  # <
        "uni003D",  # =
        "uni003E",  # >
        "uni0045",  # E
        "uni0046",  # F
        "uni0049",  # I
        "uni004C",  # L
        "uni0054",  # T
        "uni005B",  # [
        "uni005C",  # \
        "uni005D",  # ]
        "uni0066",  # f
        "uni0069",  # i
        "uni006A",  # j
        "uni006C",  # l
        "uni0074",  # t
        "uni007B",  # {
        "uni007C",  # |
        "uni007D"  # }
        }

    # リストのコードポイント範囲。
    # 範囲は終点が無視される点に注意
    sparselist_ranges = [
        range(0x2500, 0x2550),
        range(0x3008, 0x301C)
    ]

    # コードポイントが範囲内かチェック
    if glyph.unicode != -1:  # コードポイントを持つ場合のみチェック
        for r in sparselist_ranges:
            if glyph.unicode in r:
                return True  # リストに該当する場合はTrueを返す

    # グリフ名がリストにあるかチェック
    if glyph.glyphname in sparselist_set:
        return True
    else:
        return False

if __name__ == "__main__":
    main()
