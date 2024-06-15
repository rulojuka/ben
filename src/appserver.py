from gevent import monkey
monkey.patch_all()

from bottle import Bottle, run, static_file, redirect

import json
import os
import argparse

from nn.models import Models
from bots import BotBid
from bidding import bidding
from sample import Sample
import conf
from bottle import response
from json import dumps
models = Models.from_conf(conf.load('./config/default.conf'),'..')   # loading neural networks
sampler = Sample.from_conf(conf.load('./config/default.conf'))  # Load sampling strategies
emptyAuction = []
verbose = True

app = Bottle()
os.getcwd()

parser = argparse.ArgumentParser(description="Appserver")
parser.add_argument("--host", default="localhost", help="Hostname for appserver")
parser.add_argument("--port", type=int, default=8082, help="Port for appserver")
parser.add_argument("--db", default="gamedb", help="Db for appserver")

args = parser.parse_args()

port = args.port
DB_NAME = os.getcwd() + "/" + args.db
print("Reading deals from: "+DB_NAME)

script_dir = os.path.dirname(os.path.abspath(__file__))

@app.route('/bid/<hand>')
def test(hand):
    bid = BotBid([False, False], hand, models, -1, -1, sampler, verbose).bid(emptyAuction)
    response.content_type = 'application/json'
    return dumps({ "bid": bid.bid, "candidates": bid.to_dict()['candidates'] })

host = args.host
print(f'http://{host}:{port}/home')

run(app, host=host, port=port, server='gevent', log=None)
