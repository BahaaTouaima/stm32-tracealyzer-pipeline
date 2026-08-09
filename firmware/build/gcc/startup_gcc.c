/*
 * FreeRTOS V202212.00
 * Copyright (C) 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * https://www.FreeRTOS.org
 * https://github.com/FreeRTOS
 *
 */



#include <stdint.h>
#include <stdio.h>

#include "FreeRTOS.h"
#include "trcRecorder.h"

/* FreeRTOS interrupt handlers. */
extern void vPortSVCHandler( void );
extern void xPortPendSVHandler( void );
extern void xPortSysTickHandler( void );
extern void SystemInit( void );
extern void TIM2_IRQHandler( void );
extern TraceISRHandle_t xTim2ISRHandle;
/* Exception handlers. */
static void HardFault_Handler( void ) __attribute__( ( naked ) );
static void Default_Handler( void ) __attribute__( ( naked ) );
void Reset_Handler( void ) __attribute__( ( naked ) );

extern int main( void );
extern uint32_t _estack;

/* Vector table. */
const uint32_t* isr_vector[] __attribute__((section(".isr_vector"), used)) =
{
    ( uint32_t * ) &_estack,
    ( uint32_t * ) &Reset_Handler,     // Reset                -15
    ( uint32_t * ) &Default_Handler,   // NMI_Handler          -14
    ( uint32_t * ) &HardFault_Handler, // HardFault_Handler    -13
    ( uint32_t * ) &Default_Handler,   // MemManage_Handler    -12
    ( uint32_t * ) &Default_Handler,   // BusFault_Handler     -11
    ( uint32_t * ) &Default_Handler,   // UsageFault_Handler   -10
    0, // reserved   -9
    0, // reserved   -8
    0, // reserved   -7
    0, // reserved   -6
    ( uint32_t * ) &vPortSVCHandler,    // SVC_Handler          -5
    ( uint32_t * ) &Default_Handler,    // DebugMon_Handler     -4
    0, // reserved   -3
    ( uint32_t * ) &xPortPendSVHandler, // PendSV handler       -2
    ( uint32_t * ) &xPortSysTickHandler,// SysTick_Handler      -1
   0, // IRQ0  WWDG
    0, // IRQ1  PVD
    0, // IRQ2  TAMP_STAMP
    0, // IRQ3  RTC_WKUP
    0, // IRQ4  FLASH
    0, // IRQ5  RCC
    0, // IRQ6  EXTI0
    0, // IRQ7  EXTI1
    0, // IRQ8  EXTI2
    0, // IRQ9  EXTI3
    0, // IRQ10 EXTI4
    0, // IRQ11 DMA1_Stream0
    0, // IRQ12 DMA1_Stream1
    0, // IRQ13 DMA1_Stream2
    0, // IRQ14 DMA1_Stream3
    0, // IRQ15 DMA1_Stream4
    0, // IRQ16 DMA1_Stream5
    0, // IRQ17 DMA1_Stream6
    0, // IRQ18 ADC
    0, // IRQ19 CAN1_TX
    0, // IRQ20 CAN1_RX0
    0, // IRQ21 CAN1_RX1
    0, // IRQ22 CAN1_SCE
    0, // IRQ23 EXTI9_5
    0, // IRQ24 TIM1_BRK_TIM9
    0, // IRQ25 TIM1_UP_TIM10
    0, // IRQ26 TIM1_TRG_COM_TIM11
    0, // IRQ27 TIM1_CC
    ( uint32_t * ) TIM2_IRQHandler,    // IRQ28 TIM2
};

void Reset_Handler( void )
{
    SystemInit();
    (void) main();
}

/* Variables used to store the value of registers at the time a hardfault
 * occurs.  These are volatile to try and prevent the compiler/linker optimizing
 * them away as the variables never actually get used. */
volatile uint32_t r0;
volatile uint32_t r1;
volatile uint32_t r2;
volatile uint32_t r3;
volatile uint32_t r12;
volatile uint32_t lr; /* Link register. */
volatile uint32_t pc; /* Program counter. */
volatile uint32_t psr;/* Program status register. */

/* Called from the hardfault handler to provide information on the processor
 * state at the time of the fault.
 */
static __attribute__( ( used ) ) void prvGetRegistersFromStack( uint32_t *pulFaultStackAddress )
{
    r0 = pulFaultStackAddress[ 0 ];
    r1 = pulFaultStackAddress[ 1 ];
    r2 = pulFaultStackAddress[ 2 ];
    r3 = pulFaultStackAddress[ 3 ];

    r12 = pulFaultStackAddress[ 4 ];
    lr = pulFaultStackAddress[ 5 ];
    pc = pulFaultStackAddress[ 6 ];
    psr = pulFaultStackAddress[ 7 ];

    printf( "Calling prvGetRegistersFromStack() from fault handler" );
    fflush( stdout );

    /* When the following line is hit, the variables contain the register values. */
    for( ;; );
}


void Default_Handler( void )
{
    __asm volatile
    (
        ".align 8                                \n"
        " ldr r3, =0xe000ed04                    \n" /* Load the address of the interrupt control register into r3. */
        " ldr r2, [r3, #0]                       \n" /* Load the value of the interrupt control register into r2. */
        " uxtb r2, r2                            \n" /* The interrupt number is in the least significant byte - clear all other bits. */
        "Infinite_Loop:                          \n" /* Sit in an infinite loop - the number of the executing interrupt is held in r2. */
        " b  Infinite_Loop                       \n"
        " .ltorg                                 \n"
    );
}







#include "stm32f405xx.h"

volatile uint32_t ulSensorInterruptCount = 0;
static volatile uint32_t ulBurstCounter = 0;

/* E5-02: fast timer interrupt simulating sensor bursts.
 * Fires periodically at a baseline rate; every 20th firing switches
 * to a short high-frequency burst (10x faster) for 5 interrupts,
 * then returns to baseline. */
void TIM2_IRQHandler( void )
{
    xTraceISRBegin(xTim2ISRHandle);

    TIM2->SR &= ~TIM_SR_UIF;  /* clear the update interrupt flag */
    ulSensorInterruptCount++;
    ulBurstCounter++;

    if (ulBurstCounter == 20)
    {
        /* enter burst: much shorter period for a handful of ticks */
        TIM2->ARR = 500;  /* fast burst period */
    }
    else if (ulBurstCounter == 25)
    {
        /* burst done, return to baseline */
        TIM2->ARR = 5000;  /* baseline period */
        ulBurstCounter = 0;
    }

    xTraceISREnd(0);
}












void HardFault_Handler( void )
{
    __asm volatile
    (
        ".align 8                                                   \n"
        " tst lr, #4                                                \n"
        " ite eq                                                    \n"
        " mrseq r0, msp                                             \n"
        " mrsne r0, psp                                             \n"
        " ldr r1, [r0, #24]                                         \n"
        " ldr r2, =prvGetRegistersFromStack                         \n"
        " bx r2                                                     \n"
        " .ltorg                                                    \n"
    );
}


