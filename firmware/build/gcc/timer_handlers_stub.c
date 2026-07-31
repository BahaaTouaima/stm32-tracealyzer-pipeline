/* Stub handlers for MPS2 TIMER0/TIMER1 interrupts.
 * Declared and referenced directly in the vector table (startup_gcc.c)
 * but not implemented, since the interrupt-driven demo files were
 * removed from the build. Defined here so linking succeeds.
 * Marked weak so a real handler can override this later if needed. */

void __attribute__((weak)) TIMER0_Handler(void)
{
    for (;;) { }
}

void __attribute__((weak)) TIMER1_Handler(void)
{
    for (;;) { }
}
