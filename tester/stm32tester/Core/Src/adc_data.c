#include "adc_data.h"

static float wav1_samples[100] = {0};
static float wav2_samples[100] = {0};
extern int ADC_send;
extern UART_HandleTypeDef huart2;

char d1_str[20] = {0};
char d2_str[20] = {0};

bool sending = false;

void msfp_user_callback(int notif){
    switch(notif){
        case NOTIFY_STOP:
            sending = false;
            break;
        case NOTIFY_START:
            sending = true;
            break;
    }
}

void ADCdata_test_generate(void) {
    Wave wav1 = {
        WAV_SINE,
        10,
        5
    };
    Wave wav2 = {
        WAV_SQUARE,
        10,
        5
    };

    FGen_simple(wav1_samples, 100, wav1, 300);
    FGen_simple(wav2_samples, 100, wav2, 30);

    for(int i = 0; i < 100; i++) {
        //printf("#D#%f#%f#$", wav1_samples[i], wav2_samples[i]);
    }
}

void ADCdata_test_send(void) {
    /*
     * TODO:
     * Final code will work this way:
     *
     * Whenever ADC fills the first half of the buffers, the halfCplt callback
     * will trigger UART to send half the buffer (the first half) via DMA.
     * Whenever ADC fills the second half of the buffers, the Cplt callback
     * will trigger UART to send half the buffer (the second half) via DMA.
     */
    for(int i = 0; sending; i++) {
        if(i == 100) {
            i = 0;
        }
        char msg[50]; // Adjust size as needed
        snprintf(d1_str, 19, "%f", wav1_samples[i]);
        snprintf(d2_str, 19, "%f", wav2_samples[i]);
        snprintf(msg, sizeof(msg), "#D#%s#%s#%d#$", d1_str, d2_str, strlen(d1_str) + strlen(d2_str));

        //printf("#D#%s#%s#%d#$", d1_str, d2_str, strlen(d1_str) + strlen(d2_str) );
        HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
        HAL_Delay(1000);
    }

    MSFP_Notify(NOTIFY_HALT);

    while(!sending){

    }
}



