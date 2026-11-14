"""Check recovered values (scripts/data.py) against numbers printed in the paper."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import data as D

def row(rows, lab): return next(r for r in rows if r[0] == lab)
checks = [  # (description, recovered, printed, tolerance)
 ("Fig2 KID standard (Tab.1 0.1858)", row(D.FIG2_CIFAR_KID, 'Standard start')[1], 185.8, 0.1),
 ("Fig2 KID covariance (Tab.1 0.1264)", row(D.FIG2_CIFAR_KID, 'Covariance start')[1], 126.4, 0.1),
 ("Fig2 MNIST keep (Tab.1 0.02177)", row(D.FIG2_MNIST_ERR, 'Keep targeting')[1], 2.177, 0.005),
 ("Fig2 MNIST ordinary (Tab.1 0.00900)", row(D.FIG2_MNIST_ERR, 'Ordinary data')[1], 0.900, 0.005),
 ("Fig4b full moments (text 0.1405)", row(D.FIG4B_KID, 'Full moments')[1], 140.5, 0.1),
 ("Fig4b DPM++/UniPC (text 0.2225)", row(D.FIG4B_KID, 'DPM++ / UniPC')[1], 222.5, 0.1),
 ("Fig5 pixel DDIM (0.376)", row(D.FIG5_PIXEL_SPREAD, 'DDIM')[1], 0.376, 0.001),
 ("Fig5 pixel output (0.917)", row(D.FIG5_PIXEL_SPREAD, 'Output cov.')[1], 0.917, 0.001),
 ("Fig5 pixel UniPC (Supp 0.671)", row(D.FIG5_PIXEL_SPREAD, 'UniPC')[1], 0.671, 0.001),
 ("Fig5 cov DDIM (0.478)", row(D.FIG5_COVERAGE, 'DDIM')[1], 0.478, 0.001),
 ("Fig5 cov output (0.332)", row(D.FIG5_COVERAGE, 'Output cov.')[1], 0.332, 0.001),
 ("Fig5 cov UniPC (0.549)", row(D.FIG5_COVERAGE, 'UniPC')[1], 0.549, 0.001),
 ("Fig5 KID DDIM (0.0903)", row(D.FIG5_KID, 'DDIM')[1], 90.3, 0.1),
 ("Fig5 KID output (102.4)", row(D.FIG5_KID, 'Output cov.')[1], 102.4, 0.1),
 ("Fig5 KID output lo (Supp 102.4-1.6)", row(D.FIG5_KID, 'Output cov.')[2], 100.8, 0.15),
 ("Fig5 KID UniPC (69.4)", row(D.FIG5_KID, 'UniPC')[1], 69.4, 0.1),
 ("Fig5 KID UniPC hi (Supp 69.4+2.6)", row(D.FIG5_KID, 'UniPC')[3], 72.0, 0.15),
 ("Fig6 Euler KID 15 (0.00876)", D.FIG6_KID['Euler'][2], 8.76, 0.02),
 ("Fig6 Heun KID 15 (0.00250)", D.FIG6_KID['Heun'][2], 2.50, 0.02),
 ("Fig6 Heun KID 35 (0.000413)", D.FIG6_KID['Heun'][3], 0.413, 0.005),
 ("Fig6 Heun KID 7 (Supp 98.298)", D.FIG6_KID['Heun'][1], 98.298, 0.1),
 ("Fig6 Euler cov 15 (0.477)", D.FIG6_COV['Euler'][2], 0.477, 0.002),
 ("Fig6 Heun cov 15 (0.417)", D.FIG6_COV['Heun'][2], 0.417, 0.002),
 ("Fig6 cov 35 (0.501)", D.FIG6_COV['Heun'][3], 0.501, 0.002),
 ("Fig7 digit3 keep (16.67-9.83)", D.FIG7_GAP['Keep targeting'][3], 6.84, 0.03),
 ("Fig7 digit3 ordinary (9.08-9.83)", D.FIG7_GAP['Ordinary data'][3], -0.75, 0.03),
 ("Fig7 mean TV keep (14.61)", sum(a for a, b in D.FIG7_TV) / 3, 14.61, 0.03),
 ("Fig7 mean TV ordinary (8.54)", sum(b for a, b in D.FIG7_TV) / 3, 8.54, 0.03),
 ("Fig8 DINO DDIM4 est (1.306)", D.FIG8['dinov2_image'][0][1], 1.306, 0.002),
 ("Fig8 DINO DDIM4 lo (1.236)", D.FIG8['dinov2_image'][0][2], 1.236, 0.002),
 ("Fig8 DINO DDIM4 hi (1.382)", D.FIG8['dinov2_image'][0][3], 1.382, 0.002),
 ("Fig3 1% n=2000 (3.25)", D.FIG3['1%'][4][0], 3.25, 0.03),
 ("Fig3 1% n=5000 (99.90)", D.FIG3['1%'][5][0], 99.90, 0.03),
 ("Fig3 2% n=2000 (97.40)", D.FIG3['2%'][4][0], 97.40, 0.03),
 ("Fig3 0.5% n=10000 (99.95)", D.FIG3['0.5%'][6][0], 99.95, 0.03),
]
bad = 0
for d, rec, pr, tol in checks:
    ok = abs(rec - pr) <= tol
    bad += not ok
    print(("OK  " if ok else "FAIL"), f"{d:42s} recovered={rec:.4g} printed={pr:.4g}")
print(f"{len(checks) - bad}/{len(checks)} checks pass")
sys.exit(bad > 0)
