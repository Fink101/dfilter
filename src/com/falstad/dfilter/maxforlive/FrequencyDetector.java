package com.falstad.dfilter.maxforlive;

import com.falstad.dfilter.client.FFT;

/**
 * Core frequency detection module using FFT analysis
 * Detects the dominant frequency in an audio signal
 */
public class FrequencyDetector {
    private FFT fft;
    private int fftSize;
    private double sampleRate;
    private double[] fftBuffer;
    private double dominantFrequency;
    private double dominantMagnitude;

    public FrequencyDetector(int fftSize, double sampleRate) {
        this.fftSize = fftSize;
        this.sampleRate = sampleRate;
        this.fft = new FFT(fftSize);
        this.fftBuffer = new double[fftSize * 2]; // Complex numbers: real, imag pairs
        this.dominantFrequency = 0.0;
        this.dominantMagnitude = 0.0;
    }

    /**
     * Analyze audio samples and detect dominant frequency
     * @param samples Input audio samples
     */
    public void analyze(double[] samples) {
        if (samples.length != fftSize) {
            throw new IllegalArgumentException("Sample count must match FFT size: " + fftSize);
        }

        // Copy samples to FFT buffer (real part) and zero imaginary part
        for (int i = 0; i < fftSize; i++) {
            fftBuffer[i * 2] = samples[i];
            fftBuffer[i * 2 + 1] = 0.0;
        }

        // Apply Hamming window to reduce spectral leakage
        applyHammingWindow();

        // Perform FFT
        fft.transform(fftBuffer, false);

        // Find dominant frequency (peak in magnitude spectrum)
        findDominantFrequency();
    }

    /**
     * Apply Hamming window to input samples
     */
    private void applyHammingWindow() {
        for (int i = 0; i < fftSize; i++) {
            double window = 0.54 - 0.46 * Math.cos(2.0 * Math.PI * i / (fftSize - 1));
            fftBuffer[i * 2] *= window;
        }
    }

    /**
     * Find the dominant frequency from FFT results
     */
    private void findDominantFrequency() {
        int maxBin = 0;
        double maxMagnitude = 0.0;

        // Only check first half of FFT (Nyquist limit)
        // Skip DC component (bin 0)
        for (int i = 1; i < fftSize / 2; i++) {
            double real = fftBuffer[i * 2];
            double imag = fftBuffer[i * 2 + 1];
            double magnitude = Math.sqrt(real * real + imag * imag);

            if (magnitude > maxMagnitude) {
                maxMagnitude = magnitude;
                maxBin = i;
            }
        }

        // Convert bin to frequency
        this.dominantFrequency = (maxBin * sampleRate) / fftSize;
        this.dominantMagnitude = maxMagnitude;

        // Parabolic interpolation for more accurate frequency estimation
        if (maxBin > 0 && maxBin < fftSize / 2 - 1) {
            double prevReal = fftBuffer[(maxBin - 1) * 2];
            double prevImag = fftBuffer[(maxBin - 1) * 2 + 1];
            double prevMag = Math.sqrt(prevReal * prevReal + prevImag * prevImag);

            double nextReal = fftBuffer[(maxBin + 1) * 2];
            double nextImag = fftBuffer[(maxBin + 1) * 2 + 1];
            double nextMag = Math.sqrt(nextReal * nextReal + nextImag * nextImag);

            double delta = 0.5 * (prevMag - nextMag) / (prevMag - 2 * maxMagnitude + nextMag);
            this.dominantFrequency = ((maxBin + delta) * sampleRate) / fftSize;
        }
    }

    /**
     * Get the detected dominant frequency in Hz
     */
    public double getDominantFrequency() {
        return dominantFrequency;
    }

    /**
     * Get the magnitude of the dominant frequency
     */
    public double getDominantMagnitude() {
        return dominantMagnitude;
    }

    /**
     * Get the current sample rate
     */
    public double getSampleRate() {
        return sampleRate;
    }

    /**
     * Get the FFT size
     */
    public int getFFTSize() {
        return fftSize;
    }

    /**
     * Get the full magnitude spectrum
     * @return Array of magnitudes for each frequency bin
     */
    public double[] getMagnitudeSpectrum() {
        double[] spectrum = new double[fftSize / 2];
        for (int i = 0; i < fftSize / 2; i++) {
            double real = fftBuffer[i * 2];
            double imag = fftBuffer[i * 2 + 1];
            spectrum[i] = Math.sqrt(real * real + imag * imag);
        }
        return spectrum;
    }
}
