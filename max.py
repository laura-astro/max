import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import sys

def load_data(file, col_x=0, col_y=1):
    # this loads the ASCII file keeping the original structure
    data = np.loadtxt(file)
    return data[:, col_x], data[:, col_y]

def find_regions(x, y, A0, min_length):
    #this identifies regions above the limit
    above = y > A0
    changes = np.diff(above.astype(int))
    
    beginning_regions = np.where(changes == 1)[0] + 1
    end_regions = np.where(changes == -1)[0] + 1
    
    if above[0]:
        beginning_regions = np.insert(beginning_regions, 0, 0)
    if above[-1]:
        end_regions = np.append(end_regions, len(y)-1)
    
    #this groups nearby regions
    regions = []
    if len(beginning_regions) > 0:
        recent = [beginning_regions[0], end_regions[0]]
        for beginning, end in zip(beginning_regions[1:], end_regions[1:]):
            if x[beginning] - x[recent[1]] < min_length:
                recent[1] = end
            else:
                regions.append(tuple(recent))
                recent = [beginning, end]
        regions.append(tuple(recent))
    
    return regions

def analyse_large_peak(x, y, region):
    #this version protects sole points
    beginning, end = region
    x_peak = x[beginning:end+1]
    y_peak = y[beginning:end+1]
    
    if len(x_peak) == 1:
        return {
            'x_beginning': x_peak[0],
            'x_end': x_peak[0],
            'x_max': x_peak[0],
            'y_max': y_peak[0],
            'length': 0.0,
            'area': 0.0,
            'valid': False
        }
    
    derivative = np.gradient(y_peak, x_peak)
    edge_derivative = 0.1 * np.max(np.abs(derivative))
    
    try:
        peaks_derivative, _ = find_peaks(np.abs(derivative), height=edge_derivative)
        
        limit_left = peaks_derivative[0] if len(peaks_derivative) > 0 else 0
        limit_right = peaks_derivative[-1] if len(peaks_derivative) > 1 else len(x_peak)-1
        
        return {
            'x_beginning': x_peak[limit_left],
            'x_end': x_peak[limit_right],
            'x_max': x_peak[np.argmax(y_peak)],
            'y_max': np.max(y_peak),
            'length': x_peak[limit_right] - x_peak[limit_left],
            'area': np.trapz(y_peak[limit_left:limit_right+1], x_peak[limit_left:limit_right+1]),
            'valid': True
        }
    except Exception:
        return {
            'x_beginning': x_peak[0],
            'x_end': x_peak[-1],
            'valid': False
        }

def display_results(x, y, regions, results, A0):
    #this displays both graph and table simultaneously with values in each point
    plt.figure(figsize=(14, 7))
    
    # graph
    plt.plot(x, y, 'b-', label='original data', alpha=0.7)
    plt.axhline(y=A0, color='r', linestyle='--', label=f'limit A0 = {A0:.2f}')
    
    #this highlights valid peaks
    for i, res in enumerate([r for r in results if r['valid']], 1):
        plt.axvspan(res['x_beginning'], res['x_end'], color='green', alpha=0.2)
        plt.plot(res['x_max'], res['y_max'], 'ro', markersize=8)
        
        #this shows the text with values
        text = f"peak {i}\nX: {res['x_max']:.2f}\nY: {res['y_max']:.2f}"
        plt.text(res['x_max'], res['y_max'], text, 
                 ha='left', va='bottom',
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.title('Analysis of Large Peaks')
    plt.xlabel('F [muHz]')
    plt.ylabel('A [mma]')
    plt.legend()
    plt.grid(True)
    
    #table displayed in terminal
    print("\nRESULT OF VALID PEAKS")
    print("="*90)
    print("{:<6} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format(
        "Peak", "X Beginning", "X End", "X Max", "Y Max", "Length", "Area"))
    print("-"*90)
    
    for i, res in enumerate([r for r in results if r['valid']], 1):
        print("{:<6} {:<12.4f} {:<12.4f} {:<12.4f} {:<12.4f} {:<12.4f} {:<12.4f}".format(
            i, res['x_beginning'], res['x_end'], res['x_max'], res['y_max'], res['length'], res['area']))
    
    plt.show()

def main():
    print("\nANALYSIS OF LARGE PEAKS")
    
    try:
        #interactive user input
        file = input("\nData file: ").strip('"')
        col_x = int(input("X Column (0-indexed): "))
        col_y = int(input("Y Column (0-indexed): "))
        A0 = float(input("Minimum A0 value (fap): "))
        min_length = float(input("Minimum length (X units): ") or "5")
        
        #data processing
        x, y = load_data(file, col_x, col_y)
        regions = find_regions(x, y, A0, min_length)
        
        if not regions:
            print("\nNo region found above the limit")
            return
        
        results = [analyse_large_peak(x, y, r) for r in regions]
        valid_results = [r for r in results if r['valid']]
        
        if valid_results:
            display_results(x, y, regions, results, A0)
            
            if input("\nSave valid results? (y/n): ").lower() == 'y':
                name = input("File name (no extention): ").strip()
                data = np.array([(r['x_beginning'], r['x_end'], r['x_max'], r['y_max'], r['length'], r['area']) 
                          for r in valid_results])
                np.savetxt(f"{name}.txt", data, 
                          header="x_beginning x_end x_max y_max length area",
                          fmt="%.4f")
                print(f"Results saved as {name}.txt")
        else:
            print("\nNo valid peak found")
            
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
