CXX=g++
CXXFLAGS=-std=c++11 

all: 
	$(MAKE) main -j $(nproc)

main: main.o JsonTrades.o Network.o JsonResponse.o
	$(CXX) $(CXXFLAGS) $^ -o bot

.PHONY: all main clean test_params

clean:
	rm -f *.o bot

remake:
	$(MAKE) -i clean 
	$(MAKE) all