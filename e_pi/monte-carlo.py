import numpy as np
import math

# --- Helper functions to generate fixed-size frequency sequences ---

def get_first_n_fibonacci(n):
    """Gets the first n Fibonacci numbers (starting > 0)."""
    if n <= 0: return []
    seq = [1, 2]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]

def get_first_n_primes(n):
    """Gets the first n prime numbers."""
    primes = []
    num = 2
    while len(primes) < n:
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    return primes

def get_first_n_powers(n, power):
    """Gets the first n integer powers (starting from 2^power)."""
    return [(i**power) for i in range(2, n + 2)]

# --- NEW NORMALIZATION FUNCTION ---
def normalize_set(frequencies, max_val=1000.0):
    """Scales a list of frequencies to have a specific maximum value."""
    if not frequencies or max(frequencies) == 0:
        return []
    
    current_max = float(max(frequencies))
    scaling_factor = max_val / current_max
    
    return [freq * scaling_factor for freq in frequencies]

# --- The Monte Carlo Simulation Function (unchanged) ---

def run_monte_carlo_interference_sim(frequencies, num_trials=50000, duration=1.0, sample_rate=4096):
    """
    Runs a Monte Carlo simulation to test the interference properties of a set of frequencies.
    """
    peak_amplitudes = []
    max_freq = max(frequencies) if frequencies else 1
    effective_sample_rate = max(sample_rate, max_freq * 2.5) 
    t = np.linspace(0, duration, int(duration * effective_sample_rate), endpoint=False)

    for _ in range(num_trials):
        superimposed_wave = np.zeros_like(t)
        for freq in frequencies:
            phase = np.random.uniform(0, 2 * np.pi)
            superimposed_wave += np.sin(2 * np.pi * float(freq) * t + phase)
        
        peak_amplitude = np.max(np.abs(superimposed_wave))
        peak_amplitudes.append(peak_amplitude)

    mean_peak = np.mean(peak_amplitudes)
    std_dev_peak = np.std(peak_amplitudes)

    return mean_peak, std_dev_peak

if __name__ == '__main__':
    NUM_FREQUENCIES = 7

    print(f"Generating and normalizing frequency sets (size={NUM_FREQUENCIES}, max_freq=1000 Hz)...\n")

    # --- Define constants ---
    phi = (1 + math.sqrt(5)) / 2
    sqrt2 = math.sqrt(2)
    q_prime = math.sqrt(95)

    # --- Generate all raw frequency sets ---
    raw_sets = {
        "Exponential Harmony (e^n/π)": [np.exp(n) for n in range(2, NUM_FREQUENCIES + 2)],
        "Inverted Exponential (π^n/e)": [np.pi**n for n in range(2, NUM_FREQUENCIES + 2)],
        "Pure Exponential (e^n)": [np.exp(n) for n in range(2, NUM_FREQUENCIES + 2)],
        "Pure Pi Power (π^n)": [np.pi**n for n in range(2, NUM_FREQUENCIES + 2)],
        "Pure Golden Power (φ^n)": [phi**n for n in range(2, NUM_FREQUENCIES + 2)],
        "Pure Sqrt(2) Power": [sqrt2**n for n in range(2, NUM_FREQUENCIES + 2)],
        "Pure Q' (sqrt(95)) Power": [q_prime**n for n in range(2, NUM_FREQUENCIES + 2)],
        "Simple Harmonics (2^n)": [2**n for n in range(1, NUM_FREQUENCIES + 1)],
        "Fibonacci Sequence": get_first_n_fibonacci(NUM_FREQUENCIES),
        "Prime Numbers": get_first_n_primes(NUM_FREQUENCIES),
        "Squares (n^2)": get_first_n_powers(NUM_FREQUENCIES, 2),
        "Cubes (n^3)": get_first_n_powers(NUM_FREQUENCIES, 3),
        # NEW SETS AS REQUESTED
        "Linear Sequence (n)": [n for n in range(1, NUM_FREQUENCIES + 1)],
        "Harmonics from 1 (2^n)": [2**n for n in range(0, NUM_FREQUENCIES)]
    }
    
    # --- Normalize all sets and prepare for testing ---
    sets_to_test = []
    for name, freq_set in raw_sets.items():
        normalized = normalize_set(freq_set)
        sets_to_test.append((name, normalized))

    results = []
    print("Running simulations...\n")

    for name, freq_set in sets_to_test:
        if freq_set:
            mean_peak, std_dev = run_monte_carlo_interference_sim(freq_set)
            signal_to_noise = mean_peak / std_dev if std_dev > 0 else 0
            results.append({
                "name": name, 
                "mean_peak": mean_peak, 
                "std_dev": std_dev, 
                "signal_to_noise": signal_to_noise
            })

    # --- Sort and present the results by coherence ---
    
    results_sorted_by_coherence = sorted(results, key=lambda x: x['signal_to_noise'], reverse=True)

    print("--- Simulation Results (Normalized Sets, Size: 7) ---")
    print("-" * 90)
    print(f"{'Sequence Name':<30} | {'Mean Peak Amp':<15} | {'Std Dev':<15} | {'Signal/Noise (Coherence)':<25}")
    print("-" * 90)
    
    for res in results_sorted_by_coherence:
        print(f"{res['name']:<30} | {res['mean_peak']:<15.4f} | {res['std_dev']:<15.4f} | {res['signal_to_noise']:<25.4f}")
    
    print("-" * 90)

    print("\n--- Conclusion ---")
    print(f"The most coherent interference pattern (highest Signal/Noise ratio) was produced by:")
    print(f"** {results_sorted_by_coherence[0]['name']} **")
