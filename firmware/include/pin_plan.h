#ifndef PIN_PLAN_H
#define PIN_PLAN_H
/* Logical GPIO indices for the simulated adapter; see docs/ASSUMPTIONS.md. */
enum axis_assumed_pin {
    AXIS_PIN_PWM = 0,
    AXIS_PIN_DIRECTION = 1,
    AXIS_PIN_ENABLE = 2,
    AXIS_PIN_ENCODER_A = 3,
    AXIS_PIN_ENCODER_B = 4,
    AXIS_PIN_HOME = 5,
    AXIS_PIN_ESTOP_OK = 6,
    AXIS_PIN_CAN_RX = 7,
    AXIS_PIN_CAN_TX = 8,
    AXIS_PIN_FORCE_ADC = 9
};
#endif
