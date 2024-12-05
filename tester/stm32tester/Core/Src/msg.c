#include "msg.h"

#define RECV_BUFFER_SIZE 100


uint8_t recvBuf[RECV_BUFFER_SIZE] = {0};
uint8_t recvBufIndex = 0;
int msg_ready = 0;

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){
    // Previous message was not processed or Buffer is full
    if(msg_ready || recvBufIndex >= RECV_BUFFER_SIZE -1){
        goto out;
    }

    //char *msg = "RECEIVED\r\n";
    //HAL_UART_Transmit_IT(huart, (uint8_t*)msg, strlen(msg));
    printf("RECEIVED (i:%d)\r\n", recvBufIndex);

    uint8_t byteReceived = recvBuf[recvBufIndex++];

    if((char) byteReceived == 'a'){
        processMsg(recvBuf);
        recvBufIndex = 0;
    }
out:
    HAL_UART_Receive_IT(huart, &recvBuf[recvBufIndex], 1);
}

void processMsg(uint8_t *msg){
    // TODO: parse and convert
    msg_ready = 1;
}
