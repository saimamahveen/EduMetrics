
import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="EduMetrics | Student Analytics",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# 2. PROFESSIONAL UI DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #F7F7FB;
    color: #334155;
}

[data-testid="stSidebar"] {
    background-color: #EFECF6;
    border-right: 1px solid #E3DDED;
}

h1 {
    color: #65558A !important;
    font-weight: 750 !important;
}

h2, h3 {
    color: #374151 !important;
}

p, label {
    color: #64748B;
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #E8E4F0;
    box-shadow: 0 3px 12px rgba(70,55,100,0.05);
}

div[data-testid="stMetricLabel"] {
    color: #81749E;
}

div[data-testid="stMetricValue"] {
    color: #343047;
    font-weight: 700;
}

.stButton button, .stDownloadButton button {
    background: #78669D;
    color: white;
    border-radius: 9px;
    border: none;
}

.stButton button:hover, .stDownloadButton button:hover {
    background: #65558A;
    color: white;
}

[data-testid="stDataFrame"] {
    border: 1px solid #E8E4F0;
    border-radius: 12px;
}

hr {
    border-color: #E6E1EE;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. STUDENT DATASET
# ==========================================

data = {
    "Student": [
        "Aisha Khan", "Rahul Sharma", "Sara Ali",
        "Arjun Reddy", "Zoya Fatima", "Aditya Rao",
        "Meera Nair", "Kabir Singh", "Ananya Das",
        "Ibrahim Khan", "Priya Verma", "Rohan Gupta",
        "Sana Sheikh", "Vikram Patel", "Diya Menon",
        "Aarav Jain", "Fatima Noor", "Karan Kumar",
        "Nisha Roy", "Sameer Ahmed"
    ],

    "Department": [
        "CSE", "ECE", "CSE", "EEE", "IT",
        "CSE", "IT", "ECE", "CSE", "EEE",
        "IT", "CSE", "ECE", "CSE", "IT",
        "EEE", "CSE", "ECE", "IT", "CSE"
    ],

    "Maths": [
        85, 65, 92, 45, 78, 88, 76, 55, 96, 72,
        82, 60, 90, 48, 86, 68, 94, 75, 80, 58
    ],

    "Science": [
        90, 70, 88, 50, 82, 92, 80, 62, 91, 76,
        85, 67, 93, 52, 89, 72, 96, 78, 84, 61
    ],

    "English": [
        80, 75, 95, 60, 85, 86, 88, 70, 92, 81,
        90, 73, 89, 65, 94, 77, 91, 82, 87, 69
    ],

    "Computer": [
        95, 80, 90, 55, 92, 98, 85, 68, 99, 83,
        94, 75, 97, 60, 96, 79, 98, 86, 90, 72
    ],

    "Attendance": [
        95, 80, 98, 65, 90, 96, 88, 72, 99, 85,
        92, 78, 97, 68, 94, 81, 98, 89, 91, 75
    ]
}

df = pd.DataFrame(data)

subjects = ["Maths", "Science", "English", "Computer"]

# ==========================================
# 4. PERFORMANCE CALCULATIONS
# ==========================================

def analyze(data):
    result = data.copy()

    result["Average"] = result[subjects].mean(axis=1)

    result["Percentage"] = result["Average"].round(1)

    result["Result"] = result[subjects].apply(
        lambda row: "Pass" if (row >= 35).all()
        else "Fail",
        axis=1
    )

    result["Grade"] = result["Average"].apply(
        lambda x:
        "A+" if x >= 90 else
        "A" if x >= 80 else
        "B" if x >= 70 else
        "C" if x >= 60 else
        "D" if x >= 50 else "F"
    )

    return result

# ==========================================
# 5. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🎓 EduMetrics")

st.sidebar.caption("STUDENT PERFORMANCE ANALYTICS")

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Student Records",
        "Analytics",
        "Student Profile"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### About EduMetrics")

st.sidebar.write(
    "An academic analytics platform "
    "to monitor student performance, "
    "grades and attendance."
)

st.sidebar.caption("Academic Analytics | 2026")

# ==========================================
# 6. MAIN HEADER
# ==========================================

st.title("EduMetrics")

st.subheader("Student Performance Intelligence")

st.caption(
    "Monitor academic progress. "
    "Discover insights. Improve outcomes."
)

# ==========================================
# 7. ADD AND EDIT STUDENTS
# ==========================================

with st.expander("➕ Add or Edit Student Records"):

    st.write("Manage student information and academic marks.")

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )

# ==========================================
# 8. VALIDATE STUDENT DATA
# ==========================================

valid = edited_df.copy()

for col in subjects + ["Attendance"]:
    valid[col] = pd.to_numeric(
        valid[col], errors="coerce"
    )

valid = valid.dropna(
    subset=["Student", "Department"] + subjects + ["Attendance"]
)

valid = valid[
    valid[subjects + ["Attendance"]].ge(0).all(axis=1)
    &
    valid[subjects + ["Attendance"]].le(100).all(axis=1)
]

valid["Student"] = valid["Student"].astype(str).str.strip()

valid = valid[valid["Student"] != ""]

if valid.empty:
    st.warning("Please enter valid student records.")
    st.stop()

df = analyze(valid)

# ==========================================
# 9. SEARCH AND FILTERS
# ==========================================

st.sidebar.markdown("### FILTER STUDENTS")

departments = st.sidebar.multiselect(
    "Department",
    sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

grades = st.sidebar.multiselect(
    "Grade",
    sorted(df["Grade"].unique()),
    default=sorted(df["Grade"].unique())
)

filtered = df[
    df["Department"].isin(departments)
    &
    df["Grade"].isin(grades)
].copy()

if filtered.empty:
    st.warning("No students match the selected filters.")
    st.stop()

# ==========================================
# 10. OVERVIEW DASHBOARD
# ==========================================

if page == "Overview":

    st.header("Performance Overview")

    total = len(filtered)

    average = filtered["Average"].mean()

    passed = (filtered["Result"] == "Pass").sum()

    pass_rate = passed / total * 100

    attendance = filtered["Attendance"].mean()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Students", total)

    c2.metric("Average Score", f"{average:.1f}%")

    c3.metric("Pass Rate", f"{pass_rate:.1f}%")

    c4.metric("Avg Attendance", f"{attendance:.1f}%")

    st.divider()

    left, right = st.columns(2)

    # SUBJECT PERFORMANCE

    with left:

        st.subheader("Subject Performance")

        subject_avg = filtered[subjects].mean().reset_index()

        subject_avg.columns = ["Subject", "Average Marks"]

        fig = px.bar(
            subject_avg,
            x="Subject",
            y="Average Marks",
            color="Subject",
            color_discrete_sequence=[
                "#8B78B8",
                "#78A6A0",
                "#8DA9C4",
                "#D5AE86"
            ],
            template="plotly_white"
        )

        fig.update_layout(
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)

    # GRADE DISTRIBUTION

    with right:

        st.subheader("Grade Distribution")

        grade_count = filtered["Grade"].value_counts().reset_index()

        grade_count.columns = ["Grade", "Students"]

        fig = px.pie(
            grade_count,
            names="Grade",
            values="Students",
            hole=0.55,
            color_discrete_sequence=[
                "#8B78B8",
                "#78A6A0",
                "#8DA9C4",
                "#D5AE86",
                "#B9A6CB",
                "#D99595"
            ],
            template="plotly_white"
        )

        fig.update_layout(
            paper_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)

    # TOP PERFORMERS

    st.subheader("🏆 Top 5 Performers")

    top = filtered.nlargest(5, "Average")

    st.dataframe(
        top[
            ["Student", "Department", "Average", "Grade", "Attendance"]
        ],
        use_container_width=True,
        hide_index=True
    )

    # STUDENTS NEEDING ATTENTION

    st.subheader("Students Needing Attention")

    low = filtered[
        (filtered["Attendance"] < 75)
        |
        (filtered["Average"] < 50)
    ]

    if low.empty:

        st.success("No students currently need attention.")

    else:

        st.dataframe(
            low[
                ["Student", "Average", "Grade", "Attendance"]
            ],
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# 11. STUDENT RECORDS
# ==========================================

elif page == "Student Records":

    st.header("Student Database")

    search = st.text_input("Search Student Name")

    records = filtered.copy()

    if search:

        records = records[
            records["Student"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    sort_by = st.selectbox(
        "Sort By",
        ["Average", "Attendance", "Student"]
    )

    records = records.sort_values(
        sort_by,
        ascending=False
    )

    st.dataframe(
        records,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Student Records",
        records.to_csv(index=False).encode("utf-8"),
        "EduMetrics_Records.csv",
        "text/csv"
    )

# ==========================================
# 12. ACADEMIC ANALYTICS
# ==========================================

elif page == "Analytics":

    st.header("Academic Analytics")

    left, right = st.columns(2)

    # DEPARTMENT COMPARISON

    with left:

        st.subheader("Department Comparison")

        dept = filtered.groupby("Department")[subjects].mean().reset_index()

        fig = px.bar(
            dept,
            x="Department",
            y=subjects,
            barmode="group",
            color_discrete_sequence=[
                "#8B78B8",
                "#78A6A0",
                "#8DA9C4",
                "#D5AE86"
            ],
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ATTENDANCE VS MARKS

    with right:

        st.subheader("Marks vs Attendance")

        fig = px.scatter(
            filtered,
            x="Attendance",
            y="Average",
            color="Department",
            hover_name="Student",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    # SUBJECT COMPARISON

    st.subheader("Student Subject Comparison")

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    fig = px.bar(
        filtered.sort_values(
            selected_subject,
            ascending=False
        ),
        x="Student",
        y=selected_subject,
        color="Department",
        template="plotly_white"
    )

    fig.update_layout(
        xaxis_tickangle=-40
    )

    st.plotly_chart(fig, use_container_width=True)

    # STATISTICS

    st.subheader("Statistical Summary")

    st.dataframe(
        filtered[subjects].describe(),
        use_container_width=True
    )

# ==========================================
# 13. INDIVIDUAL STUDENT PROFILE
# ==========================================

elif page == "Student Profile":

    st.header("Individual Student Profile")

    selected = st.selectbox(
        "Choose Student",
        filtered["Student"].tolist()
    )

    person = filtered[
        filtered["Student"] == selected
    ].iloc[0]

    st.subheader(f"Student: {selected}")

    a, b, c = st.columns(3)

    a.metric(
        "Average Marks",
        f"{person['Average']:.1f}%"
    )

    b.metric(
        "Grade",
        person["Grade"]
    )

    c.metric(
        "Attendance",
        f"{person['Attendance']}%"
    )

    st.divider()

    st.subheader("Subject-wise Performance")

    profile_data = pd.DataFrame({
        "Subject": subjects,
        "Marks": [person[s] for s in subjects]
    })

    fig = px.bar(
        profile_data,
        x="Subject",
        y="Marks",
        color="Subject",
        color_discrete_sequence=[
            "#8B78B8",
            "#78A6A0",
            "#8DA9C4",
            "#D5AE86"
        ],
        template="plotly_white"
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Academic Details")

    st.write("Department:", person["Department"])

    st.write("Percentage:", f"{person['Percentage']}%")

    st.write("Result:", person["Result"])

    if person["Attendance"] < 75:

        st.warning("Attendance is below 75%.")

    else:

        st.success("Attendance is satisfactory.")

    if person["Average"] >= 80:

        st.success("Excellent academic performance!")

    elif person["Average"] >= 60:

        st.info("Good performance. Keep improving!")

    else:

        st.warning("Additional academic support may help.")

    st.download_button(
        "Download Individual Report",
        pd.DataFrame([person]).to_csv(index=False).encode("utf-8"),
        f"{selected.replace(' ', '_')}_Report.csv",
        "text/csv"
    )

# ==========================================
# 14. FOOTER
# ==========================================

st.divider()

st.caption(
    "© 2026 EduMetrics | Student Performance Intelligence System"
)

st.caption(
    "Developed using Python | Streamlit | Pandas | Plotly"
)
