# Max Sorter written in 2025 by Laura C. Sultan

import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def load_data(file, col_x=0, col_y=1):
    data = np.loadtxt(file)
    return data[:, col_x], data[:, col_y]

def find_all_peaks(x, y, A0, min_width=0.1):
    """ This finds all peaks above the A0 (fap), or potential peaks. """
    above_threshold = np.where(y > A0)[0]
    peaks = []
    
    for idx in above_threshold:
        # This considers each point above the edge like a separate peak
        peaks.append({
            'left': idx,
            'right': idx,
            'max': idx
        })
    
    # This adds together peaks extremely close (shorter than min_width in distance)
    merged_peaks = []
    if peaks:
        current_peak = peaks[0].copy()
        
        for peak in peaks[1:]:
            if x[peak['left']] - x[current_peak['right']] < min_width:
                # This combines it with the previous peak
                current_peak['right'] = peak['right']
                if y[peak['max']] > y[current_peak['max']]:
                    current_peak['max'] = peak['max']
            else:
                # This adds the current peak and starts anew
                merged_peaks.append(current_peak)
                current_peak = peak.copy()
        
        merged_peaks.append(current_peak)
    
    return merged_peaks

def analyze_peaks(x, y, peaks, A0):
    results = []
    for i, peak in enumerate(peaks, 1):
        x_peak = x[peak['left']:peak['right']+1]
        y_peak = y[peak['left']:peak['right']+1]
        
        results.append({
            'peak_id': i,
            'x_beginning': x[peak['left']],
            'x_end': x[peak['right']],
            'x_max': x[peak['max']],
            'y_max': y[peak['max']],
            'length': x[peak['right']] - x[peak['left']],
            'area': np.trapz(y_peak, x_peak),
            'valid': True
        })
    
    return results

def display_results(x, y, results, A0):
    plt.figure(figsize=(14, 7))
    
    # This plots the original data
    plt.plot(x, y, 'b-', label='Original data', alpha=0.7, linewidth=1)
    plt.axhline(y=A0, color='r', linestyle='--', label=f'Threshold A0 = {A0:.4f}')
    
    # This highlights valid peaks
    for res in results:
        if res['valid']:
            # Vertical line when the peak is maximum
            plt.axvline(x=res['x_max'], color='g', linestyle=':', alpha=0.5)
            
            # Dot when the peak is maximum
            plt.plot(res['x_max'], res['y_max'], 'ro', markersize=6)
            
            # Text with info
            plt.text(res['x_max'], res['y_max'], 
                    f"Peak {res['peak_id']}\nX: {res['x_max']:.2f}\nY: {res['y_max']:.2f}",
                    ha='left', va='bottom', fontsize=8,
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.title('Peak Detection Analysis')
    plt.xlabel('F [μHz]')
    plt.ylabel('A [mma]')
    plt.legend()
    plt.grid(True)
    
    # Table of results
    print("\nPEAK DETECTION RESULTS")
    print("="*90)
    print("{:<6} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format(
        "Peak", "X Start", "X End", "X Max", "Y Max", "Length", "Area"))
    print("-"*90)
    
    for res in results:
        if res['valid']:
            print("{:<6} {:<12.4f} {:<12.4f} {:<12.4f} {:<12.4f} {:<12.4f} {:<12.4f}".format(
                res['peak_id'], res['x_beginning'], res['x_end'], 
                res['x_max'], res['y_max'], res['length'], res['area']))
    
    plt.show()

def main():
    print("\nPRECISE PEAK DETECTION ANALYSIS")
    
    try:
        file = input("\nData file: ").strip('"')
        col_x = int(input("X Column (0-indexed): "))
        col_y = int(input("Y Column (0-indexed): "))
        A0 = float(input("Threshold A0 value: "))
        min_width = float(input("Minimum peak width (default 0.1): ") or "0.1")
        
        x, y = load_data(file, col_x, col_y)
        peaks = find_all_peaks(x, y, A0, min_width)
        
        if not peaks:
            print("\nNo peaks found above the threshold")
            return
        
        results = analyze_peaks(x, y, peaks, A0)
        display_results(x, y, results, A0)
        
        if input("\nSave results? (y/n): ").lower() == 'y':
            name = input("Output filename (without extension): ").strip()
            data = np.array([(r['x_beginning'], r['x_end'], r['x_max'], r['y_max'], r['length'], r['area']) 
                      for r in results if r['valid']])
            np.savetxt(f"{name}.txt", data, 
                      header="x_beginning x_end x_max y_max length area",
                      fmt="%.4f")
            print(f"Results saved to {name}.txt")
            
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
