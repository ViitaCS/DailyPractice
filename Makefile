# 编译器定义
CC      := gcc
CXX     := g++
JAVAC   := javac

# 编译选项
CFLAGS   := -Wall -lpthread
CXXFLAGS := -Wall -std=c++11
JFLAGS   := 

# 源文件自动检测
SRCS_C    := $(wildcard *.c)
SRCS_CPP  := $(wildcard *.cpp)
SRCS_JAVA := $(wildcard *.java)

# 生成目标定义
BINS_C     := $(SRCS_C:%.c=%)
BINS_CPP   := $(SRCS_CPP:%.cpp=%)
CLASSES    := $(SRCS_JAVA:%.java=%.class)

# 统一构建目标
all: c_targets cpp_targets java_targets

# ------ C语言规则 ------
c_targets: $(BINS_C)
%: %.c
	$(CC) $(CFLAGS) $< -o $@

# ------ C++规则 ------
cpp_targets: $(BINS_CPP)
%: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

# ------ Java规则 ------
java_targets: $(CLASSES)
%.class: %.java
	$(JAVAC) $(JFLAGS) $<

# 清理所有生成文件
clean:
	rm -rf $(BINS_C) $(BINS_CPP) *.class

# 强制重新构建
rebuild: clean all

.PHONY: all clean rebuild