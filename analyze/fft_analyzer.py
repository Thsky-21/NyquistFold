"""
ghostcommands/analyze/fft_analyzer.py
========================================
CONCEPT: Use the Fast Fourier Transform (FFT) to reveal hidden frequencies
in a recorded audio sample — the "forensic" tool of this repo.

In a DolphinAttack scenario:
  - Human ear hears: silence
  - Spectrogram shows: ultrasonic energy spike at carrier frequency
  - After ADC aliasing: ghost frequency appears in speech range

This module handles real .wav file input so you can test against actual recordings.

YOUR TASK: Fill in the TODOs. This module is the "evidence collector" of the repo.
"""

import numpy as np
import wave
import struct
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from dataclasses import dataclass
from typing import Optional


# ── Data Structures ────────────────────────────────────────────────────────────

@dataclass
class AudioFrame:
    """Holds a raw audio recording and its metadata."""
    samples: np.ndarray          # Raw PCM samples as float32, normalized to [-1, 1]
    sample_rate: int             # Hz
    duration_sec: float          # Total length
    num_channels: int            # 1 = mono, 2 = stereo
    source_path: Optional[str]   # File path or None if synthetic


@dataclass
class SpectralAnalysis:
    """Output of the FFT analysis pipeline."""
    freqs_hz: np.ndarray        # Frequency axis (Hz)
    magnitudes_db: np.ndarray   # Magnitude in dB (log scale — better for detecting weak aliases)
    peak_freq_hz: float         # Dominant frequency detected
    alias_candidates: list      # Frequencies flagged as potential aliases
    nyquist_hz: float           # f_s / 2 for this recording


# ── WAV File I/O ───────────────────────────────────────────────────────────────

def load_wav(filepath: str) -> AudioFrame:
    """
    Load a .wav file and return normalized float samples.
    
    TODO: Implement using Python's built-in `wave` module (no scipy needed).
    Steps:
      1. Open file with wave.open()
      2. Read metadata: framerate, nchannels, sampwidth, nframes
      3. Read raw bytes with wav.readframes(nframes)
      4. Unpack bytes to integers using struct.unpack
      5. Normalize to float32 in range [-1.0, 1.0]
      
    Hint for unpacking: fmt = f"<{nframes * nchannels}h"  (little-endian 16-bit signed int)
    Hint for normalization: samples / 32768.0
    """
    # TODO: Implement WAV loading
    raise NotImplementedError("Implement load_wav()")


def save_wav(filepath: str, samples: np.ndarray, sample_rate: int) -> None:
    """
    Save float32 samples to a .wav file.
    
    TODO: Implement the inverse of load_wav().
    Steps:
      1. Convert float32 back to int16: (samples * 32767).astype(np.int16)
      2. Pack to bytes with struct.pack
      3. Write with wave.open() in 'wb' mode
    """
    # TODO: Implement WAV saving
    raise NotImplementedError("Implement save_wav()")


# ── Spectral Analysis Pipeline ─────────────────────────────────────────────────

def analyze_spectrum(frame: AudioFrame, window: str = "hann") -> SpectralAnalysis:
    """
    Core FFT analysis. Uses a windowing function to reduce spectral leakage.
    
    WHY WINDOWING? A raw FFT assumes the signal is periodic within the window.
    If it isn't, you get "spectral leakage" — energy smears across nearby bins,
    making it hard to detect low-amplitude alias frequencies. A Hann window fixes this.
    
    TODO: Implement the full pipeline:
      1. Apply window: windowed = samples * np.hanning(len(samples))
      2. Compute FFT: use np.fft.rfft (real-input FFT, output is single-sided)
      3. Convert to dB scale: mags_db = 20 * np.log10(np.abs(fft_result) / len(samples) + 1e-10)
         (the +1e-10 prevents log(0))
      4. Compute frequency axis: freqs = np.fft.rfftfreq(len(samples), d=1/sample_rate)
      5. Find peak: freqs[np.argmax(mags_db)]
      6. Detect alias candidates (see detect_aliases() below)
    """
    # TODO: Implement and return a SpectralAnalysis dataclass
    raise NotImplementedError("Implement analyze_spectrum()")


def detect_aliases(freqs_hz: np.ndarray, mags_db: np.ndarray, sample_rate: int,
                   threshold_db: float = -40.0) -> list:
    """
    Flag frequencies that are likely aliases rather than genuine signal components.
    
    DETECTION LOGIC:
    An aliased frequency f_alias = |f_source - n * f_s| for some integer n.
    
    Heuristic: if a peak appears at f_alias, and:
      - There is NO corresponding energy at (f_s - f_alias) in the recording
        (because the original ultrasonic source was filtered by hardware)
      - The peak is isolated (no harmonic series around it)
    ...then it is likely an alias, not a real voice component.
    
    TODO: Implement this detection logic.
    This is the core "liveness detection" idea — real speech has harmonics,
    aliased tones are usually pure sinusoids with no overtone structure.
    
    Returns: list of {"freq_hz": float, "mag_db": float, "reason": str}
    """
    alias_candidates = []
    nyquist = sample_rate / 2

    # TODO: Find all spectral peaks above threshold_db
    # TODO: For each peak, check if it looks like an isolated tone (alias signature)
    # TODO: Check if folded counterpart (sample_rate - freq) also has energy

    return alias_candidates


# ── Spectrogram Visualization ──────────────────────────────────────────────────

def plot_spectrogram(frame: AudioFrame, highlight_aliases: bool = True) -> None:
    """
    Plot a Short-Time Fourier Transform (STFT) spectrogram.
    
    Unlike a single FFT, a spectrogram shows how frequency content changes over TIME.
    This is how you'd catch a DolphinAttack in a recording — you'd see the ultrasonic
    burst appear at a specific timestamp.
    
    TODO: Implement using matplotlib.pyplot.specgram() OR compute STFT manually:
      - Divide signal into overlapping frames (e.g., 25ms window, 10ms hop)
      - Apply window to each frame
      - Compute FFT of each frame
      - Stack magnitude columns → 2D array → imshow()
    
    If highlight_aliases=True, draw a red horizontal line at f_s/2 (Nyquist limit)
    and annotate any frequencies flagged by detect_aliases().
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_title("Spectrogram — GhostCommands Analysis")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")

    # TODO: Compute and plot spectrogram
    # TODO: If highlight_aliases, add annotation overlays

    nyquist = frame.sample_rate / 2
    ax.axhline(y=nyquist, color="red", linestyle="--", label=f"Nyquist limit ({nyquist/1000:.1f} kHz)")
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_fft_comparison(clean: AudioFrame, attacked: AudioFrame) -> None:
    """
    Side-by-side FFT: clean recording vs attacked recording.
    
    This is your key "before/after" visualization for the repo README.
    The attacked recording should show the ghost alias frequency that
    the clean recording does NOT have.
    
    TODO: Call analyze_spectrum() on both, then plot their magnitude spectra
    on the same axes. Mark the alias frequency with a vertical line.
    """
    # TODO: Implement
    raise NotImplementedError("Implement plot_fft_comparison()")


# ── Synthetic Test Data Generator ─────────────────────────────────────────────

def generate_synthetic_attack_wav(output_path: str, sample_rate: int = 16_000) -> AudioFrame:
    """
    Create a synthetic .wav file that simulates what the AI's ADC records
    during a DolphinAttack — without needing real hardware.
    
    Signal model:
      - 20 kHz AM-modulated carrier → aliases to 4 kHz after 16 kHz sampling
      - Mix with low-level white noise (realistic ADC noise floor ~-60 dB)
    
    TODO: Implement using aliasing_demo.generate_attack_signal()
    Then add noise: signal + 0.005 * np.random.randn(len(signal))
    Then save with save_wav() and return an AudioFrame.
    """
    # TODO: Implement
    raise NotImplementedError("Implement generate_synthetic_attack_wav()")


# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("[*] GhostCommands — FFT Analyzer")
    print("    Generating synthetic attack recording...")

    # TODO: Call generate_synthetic_attack_wav(), then analyze_spectrum(), then plot_spectrogram()
    print("    [!] Implement the TODOs above and run again.")