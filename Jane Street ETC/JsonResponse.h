//
// Created by juice on 7/13/2019.
//

#ifndef TEST_IAMBALLER2_JSONREPONSE_H
#define TEST_IAMBALLER2_JSONREPONSE_H
#include <vector>
#include <map>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include "JsonTrades.h"
#include "Network.h"

class JsonResponse {
private:
    int cur_bought = 0;
    int cur_sell =0;
    int m_current = 0;

    double midADR = 0.0;
    bool midflagADR = false;

    double midGS = 0.0;
    bool midflagGS = false;

    double midMS = 0.0;
    bool midflagMS = false;

    double midWFC = 0.0;
    bool midflagWFC = false;



    const float decay = 0.5;
    std::map<int, int> orderLookupTable;
    std::map<std::string, float> latestEMA;
    std::string bondArbitrage(Connection* conn, std::string line);
    std::string ADRArbitrage(Connection* conn, std::string line);
    std::string calculateMidValbz(Connection* conn, std::string line);
    
    std::string XLFArbitrage(Connection* conn, std::string line);
    std::string calculateMidMS(Connection* conn, std::string line);
    std::string calculateMidGS(Connection* conn, std::string line);
    std::string calculateMidWFC(Connection* conn, std::string line);
    

public:
    //JsonTrades();
    void updateData(Connection *conn);

    std::map<std::string, std::vector<rapidjson::Value>> bidHistory;
    std::map<std::string, std::vector<rapidjson::Value>> askHistory;

    int getSharesFulfilled(int orderID);
};
#endif //TEST_IAMBALLER2_JSONREPONSE_H
