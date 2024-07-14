# Makefile for c++ libraries
CC = g++
CFLAGS = -shared -fPIC
TARGET = ./lib/entropy.dll
SOURCE = ./lib/entropy.cpp

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(TARGET)