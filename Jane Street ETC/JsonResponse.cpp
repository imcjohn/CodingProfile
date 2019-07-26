//
// Created by juice on 7/13/2019.
//
#ifndef TEST_IAMBALLER2_JSONREPONSE_C
#define TEST_IAMBALLER2_JSONREPONSE_C
#include <iostream>
#include <string>
#include <vector>
#include <unistd.h>
#include "JsonResponse.h"

void JsonResponse::updateData(Connection *conn){
    std::string line = conn->read_from_exchange();
    rapidjson::Document document;
    document.Parse(line.c_str());
    rapidjson::Value &v = document["type"];
    const char *type = v.GetString();
    //std::cout << "TYPE IS " << type << std::endl;
    if (strcmp(type,"reject")== 0){
        v = document["error"];
        const char *error = v.GetString();
        if (strcmp(error,"TRADING_CLOSED") == 0){
            usleep(15000000); // after trading closes, exactly 15 seconds till new round so time restart correctly
            exit(0); // process is auto-bounced by runner
        }
    }
    else if (strcmp(type, "book") == 0){
        rapidjson::Value &sym = document["symbol"];
        std::string symbol(sym.GetString());
        if (symbol.compare("BOND") == 0)
            bondArbitrage(conn,line);
        if (symbol.compare("VALBZ") == 0)
            calculateMidValbz(conn,line);
        if(symbol.compare("VALE") == 0 && midflagADR){
            ADRArbitrage(conn, line);
        }
        if(symbol.compare("GS") == 0){
            calculateMidGS(conn, line);
        }
        if(symbol.compare("MS") == 0){
            calculateMidMS(conn, line);
        }
        if(symbol.compare("WFC") == 0){
            calculateMidWFC(conn, line);
        }
        if(symbol.compare("XLF") == 0 && midflagGS && midflagMS && midflagWFC){
            XLFArbitrage(conn, line);
        }

    }
}




std::string JsonResponse::XLFArbitrage(Connection* conn, std::string line){
    rapidjson::Document document;
    document.Parse(line.c_str());
    rapidjson::Value &sym = document["symbol"];
    std::string symbol(sym.GetString());
    //std::cout << line << std::endl;
    
    JsonTrades t;
    double midXLF = (3.0 * 1000.0 + 2.0 * midGS + 3.0 * midMS + 2.0 * midWFC) / 10.0;
    rapidjson::Value &v = document["buy"];

    if (v.IsArray()) {
        auto bids = v.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
             //std::cout << "PRICE_XLF:" << price << std::endl;
            if ((double)price < midXLF) {
                std::string res = t.add_buy("XLF", volume, price, this->m_current);
                this->m_current += 1;
                conn->send_to_exchange(res);
                //std::cout << "SEND" << std::endl;
            }
        }
    }

    rapidjson::Value &vv = document["sell"];
    if (vv.IsArray()) {
        auto bids = vv.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            if ( (double)price > midXLF) {
                std::string res = t.add_sell("XLF", volume, price, this->m_current);
                this->m_current += 1;
                conn->send_to_exchange(res);
                //std::cout << "SEND" << std::endl;
            }
        }
    }


    return "success";
};




int JsonResponse::getSharesFulfilled(int orderID){
    return orderLookupTable[orderID];
} // -1 means fully cleared, otherwise returns # of shares fulfilled


std::string JsonResponse::calculateMidGS(Connection* conn, std::string line){
    rapidjson::Document document;
    document.Parse(line.c_str());
    //std::cout << line << std::endl;
    rapidjson::Value &v = document["buy"];
    JsonTrades t;
    int bb = 0;
    int c = 0;
    if (v.IsArray()) {
        auto bids = v.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            bb += price;
            c += 1;
        }
    }
    double avg_bids = (double)bb/(double)c;

    rapidjson::Value &vv = document["sell"];
    if (v.IsArray()) {
        auto bids = v.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            bb += price;
            c += 1;
        }
    }
    double avg_ask = (double)bb/(double)c;

    midGS = (avg_bids + avg_ask) / 2.0;
    midflagGS = true;
    return "success";
};



std::string JsonResponse::calculateMidMS(Connection* conn, std::string line){
    rapidjson::Document document;
    document.Parse(line.c_str());
    //std::cout << line << std::endl;
    rapidjson::Value &v = document["buy"];
    JsonTrades t;
    int bb = 0;
    int c = 0;
    if (v.IsArray()) {
        auto bids = v.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            bb += price;
            c += 1;
        }
    }
    double avg_bids = (double)bb/(double)c;

    rapidjson::Value &vv = document["sell"];
    if (v.IsArray()) {
        auto bids = v.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            bb += price;
            c += 1;
        }
    }
    double avg_ask = (double)bb/(double)c;

    midMS = (avg_bids + avg_ask) / 2.0;
    midflagMS = true;
    return "success";
};


std::string JsonResponse::calculateMidWFC(Connection* conn, std::string line){
    rapidjson::Document document;
    document.Parse(line.c_str());
    //std::cout << line << std::endl;
    rapidjson::Value &v = document["buy"];
    JsonTrades t;
    int bb = 0;
    int c = 0;
    if (v.IsArray()) {
        auto bids = v.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            bb += price;
            c += 1;
        }
    }
    double avg_bids = (double)bb/(double)c;

    rapidjson::Value &vv = document["sell"];
    if (v.IsArray()) {
        auto bids = v.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            bb += price;
            c += 1;
        }
    }
    double avg_ask = (double)bb/(double)c;

    midWFC = (avg_bids + avg_ask) / 2.0;
    midflagWFC = true;
    return "success";
};



std::string JsonResponse::ADRArbitrage(Connection* conn, std::string line){
    rapidjson::Document document;
    document.Parse(line.c_str());
    rapidjson::Value &sym = document["symbol"];
    std::string symbol(sym.GetString());
    //std::cout << line << std::endl;
    
    JsonTrades t;

    rapidjson::Value &v = document["buy"];

    if (v.IsArray()) {
        auto bids = v.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
             //std::cout << "PRICE_VALE:" << price << std::endl;
            if ((double)price < midADR) {
                std::string res = t.add_buy("VALE", volume, price, this->m_current);
                this->m_current += 1;
                conn->send_to_exchange(res);
                //std::cout << "SEND" << std::endl;
            }
        }
    }

    rapidjson::Value &vv = document["sell"];
    if (vv.IsArray()) {
        auto bids = vv.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            if ( (double)price > midADR) {
                std::string res = t.add_sell("VALE", volume, price, this->m_current);
                this->m_current += 1;
                conn->send_to_exchange(res);
                //std::cout << "SEND" << std::endl;
            }
        }
    }


    return "success";
};

std::string JsonResponse::calculateMidValbz(Connection* conn, std::string line){
    rapidjson::Document document;
    document.Parse(line.c_str());
    //std::cout << line << std::endl;
    int thresh = 1000;
    rapidjson::Value &v = document["buy"];
    JsonTrades t;
    int bb = 0;
    int c = 0;
    if (v.IsArray()) {
        auto bids = v.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            bb += price;
            c += 1;
        }
    }
    double avg_bids = (double)bb/(double)c;

    rapidjson::Value &vv = document["sell"];
    if (v.IsArray()) {
        auto bids = v.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            bb += price;
            c += 1;
        }
    }
    double avg_ask = (double)bb/(double)c;

    midADR = (avg_bids + avg_ask) / 2.0;
    midflagADR = true;
    return "success";
};


std::string JsonResponse::bondArbitrage(Connection* conn, std::string line){
    rapidjson::Document document;
    document.Parse(line.c_str());
    //std::cout << line << std::endl;
    int thresh = 1000;
    rapidjson::Value &v = document["buy"];
    JsonTrades t;
    if (v.IsArray()) {
        auto bids = v.GetArray();
        for (auto &i : bids) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            //std::cout << "PRICEB:" << price << std::endl;
            if (price < thresh) {
                std::string res = t.add_buy("BOND", volume, price, this->m_current);
                this->m_current += 1;
                conn->send_to_exchange(res);
                //std::cout << "SEND" << std::endl;
            }

        }
    }
    rapidjson::Value &vv = document["sell"];
    if (vv.IsArray()) {
        auto asks = vv.GetArray();
        for (auto &i : asks) {
            int price = i[0].GetInt();
            int volume = i[1].GetInt();
            //std::cout << "PRICEA:" << price << std::endl;
            if (price > thresh) {
                std::string res = t.add_sell("BOND", volume, price, this->m_current);
                this->m_current += 1;
                conn->send_to_exchange(res);
                //std::cout << "SEND" << std::endl;
            }
        }
    }

    return "success";
};
#endif