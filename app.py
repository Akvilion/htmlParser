from flask import Flask, request, make_response, jsonify
from parserHandler import Parser
import pandas as pd
import customExeptions as cex


app = Flask(__name__)


@app.route("/", methods=["GET"])
def parser():

    url: str = request.args.get("url", "")
    if url:
        try:
            parser = Parser(url)
            csv_data = parser.csvFile()
        except cex.ParserExeption:
            return jsonify({"exeption": "Something wrong with Parser"}), 200
        except cex.ConvertToCSVExeption:
            return jsonify({"exeption": "Something wrong with CSV converter"}), 200
        except cex.RequestExeption:
            return jsonify({"exeption": "Something wrong with URL request"}), 200
        except:
            return jsonify({"exeption": "Something go wrong completely"}), 200
        else:
            response = make_response(csv_data)
            response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
            response.headers['Content-Type'] = 'text/csv'
            return response  
    else:
        return jsonify({"URL is needed": "plese specify URL"})


if __name__ == "__main__":
    app.run(debug=True)
