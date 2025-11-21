package com.falstad.dfilter.maxforlive;

import com.cycling74.max.MaxObject;
import com.cycling74.max.DataTypes;
import javax.swing.JFrame;

/**
 * Max for Live frequency detector plugin (mxj object)
 *
 * Usage in Max:
 *   [mxj com.falstad.dfilter.maxforlive.MaxFrequencyPlugin]
 *
 * Inlets:
 *   0: Audio signal list (buffer of samples)
 *   1: Control messages (bang, reset, samplerate)
 *
 * Outlets:
 *   0: Detected frequency (float, Hz)
 *   1: Magnitude (float)
 *   2: Note name (string)
 */
public class MaxFrequencyPlugin extends MaxObject {
    private FrequencyDetector detector;
    private FrequencyUI ui;
    private JFrame uiFrame;
    private int fftSize = 2048;
    private double sampleRate = 44100.0;
    private double[] sampleBuffer;
    private int bufferPos = 0;

    /**
     * Constructor - called when object is created in Max
     */
    public MaxFrequencyPlugin() {
        // Declare 2 inlets: audio signal, control
        declareInlets(new int[]{DataTypes.ALL, DataTypes.ALL});

        // Declare 3 outlets: frequency, magnitude, note
        declareOutlets(new int[]{DataTypes.FLOAT, DataTypes.FLOAT, DataTypes.ALL});

        // Initialize detector
        detector = new FrequencyDetector(fftSize, sampleRate);
        sampleBuffer = new double[fftSize];
        bufferPos = 0;

        post("DFilter Frequency Detector initialized");
        post("FFT Size: " + fftSize + ", Sample Rate: " + sampleRate + " Hz");
    }

    /**
     * Handle bang message - trigger analysis
     */
    public void bang() {
        analyze();
    }

    /**
     * Handle list of audio samples
     */
    public void list(float[] samples) {
        // Accumulate samples into buffer
        for (float sample : samples) {
            sampleBuffer[bufferPos++] = sample;

            // When buffer is full, analyze
            if (bufferPos >= fftSize) {
                analyze();
                bufferPos = 0;
            }
        }
    }

    /**
     * Set sample rate
     */
    public void samplerate(float rate) {
        this.sampleRate = rate;
        detector = new FrequencyDetector(fftSize, rate);
        post("Sample rate set to: " + rate + " Hz");
    }

    /**
     * Set FFT size (must be power of 2)
     */
    public void fftsize(int size) {
        if ((size & (size - 1)) != 0) {
            error("FFT size must be power of 2");
            return;
        }
        this.fftSize = size;
        detector = new FrequencyDetector(fftSize, sampleRate);
        sampleBuffer = new double[fftSize];
        bufferPos = 0;
        post("FFT size set to: " + size);
    }

    /**
     * Reset the detector
     */
    public void reset() {
        bufferPos = 0;
        for (int i = 0; i < sampleBuffer.length; i++) {
            sampleBuffer[i] = 0.0;
        }
        post("Detector reset");
    }

    /**
     * Show UI window
     */
    public void showui() {
        if (uiFrame == null) {
            createUI();
        }
        uiFrame.setVisible(true);
    }

    /**
     * Hide UI window
     */
    public void hideui() {
        if (uiFrame != null) {
            uiFrame.setVisible(false);
        }
    }

    /**
     * Create UI window
     */
    private void createUI() {
        ui = new FrequencyUI();
        uiFrame = new javax.swing.JFrame("Frequency Detector");
        uiFrame.setDefaultCloseOperation(javax.swing.JFrame.HIDE_ON_CLOSE);
        uiFrame.add(ui);
        uiFrame.pack();
        uiFrame.setLocationRelativeTo(null);
    }

    /**
     * Perform frequency analysis and output results
     */
    private void analyze() {
        try {
            // Analyze samples
            detector.analyze(sampleBuffer);

            double frequency = detector.getDominantFrequency();
            double magnitude = detector.getDominantMagnitude();

            // Output to Max outlets
            outlet(0, (float) frequency);
            outlet(1, (float) magnitude);
            outlet(2, frequencyToNote(frequency));

            // Update UI if visible
            if (ui != null) {
                ui.updateFrequency(frequency, magnitude);
            }

        } catch (Exception e) {
            error("Analysis error: " + e.getMessage());
        }
    }

    /**
     * Convert frequency to note name
     */
    private String frequencyToNote(double frequency) {
        if (frequency < 20 || frequency > 20000) {
            return "--";
        }

        String[] noteNames = {"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"};
        double a4 = 440.0;
        double semitones = 12 * (Math.log(frequency / a4) / Math.log(2));
        int semitonesRounded = (int) Math.round(semitones);
        int noteIndex = (semitonesRounded + 9) % 12;
        if (noteIndex < 0) noteIndex += 12;
        int octave = 4 + (semitonesRounded + 9) / 12;

        return noteNames[noteIndex] + octave;
    }

    /**
     * Cleanup when object is deleted
     */
    protected void notifyDeleted() {
        if (uiFrame != null) {
            uiFrame.dispose();
        }
    }
}
