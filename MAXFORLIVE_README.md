# DFilter Max for Live Frequency Detector Plugin

A minimalistic frequency detection plugin based on the DFilter digital signal processing library, compatible with Max for Live and runnable as a standalone application.

## Features

- **Real-time frequency detection** using FFT analysis (2048-point FFT by default)
- **Musical note detection** - converts detected frequency to nearest musical note (e.g., A4, C3)
- **Minimalistic UI** - clean, modern interface showing frequency, note, and magnitude
- **Dual-mode operation**:
  - Max for Live plugin (mxj object)
  - Standalone Java application with built-in test tone generator

## Project Structure

```
dfilter/
├── src/com/falstad/dfilter/
│   ├── client/
│   │   ├── FFT.java              # Fast Fourier Transform implementation
│   │   └── Complex.java          # Complex number operations
│   └── maxforlive/
│       ├── FrequencyDetector.java    # Core frequency detection engine
│       ├── FrequencyUI.java          # Minimalistic UI panel
│       ├── MaxFrequencyPlugin.java   # Max for Live integration (mxj)
│       └── StandaloneApp.java        # Standalone application
├── src/com/cycling74/max/
│   ├── MaxObject.java            # Max SDK stub (replace with actual SDK)
│   └── DataTypes.java            # Max SDK data types
└── build/
    ├── frequency-plugin-standalone.jar   # Standalone runnable JAR
    └── frequency-plugin-mxj.jar          # Max for Live plugin JAR
```

## Building

### Option 1: Using Maven (requires internet)
```bash
mvn clean package
```

### Option 2: Using javac directly
```bash
# Create build directory
mkdir -p build/classes

# Compile all sources
javac -d build/classes -sourcepath src \
    src/com/falstad/dfilter/client/FFT.java \
    src/com/falstad/dfilter/client/Complex.java \
    src/com/cycling74/max/*.java \
    src/com/falstad/dfilter/maxforlive/*.java

# Create standalone JAR
cd build/classes
jar cvfe ../frequency-plugin-standalone.jar \
    com.falstad.dfilter.maxforlive.StandaloneApp \
    com/falstad/dfilter/client/*.class \
    com/falstad/dfilter/maxforlive/*.class

# Create Max for Live JAR
jar cvf ../frequency-plugin-mxj.jar \
    com/cycling74/max/*.class \
    com/falstad/dfilter/client/FFT.class \
    com/falstad/dfilter/client/Complex.class \
    com/falstad/dfilter/maxforlive/FrequencyDetector.class \
    com/falstad/dfilter/maxforlive/FrequencyUI.class \
    com/falstad/dfilter/maxforlive/MaxFrequencyPlugin.class
```

## Usage

### Standalone Application

Run the standalone application with built-in test tone generator:

```bash
java -jar build/frequency-plugin-standalone.jar
```

**Features:**
- Select from predefined test frequencies (A4-440Hz, C4-261.6Hz, etc.)
- Choose waveform type (Sine, Square, Sawtooth, Triangle)
- Adjust volume with slider
- Real-time frequency display with note name
- Visual magnitude meter

### Max for Live Plugin

#### Installation:

1. **Replace Max SDK stub** (if not already done):
   - Locate your Max installation's Java SDK: `[Max]/Cycling '74/java/lib/max.jar`
   - Replace the stub files in `src/com/cycling74/max/` or add max.jar to classpath

2. **Compile with actual Max SDK**:
   ```bash
   javac -cp "/path/to/Max/java/lib/max.jar" -d build/classes -sourcepath src \
       src/com/falstad/dfilter/maxforlive/*.java

   jar cvf build/frequency-plugin-mxj.jar -C build/classes .
   ```

3. **Install in Max**:
   - Copy `frequency-plugin-mxj.jar` to `[Max]/Cycling '74/java/classes/`
   - Or place in your project folder and reference with full path

#### Usage in Max/MSP:

Create a Max patch with the mxj object:

```
[mxj com.falstad.dfilter.maxforlive.MaxFrequencyPlugin]
```

**Inlets:**
- **Inlet 0**: Audio signal (list of samples) or bang to trigger analysis
- **Inlet 1**: Control messages

**Outlets:**
- **Outlet 0**: Detected frequency (float, Hz)
- **Outlet 1**: Magnitude (float)
- **Outlet 2**: Note name (string, e.g., "A4")

**Messages:**
- `bang` - Trigger frequency analysis
- `list <samples>` - Send audio samples for analysis
- `samplerate <rate>` - Set sample rate (default: 44100)
- `fftsize <size>` - Set FFT size, must be power of 2 (default: 2048)
- `reset` - Reset the detector
- `showui` - Show frequency display window
- `hideui` - Hide frequency display window

#### Example Max Patch:

```
[adc~]
  |
[snapshot~ 2048]
  |
[mxj com.falstad.dfilter.maxforlive.MaxFrequencyPlugin]
  |    |    |
  |    |    [prepend set]
  |    |      |
  |    |    [message "Note: $1"]
  |    |
  |  [message "Magnitude: $1"]
  |
[number]
  |
[message "Frequency: $1 Hz"]
```

## Technical Details

### Frequency Detection Algorithm

1. **Windowing**: Applies Hamming window to reduce spectral leakage
2. **FFT**: Performs Fast Fourier Transform (2048-point default)
3. **Peak Detection**: Finds dominant frequency bin in magnitude spectrum
4. **Parabolic Interpolation**: Refines frequency estimate for sub-bin accuracy
5. **Note Conversion**: Maps frequency to nearest musical note using A4=440Hz reference

### Key Parameters

- **FFT Size**: 2048 samples (configurable, must be power of 2)
- **Sample Rate**: 44100 Hz (configurable)
- **Frequency Range**: 20 Hz - 20 kHz (audible range)
- **Frequency Resolution**: Sample Rate / FFT Size = ~21.5 Hz at 44100 Hz

### UI Design

- **Modern Dark Theme**: Dark background with cyan accents
- **Large Frequency Display**: 72pt bold font for easy reading
- **Musical Note**: Shows nearest note with octave (e.g., A4, C#3)
- **Magnitude Meter**: Visual representation of signal strength

## Dependencies

- **Java 8 or higher**
- **Swing** (included in Java)
- **Java Sound API** (included in Java)
- **Max SDK** (for Max for Live integration only)

## License

Based on DFilter by Paul Falstad, licensed under GNU GPL v2.

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

## Credits

- **Original DFilter**: Paul Falstad (http://www.falstad.com/dfilter/)
- **Max for Live Plugin**: Based on DFilter fork
- **FFT Implementation**: From DFilter codebase

## Troubleshooting

### Max for Live Issues

1. **Class not found error**: Ensure JAR is in Max's Java classpath
2. **Audio not processing**: Check that sample rate matches your Max audio settings
3. **No output**: Verify FFT buffer is filled before analysis (send list of 2048 samples)

### Standalone Issues

1. **No audio device found**: Check Java sound system configuration
2. **GUI not showing**: Ensure running in non-headless environment
3. **Inaccurate frequency**: Try larger FFT size for better resolution

## Future Enhancements

- Real-time audio input (microphone) in standalone mode
- Multiple frequency detection (polyphonic)
- Frequency tracking and history
- MIDI note output for Max for Live
- Tuner mode with cents deviation
- Spectrum analyzer view

## Contact

For issues or contributions, please refer to the main DFilter repository.
