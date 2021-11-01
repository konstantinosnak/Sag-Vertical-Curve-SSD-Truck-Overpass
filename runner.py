import os, sys

### Default values
curves = {
    50  : [1300, 1400, 1500, 1600, 1700],
    60  : [1800, 1900, 2000, 2100, 2200],
    70  : [2300, 2400, 2500, 2600, 2700, 2800, 2900],
    80  : [3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700],
    90  : [3800, 3900, 4000, 4100, 4200, 4300, 4400],
    100 : [4500, 4600, 4700, 4800, 4900, 5000, 5100, 5200, 5300, 5400],
    110 : [5500, 5600, 5700, 5800, 5900, 6000, 6100, 6200],
    120 : [6300, 6400, 6500, 6600, 6700, 6800, 6900, 7000, 7100, 7200],
    130 : [7300, 7400, 7500, 7700, 7700, 7800, 7900, 8000, 8100, 8200, 8300],
}

### Arguments
if len(sys.argv[1:]) > 0:
    speeds = [int(x) for x in sys.argv[1:]]
else:
    speeds = list(curves.keys()) # All available

### Run
for speed in speeds:
    for curve in curves[speed]:
        print(f'\n---\n> Running speed={speed} curve={curve} ...\n---')
        os.system(f'python main.py {speed} {curve} 0')