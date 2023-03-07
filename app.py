from flask import Flask, request, make_response
from handler import Parser
import pandas as pd


app = Flask(__name__)


@app.route("/", methods=["GET"])
def parser():


    # url: str = request.args.get("url", "")
    url = "https://ru.wikipedia.org/wiki/%D0%A2%D1%83-160"
    
    a = Parser(url)
    csv_data = a.csvFile()
    # header, links, paragraphs, lang = a.xxx()
    # df = pd.DataFrame({'URL': pd.Series(url), 'Header': pd.Series(header), 'Paragraph': pd.Series(paragraphs), 'Links': pd.Series(links), 'Language': pd.Series(lang)})
    # csv_data = df.to_csv(index=False)
    response = make_response(csv_data)

    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response


if __name__ == "__main__":
    app.run(debug=True)
