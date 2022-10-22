from flask import (
    Flask,
    render_template,
    request,
)
import wiring_rs

app = Flask(__name__)


def identity(x):
    res = str(x)
    return res


def ldtab_2_man(x):
    ofn = wiring_rs.ldtab_2_ofn(x)
    man = wiring_rs.ofn_2_man(ofn)
    return man


def get_translation(input_format, out_format):
    if input_format == "OFN":
        if out_format == "LDTab":
            return wiring_rs.ofn_2_ldtab
        if out_format == "Manchester":
            return wiring_rs.ofn_2_man
        if out_format == "OFN":
            return identity

    if input_format == "LDTab":
        if out_format == "OFN":
            return wiring_rs.ldtab_2_ofn
        if out_format == "Manchester":
            return ldtab_2_man
        if out_format == "LDTab":
            return identity

    return "error"


# we could store changes in a data base - do we want to
@app.route("/", methods=["POST", "GET"])
def index():

    # input_formats = ["LDTab", "OFN", "RDFXML", "Turtle", "N-Triples"]
    input_formats = ["LDTab", "OFN"]

    output_formats = [
        "LDTab",
        "OFN",
        "Manchester",
    ]

    if request.method == "POST":

        if "translate" in request.form:

            # get input graph from form
            input = request.form["input"]

            select = request.form.get("in_select")
            in_format = str(select)

            select = request.form.get("out_select")
            out_format = str(select)

            # get format conversion function
            translate = get_translation(in_format, out_format)

            # translate input line by line (so there is no support for typing)
            res = ""
            for a in input.splitlines():
                translation = translate(a)
                res += translation + "\n"

            # TODO: parse input as lines
            # TODO: parse input to output conversion
            # TODO: translate input with wiring
            # TODO: put translation into output window

        return render_template(
            "index.html",
            # inputWiring=in_format,
            outputWiring=res,
            input_formats=input_formats,
            output_formats=output_formats,
        )

    else:

        # return render_template("index.html", examples=examples)
        return render_template(
            "index.html",
            input_formats=input_formats,
            output_formats=output_formats,
        )


if __name__ == "__main__":
    app.run(debug=True)