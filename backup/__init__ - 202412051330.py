# utils/__init__.py

# オンカーブポイント2つだけのエレメント、たぶんゴミなので削除する。
# rm_littleline(glyph, min_distance=20)
from .ys_fontforge_Remove_artifacts import ys_rm_little_line

# バウンディングボックスで判定して、しきい値以下のオブジェクトは削除する。
#  ys_rm_small_poly(glyph, width_threshold, height_threshold)
from .ys_fontforge_Remove_artifacts import ys_rm_small_poly



# 自己交差の解消スクリプト。極端な角度を丸める効果を持つ。
# 処理後はglyph.removeOverlap()で重複した点を消すこと。
# rm_self_insec(glyph, angle_threshold=2)
from .ys_fontforge_Repair_Self_Intersections import ys_repair_Self_Insec



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



# 輪郭の右辺だけを引き延ばします。
# 逆方向の輪郭は左辺が縮小します。
# ys_expand_Xweight(glyph, offset)
from .ys_fontforge_widestroke import ys_expand_Xweight

# 幅を広げるためのストロークを追加する。
# 超高確率で自己交差を発生させるので処置必須。
# ys_widestroke(glyph, stroke_width, storoke_height)
from .ys_fontforge_widestroke import ys_widestroke




