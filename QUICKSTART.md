# Quick Start Guide - DFilter Frequency Detector Plugin

## 🚀 Run Standalone Application (No Max Required!)

The fastest way to try the frequency detector:

```bash
java -jar build/frequency-plugin-standalone.jar
```

### What You'll See:

A modern, dark-themed window with:
- **Large frequency display** in Hz
- **Musical note name** (e.g., A4, C#3)
- **Magnitude meter** showing signal strength
- **Control panel** with:
  - Frequency selector (A4-440Hz, C4-261.6Hz, etc.)
  - Waveform selector (Sine, Square, Sawtooth, Triangle)
  - Volume slider

### How to Use:

1. **Select a test frequency** from the dropdown (default: A4 - 440 Hz)
2. **Choose a waveform** (Sine is recommended for accurate detection)
3. **Click "Start Audio"** - you'll hear the test tone
4. **Watch the display** update with the detected frequency
5. **Experiment**:
   - Try different frequencies
   - Switch waveforms
   - Adjust volume
6. **Click "Stop Audio"** when done

### Expected Results:

- **A4 (440 Hz)**: Should detect ~440.0 Hz, display "A4"
- **C4 (261.6 Hz)**: Should detect ~261.6 Hz, display "C4"
- **Accuracy**: Typically within ±1-2 Hz for pure tones

---

## 🎛️ Use in Max for Live

### Prerequisites:
- Max/MSP or Ableton Live with Max for Live
- Java 8+ installed
- Compiled `frequency-plugin-mxj.jar`

### Installation:

1. **Locate your Max Java folder**:
   - Mac: `/Applications/Max.app/Contents/Resources/C74/packages/max-mxj/java/classes/`
   - Windows: `C:\Program Files\Cycling '74\Max\resources\packages\max-mxj\java\classes\`

2. **Copy the JAR file**:
   ```bash
   cp build/frequency-plugin-mxj.jar [Max Java Classes Folder]
   ```

3. **Open Max/MSP**

4. **Create a new patcher**

5. **Add the mxj object**:
   ```
   Type 'n' to create new object, then type:
   mxj com.falstad.dfilter.maxforlive.MaxFrequencyPlugin
   ```

### Simple Test Patch:

```
[cycle~ 440]  (generate 440 Hz tone)
    |
[snapshot~ 2048]  (capture 2048 samples)
    |
[button]  (click to analyze)
    |
[mxj com.falstad.dfilter.maxforlive.MaxFrequencyPlugin]
    |         |         |
    |         |         [message] (note name)
    |         |
    |         [number] (magnitude)
    |
[number] (frequency in Hz)
```

Or use the pre-made example patch:
```bash
examples/frequency-detector.maxpat
```

---

## 📦 Build from Source

### Quick Build:

```bash
# Compile
mkdir -p build/classes
javac -d build/classes -sourcepath src \
    src/com/falstad/dfilter/client/*.java \
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
    com/falstad/dfilter/maxforlive/*.class
cd ../..
```

---

## 🎯 Test Scenarios

### Test 1: Basic Frequency Detection (Standalone)
1. Run standalone app
2. Select "A4 - 440 Hz"
3. Select "Sine" waveform
4. Start audio
5. **Expected**: Display shows ~440.0 Hz, "A4"

### Test 2: Different Notes (Standalone)
1. Try each preset frequency:
   - C4 → ~261.6 Hz
   - E4 → ~329.6 Hz
   - G4 → ~392.0 Hz
   - A5 → ~880.0 Hz
2. **Expected**: Each shows correct frequency and note

### Test 3: Waveform Comparison (Standalone)
1. Select "A4 - 440 Hz"
2. Try each waveform:
   - Sine: Cleanest detection, single peak
   - Square: Detects fundamental + harmonics
   - Sawtooth: Multiple harmonics visible
   - Triangle: Similar to square but different harmonics
3. **Expected**: All detect ~440 Hz as dominant frequency

### Test 4: Max Integration
1. Open `examples/frequency-detector.maxpat`
2. Enable audio (click speaker icon)
3. Click button to analyze
4. **Expected**: Numbers appear showing ~440 Hz

---

## 🔧 Troubleshooting

### Standalone App Issues

**Problem**: "No audio device found"
- **Solution**: Check audio permissions, ensure audio device is available

**Problem**: Frequency detection is inaccurate
- **Solution**:
  - Use Sine waveform for testing
  - Increase volume
  - Wait for buffer to fill (takes ~50ms at 44100 Hz)

**Problem**: GUI doesn't appear
- **Solution**: Ensure running in graphical environment (not headless server)

### Max for Live Issues

**Problem**: "Class not found" error
- **Solution**:
  1. Verify JAR is in Max's Java classes folder
  2. Restart Max
  3. Check Java version (Java 8+ required)

**Problem**: No output from plugin
- **Solution**:
  1. Send enough samples (2048 for default FFT size)
  2. Use snapshot~ with size 2048
  3. Click button or send bang to trigger analysis

**Problem**: Inaccurate detection
- **Solution**:
  - Ensure sample rate matches Max's audio settings
  - Send message: `samplerate 44100` (or your rate)
  - Try larger FFT: `fftsize 4096`

---

## 📊 Technical Specs

- **Algorithm**: FFT with Hamming window + parabolic interpolation
- **Default FFT Size**: 2048 samples
- **Default Sample Rate**: 44100 Hz
- **Frequency Resolution**: ~21.5 Hz (44100 / 2048)
- **Frequency Range**: 20 Hz - 20 kHz
- **Detection Accuracy**: ±1-2 Hz for pure tones

---

## 🎨 UI Features

### Standalone Application UI:
- **Dark theme** - Easy on the eyes
- **Large font** - 72pt frequency display
- **Color coding**:
  - Cyan: Active signal detected
  - Gray: No signal / below threshold
- **Real-time updates** - ~20 updates per second
- **Magnitude meter** - Visual feedback of signal strength

---

## 💡 Tips

1. **For best accuracy**: Use sine waves and moderate volume
2. **For faster detection**: Reduce FFT size (trade-off: lower resolution)
3. **For better resolution**: Increase FFT size to 4096 or 8192
4. **Testing harmonics**: Use square or sawtooth waveforms
5. **In Max**: Use `[poly~]` for polyphonic analysis

---

## 📖 Next Steps

- Read full documentation: `MAXFORLIVE_README.md`
- Explore source code: `src/com/falstad/dfilter/maxforlive/`
- Modify UI colors: `FrequencyUI.java` lines 16-19
- Adjust FFT parameters: `FrequencyDetector.java`
- Create custom Max patches for your workflow

---

## 🐛 Found an Issue?

Report issues or contribute improvements to the project repository.

Enjoy detecting frequencies! 🎵
