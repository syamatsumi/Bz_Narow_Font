# utils/__init__.py

# 自己交差の解消スクリプト。極端な角度を丸める効果を持つ。
# 処理後はglyph.removeOverlap()で重複した点を消すこと。
# rm_self_insec(glyph, angle_threshold=2)
from .ys_fontforge_Repair_Self_Intersections import ys_repair_Self_Insec

# 上の自己交差解消スクリプトの改善前のもの
# trim_spikes(glyph, angle_threshold=2)
from .ys_fontforge_trim_spikes import ys_trim_spikes

# オンカーブポイント2つだけのエレメント、たぶんゴミなので削除する。
# rm_littleline(glyph, min_distance=20)
from .ys_fontforge_Remove_artifacts import ys_rm_little_line

# バウンディングボックスで判定して、しきい値以下のオブジェクトは削除する。
# rm_smallpoly(width_threshold, height_threshold, glyph)
from .ys_fontforge_Remove_artifacts import ys_rm_small_poly

# パスを閉じてみて、閉じられないパスは削除する
# ys_closepath(glyph)
from .ys_fontforge_tryfix import ys_closepath

# 細かい単純化の設定を行ったもの
# ys_simplify(glyph)
from .ys_fontforge_tryfix import ys_simplify

# 拡大縮小と単純化で誤差が上手くまるまって修正されないかなぁって関数。
# ys_rescale_chain(glyph)
from .ys_fontforge_tryfix import ys_rescale_chain

# 拡大縮小と単純化で誤差が上手くまるまって修正されないかなぁって関数。
# ys_widestroke(stroke_width, glyph)
from .ys_fontforge_widestroke import ys_widestroke

