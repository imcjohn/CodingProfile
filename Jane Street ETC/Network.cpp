#include "Network.h"

    Configuration::Configuration(bool test_mode) : team_name("TEAMNAME"){
        //exchange_port = 20000; /* Default text based port */
        exchange_port = 25000; // json port
        if(true == test_mode) {
            exchange_hostname = "test-exch-" + team_name;
            exchange_port += test_exchange_index;
        } else {
            exchange_hostname = "production";
        }
    }

    Connection::Connection(Configuration configuration){
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) {
            throw std::runtime_error("Could not create socket");
        }
        std::string hostname = configuration.exchange_hostname;
        hostent *record = gethostbyname(hostname.c_str());
        if(!record) {
            throw std::invalid_argument("Could not resolve host '" + hostname + "'");
        }
        in_addr *address = reinterpret_cast<in_addr *>(record->h_addr);
        std::string ip_address = inet_ntoa(*address);
        struct sockaddr_in server;
        server.sin_addr.s_addr = inet_addr(ip_address.c_str());
        server.sin_family = AF_INET;
        server.sin_port = htons(configuration.exchange_port);

        int res = connect(sock, ((struct sockaddr *) &server), sizeof(server));
        if (res < 0) {
            throw std::runtime_error("could not connect");
        }
        FILE *exchange_in = fdopen(sock, "r");
        if (exchange_in == NULL){
            throw std::runtime_error("could not open socket for writing");
        }
        FILE *exchange_out = fdopen(sock, "w");
        if (exchange_out == NULL){
            throw std::runtime_error("could not open socket for reading");
        }

        setlinebuf(exchange_in);
        setlinebuf(exchange_out);
        this->in = exchange_in;
        this->out = exchange_out;
        this->socket_fd = res;
    }

    /** Send a string to the server */
    void Connection::send_to_exchange(std::string input) {
        std::string line(input);
        /* All messages must always be uppercase */
        //std::transform(line.begin(), line.end(), line.begin(), ::toupper);
        int res = fprintf(this->out, "%s\n", line.c_str());
        if (res < 0) {
            throw std::runtime_error("error sending to exchange");
        }
    }

    /** Read a line from the server, dropping the newline at the end */
    std::string Connection::read_from_exchange()
    {
        /* We assume that no message from the exchange is longer
           than 10,000 chars */
        const size_t len = 10000;
        char buf[len];
        if(!fgets(buf, len, this->in)){
            throw std::runtime_error("reading line from socket");
        }

        int read_length = strlen(buf);
        std::string result(buf);
        /* Chop off the newline */
        result.resize(result.length() - 1);
        return result;
    }

std::string join(std::string sep, std::vector<std::string> strs) {
    std::ostringstream stream;
    const int size = strs.size();
    for(int i = 0; i < size; ++i) {
        stream << strs[i];
        if(i != (strs.size() - 1)) {
            stream << sep;
        }
    }
    return stream.str();
}
