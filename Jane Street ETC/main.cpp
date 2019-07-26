// rapidjson/example/simpledom/s   impledom.cpp`
// g++ IDDistributor.h main.cpp RawTrades.cpp
#include <iostream>
#include <string>
#include "IDDistributor.h"
#include "JsonTrades.h"
#include "Network.h"
#include "JsonResponse.h"
int main(int argc, char *argv[])
{
    // Be very careful with this boolean! It switches between test and prod
    bool test_mode = false;
    Configuration config(test_mode);
    // Connection conn(config);
    Connection* conn = new Connection(config);
    std::string data("{\"type\": \"hello\", \"team\": \"TEAMNAME\"}");
    std::cout << data << std::endl;
    conn->send_to_exchange(data);
    std::string line = conn->read_from_exchange();
    std::cout << "The exchange replied: " << line << std::endl;
    // Initialize objects for helping comms
    JsonTrades t;
    JsonResponse* r = new JsonResponse();

    //BondArbitrage bonds(0,10000);
    while (true){
        r->updateData(conn);
        //bonds.run(conn, r);

        // int cur = (int)r.getCurrentAsk("BOND");
        // if (cur != prev) {
        //     std::cout << "bond value is " << << std::endl;
        //     prev = cur;
        // }
    }
    return 0;
}
