//
// Created by juice on 7/12/2019.
//

#include "JsonTrades.h"
#ifndef TEST_IAMBALLER2_JSONTRADES_CPP
#define TEST_IAMBALLER2_JSONTRADES_CPP
void JsonTrades::send_msg(const char * msg) {
    std::cout << "YEET" << msg << std::endl;
}

char * JsonTrades::recv_msg() {
    return "hi";
}

std::string JsonTrades::gen_order(const char * symbol, const char * type, int t_len, const char * dir, int dir_len,
        double quantity, double price, long long int orderid)
{
    rapidjson::Document d;
    d.SetObject();
    // add value
    rapidjson::Value type_val(type,t_len);
    d.AddMember("type",type_val,d.GetAllocator());
    // add order id
    auto order_id = (int64_t) orderid;
    rapidjson::Value oid_val(order_id);
    d.AddMember("order_id",oid_val,d.GetAllocator());
    // add symbol
    rapidjson::Value symbol_value(symbol,strlen(symbol));
    d.AddMember("symbol",symbol_value,d.GetAllocator());
    // add dir
    rapidjson::Value dir_value(dir,dir_len);
    d.AddMember("dir",dir_value,d.GetAllocator());
    // add quantity
    rapidjson::Value quantity_value((int)quantity);
    d.AddMember("size",quantity_value,d.GetAllocator());
    // add price
    rapidjson::Value price_value((int)price);
    d.AddMember("price",price_value,d.GetAllocator());
    rapidjson::StringBuffer buffer;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
    d.Accept(writer);
    const char * output = buffer.GetString();
    std::string out(output);
    return out;
}

std::string JsonTrades::add_buy(const char * symbol, double quantity, double price, long long int orderid){
    return gen_order(symbol,"add",3,"BUY",3,quantity, price, orderid);
}

std::string JsonTrades::add_sell(const char * symbol, double quantity, double price, long long int orderid){
    return gen_order(symbol,"add",3,"SELL",4,quantity,price, orderid);
}

std::string JsonTrades::convert_sell(const char * symbol, double quantity, double price, long long int orderid){
    return gen_order(symbol,"convert",7,"SELL",4,quantity,price, orderid);
}

std::string JsonTrades::convert_buy(const char * symbol, double quantity, double price, long long int orderid){
    return gen_order(symbol,"convert",7,"BUY",3,quantity,price, orderid);
}

#endif