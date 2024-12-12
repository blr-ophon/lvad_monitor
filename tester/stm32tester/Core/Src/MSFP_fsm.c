#include "MSFP_fsm.h"

#define RECV_BUFFER_SIZE 100

extern UART_HandleTypeDef *msfp_huart;

uint8_t msfp_recvBuf[RECV_BUFFER_SIZE] = {0};
uint8_t msfp_recvBufIndex = 0;

uint8_t FSM_State = STATE_IDLE;
bool user_halt = false;
bool user_ready = false;

/*
 * Callback. This function will be called whenever MSFP has to notify the user
 * (START and STOP)
 */
void (*userNotify)(int);

// TODO: append to packet queue?
MSFP_Packet last_packet;


void MSFP_Notify(MSFP_Notification notif){
    switch(notif){
        case NOTIFY_READY:
            user_ready = true;
            break;
        case NOTIFY_HALT:
            if(FSM_State == STATE_TRANS){
                user_halt = true;
            }
            break;
        default:
            break;
    }

    MSFP_fsm_update(msfp_huart);
}


void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    MSFP_ReceiveMsg(huart);
}


/*
 * Appends all bytes received in UART port until end of message is received
 */
void MSFP_ReceiveMsg(UART_HandleTypeDef *huart) {
    // Previous message was not processed or Buffer is full
    if(msfp_recvBufIndex >= RECV_BUFFER_SIZE -1) {
        //Discard all in buffer
        msfp_recvBufIndex = 0;
        goto out;
    }

    //char *msg = "RECEIVED\r\n";
    //HAL_UART_Transmit_IT(huart, (uint8_t*)msg, strlen(msg));
    //printf("RECEIVED (i:%d)\r\n", recvBufIndex);

    uint8_t byteReceived = msfp_recvBuf[msfp_recvBufIndex++];

    if((char) byteReceived == '$') {
        // End of message
        __HAL_UART_DISABLE_IT(huart, UART_IT_RXNE);
        // printf("(MCU) Received: %s\r\n", (char*)msfp_recvBuf);

        // Parse packet
        MSFP_Packet packet;
        if(MSFP_ParseMsg(msfp_recvBuf, msfp_recvBufIndex, &packet) > 0){
            last_packet = packet;
            // Notify fsm
            MSFP_fsm_update(huart);
        }

        __HAL_UART_ENABLE_IT(huart, UART_IT_RXNE);
        // Prepare for next message
        memset(msfp_recvBuf, 0, RECV_BUFFER_SIZE);
        msfp_recvBufIndex = 0;
    }

out:
    HAL_UART_Receive_IT(huart, &msfp_recvBuf[msfp_recvBufIndex], 1);
}



/*
 * Called everytime a valid message is received
 */
int MSFP_fsm_update(UART_HandleTypeDef *huart){
    int rv = 0;

    switch(FSM_State){
        case STATE_IDLE:
            // Waiting for SYNC packet
            if(last_packet.type == PKTTYPE_SYNC){
                // Respond SYNC packet
                //char *msg = "(MCU) SYNC RECEIVED\r\n";
                FSM_State = STATE_SYNC;
                char *msg = "#!#2#$";
                HAL_UART_Transmit_IT(huart, (uint8_t*)msg, strlen(msg));
                // printf("(MCU) SYNC RECEIVED (i:%d)\r\n", msfp_recvBufIndex);
            }
            break;

        case STATE_SYNC:
            // Waiting for Acknowledge
            if(last_packet.type == PKTTYPE_ACK){
                //char *msg = "(MCU) ACK received";
                //HAL_UART_Transmit_IT(huart, (uint8_t*)msg, strlen(msg));
                FSM_State = STATE_CONN;
            }else{
                char *msg = ". ";
                HAL_UART_Transmit_IT(huart, (uint8_t*)msg, strlen(msg));
                //FSM_State = STATE_IDLE;
            }
            // Set peripherals
            break;

        case STATE_CONN:
            // Waiting for transfer instructions
            if(last_packet.type == PKTTYPE_REQ){
                FSM_State = STATE_TRANS;
                userNotify(NOTIFY_START);

            }else{
                char *msg = ". ";
                HAL_UART_Transmit_IT(huart, (uint8_t*)msg, strlen(msg));
                //FSM_State = STATE_IDLE;
            }
            // Respond to keep alive
            break;

        case STATE_TRANS:
            // Allow data until stop is called

            if(user_halt){
                // Wait for MCU to stop it's tasks
                char *msg = "#S#$";
                HAL_UART_Transmit(huart, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
                FSM_State = STATE_CONN;
                user_halt = false;
            }

            else if(last_packet.type == PKTTYPE_STOP){
                //Respond stop
                // Signal stop request from controller. Wait for user halt
                userNotify(NOTIFY_STOP);
            }
            break;
    }
    memset(&last_packet, 0, sizeof(MSFP_Packet));

out:
    return rv;
}




////////////////////////////////////////////////////////////////////////////////
///                             DEPRECATED
////////////////////////////////////////////////////////////////////////////////

void oldMSFP_ParseMsg(UART_HandleTypeDef *huart, uint8_t *msg){
    // TODO
    char *msg_str = (char*) msg;
    char *pMsgStart = strchr(msg_str, '#');

    if(pMsgStart == NULL) {
        //No '#' found. Discard message
        msfp_recvBufIndex = 0;
        return;
    }

    char opt = pMsgStart[1];
    switch(opt) {
    case '?':
        //printf("#!#%d#$", data_streams_n);
        break;
    case 'A':
        // Send analog data
        //ADC_send = SET;
        printf("Send analog data\r\n");
        break;
    case 'S':
        // Stop sending
        
        //Wait for current msg on buffer to be sent, then send STOP confirmation
        while (HAL_UART_GetState(huart) != HAL_UART_STATE_READY) {}
        printf("#S#$");

        //ADC_send = RESET;
        break;
    default:
        printf("Unrecognized\r\n");
    }
}
