import ssd_calc
import height

import pandas as pd 
import sys
import os

### First message
print("This programm calculates the height of the line of sight for symmetrical curves.")

### Usage
def print_usage():
    print('Usage:\n' + sys.argv[0] + ' vo Hw HPVI')
    print('vo: Truck speed, Hw: Curve radius (aktina kampylis), HPVI: PVI elevation (float)')
    print('If no arguments are given, values are asked interactively.')

### Input parsing
args = sys.argv[1:]
if len(args) == 0: # Interactive
    print_usage()
    print('\n---- Interactive mode----\n')
    # Interactive inputs
    vo = int(input("Truck speed (km/h): "))
    Hw = int(input("Curve radius (aktina kampylis) (m): ")) 
    HPVI = float(input("PVI elevation [could be float] (m): "))
elif args[0] == '--help' or args[0] == '-h':
    print_usage()
    exit(1) # Exit the program
elif len(args) == 3:
    vo = int(args[0])
    Hw = int(args[1])
    HPVI = float(args[2])
else:
    print_usage()
    exit(1) # Exit the program

### For loops
if   vo < 60:
    max_s_per_vo = 14
elif vo < 70:
    max_s_per_vo = 13
elif vo < 80:
    max_s_per_vo = 12
elif vo < 100:
    max_s_per_vo = 10
elif vo < 110:
    max_s_per_vo = 9
else:
    max_s_per_vo = 5

### Convert vo to m/s (from km/h)
vo = vo * (1000.0 / 3600.0) # Gia km/h -> m/s

### In case values need to be calculated for larger meter intervals
step_in_meters = 1

### Iterate through all possible grade combinations
for s1 in range(-max_s_per_vo, 1, 1): # i.e., -12..0
    for s2 in range(max_s_per_vo, -1, -1): # i.e., 12..0
        ### Skip straight roads (also leads to division by ZERO) -- ACHTUNG
        if s1 == 0 and s2 == 0:
            continue

        print(f'\tProcessing s1={s1} s2={s2} ...')

        ### Constants
        Ad = ((s2*0.01)-(s1*0.01)) # *0.01 to convert from % to normal value (e.g., 12% -> 0.12)
        T = ((Hw//2)*(Ad))
        L = 2 * T # Length of sag vertical curve  
        xpvi = T + 200 # Starting position, 200 was chosen as a safe value
        xvpc = round(xpvi-T) # Where curve starts
        xvpt = xvpc
        H0 = (HPVI+ (abs(s1*0.01*xpvi))) # Height of starting position
        hVPC = H0 + (s1*0.01*xvpc) # Height of VPC
        hVPT = HPVI + (s2*0.01*T) # Height of VPT
        xroadall = round(xvpc+L+xvpt) # Length of road
        eyes_height = 2.33 # Driver's eyes height
        obstacle_height = 0.6

        ### Calculate height using dedicated class
        height_c = height.height_calculator( xvpc, H0, s1, s2, hVPC, Ad, L, hVPT )
        
        ### Calculate height of road for each position
        hroad=[]
        for x in range(0, xroadall+1 ,1):
            hroad.append( height_c.get(x) )

        ### Will contain results
        data = {}

        ### Coefficients to check to transform passenger car SSD to truck SSD
        ssd_coefs = [ (3.4/9.81)/0.16 ]
        
        ### ssd_coef is only ssd_coef now, used to be more options
        for ssd_coef in ssd_coefs:
            ### in string form
            ssd_coef_str = str(ssd_coef)

            hlines=[] # list of (hline lists) for each x
            hdiffs=[]
            
            ### Create instance of SSD class
            ssd_c = ssd_calc.ssd(xvpc, L, s1, s2, Hw, vo)

            for x in range (0, xroadall+1, 1):
                ssd = (ssd_coef * ((ssd_c.get(x))-(vo*2.5))) + (vo*2.5)
                sline = ((height_c.get(x+ssd)+obstacle_height)-(height_c.get(x)+eyes_height))/ssd

                hline=[]
                for i in range (0,xroadall+1,1):
                    # Using line equation: y-yo=s*(x-xo)
                    hi = (height_c.get(x)+eyes_height)+((sline*(i-x)))
                    hline.append(hi)

                hdiff=[]
                for i in range (0, xroadall+1, 1):
                    hdiffi=((hline[i]-hroad[i]))
                    hdiff.append(hdiffi)
 
                hlines.append(hline)
                hdiffs.append(hdiff)

            data[ssd_coef_str] = {
                'x': range(0,xroadall+1,step_in_meters),
                'start4.3' : [],
                'end4.3' : [],
                'start4.6' : [],
                'end4.6' : [],
                'start4.9' : [],
                'end4.9' : [], 
                'hroad_max_s_start4.3' : [],
                'hroad_max_s_end4.3' : [],
                'hroad_max_s_start4.6' : [],
                'hroad_max_s_end4.6' : [],
                'hroad_max_s_start4.9' : [],
                'hroad_max_s_end4.9' : [],
                'distance from PVI': [],
                'track_finish': [],
                'ssd': [],
            }

            for i in range(0, xroadall+1, step_in_meters):
                hdiffs_important = []
                xs = []
                for k in range(len(hdiffs[i])):
                    if k % step_in_meters == 0 and k >= i:
                        hdiffs_important.append( hdiffs[i][k] )
                        xs.append(k-xpvi)

                data[ssd_coef_str]['distance from PVI'].append( i - xpvi )

                ### Last time it becomes < 4.3
                start43 = -1
                end43   = -1
                for k in range(len(hdiffs_important)):
                    val = hdiffs_important[k]
                    if val > 4.3:
                        start_k = k
                        start43 = xs[k]
                        break
                for k in range(len(hdiffs_important[::-1])): # reverse
                    val = hdiffs_important[::-1][k]
                    if val > 4.3:
                        end_k = len(hdiffs_important) - k + 1
                        end43 = xs[end_k]
                        break
                data[ssd_coef_str]['start4.3'].append(start43)
                data[ssd_coef_str]['end4.3'].append(end43)

                ### Last time it becomes < 4.6
                start46 = -1
                end46   = -1
                for k in range(len(hdiffs_important)):
                    val = hdiffs_important[k]
                    if val > 4.6:
                        start_k = k
                        start46 = xs[k]
                        break
                for k in range(len(hdiffs_important[::-1])): # reverse
                    val = hdiffs_important[::-1][k]
                    if val > 4.6:
                        end_k = len(hdiffs_important) - k + 1
                        end46 = xs[end_k]
                        break
                data[ssd_coef_str]['start4.6'].append(start46)
                data[ssd_coef_str]['end4.6'].append(end46)

                ### Last time it becomes < 4.9
                start49 = -1
                end49   = -1
                for k in range(len(hdiffs_important)):
                    val = hdiffs_important[k]
                    if val > 4.9:
                        start_k = k
                        start49 = xs[k]
                        break
                for k in range(len(hdiffs_important[::-1])): # reverse
                    val = hdiffs_important[::-1][k]
                    if val > 4.9:
                        end_k = len(hdiffs_important) - k + 1
                        end49 = xs[end_k]
                        break
                data[ssd_coef_str]['start4.9'].append(start49)
                data[ssd_coef_str]['end4.9'].append(end49)

                ### Gradients depending on position

                def get_gradient(start, end):
                    gradient_start = -100
                    gradient_end = -100

                    hroad_max_x_adj_start = start + xpvi
                    hroad_max_x_adj_end = end + xpvi

                    if hroad_max_x_adj_start <= 200:
                        gradient_start = s1
                    if hroad_max_x_adj_start > 200 and hroad_max_x_adj_start < xroadall-200:
                        sx = s1 + 100.0*(hroad_max_x_adj_start-200)/Hw
                        gradient_start = sx
                    if hroad_max_x_adj_start >= xroadall-200:
                        gradient_start = s2

                    if hroad_max_x_adj_end <= 200:
                        gradient_end = s1
                    if hroad_max_x_adj_end > 200 and hroad_max_x_adj_end < xroadall-200:
                        sx = s1 + 100.0*(hroad_max_x_adj_end-200)/Hw
                        gradient_end = sx
                    if hroad_max_x_adj_end >= xroadall-200:
                        gradient_end = s2

                    return (gradient_start, gradient_end)

                (x, y) = get_gradient(start43, end43)
                data[ssd_coef_str]['hroad_max_s_start4.3'].append(x)
                data[ssd_coef_str]['hroad_max_s_end4.3'].append(y)
                (x, y) = get_gradient(start46, end46)
                data[ssd_coef_str]['hroad_max_s_start4.6'].append(x)
                data[ssd_coef_str]['hroad_max_s_end4.6'].append(y)
                (x, y) = get_gradient(start49, end49)
                data[ssd_coef_str]['hroad_max_s_start4.9'].append(x)
                data[ssd_coef_str]['hroad_max_s_end4.9'].append(y)                

                ### Track finish
                ssd = (ssd_coef * ((ssd_c.get(i))-(vo*2.5))) + (vo*2.5)
                data[ssd_coef_str]['track_finish'].append( (i - xpvi) + ssd )
                data[ssd_coef_str]['ssd'].append( ssd )

        ### data_csv is needed, because we want to save results in csv form.
        ### Thus, we need a single column titles for every result
        ### E.g., in data, we had data['3.17']['start4.3']
        ### Now we have: data_csv['ssd3.17--start4.3'], so it's a single "title" that
        ### can be used as column title
        data_csv = {}
        data_csv['x'] = range(0,xroadall+1,step_in_meters)
        data_csv['distance from PVI'] = data[str(ssd_coefs[0])]['distance from PVI']
        for ssd_coef_str in data.keys():
            data_s = data[ssd_coef_str]
            for key in ['track_finish', 'ssd', 'start4.3', 'end4.3', 'start4.6', 'end4.6', 'start4.9', 'end4.9', 'hroad_max_s_start4.3', 'hroad_max_s_end4.3', 'hroad_max_s_start4.6', 'hroad_max_s_end4.6', 'hroad_max_s_start4.9', 'hroad_max_s_end4.9']:
                data_csv['ssd' + ssd_coef_str + '--' + key] = data_s[key]

        ### Save csv
        df = pd.DataFrame(data_csv)
        # Directory in which the python file is located
        current_dir = os.path.dirname(os.path.realpath(__file__))
        current_dir = current_dir + f'/results/vo_{round(vo * 3600/1000)}_km_h/vo_{round(vo * 3600/1000)}_km_h__curve_{Hw}'
        # Create directory if it does not exist
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)
        # Actually save "dataframe" to csv
        df.to_csv(
            f'{current_dir}/s1_{s1}__s2_{s2}__results_per_{step_in_meters}_m.csv',
            index=False
        )
