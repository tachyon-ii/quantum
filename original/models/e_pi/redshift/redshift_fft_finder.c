/*
 * redshift_fft_finder.c
 * gcc -O3 redshift_fft_finder.c -o redshift_fft_finder -lfftw3 -lm -I/opt/homebrew/Cellar/fftw/3.3.10_2/include -L/opt/homebrew/Cellar/fftw/3.3.10_2/lib
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <fftw3.h>

#define NUM_HARMONICS 11
#define PI 3.14159265358979323846
#define MAX_SAMPLES 360000

float f_n(int n) {
    return pow(M_E, n) / PI;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <input_file> <redshift>\n", argv[0]);
        return 1;
    }

    const char *filename = argv[1];
    double z = atof(argv[2]);

    FILE *f = fopen(filename, "rb");
    if (!f) {
        perror("Failed to open input file");
        return 1;
    }

    float *time = malloc(sizeof(float) * MAX_SAMPLES);
    float *signal = malloc(sizeof(float) * MAX_SAMPLES);
    int count = 0;
    while (count < MAX_SAMPLES && fread(&time[count], sizeof(float), 1, f) == 1 &&
           fread(&signal[count], sizeof(float), 1, f) == 1) {
        ++count;
    }
    fclose(f);

    printf("Loaded %d samples\n", count);

    // Apply Hann window
    for (int i = 0; i < count; ++i) {
        double hann = 0.5 * (1.0 - cos(2 * PI * i / (count - 1)));
        signal[i] *= hann;
    }

    fftw_complex *out = fftw_malloc(sizeof(fftw_complex) * (count / 2 + 1));
    double *in = fftw_malloc(sizeof(double) * count);
    for (int i = 0; i < count; ++i) {
        in[i] = signal[i];
    }

    fftw_plan plan = fftw_plan_dft_r2c_1d(count, in, out, FFTW_ESTIMATE);
    fftw_execute(plan);

    double sample_rate = 1.0 / (time[1] - time[0]);
    double df = sample_rate / count;

    double total_power = 0.0;
    for (int n = 0; n < NUM_HARMONICS; ++n) {
        double target_freq = f_n(n) / (1.0 + z);
        int bin = (int)(target_freq / df);
        double power = 0.0;
        for (int i = bin - 2; i <= bin + 2; ++i) {
            if (i >= 0 && i < count / 2 + 1) {
                double re = out[i][0];
                double im = out[i][1];
                power += (re * re + im * im) / count;
            }
        }
        printf("n=%2d | f=%.6f Hz | bin=%5d | power=%.6e\n", n, target_freq, bin, power);
        total_power += power;
    }

    printf("Total scroll harmonic power: %.6e\n", total_power);

    fftw_destroy_plan(plan);
    fftw_free(in);
    fftw_free(out);
    free(time);
    free(signal);

    return 0;
}

