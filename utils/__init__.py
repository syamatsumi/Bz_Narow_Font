# utils/__init__.py


# パスを閉じてみて、閉じられないパスは削除する
# ys_closepath(glyph)
from .ys_fontforge_Remove_artifacts import ys_closepath

# 周長に対して極端に面積の小さなコンターを削除する関数。
# でかくて細長いコンターを巻き込むことがあるので、
# 全体の面積比から見て充分小さいものに限定する。
# ys_rm_spikecontours(glyph, c_thresh=0.1, g_thresh=0.001, p_thresh=10)
from .ys_fontforge_Remove_artifacts import ys_rm_spikecontours

# オンカーブポイント2つだけの孤立したエレメント、たぶんゴミなので削除する。
# rm_littleline(glyph, min_distance=20)
from .ys_fontforge_Remove_artifacts import ys_rm_isolatepath

# バウンディングボックスで判定して、しきい値以下のオブジェクトは削除する。
#  ys_rm_small_poly(glyph, width_threshold, height_threshold)
from .ys_fontforge_Remove_artifacts import ys_rm_small_poly



# 自己交差の解消スクリプト。極端な角度を丸める効果を持つ。
# 処理後はglyph.removeOverlap()で重複した点を消すこと。
# rm_self_insec(glyph, angle_threshold=2)
from .ys_fontforge_Repair_spikes import ys_repair_spikes



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



# 幅を広げるためのストロークを追加する。
# 超高確率で自己交差を発生させるので処置必須。
# ys_widestroke(glyph, stroke_width, storoke_height)
from .ys_fontforge_widestroke import ys_widestroke



# 白抜き文字に拡幅処理をかけると文字が崩れるので、
# 問題となる処理から除外するためのリストとフラグ処理のために。
# 外部データ化した方がいいのかもしれんけど。
# ys_list_invglyph(input_str, flag)
from .ys_listbk import ys_blacklist
from .ys_listwh import ys_whitelist
from .ys_listig import ys_ignorlist
from .ys_listsp import ys_sparselist
from .ys_listsw import ys_swaplist, ys_pswaplist
