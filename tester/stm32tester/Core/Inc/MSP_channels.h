#ifndef MSFP_CHANNELS_H
#define MSFP_CHANNELS_H

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_CHANNELS 32 

typedef struct{
    uint8_t* buf;
    uint8_t data_format;
    int max_rate;
    int clear_to_send;
} MSFP_Channel;

typedef struct{
    MSFP_Channel channels[MAX_CHANNELS];
    bool map[MAX_CHANNELS];
} MSFP_ChannelList;

void MSFP_clearChannels(void);
int MSFP_addChannel(uint8_t id, uint8_t data_format, uint32_t max_rate);
int MSFP_removeChannel(uint8_t id);

#endif
