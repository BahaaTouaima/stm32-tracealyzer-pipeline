import struct
import sys

# TraceHeader_t layout (from trcStreamingRecorder.c):
# uint32_t uiPSF;
# uint16_t uiVersion;
# uint16_t uiPlatform;
# uint32_t uiOptions;
# uint32_t uiNumCores;
# uint32_t isrTailchainingThreshold;
# uint16_t uiPlatformCfgPatch;
# uint8_t  uiPlatformCfgMinor;
# uint8_t  uiPlatformCfgMajor;
# char     platformCfg[8];
HEADER_FORMAT = "<IHHIII HBB 8s".replace(" ", "")
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "trace.bin"
    with open(path, "rb") as f:
        data = f.read(HEADER_SIZE)

    if len(data) < HEADER_SIZE:
        print(f"File too short: got {len(data)} bytes, need {HEADER_SIZE}")
        return

    (psf, version, platform, options, num_cores,
     isr_thresh, cfg_patch, cfg_minor, cfg_major, platform_cfg) = struct.unpack(HEADER_FORMAT, data)

    print(f"Header size (bytes):     {HEADER_SIZE}")
    print(f"uiPSF (magic):           0x{psf:08X}")
    print(f"uiVersion:               {version}")
    print(f"uiPlatform:              {platform}")
    print(f"uiOptions:               0x{options:08X}")
    print(f"uiNumCores:              {num_cores}")
    print(f"isrTailchainingThreshold:{isr_thresh}")
    print(f"platformCfg version:     {cfg_major}.{cfg_minor}.{cfg_patch}")
    print(f"platformCfg name:        {platform_cfg}")

if __name__ == "__main__":
    main()
