from flask import (
    Flask,
    render_template,
    request,
)
import wiring_rs
import ldtab_rs

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
    input_formats = ["LDTab", "OFN", "RDFXML"]

    output_formats = [
        "LDTab",
        "OFN",
        "Manchester",
    ]

    if request.method == "POST":

        previous_in_format = request.form["in_select"]
        previous_out_format = request.form["out_select"]
        # {"selected_item": "team_polo"}

        if "switch" in request.form:
            input = request.form["input"]
            output = request.form["output"]

            return render_template(
                "index.html",
                inputWiring=output,
                outputWiring=input,
                previous_in_format=previous_in_format,
                previous_out_format=previous_out_format,
                input_formats=input_formats,
                output_formats=output_formats,
            )

        if "translate" in request.form:

            # get input graph from form
            input = request.form["input"]

            select = request.form.get("in_select")
            in_format = str(select)

            select = request.form.get("out_select")
            out_format = str(select)

            # RDFXML write to tmp file
            if in_format == "RDFXML":
                f = open("tmp/ont.owl", "w")
                f.write(input)
                f.close()

                # RDFXML -> LDTab
                triples = ldtab_rs.import_thick_triples("tmp/ont.owl")

                # TODO translate here?
                translate = get_translation("LDTab", out_format)

                res = ""
                for t in triples:
                    translation = translate(t)
                    res += translation + "\n"

            else:

                # get format conversion function
                translate = get_translation(in_format, out_format)

                # translate input line by line (so there is no support for typing)
                res = ""
                for a in input.splitlines():
                    translation = translate(a)
                    res += translation + "\n"

        return render_template(
            "index.html",
            inputWiring=input,
            outputWiring=res,
            previous_in_format=previous_in_format,
            previous_out_format=previous_out_format,
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
