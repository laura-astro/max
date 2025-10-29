import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def load_data(file, col_x=0, col_y=1):
    data = np.loadtxt(file)
    return data[:, col_x], data[:, col_y]

def find_all_peaks(x, y, A0, min_width=0.1):
    """Encontra todos os pontos acima de A0, tratando cada um como pico potencial"""
    above_threshold = np.where(y > A0)[0]
    peaks = []
    
    for idx in above_threshold:
        # Considera cada ponto acima do limiar como um pico separado
        peaks.append({
            'left': idx,
            'right': idx,
            'max': idx
        })
    
    # Junta picos muito próximos (menos que min_width de distância)
    merged_peaks = []
    if peaks:
        current_peak = peaks[0].copy()
        
        for peak in peaks[1:]:
            if x[peak['left']] - x[current_peak['right']] < min_width:
                # Junta com o pico anterior
                current_peak['right'] = peak['right']
                if y[peak['max']] > y[current_peak['max']]:
                    current_peak['max'] = peak['max']
            else:
                # Adiciona o pico atual e começa novo
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
    
    # Plot dos dados originais
    plt.plot(x, y, 'b-', label='Original data', alpha=0.7, linewidth=1)
    plt.axhline(y=A0, color='r', linestyle='--', label=f'Threshold A0 = {A0:.4f}')
    
    # Destaque para os picos válidos
    for res in results:
        if res['valid']:
            # Linha vertical no máximo do pico
            plt.axvline(x=res['x_max'], color='g', linestyle=':', alpha=0.5)
            
            # Ponto no máximo do pico
            plt.plot(res['x_max'], res['y_max'], 'ro', markersize=6)
            
            # Texto com informações
            plt.text(res['x_max'], res['y_max'], 
                    f"Peak {res['peak_id']}\nX: {res['x_max']:.2f}\nY: {res['y_max']:.2f}",
                    ha='left', va='bottom', fontsize=8,
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.title('Peak Detection Analysis')
    plt.xlabel('F [μHz]')
    plt.ylabel('A [mma]')
    plt.legend()
    plt.grid(True)
    
    # Tabela de resultados
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
