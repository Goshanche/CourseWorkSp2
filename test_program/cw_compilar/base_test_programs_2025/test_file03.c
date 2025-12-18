#define _CRT_SECURE_NO_WARNINGS

#include "stdio.h"

int data[8192] = {0};
int contextStack[8192] = {0}, contextStackIndex = 0;
int opStack[8192] = {0}, opStackIndex = 0, opTemp = 0;
int lastBindDataIndex = 0;

int main() {
    contextStackIndex = 0;
    opStackIndex = 0;
    opTemp = 0;
    lastBindDataIndex = 0;

    //";"

    //"4"
    opStack[++opStackIndex] = opTemp = 0x00000004;

    //"Input"
    (void)scanf_s("%d", &opTemp);
    data[opStack[opStackIndex]] = opTemp, opStackIndex = 0;

    //null statement (non-context)

    //";"

    //"8"
    opStack[++opStackIndex] = opTemp = 0x00000008;

    //"Input"
    (void)scanf_s("%d", &opTemp);
    data[opStack[opStackIndex]] = opTemp, opStackIndex = 0;

    //null statement (non-context)

    //";"

    //"aaaa1"
    opStack[++opStackIndex] = opTemp = data[0x00000004];

    //"12"
    opStack[++opStackIndex] = opTemp = 0x0000000C;

    //":>"
    lastBindDataIndex = opStack[opStackIndex];
    data[lastBindDataIndex] = opTemp = opStack[opStackIndex - 1], opStackIndex = 0;

    //null statement (non-context)

    //";"

    //"While"
LABEL__WHILE_00007FF6CECBA490:

    //"clea1"
    opStack[++opStackIndex] = opTemp = data[0x0000000C];

    //"bbbb2"
    opStack[++opStackIndex] = opTemp = data[0x00000008];

    //"Le"
    opTemp = opStack[opStackIndex - 1] = opStack[opStackIndex - 1] <= opStack[opStackIndex]; --opStackIndex;

    //null statement (non-context)

    //after cond expresion (after "While")
    if (opTemp == 0) goto LABEL__AFTER_WHILE_00007FF6CECBA490;

    //"clea1"
    opStack[++opStackIndex] = opTemp = data[0x0000000C];

    //"clea1"
    opStack[++opStackIndex] = opTemp = data[0x0000000C];

    //"Mul"
    opTemp = opStack[opStackIndex - 1] *= opStack[opStackIndex]; --opStackIndex;

    //"Output"
    (void)printf("%d\r\n", opTemp = opStack[opStackIndex]), opStackIndex = 0;

    //null statement (non-context)

    //";"

    //"clea1"
    opStack[++opStackIndex] = opTemp = data[0x0000000C];

    //"1"
    opStack[++opStackIndex] = opTemp = 0x00000001;

    //"+"
    opTemp = opStack[opStackIndex - 1] += opStack[opStackIndex]; --opStackIndex;

    //"12"
    opStack[++opStackIndex] = opTemp = 0x0000000C;

    //":>"
    lastBindDataIndex = opStack[opStackIndex];
    data[lastBindDataIndex] = opTemp = opStack[opStackIndex - 1], opStackIndex = 0;

    //null statement (non-context)

    //";"

    //end of while
    goto LABEL__WHILE_00007FF6CECBA490;
LABEL__AFTER_WHILE_00007FF6CECBA490:

    //"0"
    opStack[++opStackIndex] = opTemp = 0x00000000;

    //"20"
    opStack[++opStackIndex] = opTemp = 0x00000014;

    //":>"
    lastBindDataIndex = opStack[opStackIndex];
    data[lastBindDataIndex] = opTemp = opStack[opStackIndex - 1], opStackIndex = 0;

    //null statement (non-context)

    //";"

    //"1"
    opStack[++opStackIndex] = opTemp = 0x00000001;

    //"12"
    opStack[++opStackIndex] = opTemp = 0x0000000C;

    //":>"
    lastBindDataIndex = opStack[opStackIndex];
    data[lastBindDataIndex] = opTemp = opStack[opStackIndex - 1], opStackIndex = 0;

    //null statement (non-context)

    //";"

    //"While"
LABEL__WHILE_00007FF6CECC3608:

    //"clea1"
    opStack[++opStackIndex] = opTemp = data[0x0000000C];

    //"aaaa1"
    opStack[++opStackIndex] = opTemp = data[0x00000004];

    //"Le"
    opTemp = opStack[opStackIndex - 1] = opStack[opStackIndex - 1] <= opStack[opStackIndex]; --opStackIndex;

    //null statement (non-context)

    //after cond expresion (after "While")
    if (opTemp == 0) goto LABEL__AFTER_WHILE_00007FF6CECC3608;

    //"1"
    opStack[++opStackIndex] = opTemp = 0x00000001;

    //"16"
    opStack[++opStackIndex] = opTemp = 0x00000010;

    //":>"
    lastBindDataIndex = opStack[opStackIndex];
    data[lastBindDataIndex] = opTemp = opStack[opStackIndex - 1], opStackIndex = 0;

    //null statement (non-context)

    //";"

    //"While"
LABEL__WHILE_00007FF6CECC6C10:

    //"cleb1"
    opStack[++opStackIndex] = opTemp = data[0x00000010];

    //"bbbb2"
    opStack[++opStackIndex] = opTemp = data[0x00000008];

    //"Le"
    opTemp = opStack[opStackIndex - 1] = opStack[opStackIndex - 1] <= opStack[opStackIndex]; --opStackIndex;

    //null statement (non-context)

    //after cond expresion (after "While")
    if (opTemp == 0) goto LABEL__AFTER_WHILE_00007FF6CECC6C10;

    //"xval1"
    opStack[++opStackIndex] = opTemp = data[0x00000014];

    //"1"
    opStack[++opStackIndex] = opTemp = 0x00000001;

    //"+"
    opTemp = opStack[opStackIndex - 1] += opStack[opStackIndex]; --opStackIndex;

    //"20"
    opStack[++opStackIndex] = opTemp = 0x00000014;

    //":>"
    lastBindDataIndex = opStack[opStackIndex];
    data[lastBindDataIndex] = opTemp = opStack[opStackIndex - 1], opStackIndex = 0;

    //null statement (non-context)

    //";"

    //"cleb1"
    opStack[++opStackIndex] = opTemp = data[0x00000010];

    //"1"
    opStack[++opStackIndex] = opTemp = 0x00000001;

    //"+"
    opTemp = opStack[opStackIndex - 1] += opStack[opStackIndex]; --opStackIndex;

    //"16"
    opStack[++opStackIndex] = opTemp = 0x00000010;

    //":>"
    lastBindDataIndex = opStack[opStackIndex];
    data[lastBindDataIndex] = opTemp = opStack[opStackIndex - 1], opStackIndex = 0;

    //null statement (non-context)

    //";"

    //end of while
    goto LABEL__WHILE_00007FF6CECC6C10;
LABEL__AFTER_WHILE_00007FF6CECC6C10:

    //"clea1"
    opStack[++opStackIndex] = opTemp = data[0x0000000C];

    //"1"
    opStack[++opStackIndex] = opTemp = 0x00000001;

    //"+"
    opTemp = opStack[opStackIndex - 1] += opStack[opStackIndex]; --opStackIndex;

    //"12"
    opStack[++opStackIndex] = opTemp = 0x0000000C;

    //":>"
    lastBindDataIndex = opStack[opStackIndex];
    data[lastBindDataIndex] = opTemp = opStack[opStackIndex - 1], opStackIndex = 0;

    //null statement (non-context)

    //end of while
    goto LABEL__WHILE_00007FF6CECC3608;
LABEL__AFTER_WHILE_00007FF6CECC3608:

    //null statement (non-context)

    //"xval1"
    opStack[++opStackIndex] = opTemp = data[0x00000014];

    //"Output"
    (void)printf("%d\r\n", opTemp = opStack[opStackIndex]), opStackIndex = 0;

    //null statement (non-context)

    //";"

    //"4"
    opStack[++opStackIndex] = opTemp = 0x00000004;

    //"Input"
    (void)scanf_s("%d", &opTemp);
    data[opStack[opStackIndex]] = opTemp, opStackIndex = 0;

    //null statement (non-context)

    //";"

    return 0;
}