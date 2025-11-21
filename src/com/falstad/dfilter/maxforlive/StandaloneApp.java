package com.falstad.dfilter.maxforlive;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import javax.sound.sampled.*;

/**
 * Standalone application for frequency detection
 * Generates test tones and displays detected frequency in real-time
 */
public class StandaloneApp extends JFrame {
    private FrequencyDetector detector;
    private FrequencyUI frequencyUI;
    private JPanel controlPanel;
    private JButton startButton;
    private JButton stopButton;
    private JComboBox<String> frequencySelector;
    private JComboBox<String> waveformSelector;
    private JSlider volumeSlider;
    private JLabel statusLabel;

    private AudioGenerator audioGenerator;
    private boolean isRunning = false;

    private static final int FFT_SIZE = 2048;
    private static final double SAMPLE_RATE = 44100.0;

    // Predefined test frequencies
    private static final String[] TEST_FREQUENCIES = {
        "A4 - 440 Hz",
        "C4 - 261.6 Hz",
        "E4 - 329.6 Hz",
        "G4 - 392.0 Hz",
        "A5 - 880 Hz",
        "C3 - 130.8 Hz",
        "Custom Sweep"
    };

    private static final String[] WAVEFORMS = {
        "Sine",
        "Square",
        "Sawtooth",
        "Triangle"
    };

    public StandaloneApp() {
        super("DFilter Frequency Detector - Standalone");

        // Initialize detector
        detector = new FrequencyDetector(FFT_SIZE, SAMPLE_RATE);

        // Setup UI
        setupUI();

        // Window settings
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        pack();
        setLocationRelativeTo(null);
        setResizable(false);
    }

    private void setupUI() {
        setLayout(new BorderLayout(10, 10));

        // Frequency display panel
        frequencyUI = new FrequencyUI();
        add(frequencyUI, BorderLayout.CENTER);

        // Control panel
        controlPanel = new JPanel();
        controlPanel.setLayout(new BoxLayout(controlPanel, BoxLayout.Y_AXIS));
        controlPanel.setBackground(new Color(30, 30, 35));
        controlPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Frequency selector
        JPanel freqPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        freqPanel.setBackground(new Color(30, 30, 35));
        freqPanel.add(new JLabel("Test Frequency:"));
        frequencySelector = new JComboBox<>(TEST_FREQUENCIES);
        freqPanel.add(frequencySelector);
        controlPanel.add(freqPanel);

        // Waveform selector
        JPanel wavePanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        wavePanel.setBackground(new Color(30, 30, 35));
        wavePanel.add(new JLabel("Waveform:"));
        waveformSelector = new JComboBox<>(WAVEFORMS);
        wavePanel.add(waveformSelector);
        controlPanel.add(wavePanel);

        // Volume slider
        JPanel volumePanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        volumePanel.setBackground(new Color(30, 30, 35));
        volumePanel.add(new JLabel("Volume:"));
        volumeSlider = new JSlider(0, 100, 30);
        volumeSlider.setPreferredSize(new Dimension(150, 30));
        volumePanel.add(volumeSlider);
        controlPanel.add(volumePanel);

        // Buttons
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
        buttonPanel.setBackground(new Color(30, 30, 35));

        startButton = new JButton("Start Audio");
        startButton.addActionListener(e -> startAudio());
        buttonPanel.add(startButton);

        stopButton = new JButton("Stop Audio");
        stopButton.setEnabled(false);
        stopButton.addActionListener(e -> stopAudio());
        buttonPanel.add(stopButton);

        controlPanel.add(buttonPanel);

        // Status label
        statusLabel = new JLabel("Ready");
        statusLabel.setForeground(Color.WHITE);
        statusLabel.setHorizontalAlignment(SwingConstants.CENTER);
        controlPanel.add(Box.createRigidArea(new Dimension(0, 10)));
        controlPanel.add(statusLabel);

        add(controlPanel, BorderLayout.SOUTH);

        // Style labels
        for (Component comp : controlPanel.getComponents()) {
            if (comp instanceof JPanel) {
                for (Component subComp : ((JPanel) comp).getComponents()) {
                    if (subComp instanceof JLabel) {
                        subComp.setForeground(Color.WHITE);
                    }
                }
            }
        }
    }

    private void startAudio() {
        if (isRunning) return;

        String selectedFreq = (String) frequencySelector.getSelectedItem();
        String selectedWaveform = (String) waveformSelector.getSelectedItem();
        double frequency = parseFrequency(selectedFreq);

        try {
            audioGenerator = new AudioGenerator(frequency, selectedWaveform, SAMPLE_RATE);
            audioGenerator.start();
            isRunning = true;

            startButton.setEnabled(false);
            stopButton.setEnabled(false);
            statusLabel.setText("Generating audio at " + frequency + " Hz...");

        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this,
                "Error starting audio: " + ex.getMessage(),
                "Audio Error",
                JOptionPane.ERROR_MESSAGE);
            statusLabel.setText("Error: " + ex.getMessage());
        }
    }

    private void stopAudio() {
        if (!isRunning) return;

        if (audioGenerator != null) {
            audioGenerator.stopAudio();
            try {
                audioGenerator.join(1000);
            } catch (InterruptedException e) {
                // Ignore
            }
            audioGenerator = null;
        }

        isRunning = false;
        startButton.setEnabled(true);
        stopButton.setEnabled(false);
        statusLabel.setText("Stopped");
        frequencyUI.reset();
    }

    private double parseFrequency(String selection) {
        if (selection.contains("440")) return 440.0;
        if (selection.contains("261.6")) return 261.6;
        if (selection.contains("329.6")) return 329.6;
        if (selection.contains("392.0")) return 392.0;
        if (selection.contains("880")) return 880.0;
        if (selection.contains("130.8")) return 130.8;
        return 440.0; // Default
    }

    /**
     * Inner class to generate audio and analyze it
     */
    private class AudioGenerator extends Thread {
        private double frequency;
        private String waveform;
        private double sampleRate;
        private SourceDataLine line;
        private volatile boolean running = true;

        public AudioGenerator(double freq, String wave, double rate) {
            this.frequency = freq;
            this.waveform = wave;
            this.sampleRate = rate;
        }

        @Override
        public void run() {
            try {
                // Setup audio output
                AudioFormat format = new AudioFormat((float) sampleRate, 16, 1, true, false);
                DataLine.Info info = new DataLine.Info(SourceDataLine.class, format);
                line = (SourceDataLine) AudioSystem.getLine(info);
                line.open(format);
                line.start();

                byte[] audioBuffer = new byte[FFT_SIZE * 2]; // 16-bit samples
                double[] analysisBuffer = new double[FFT_SIZE];
                int bufferIndex = 0;

                double phase = 0.0;
                double phaseIncrement = 2.0 * Math.PI * frequency / sampleRate;
                double volume = volumeSlider.getValue() / 100.0;

                while (running) {
                    // Generate audio samples
                    for (int i = 0; i < audioBuffer.length; i += 2) {
                        double sample = generateSample(phase) * volume * 0.5;

                        // Convert to 16-bit PCM
                        short pcmValue = (short) (sample * 32767);
                        audioBuffer[i] = (byte) (pcmValue & 0xFF);
                        audioBuffer[i + 1] = (byte) ((pcmValue >> 8) & 0xFF);

                        // Store for analysis
                        analysisBuffer[bufferIndex++] = sample;

                        if (bufferIndex >= FFT_SIZE) {
                            // Analyze
                            analyzeAndDisplay(analysisBuffer);
                            bufferIndex = 0;
                        }

                        phase += phaseIncrement;
                        if (phase > 2.0 * Math.PI) {
                            phase -= 2.0 * Math.PI;
                        }
                    }

                    // Play audio
                    line.write(audioBuffer, 0, audioBuffer.length);

                    // Update volume
                    volume = volumeSlider.getValue() / 100.0;
                }

                line.drain();
                line.close();

            } catch (Exception ex) {
                SwingUtilities.invokeLater(() -> {
                    statusLabel.setText("Error: " + ex.getMessage());
                });
            }
        }

        private double generateSample(double phase) {
            switch (waveform) {
                case "Sine":
                    return Math.sin(phase);
                case "Square":
                    return phase < Math.PI ? 1.0 : -1.0;
                case "Sawtooth":
                    return 2.0 * (phase / (2.0 * Math.PI)) - 1.0;
                case "Triangle":
                    double t = phase / (2.0 * Math.PI);
                    return t < 0.5 ? 4.0 * t - 1.0 : 3.0 - 4.0 * t;
                default:
                    return Math.sin(phase);
            }
        }

        private void analyzeAndDisplay(double[] samples) {
            detector.analyze(samples);
            double detectedFreq = detector.getDominantFrequency();
            double magnitude = detector.getDominantMagnitude();

            SwingUtilities.invokeLater(() -> {
                frequencyUI.updateFrequency(detectedFreq, magnitude);
                stopButton.setEnabled(true);
            });
        }

        public void stopAudio() {
            running = false;
        }
    }

    public static void main(String[] args) {
        // Set look and feel
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            // Use default look and feel
        }

        // Create and show application
        SwingUtilities.invokeLater(() -> {
            StandaloneApp app = new StandaloneApp();
            app.setVisible(true);
        });
    }
}
