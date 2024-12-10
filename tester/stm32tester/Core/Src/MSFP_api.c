#include "MSFP_api.h"

uint32_t maxSampleRate = 0;

void MSFP_Init(void){
    /*
     * User specify number of streams and max sample rate,
     * also the main() IT line and uart where the MSFP will run. 
     *
     * User also specifies another IT line, from which MSFP
     * will interact with user
     */
    MSFP_clearChannels();
}



