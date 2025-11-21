package com.falstad.dfilter.maxforlive;

import javax.swing.*;
import java.awt.*;
import java.awt.geom.Rectangle2D;

/**
 * Minimalistic UI panel to display frequency information
 */
public class FrequencyUI extends JPanel {
    private double currentFrequency;
    private double currentMagnitude;
    private String noteString;
    private boolean isActive;

    // Color scheme
    private static final Color BG_COLOR = new Color(30, 30, 35);
    private static final Color TEXT_COLOR = new Color(220, 220, 220);
    private static final Color ACCENT_COLOR = new Color(0, 180, 255);
    private static final Color METER_BG = new Color(50, 50, 55);

    public FrequencyUI() {
        this.currentFrequency = 0.0;
        this.currentMagnitude = 0.0;
        this.noteString = "--";
        this.isActive = false;

        setPreferredSize(new Dimension(400, 300));
        setBackground(BG_COLOR);
    }

    /**
     * Update the displayed frequency
     */
    public void updateFrequency(double frequency, double magnitude) {
        this.currentFrequency = frequency;
        this.currentMagnitude = magnitude;
        this.isActive = magnitude > 0.1; // Threshold for active signal
        this.noteString = frequencyToNote(frequency);
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);

        int width = getWidth();
        int height = getHeight();

        // Draw title
        g2d.setColor(TEXT_COLOR);
        g2d.setFont(new Font("Sans-Serif", Font.BOLD, 16));
        String title = "FREQUENCY DETECTOR";
        FontMetrics fm = g2d.getFontMetrics();
        int titleWidth = fm.stringWidth(title);
        g2d.drawString(title, (width - titleWidth) / 2, 30);

        // Draw frequency display
        g2d.setFont(new Font("Sans-Serif", Font.BOLD, 72));
        String freqText = String.format("%.1f", currentFrequency);
        fm = g2d.getFontMetrics();
        int freqWidth = fm.stringWidth(freqText);

        if (isActive) {
            g2d.setColor(ACCENT_COLOR);
        } else {
            g2d.setColor(new Color(80, 80, 85));
        }
        g2d.drawString(freqText, (width - freqWidth) / 2, height / 2);

        // Draw Hz label
        g2d.setFont(new Font("Sans-Serif", Font.PLAIN, 24));
        g2d.setColor(TEXT_COLOR);
        String hzLabel = "Hz";
        fm = g2d.getFontMetrics();
        int hzWidth = fm.stringWidth(hzLabel);
        g2d.drawString(hzLabel, (width - hzWidth) / 2, height / 2 + 40);

        // Draw note name
        g2d.setFont(new Font("Sans-Serif", Font.BOLD, 36));
        fm = g2d.getFontMetrics();
        int noteWidth = fm.stringWidth(noteString);
        if (isActive) {
            g2d.setColor(ACCENT_COLOR);
        } else {
            g2d.setColor(new Color(80, 80, 85));
        }
        g2d.drawString(noteString, (width - noteWidth) / 2, height / 2 + 90);

        // Draw magnitude meter
        drawMagnitudeMeter(g2d, width, height);
    }

    /**
     * Draw a simple magnitude meter
     */
    private void drawMagnitudeMeter(Graphics2D g2d, int width, int height) {
        int meterWidth = width - 100;
        int meterHeight = 20;
        int meterX = 50;
        int meterY = height - 60;

        // Background
        g2d.setColor(METER_BG);
        g2d.fillRoundRect(meterX, meterY, meterWidth, meterHeight, 10, 10);

        // Active level
        double normalizedMag = Math.min(1.0, currentMagnitude / 1000.0); // Normalize
        int activeWidth = (int) (meterWidth * normalizedMag);

        if (activeWidth > 0) {
            g2d.setColor(ACCENT_COLOR);
            g2d.fillRoundRect(meterX, meterY, activeWidth, meterHeight, 10, 10);
        }

        // Label
        g2d.setColor(TEXT_COLOR);
        g2d.setFont(new Font("Sans-Serif", Font.PLAIN, 12));
        g2d.drawString("MAGNITUDE", meterX, meterY - 5);
    }

    /**
     * Convert frequency to nearest musical note
     */
    private String frequencyToNote(double frequency) {
        if (frequency < 20 || frequency > 20000) {
            return "--";
        }

        String[] noteNames = {"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"};

        // Calculate semitones from A4 (440 Hz)
        double a4 = 440.0;
        double semitones = 12 * (Math.log(frequency / a4) / Math.log(2));
        int semitonesRounded = (int) Math.round(semitones);

        // Calculate octave and note
        int noteIndex = (semitonesRounded + 9) % 12;
        if (noteIndex < 0) noteIndex += 12;

        int octave = 4 + (semitonesRounded + 9) / 12;

        return noteNames[noteIndex] + octave;
    }

    /**
     * Reset the display
     */
    public void reset() {
        this.currentFrequency = 0.0;
        this.currentMagnitude = 0.0;
        this.noteString = "--";
        this.isActive = false;
        repaint();
    }
}
