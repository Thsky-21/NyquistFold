"""
NyquistFold/tests/test_pipeline.py
======================================
End-to-end test: generate a synthetic attack → analyze → run liveness detection.

Tests are ordered from simplest (math) to most complex (full pipeline).
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from simulate.aliasing_demo import (
    generate_clean_signal, generate_attack_signal,
    downsample_signal, compute_fft, T, SAMPLE_RATE_HZ, F_ALIAS_HZ
)
from analyze.fft_analyzer import (
    AudioFrame, analyze_spectrum, detect_aliases, generate_synthetic_attack_wav
)
from defense.liveness_detector import (
    compute_liveness, check_harmonic_structure, check_temporal_variance
)


# ── Level 1: Unit Tests — Pure Math ───────────────────────────────────────────

def test_generate_clean_signal_shape():
    """Signal length must match time array."""
    sig = generate_clean_signal(1000, T)
    assert len(sig) == len(T), "Signal length mismatch"

def test_generate_clean_signal_is_sine():
    """Peak frequency of FFT must match input frequency."""
    freq = 1000
    sig = generate_clean_signal(freq, T)
    freqs, mags = compute_fft(sig, SAMPLE_RATE_HZ)
    peak = freqs[np.argmax(mags)]
    assert abs(peak - freq) < 50, f"Expected peak near {freq}Hz, got {peak}Hz"

def test_clean_signal_is_bounded():
    """Pure sine should stay within [-1, 1]."""
    sig = generate_clean_signal(440, T)
    assert np.all(np.abs(sig) <= 1.01), "Signal amplitude out of expected range"


# ── Level 2: Unit Tests — Aliasing Math ───────────────────────────────────────

def test_aliasing_occurs():
    """
    Core theorem test: a 20kHz signal sampled at 16kHz must produce a 4kHz alias.
    
    TODO: After implementing downsample_signal and compute_fft:
      1. Generate attack signal at 20kHz
      2. Downsample to SAMPLE_RATE_HZ
      3. Compute FFT
      4. Assert that the peak is near F_ALIAS_HZ (4kHz), NOT near 20kHz
    """
    # TODO: Implement this test
    pass

def test_no_alias_below_nyquist():
    """
    A 1kHz signal sampled at 16kHz should NOT alias — it's below Nyquist.
    FFT peak should remain at 1kHz.
    """
    # TODO: Implement this test
    pass


# ── Level 3: Integration Tests — Analysis Pipeline ────────────────────────────

def test_analyze_spectrum_returns_correct_shape():
    """FFT output shape must match expected for given signal length."""
    samples = np.sin(2 * np.pi * 440 * T).astype(np.float32)
    frame = AudioFrame(samples=samples, sample_rate=SAMPLE_RATE_HZ,
                       duration_sec=len(T)/SAMPLE_RATE_HZ, num_channels=1, source_path=None)
    result = analyze_spectrum(frame)
    assert len(result.freqs_hz) == len(result.magnitudes_db)
    assert result.nyquist_hz == SAMPLE_RATE_HZ / 2

def test_detect_aliases_flags_known_alias():
    """
    Synthetic aliased signal at 4kHz should be flagged as alias candidate.
    TODO: Implement after detect_aliases() is implemented.
    """
    pass


# ── Level 4: Integration Tests — Defense Layer ────────────────────────────────

def test_genuine_speech_passes_liveness():
    """
    Synthetic speech-like signal (has harmonics at 200, 400, 600... Hz)
    must score above threshold in liveness detection.
    
    TODO: Build a synthetic "speech" signal as sum of harmonics, run compute_liveness().
    """
    pass

def test_aliased_signal_fails_liveness():
    """
    Pure sine wave at 4kHz (alias signature: no harmonics, stationary)
    must be flagged as NOT genuine speech.
    
    TODO: Build a pure 4kHz sine signal, run compute_liveness(), assert is_genuine_speech=False.
    This is the KEY test that validates the defense module works.
    """
    pass

def test_harmonic_score_pure_sine_is_low():
    """
    A pure sine wave has only one spectral peak — harmonic score should be near 0.
    """
    # TODO: Implement
    pass

def test_harmonic_score_speech_signal_is_high():
    """
    A signal with harmonics at f0, 2*f0, 3*f0, 4*f0, 5*f0 should score near 1.0.
    """
    # TODO: Implement
    pass


# ── Level 5: End-to-End Pipeline Test ─────────────────────────────────────────

def test_full_pipeline():
    """
    Full pipeline: generate attack → analyze → detect.
    Confirms the whole system works together.
    
    TODO:
      1. Call generate_synthetic_attack_wav() to create test data
      2. Run analyze_spectrum()
      3. Run compute_liveness()
      4. Assert is_genuine_speech == False (attack should be detected)
      5. Assert at least one flag is set
    """
    pass


if __name__ == "__main__":
    print("[*] Running basic sanity checks (before pytest)...")
    print("    Run: pip install pytest && pytest tests/ -v")
    print()
    
    # Quick smoke test
    try:
        sig = generate_clean_signal(1000, T)
        print(f"    [OK] generate_clean_signal returned array of shape {sig.shape}")
    except NotImplementedError:
        print("    [--] generate_clean_signal not yet implemented")
    
    try:
        freqs, mags = compute_fft(sig, SAMPLE_RATE_HZ)
        print(f"    [OK] compute_fft returned {len(freqs)} frequency bins")
    except (NotImplementedError, UnboundLocalError):
        print("    [--] compute_fft not yet implemented")