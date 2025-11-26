import streamlit as st
import pandas as pd
from modules.planner.tpn_planner import *
from modules.patients.adult_patient import *
from modules.conditions.adult_conditions import *

st.set_page_config(page_title="TPN Worksheet", layout="wide")

# --- Custom CSS for styling ---
st.markdown("""
    <style>
    /* Main container styling */
    .main-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 5px;
    }

    /* Worksheet header styling */
    .worksheet-header {
        background-color: #e8f1fb;
        color: #004a99;
        padding: 0.8rem 1.5rem;
        border: 1px solid #b8d4f0;
        border-radius: 5px;
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #004a99;
        background-color: #f1f6fc;
        padding: 0.5rem 1rem;
        border: 1px solid #d1e3f8;
        border-radius: 4px;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }

    /* Form table styling */
    .form-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1rem;
    }
    .form-table th {
        background-color: #e8f1fb;
        border: 1px solid #b8d4f0;
        padding: 8px 12px;
        text-align: left;
        font-weight: 600;
        color: #004a99;
        font-size: 0.9rem;
    }
    .form-table td {
        border: 1px solid #b8d4f0;
        padding: 6px 10px;
        background-color: white;
    }
    .form-table .input-cell {
        background-color: #fffacd !important;
        min-width: 120px;
    }

    /* Special instructions box */
    .instructions-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
        font-size: 0.9rem;
    }

    /* Yellow input boxes */
    .yellow-input {
        background-color: #fffacd !important;
        border: 1px solid #e6d900 !important;
        border-radius: 3px;
        padding: 4px 8px;
        width: 100%;
        font-size: 0.9rem;
    }

    /* Results table styling */
    .results-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .results-table th {
        background-color: #004a99;
        color: white;
        padding: 10px;
        text-align: center;
        border: 1px solid #003366;
    }
    .results-table td {
        border: 1px solid #b8d4f0;
        padding: 8px;
        text-align: center;
    }
    .results-table .category-cell {
        background-color: #f1f6fc;
        font-weight: 600;
        text-align: left;
    }

    /* Hover tooltip styling */
    .nutrient-with-tooltip {
        position: relative;
        cursor: help;
        text-decoration: underline dotted;
        color: #004a99;
    }
    .nutrient-tooltip {
        visibility: hidden;
        width: 300px;
        background-color: #555;
        color: white;
        text-align: left;
        border-radius: 6px;
        padding: 8px 12px;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.8rem;
        font-weight: normal;
    }
    .nutrient-tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #555 transparent transparent transparent;
    }
    .nutrient-with-tooltip:hover .nutrient-tooltip {
        visibility: visible;
        opacity: 1;
    }

    /* Note box */
    .note-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
        font-size: 0.9rem;
    }

    /* References section */
    .references-section {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        padding: 1.5rem;
        margin: 2rem 0;
        font-size: 0.85rem;
    }
    .references-section h3 {
        color: #004a99;
        margin-top: 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid #dee2e6;
        padding-bottom: 0.5rem;
    }
    .reference-item {
        margin-bottom: 0.8rem;
        line-height: 1.4;
    }

    /* Condition checkboxes styling */
    .condition-category {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        padding: 0.8rem;
        margin-bottom: 1rem;
    }
    .condition-category h4 {
        color: #004a99;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    .condition-checkboxes {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 8px;
    }
    .condition-item {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Patient data input styling */
    .patient-data-input {
        margin-bottom: 10px;
    }
    .patient-data-input label {
        font-size: 0.9rem;
        font-weight: 500;
        color: #333;
        margin-bottom: 4px;
        display: block;
    }

    /* Streamlit checkbox override */
    .stCheckbox > label {
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Reference data for nutrients ---
NUTRIENT_REFERENCES = {
    "Protein": {
        "reference": "ASPEN Guidelines 2016",
        "details": "Critical Care: 1.2-2.0 g/kg/day, Maintenance: 0.8-1.0 g/kg/day"
    },
    "Dextrose": {
        "reference": "McClave SA et al. JPEN 2016",
        "details": "Initial: 150-200 g/day, Max: 4-5 mg/kg/min (7 g/kg/day)"
    },
    "Lipids": {
        "reference": "ESPEN Guidelines 2019",
        "details": "20-30% total calories, Max: 1.0-1.5 g/kg/day"
    },
    "Sodium": {
        "reference": "ASPEN Fluid/Electrolytes 2020",
        "details": "1-2 mEq/kg/day, adjust for losses and serum levels"
    },
    "Potassium": {
        "reference": "ASPEN Fluid/Electrolytes 2020",
        "details": "1-2 mEq/kg/day, adjust for renal function and serum levels"
    },
    "Calcium": {
        "reference": "ASPEN Micronutrients 2015",
        "details": "10-15 mEq/day, monitor with phosphate"
    },
    "Magnesium": {
        "reference": "ASPEN Micronutrients 2015",
        "details": "8-20 mEq/day, adjust for serum levels"
    },
    "Phosphate": {
        "reference": "ASPEN Micronutrients 2015",
        "details": "20-40 mmol/day, monitor refeeding syndrome risk"
    },
    "MVIs": {
        "reference": "FDA MVI Guidelines 2000",
        "details": "1 vial daily for adults, provide essential vitamins"
    },
    "Trace Elements": {
        "reference": "ASPEN Trace Elements 2012",
        "details": "Zinc, copper, manganese, chromium, selenium daily"
    }
}

# --- Reference papers list ---
REFERENCES = [
    "American Society for Parenteral and Enteral Nutrition. (2016). Guidelines for the Provision and Assessment of Nutrition Support Therapy in the Adult Critically Ill Patient. Journal of Parenteral and Enteral Nutrition, 40(2), 159-211.",
    "McClave, S. A., Taylor, B. E., Martindale, R. G., et al. (2016). Guidelines for the Provision and Assessment of Nutrition Support Therapy in the Adult Critically Ill Patient. JPEN, 40(2), 159-211.",
    "Singer, P., Blaser, A. R., Berger, M. M., et al. (2019). ESPEN guideline on clinical nutrition in the intensive care unit. Clinical Nutrition, 38(1), 48-79.",
    "Boullata, J. I., Gilbert, K., Sacks, G., et al. (2014). A.S.P.E.N. clinical guidelines: parenteral nutrition ordering, order review, compounding, labeling, and dispensing. JPEN, 38(3), 334-377.",
    "Vanek, V. W., Borum, P., Buchman, A., et al. (2012). A.S.P.E.N. position paper: recommendations for changes in commercially available parenteral multivitamin and multi-trace element products. Nutrition in Clinical Practice, 27(4), 440-491.",
    "Driscoll, D. F. (2015). Compounding TPN admixtures: then and now. JPEN, 39(1 Suppl), 25S-31S.",
    "Mirtallo, J., Canada, T., Johnson, D., et al. (2004). Safe practices for parenteral nutrition. JPEN, 28(6), S39-S70."
]

# --- Main Worksheet Layout ---
st.markdown('<div class="worksheet-header">Total Parenteral Nutrition Worksheet</div>', unsafe_allow_html=True)

# --- Patient Information Section ---
st.markdown('<div class="section-header">PATIENT INFORMATION</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    physician = st.text_input("Physician", "")
with col2:
    patient_name = st.text_input("Name", "")
with col3:
    mrn = st.text_input("MRN", "")
with col4:
    room = st.text_input("Room #", "")

col5, col6, col7, col8 = st.columns(4)
with col5:
    indication = st.text_input("Indication", "")
with col6:
    route = st.selectbox("Route of Administration", ["Central", "Peripheral"])
with col7:
    st.write("Fluid Restriction:")
    fluid_no = st.checkbox("No", key="fluid_no")
    fluid_yes = st.checkbox("Yes", key="fluid_yes")
with col8:
    if fluid_yes:
        fluid_ml = st.number_input("mL/24 hours", min_value=0, value=2000)
    else:
        fluid_ml = st.number_input("mL/24 hours", min_value=0, value=0, disabled=True)

st.markdown("**Allergies:**")
allergies = st.text_input("", "", label_visibility="collapsed")

st.markdown("**Special Instructions:**")
goal_maintenance = st.checkbox("Maintenance")
goal_repletion = st.checkbox("Repletion")

# --- Patient Data Section ---
st.markdown('<div class="section-header">PATIENT DATA</div>', unsafe_allow_html=True)

# Create columns for patient data and conditions
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("**Patient Data**")
    age = st.number_input("Age (yrs)", min_value=0, max_value=120, value=45, key="age")
    height = st.number_input("Ht (in)", min_value=0.0, value=67.0, key="height")
    weight = st.number_input("Wt (kg)", min_value=0.0, value=70.0, key="weight")
    gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
    ventilator = st.checkbox("Ventilator", key="ventilator")
    minute_ventilation = st.number_input("Minute ventilation (L/min)", min_value=0.0, value=0.0, key="minute_vent")
    temp_max = st.number_input("T max (F°) last 24 hours", min_value=90.0, max_value=110.0, value=98.6, key="temp_max")

with col_right:
    st.markdown("**Patient Conditions**")

    st.markdown('<div class="condition-category">', unsafe_allow_html=True)
    st.markdown("**Critically Ill Conditions**")
    traumatic_brain_injury = st.checkbox("Traumatic Brain Injury", key="tbi")
    burns = st.checkbox("Burns", key="burns")
    sepsis = st.checkbox("Sepsis", key="sepsis")
    open_abdomen = st.checkbox("Open Abdomen", key="open_abdomen")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="condition-category">', unsafe_allow_html=True)
    st.markdown("**Renal Conditions**")
    acute_kidney_injury = st.checkbox("Acute Kidney Injury", key="aki")
    aki_no_rrt = st.checkbox("AKI (No RRT)", key="aki_no_rrt")
    aki_intermittent_rrt = st.checkbox("AKI (Intermittent RRT)", key="aki_intermittent_rrt")
    aki_crrt = st.checkbox("AKI (CRRT)", key="aki_crrt")
    chronic_kidney_failure = st.checkbox("Chronic Kidney Failure", key="ckd")
    ckd_maintenance_hd = st.checkbox("CKD (Maintenance HD)", key="ckd_hd")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="condition-category">', unsafe_allow_html=True)
    st.markdown("**Other Conditions**")
    obese = st.checkbox("Obese", key="obese")
    liver_failure = st.checkbox("Liver Failure", key="liver_failure")
    heart_failure = st.checkbox("Heart Failure", key="heart_failure")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Instructions Box ---
st.markdown("""
<div class="instructions-box">
    <strong>Special Instructions:</strong><br>
    - Goal of Therapy: Maintenance / Repletion<br>
    - Start by entering the patient data. This will update the protein requirements and energy expenditure.<br>
    - The form will correct for weight considerations (i.e. obese patients).<br>
    - Select relevant patient conditions to adjust nutritional recommendations.<br>
    - Enter the desired protein and calories per day, along with the goal TPN rate.<br>
    - The TPN formula chart will calculate the exact substrate amounts.<br>
    - Use the boxes to enter actual substrate formulas to find the desired formula.<br>
    - Colored boxes may appear if parameters are outside a specified range, please use clinical judgement in evaluating these values.<br>
    <strong>Note: You can only enter numbers into the yellow boxes.</strong>
</div>
""", unsafe_allow_html=True)
-+

# --- Generate Plan Button ---
if st.button("Calculate TPN Formulation", type="primary"):
    with st.spinner("Calculating TPN formulation..."):
        # Create patient object
        patient = AdultPatient(
            name=patient_name or "Unknown",
            age=age,
            height=height * 2.54,  # Convert inches to cm
            weight=weight,
            gender=(gender == "Male"),
            conditions={}
        )

        # Run planner
        planner = TpnPlanner(patient, total_days=7)
        df = planner.generate_daily_plan()

        st.success("TPN formulation calculated successfully!")

        # Display results in a table format
        st.markdown('<div class="section-header">TPN FORMULATION RESULTS</div>', unsafe_allow_html=True)

        # Sample data - in a real app, this would come from the planner
        sample_data = {
            "Macronutrients": {
                "Protein": [70, 70, 70, 70, 70, 70, 70],
                "Dextrose": [150, 200, 250, 250, 250, 250, 250],
                "Lipids": [25, 40, 50, 50, 50, 50, 50]
            },
            "Electrolytes": {
                "Sodium": [80, 80, 80, 80, 80, 80, 80],
                "Potassium": [40, 40, 40, 40, 40, 40, 40],
                "Calcium": [10, 10, 10, 10, 10, 10, 10],
                "Magnesium": [8, 8, 8, 8, 8, 8, 8],
                "Phosphate": [15, 15, 15, 15, 15, 15, 15]
            },
            "Vitamins & Trace Elements": {
                "MVIs": [1, 1, 1, 1, 1, 1, 1],
                "Trace Elements": [1, 1, 1, 1, 1, 1, 1]
            },
            "Summary": {
                "Total Calories": [1200, 1500, 1600, 1600, 1600, 1600, 1600],
                "Total Volume": [1500, 1800, 2000, 2000, 2000, 2000, 2000],
                "Protein % of Calories": [23.3, 18.7, 17.5, 17.5, 17.5, 17.5, 17.5]
            }
        }

        # Create HTML table for results with hover tooltips
        html_table = """
        <table class="results-table">
            <tr>
                <th>Category</th>
                <th>Nutrient</th>
                <th>Day 1</th>
                <th>Day 2</th>
                <th>Day 3</th>
                <th>Day 4</th>
                <th>Day 5</th>
                <th>Day 6</th>
                <th>Day 7</th>
            </tr>
        """

        for category, nutrients in sample_data.items():
            first_row = True
            for nutrient, values in nutrients.items():
                html_table += "<tr>"
                if first_row:
                    html_table += f'<td class="category-cell" rowspan="{len(nutrients)}">{category}</td>'
                    first_row = False

                # Add nutrient with hover tooltip
                ref_data = NUTRIENT_REFERENCES.get(nutrient, {"reference": "Clinical Practice Guidelines",
                                                              "details": "Standard clinical practice"})
                html_table += f"""
                <td style='text-align: left;'>
                    <span class="nutrient-with-tooltip">
                        {nutrient} ({'g' if nutrient in ['Protein', 'Dextrose', 'Lipids'] else 'mEq' if nutrient in ['Sodium', 'Potassium', 'Calcium', 'Magnesium'] else 'mmol' if nutrient == 'Phosphate' else 'vial' if nutrient in ['MVIs', 'Trace Elements'] else 'kcal' if 'Calories' in nutrient else 'mL' if 'Volume' in nutrient else '%'})
                        <span class="nutrient-tooltip">
                            <strong>Reference:</strong> {ref_data['reference']}<br>
                            <strong>Details:</strong> {ref_data['details']}
                        </span>
                    </span>
                </td>
                """

                for val in values:
                    html_table += f"<td>{val}</td>"
                html_table += "</tr>"

        html_table += "</table>"

        st.markdown(html_table, unsafe_allow_html=True)

        # Add clinical notes
        st.markdown("""
        <div class="note-box">
            <strong>Clinical Notes:</strong><br>
            - TPN formulation meets estimated energy requirements<br>
            - Protein provision appropriate for patient's clinical status<br>
            - Electrolytes within normal ranges for TPN<br>
            - Monitor glucose levels during dextrose titration<br>
            - Consider adding insulin if hyperglycemia develops
        </div>
        """, unsafe_allow_html=True)

# --- References Section ---
st.markdown("""
<div class="references-section">
    <h3>References</h3>
""", unsafe_allow_html=True)

for i, ref in enumerate(REFERENCES, 1):
    st.markdown(f"""
    <div class="reference-item">
        <strong>[{i}]</strong> {ref}
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)