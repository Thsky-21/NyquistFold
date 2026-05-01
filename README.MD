#  NyquistFold 
### DSP Aliasing Vulnerability Research — Audio Adversarial ML

> *"The AI couldn't hear the attack. Neither could you."*

A research repo demonstrating how the **Nyquist-Shannon Sampling Theorem** can be weaponized to inject inaudible commands into voice-driven AI systems — and how to detect and block them.

---

## The Core Idea

```
Attacker sends:   20,000 Hz  (ultrasonic — completely silent to humans)
AI's ADC samples: 16,000 Hz  (standard voice recording rate)
What the AI hears: |20,000 - 16,000| = 4,000 Hz ← "ghost" frequency
```

This is **aliasing** — a mathematical artifact of sampling theory turned into an attack vector.

Real-world name: **DolphinAttack** (Zhejiang University, ACM CCS 2017 Best Paper).  
Real-world targets: Siri, Google Assistant, Alexa, Cortana — all confirmed vulnerable.

---

## Repo Structure

```
NyquistFold/
├── simulate/
│   └── aliasing_demo.py      # Math layer — prove aliasing happens in software
├── analyze/
│   └── fft_analyzer.py       # Forensics layer — detect ghost frequencies in recordings
├── defense/
│   └── liveness_detector.py  # Defense layer — block aliased commands before they reach the LLM
├── tests/
│   └── test_pipeline.py      # Test suite — 5 levels from unit math to full E2E
├── assets/                   # Generated plots go here
└── requirements.txt
```

---

## Learning Path (Implement in This Order)

### Stage 1 — The Math `simulate/aliasing_demo.py`
1. `generate_clean_signal()` — basic sine wave generation
2. `compute_fft()` — frequency domain transform
3. `downsample_signal()` — simulate the ADC
4. `generate_attack_signal()` — AM modulation
5. `plot_aliasing_effect()` — visualize the "fold"

**Checkpoint:** Run `python simulate/aliasing_demo.py` and see the ghost frequency appear in the FFT plot.

---

### Stage 2 — The Forensics `analyze/fft_analyzer.py`
1. `load_wav()` / `save_wav()` — real audio file I/O (no scipy — learn the raw bytes)
2. `analyze_spectrum()` — windowed FFT with Hann window
3. `detect_aliases()` — flag frequencies that lack harmonic context
4. `plot_spectrogram()` — STFT for time-frequency visualization

**Checkpoint:** Load a real `.wav` file and show its spectrum. Inject a known alias and verify detection.

---

### Stage 3 — The Defense `defense/liveness_detector.py`
1. `check_harmonic_structure()` — does the signal have overtones?
2. `check_temporal_variance()` — does the signal change over time like speech?
3. `check_formants_present()` — are vocal tract resonances present?
4. `compute_liveness()` — weighted composite scorer
5. `check_audio()` — Thskyshield integration interface

**Checkpoint:** Run all tests in `tests/test_pipeline.py`. The key test: `test_aliased_signal_fails_liveness()`.

---

## Key DSP Concepts Referenced

| Concept | Where it appears |
|---|---|
| Nyquist-Shannon Theorem | `aliasing_demo.py` constants |
| Aliasing / Spectral Folding | `generate_attack_signal()`, `downsample_signal()` |
| FFT / RFFT | `compute_fft()`, `analyze_spectrum()` |
| Windowing (Hann) | `analyze_spectrum()` |
| STFT / Spectrogram | `plot_spectrogram()` |
| AM Modulation | `generate_attack_signal()` |
| Harmonic Series | `check_harmonic_structure()` |
| Speech Formants (F1/F2/F3) | `check_formants_present()` |
| Temporal Non-stationarity | `check_temporal_variance()` |

---

## Future Integration — Thskyshield

`defense/liveness_detector.py` exposes a `check_audio()` function with a governance decision schema compatible with Thskyshield's compute log format.

Planned integration:
```
Voice Input → check_audio() → [BLOCK if aliased] → LLM API call
                ↓
         Thskyshield budget logger
```

This makes GhostCommands the **audio input governance layer** — sitting upstream of the financial kill-switch.

---

## References

- [DolphinAttack (2017)](https://dl.acm.org/doi/10.1145/3133956.3134052) — Zhejiang University, ACM CCS Best Paper
- [Nyquist-Shannon Sampling Theorem](https://en.wikipedia.org/wiki/Nyquist–Shannon_sampling_theorem)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- EU Cyber Resilience Act (enforcement Sept 2026)

---

## Requirements

```
numpy
matplotlib
pytest
```

Install: `pip install -r requirements.txt`  
Run tests: `pytest tests/ -v`

---

*Built as a learning project for adversarial ML + DSP security research.*  
*Future: integrate as an audio governance layer in [Thskyshield](https://thskyshield.com).*
