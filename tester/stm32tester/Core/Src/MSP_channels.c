#include "MSP_channels.h"

MSFP_ChannelList msfp_channels;

void MSFP_clearChannels(void){
    memset(&msfp_channels, 0, sizeof(MSFP_ChannelList));
}

int MSFP_addChannel(uint8_t id, uint8_t data_format, uint32_t max_rate){
    int rv = 0;

    if(id >= MAX_CHANNELS){
        rv = -1;
        goto out;
    }

    msfp_channels.channels[id].data_format = data_format;
    msfp_channels.channels[id].max_rate = max_rate;
    msfp_channels.map[id] = 1;

out: 
    return rv;
}

int MSFP_removeChannel(uint8_t id){
    memset(&(msfp_channels.channels[id]), 0, sizeof(MSFP_Channel));
    msfp_channels.map[id] = 0;
}
