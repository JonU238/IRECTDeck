import math
from collections import namedtuple
LoraSettings = namedtuple("LoraSettings", ["SF", "BW", "CR", "PreambleSize", "CrcOn", "ImplicitHeader", "LDR", "MaxSize"])
# Source: https://github.com/ifTNT/lora-air-time

def n_symbol(payload_len: int, settings: LoraSettings):
    payload_bits = 8 * payload_len
    payload_bits -= settings.SF * 4
    payload_bits += 8
    if settings.CrcOn:
        payload_bits+=16

    if settings.ImplicitHeader:
        payload_bits+=16
    payload_bits = max(payload_bits, 0)

    bits_per_symbol = settings.SF
    if settings.LDR:
        bits_per_symbol -= 2
    payload_symbol = math.ceil(payload_bits / 4 / bits_per_symbol) * settings.CR;
    payload_symbol += 8;

    preamble_symbols = settings.PreambleSize+4.25 
    return payload_symbol, preamble_symbols 


def airtimeOne(payload_len: int, settings: LoraSettings) -> float:
    if payload_len > 255:
        raise ValueError("Max packet size = 255")
    T_s = (2**settings.SF)/settings.BW
    n_sym, n_pre = n_symbol(payload_len, settings)
    return T_s * (n_sym + n_pre)


def airtime(payload_len: int, settings: LoraSettings) -> float:
    repeated = payload_len // settings.MaxSize
    remainder = payload_len % settings.MaxSize
    return repeated * airtimeOne(settings.MaxSize, settings) + airtimeOne(remainder, settings)

settings = LoraSettings(
    SF=12,                # Spreading Factor
    BW=500,              # Bandwidth in Hz
    CR=8,                # Coding Rate
    PreambleSize=8,      # Preamble size in symbols
    CrcOn=True,          # CRC enabled
    ImplicitHeader=False,# Explicit header mode
    LDR=False,           # Low Data Rate optimization
    MaxSize=255          # Max payload size
)

print(airtimeOne(21,settings))