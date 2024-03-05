# Makefile for c++ libraries
CC = g++
CFLAGS = -shared -fPIC
TARGET1 = ./cpplib/DispSampEn2D.dll
SOURCE1 = ./cpplib/DispSampEn2D.cpp
TARGET2 = ./cpplib/SampEn2D.dll
SOURCE2 = ./cpplib/SampEn2D.cpp
TARGET3 = ./cpplib/DispEn2D.dll
SOURCE3 = ./cpplib/DispEn2D.cpp

all: $(TARGET1) $(TARGET2) $(TARGET3) $(TARGET4) $(TARGET5)

$(TARGET1): $(SOURCE1)
	$(CC) $(CFLAGS) -o $@ $^

$(TARGET2): $(SOURCE2)
	$(CC) $(CFLAGS) -o $@ $^

$(TARGET3): $(SOURCE3)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(TARGET1) $(TARGET2) $(TARGET3)