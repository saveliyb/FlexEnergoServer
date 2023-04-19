from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
import os
import asyncio
import json
import VCG
from datetime import datetime
import logging


"""main server with VCG auction"""

app = FastAPI()

log_file = f'var/log/auction_logs_{datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}.txt'
with open(log_file, "w+") as file:
    file.close()
logging.basicConfig(filename=log_file, level=logging.INFO)

AuctionVCG = VCG.Auction(log_file=log_file)


@app.post("/add_bet_buy")
async def add_bet_buy(request: Request):
    """accepting buyers' bids from cupolas"""
    bet_ = await request.json()
    print(f"VCG принял лот {bet_['lot']} на покупку от Агента {bet_['user_id']} по цене {bet_['bet']}")
    if bet_["bet"] > 0:
        AuctionVCG.add_bet_buy(price=bet_["bet"], quantity=bet_["lot"], buyer=str(bet_["user_id"]))
    return "ok"


@app.post("/add_bet_sell")
async def add_bet_sell(request: Request):
    """accepting sellers' bids"""
    bet_ = await request.json()
    print(f"VCG принял лот {bet_['lot']} на продажу от Агента {bet_['user_id']} по цене {bet_['bet']}")
    if bet_["bet"] > 0:
        AuctionVCG.add_bet_sell(price=bet_["bet"], quantity=bet_["lot"], seller=str(bet_["user_id"]))
    return "ok"


result_vcg = {
    'user_id': [],
    'how': [],
    'price': [],
    'seller': []
}


@app.get("/get_VCG_result", response_class=HTMLResponse)
async def get_vcg_result():
    """output of vcg auction results"""
    global result_vcg
    string = AuctionVCG.result()
    if string != {
        "user_id": {},
        "how": {},
        "price": {},
        "seller": {}
    } and string != result_vcg:
        result_vcg = string
    if type(result_vcg) != str:
        result_vcg = json.dumps(result_vcg)
    return result_vcg


@app.get("/get_VCG_result_for_agent/{agent_id}")
async def get_VCG_result_for_agent(agent_id: str):
    agent_id = str(agent_id)
    lst_result = AuctionVCG.result()
    lst_lots_wanted = AuctionVCG.not_purchased_lots()
    lots_wanted = {}
    auc_result = {}
    for item in lst_result:
        buyer = item["buyer"]
        seller = item["seller"]
        quantity = item["quantity"]
        price = item["price"]
        if buyer not in auc_result:
            auc_result[buyer] = ["deals", {seller: {"quantity": quantity, "price": price}}]
        else:
            auc_result[buyer].append({seller: {"quantity": quantity, "price": price}})

    for item in lst_lots_wanted:
        seller = item["seller"]
        quantity = item["quantity"]
        lots_wanted[seller] = ["not_purchased", {"quantity": quantity, "price": 0}]
    try:
        if agent_id in auc_result.keys():
            return auc_result[agent_id]
        else:
            return lots_wanted[agent_id]
    except KeyError:
        return []


@app.get("/index")
async def index():
    print("ok")
    return {"Hello", "World!"}


async def loop():
    """auction cycle"""
    global result_vcg
    second = 20
    while True:
        await asyncio.sleep(second)
        AuctionVCG.vcg()
        string_ = AuctionVCG.result()
        if string_ != {'user_id': {}, 'how': {}, 'price': {}, 'seller': {}} and string_ != result_vcg \
                and string_ != {'user_id': [], 'how': [], 'price': [], 'seller': []}:
            result_vcg = string_
        try:
            print(result_vcg)
        except NameError:
            pass


if os.name == 'nt':
    """crutch for windows"""
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.gather(loop())
