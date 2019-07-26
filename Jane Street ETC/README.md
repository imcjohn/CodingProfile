#Jane Street Electronic Trading Competition Code
## Trading bot created at the Jane Street ETC by me and my two teammates, written in C++.

## Descriptions by file
* JsonResponse.cpp/h - Class to handle responses from server and do appropriate trading responses. JSON parsing and framework written by me, but most of the ideas for the algorithms came from my teammates and the writeup from Jane Street
* JsonTrades.cpp/h - Class to appropriately encapsulate messages back to server. Written by me.
* Network.cpp/h - Class wrapper around the network communication code provided to us by Jane Street.
* main.cpp - Basic runner to tie the appropriate classes together
 