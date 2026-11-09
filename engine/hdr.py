"""SDR graphics -> HLG (BT.2020) code values, so overlays sit at HDR reference white (~75% HLG, 203 nits)
instead of glowing at peak. Used when REEL_HDR=1 and the source footage is iPhone HLG."""
import numpy as np, os
ON = os.environ.get('REEL_HDR', '0') == '1'
_s = np.arange(256, dtype=np.float32) / 255
_LIN = np.where(_s <= 0.04045, _s / 12.92, ((_s + 0.055) / 1.055) ** 2.4).astype(np.float32)   # sRGB EOTF
_M = np.array([[0.6274, 0.3293, 0.0433], [0.0691, 0.9195, 0.0114], [0.0164, 0.0880, 0.8956]], np.float32)  # 709->2020 (RGB)
_x = np.linspace(0, 1, 4096, dtype=np.float32)
_E = (0.203 * _x) ** (1 / 1.2)                                  # display-linear (ref white 203 nits of 1000) -> scene light
_a, _b, _c = 0.17883277, 0.28466892, 0.55991073
_HLG = (np.where(_E <= 1 / 12, np.sqrt(3 * _E), _a * np.log(np.maximum(12 * _E - _b, 1e-6)) + _c) * 255).astype(np.float32)

def sdr2hlg(bgr):
    """bgr: float/uint8 array (...,3) of sRGB graphics in BGR order, 0-255 -> float HLG codes 0-255 (BGR)."""
    lin = _LIN[np.clip(bgr + 0.5, 0, 255).astype(np.uint8)][..., ::-1]          # -> RGB linear
    l2 = np.clip(lin @ _M.T, 0, 1)
    return _HLG[(l2 * 4095 + 0.5).astype(np.int32)][..., ::-1]
