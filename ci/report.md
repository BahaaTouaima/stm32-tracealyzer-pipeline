# STM32 FreeRTOS Stress Test & Weakness Report

_Generated 2026-08-11 11:09:54 &middot; 10 finding(s)_

## Summary

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 8 |
| Medium | 2 |
| Low | 0 |

## Findings

### 1. [HIGH] skipped_task — t = 52.096ms

**Description:** Task waited 38.515ms to run after becoming ready (t=52.096ms)

**Recommendation:** Check for higher-priority tasks monopolizing the CPU during this window; consider raising this task's priority or adding time slicing.

<details>
<summary>Trace evidence (&plusmn;20ms)</summary>

| timestamp_ms | event_name | task_name | task_state | param2_raw |
| --- | --- | --- | --- | --- |
| 32.784 | 0x93 | DeadlineLog |  | 20 |
| 32.788 | TASK_DELAY_UNTIL |  | DELAYED |  |
| 32.795 | TASK_ACTIVATE | TX | RUNNING | 1 |
| 32.799 | QUEUE_SEND | Blinky-Queue |  | 1 |
| 32.801 | TASK_READY | Rx | READY |  |
| 32.804 | TASK_ACTIVATE | Rx | RUNNING | 2 |
| 32.808 | QUEUE_RECEIVE | Blinky-Queue |  | 4294967295 |
| 32.818 | 0x91 | Log |  | 1936942413 |
| 32.825 | QUEUE_RECEIVE_BLOCK | Blinky-Queue |  | 4294967295 |
| 32.831 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 32.834 | UNUSED_STACK | StackTest |  | 49 |
| 32.835 | TASK_DELAY |  | DELAYED |  |
| 32.839 | TASK_ACTIVATE | TX | RUNNING | 1 |
| 32.841 | TASK_DELAY_UNTIL |  | DELAYED |  |
| 32.845 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 33.067 | NEW_TIME |  |  |  |
| 34.032 | NEW_TIME |  |  |  |
| 35.058 | NEW_TIME |  |  |  |
| 36.062 | NEW_TIME |  |  |  |
| 37.062 | NEW_TIME |  |  |  |
| 38.075 | NEW_TIME |  |  |  |
| 39.028 | NEW_TIME |  |  |  |
| 40.029 | NEW_TIME |  |  |  |
| 41.147 | NEW_TIME |  |  |  |
| 42.095 | NEW_TIME |  |  |  |
| 42.096 | TASK_READY | TzCtrl | READY |  |
| 42.1 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 42.11 | UNUSED_STACK | StackTest |  | 49 |
| 42.113 | TASK_DELAY |  | DELAYED |  |
| 42.119 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 43.203 | NEW_TIME |  |  |  |
| 44.07 | NEW_TIME |  |  |  |
| 45.066 | NEW_TIME |  |  |  |
| 46.085 | NEW_TIME |  |  |  |
| 47.218 | NEW_TIME |  |  |  |
| 48.07 | NEW_TIME |  |  |  |
| 49.062 | NEW_TIME |  |  |  |
| 50.066 | NEW_TIME |  |  |  |
| 51.084 | NEW_TIME |  |  |  |
| 52.094 | NEW_TIME |  |  |  |
| 52.095 | TASK_READY | StressLoad | READY |  |
| 52.096 | TASK_READY | Skipped | READY |  |
| 52.097 | TASK_READY | TzCtrl | READY |  |
| 52.1 | TASK_ACTIVATE | StressLoad | RUNNING | 3 |
| 53.15 | NEW_TIME |  |  |  |
| 54.058 | NEW_TIME |  |  |  |
| 55.07 | NEW_TIME |  |  |  |
| 56.088 | NEW_TIME |  |  |  |
| 57.145 | NEW_TIME |  |  |  |
| 58.155 | NEW_TIME |  |  |  |
| 59.049 | NEW_TIME |  |  |  |
| 60.07 | NEW_TIME |  |  |  |
| 60.429 | ISR_BEGIN | TIM2_Sensor |  |  |
| 60.432 | TASK_ACTIVATE | StressLoad | RUNNING |  |
| 61.083 | NEW_TIME |  |  |  |
| 62.25 | NEW_TIME |  |  |  |
| 63.058 | NEW_TIME |  |  |  |
| 64.052 | NEW_TIME |  |  |  |
| 65.085 | NEW_TIME |  |  |  |
| 66.094 | NEW_TIME |  |  |  |
| 67.086 | NEW_TIME |  |  |  |
| 68.062 | NEW_TIME |  |  |  |
| 69.054 | NEW_TIME |  |  |  |
| 70.054 | NEW_TIME |  |  |  |
| 71.081 | NEW_TIME |  |  |  |
| 72.073 | NEW_TIME |  |  |  |

</details>

---

### 2. [HIGH] skipped_task — t = 714.047ms

**Description:** Task waited 38.742ms to run after becoming ready (t=714.047ms)

**Recommendation:** Check for higher-priority tasks monopolizing the CPU during this window; consider raising this task's priority or adding time slicing.

<details>
<summary>Trace evidence (&plusmn;20ms)</summary>

| timestamp_ms | event_name | task_name | task_state | param2_raw |
| --- | --- | --- | --- | --- |
| 694.048 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 695.039 | NEW_TIME |  |  |  |
| 696.036 | NEW_TIME |  |  |  |
| 697.034 | NEW_TIME |  |  |  |
| 697.112 | ISR_BEGIN | TIM2_Sensor |  |  |
| 697.12 | TASK_ACTIVATE | IDLE | RUNNING |  |
| 698.038 | NEW_TIME |  |  |  |
| 699.039 | NEW_TIME |  |  |  |
| 700.037 | NEW_TIME |  |  |  |
| 701.041 | NEW_TIME |  |  |  |
| 702.037 | NEW_TIME |  |  |  |
| 703.035 | NEW_TIME |  |  |  |
| 703.036 | TASK_READY | ResClaimant | READY |  |
| 703.038 | TASK_ACTIVATE | ResClaimant | RUNNING | 3 |
| 703.043 | MUTEX_TAKE | ContentionMutex |  | 50 |
| 703.048 | MUTEX_GIVE | ContentionMutex |  |  |
| 703.052 | TASK_DELAY |  | DELAYED |  |
| 703.056 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 704.037 | NEW_TIME |  |  |  |
| 704.038 | TASK_READY | TzCtrl | READY |  |
| 704.041 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 704.044 | UNUSED_STACK | StressLoad |  | 100 |
| 704.045 | TASK_DELAY |  | DELAYED |  |
| 704.049 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 705.036 | NEW_TIME |  |  |  |
| 706.038 | NEW_TIME |  |  |  |
| 707.047 | NEW_TIME |  |  |  |
| 708.046 | NEW_TIME |  |  |  |
| 709.04 | NEW_TIME |  |  |  |
| 709.041 | TASK_READY | Deadline | READY |  |
| 709.045 | TASK_ACTIVATE | Deadline | RUNNING | 2 |
| 710.045 | NEW_TIME |  |  |  |
| 710.047 | TASK_READY | TX | READY |  |
| 711.068 | NEW_TIME |  |  |  |
| 712.037 | NEW_TIME |  |  |  |
| 713.045 | NEW_TIME |  |  |  |
| 713.408 | 0x93 | DeadlineLog |  | 20 |
| 713.413 | TASK_DELAY_UNTIL |  | DELAYED |  |
| 713.421 | TASK_ACTIVATE | TX | RUNNING | 1 |
| 713.43 | QUEUE_SEND | Blinky-Queue |  | 1 |
| 713.432 | TASK_READY | Rx | READY |  |
| 713.435 | TASK_ACTIVATE | Rx | RUNNING | 2 |
| 713.438 | QUEUE_RECEIVE | Blinky-Queue |  | 4294967295 |
| 713.448 | 0x91 | Log |  | 1936942413 |
| 713.456 | QUEUE_RECEIVE_BLOCK | Blinky-Queue |  | 4294967295 |
| 713.462 | TASK_ACTIVATE | TX | RUNNING | 1 |
| 713.464 | TASK_DELAY_UNTIL |  | DELAYED |  |
| 713.468 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 714.045 | NEW_TIME |  |  |  |
| 714.046 | TASK_READY | StressLoad | READY |  |
| 714.047 | TASK_READY | Skipped | READY |  |
| 714.047 | TASK_READY | TzCtrl | READY |  |
| 714.05 | TASK_ACTIVATE | StressLoad | RUNNING | 3 |
| 715.036 | NEW_TIME |  |  |  |
| 716.052 | NEW_TIME |  |  |  |
| 717.042 | NEW_TIME |  |  |  |
| 718.034 | NEW_TIME |  |  |  |
| 719.038 | NEW_TIME |  |  |  |
| 720.038 | NEW_TIME |  |  |  |
| 721.037 | NEW_TIME |  |  |  |
| 722.035 | NEW_TIME |  |  |  |
| 723.038 | NEW_TIME |  |  |  |
| 724.034 | NEW_TIME |  |  |  |
| 725.034 | NEW_TIME |  |  |  |
| 726.034 | NEW_TIME |  |  |  |
| 727.039 | NEW_TIME |  |  |  |
| 728.037 | NEW_TIME |  |  |  |
| 729.052 | NEW_TIME |  |  |  |
| 730.032 | NEW_TIME |  |  |  |
| 731.035 | NEW_TIME |  |  |  |
| 732.034 | NEW_TIME |  |  |  |
| 733.032 | NEW_TIME |  |  |  |
| 734.033 | NEW_TIME |  |  |  |

</details>

---

### 3. [HIGH] skipped_task — t = 802.093ms

**Description:** Task waited 43.614ms to run after becoming ready (t=802.093ms)

**Recommendation:** Check for higher-priority tasks monopolizing the CPU during this window; consider raising this task's priority or adding time slicing.

<details>
<summary>Trace evidence (&plusmn;20ms)</summary>

| timestamp_ms | event_name | task_name | task_state | param2_raw |
| --- | --- | --- | --- | --- |
| 783.089 | NEW_TIME |  |  |  |
| 784.062 | NEW_TIME |  |  |  |
| 785.068 | NEW_TIME |  |  |  |
| 786.09 | NEW_TIME |  |  |  |
| 787.094 | NEW_TIME |  |  |  |
| 788.051 | NEW_TIME |  |  |  |
| 789.084 | NEW_TIME |  |  |  |
| 789.615 | ISR_BEGIN | TIM2_Sensor |  |  |
| 789.62 | TASK_ACTIVATE | IDLE | RUNNING |  |
| 790.085 | NEW_TIME |  |  |  |
| 791.058 | NEW_TIME |  |  |  |
| 792.056 | NEW_TIME |  |  |  |
| 792.057 | TASK_READY | TzCtrl | READY |  |
| 792.063 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 792.068 | UNUSED_STACK | StackTest |  | 49 |
| 792.071 | TASK_DELAY |  | DELAYED |  |
| 792.076 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 793.088 | NEW_TIME |  |  |  |
| 794.105 | NEW_TIME |  |  |  |
| 795.052 | NEW_TIME |  |  |  |
| 796.099 | NEW_TIME |  |  |  |
| 797.215 | NEW_TIME |  |  |  |
| 798.07 | NEW_TIME |  |  |  |
| 799.097 | NEW_TIME |  |  |  |
| 800.051 | NEW_TIME |  |  |  |
| 801.051 | NEW_TIME |  |  |  |
| 802.091 | NEW_TIME |  |  |  |
| 802.092 | TASK_READY | StressLoad | READY |  |
| 802.093 | TASK_READY | Skipped | READY |  |
| 802.093 | TASK_READY | TzCtrl | READY |  |
| 802.096 | TASK_ACTIVATE | StressLoad | RUNNING | 3 |
| 803.058 | NEW_TIME |  |  |  |
| 804.065 | NEW_TIME |  |  |  |
| 805.092 | NEW_TIME |  |  |  |
| 806.092 | NEW_TIME |  |  |  |
| 807.059 | NEW_TIME |  |  |  |
| 808.087 | NEW_TIME |  |  |  |
| 809.089 | NEW_TIME |  |  |  |
| 809.09 | TASK_READY | Deadline | READY |  |
| 810.071 | NEW_TIME |  |  |  |
| 811.063 | NEW_TIME |  |  |  |
| 812.108 | NEW_TIME |  |  |  |
| 813.105 | NEW_TIME |  |  |  |
| 814.076 | NEW_TIME |  |  |  |
| 815.057 | NEW_TIME |  |  |  |
| 816.07 | NEW_TIME |  |  |  |
| 817.028 | NEW_TIME |  |  |  |
| 818.066 | NEW_TIME |  |  |  |
| 819.059 | NEW_TIME |  |  |  |
| 820.062 | NEW_TIME |  |  |  |
| 821.027 | NEW_TIME |  |  |  |
| 822.063 | NEW_TIME |  |  |  |

</details>

---

### 4. [HIGH] skipped_task — t = 895.043ms

**Description:** Task waited 39.579ms to run after becoming ready (t=895.043ms)

**Recommendation:** Check for higher-priority tasks monopolizing the CPU during this window; consider raising this task's priority or adding time slicing.

<details>
<summary>Trace evidence (&plusmn;20ms)</summary>

| timestamp_ms | event_name | task_name | task_state | param2_raw |
| --- | --- | --- | --- | --- |
| 875.045 | TASK_DELAY |  | DELAYED |  |
| 875.054 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 876.029 | NEW_TIME |  |  |  |
| 877.064 | NEW_TIME |  |  |  |
| 878.063 | NEW_TIME |  |  |  |
| 879.06 | NEW_TIME |  |  |  |
| 880.097 | NEW_TIME |  |  |  |
| 881.031 | NEW_TIME |  |  |  |
| 882.064 | NEW_TIME |  |  |  |
| 882.08 | ISR_BEGIN | TIM2_Sensor |  |  |
| 882.084 | TASK_ACTIVATE | IDLE | RUNNING |  |
| 883.078 | NEW_TIME |  |  |  |
| 884.026 | NEW_TIME |  |  |  |
| 885.064 | NEW_TIME |  |  |  |
| 885.065 | TASK_READY | TzCtrl | READY |  |
| 885.07 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 885.08 | UNUSED_STACK | StressLoad |  | 100 |
| 885.083 | TASK_DELAY |  | DELAYED |  |
| 885.092 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 886.114 | NEW_TIME |  |  |  |
| 887.083 | NEW_TIME |  |  |  |
| 888.065 | NEW_TIME |  |  |  |
| 889.026 | NEW_TIME |  |  |  |
| 890.027 | NEW_TIME |  |  |  |
| 891.031 | NEW_TIME |  |  |  |
| 891.032 | TASK_READY | StressLoad | READY |  |
| 891.037 | TASK_ACTIVATE | StressLoad | RUNNING | 3 |
| 892.074 | NEW_TIME |  |  |  |
| 893.045 | NEW_TIME |  |  |  |
| 894.034 | NEW_TIME |  |  |  |
| 895.041 | NEW_TIME |  |  |  |
| 895.043 | TASK_READY | Skipped | READY |  |
| 895.043 | TASK_READY | TzCtrl | READY |  |
| 896.038 | NEW_TIME |  |  |  |
| 897.037 | NEW_TIME |  |  |  |
| 898.038 | NEW_TIME |  |  |  |
| 899.057 | NEW_TIME |  |  |  |
| 900.047 | NEW_TIME |  |  |  |
| 901.219 | NEW_TIME |  |  |  |
| 902.198 | NEW_TIME |  |  |  |
| 903.059 | NEW_TIME |  |  |  |
| 904.103 | NEW_TIME |  |  |  |
| 905.097 | NEW_TIME |  |  |  |
| 906.084 | NEW_TIME |  |  |  |
| 907.055 | NEW_TIME |  |  |  |
| 908.036 | NEW_TIME |  |  |  |
| 909.034 | NEW_TIME |  |  |  |
| 909.035 | TASK_READY | Deadline | READY |  |
| 910.035 | NEW_TIME |  |  |  |
| 910.035 | TASK_READY | TX | READY |  |
| 911.034 | NEW_TIME |  |  |  |
| 912.036 | NEW_TIME |  |  |  |
| 913.037 | NEW_TIME |  |  |  |
| 914.043 | NEW_TIME |  |  |  |
| 915.035 | NEW_TIME |  |  |  |

</details>

---

### 5. [HIGH] skipped_task — t = 984.034ms

**Description:** Task waited 39.523ms to run after becoming ready (t=984.034ms)

**Recommendation:** Check for higher-priority tasks monopolizing the CPU during this window; consider raising this task's priority or adding time slicing.

<details>
<summary>Trace evidence (&plusmn;20ms)</summary>

| timestamp_ms | event_name | task_name | task_state | param2_raw |
| --- | --- | --- | --- | --- |
| 964.037 | NEW_TIME |  |  |  |
| 964.038 | TASK_READY | TzCtrl | READY |  |
| 964.041 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 964.046 | UNUSED_STACK | StackTest |  | 49 |
| 964.048 | TASK_DELAY |  | DELAYED |  |
| 964.057 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 965.037 | NEW_TIME |  |  |  |
| 966.039 | NEW_TIME |  |  |  |
| 967.042 | NEW_TIME |  |  |  |
| 968.064 | NEW_TIME |  |  |  |
| 969.056 | NEW_TIME |  |  |  |
| 970.037 | NEW_TIME |  |  |  |
| 971.037 | NEW_TIME |  |  |  |
| 972.033 | NEW_TIME |  |  |  |
| 973.032 | NEW_TIME |  |  |  |
| 974.036 | NEW_TIME |  |  |  |
| 974.037 | TASK_READY | TzCtrl | READY |  |
| 974.041 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 974.047 | UNUSED_STACK | StackTest |  | 49 |
| 974.05 | TASK_DELAY |  | DELAYED |  |
| 974.055 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 974.554 | ISR_BEGIN | TIM2_Sensor |  |  |
| 974.565 | TASK_ACTIVATE | IDLE | RUNNING |  |
| 975.056 | NEW_TIME |  |  |  |
| 976.036 | NEW_TIME |  |  |  |
| 977.029 | NEW_TIME |  |  |  |
| 978.034 | NEW_TIME |  |  |  |
| 979.033 | NEW_TIME |  |  |  |
| 980.033 | NEW_TIME |  |  |  |
| 980.034 | TASK_READY | StressLoad | READY |  |
| 980.037 | TASK_ACTIVATE | StressLoad | RUNNING | 3 |
| 981.035 | NEW_TIME |  |  |  |
| 982.037 | NEW_TIME |  |  |  |
| 983.036 | NEW_TIME |  |  |  |
| 984.033 | NEW_TIME |  |  |  |
| 984.034 | TASK_READY | Skipped | READY |  |
| 984.034 | TASK_READY | TzCtrl | READY |  |
| 985.032 | NEW_TIME |  |  |  |
| 986.034 | NEW_TIME |  |  |  |
| 987.031 | NEW_TIME |  |  |  |
| 988.041 | NEW_TIME |  |  |  |
| 989.044 | NEW_TIME |  |  |  |
| 990.033 | NEW_TIME |  |  |  |
| 991.034 | NEW_TIME |  |  |  |
| 992.033 | NEW_TIME |  |  |  |
| 993.033 | NEW_TIME |  |  |  |
| 994.032 | NEW_TIME |  |  |  |
| 995.282 | NEW_TIME |  |  |  |
| 996.161 | NEW_TIME |  |  |  |
| 997.068 | NEW_TIME |  |  |  |
| 998.055 | NEW_TIME |  |  |  |
| 999.053 | NEW_TIME |  |  |  |
| 1000.081 | NEW_TIME |  |  |  |
| 1001.158 | NEW_TIME |  |  |  |
| 1002.088 | NEW_TIME |  |  |  |
| 1003.079 | NEW_TIME |  |  |  |
| 1003.081 | TASK_READY | ResClaimant | READY |  |
| 1003.089 | TASK_ACTIVATE | ResClaimant | RUNNING | 3 |
| 1003.098 | MUTEX_TAKE | ContentionMutex |  | 50 |
| 1003.105 | MUTEX_GIVE | ContentionMutex |  |  |
| 1003.109 | TASK_DELAY |  | DELAYED |  |
| 1003.117 | TASK_ACTIVATE | StressLoad | RUNNING | 3 |

</details>

---

### 6. [HIGH] skipped_task — t = 1073.047ms

**Description:** Task waited 34.288ms to run after becoming ready (t=1073.047ms)

**Recommendation:** Check for higher-priority tasks monopolizing the CPU during this window; consider raising this task's priority or adding time slicing.

<details>
<summary>Trace evidence (&plusmn;20ms)</summary>

| timestamp_ms | event_name | task_name | task_state | param2_raw |
| --- | --- | --- | --- | --- |
| 1053.07 | NEW_TIME |  |  |  |
| 1053.071 | TASK_READY | TzCtrl | READY |  |
| 1053.075 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 1053.08 | UNUSED_STACK | TX |  | 86 |
| 1053.082 | TASK_DELAY |  | DELAYED |  |
| 1053.089 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 1054.041 | NEW_TIME |  |  |  |
| 1055.043 | NEW_TIME |  |  |  |
| 1056.034 | NEW_TIME |  |  |  |
| 1057.035 | NEW_TIME |  |  |  |
| 1058.033 | NEW_TIME |  |  |  |
| 1059.034 | NEW_TIME |  |  |  |
| 1060.042 | NEW_TIME |  |  |  |
| 1061.053 | NEW_TIME |  |  |  |
| 1062.041 | NEW_TIME |  |  |  |
| 1063.039 | NEW_TIME |  |  |  |
| 1063.041 | TASK_READY | TzCtrl | READY |  |
| 1063.046 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 1063.054 | UNUSED_STACK | StressLoad |  | 100 |
| 1063.059 | TASK_DELAY |  | DELAYED |  |
| 1063.069 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 1064.042 | NEW_TIME |  |  |  |
| 1064.043 | TASK_READY | StackTest | READY |  |
| 1064.046 | TASK_ACTIVATE | StackTest | RUNNING | 1 |
| 1064.066 | TASK_DELAY |  | DELAYED |  |
| 1064.071 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 1065.034 | NEW_TIME |  |  |  |
| 1066.039 | NEW_TIME |  |  |  |
| 1066.046 | ISR_BEGIN | TIM2_Sensor |  |  |
| 1066.052 | TASK_ACTIVATE | IDLE | RUNNING |  |
| 1067.054 | NEW_TIME |  |  |  |
| 1068.051 | NEW_TIME |  |  |  |
| 1069.035 | NEW_TIME |  |  |  |
| 1069.036 | TASK_READY | StressLoad | READY |  |
| 1069.039 | TASK_ACTIVATE | StressLoad | RUNNING | 3 |
| 1070.033 | NEW_TIME |  |  |  |
| 1071.035 | NEW_TIME |  |  |  |
| 1072.035 | NEW_TIME |  |  |  |
| 1073.046 | NEW_TIME |  |  |  |
| 1073.047 | TASK_READY | Skipped | READY |  |
| 1073.047 | TASK_READY | TzCtrl | READY |  |
| 1074.04 | NEW_TIME |  |  |  |
| 1075.045 | NEW_TIME |  |  |  |
| 1076.031 | NEW_TIME |  |  |  |
| 1077.033 | NEW_TIME |  |  |  |
| 1078.034 | NEW_TIME |  |  |  |
| 1079.041 | NEW_TIME |  |  |  |
| 1080.042 | NEW_TIME |  |  |  |
| 1081.042 | NEW_TIME |  |  |  |
| 1082.033 | NEW_TIME |  |  |  |
| 1083.036 | NEW_TIME |  |  |  |
| 1084.034 | NEW_TIME |  |  |  |
| 1085.032 | NEW_TIME |  |  |  |
| 1086.049 | NEW_TIME |  |  |  |
| 1087.059 | NEW_TIME |  |  |  |
| 1088.047 | NEW_TIME |  |  |  |
| 1089.031 | NEW_TIME |  |  |  |
| 1090.034 | NEW_TIME |  |  |  |
| 1091.032 | NEW_TIME |  |  |  |
| 1092.034 | NEW_TIME |  |  |  |
| 1093.046 | NEW_TIME |  |  |  |

</details>

---

### 7. [HIGH] skipped_task — t = 1157.04ms

**Description:** Task waited 39.579ms to run after becoming ready (t=1157.040ms)

**Recommendation:** Check for higher-priority tasks monopolizing the CPU during this window; consider raising this task's priority or adding time slicing.

<details>
<summary>Trace evidence (&plusmn;20ms)</summary>

| timestamp_ms | event_name | task_name | task_state | param2_raw |
| --- | --- | --- | --- | --- |
| 1137.042 | NEW_TIME |  |  |  |
| 1137.043 | TASK_READY | TzCtrl | READY |  |
| 1137.047 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 1137.053 | UNUSED_STACK | StackTest |  | 49 |
| 1137.055 | TASK_DELAY |  | DELAYED |  |
| 1137.06 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 1138.044 | NEW_TIME |  |  |  |
| 1139.039 | NEW_TIME |  |  |  |
| 1140.056 | NEW_TIME |  |  |  |
| 1141.032 | NEW_TIME |  |  |  |
| 1142.036 | NEW_TIME |  |  |  |
| 1143.037 | NEW_TIME |  |  |  |
| 1144.033 | NEW_TIME |  |  |  |
| 1145.033 | NEW_TIME |  |  |  |
| 1146.051 | NEW_TIME |  |  |  |
| 1147.046 | NEW_TIME |  |  |  |
| 1147.047 | TASK_READY | TzCtrl | READY |  |
| 1147.05 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 1147.054 | UNUSED_STACK | StackTest |  | 49 |
| 1147.056 | TASK_DELAY |  | DELAYED |  |
| 1147.062 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 1148.035 | NEW_TIME |  |  |  |
| 1149.034 | NEW_TIME |  |  |  |
| 1150.034 | NEW_TIME |  |  |  |
| 1151.041 | NEW_TIME |  |  |  |
| 1152.032 | NEW_TIME |  |  |  |
| 1152.034 | TASK_READY | ResHolder | READY |  |
| 1152.036 | TASK_ACTIVATE | ResHolder | RUNNING | 1 |
| 1152.041 | MUTEX_TAKE | ContentionMutex |  | 4294967295 |
| 1152.044 | TASK_DELAY |  | DELAYED |  |
| 1152.048 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 1153.048 | NEW_TIME |  |  |  |
| 1153.049 | TASK_READY | ResClaimant | READY |  |
| 1153.052 | TASK_ACTIVATE | ResClaimant | RUNNING | 3 |
| 1153.067 | MUTEX_TAKE_BLOCK | ContentionMutex |  | 50 |
| 1153.069 | TASK_PRIO_INHERIT | ResHolder |  | 3 |
| 1153.08 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 1154.036 | NEW_TIME |  |  |  |
| 1155.034 | NEW_TIME |  |  |  |
| 1156.035 | NEW_TIME |  |  |  |
| 1157.038 | NEW_TIME |  |  |  |
| 1157.039 | TASK_READY | StressLoad | READY |  |
| 1157.04 | TASK_READY | Skipped | READY |  |
| 1157.04 | TASK_READY | TzCtrl | READY |  |
| 1157.043 | TASK_ACTIVATE | StressLoad | RUNNING | 3 |
| 1158.128 | NEW_TIME |  |  |  |
| 1159.043 | NEW_TIME |  |  |  |
| 1159.513 | ISR_BEGIN | TIM2_Sensor |  |  |
| 1159.518 | TASK_ACTIVATE | StressLoad | RUNNING |  |
| 1160.049 | NEW_TIME |  |  |  |
| 1161.036 | NEW_TIME |  |  |  |
| 1162.036 | NEW_TIME |  |  |  |
| 1163.036 | NEW_TIME |  |  |  |
| 1164.036 | NEW_TIME |  |  |  |
| 1165.037 | NEW_TIME |  |  |  |
| 1166.045 | NEW_TIME |  |  |  |
| 1167.04 | NEW_TIME |  |  |  |
| 1168.032 | NEW_TIME |  |  |  |
| 1169.044 | NEW_TIME |  |  |  |
| 1170.034 | NEW_TIME |  |  |  |
| 1171.037 | NEW_TIME |  |  |  |
| 1172.032 | NEW_TIME |  |  |  |
| 1173.05 | NEW_TIME |  |  |  |
| 1174.044 | NEW_TIME |  |  |  |
| 1175.033 | NEW_TIME |  |  |  |
| 1176.031 | NEW_TIME |  |  |  |
| 1177.032 | NEW_TIME |  |  |  |

</details>

---

### 8. [HIGH] skipped_task — t = 1246.034ms

**Description:** Task waited 36.732ms to run after becoming ready (t=1246.034ms)

**Recommendation:** Check for higher-priority tasks monopolizing the CPU during this window; consider raising this task's priority or adding time slicing.

<details>
<summary>Trace evidence (&plusmn;20ms)</summary>

| timestamp_ms | event_name | task_name | task_state | param2_raw |
| --- | --- | --- | --- | --- |
| 1226.036 | NEW_TIME |  |  |  |
| 1226.037 | TASK_READY | TzCtrl | READY |  |
| 1226.045 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 1226.051 | UNUSED_STACK | TX |  | 86 |
| 1226.053 | TASK_DELAY |  | DELAYED |  |
| 1226.058 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 1227.034 | NEW_TIME |  |  |  |
| 1228.036 | NEW_TIME |  |  |  |
| 1229.035 | NEW_TIME |  |  |  |
| 1230.037 | NEW_TIME |  |  |  |
| 1231.032 | NEW_TIME |  |  |  |
| 1231.05 | ISR_BEGIN | TIM2_Sensor |  |  |
| 1231.052 | TASK_ACTIVATE | IDLE | RUNNING |  |
| 1232.035 | NEW_TIME |  |  |  |
| 1233.039 | NEW_TIME |  |  |  |
| 1234.034 | NEW_TIME |  |  |  |
| 1235.034 | NEW_TIME |  |  |  |
| 1236.036 | NEW_TIME |  |  |  |
| 1236.036 | TASK_READY | TzCtrl | READY |  |
| 1236.039 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 1236.043 | UNUSED_STACK | StressLoad |  | 100 |
| 1236.045 | TASK_DELAY |  | DELAYED |  |
| 1236.049 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 1237.036 | NEW_TIME |  |  |  |
| 1238.04 | NEW_TIME |  |  |  |
| 1239.034 | NEW_TIME |  |  |  |
| 1239.484 | ISR_BEGIN | TIM2_Sensor |  |  |
| 1239.486 | TASK_ACTIVATE | IDLE | RUNNING |  |
| 1240.119 | NEW_TIME |  |  |  |
| 1241.034 | NEW_TIME |  |  |  |
| 1242.04 | NEW_TIME |  |  |  |
| 1243.035 | NEW_TIME |  |  |  |
| 1244.035 | NEW_TIME |  |  |  |
| 1245.034 | NEW_TIME |  |  |  |
| 1246.032 | NEW_TIME |  |  |  |
| 1246.033 | TASK_READY | StressLoad | READY |  |
| 1246.034 | TASK_READY | Skipped | READY |  |
| 1246.034 | TASK_READY | TzCtrl | READY |  |
| 1246.037 | TASK_ACTIVATE | StressLoad | RUNNING | 3 |
| 1247.033 | NEW_TIME |  |  |  |
| 1247.916 | ISR_BEGIN | TIM2_Sensor |  |  |
| 1247.919 | TASK_ACTIVATE | StressLoad | RUNNING |  |
| 1248.034 | NEW_TIME |  |  |  |
| 1249.032 | NEW_TIME |  |  |  |
| 1250.035 | NEW_TIME |  |  |  |
| 1251.036 | NEW_TIME |  |  |  |
| 1252.036 | NEW_TIME |  |  |  |
| 1252.036 | TASK_READY | ResHolder | READY |  |
| 1253.035 | NEW_TIME |  |  |  |
| 1254.037 | NEW_TIME |  |  |  |
| 1255.038 | NEW_TIME |  |  |  |
| 1256.036 | NEW_TIME |  |  |  |
| 1257.031 | NEW_TIME |  |  |  |
| 1258.036 | NEW_TIME |  |  |  |
| 1259.036 | NEW_TIME |  |  |  |
| 1260.033 | NEW_TIME |  |  |  |
| 1261.033 | NEW_TIME |  |  |  |
| 1262.034 | NEW_TIME |  |  |  |
| 1263.038 | NEW_TIME |  |  |  |
| 1264.036 | NEW_TIME |  |  |  |
| 1264.037 | TASK_READY | StackTest | READY |  |
| 1265.031 | NEW_TIME |  |  |  |
| 1266.034 | NEW_TIME |  |  |  |

</details>

---

### 9. [MEDIUM] missed_deadline — t = 722.051ms

**Description:** Deadline task started 167.943ms late (expected t=654.108ms, actual t=722.051ms)

**Recommendation:** Review the task's priority and the load of higher-priority tasks running around this time; the deadline task may be getting starved.

<details>
<summary>Trace evidence (&plusmn;20ms)</summary>

| timestamp_ms | event_name | task_name | task_state | param2_raw |
| --- | --- | --- | --- | --- |
| 703.035 | NEW_TIME |  |  |  |
| 703.036 | TASK_READY | ResClaimant | READY |  |
| 703.038 | TASK_ACTIVATE | ResClaimant | RUNNING | 3 |
| 703.043 | MUTEX_TAKE | ContentionMutex |  | 50 |
| 703.048 | MUTEX_GIVE | ContentionMutex |  |  |
| 703.052 | TASK_DELAY |  | DELAYED |  |
| 703.056 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 704.037 | NEW_TIME |  |  |  |
| 704.038 | TASK_READY | TzCtrl | READY |  |
| 704.041 | TASK_ACTIVATE | TzCtrl | RUNNING | 1 |
| 704.044 | UNUSED_STACK | StressLoad |  | 100 |
| 704.045 | TASK_DELAY |  | DELAYED |  |
| 704.049 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 705.036 | NEW_TIME |  |  |  |
| 706.038 | NEW_TIME |  |  |  |
| 707.047 | NEW_TIME |  |  |  |
| 708.046 | NEW_TIME |  |  |  |
| 709.04 | NEW_TIME |  |  |  |
| 709.041 | TASK_READY | Deadline | READY |  |
| 709.045 | TASK_ACTIVATE | Deadline | RUNNING | 2 |
| 710.045 | NEW_TIME |  |  |  |
| 710.047 | TASK_READY | TX | READY |  |
| 711.068 | NEW_TIME |  |  |  |
| 712.037 | NEW_TIME |  |  |  |
| 713.045 | NEW_TIME |  |  |  |
| 713.408 | 0x93 | DeadlineLog |  | 20 |
| 713.413 | TASK_DELAY_UNTIL |  | DELAYED |  |
| 713.421 | TASK_ACTIVATE | TX | RUNNING | 1 |
| 713.43 | QUEUE_SEND | Blinky-Queue |  | 1 |
| 713.432 | TASK_READY | Rx | READY |  |
| 713.435 | TASK_ACTIVATE | Rx | RUNNING | 2 |
| 713.438 | QUEUE_RECEIVE | Blinky-Queue |  | 4294967295 |
| 713.448 | 0x91 | Log |  | 1936942413 |
| 713.456 | QUEUE_RECEIVE_BLOCK | Blinky-Queue |  | 4294967295 |
| 713.462 | TASK_ACTIVATE | TX | RUNNING | 1 |
| 713.464 | TASK_DELAY_UNTIL |  | DELAYED |  |
| 713.468 | TASK_ACTIVATE | IDLE | RUNNING | 0 |
| 714.045 | NEW_TIME |  |  |  |
| 714.046 | TASK_READY | StressLoad | READY |  |
| 714.047 | TASK_READY | Skipped | READY |  |
| 714.047 | TASK_READY | TzCtrl | READY |  |
| 714.05 | TASK_ACTIVATE | StressLoad | RUNNING | 3 |
| 715.036 | NEW_TIME |  |  |  |
| 716.052 | NEW_TIME |  |  |  |
| 717.042 | NEW_TIME |  |  |  |
| 718.034 | NEW_TIME |  |  |  |
| 719.038 | NEW_TIME |  |  |  |
| 720.038 | NEW_TIME |  |  |  |
| 721.037 | NEW_TIME |  |  |  |
| 722.035 | NEW_TIME |  |  |  |
| 723.038 | NEW_TIME |  |  |  |
| 724.034 | NEW_TIME |  |  |  |
| 725.034 | NEW_TIME |  |  |  |
| 726.034 | NEW_TIME |  |  |  |
| 727.039 | NEW_TIME |  |  |  |
| 728.037 | NEW_TIME |  |  |  |
| 729.052 | NEW_TIME |  |  |  |
| 730.032 | NEW_TIME |  |  |  |
| 731.035 | NEW_TIME |  |  |  |
| 732.034 | NEW_TIME |  |  |  |
| 733.032 | NEW_TIME |  |  |  |
| 734.033 | NEW_TIME |  |  |  |
| 735.04 | NEW_TIME |  |  |  |
| 736.032 | NEW_TIME |  |  |  |
| 737.034 | NEW_TIME |  |  |  |
| 738.029 | NEW_TIME |  |  |  |
| 739.035 | NEW_TIME |  |  |  |
| 740.035 | NEW_TIME |  |  |  |
| 741.051 | NEW_TIME |  |  |  |

</details>

---

### 10. [MEDIUM] low_stack — t = N/A

**Description:** Task 'StackTest' has only 38.3% stack remaining (196 of 512 bytes)

**Recommendation:** Increase the allocated stack size for this task, or reduce local variable / call-depth usage inside it.

<details>
<summary>Trace evidence (&plusmn;20ms)</summary>

_No trace evidence available for this finding._

</details>

---

