from flask_classful import FlaskView, route
from flask import Flask, jsonify, request, render_template
from blockchain_utils import blockchain_utils
from interaction import mint_post
from account_model import account_model
import hashlib
from wallet_list import wallet_list
from cryptography.fernet import Fernet
import json
from valid_key import valid_key

global key
global f
key = Fernet.generate_key()
f = Fernet(key)
node = None

class node_api(FlaskView):
    
    def __init__(self):
        self.app = Flask(__name__)
        self.Account_model = account_model()
        
    def start(self, api_port):
        node_api.register(self.app, route_base="/")
        self.app.run(host="localhost", port=api_port)
        
    def inject_node(self, injected_node):
        global node
        node = injected_node
        global Valid_key
        Valid_key = valid_key(node.Wallet.public_key_string())
        
    @route("/info", methods=["GET"])
    def info(self):
        return "This is a communication interface to a nodes blockchain", 200
    
    @route("/blockchain", methods=["GET"])
    def blockchain(self):
        return node.Blockchain.toJson(), 200
    
    @route("/transaction_pool", methods=["GET"])
    def transaction_pool(self):
        transactions = {}
        for ctr, transaction in enumerate(node.Transaction_pool.transactions):
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200
    
    @route("/transaction", methods=["POST"])
    def transaction(self):
        values = request.get_json()
        if not "transaction" in values:
            return "Missing transaction value", 400
        transaction = blockchain_utils.decode(values["transaction"])
        node.handle_transaction(transaction)
        response = {"message": "Received transaction"}
        return jsonify(response), 201

        
    @route("/message", methods = ["POST", "GET"])
    def message(self):
        transaction_from = request.remote_addr
        node_address = str(request.url_root)
        this_node = transaction_from.replace("localhost:", "node")
        form_data = request.form
        form_value = form_data["Message"]
        data_in_bytes = json.dumps(form_value).encode('utf-8')
        global encrypted_data
        encrypted_data = f.encrypt(data_in_bytes)
        mint_post(node.Wallet, node.Wallet, "POST", 1, encrypted_data.decode("utf-8"))
        return render_template('message.html', form_value=form_value, node=this_node, node_address=node_address)
    
    @route("/messages", methods=["GET"])
    def messages(self):
        posts = {}
        feed = node.Blockchain.toJson()
        for values in feed.values():
            for dics in values:
                post_id = []
                for value in dics.values():
                    if type(value) is list:
                        for x in value:
                            for i in x.keys():
                                if i == "data":
                                    encrypted_post = x["data"]
                                    decrypted_post = f.decrypt((encrypted_post.encode("utf-8")))
                                    post_dict = decrypted_post.decode("utf-8")
                                    block_count = dics["block_count"]
                                    signature = x["id"]
                                    #sender_hash = hashlib.sha256(((x["sender_public_key"]).encode("utf-8"))).hexdigest()
                                    sender = "Me"
                                    post_id.extend([("From: " + str(sender)), ("Minted on Block: " + str(block_count)), ("Post ID: " + str(signature))])
                                    posts[post_dict] = post_id
        return render_template("messages.html", posts=posts)
    
    @route("/minting", methods=["GET"])
    def minting(self):
        return render_template("minting.html")
    
    @route("/iskeyvalid", methods=["GET"])
    def iskeyvalid(self):
        return str(Valid_key.is_key_valid(node.Wallet.public_key_string()))
                        
                    