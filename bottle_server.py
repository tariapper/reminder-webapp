import bottle

@bottle.route("/")
def htmlLoad():
    return bottle.static_file("templates/index.html", root=".")


if __name__ == "__main__":
    bottle.run(host="0.0.0.0",port=5000,debug=True)