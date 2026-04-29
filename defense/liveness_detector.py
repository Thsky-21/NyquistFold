"""
ghostcommands/defense/liveness_detector.py
============================================
CONCEPT: Detect whether an incoming audio signal is genuine human speech
or an adversarial aliased injection — the "antivirus" layer of this repo.

KEY INSIGHT (your technical moat):
  Real human speech has a rich HARMONIC SERIES. When you say "A" at 440 Hz,
  you simultaneously produce energy at 880 Hz, 1320 Hz, 1760 Hz... (integer multiples).
  
  An aliased ultrasonic tone is a pure sine wave — it has NO harmonics.
  This absence of harmonics is the fingerprint of an adversarial signal.

SECONDARY INSIGHT:
  Real speech also has formants — resonance peaks that move continuously over time.
  A DolphinAttack signal is stationary — the frequencies don't change.
  Temporal variance analysis can catch this.

This module is the "defense" layer. In Thskyshield terms: the kill-switch
for the audio input channel before the voice command reaches the LLM.

YOUR TASK: Fill in the TODOs. This is the highest-value module in the repo.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional
from analyze.fft_analyzer import AudioFrame, SpectralAnalysis, analyze_spectrum


# ── Detection Output ───────────────────────────────────────────────────────────

@dataclass
class LivenessReport:
    """
    Output of the liveness detection pipeline.
    In Thskyshield integration: this maps to a governance decision (allow/block).
    """
    is_genuine_speech: bool           # Final verdict
    confidence: float                 # 0.0 (certain fake) → 1.0 (certain genuine)
    
    # Individual test scores (0.0 = failed, 1.0 = passed)
    harmonic_score: float             # Does the signal have harmonic structure?
    temporal_variance_score: float    # Does the signal change over time like speech?
    formant_score: float              # Are speech formants (F1/F2/F3) present?
    
    # Evidence
    dominant_freq_hz: float           # Peak frequency detected
    harmonic_series: list             # Detected harmonics (empty = likely alias)
    flags: list = field(default_factory=list)  # Human-readable warnings


# ── Test 1: Harmonic Structure ─────────────────────────────────────────────────

def check_harmonic_structure(analysis: SpectralAnalysis, 
                              tolerance_hz: float = 30.0) -> tuple[float, list]:
    """
    Test whether the signal's spectral peaks form a harmonic series.
    
    Algorithm:
      1. Find the fundamental frequency (f0) — the lowest significant peak
      2. Check for energy at 2*f0, 3*f0, 4*f0, ... up to Nyquist
      3. Score = (harmonics_found) / (harmonics_expected)
    
    Example:
      Real speech at f0=200Hz → expect peaks at 400, 600, 800, 1000, 1200...
      Aliased tone at 4000Hz → isolated peak, no harmonics → score ≈ 0.0
    
    TODO: Implement this.
    Hint: 
      - Find peaks using: peak_indices = np.where(magnitudes_db > -40)[0]
      - For each candidate f0, check how many of its harmonics are present
      - Return the (score, list_of_detected_harmonics) for the best candidate f0
      
    tolerance_hz: how close a peak must be to the expected harmonic to count
    """
    harmonics_found = []
    score = 0.0
    
    # TODO: Find fundamental frequency candidate
    # TODO: Walk up harmonic series: 2*f0, 3*f0, ...
    # TODO: At each step, check if a peak exists within ±tolerance_hz
    # TODO: Compute score as ratio of found/expected harmonics
    
    return score, harmonics_found


# ── Test 2: Temporal Variance ──────────────────────────────────────────────────

def check_temporal_variance(frame: AudioFrame, 
                             window_ms: int = 25, 
                             hop_ms: int = 10) -> float:
    """
    Test whether the signal's frequency content changes over time.
    
    Real speech is highly non-stationary — phonemes change every ~50–100ms.
    An aliased injection is a modulated sine wave — very stationary.
    
    Algorithm:
      1. Divide the signal into short overlapping frames
      2. Compute the dominant frequency in each frame
      3. Compute the variance of these dominant frequencies across time
      4. High variance → speech-like. Low variance → synthetic/aliased.
    
    TODO: Implement this.
    
    Returns: score in [0.0, 1.0] — higher means more speech-like temporal variation
    """
    window_samples = int(frame.sample_rate * window_ms / 1000)
    hop_samples    = int(frame.sample_rate * hop_ms / 1000)
    
    dominant_freqs_over_time = []
    
    # TODO: Slide a window across the signal
    # TODO: For each window, compute FFT, find dominant frequency
    # TODO: Append to dominant_freqs_over_time
    # TODO: Return normalized variance (scale to [0, 1])
    
    return 0.0  # placeholder


# ── Test 3: Formant Detection ──────────────────────────────────────────────────

def check_formants_present(analysis: SpectralAnalysis) -> float:
    """
    Test whether speech formants (F1, F2, F3) are present.
    
    Human vocal tract resonances create spectral peaks called formants:
      F1: 300–1000 Hz   (jaw/tongue height)
      F2: 900–2500 Hz   (tongue frontness)
      F3: 2000–3500 Hz  (lip rounding / identity)
    
    An aliased command typically has energy in only ONE narrow frequency band,
    not the distributed formant structure of real speech.
    
    TODO: Implement this.
    Check if there is significant energy in at least 2 of the 3 formant regions.
    
    Returns: score in [0.0, 1.0] — 1.0 means all three formant bands have energy
    """
    FORMANT_RANGES = [
        (300,  1000),   # F1
        (900,  2500),   # F2
        (2000, 3500),   # F3
    ]
    formants_detected = 0
    
    # TODO: For each formant range, check if the max magnitude exceeds a threshold
    # Hint: mask = (freqs >= low) & (freqs <= high)
    #        band_max_db = np.max(magnitudes_db[mask])
    
    return formants_detected / len(FORMANT_RANGES)


# ── Composite Liveness Scorer ──────────────────────────────────────────────────

def compute_liveness(frame: AudioFrame) -> LivenessReport:
    """
    Run all three tests and produce a final verdict.
    
    Weighting (tunable — this is your hyperparameter space):
      - Harmonic structure  : 50%  (strongest signal for alias detection)
      - Temporal variance   : 30%  (second most reliable)
      - Formant presence    : 20%  (useful but can false-positive on music/noise)
    
    Decision threshold: confidence > 0.6 → genuine speech
    
    TODO: Call the three check_* functions, compute weighted score, populate LivenessReport.
    """
    WEIGHTS = {
        "harmonic":  0.50,
        "temporal":  0.30,
        "formant":   0.20,
    }
    THRESHOLD = 0.60

    analysis = analyze_spectrum(frame)

    # TODO: Call check_harmonic_structure(analysis) → (harmonic_score, harmonics)
    # TODO: Call check_temporal_variance(frame) → temporal_score
    # TODO: Call check_formants_present(analysis) → formant_score
    
    harmonic_score   = 0.0  # replace
    harmonics        = []   # replace
    temporal_score   = 0.0  # replace
    formant_score    = 0.0  # replace

    # Weighted composite
    confidence = (
        WEIGHTS["harmonic"] * harmonic_score +
        WEIGHTS["temporal"] * temporal_score +
        WEIGHTS["formant"]  * formant_score
    )

    flags = []
    if harmonic_score < 0.3:
        flags.append("WARN: No harmonic series detected — possible aliased injection")
    if temporal_score < 0.2:
        flags.append("WARN: Signal is stationary — possible synthetic source")
    if formant_score < 0.5:
        flags.append("WARN: Speech formants absent")

    return LivenessReport(
        is_genuine_speech        = confidence >= THRESHOLD,
        confidence               = round(confidence, 3),
        harmonic_score           = round(harmonic_score, 3),
        temporal_variance_score  = round(temporal_score, 3),
        formant_score            = round(formant_score, 3),
        dominant_freq_hz         = analysis.peak_freq_hz,
        harmonic_series          = harmonics,
        flags                    = flags,
    )


# ── Thskyshield Integration Interface ─────────────────────────────────────────
# Future: wrap this as a FastAPI endpoint and register as a Thskyshield "compute hook"
# The governance layer calls check_audio() BEFORE forwarding audio to the LLM API.
# If blocked, it increments the budget counter and logs the adversarial event.

def check_audio(raw_pcm: bytes, sample_rate: int) -> dict:
    """
    Thskyshield-compatible interface.
    Input : raw PCM bytes from the voice pipeline
    Output: governance decision dict
    
    TODO: Convert raw_pcm bytes → AudioFrame → compute_liveness() → format response.
    
    Response schema (mirrors Thskyshield's existing governance log format):
    {
        "allowed": bool,
        "reason": str,
        "confidence": float,
        "flags": list[str],
        "request_id": str   # generate with uuid4
    }
    """
    import uuid
    
    # TODO: Convert bytes → numpy array → AudioFrame
    # TODO: Call compute_liveness()
    # TODO: Return governance decision dict
    
    return {
        "allowed":    True,   # placeholder
        "reason":     "TODO: Implement check_audio()",
        "confidence": 0.0,
        "flags":      [],
        "request_id": str(uuid.uuid4()),
    }


# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("[*] GhostCommands — Liveness Detector")
    print()
    print("    This module scores an audio signal across 3 axes:")
    print("    1. Harmonic structure   (real speech has overtones; aliases don't)")
    print("    2. Temporal variance    (real speech changes; sine waves don't)")
    print("    3. Formant presence     (F1/F2/F3 are the fingerprint of the vocal tract)")
    print()
    print("    Final output → LivenessReport (governance decision for Thskyshield)")
    print()
    print("    [!] Implement the TODOs and run: python -m defense.liveness_detector")