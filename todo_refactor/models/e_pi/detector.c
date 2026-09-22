#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

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

    double total_power = 0.0;
    for (int n = 0; n < NUM_HARMONICS; ++n) {
        double freq = f_n(n) / (1.0 + z);
        double sin_sum = 0.0, cos_sum = 0.0;

        for (int i = 0; i < count; ++i) {
            double t = time[i];
            double s = signal[i];
            double phase = 2.0 * PI * freq * t;
            sin_sum += s * sin(phase);
            cos_sum += s * cos(phase);
        }

        double power = (sin_sum * sin_sum + cos_sum * cos_sum) / count;
        printf("n=%2d | f=%.6f Hz | power=%.6e\n", n, freq, power);
        total_power += power;
    }

    printf("Total scroll harmonic power: %.6e\n", total_power);

    free(time);
    free(signal);

    return 0;
}

