# Questions

## What's `stdint.h`?

It is header file where described additional extended integer types with certain exact widths

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

Guaranteed number of bits in variable in any platforms

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE - 8 bits
DWORD - 32 bits
LONG - 32 bits (one of them sign bit)
WORD - 16 bits

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

1st - 0xff, 2nd - 0xd8

## What's the difference between `bfSize` and `biSize`?

bfSize - The size of the BMP file in bytes
biSize = The size of this (BITMAPINFOHEADER) header

## What does it mean if `biHeight` is negative?

If biHeight is negative, the bitmap is a top-down with the origin at the upper left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

Because system probably may not open file due output file not exist, device is full
or program has not permission for required disc operation.

## Why is the third argument to `fread` always `1` in our code?

Because program read only one structure at one operation.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

Sets read / write pointer in file.

## What is `SEEK_CUR`?

It is constant which represent current position in file as base for offset.

## Whodunit?

It was professor Plum with the candlestick in the library.