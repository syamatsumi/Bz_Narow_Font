# utils/__init__.py

# オンカーブポイント2つだけのエレメント、たぶんゴミなので削除する。
# rm_littleline(glyph, min_distance=20)
from .ys_fontforge_Remove_artifacts import ys_rm_little_line

# バウンディングボックスで判定して、しきい値以下のオブジェクトは削除する。
# rm_smallpoly(width_threshold, height_threshold, glyph)
from .ys_fontforge_Remove_artifacts import ys_rm_small_poly



# 自己交差の解消スクリプト。極端な角度を丸める効果を持つ。
# 処理後はglyph.removeOverlap()で重複した点を消すこと。
# rm_self_insec(glyph, angle_threshold=2)
from .ys_fontforge_Repair_Self_Intersections import ys_repair_Self_Insec

# ノコギリ歯状になっている部分を平らにする。
# 1単位以下に近接したポイントを一箇所に纏めて実質的に均す。
# ys_sawtooth_reduction(glyph)
from .ys_fontforge_Repair_Self_Intersections import ys_sawtooth_reduction



# パスを閉じてみて、閉じられないパスは削除する
# ys_closepath(glyph)
from .ys_fontforge_tryfix import ys_closepath

# 自己交差解消スクリプトで角度を広げつつ再試行する。
# 1～6度までやってみて、ダメでも1度の解消は適用する。
# ys_Repair_Self_Intersections(glyph)
from .ys_fontforge_tryfix import ys_repair_si_chain

# 拡大縮小と単純化で誤差が上手くまるまって修正されないかなぁって関数。
# ys_rescale_chain(glyph)
from .ys_fontforge_tryfix import ys_rescale_chain

# 細かい単純化の設定を行ったもの
# ys_simplify(glyph)
from .ys_fontforge_tryfix import ys_simplify



# 横にずらしてはっつければ、上手いこと
# 幅だけ広がってくれるんじゃねというブツ。
# ys_widepaste(rwidth, rheight, glyph)
from .ys_fontforge_widestroke import ys_widepaste

# 幅を広げるためのストロークを追加する。
# 超高確率で自己交差を発生させるので処置必須。
# ys_widestroke(stroke_width, glyph)
from .ys_fontforge_widestroke import ys_widestroke




