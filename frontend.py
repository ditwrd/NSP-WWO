import os
import numpy as np
from backend import NSP_Class, WWO
import streamlit as st

# os.environ["MODIN_ENGINE"] = "dask"
# from distributed import Client
# client = Client()
import pandas as pd


class Main:
    def __init__(self):
        pass

    def main(self):
        st.set_page_config(
            page_title="Optimizing Nurse Schedulin Problem with Water Wave Optimization",
            page_icon=":calendar:",
            layout="wide",
        )
        # Input
        self.input()
        # Output
        self.output()

    def input(self):
        st.session_state["optimize"] = False
        with st.sidebar.form("Input"):
            st.title("Input Parameter")
            st.number_input("Iteration", key="iter", value=1000)
            st.number_input("H Max (Max Wave Height)", key="hmax", value=6.0,step=0.000001,max_value=100000.0,min_value=0.0)
            st.number_input("Lambda (Wavelength)", key="lambd", value=0.5,step=0.000001,max_value=100000.0,min_value=0.0)
            st.number_input("Alpha", key="alpha", value=1.001,step=0.000001,max_value=100000.0,min_value=0.0)
            st.number_input("Beta Max", key="beta_max", value=0.01,step=0.000001,max_value=100000.0,min_value=0.0)
            st.number_input("Beta Min", key="beta_min", value=0.001,step=0.000001,max_value=100000.0,min_value=0.0)
            st.number_input("Epsilon", key="epsilon", value=1e-31)
            st.number_input("K Max", key="k_max", value=12)
            st.number_input("Upper Bound", key="upper_bound", value=1)
            st.number_input("Lower Bound", key="lower_bound", value=0)
            if st.form_submit_button("Optimize"):
                st.session_state["optimize"] = True

    def output(self):
        st.title("Optimizing Nurse Scheduling Problem with Water Wave Optimization")
        units_name = ["IGD", "Rawat Inap", "Anastesi", "ICU", "OK"]
        units_nurse_num = np.array([30, 122, 23, 28, 33])
        units_morning_shift = np.array([8, 34, 6, 7, 8])
        units_afternoon_shift = np.array([8, 34, 6, 7, 8])
        units_night_shift = np.array([6, 24, 5, 6, 6])

        units_minimum_shift = np.vstack(
            (units_morning_shift, units_afternoon_shift, units_night_shift)
        ).T
        units_minimum_shift = np.hstack((units_minimum_shift, np.zeros((5, 1))))

        cols = st.columns(len(units_name))
        for index in range(len(units_name)):
            with cols[index]:
                st.header(units_name[index])
                st.write(
                    f"""Total Nurse = {str(units_nurse_num[index])}  \nMorning Shift = {str(units_morning_shift[index])}  \nNoon Shift = {str(units_afternoon_shift[index])}  \nNight Shift = {str(units_night_shift[index])}"""
                )

        NSP_Class_Dict = {}
        for index, unit in enumerate(units_name):
            NSP_Class_Dict[unit] = NSP_Class(
                day=30,
                units_name=unit,
                unit_total_nurse=units_nurse_num[index],
                unit_minimum_shift=units_minimum_shift[index, :],
                hard_constraint_multiplier=1000,
            )
        cols2 = st.columns(3)
        with cols2[0]:
            st.subheader("IGD")
            st.dataframe(
                pd.DataFrame(
                    NSP_Class_Dict["IGD"].nurse_array_col,
                    index=[
                        "Perawat " + str(i)
                        for i in np.arange(
                            1, NSP_Class_Dict["IGD"].nurse_array_col.shape[0] + 1
                        )
                    ],
                    columns=[
                        "Hari " + str(i)
                        for i in np.arange(
                            1, NSP_Class_Dict["IGD"].nurse_array_col.shape[1] + 1
                        )
                    ],
                )
            )
            st.subheader("Rawat Inap")
            st.dataframe(
                pd.DataFrame(
                    NSP_Class_Dict["Rawat Inap"].nurse_array_col,
                    index=[
                        "Perawat " + str(i)
                        for i in np.arange(
                            1, NSP_Class_Dict["Rawat Inap"].nurse_array_col.shape[0] + 1
                        )
                    ],
                    columns=[
                        "Hari " + str(i)
                        for i in np.arange(
                            1, NSP_Class_Dict["Rawat Inap"].nurse_array_col.shape[1] + 1
                        )
                    ],
                )
            )
            st.subheader("Anastesi")
            st.dataframe(
                pd.DataFrame(
                    NSP_Class_Dict["Anastesi"].nurse_array_col,
                    index=[
                        "Perawat " + str(i)
                        for i in np.arange(
                            1, NSP_Class_Dict["Anastesi"].nurse_array_col.shape[0] + 1
                        )
                    ],
                    columns=[
                        "Hari " + str(i)
                        for i in np.arange(
                            1, NSP_Class_Dict["Anastesi"].nurse_array_col.shape[1] + 1
                        )
                    ],
                )
            )
            st.subheader("ICU")
            st.dataframe(
                pd.DataFrame(
                    NSP_Class_Dict["ICU"].nurse_array_col,
                    index=[
                        "Perawat " + str(i)
                        for i in np.arange(
                            1, NSP_Class_Dict["ICU"].nurse_array_col.shape[0] + 1
                        )
                    ],
                    columns=[
                        "Hari " + str(i)
                        for i in np.arange(
                            1, NSP_Class_Dict["ICU"].nurse_array_col.shape[1] + 1
                        )
                    ],
                )
            )
            st.subheader("OK")
            st.dataframe(
                pd.DataFrame(
                    NSP_Class_Dict["OK"].nurse_array_col,
                    index=[
                        "Perawat " + str(i)
                        for i in np.arange(
                            1, NSP_Class_Dict["OK"].nurse_array_col.shape[0] + 1
                        )
                    ],
                    columns=[
                        "Hari " + str(i)
                        for i in np.arange(
                            1, NSP_Class_Dict["OK"].nurse_array_col.shape[1] + 1
                        )
                    ],
                )
            )

        with cols2[1]:
            igd_plot_text = st.empty()
            igd_plot = st.empty()
            r_inap_plot_text = st.empty()
            r_inap_plot = st.empty()
            anastesi_plot_text = st.empty()
            anastesi_plot = st.empty()
            icu_plot_text = st.empty()
            icu_plot = st.empty()
            ok_plot_text = st.empty()
            ok_plot = st.empty()

        with cols2[2]:
            igd_cost_text = st.empty()
            igd_2 = st.empty()
            r_inap_cost_text = st.empty()
            r_inap_2 = st.empty()
            anastesi_cost_text = st.empty()
            anastesi_2 = st.empty()
            icu_cost_text = st.empty()
            icu_2 = st.empty()
            ok_cost_text = st.empty()
            ok_2 = st.empty()

        if st.session_state["optimize"]:
            WWO_Class_Dict = {}
            for index, unit_name in enumerate(units_name):
                WWO_Class_Dict[unit_name] = WWO(
                    NSP=NSP_Class_Dict[unit_name],
                    iteration=st.session_state["iter"],
                    hmax=st.session_state["hmax"],
                    lambd=st.session_state["lambd"],
                    alpha=st.session_state["alpha"],
                    epsilon=st.session_state["epsilon"],
                    beta_max=st.session_state["beta_max"],
                    beta_min=st.session_state["beta_min"],
                    k_max=st.session_state["k_max"],
                    upper_bound=st.session_state["upper_bound"],
                    lower_bound=st.session_state["lower_bound"],
                )

            igd_pos, _ = WWO_Class_Dict["IGD"].optimize()
            igd_plot_text.subheader("IGD WWO Plot")
            igd_plot.line_chart(WWO_Class_Dict["IGD"].best_fit_iteration)
            igd_cost_text.subheader(
                f"""Cost {min(WWO_Class_Dict["IGD"].best_fit_iteration)} -> {max(WWO_Class_Dict["IGD"].best_fit_iteration)}"""
            )
            igd_2.dataframe(
                pd.DataFrame(
                    igd_pos,
                    index=[
                        "Perawat " + str(i) for i in np.arange(1, igd_pos.shape[0] + 1)
                    ],
                    columns=[
                        "Hari " + str(i) for i in np.arange(1, igd_pos.shape[1] + 1)
                    ],
                )
            )

            r_inap_pos, _ = WWO_Class_Dict["Rawat Inap"].optimize()
            r_inap_plot_text.subheader("Rawat Inap WWO Plot")
            r_inap_plot.line_chart(WWO_Class_Dict["Rawat Inap"].best_fit_iteration)
            r_inap_cost_text.subheader(
                f"""Cost {min(WWO_Class_Dict["Rawat Inap"].best_fit_iteration)} -> {max(WWO_Class_Dict["Rawat Inap"].best_fit_iteration)}"""
            )
            r_inap_2.dataframe(
                pd.DataFrame(
                    r_inap_pos,
                    index=[
                        "Perawat " + str(i)
                        for i in np.arange(1, r_inap_pos.shape[0] + 1)
                    ],
                    columns=[
                        "Hari " + str(i) for i in np.arange(1, r_inap_pos.shape[1] + 1)
                    ],
                )
            )
            anastesi_pos, _ = WWO_Class_Dict["Anastesi"].optimize()
            anastesi_plot_text.subheader("Anastesi WWO Plot")
            anastesi_plot.line_chart(WWO_Class_Dict["Anastesi"].best_fit_iteration)
            anastesi_cost_text.subheader(
                f"""Cost {min(WWO_Class_Dict["Anastesi"].best_fit_iteration)} -> {max(WWO_Class_Dict["Anastesi"].best_fit_iteration)}"""
            )
            anastesi_2.dataframe(
                pd.DataFrame(
                    anastesi_pos,
                    index=[
                        "Perawat " + str(i)
                        for i in np.arange(1, anastesi_pos.shape[0] + 1)
                    ],
                    columns=[
                        "Hari " + str(i)
                        for i in np.arange(1, anastesi_pos.shape[1] + 1)
                    ],
                )
            )
            icu_pos, _ = WWO_Class_Dict["ICU"].optimize()
            icu_plot_text.subheader("ICU WWO Plot")
            icu_plot.line_chart(WWO_Class_Dict["ICU"].best_fit_iteration)
            icu_cost_text.subheader(
                f"""Cost {min(WWO_Class_Dict["ICU"].best_fit_iteration)} -> {max(WWO_Class_Dict["ICU"].best_fit_iteration)}"""
            )
            icu_2.dataframe(
                pd.DataFrame(
                    icu_pos,
                    index=[
                        "Perawat " + str(i) for i in np.arange(1, icu_pos.shape[0] + 1)
                    ],
                    columns=[
                        "Hari " + str(i) for i in np.arange(1, icu_pos.shape[1] + 1)
                    ],
                )
            )
            ok_pos, _ = WWO_Class_Dict["OK"].optimize()
            ok_plot_text.subheader("OK WWO Plot")
            ok_plot.line_chart(WWO_Class_Dict["OK"].best_fit_iteration)
            ok_cost_text.subheader(
                f"""Cost {min(WWO_Class_Dict["OK"].best_fit_iteration)} -> {max(WWO_Class_Dict["OK"].best_fit_iteration)}"""
            )
            ok_2.dataframe(
                pd.DataFrame(
                    ok_pos,
                    index=[
                        "Perawat " + str(i) for i in np.arange(1, ok_pos.shape[0] + 1)
                    ],
                    columns=[
                        "Hari " + str(i) for i in np.arange(1, ok_pos.shape[1] + 1)
                    ],
                )
            )


if __name__ == "__main__":
    Main().main()
