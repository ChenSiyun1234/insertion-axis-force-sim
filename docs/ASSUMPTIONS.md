# Assumptions and component references

This is a simulation. I use `assumed` for my mechanics, circuit, pin and traffic choices, including computed calibration. `datasheet` marks component parameters under the linked test conditions. Typical curves describe the reference part response.

## Compact linear insertion fixture

The compact axis replaces an articulated mechanism with a direct screw-driven linear carriage. Its transmission radius is lead divided by twice pi; it is a conversion factor, not a lever arm. Both fixtures use only primitive geometry.

## Compact mechanics: SI units unless field states otherwise

| Parameter | Value | Classification |
|---|---|---|
| carriage_mass | 2.0 | assumed |
| module_mass | 2.0 | assumed |
| lead | 0.01 | assumed |
| gap | 0.01 | assumed |
| friction | 4.0 | assumed |
| latch_peak | 20.0 | assumed |
| latch_hold | 8.0 | assumed |
| latch_length | 0.008 | assumed |
| end | 0.04 | assumed |
| end_k | 500000.0 | assumed |
| jam_at | 0.02 | assumed |
| jam_k | 20000.0 | assumed |
| contact_k | 20000.0 | assumed |
| damping_ratio | 0.05 | assumed |
| kt | 0.06 | assumed |
| gear | 1.0 | assumed |
| efficiency | 0.8 | assumed |
| rotor_j | 1.2e-05 | assumed |
| current_tau | 0.0005 | assumed |
| max_current | 4.0 | assumed |
| joint_friction | 1.0 | assumed |
| encoder_counts | 4096 | assumed |

## Heavy fixture, bridge and integration defaults

| Parameter | Value | Classification |
|---|---|---|
| lead | 0.01 | assumed |
| efficiency | 0.9 | assumed |
| kt | 0.1 | assumed |
| rotor_j | 1.2e-05 | assumed |
| max_current | 8 | assumed |
| current_tau | 0.0005 | assumed |
| carriage_mass | 6 | assumed |
| coulomb | 10 | assumed |
| friction_smoothing | 0.001 | assumed |
| viscous | 50 | assumed |
| server_mass | 25 | assumed |
| rail_mu | 0.1 | assumed |
| gravity | 9.81 | assumed |
| pusher_k | 200 | assumed |
| damping_ratio | 0.05 | assumed |
| mate_start | 280 | assumed |
| mate_rise_end | 290 | assumed |
| connector_peak | 90 | assumed |
| connector_hold | 60 | assumed |
| end_stop | 295 | assumed |
| end_k | 500 | assumed |
| x_jam | 150 | assumed |
| k_jam | 100 | assumed |
| encoder_lines | 2048 | assumed |
| quadrature | 4 | assumed |
| cell_rating | 500 | assumed |
| cell_mv_v | 2 | assumed |
| excitation | 5 | assumed |
| vibration_rms | 2 | assumed |
| vibration_amp | 5 | assumed |
| vibration_hz | 150 | assumed |
| dt | 0.0001 | assumed |
| control_dt | 0.001 | assumed |
| baud | 115200 | assumed |
| seed | 42 | assumed |

## Resistive sensor front ends

| Parameter | Value | Classification |
|---|---|---|
| standard (pull-down ohm, series ohm, shunt F) | (3300, 1000, 4.7e-08) | assumed |
| slow (pull-down ohm, series ohm, shunt F) | (6800, 4700, 2.2e-07) | assumed |
| sensitive (pull-down ohm, series ohm, shunt F) | (1500, 680, 2.2e-08) | assumed |

## Sensor model

| Parameter | Value | Classification |
|---|---|---|
| Typical FSR curve points (N, ohm) | ((0.3, 62000), (0.5, 29000), (1, 15000), (2, 8500), (5, 4300), (10, 2550), (20, 1500)) | datasheet: Interlink typical graph; approximate digitization |
| Power-law fit R = A F^(-b) | (17394.594950645427, 0.8503824633118839) | assumed: least-squares fit to typical points |
| Actuation threshold N | 0.2 | datasheet: typical minimum |
| Off resistance ohm | 10000000 | assumed: finite approximation to datasheet >10 Mohm |
| Excitation / reference V | 3.3 | assumed |
| ADC bits / full scale | (12, 4095) | assumed |
| ADC noise RMS LSB | 1.5 | assumed |
| Acquisition rate Hz | 1000 | assumed |
| Initial filter voltage V | 0 | assumed |
| Above-curve extrapolation beyond N | 20 | assumed |

Reference: [Interlink FSR 400 Series](https://www.interlinkelectronics.com/downloads/datasheets/fsr-400-series-datasheet.pdf), typical curve and Model 402. Hysteresis, drift, sample-and-hold loading and manufacturing spread are omitted.

## Bridge converter model (rate Hz, settling periods, noise V RMS, full scale V)

| Parameter | Value | Classification |
|---|---|---|
| IDEAL_1000 | (1000, 0, 0.0, 0.016) | assumed: synthetic reference |
| HX711_10 | (10, 4, 5e-08, 0.01953125) | datasheet: component reference below |
| HX711_80 | (80, 4, 9e-08, 0.01953125) | datasheet: component reference below |
| ADS1220_330 | (330, 1, 3.4e-07, 0.016) | datasheet: component reference below |
| ADS1220_1000 | (1000, 1, 7e-07, 0.016) | datasheet: component reference below |
| ADS1220_2000 | (2000, 1, 8.2e-07, 0.016) | datasheet: component reference below |

References: [HX711](https://cdn.sparkfun.com/assets/0/2/7/d/1/HX711_datasheet.pdf), electrical characteristics at gain 128; [ADS1220](https://www.ti.com/lit/ds/symlink/ads1220.pdf), gain 128 noise tables and single-cycle settling. All bridge excitation, vibration and load choices remain assumed.

## Controller defaults (value; allowed range; unit)

| Parameter | Value | Classification |
|---|---|---|
| lc_counts_per_N | 10485.76; 1..1000000.0; counts/N | assumed |
| pusher_stiffness_N_per_mm | 200; 1..1000; N/mm | assumed |
| free_limit_N | 60; 1..500; N | assumed |
| mate_limit_N | 150; 1..500; N | assumed |
| seat_force_N | 110; 1..500; N | assumed |
| mate_start_mm | 278; 0..1000; mm | assumed |
| seat_lo_mm | 293; 0..1000; mm | assumed |
| seat_hi_mm | 297; 0..1000; mm | assumed |
| approach_speed_mm_s | 100; 1..200; mm/s | assumed |
| insert_speed_mm_s | 10; 1..100; mm/s | assumed |
| slow_zone_mm | 270; 0..1000; mm | assumed |
| force_filter_hz | 0; 0..500; Hz | assumed |
| stale_timeout_ms | 5; 5..5000; ms | assumed |
| backoff_mm | 2; 0..20; mm | assumed |
| comm_timeout_ms | 200; 20..5000; ms | assumed |
| envelope_enabled | 1; 0..1; bool | assumed |
| max_current_A | 8; 0.1..8; A | assumed |
| accel_mm_s2 | 500; 10..3000; mm/s^2 | assumed |
| velocity_kp | 0.035; 0..1; A/(mm/s) | assumed |
| velocity_ki | 0.12; 0..10; A/mm | assumed |
| velocity_filter_hz | 80; 1..500; Hz | assumed |
| backoff_speed_mm_s | 10; 1..50; mm/s | assumed |
| counts_per_mm | 819.2; 1..100000; counts/mm | assumed |
| position_kp | 5; 0.1..50; 1/s | assumed |
| force_sensor | 0; 0..1; enum | assumed |
| fsr_pulldown_ohm | 3300; 1..10000000; ohm | assumed |
| fsr_a | 17394.59495; 1..10000000; ohm*N^b | assumed |
| fsr_b | 0.8503824633; 0.1..3; 1 | assumed |
| adc_full_scale | 4095; 2..65535; counts | assumed |
| adc_vref | 3.3; 0.1..5; V | assumed |
| drive_mode | 0; 0..1; enum | assumed |
| duty_kp | 0.004375; 0..1; duty/(mm/s) | assumed |
| duty_ki | 0.015; 0..10; duty/mm | assumed |
| wiring_check_mm_s | 2; 0.1..200; mm/s | assumed |
| wiring_check_ms | 50; 1..5000; ms | assumed |
| home_speed_mm_s | 5; 1..50; mm/s | assumed |
| home_debounce_ms | 3; 1..100; ms | assumed |
| home_backoff_mm | 1; 0.01..20; mm | assumed |
| home_max_travel_mm | 60; 1..1000; mm | assumed |

## Compact fixture control overrides

| Parameter | Value | Classification |
|---|---|---|
| free_limit_N | 15 | assumed |
| mate_limit_N | 35 | assumed |
| seat_force_N | 25 | assumed |
| approach_speed_mm_s | 30 | assumed |
| insert_speed_mm_s | 10 | assumed |
| mate_start_mm | 40.0 | assumed |
| seat_lo_mm | 47.0 | assumed |
| seat_hi_mm | 52.0 | assumed |
| slow_zone_mm | 8.0 | assumed |
| pusher_stiffness_N_per_mm | 20.0 | assumed |
| counts_per_mm | 409.6 | assumed |
| accel_mm_s2 | 100 | assumed |
| backoff_mm | 2 | assumed |
| drive_mode | 1 | assumed |
| duty_kp | 0.004375 | assumed |
| duty_ki | 0.015 | assumed |

## PWM motor and home switch

| Parameter | Value | Classification |
|---|---|---|
| Supply V / winding ohm / inductance H | (24, 3, 0.0005) | assumed |
| Back-EMF constant V s/rad | 0.06 | assumed: reciprocal SI motor constant |
| Initial switch position mm / bounce ms / random seed | (-30, 2, 41) | assumed |
| Contact regularization impedance / points | (0.001, 4) | assumed |
| Unloading observation s / insertion budget s | (1.5, 12) | assumed |
| Homing run budget s / heartbeat period ms | (30, 50) | assumed |

## Logical pin plan

| Parameter | Value | Classification |
|---|---|---|
| PWM | 0 | assumed: simulated logical index |
| direction | 1 | assumed: simulated logical index |
| enable | 2 | assumed: simulated logical index |
| encoder A | 3 | assumed: simulated logical index |
| encoder B | 4 | assumed: simulated logical index |
| home active-low | 5 | assumed: simulated logical index |
| E-stop healthy | 6 | assumed: simulated logical index |
| CAN RX | 7 | assumed: simulated logical index |
| CAN TX | 8 | assumed: simulated logical index |
| force-node ADC | 9 | assumed: simulated logical index |

The force-node ADC and controller use separate logical nodes. The pin plan maps signals to the C simulation interface.

## CAN and delay experiments

| Parameter | Value | Classification |
|---|---|---|
| Bitrate bit/s | 1000000 | assumed |
| Force identifiers high / low | ('0x080', '0x700') | assumed |
| Motion command/status IDs | ('0x101..0x103', '0x181..0x183') | assumed |
| Additional shared-bus command/status IDs | ('0x201..0x206', '0x011..0x016') | assumed |
| Motion nodes / extra shared nodes / payload bytes | (3, 6, 8) | assumed |
| Motion command period ms / reply processing ms | (10, 0.1) | assumed |
| Transmit slots / receive FIFOs / depth | (3, 2, 3) | assumed |
| Force payload bytes (FSR / bridge) | (2, 3) | assumed |
| Closed-loop send periods ms | (1, 2, 5, 10, 20) | assumed |
| Injected delays ms / drop fraction | ((0, 1, 5, 10, 20), 0.05) | assumed |
| Closed-loop phase seed / delay-loss seed | (7, 7) | assumed |
| Open-loop duration s / discarded startup s / seeds | (3, 0.5, (0, 1, 2)) | assumed |
| Open-loop send periods ms / bit-error probabilities | ((1, 5, 20), (0, 0.0001)) | assumed |
| Open-loop force waveform N / period s | ('20 + 20 sin(t)', 2) | assumed |
| Stale budget ms | max(5, 2*send_ms + 1); separate 10 ms send / 5 ms timeout case | assumed |


I use the [Bosch CAN 2.0, part A](https://www.port.de/fileadmin/user_upload/Dateien_IST_fuer_Migration/CAN20A.pdf)
frame, CRC, stuffing, arbitration and error-flag rules. Queue sizes follow
[STM32G4 RM0440, section 44.3.6](https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf):
212 RAM words, three transmit elements and two receive FIFOs of depth three.
Transmit queue mode selects the lowest identifier; full receive FIFOs discard
the new frame (FnOM=0).

All receivers acknowledge. Failed bit-error attempts occupy a full frame plus
17 recovery bits: six active error bits, eight delimiter bits and three
intermission bits. The transmitter error counter rises by eight on failure and
falls by one on success; bus-off starts at 256 with recovery disabled. The
eight-bit error-passive suspension delays only the sender. Receiver error
counters, clock drift and physical fault locations are outside this timing model.

Synthetic motion nodes exchange commands and status on the periods above; status
is released 0.1 ms after command EOF. Interrupt or tick-based receive draining is
selected per case. The open-loop sweep feeds the sensitive FSR divider with a
sinusoidal force rounded to unsigned ADC codes; it isolates transport timing
from plant motion, RC settling and sensor noise.

## Visual layout (SI units)

| Parameter | Value | Classification |
|---|---|---|
| Base plate center / half-size | ((0.2, 0, -0.07), (0.4, 0.15, 0.02)) | assumed |
| Fixture world height | 0.5 | assumed |
| Rail centers y / half-size | ((-0.09, 0.09), (0.35, 0.01, 0.015)) | assumed |
| Controller box position / half-size | ((-0.13, 0.11, 0.02), (0.06, 0.03, 0.025)) | assumed |
| Carriage center / half-size | ((-0.06, 0, 0), (0.05, 0.06, 0.025)) | assumed |
| Compact pad center / half-size | ((-0.004, 0, 0), (0.004, 0.025, 0.025)) | assumed |
| Compact load half-size | (0.02, 0.04, 0.04) | assumed |
| Heavy load center / half-size | ((0.1, 0, 0), (0.1, 0.08, 0.04)) | assumed |
| Stop half-size compact / heavy | ((0.015, 0.1, 0.06), (0.02, 0.12, 0.06)) | assumed |
| Jam marker half-size | (0.008, 0.025, 0.04) | assumed |
| Ground half-extent / display thickness | (2, 2, 0.1) | assumed |

All remaining camera poses, light positions, colors and overlay coordinates in `sim3d/scene.py` and `sim3d/render.py` are assumed display choices. They do not affect force or inertia. Gravity is disabled in the constrained horizontal MuJoCo fixtures; the heavy model uses its assumed gravity value only in rail friction.

## Isolated input circuit

| Parameter | Value | Classification |
|---|---|---|
| R1 / R2 / shunt / pull-up ohm | (887, 887, 453, 10000) | assumed |
| Resistor tolerances | (0.99, 1.01) | assumed |
| Input sweep V / spacing V | ((-30, 30), 0.02) | assumed |
| Logic supply V / LOW-HIGH thresholds V | (3.3, 0.99, 2.31) | assumed |
| DZ1 nominal V / corner V | (2.7, (2.5, 2.9)) | datasheet: BZX55C2V7 reference in hw/DESIGN.md |
| Optocoupler CTR / LED VF corners | ((1, 4), (1.1, 1.4)) | datasheet: TLP291 GB test points; extension across current assumed |
| Nominal CTR / LED VF | (2, 1.25) | assumed |
| Photocurrent resistors ohm / capacitor F | (1000, 1000, 7e-09) | assumed |
| Sink floor V / taper V / dark current A / output C F | (0.2, 0.01, 1e-05, 3e-11) | assumed |
| Rectifier model Is A / N / Rs ohm | (1e-09, 1.6, 0.1) | assumed |
| Zener model Is A / N / Rs ohm | (1e-12, 1, 10) | assumed |
| Thermal voltage V / opto ideality | (0.02585, 2) | assumed |
| Step stimulus V / rise-fall s / edges s | (24, 1e-07, (0.001, 0.003)) | assumed |
| Independent resistor corner combinations | 16 | assumed |
| Type 3 comparison regions V and mA | ON: 11..30 V, 2..15 mA; OFF union: -3..5 V to 15 mA, <=1.5 mA through 11 V | datasheet: source tables linked in hw/DESIGN.md |

## Brake circuit

| Parameter | Value | Classification |
|---|---|---|
| Coil V / W / R ohm / L H | (24, 8, 72, 0.6) | assumed |
| Supply corners V | (21.6, 24, 26.4) | assumed |
| Gate source V / Rg ohm / Rpd ohm | (3.3, 330, 10000) | assumed |
| Off time s / end time s / max integration step s | (0.05, 0.12, 1e-05) | assumed |
| Drop-out fraction / free-fall gravity | (0.3, 9.80665) | assumed |
| IRL540N Vth V / Rds reference ohm-V | ((1, 1.5, 2), (0.063, 4, 0.044, 10)) | datasheet: test conditions in hw/DESIGN.md |
| Cgs / Cgd / Cds F | (1.63e-09, 1.7e-10, 1.8e-10) | datasheet: derived from typical one-bias capacitances |
| SMBJ24A breakdown / clamp V and test current A | ((26.7, 28.1, 29.5), 38.9, 15.4) | datasheet: nominal midpoint assumed |
| SMBJ43A breakdown / clamp V and test current A | ((47.8, 50.3, 52.8), 69.4, 8.6) | datasheet: nominal midpoint assumed |
| TVS dynamic resistance ohm | (0.6103896103896103, 1.9302325581395359) | assumed: linear fits to reference endpoints |
| Reset switch Ron / Roff / threshold / hysteresis | (0.01, 1000000000000000.0, 0.5, 0.1) | assumed |
| Gate resistor factors | (0.99, 1.01) | assumed |
| Conservative pulse envelope W / s | (100, 0.01) | assumed: screening interpretation, not repetitive rating |

The electrical component source links and their test conditions are in [hw/DESIGN.md](../hw/DESIGN.md). All SPICE model coefficients, integration tolerances and ideal switch parameters are assumed fits, even where anchored to a datasheet point. The circuit studies do not simulate physical isolation, layout, temperature or mechanical brake engagement.

## Reference experiment grids

All sweep settings are **assumed**: speeds 25, 50, 100 and 200 mm/s; stiffness 200, 50, 20 and 5 N/mm; accelerations 500 and 50 mm/s?; jam coordinates 50, 150 and 250 mm; filter bypass, 200, 100, 50 and 20 Hz; nominal random seeds 42 through 61. The previous-gain diagnostic uses velocity Kp 0.035 and Ki 0.8. The runners define the full experiment grids.
