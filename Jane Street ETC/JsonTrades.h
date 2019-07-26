//
// Created by juice on 7/12/2019.
//

#ifndef TEST_IAMBALLER2_JSONTRADES_H
#define TEST_IAMBALLER2_JSONTRADES_H
#include <chrono>
#include <iostream>
#include <string>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"

class JsonTrades {
private:
    char * recv_msg();
    std::string gen_order(const char * symbol, const char * type, int t_len, const char * dir, int dir_len,
                           double quantity, double price, long long int orderid);
    void send_msg(const char * msg);
public:
    std::string add_sell(const char * symbol, double quantity, double price, long long int orderid);
    std::string add_buy(const char * symbol, double quantity, double price, long long int orderid);
    std::string convert_sell(const char * symbol, double quantity, double price, long long int orderid);
    std::string convert_buy(const char * symbol, double quantity, double price, long long int orderid);
};


#endif //TEST_IAMBALLER2_JSONTRADES_H
