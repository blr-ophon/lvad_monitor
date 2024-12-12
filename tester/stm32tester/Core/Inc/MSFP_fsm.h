#ifndef MSFP_FSM_H
#define MSFP_FSM_H

#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include "stm32f3xx_hal.h"
#include "MSP_channels.h"
#include "MSFP_parser.h"

typedef enum{
    STATE_IDLE,
    STATE_SYNC,
    STATE_CONN,
    STATE_TRANS,
} MSFP_State;

typedef enum{
    NOTIFY_STOP,
    NOTIFY_START,
    NOTIFY_READY,
    NOTIFY_HALT,
} MSFP_Notification;

int MSFP_fsm_update(UART_HandleTypeDef *huart);
void MSFP_ReceiveMsg(UART_HandleTypeDef *huart);
void MSFP_Notify(MSFP_Notification notif);

#endif
