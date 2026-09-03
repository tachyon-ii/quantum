/*
 * monte-casino.c
 * gcc -O3 -Wall -march=native -ffast-math monte-casino.c -o monte-casino -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>

// High precision constants
#define E 2.718281828459045235360287471352662497757247093699959574966L
#define PI 3.141592653589793238462643383279502884197169399375105820974L
#define SMALL 1e-9L
#define PHI ((1.0L + sqrtl(5.0L)) / 2.0L)

// Test constants around e and π
#define QE_MINUS (E - SMALL)
#define QE_PLUS (E + SMALL)
#define QPI_MINUS (PI - SMALL)
#define QPI_PLUS (PI + SMALL)

// Additional candidate constants for Q'
#define SQRT2 1.414213562373095048801688724209698078569671875376948073176L
#define SQRT3 1.732050807568877293527446341505872366942805253810380628055L
#define SQRT5 2.236067977499789696409173668731276235440618359611525724270L
#define SQRT7 2.645751311064590590501615753639260425710259183082450180368L
#define EULER_GAMMA 0.577215664901532860606512090082402431042159335939923598805L
#define CATALAN 0.915965594177219015054603514932384110774149374281672134266L

// Simulation parameters
#define NUM_FREQUENCIES 7
#define MAX_FREQ 1000.0L
#define NUM_TRIALS 10000
#define DURATION (8.0L * E * PI)  // Clean multiples of lowest frequency waves
#define SAMPLE_RATE 8192

#define MAX_SETS 50
#define MAX_NAME_LEN 60

// Structure to hold frequency set data
typedef struct {
    char name[MAX_NAME_LEN];
    long double frequencies[NUM_FREQUENCIES];
    int count;
    long double base_constant;
    char description[30];
} FrequencySet;

// Structure to hold simulation results
typedef struct {
    char name[MAX_NAME_LEN];
    long double mean_peak;
    long double std_dev;
    long double signal_to_noise;
    long double base_constant;
    char description[30];
} SimulationResult;

// --- Normalization function ---
void normalize_set(long double *frequencies, int count, long double max_val) {
    if (count <= 0) return;
    
    long double current_max = 0.0L;
    for (int i = 0; i < count; i++) {
        if (frequencies[i] > current_max) {
            current_max = frequencies[i];
        }
    }
    
    if (current_max == 0.0L) return;
    
    long double scaling_factor = max_val / current_max;
    for (int i = 0; i < count; i++) {
        frequencies[i] *= scaling_factor;
    }
}

// --- Unicode-aware padding function ---
int count_visual_chars(const char *str) {
    int visual_count = 0;
    int i = 0;
    
    while (str[i] != '\0') {
        unsigned char c = str[i];
        if (c < 0x80) {
            // ASCII character
            i++;
        } else if ((c & 0xE0) == 0xC0) {
            // 2-byte UTF-8 character
            i += 2;
        } else if ((c & 0xF0) == 0xE0) {
            // 3-byte UTF-8 character
            i += 3;
        } else if ((c & 0xF8) == 0xF0) {
            // 4-byte UTF-8 character
            i += 4;
        } else {
            // Invalid UTF-8, treat as single byte
            i++;
        }
        visual_count++;
    }
    return visual_count;
}

void print_padded(const char *str, int width) {
    int visual_chars = count_visual_chars(str);
    int padding = width - visual_chars;
    if (padding < 0) padding = 0;
    
    printf("%s", str);
    for (int i = 0; i < padding; i++) {
        printf(" ");
    }
}

// --- Random number generator (0 to 1) ---
long double random_uniform() {
    return (long double)rand() / RAND_MAX;
}

// --- The Monte Carlo Simulation Function ---
void run_monte_carlo_interference_sim(long double *frequencies, int freq_count, 
                                    long double *mean_peak, long double *std_dev) {
    long double *peak_amplitudes = malloc(NUM_TRIALS * sizeof(long double));
    long double max_freq = 0.0L;
    
    // Find maximum frequency
    for (int i = 0; i < freq_count; i++) {
        if (frequencies[i] > max_freq) {
            max_freq = frequencies[i];
        }
    }
    
    long double effective_sample_rate = fmaxl(SAMPLE_RATE, max_freq * 2.5L);
    int num_samples = (int)(DURATION * effective_sample_rate);
    
    for (int trial = 0; trial < NUM_TRIALS; trial++) {
        // Generate random phases for this trial
        long double phases[NUM_FREQUENCIES];
        for (int freq_idx = 0; freq_idx < freq_count; freq_idx++) {
            phases[freq_idx] = random_uniform() * 2.0L * PI;
        }
        
        long double peak_amplitude = 0.0L;
        
        // Generate superimposed wave and find peak
        for (int sample = 0; sample < num_samples; sample++) {
            long double t = (long double)sample / effective_sample_rate;
            long double superimposed_value = 0.0L;
            
            for (int freq_idx = 0; freq_idx < freq_count; freq_idx++) {
                superimposed_value += sinl(2.0L * PI * frequencies[freq_idx] * t + phases[freq_idx]);
            }
            
            long double abs_value = fabsl(superimposed_value);
            if (abs_value > peak_amplitude) {
                peak_amplitude = abs_value;
            }
        }
        
        peak_amplitudes[trial] = peak_amplitude;
    }
    
    // Calculate mean
    long double sum = 0.0L;
    for (int i = 0; i < NUM_TRIALS; i++) {
        sum += peak_amplitudes[i];
    }
    *mean_peak = sum / NUM_TRIALS;
    
    // Calculate standard deviation
    long double variance_sum = 0.0L;
    for (int i = 0; i < NUM_TRIALS; i++) {
        long double diff = peak_amplitudes[i] - *mean_peak;
        variance_sum += diff * diff;
    }
    *std_dev = sqrtl(variance_sum / NUM_TRIALS);
    
    free(peak_amplitudes);
}

// --- Generate power sequence for a given base ---
void generate_power_sequence(long double *result, long double base, int n) {
    for (int i = 0; i < n; i++) {
        result[i] = powl(base, i + 2);
    }
}

// --- Generate modified power sequence (base^n / modifier) ---
void generate_modified_power_sequence(long double *result, long double base, long double modifier, int n) {
    for (int i = 0; i < n; i++) {
        result[i] = powl(base, i + 2) / modifier;
    }
}

// --- Comparison function for sorting results ---
int compare_results(const void *a, const void *b) {
    SimulationResult *resA = (SimulationResult *)a;
    SimulationResult *resB = (SimulationResult *)b;
    
    if (resB->signal_to_noise > resA->signal_to_noise) return 1;
    if (resB->signal_to_noise < resA->signal_to_noise) return -1;
    return 0;
}

int main() {
    // Seed random number generator
    srand(time(NULL));
    
    printf("=== GOLDILOCKS PEAK ANALYSIS FOR e AND π ===\n");
    printf("Testing bimodal peaks hypothesis and searching for superior Q'\n");
    printf("Duration: %.6Lf seconds (8 * e * π)\n", DURATION);
    printf("Frequencies: %d, Trials: %d\n\n", NUM_FREQUENCIES, NUM_TRIALS);
    
    // --- Generate all frequency sets ---
    FrequencySet sets[MAX_SETS];
    int set_count = 0;
    
    // Type 1: Pure power sequences
    // e group
    strcpy(sets[set_count].name, "(e-ε)^n");
    strcpy(sets[set_count].description, "e minus epsilon");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = E - SMALL;
    generate_power_sequence(sets[set_count].frequencies, E - SMALL, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "e^n");
    strcpy(sets[set_count].description, "Euler's number");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = E;
    generate_power_sequence(sets[set_count].frequencies, E, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "(e+ε)^n");
    strcpy(sets[set_count].description, "e plus epsilon");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = E + SMALL;
    generate_power_sequence(sets[set_count].frequencies, E + SMALL, NUM_FREQUENCIES);
    set_count++;
    
    // Type 2: Modified power sequences (base^n / modifier)
    // e^n / π group
    strcpy(sets[set_count].name, "(e-ε)^n/π");
    strcpy(sets[set_count].description, "e-ε powers over pi");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = E - SMALL;
    generate_modified_power_sequence(sets[set_count].frequencies, E - SMALL, PI, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "e^n/π");
    strcpy(sets[set_count].description, "e powers over pi");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = E;
    generate_modified_power_sequence(sets[set_count].frequencies, E, PI, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "(e+ε)^n/π");
    strcpy(sets[set_count].description, "e+ε powers over pi");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = E + SMALL;
    generate_modified_power_sequence(sets[set_count].frequencies, E + SMALL, PI, NUM_FREQUENCIES);
    set_count++;
    
    // π group
    strcpy(sets[set_count].name, "(π-ε)^n");
    strcpy(sets[set_count].description, "pi minus epsilon");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = PI - SMALL;
    generate_power_sequence(sets[set_count].frequencies, PI - SMALL, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "π^n");
    strcpy(sets[set_count].description, "Pi");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = PI;
    generate_power_sequence(sets[set_count].frequencies, PI, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "(π+ε)^n");
    strcpy(sets[set_count].description, "pi plus epsilon");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = PI + SMALL;
    generate_power_sequence(sets[set_count].frequencies, PI + SMALL, NUM_FREQUENCIES);
    set_count++;
    
    // π^n / e group
    strcpy(sets[set_count].name, "(π-ε)^n/e");
    strcpy(sets[set_count].description, "π-ε powers over e");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = PI - SMALL;
    generate_modified_power_sequence(sets[set_count].frequencies, PI - SMALL, E, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "π^n/e");
    strcpy(sets[set_count].description, "pi powers over e");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = PI;
    generate_modified_power_sequence(sets[set_count].frequencies, PI, E, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "(π+ε)^n/e");
    strcpy(sets[set_count].description, "π+ε powers over e");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = PI + SMALL;
    generate_modified_power_sequence(sets[set_count].frequencies, PI + SMALL, E, NUM_FREQUENCIES);
    set_count++;
    
    // Type 3: Ratio base sequences
    strcpy(sets[set_count].name, "(π/e)^n");
    strcpy(sets[set_count].description, "pi over e ratio");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = PI / E;
    generate_power_sequence(sets[set_count].frequencies, PI / E, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "(e/π)^n");
    strcpy(sets[set_count].description, "e over pi ratio");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = E / PI;
    generate_power_sequence(sets[set_count].frequencies, E / PI, NUM_FREQUENCIES);
    set_count++;
    
    // Sanity check sequences
    strcpy(sets[set_count].name, "√2^n");
    strcpy(sets[set_count].description, "Square root of 2");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = SQRT2;
    generate_power_sequence(sets[set_count].frequencies, SQRT2, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "3^n");
    strcpy(sets[set_count].description, "Powers of 3");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = 3.0L;
    generate_power_sequence(sets[set_count].frequencies, 3.0L, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "2^n");
    strcpy(sets[set_count].description, "Powers of 2");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = 2.0L;
    generate_power_sequence(sets[set_count].frequencies, 2.0L, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "φ^n");
    strcpy(sets[set_count].description, "Golden ratio");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = PHI;
    generate_power_sequence(sets[set_count].frequencies, PHI, NUM_FREQUENCIES);
    set_count++;
    
    // Additional interesting constants
    strcpy(sets[set_count].name, "((e+π)/2)^n");
    strcpy(sets[set_count].description, "Arithmetic mean of e,π");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = (E + PI) / 2.0L;
    generate_power_sequence(sets[set_count].frequencies, (E + PI) / 2.0L, NUM_FREQUENCIES);
    set_count++;
    
    strcpy(sets[set_count].name, "√95^n");
    strcpy(sets[set_count].description, "Square root of 95");
    sets[set_count].count = NUM_FREQUENCIES;
    sets[set_count].base_constant = sqrtl(95.0L);
    generate_power_sequence(sets[set_count].frequencies, sqrtl(95.0L), NUM_FREQUENCIES);
    set_count++;
    
    // --- Normalize all sets ---
    for (int i = 0; i < set_count; i++) {
        normalize_set(sets[i].frequencies, sets[i].count, MAX_FREQ);
    }
    
    // --- Run simulations ---
    SimulationResult results[MAX_SETS];
    int result_count = 0;
    
    printf("Running simulations...\n\n");
    
    for (int i = 0; i < set_count; i++) {
        long double mean_peak, std_dev;
        run_monte_carlo_interference_sim(sets[i].frequencies, sets[i].count, 
                                       &mean_peak, &std_dev);
        
        strcpy(results[result_count].name, sets[i].name);
        results[result_count].mean_peak = mean_peak;
        results[result_count].std_dev = std_dev;
        results[result_count].signal_to_noise = (std_dev > 0) ? mean_peak / std_dev : 0.0L;
        results[result_count].base_constant = sets[i].base_constant;
        strcpy(results[result_count].description, sets[i].description);
        result_count++;
        
        // Progress indicator
        printf("Completed %d/%d simulations...\n", i + 1, set_count);
    }
    
    // --- Sort results by coherence (signal to noise ratio) ---
    qsort(results, result_count, sizeof(SimulationResult), compare_results);
    
    // --- Display results ---
    printf("\n=== GOLDILOCKS PEAK ANALYSIS RESULTS ===\n");
    printf("Duration: %.6Lf seconds, Frequencies: %d, Trials: %d\n", DURATION, NUM_FREQUENCIES, NUM_TRIALS);
    printf("---------------------------------------------------------------------------------------------\n");
    printf("Sequence        | Mean Peak    | Std Dev      | S/N Ratio       | Base Const   | Description         \n");
    printf("---------------------------------------------------------------------------------------------\n");
    
    for (int i = 0; i < result_count; i++) {
        print_padded(results[i].name, 15);
        printf(" | %12.6Lf | %12.6Lf | %15.6Lf | %12.9Lf | %-20s\n",
               results[i].mean_peak, results[i].std_dev, results[i].signal_to_noise, 
               results[i].base_constant, results[i].description);
    }
    
    printf("---------------------------------------------------------------------------------------------\n");
    
    // --- Analysis of results ---
    printf("\n=== GOLDILOCKS PEAK ANALYSIS ===\n");
    
    // Find e and π performance
    long double e_performance = 0.0L, pi_performance = 0.0L;
    long double e_minus_performance = 0.0L, e_plus_performance = 0.0L;
    long double pi_minus_performance = 0.0L, pi_plus_performance = 0.0L;
    
    for (int i = 0; i < result_count; i++) {
        long double base = results[i].base_constant;
        if (fabsl(base - E) < 1e-10L && strstr(results[i].name, "e^n") != NULL && strstr(results[i].name, "/") == NULL) {
            e_performance = results[i].signal_to_noise;
        } else if (fabsl(base - PI) < 1e-10L && strstr(results[i].name, "π^n") != NULL && strstr(results[i].name, "/") == NULL) {
            pi_performance = results[i].signal_to_noise;
        } else if (fabsl(base - (E - SMALL)) < 1e-10L && strstr(results[i].name, "(e-ε)^n") != NULL && strstr(results[i].name, "/") == NULL) {
            e_minus_performance = results[i].signal_to_noise;
        } else if (fabsl(base - (E + SMALL)) < 1e-10L && strstr(results[i].name, "(e+ε)^n") != NULL && strstr(results[i].name, "/") == NULL) {
            e_plus_performance = results[i].signal_to_noise;
        } else if (fabsl(base - (PI - SMALL)) < 1e-10L && strstr(results[i].name, "(π-ε)^n") != NULL && strstr(results[i].name, "/") == NULL) {
            pi_minus_performance = results[i].signal_to_noise;
        } else if (fabsl(base - (PI + SMALL)) < 1e-10L && strstr(results[i].name, "(π+ε)^n") != NULL && strstr(results[i].name, "/") == NULL) {
            pi_plus_performance = results[i].signal_to_noise;
        }
    }
    
    printf("\nPOSTULATE #1 ANALYSIS (Bimodal Goldilocks Peaks):\n");
    printf("e^n performance:       %.6Lf\n", e_performance);
    printf("(e-ε)^n performance:   %.6Lf (change: %+.6Lf)\n", e_minus_performance, e_minus_performance - e_performance);
    printf("(e+ε)^n performance:   %.6Lf (change: %+.6Lf)\n", e_plus_performance, e_plus_performance - e_performance);
    printf("π^n performance:       %.6Lf\n", pi_performance);
    printf("(π-ε)^n performance:   %.6Lf (change: %+.6Lf)\n", pi_minus_performance, pi_minus_performance - pi_performance);
    printf("(π+ε)^n performance:   %.6Lf (change: %+.6Lf)\n", pi_plus_performance, pi_plus_performance - pi_performance);
    
    printf("\nPOSTULATE #2 ANALYSIS (e^n/π superiority):\n");
    printf("Best performer: %s\n", results[0].name);
    printf("Best S/N ratio: %.6Lf\n", results[0].signal_to_noise);
    
    // Find e^n/π performance specifically
    long double e_over_pi_performance = 0.0L;
    for (int i = 0; i < result_count; i++) {
        if (strcmp(results[i].name, "e^n/π") == 0) {
            e_over_pi_performance = results[i].signal_to_noise;
            break;
        }
    }
    
    if (strcmp(results[0].name, "e^n/π") == 0) {
        printf("*** POSTULATE #2 CONFIRMED: e^n/π is the superior sequence! ***\n");
        printf("e^n/π outperforms all other sequences tested.\n");
    } else {
        printf("e^n/π performance: %.6Lf (ranked #", e_over_pi_performance);
        // Find rank of e^n/π
        for (int i = 0; i < result_count; i++) {
            if (strcmp(results[i].name, "e^n/π") == 0) {
                printf("%d)\n", i + 1);
                break;
            }
        }
        printf("Postulate #2 not confirmed - e^n/π is not the top performer.\n");
    }
    
    printf("\nTop 5 performers:\n");
    for (int i = 0; i < 5 && i < result_count; i++) {
        printf("%d. %s (%.6Lf)\n", i+1, results[i].name, results[i].signal_to_noise);
    }
    
    return 0;
}
