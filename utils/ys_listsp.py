#!fontforge --lang=py -script

import fontforge

def ys_sparselist(glyph):
    sparselist_set = {
        "uni4E00",  # 一
        "uni4E01",  # 丁
        "uni4E03",  # 七
        "uni4E09",  # 三
        "uni4E36",  # 丶
        "uni4E59",  # 乙
        "uni4E5A",  # 乚
        "uni4E5D",  # 九
        "uni4E5E",  # 乞
        "uni4E85",  # 亅
        "uni4E86",  # 了
        "uni4E8C",  # 二
        "uni4E94",  # 五
        "uni4E9E",  # 亞
        "uni4EA0",  # 亠
        "uni4EA1",  # 亡
        "uni4EA2",  # 亢
        "uni4EA3",  # 亣
        "uni4EA4",  # 交
        "uni4EBA",  # 人
        "uni4EC1",  # 仁
        "uni4ECA",  # 今
        "uni513F",  # 儿
        "uni5140",  # 兀
        "uni5141",  # 允
        "uni5142",  # 兂
        "uni5143",  # 元
        "uni5144",  # 兄
        "uni5145",  # 充
        "uni514B",  # 克
        "uni5165",  # 入
        "uni5168",  # 全
        "uni516B",  # 八
        "uni516C",  # 公
        "uni516D",  # 六
        "uni516F",  # 兯
        "uni5170",  # 兰
        "uni5171",  # 共
        "uni5172",  # 兲
        "uni5173",  # 关
        "uni5174",  # 兴
        "uni5175",  # 兵
        "uni51E0",  # 几
        "uni51E1",  # 凡
        "uni51E2",  # 凢
        "uni51E3",  # 凣
        "uni51F5",  # 凵
        "uni51F6",  # 凶
        "uni51F7",  # 凷
        "uni51F8",  # 凸
        "uni51F9",  # 凹
        "uni51FA",  # 出
        "uni51FB",  # 击
        "uni5200",  # 刀
        "uni5201",  # 刁
        "uni5202",  # 刂
        "uni5203",  # 刃
        "uni5204",  # 刄
        "uni5205",  # 刅
        "uni5206",  # 分
        "uni529B",  # 力
        "uni52F9",  # 勹
        "uni52FA",  # 勺
        "uni52FB",  # 勻
        "uni52FD",  # 勽
        "uni5300",  # 匀
        "uni5315",  # 匕
        "uni5316",  # 化
        "uni5317",  # 北
        "uni531A",  # 匚
        "uni531E",  # 匞
        "uni5321",  # 匡
        "uni5338",  # 匸
        "uni5339",  # 匹
        "uni533A",  # 区
        "uni5341",  # 十
        "uni5342",  # 卂
        "uni5343",  # 千
        "uni5344",  # 卄
        "uni5348",  # 午
        "uni5349",  # 卉
        "uni534A",  # 半
        "uni534B",  # 卋
        "uni534D",  # 卍
        "uni534E",  # 华
        "uni5350",  # 卐
        "uni535C",  # 卜
        "uni535D",  # 卝
        "uni535E",  # 卞
        "uni5360",  # 占
        "uni5361",  # 卡
        "uni5362",  # 卢
        "uni53E3",  # 口
        "uni53F3",  # 右
        "uni5408",  # 合
        "uni571F",  # 土
        "uni58EB",  # 士
        "uni58EC",  # 壬
        "uni5915",  # 夕
        "uni5927",  # 大
        "uni5929",  # 天
        "uni592B",  # 夫
        "uni592E",  # 央
        "uni59BB",  # 妻
        "uni5B50",  # 子
        "uni5DE5",  # 工
        "uni5DE6",  # 左
        "uni5DF1",  # 己
        "uni5DF3",  # 巳
        "uni5DFE",  # 巾
        "uni5E72",  # 干
        "uni5E74",  # 年
        "uni5E78",  # 幸
        "uni6238",  # 戸
        "uni624B",  # 手
        "uni624C",  # 扌
        "uni624D",  # 才
        "uni6597",  # 斗
        "uni65E5",  # 日
        "uni6614",  # 昔
        "uni6708",  # 月
        "uni6728",  # 木
        "uni672C",  # 本
        "uni6C34",  # 水
        "uni706B",  # 火
        "uni738B",  # 王
        "uni76EE",  # 目
        "uni8DB3",  # 足
        "uniFB01",  # ﬁ
        "uniFB02",  # ﬂ
        "uniFE45",  # ﹅
        "uniFE46",  # ﹆
        "uni4ECA",  # 今
        "uni4ECB",  # 介
        "uni4ECC",  # 仌
        "uni4ECF",  # 仏
        "uni4ED0",  # 仐
        "uni4ED1",  # 仑
        "uni4ED2",  # 仒
        "uni4ED3",  # 仓
        "uni4EDB",  # 仛
        "uni4EDC",  # 仜
        "uni4EDD",  # 仝
        "uni5182",  # 冂
        "uni5183",  # 冃
        "uni5184",  # 冄
        "uni5187",  # 冇
        "uni5188",  # 冈
        "uni5196",  # 冖
        "uni5197",  # 冗
        "uni5198",  # 冘
        "uni5199",  # 写
        "uni519D",  # 冝
        "uni51AB",  # 冫
        "uni51AC",  # 冬
        "uni51AD",  # 冭
        "uni51AE",  # 冮
        "uni51B1",  # 冱
        "uni51B2",  # 冲
        "uni51B5",  # 况
        "uni51B8",  # 冸
        "uni5369",  # 卩
        "uni536A",  # 卪
        "uni536B",  # 卫
        "uni5382",  # 厂
        "uni5383",  # 厃
        "uni5385",  # 厅
        "uni5387",  # 厇
        "uni5388",  # 厈
        "uni538B",  # 压
        "uni538F",  # 厏
        "uni53B6",  # 厶
        "uni53B7",  # 厷
        "uni53B9",  # 厹
        "uni53BA",  # 厺
        "uni53BB",  # 去
        "uni53BC",  # 厼
        "uni53C8",  # 又
        "uni53C9",  # 叉
        "uni53CB",  # 友
        "uni53CD",  # 反
        "uni53E3",  # 口
        "uni53E4",  # 古
        "uni53EA",  # 只
        "uni53EC",  # 召
        "uni53EF",  # 可
        "uni53F0",  # 台
        "uni53F2",  # 史
        "uni53F3",  # 右
        "uni53F4",  # 叴
        "uni53F6",  # 叶
        "uni53F7",  # 号
        "uni53F8",  # 司
        "uni56D7",  # 囗
        "uni5721",  # 圡
        "uni5722",  # 圢
        "uni5723",  # 圣
        "uni5724",  # 圤
        "uni5725",  # 圥
        "uni5727",  # 圧
        "uni5728",  # 在
        "uni5729",  # 圩
        "uni572D",  # 圭
        "uni572E",  # 圮
        "uni573C",  # 圼
        "uni58ED",  # 壭
        "uni58EE",  # 壮
        "uni58F1",  # 壱
        "uni58F2",  # 売
        "uni58F3",  # 壳
        "uni58F4",  # 壴
        "uni58F5",  # 壵
        "uni5902",  # 夂
        "uni5905",  # 夅
        "uni5906",  # 夆
        "uni590A",  # 夊
        "uni5916",  # 外
        "uni5928",  # 夨
        "uni592A",  # 太
        "uni592C",  # 夬
        "uni592D",  # 夭
        "uni592F",  # 夯
        "uni5930",  # 夰
        "uni5931",  # 失
        "uni5932",  # 夲
        "uni5933",  # 夳
        "uni5934",  # 头
        "uni5973",  # 女
        "uni5B51",  # 孑
        "uni5B52",  # 孒
        "uni5B53",  # 孓
        "uni5B57",  # 字
        "uni5948",  # 奈
        "uni5BF8",  # 寸
        "uni5BFA",  # 寺
        "uni5BFB",  # 寻
        "uni5BFC",  # 导
        "uni5BFF",  # 寿
        "uni5C10",  # 尐
        "uni5C24",  # 尤
        "uni5C38",  # 尸
        "uni5C39",  # 尹
        "uni5C3A",  # 尺
        "uni5DE8",  # 巨
        "uni5DF2",  # 已
        "uni5E75",  # 幵
        "uni5E76",  # 并
        "uni5E77",  # 幷
        "uni5E7F",  # 广
        "uni5E80",  # 庀
        "uni5E81",  # 庁
        "uni5E84",  # 庄
        "uni5EF4",  # 廴
        "uni5EFE",  # 廾
        "uni5EFF",  # 廿
        "uni5F00",  # 开
        "uni5F01",  # 弁
        "uni5F02",  # 异
        "uni5F03",  # 弃
        "uni5F04",  # 弄
        "uni5F05",  # 弅
        "uni5F06",  # 弆
        "uni5F07",  # 弇
        "uni5F0B",  # 弋
        "uni5F0C",  # 弌
        "uni5F0D",  # 弍
        "uni5F0E",  # 弎
        "uni5F0F",  # 式
        "uni5F10",  # 弐
        "uni5F13",  # 弓
        "uni5F14",  # 弔
        "uni5F15",  # 引
        "uni5F16",  # 弖
        "uni5F61",  # 彡
        "uni5F73",  # 彳
        "uni5F7A",  # 彺
        "uni5FC4",  # 忄
        "uni624B",  # 手
        "uni624C",  # 扌
        "uni624D",  # 才
        "uni652F",  # 支
        "uni6534",  # 攴
        "uni6535",  # 攵
        "uni6587",  # 文
        "uni6588",  # 斈
        "uni6589",  # 斉
        "uni658A",  # 斊
        "uni6597",  # 斗
        "uni65A4",  # 斤
        "uni65A5",  # 斥
        "uni65B9",  # 方
        "uni65E0",  # 无
        "uni65E1",  # 旡
        "uni65E5",  # 日
        "uni65E6",  # 旦
        "uni65E7",  # 旧
        "uni65E8",  # 旨
        "uni65E9",  # 早
        "uni65EC",  # 旬
        "uni65EB",  # 旫
        "uni65F0",  # 旰
        "uni65F1",  # 旱
        "uni65EE",  # 旮
        "uni65EF",  # 旯
        "uni65F2",  # 旲
        "uni65F3",  # 旳
        "uni65F4",  # 旴
        "uni65F5",  # 旵
        "uni65F6",  # 时
        "uni65F7",  # 旷
        "uni660A",  # 昊
        "uni660B",  # 昋
        "uni660C",  # 昌
        "uni660D",  # 昍
        "uni660E",  # 明
        "uni66F0",  # 曰
        "uni6708",  # 月
        "uni6709",  # 有
        "uni6728",  # 木
        "uni6729",  # 朩
        "uni672A",  # 未
        "uni672B",  # 末
        "uni672C",  # 本
        "uni672D",  # 札
        "uni672F",  # 术
        "uni6730",  # 朰
        "uni6731",  # 朱
        "uni6B62",  # 止
        "uni6B63",  # 正
        "uni6B79",  # 歹
        "uni6B7A",  # 歺
        "uni6C0F",  # 氏
        "uni6C10",  # 氐
        "uni6C11",  # 民
        "uni6C14",  # 气
        "uni6C15",  # 氕
        "uni6C17",  # 気
        "uni6C35",  # 氵
        "uni7592",  # 疒
        "uni767D",  # 白
        "uni767E",  # 百
        "uni7680",  # 皀
        "uni7681",  # 皁
        "uni7682",  # 皂
        "uni7683",  # 皃
        "uni7687",  # 皇
        "uni77E2",  # 矢
        "uni77F3",  # 石
        "uni793A",  # 示
        "uni793B",  # 礻
        "uni793C",  # 礼
        "uni793E",  # 社
        "uni7A74",  # 穴
        "uni7ACB",  # 立
        "uni7AF9",  # 竹
        "uni7AFA",  # 竺
        "uni7C73",  # 米
        "uni7F36",  # 缶
        "uni7F8A",  # 羊
        "uni7F8C",  # 羌
        "uni7F8E",  # 美
        "uni8001",  # 老
        "uni8002",  # 耂
        "uni8003",  # 考
        "uni81E3",  # 臣
        "uni81FC",  # 臼
        "uni820C",  # 舌
        "uni820D",  # 舍
        "uni820E",  # 舎
        "uni821F",  # 舟
        "uni826E",  # 艮
        "uni826F",  # 良
        "uni8272",  # 色
        "uni8279",  # 艹
        "uni827A",  # 艺
        "uni827B",  # 艻
        "uni827C",  # 艼
        "uni827D",  # 艽
        "uni827E",  # 艾
        "uni827F",  # 艿
        "uni8280",  # 芀
        "uni8281",  # 芁
        "uni8282",  # 节
        "uni8283",  # 芃
        "uni8284",  # 芄
        "uni8285",  # 芅
        "uni8863",  # 衣
        "uni8864",  # 衤
        "uni8C46",  # 豆
        "uni8C55",  # 豕
        "uni8C9D",  # 貝
        "uni8C9E",  # 貞
        "uni8C9F",  # 貟
        "uni8CA0",  # 負
        "uni8CA2",  # 貢
        "uni8CAC",  # 責
        "uni8CB4",  # 貴
        "uni8CB5",  # 貵
        "uni8EAB",  # 身
        "uni8FB6",  # 辶
        "uni8FB7",  # 辷
        "uni8FBB",  # 辻
        "uni8FBD",  # 辽
        "uni8FC0",  # 迀
        "uni8FC1",  # 迁
        "uni8FC2",  # 迂
        "uni9577",  # 長
        "uni9578",  # 镸
        "uni9580",  # 門
        "uni961C",  # 阜
        "uni961D",  # 阝
        "uni9752",  # 青
        "uni975E",  # 非
        "uniFA3C",  # 屮
        "uniFA55",  # 突
        "uniFA5C",  # 臭
        "uniFA66",  # 辶
        "uniFFEE",  # ￮
        "uni2000B",  # 𠀋
        "uni20089",  # 𠂉
        "uni200A4",  # 𠂤
        "uni201A2",  # 𠆢
        "uni20628",  # 𠘨
        "uni2097C",  # 𠥼
        "uni2099D",  # 𠦝
        "uni20AD3",  # 𠫓
        "uni2123D",  # 𡈽
        "uni215D7",  # 𡗗
        "uni219C3",  # 𡧃
        "uni2634C",  # 𦍌
        "uni26AFF",  # 𦫿
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
        }

    # リストのコードポイント範囲。
    # 範囲は終点が無視されるため指定範囲は終点+1
    sparselist_ranges = [
        range(0x21, 0x39 + 1),
        range(0x42, 0x4C + 1),
        range(0x4E, 0x56 + 1),
        range(0x58, 0x6C + 1),
        range(0x6E, 0x76 + 1),
        range(0x78, 0x7F + 1),
        range(0x3000, 0x301F + 1),
        range(0x3030, 0x30FF + 1),
        range(0x31F0, 0x31FF + 1),
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