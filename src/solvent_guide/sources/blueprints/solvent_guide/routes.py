import json
import os
from typing import Optional

import pandas as pd
import plotly
import plotly.express as px
from flask import Response, render_template, jsonify, request


from . import solvent_guide_bp


def get_radar_plot(s: str, h: str, e: str) -> str:
    df = pd.DataFrame(dict(r=[s, h, e], theta=["S", "H", "E"]))
    fig = px.line_polar(df, r="r", theta="theta", line_close=True, range_r=[0, 10])
    fig.update_traces(fill="toself")
    fig.update_xaxes(range=[0, 5])
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig.update_layout(height=250, width=250)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@solvent_guide_bp.route("/", methods=["GET", "POST"])
@solvent_guide_bp.route("/solvent_guide/<sol>", methods=["GET", "POST"])
def solvent_guide(sol: Optional[str] = None) -> Response:
    try:
        CHEM21 = pd.read_csv(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "CHEM21_full_updated.csv"), dtype={'Number': 'Int64'}
        )
    except FileNotFoundError:
        CHEM21 = pd.read_csv(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "CHEM21_full.csv")
        )

    CHEM21 = CHEM21.sort_values(by="Family")
    CHEM21 = CHEM21.sort_values(by="Solvent")
    CHEM21 = CHEM21.fillna("")
    solvents = CHEM21.to_dict("index")
    solvents = list(solvents.values())
    families = sorted(list(set(CHEM21["Family"].tolist())))

    # if from reaction table and a solvent was selected
    if sol:
        if sol not in CHEM21["Solvent Alternative Name"].tolist():
            sol = None
        else:
            sol = CHEM21[CHEM21["Solvent Alternative Name"] == sol]["Number"].tolist()[
                0
            ]
    return render_template(
        "solvent_guide.html",
        solvents=solvents,
        families=families,
        sol=sol,
    )


@solvent_guide_bp.route("/solvent_guide_help", methods=["GET", "POST"])
def solvent_guide_help() -> Response:

    return render_template(
        "solvent_guide_help.html",
        graphJSON=[get_radar_plot(8, 3, 5)],
    )


@solvent_guide_bp.route("/get_custom_colours", methods=["GET", "POST"])
def get_custom_colours() -> Response:

    try:
        colours = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_colours.txt")))

    except FileNotFoundError:
        colours = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "default_colours.txt")))

    return jsonify({"colours": colours})


@solvent_guide_bp.route("/change_hazard_colours", methods=["GET", "POST"])
def change_hazard_colours():

    if request.form["mode"] == "update":
        updated_dict = {
            "Recommended": request.form["Recommended"],
            "Problematic": request.form["Problematic"],
            "Hazardous": request.form["Hazardous"],
            "HighlyHazardous": request.form["HighlyHazardous"],
            "Recommended_text": request.form["Recommended_text"],
            "Problematic_text": request.form["Problematic_text"],
            "Hazardous_text": request.form["Hazardous_text"],
            "HighlyHazardous_text": request.form["HighlyHazardous_text"]
        }

        with open(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_colours.txt"), 'w'
        ) as f:

            f.write(json.dumps(updated_dict))

        return jsonify({"message": "Hazard colours were successfully updated!"})

    else:
        try:
            os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_colours.txt"))

        except FileNotFoundError:
            return jsonify({"message": "Hazard colours were reverted to the default!"})

        return jsonify({"message": "Hazard colours were reverted to the default!"})


@solvent_guide_bp.route("/accessibility", methods=["GET", "POST"])
def accessibility() -> Response:

    return render_template(
        "accessibility.html"
    )

