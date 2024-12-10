#ifndef MSFP_API_H
#define MSFP_API_H

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "stm32f3xx_hal.h"
#include "MSP_channels.h"
#include "MSFP_fsm.h"


void MSFP_Init(void);
void MSFP_Connect(void);
void MSFP_Encode(void);
void MSFP_Decode(void);

#endif
