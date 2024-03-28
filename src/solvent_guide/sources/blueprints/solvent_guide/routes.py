import json
import os
from typing import Optional

import pandas as pd
import plotly
import plotly.express as px
import pubchempy as pcp
from pubchemprops.pubchemprops import get_second_layer_props
from flask import Response, render_template, jsonify, request
from .CHEM21_calculator import CHEM21Calculator


from . import solvent_guide_bp


def get_radar_plot(s: int, h: int, e: int) -> str:
    df = pd.DataFrame(dict(r=[s, h, e], theta=["S", "H", "E"]))
    fig = px.line_polar(df, r="r", theta="theta", line_close=True, range_r=[0, 10])
    fig.update_traces(fill="toself")
    fig.update_xaxes(range=[0, 5])
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig.update_layout(height=250, width=250)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def read_chem21():
    try:
        CHEM21 = pd.read_csv(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "CHEM21_full_updated.csv"),
            index_col=0
        )
    except FileNotFoundError:
        CHEM21 = pd.read_csv(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "CHEM21_full.csv"), index_col=0
        )
    return CHEM21

@solvent_guide_bp.route("/", methods=["GET", "POST"])
@solvent_guide_bp.route("/solvent_guide/<sol>", methods=["GET", "POST"])
def solvent_guide(sol: Optional[str] = None) -> Response:

    CHEM21 = read_chem21()

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

@solvent_guide_bp.route("/new_solvent", methods = ["GET", "POST"])
def new_solvent() -> Response:

    return render_template(
        "new_solvent.html"
    )

@solvent_guide_bp.route("/add_solvent", methods = ["GET", "POST"])
def add_solvent() -> Response:
    data = request.get_json()
    cas_number = data['cas_number']
    value_dict = {}
    get_pubchemid = pcp.get_cids(cas_number)
    get_props = get_second_layer_props(cas_number, ['Boiling Point', 'Flash Point'])
    for key, val in get_props.items():
        for i in val:
            if 'Value' in i.keys():
                den_value = i['Value']
                if 'StringWithMarkup' in den_value.keys():
                    string_dict = den_value['StringWithMarkup'][0]
                    if 'String' in string_dict.keys():
                        if key in ['Boiling Point', 'Flash Point']:
                            if '°C' in string_dict['String']:
                                value_dict[key] = string_dict['String']
    print(value_dict)
    _example_flashcard = render_template("_example_flashcard.html")
    return json.dumps({'example_flashcard':_example_flashcard})


@solvent_guide_bp.route("/save_flashcard", methods = ["GET", "POST"])
def save_flashcard() -> Response:
    data = request.get_json()
    dict_variable = {key.replace('-', ' '): value for (key, value) in data.items()}
    dict_variable['graph'] = get_radar_plot(int(dict_variable['Safety']), int(dict_variable['Health']), int(dict_variable['Env']))
    CHEM21 = read_chem21()
    dict_variable['Number'] = max(CHEM21['Number']) + 1
    df = pd.DataFrame(dict_variable, index=[0])
    updated_chem21 = pd.concat([CHEM21, df])
    updated_chem21 = updated_chem21.reset_index(drop=True)
    updated_chem21.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "CHEM21_full_updated.csv"))
    return jsonify('success')


@solvent_guide_bp.route("/CHEM21", methods = ["GET", "POST"])
def CHEM21() -> Response:


    return render_template(
        "CHEM21.html"
    )


@solvent_guide_bp.route("/CHEM21_calculator", methods = ["GET", "POST"])
def CHEM21_calculator() -> Response:
    data = request.get_json()
    converted_data = {key: (float(value) if value != '' and type(value) != bool else 0) for (key, value) in data.items()}
    x = CHEM21Calculator(flash_point=converted_data['FP'], boiling_point=converted_data['BP'], ignition_temp=converted_data['IT'], hazard_codes=data['Hazard_codes'],
                         peroxability=data['peroxability'], resistivity=['resistivity'], reach=['reach'])

    return json.dumps(x.calculate_all())









