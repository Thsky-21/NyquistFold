"""
ghostcommands/simulate/aliasing_demo.py
========================================
CONCEPT: Demonstrate the Nyquist-Shannon Sampling Theorem breaking down.

When an attacker sends a signal at frequency f_attack > f_s/2 (Nyquist limit),
the ADC cannot distinguish it from a lower "alias" frequency:

    f_alias = |f_attack - f_s|

This alias falls into the audible/processable range of the AI's speech engine.

YOUR TASK: Fill in the TODOs below. Run this script to see aliasing visually.
"""

import numpy as np
import matplotlib.pyplot as plt

# ── Constants ──────────────────────────────────────────────────────────────────
SAMPLE_RATE_HZ   = 16_000   # Typical voice AI sample rate (16 kHz)
NYQUIST_HZ       = SAMPLE_RATE_HZ / 2   # 8 kHz — highest frequency we can cleanly represent
DURATION_SEC     = 0.05     # 50ms signal window — enough to see the pattern
T                = np.linspace(0, DURATION_SEC, int(SAMPLE_RATE_HZ * DURATION_SEC), endpoint=False)

# ── Attack Signal Parameters ───────────────────────────────────────────────────
F_ATTACK_HZ  = 20_000   # Attacker's ultrasonic carrier (20 kHz — inaudible to humans)
F_PAYLOAD_HZ = 1_000    # The "hidden" command frequency we want to inject (1 kHz — audible to AI)
F_ALIAS_HZ   = abs(F_ATTACK_HZ - SAMPLE_RATE_HZ)  # = 4000 Hz — what the AI actually "hears"

print(f"[+] Attack frequency  : {F_ATTACK_HZ / 1000:.1f} kHz  (inaudible to humans)")
print(f"[+] Nyquist limit     : {NYQUIST_HZ / 1000:.1f} kHz")
print(f"[+] Expected alias    : {F_ALIAS_HZ / 1000:.1f} kHz  (AI hears THIS)")


# ── Part 1: Generate Signals ───────────────────────────────────────────────────

def generate_clean_signal(freq_hz: float, t: np.ndarray) -> np.ndarray:
    """
    Generate a pure sine wave at the given frequency.

    Formula: x(t) = A * sin(2 * pi * f * t)
    
    TODO: Implement this. Use numpy's sin function.
    Hint: np.sin(2 * np.pi * freq_hz * t)
    """
    # TODO: return the sine wave
    raise NotImplementedError("Implement generate_clean_signal()")


def generate_attack_signal(carrier_hz: float, payload_hz: float, t: np.ndarray) -> np.ndarray:
    """
    Generate an AM (Amplitude Modulated) ultrasonic attack signal.
    
    In DolphinAttack, the voice command is modulated onto an ultrasonic carrier.
    The microphone's non-linearity demodulates it back into audible range.
    
    Formula: x(t) = [1 + m * sin(2π * f_payload * t)] * sin(2π * f_carrier * t)
    where m = modulation index (0 to 1)
    
    TODO: Implement AM modulation.
    Hint: carrier * (1 + modulation_depth * payload)
    """
    modulation_depth = 0.8
    # TODO: return the AM-modulated signal
    raise NotImplementedError("Implement generate_attack_signal()")


def downsample_signal(signal: np.ndarray, original_rate: int, target_rate: int) -> np.ndarray:
    """
    Simulate the ADC sampling at a lower rate (the 'victim' device's microphone).
    This is where aliasing actually occurs — no anti-aliasing filter applied.
    
    TODO: Implement naive downsampling (just take every Nth sample).
    Hint: decimation_factor = original_rate // target_rate
          return signal[::decimation_factor]
    
    NOTE: Real-world ADCs apply a hardware anti-aliasing LPF before this step,
    but many cheap MEMS mics have inadequate filter roll-off — that's the vulnerability.
    """
    decimation_factor = original_rate // target_rate
    # TODO: return the downsampled signal
    raise NotImplementedError("Implement downsample_signal()")


# ── Part 2: Visualize What the AI "Hears" ─────────────────────────────────────

def plot_aliasing_effect():
    """
    Side-by-side plot:
      Left : Time domain — original attack signal vs what the AI records
      Right: Frequency domain (FFT) — showing the ghost alias frequency appearing
    """
    # TODO (after implementing above functions):
    #   1. Generate the attack signal
    #   2. Downsample it to SAMPLE_RATE_HZ (simulating the victim's ADC)
    #   3. Run FFT on both signals
    #   4. Plot:
    #      - Top-left    : attack signal waveform (time domain)
    #      - Bottom-left : downsampled signal waveform  
    #      - Top-right   : FFT of attack (shows spike at F_ATTACK_HZ)
    #      - Bottom-right: FFT of downsampled (shows spike at F_ALIAS_HZ — the ghost!)

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("GhostCommands: Aliasing Attack Visualization", fontsize=14, fontweight="bold")

    # TODO: Populate each subplot
    # axes[0][0].plot(...)  — original signal, time domain
    # axes[0][1].plot(...)  — original signal, FFT
    # axes[1][0].plot(...)  — downsampled signal, time domain
    # axes[1][1].plot(...)  — downsampled signal, FFT (the "ghost" frequency appears here)

    plt.tight_layout()
    plt.savefig("aliasing_demo.png", dpi=150)
    print("[+] Saved aliasing_demo.png")
    plt.show()


def compute_fft(signal: np.ndarray, sample_rate: int):
    """
    Compute the single-sided FFT magnitude spectrum.
    Returns (frequencies_hz, magnitudes).
    
    TODO: Implement using np.fft.rfft and np.fft.rfftfreq
    Hint: 
        freqs = np.fft.rfftfreq(len(signal), d=1/sample_rate)
        mags  = np.abs(np.fft.rfft(signal)) / len(signal)
    """
    # TODO: return (freqs, mags)
    raise NotImplementedError("Implement compute_fft()")


# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[*] Running aliasing simulation...")
    print(f"    Nyquist theorem: max clean frequency at {SAMPLE_RATE_HZ}Hz SR = {NYQUIST_HZ}Hz")
    print(f"    Attacker sends {F_ATTACK_HZ}Hz → folds to {F_ALIAS_HZ}Hz inside AI's range\n")
    plot_aliasing_effect()