"""Every number plotted in the main-paper figures, with its source.

Values marked [recovered] were read back from the vector geometry of the
draft figure PDFs (scripts/recover/recover_main.py); they were not printed
in the manuscript. Every value that IS printed was checked against the text
by scripts/recover/check_recovered.py (max deviation reported there).
Please replace [recovered] values with the analysis output when convenient.
"""

# Fig. 2(a) KID x1e3, two calls, 5 panels, ordinary 95% t. Points: Tab. 1 (0.1858, 0.1264); intervals [recovered]
FIG2_CIFAR_KID = [  # (label, estimate, lo, hi)
    ('Standard start', 185.8, 183.4, 188.1),
    ('Covariance start', 126.4, 124.7, 128.1),
]

# Fig. 2(b) mean class-mass error (%), 3 seeds, 95% t. Points: Tab. 1 (2.177, 0.900); intervals [recovered]
FIG2_MNIST_ERR = [  # (label, estimate, lo, hi)
    ('Keep targeting', 2.177, 1.435, 2.918),
    ('Ordinary data', 0.8997, 0.4282, 1.371),
]

# Fig. 4(b) KID x1e3, fresh two-call confirmation. Points: Sec. 4.1 text; intervals [recovered]
FIG4B_KID = [  # (label, estimate, lo, hi)
    ('Leading DDIM', 185.8, 183.4, 188.1),
    ('Trailing DDIM', 192.3, 191.4, 193.2),
    ('DPM++ / UniPC', 222.5, 220.4, 224.7),
    ('Full moments', 140.5, 139.4, 141.6),
    ('Covariance only', 126.4, 124.7, 128.1),
]

# Fig. 4(a) pixel-PCA variance ratio vs calls [recovered]
FIG4A_CALLS = [1, 2, 4, 8]
FIG4A = {
    'Matched Gaussian': [1.0, 0.655, 0.513, 0.665],
    'Normal Gaussian': [0.206, 0.142, 0.41, 0.644],
    'Learned DDIM': [0.107, 0.107, 0.37, 0.614],
}

# Fig. 5 four-call pixel variance ratio. Points: Sec. 4.2 text / Supp. Tab. 6; intervals [recovered]
FIG5_PIXEL_SPREAD = [  # (label, estimate, lo, hi)
    ('DDIM', 0.3764, 0.3693, 0.3836),
    ('Output cov.', 0.9175, 0.898, 0.937),
    ('UniPC', 0.6707, 0.6592, 0.6822),
]

# Fig. 5 four-call real-data DINO coverage. Points: Sec. 4.2 text / Supp. Tab. 6; intervals [recovered]
FIG5_COVERAGE = [  # (label, estimate, lo, hi)
    ('DDIM', 0.4782, 0.455, 0.5013),
    ('Output cov.', 0.3317, 0.3162, 0.3472),
    ('UniPC', 0.5494, 0.5282, 0.5705),
]

# Fig. 5 four-call KID x1e3. Points: Sec. 4.2 text / Supp. Tab. 6; intervals [recovered]
FIG5_KID = [  # (label, estimate, lo, hi)
    ('DDIM', 90.26, 87.77, 92.75),
    ('Output cov.', 102.4, 100.7, 104.0),
    ('UniPC', 69.43, 66.8, 72.05),
]

# Fig. 6 EDM Euler vs Heun (descriptive, no intervals). Points at 15/35 calls: Sec. 4.2 text; Heun-7 KID: Supp. table (98.298); others [recovered]
FIG6_CALLS = [3, 7, 15, 35]
FIG6_KID = {'Euler': [202.6, 36.55, 8.758, 2.5], 'Heun': [649.1, 98.3, 2.504, 0.4129]}
FIG6_COV = {'Euler': [0.111, 0.341, 0.477, 0.501], 'Heun': [0.0, 0.191, 0.417, 0.501]}

# Fig. 7(a) signed mass gap from real data (percentage points), digits 0-9 and R = classifier reject. Digit 3: Sec. 4.3 text (16.67-9.83, 9.08-9.83); others [recovered]
FIG7_KEYS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'R']
FIG7_GAP = {'Keep targeting': [-1.65, -2.36, -2.34, 6.84, -2.18, -1.06, -0.367, -1.2, -1.46, -1.68, 7.46],
            'Ordinary data': [-0.697, -1.14, -1.88, -0.747, -1.47, -0.49, 0.0833, -0.313, -0.693, -0.733, 8.08]}
# Fig. 7(b) total variation (%) per training seed. Seed means 14.61 -> 8.54 match Sec. 4.3 text (0.1461 -> 0.0854); per-seed values [recovered]
FIG7_TV = [(15.98, 9.24), (14.53, 9.46), (13.33, 6.91)]

# Fig. 8 within-prompt spread ratio vs reference, 4 representations x 5 configurations, bootstrap 95% intervals over prompts.
# DINOv2 DDIM4 row: Sec. 4.5 text (1.306 [1.236,1.382]); others [recovered]
FIG8 = {
    'sampling_latent': [('DDIM4 / 7.5', 0.414, 0.4015, 0.427), ('LCM4 / 7.5', 0.9725, 0.9496, 0.9953), ('LCM4 / 1', 1.355, 1.32, 1.391), ('DMD2 / 7.5', 1.166, 1.129, 1.205), ('DMD2 / 1.75', 1.592, 1.548, 1.638)],
    'image_reencoding': [('DDIM4 / 7.5', 0.4822, 0.4694, 0.4955), ('LCM4 / 7.5', 0.9705, 0.9509, 0.99), ('LCM4 / 1', 1.283, 1.252, 1.315), ('DMD2 / 7.5', 1.172, 1.137, 1.208), ('DMD2 / 1.75', 1.524, 1.485, 1.566)],
    'dinov2_image': [('DDIM4 / 7.5', 1.306, 1.236, 1.382), ('LCM4 / 7.5', 1.101, 1.065, 1.138), ('LCM4 / 1', 0.6954, 0.6548, 0.7367), ('DMD2 / 7.5', 1.251, 1.208, 1.297), ('DMD2 / 1.75', 0.901, 0.8726, 0.9287)],
    'clip_image': [('DDIM4 / 7.5', 1.162, 1.088, 1.244), ('LCM4 / 7.5', 1.111, 1.072, 1.153), ('LCM4 / 1', 0.7231, 0.6751, 0.7728), ('DMD2 / 7.5', 1.256, 1.203, 1.314), ('DMD2 / 1.75', 0.9075, 0.879, 0.9358)],
}

# Fig. 3 complete-removal detection probability (%) vs samples per set; exact 95% binomial intervals; 2,000 trials per point.
# 1% and 2% at n=2000/5000 and 0.5% at 10000: Supp. table (support power, M=10); others [recovered]
FIG3_N = [100, 250, 500, 1000, 2000, 5000, 10000]
FIG3 = {
    '0.5%': [(0.0, 0.0, 0.18), (0.0, 0.0, 0.18), (0.0, 0.0, 0.18), (0.0, 0.0, 0.18), (0.0, 0.0, 0.18), (17.0, 15.38, 18.72), (99.95, 99.72, 100.0)],
    '1%': [(0.0, 0.0, 0.18), (0.0, 0.0, 0.18), (0.0, 0.0, 0.18), (0.0, 0.0, 0.18), (3.25, 2.52, 4.12), (99.9, 99.64, 99.99), (100.0, 99.82, 100.0)],
    '2%': [(0.0, 0.0, 0.18), (0.0, 0.0, 0.18), (0.0, 0.0, 0.18), (3.15, 2.43, 4.01), (97.4, 96.6, 98.05), (100.0, 99.82, 100.0), (100.0, 99.82, 100.0)],
    '5%': [(0.0, 0.0, 0.18), (0.0, 0.0, 0.18), (24.65, 22.77, 26.6), (99.95, 99.72, 100.0), (100.0, 99.82, 100.0), (100.0, 99.82, 100.0), (100.0, 99.82, 100.0)],
}
