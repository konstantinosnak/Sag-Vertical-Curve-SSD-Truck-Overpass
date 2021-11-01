# Sag Vertical Curve SSD Truck Overpass

Vertical clearance assessment of overpassing structures on sag vertical curves for trucks.

*For every possible combination of speed, curve, and grade the positions where driver sight distance gets interrupted get calculated.*

All calculated result .csv files can be found at [https://github.com/konstantinosnak/Sag-Vertical-Curve-SSD-Truck-Overpass/releases/download/1.0/results-final.zip](https://github.com/konstantinosnak/Sag-Vertical-Curve-SSD-Truck-Overpass/releases/download/1.0/results-final.zip)

## Installation

- Python 3.6+ is required (with pip) to be installed in the system and available in path.
- `pip install -r requirements.txt`

## Usage

From inside the project root, after dependencies are installed.

### Interactive mode

This mode will ask for speed, curve, and PVI elevation in the terminal when run.

```
python main.py
```

### Manual mode

Arguments are given directly in the terminal.

```
python main.py SPEED CURVE PVI_ELEVATION
```

E.g., `python main.py 70 2500 0`

### Results

Results will be present in `csv` files inside the `results/` directory.
