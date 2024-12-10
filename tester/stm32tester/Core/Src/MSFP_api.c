#include "MSFP_api.h"

uint32_t maxSampleRate = 0;
UART_HandleTypeDef *msfp_huart = NULL;
extern uint8_t msfp_recvBuf[100];

void MSFP_Init(UART_HandleTypeDef *huart){
    /*
     * TODO: pass a MSFP_HandleInit instead of huart
     * User code must specify each channel available
     * User code must specify an IRQ line from which MSFP will inform
     * of a stop request. IRQ handle is for user code.
     *
     *
     * User also specifies another IT line, from which MSFP
     * will interact with user
     */
    msfp_huart = huart;
    MSFP_clearChannels();

    // Start listening to UART port
    HAL_UART_Receive_IT(msfp_huart, msfp_recvBuf, 1);
}

/*
 * User code must always call this function if sensors will stop sending data.
 * Either normally or by some error.
 */
void MSFP_HaltNotify(void){
    //TODO: pass a MSFP_HandleInit instead of huart
    MSFP_fsm_update(msfp_huart);
}


