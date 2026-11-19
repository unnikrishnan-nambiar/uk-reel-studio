# Source-time segments, in EDIT order. h1..h3 = three hook takes; each final version = one hook + BODY.
HOOKS = {'h1': [0.20, 3.14], 'h2': [4.25, 6.66], 'h3': [7.54, 10.60]}
BODY = [[11.25, 15.58], [15.95, 18.60], [18.95, 21.19], [21.65, 34.65], [34.95, 35.93], [36.30, 38.06],
        [38.52, 44.86], [45.19, 48.23], [48.53, 56.12], [56.46, 61.03]]
ALL = [HOOKS['h1'], HOOKS['h2'], HOOKS['h3']] + BODY
