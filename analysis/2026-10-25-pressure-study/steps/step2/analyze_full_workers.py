"""Pure worker functions for analyze_full.py (imported by the main script and by its process-pool children).

Kept in a separate module so that Windows 'spawn' children import only this file, never the analysis script.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd


def rankdata(x):
    return pd.Series(x).rank().to_numpy()


def int_rank(codes_):
    """Average ranks for small-integer codes (fast, tie-aware)."""
    cnt = np.bincount(codes_)
    cum = np.cumsum(cnt)
    avg = cum - (cnt - 1) / 2.0
    return avg[codes_]


def stat_fast(xc, ptype, yc, yr, okind):
    """Effect magnitude only (for permutation / bootstrap). For ptype 'num', xc must already be ranks."""
    if ptype in ("ord", "num"):
        rx = int_rank(xc) if ptype == "ord" else xc
        if rx.std() == 0 or yr.std() == 0:
            return 0.0
        return abs(float(np.corrcoef(rx, yr)[0, 1]))
    ng = xc.max() + 1
    if okind == "bin":
        tab = np.bincount(xc * 2 + yc, minlength=ng * 2).reshape(ng, 2).astype(float)
        tab = tab[tab.sum(1) > 0]
        n = tab.sum()
        if tab.shape[0] < 2 or (tab.sum(0) == 0).any():
            return 0.0
        exp = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / n
        chi = ((tab - exp) ** 2 / exp).sum()
        r, k = tab.shape[0], 2
        phi2c = max(0.0, chi / n - (k - 1) * (r - 1) / (n - 1))
        rc = r - (r - 1) ** 2 / (n - 1)
        kc = k - (k - 1) ** 2 / (n - 1)
        return math.sqrt(phi2c / min(kc - 1, rc - 1))
    cnt = np.bincount(xc).astype(float)
    ok = cnt > 0
    m = np.bincount(xc, weights=yr)[ok] / cnt[ok]
    ss_b = (cnt[ok] * (m - yr.mean()) ** 2).sum()
    ss_t = ((yr - yr.mean()) ** 2).sum()
    return math.sqrt(ss_b / ss_t) if ss_t > 0 else 0.0


def _encode(xvals, ptype, vals):
    if ptype in ("ord", "num"):
        return np.searchsorted(vals, xvals)
    return np.searchsorted(vals, xvals.astype(str))


def perm_task(t):
    """Besag-Clifford sequential permutation for one (parameter, outcome) pair.

    t: dict with key, mode ('scenario' | 'strata'), ptype, vals, yc, yr, okind2, obs, seed, bmax, h_exceed and
       mode-specific arrays: scenario -> tbl (scenario x level lookup), si, li, n_scen; strata -> xs, sc_codes.
    """
    rng = np.random.default_rng(t["seed"])
    ptype, vals, yc, yr, okind2, obs = t["ptype"], t["vals"], t["yc"], t["yr"], t["okind2"], t["obs"]
    if t["mode"] == "scenario":
        tbl, si, li, ns = t["tbl"], t["si"], t["li"], t["n_scen"]

        def draw():
            pi = rng.permutation(ns)
            return tbl[pi[si], li]
    else:
        xs, sc = t["xs"], t["sc_codes"]
        order = np.argsort(sc, kind="stable")

        def draw():
            pidx = np.argsort(sc + rng.random(len(xs)))
            out = np.empty_like(xs)
            out[order] = xs[pidx]
            return out
    h = L = 0
    while L < t["bmax"] and h < t["h_exceed"]:
        xp = draw()
        xq = xp if ptype == "num" else _encode(xp, ptype, vals)
        L += 1
        if stat_fast(xq, ptype, yc, yr, okind2) >= obs - 1e-12:
            h += 1
    p = h / L if h >= t["h_exceed"] else (h + 1) / (L + 1)
    return t["key"], p, L, h


def ridge_logit(X, y, lam=1.0, iters=50, pen_mask=None):
    """Ridge-penalised logistic regression by Newton-Raphson. Intercept (column 0) unpenalised."""
    k = X.shape[1]
    beta = np.zeros(k)
    pm = np.ones(k) if pen_mask is None else np.asarray(pen_mask, float)
    pm[0] = 0
    P = np.diag(lam * pm)
    for _ in range(iters):
        eta_ = np.clip(X @ beta, -30, 30)
        mu = 1 / (1 + np.exp(-eta_))
        W = mu * (1 - mu) + 1e-9
        g = X.T @ (y - mu) - P @ beta
        Hm = (X.T * W) @ X + P + 1e-9 * np.eye(k)
        step = np.linalg.solve(Hm, g)
        beta += step
        if np.abs(step).max() < 1e-7:
            break
    mu = np.clip(1 / (1 + np.exp(-np.clip(X @ beta, -30, 30))), 1e-12, 1 - 1e-12)
    dev = -2 * np.sum(y * np.log(mu) + (1 - y) * np.log(1 - mu))
    return beta, mu, dev


def inter_task(t):
    """Null distribution of (deviance drop of A x B over A + B) - extra df.

    Each draw resamples scenarios with replacement (cluster bootstrap of the design rows) and simulates y from the
    null mean mu0 (additive fit plus shrunken scenario offsets, which carries within-scenario correlation).
    """
    rng = np.random.default_rng(t["seed"])
    Xa, Xi, mu0, rows, extra, lam = t["Xa"], t["Xi"], t["mu0"], t["scen_rows"], t["extra"], t["lam"]
    G = len(rows)
    out = np.empty(t["B"])
    for b in range(t["B"]):
        ix = np.concatenate([rows[i] for i in rng.integers(0, G, G)])
        ys = (rng.random(len(ix)) < mu0[ix]).astype(float)
        _, _, d1 = ridge_logit(Xa[ix], ys, lam)
        _, _, d2 = ridge_logit(Xi[ix], ys, lam)
        out[b] = d1 - d2 - extra
    return t["key"], out
