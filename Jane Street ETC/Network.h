//
// Created by juice on 7/13/2019.
//

#ifndef NETWORK_H
#define NETWORK_H
/* C includes for networking things */
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

/* C++ includes */
#include <string>
#include <iostream>
#include <stdexcept>
#include <algorithm>
#include <vector>
#include <sstream>

/* The Configuration class is used to tell the bot how to connect
   to the appropriate exchange. The `test_exchange_index` variable
   only changes the Configuration when `test_mode` is set to `true`.
*/
class Configuration {
private:
    /*
      0 = prod-like
      1 = slower
      2 = empty
    */
    static int const test_exchange_index = 0;
public:
    std::string team_name;
    std::string exchange_hostname;
    int exchange_port;
    /* replace REPLACEME with your team name! */
    Configuration(bool test_mode);
};

/* Connection establishes a read/write connection to the exchange,
   and facilitates communication with it */
class Connection {
private:
    FILE * in;
    FILE * out;
    int socket_fd;
public:
    Connection(Configuration configuration);

    /** Send a string to the server */
    void send_to_exchange(std::string input);

    /** Read a line from the server, dropping the newline at the end */
    std::string read_from_exchange();
};

#endif