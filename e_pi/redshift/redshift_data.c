/*
 * redshift_data.c
 * gcc -O3 redshift_data.c -o redshift_data -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>

#define DURATION_SECONDS 360000
#define SAMPLE_RATE 10
#define Z_REDSHIFT 1089.0
#define PI 3.14159265358979323846
#define AMP_SCALE 1e-6
#define NOISE_STD 1.0
#define NUM_HARMONICS 11

float randn() {
    static int hasSpare = 0;
    static double spare;
    if (hasSpare) {
        hasSpare = 0;
        return spare;
    }
    hasSpare = 1;
    double u, v, s;
    do {
        u = (rand() / ((double)RAND_MAX)) * 2.0 - 1.0;
        v = (rand() / ((double)RAND_MAX)) * 2.0 - 1.0;
        s = u * u + v * v;
    } while (s >= 1.0 || s == 0.0);
    s = sqrt(-2.0 * log(s) / s);
    spare = v * s;
    return u * s;
}

float f_n(int n) {
    return pow(M_E, n) / PI;
}

float amplitude_for_n(int n, const char *mode, int noise_only, int signal_only) {
    if (noise_only) return 0.0;
    if (strcmp(mode, "inverse") == 0)
        return AMP_SCALE / (1.0 + n);
    else if (strcmp(mode, "direct") == 0)
        return AMP_SCALE * (1.0 + n);
    else
        return AMP_SCALE;
}

int main(int argc, char *argv[]) {
    int noise_only = 0;
    int signal_only = 0;
    const char *mode = "flat";

    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "--noise-only") == 0) {
            noise_only = 1;
        } else if (strcmp(argv[i], "--signal-only") == 0) {
            signal_only = 1;
        } else {
            mode = argv[i];
        }
    }

    FILE *f = fopen("scroll_data.bin", "wb");
    if (!f) {
        perror("Failed to open output file");
        return 1;
    }

    srand(time(NULL));
    const int total_samples = DURATION_SECONDS * SAMPLE_RATE;
    const float dt = 1.0f / SAMPLE_RATE;

    float *phases = malloc(sizeof(float) * NUM_HARMONICS);
    float *freqs = malloc(sizeof(float) * NUM_HARMONICS);

    for (int n = 0; n < NUM_HARMONICS; ++n) {
        freqs[n] = f_n(n) / (1.0 + Z_REDSHIFT);
        phases[n] = 0.0f; // set constant phase for testability
    }

    for (int i = 0; i < total_samples; ++i) {
        float t = i * dt;
        float window = 0.5f * (1.0f - cosf(2.0f * PI * i / (total_samples - 1)));
        float sample = signal_only ? 0.0f : randn() * NOISE_STD * window;

        for (int n = 0; n < NUM_HARMONICS; ++n) {
            float amp = amplitude_for_n(n, mode, noise_only, signal_only);
            float freq = freqs[n];
            sample += amp;
        }

        fwrite(&t, sizeof(float), 1, f);
        fwrite(&sample, sizeof(float), 1, f);
    }

    fclose(f);
    free(phases);
    free(freqs);

    printf("Generated scroll_data.bin (%d samples)%s%s\n", total_samples,
           noise_only ? " [noise only mode]" : "",
           signal_only ? " [signal only mode]" : "");
    return 0;
}

