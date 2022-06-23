@route("/feed", methods=["GET"])
def feed(self):
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
                                post = x["data"]["Post"]
                                block_count = dics["block_count"]
                                signature = x["id"]
                                sender_hash = hashlib.sha256(((x["sender_public_key"]).encode("utf-8"))).hexdigest()
                                sender = wallet_list[str(sender_hash)]
                                post_id.extend([("From: " + str(sender)), ("Minted on Block: " + str(block_count)), ("Post ID: " + str(signature))])
                                posts[post] = post_id
    return render_template("feed.html", posts=posts)
