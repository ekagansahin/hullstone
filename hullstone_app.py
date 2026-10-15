# Hullstone — faceted stone designer (Streamlit UI)
# Run:  pip install -r requirements.txt
#       streamlit run hullstone_app.py
import io
import struct
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy.spatial import ConvexHull, QhullError

from i18n import DEFAULT_LANG, LANGS, translator

# PNG instead of an emoji: the favicon looks the same on every OS and browser.
ICON = Path(__file__).parent / "assets" / "icon.png"
st.set_page_config(page_title="Hullstone",
                   page_icon=str(ICON) if ICON.exists() else ":material/diamond:",
                   layout="wide")

DEFAULT_BASE = pd.DataFrame(
    [(0, 0, 0), (45, -5, 0), (60, 20, 0), (40, 45, 0), (-20, 25, 0)],
    columns=["x", "y", "z"], dtype=float)
DEFAULT_TOP = pd.DataFrame(
    [(30, 0, 22), (48, 15, 30), (38, 38, 34), (15, 35, 30), (8, 15, 26), (-18, 25, 2)],
    columns=["x", "y", "z"], dtype=float)

AXES = ("x", "y", "z")
# Default min/max size of the bounding box per axis, mm
DEFAULT_LIMITS = {"x": (60.0, 90.0), "y": (40.0, 60.0), "z": (25.0, 40.0)}
LIMIT_TOL = 0.05  # rounding tolerance, mm


# ---------- geometry ----------
def build_mesh(pts: np.ndarray):
    """Convex hull; returns triangles with outward-facing normals."""
    hull = ConvexHull(pts)
    c = pts.mean(0)
    tris = []
    for s in hull.simplices:
        a, b, d = pts[s]
        n = np.cross(b - a, d - a)
        if np.dot(n, a - c) < 0:
            b, d = d, b
            n = -n
        tris.append((n / np.linalg.norm(n), a, b, d))
    return tris, hull.volume, count_facets(hull)


def count_facets(hull) -> int:
    """Counts coplanar triangles as a single face."""
    return len(np.unique(np.round(hull.equations, 5), axis=0))


def _spread_sample(sampler, n, rng, min_gap, tries=4000):
    """Picks n points that are not too close to each other (in normalized coordinates)."""
    out = []
    while len(out) < n:
        for _ in range(tries):
            p = sampler(rng)
            if all(np.linalg.norm(p - q) >= min_gap for q in out):
                out.append(p)
                break
        else:
            min_gap *= 0.8  # relax the spacing if they don't fit
    return np.array(out)


def random_shape(n_faces: int, rng, limits=DEFAULT_LIMITS):
    """Random flat-bottomed convex block with exactly n_faces planar faces.

    From Euler's formula, for a k-sided base and triangular side faces:
    faces = 2*(top points) + k - 1  →  top points = (faces + 1 - k) / 2

    limits: {"x": (min, max), "y": ..., "z": ...} in mm. On each attempt a target
    size is drawn from this range per axis and the bounding box is set to exactly it.
    """
    ks = [k for k in range(3, min(9, n_faces))
          if (n_faces + 1 - k) % 2 == 0 and (n_faces + 1 - k) // 2 >= 1]
    for _ in range(300):
        target = np.array([round(rng.uniform(*limits[ax]), 1) for ax in AXES])
        a, b, c = target[0] / 2, target[1] / 2, target[2]
        k = int(rng.choice(ks))
        n_top = (n_faces + 1 - k) // 2

        # base: k points on an ellipse (convex by construction)
        ang = _spread_sample(lambda r: np.array([r.uniform(0, 2 * np.pi)]), k, rng,
                             min_gap=1.2 * np.pi / k)[:, 0]
        ang.sort()
        base = np.c_[a * np.cos(ang), b * np.sin(ang), np.zeros(k)]

        # top: points on an ellipsoid surface -> every one becomes a hull vertex
        def on_dome(r):
            t = r.uniform(0.15, 0.97)
            phi = r.uniform(0, 2 * np.pi)
            rr = np.sqrt(1 - t * t)
            return np.array([rr * np.cos(phi), rr * np.sin(phi), t])
        u = _spread_sample(on_dome, n_top, rng, min_gap=1.6 / np.sqrt(n_top + 1))
        top = u * [a, b, c]

        # random shear so the part looks asymmetric
        sx, sy = rng.uniform(-0.45, 0.45, 2)
        top[:, 0] += sx * top[:, 2]
        top[:, 1] += sy * top[:, 2]

        # scale per axis so the bounding box sits at the origin with size exactly `target`.
        # Affine map: planes stay planar and the shape stays convex.
        pts = np.vstack([base, top])
        lo, hi = pts.min(0), pts.max(0)
        if np.any(hi - lo < 1e-9):
            continue
        pts = np.round((pts - lo) / (hi - lo) * target, 1)
        try:
            hull = ConvexHull(pts)
        except QhullError:
            continue
        if count_facets(hull) == n_faces and len(hull.vertices) == len(pts):
            cols = list(AXES)
            return pd.DataFrame(pts[:k], columns=cols), pd.DataFrame(pts[k:], columns=cols)
    raise GenerationError(n_faces)


class GenerationError(ValueError):
    """No shape with the requested face count was found (message is translated in the UI)."""


def fit_to_limits(pts: np.ndarray, limits) -> np.ndarray:
    """Scales each out-of-range axis independently to the nearest limit.

    The lower corner of the bounding box stays fixed (a z = 0 base stays in place).
    """
    lo = pts.min(0)
    size = pts.max(0) - lo
    f = np.ones(3)
    for i, ax in enumerate(AXES):
        mn, mx = limits[ax]
        if size[i] > 1e-9:
            f[i] = np.clip(size[i], mn, mx) / size[i]
    return lo + (pts - lo) * f


def limit_violations(size, limits) -> list[tuple]:
    """Axes outside the limits: [(axis, size, min, max), ...]"""
    out = []
    for i, ax in enumerate(AXES):
        mn, mx = limits[ax]
        if size[i] < mn - LIMIT_TOL or size[i] > mx + LIMIT_TOL:
            out.append((ax, size[i], mn, mx))
    return out


def stl_bytes(tris) -> bytes:
    buf = io.BytesIO()
    buf.write(b"hullstone".ljust(80, b"\0"))
    buf.write(struct.pack("<I", len(tris)))
    for n, a, b, d in tris:
        buf.write(struct.pack("<12fH", *n, *a, *b, *d, 0))
    return buf.getvalue()


def plot_mesh(tris, pts):
    verts = np.array([v for _, a, b, d in tris for v in (a, b, d)])
    i = np.arange(0, len(verts), 3)
    fig = go.Figure()
    fig.add_trace(go.Mesh3d(
        x=verts[:, 0], y=verts[:, 1], z=verts[:, 2], i=i, j=i + 1, k=i + 2,
        color="#3a4250", flatshading=True, opacity=1.0,
        lighting=dict(ambient=0.35, diffuse=0.9, specular=0.15, roughness=0.8),
        lightposition=dict(x=200, y=100, z=300), hoverinfo="skip"))
    # edges
    ex, ey, ez = [], [], []
    for _, a, b, d in tris:
        for p, q in ((a, b), (b, d), (d, a)):
            ex += [p[0], q[0], None]; ey += [p[1], q[1], None]; ez += [p[2], q[2], None]
    fig.add_trace(go.Scatter3d(x=ex, y=ey, z=ez, mode="lines",
                               line=dict(color="#c9d1dc", width=2), hoverinfo="skip"))
    # control points
    fig.add_trace(go.Scatter3d(
        x=pts[:, 0], y=pts[:, 1], z=pts[:, 2], mode="markers+text",
        marker=dict(size=4, color="#e8a33d"),
        text=[str(k) for k in range(len(pts))], textposition="top center",
        hovertemplate="P%{text}: (%{x:.1f}, %{y:.1f}, %{z:.1f})<extra></extra>"))
    fig.update_layout(
        showlegend=False, height=620, margin=dict(l=0, r=0, t=0, b=0),
        scene=dict(aspectmode="data",
                   xaxis_title="X (mm)", yaxis_title="Y (mm)", zaxis_title="Z (mm)"))
    return fig


# ---------- state ----------
if "base" not in st.session_state:
    st.session_state.base = DEFAULT_BASE.copy()
    st.session_state.top = DEFAULT_TOP.copy()
    st.session_state.scale = 1.0
    st.session_state.result = None


def regenerate():
    pts = pd.concat([st.session_state.base, st.session_state.top]).dropna().to_numpy(float)
    pts = pts * st.session_state.scale
    # err holds a translation key; the text is rendered in the selected language
    if len(pts) < 4:
        st.session_state.result = dict(err="err_min_points")
        return
    try:
        tris, vol, faces = build_mesh(pts)
        st.session_state.result = dict(pts=pts, tris=tris, vol=vol, faces=faces, err=None)
    except (QhullError, ValueError):
        st.session_state.result = dict(err="err_flat")


def fit_state_to_limits(limits):
    """Fits the current points (scale included) to the limits and resets scale to 1."""
    sc = st.session_state.scale
    b = st.session_state.base.dropna().to_numpy(float) * sc
    t = st.session_state.top.dropna().to_numpy(float) * sc
    pts = np.round(fit_to_limits(np.vstack([b, t]), limits), 2)
    cols = list(AXES)
    st.session_state.base = pd.DataFrame(pts[:len(b)], columns=cols)
    st.session_state.top = pd.DataFrame(pts[len(b):], columns=cols)
    st.session_state.scale = 1.0
    for k in ("ed_base", "ed_top"):
        st.session_state.pop(k, None)
    regenerate()


if st.session_state.result is None:
    regenerate()

# ---------- language ----------
if "lang" not in st.session_state:
    q = st.query_params.get("lang", DEFAULT_LANG)
    st.session_state.lang = q if q in LANGS else DEFAULT_LANG


def _sync_lang_param():
    # Keep the language in the URL (?lang=tr) so it survives reloads and shared links.
    st.query_params["lang"] = st.session_state.lang


t = translator(st.session_state.lang)

# ---------- UI ----------
head_l, head_r = st.columns([5, 1], vertical_alignment="bottom")
head_l.title("Hullstone")
head_r.selectbox(":material/language: " + t("lang_label"), list(LANGS),
                 format_func=LANGS.get, key="lang", on_change=_sync_lang_param)
st.caption(t("caption"))

left, right = st.columns([1, 2], gap="large")

with left:
    st.subheader(t("limits_header"))
    limits, bad = {}, []
    for ax in AXES:
        lo_def, hi_def = DEFAULT_LIMITS[ax]
        c_min, c_max = st.columns(2)
        mn = c_min.number_input(f"{ax.upper()} min", 1.0, 2000.0, lo_def, 1.0,
                                key=f"lim_{ax}_min")
        mx = c_max.number_input(f"{ax.upper()} max", 1.0, 2000.0, hi_def, 1.0,
                                key=f"lim_{ax}_max")
        limits[ax] = (float(mn), float(mx))
        if mn > mx:
            bad.append(ax.upper())
    limits_ok = not bad
    if not limits_ok:
        st.error(t("limits_bad", axes=", ".join(bad)))
    st.caption(t("limits_caption"))

    st.subheader(t("random_header"))
    rc1, rc2 = st.columns([1, 1], vertical_alignment="bottom")
    n_faces = rc1.number_input(t("n_faces"), min_value=4, max_value=40, value=10, step=1,
                               help=t("n_faces_help"), key="n_faces")
    if rc2.button(t("generate"), type="primary", width="stretch",
                  disabled=not limits_ok, key="btn_generate"):
        try:
            b_df, t_df = random_shape(int(n_faces), np.random.default_rng(), limits)
            st.session_state.base, st.session_state.top = b_df, t_df
            st.session_state.scale = 1.0
            for k in ("ed_base", "ed_top"):
                st.session_state.pop(k, None)
            regenerate()
            st.rerun()
        except GenerationError:
            st.error(t("gen_failed", n=int(n_faces)))

    with st.form("params"):
        st.subheader(t("base_header"))
        base = st.data_editor(st.session_state.base, num_rows="dynamic",
                              width="stretch", key="ed_base")
        st.subheader(t("top_header"))
        top = st.data_editor(st.session_state.top, num_rows="dynamic",
                             width="stretch", key="ed_top")
        scale = st.number_input(t("scale"), 0.1, 10.0, st.session_state.scale, 0.1)
        c1, c2 = st.columns(2)
        apply = c1.form_submit_button(t("apply"), type="primary", width="stretch")
        reset = c2.form_submit_button(t("reset"), width="stretch")

    if apply:
        st.session_state.base, st.session_state.top = base, top
        st.session_state.scale = scale
        regenerate()
        st.rerun()
    if reset:
        st.session_state.base = DEFAULT_BASE.copy()
        st.session_state.top = DEFAULT_TOP.copy()
        st.session_state.scale = 1.0
        for k in ("ed_base", "ed_top"):
            st.session_state.pop(k, None)
        regenerate()
        st.rerun()

    st.info(t("tip"))

with right:
    r = st.session_state.result
    if r["err"]:
        st.error(t(r["err"]))
    else:
        st.plotly_chart(plot_mesh(r["tris"], r["pts"]), width="stretch")
        size = r["pts"].max(0) - r["pts"].min(0)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(t("m_size"), f"{size[0]:.0f}×{size[1]:.0f}×{size[2]:.0f}")
        m2.metric(t("m_volume"), f"{r['vol'] / 1000:.1f} cm³")
        m3.metric(t("m_faces"), r["faces"])
        m4.metric(t("m_tris"), len(r["tris"]))
        viol = limit_violations(size, limits)
        if not limits_ok:
            pass
        elif viol:
            items = "; ".join(t("violation_item", ax=ax.upper(), v=f"{v:.1f}",
                                mn=f"{mn:g}", mx=f"{mx:g}") for ax, v, mn, mx in viol)
            st.warning(t("out_of_limits", items=items))
            if st.button(t("fit"), width="stretch", help=t("fit_help"), key="btn_fit"):
                fit_state_to_limits(limits)
                st.rerun()
        else:
            st.success(t("in_limits"))
        if r["pts"][:, 2].min() < -1e-6:
            st.warning(t("below_bed"))
        st.download_button(t("download"), stl_bytes(r["tris"]),
                           file_name="hullstone.stl", mime="model/stl",
                           type="primary", width="stretch", key="btn_download")

# ---------- footer ----------
st.divider()
st.markdown(
    "<div style='text-align:center; opacity:0.6; font-size:0.85rem;'>"
    "© 2026 Kağan ŞAHİN</div>",
    unsafe_allow_html=True)
