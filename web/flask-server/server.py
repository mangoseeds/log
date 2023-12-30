from flask import Flask

app = Flask(__name__)

# EXAMPLE Names API Route
@app.route("/names")
def names():
	return {"names": ["정지혜", "김희진", "배주연"]}

if __name__ == "__main__":
	app.run(debug=True)