CC      := gcc
CXX     := g++
JAVAC   := javac

CFLAGS   := -Wall -lpthread
CXXFLAGS := -Wall -std=c++11
JFLAGS   :=

SRCS_C    := $(wildcard *.c)
SRCS_CPP  := $(wildcard *.cpp)
SRCS_JAVA := $(wildcard *.java)

BINS_C     := $(SRCS_C:%.c=%)
BINS_CPP   := $(SRCS_CPP:%.cpp=%)
CLASSES    := $(SRCS_JAVA:%.java=%.class)

all: c_targets cpp_targets java_targets

c_targets: $(BINS_C)
%: %.c
	$(CC) $(CFLAGS) $< -o $@

cpp_targets: $(BINS_CPP)
%: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

java_targets: $(CLASSES)
%.class: %.java
	$(JAVAC) $(JFLAGS) $<

clean:
	rm -rf $(BINS_C) $(BINS_CPP) *.class

rebuild: clean all

.PHONY: all clean rebuild