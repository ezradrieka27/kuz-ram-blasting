import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import math

#Solving the problem
def solve_kuz_ram(bench_height, stem, sub_drill, 
                  burden, spacing, p_rock, p_explosive, 
                  diameter, wts, a, pattern, dd, oversize):
    h_column = float(bench_height) - float(stem) + float(sub_drill)
    # Tons/hole
    ton_hole = float(burden) * float(spacing) * float(bench_height) * float(p_rock)
    #volume
    volume = float(burden) * float(spacing) * float(bench_height)
    # charge calculation
    charge = float(
        p_explosive * math.pi * 1000 *h_column * (diameter/1000/2)**2
    )
    pf = charge/ton_hole
    
    #pf is powder factor
    # a is rockfactor
    # p_rock is rockdensity in SG
    
    #d_50 in milimeters
    d_50 = float(a) * 10 * (
        (volume / charge
        )**0.8
        ) * (charge **(1/6)) * ((115/wts) ** 0.633)
    
    
    # Uniformity index
    uniform_index = pattern * (
        (
            h_column - float(sub_drill)
        )/float(bench_height) * (
            2.2 - 14 * float(burden)/(float(diameter))
            ) *(
                ((1 + float(spacing/float(burden)))/2
                ) ** 0.5) * (1 - (float(dd)/float(burden)))
                    
            )
    uniform_index = round(uniform_index, 2)
    #Particular size in milimeters
    particular_size = d_50 / (0.693 ** (1/uniform_index))
    particular_size = round(particular_size, 0)
    data = pd.DataFrame(columns = ['percentage','Size_Particle'])
    for i in range(10, 101, 10):
        if i == 100:
            i = 99.5
   
        something = (-math.log(1-(i/100)))
        
        size = particular_size * (something)**(1/uniform_index)
        data.loc[ len(data) ] = [i,size]
        
 
    d80 = data.Size_Particle[7]
    perc_oversize = math.exp(-(
        (oversize/particular_size)**uniform_index
    ))*100
    

    return (ton_hole, volume, pf,burden, spacing,stem, charge, d_50/10, uniform_index, data, d80, perc_oversize )


bench_height = 10
p_rock = 2.7
p_exp = 0.8
wts = 100
pattern = 1.1
dd = 0.1
rock_factor = 4
diameter = 140
mic = 86.34
oversize = 700

lst_dict = []
cols = ['tonhole','volume','pf','burden','spacing','stemming','charge','d50', 'uniform', 'psd', 'd80', 'oversize']
df = pd.DataFrame(columns=cols)

# def solve_kuz_ram(bench_height, stem, sub_drill, 
#                   burden, spacing, p_rock, p_explosive, 
#                   diameter, wts, a, pattern, dd, oversize):

burden_min = 25 * diameter / 1000
burden_min = int(round(burden_min,1)*10)
burden_max = 40 * diameter / 1000
burden_max = int(round(burden_max,1)*10)

for i in range(burden_min,burden_max,1):
    burden = i/10
    stem = burden
    subdrill = 0.3 * burden
    spacing_min = i
    spacing_max = int(round(1.25 * burden,1)*10)
    
    for j in range(spacing_min,spacing_max):
        spacing = j/10
        result = solve_kuz_ram(bench_height, stem, subdrill, 
                    burden, spacing, p_rock, p_exp, 
                    diameter, wts, rock_factor, pattern, dd, oversize)
        df.loc[ len(df) ] = [result[c] for c in range(0,len(result))]

# df = df.loc[(df.charge <= mic) & (df.d80 <=700) ]
# df = df.loc[(df.charge <= mic) ]
df.to_clipboard()
    

