import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="EduMetrics | Student Analytics",
    page_icon="🎓",
    layout="wide",
)

# ==========================================
# 2. DESIGN SYSTEM
# ==========================================

ACCENT = "#8B93FF"
PALETTE = ["#8B93FF", "#5EEAD4", "#F5B971", "#F58BA5", "#7DC4FF", "#C4A8FF"]
MUTED = "#8A93AB"
GRID = "rgba(255,255,255,0.06)"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #0A0E1A;
    --surface: rgba(255,255,255,0.035);
    --surface-hover: rgba(255,255,255,0.06);
    --border: rgba(255,255,255,0.07);
    --text: #E6E9F2;
    --muted: #8A93AB;
    --accent: #8B93FF;
    --accent-2: #5EEAD4;
}

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif !important;
}

/* Ambient background glow */
.stApp {
    background:
        radial-gradient(900px 500px at 85% -10%, rgba(139,147,255,0.14), transparent 60%),
        radial-gradient(700px 400px at -5% 10%, rgba(94,234,212,0.07), transparent 60%),
        var(--bg);
    color: var(--text);
}

header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1222 0%, #0A0E1A 100%);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

.brand {
    display: flex; align-items: center; gap: 12px;
    padding: 4px 2px 18px 2px;
}
.brand-logo {
    width: 38px; height: 38px; border-radius: 11px;
    display: grid; place-items: center; font-size: 19px;
    background: linear-gradient(135deg, #8B93FF, #5EEAD4);
    box-shadow: 0 6px 20px rgba(139,147,255,0.35);
}
.brand-name { font-weight: 700; font-size: 1.12rem; letter-spacing: -0.01em; color: var(--text); line-height: 1.1; }
.brand-tag  { font-size: 0.62rem; letter-spacing: 0.14em; color: var(--muted); text-transform: uppercase; margin-top: 3px; }

.side-label {
    font-size: 0.66rem; letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--muted); margin: 18px 0 8px 2px; font-weight: 600;
}

[data-testid="stSidebar"] [role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 9px 12px; border-radius: 10px; width: 100%;
    border: 1px solid transparent; transition: all .18s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: var(--surface-hover); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, rgba(139,147,255,0.18), rgba(139,147,255,0.04));
    border-color: rgba(139,147,255,0.30);
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] label p { font-weight: 500; font-size: 0.92rem; }

/* ---------- Page header ---------- */
.hero { margin-bottom: 1.6rem; }
.eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 0.7rem; letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--accent-2); font-weight: 600; margin-bottom: 10px;
}
.eyebrow::before {
    content: ""; width: 7px; height: 7px; border-radius: 50%;
    background: var(--accent-2); box-shadow: 0 0 10px var(--accent-2);
}
.hero h1 {
    font-size: 2.35rem; font-weight: 700; letter-spacing: -0.03em; margin: 0 0 6px 0;
    background: linear-gradient(90deg, #FFFFFF 20%, #AEB4FF 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { color: var(--muted); font-size: 0.98rem; margin: 0; }

h2, h3 { letter-spacing: -0.02em; color: var(--text) !important; font-weight: 600 !important; }
.section-title {
    font-size: 1.02rem; font-weight: 600; color: var(--text);
    margin: 1.6rem 0 0.7rem 0; display: flex; align-items: center; gap: 10px;
}
.section-title::after { content: ""; flex: 1; height: 1px; background: var(--border); }

/* ---------- KPI cards ---------- */
.kpi {
    position: relative; overflow: hidden;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 16px; padding: 20px 22px;
    backdrop-filter: blur(10px);
    transition: transform .2s ease, border-color .2s ease, background .2s ease;
}
.kpi:hover { transform: translateY(-3px); border-color: rgba(139,147,255,0.35); background: var(--surface-hover); }
.kpi::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--k, #8B93FF), transparent);
}
.kpi-top { display: flex; justify-content: space-between; align-items: center; }
.kpi-label { font-size: 0.74rem; color: var(--muted); letter-spacing: 0.06em; text-transform: uppercase; font-weight: 500; }
.kpi-icon {
    width: 30px; height: 30px; border-radius: 9px; display: grid; place-items: center; font-size: 14px;
    background: color-mix(in srgb, var(--k, #8B93FF) 16%, transparent);
}
.kpi-value { font-size: 2rem; font-weight: 700; letter-spacing: -0.03em; margin-top: 12px; color: #fff; }
.kpi-sub { font-size: 0.78rem; color: var(--muted); margin-top: 2px; }

/* ---------- Panels (charts) ---------- */
[data-testid="stPlotlyChart"] {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 16px; padding: 10px 8px 2px 8px;
}

/* ---------- Tables ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border); border-radius: 14px; overflow: hidden;
}

/* ---------- Inputs ---------- */
[data-baseweb="select"] > div, [data-baseweb="input"] > div, .stTextInput input {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] > div:hover, [data-baseweb="input"] > div:focus-within {
    border-color: rgba(139,147,255,0.5) !important;
}
[data-baseweb="tag"] { background: rgba(139,147,255,0.18) !important; border-radius: 7px !important; }

/* ---------- Buttons ---------- */
.stButton button, .stDownloadButton button {
    background: linear-gradient(135deg, #8B93FF, #6C74E8);
    color: #fff; border: none; border-radius: 10px;
    padding: 0.55rem 1.2rem; font-weight: 600;
    box-shadow: 0 6px 18px rgba(139,147,255,0.25);
    transition: all .18s ease;
}
.stButton button:hover, .stDownloadButton button:hover {
    transform: translateY(-1px); color: #fff;
    box-shadow: 0 10px 26px rgba(139,147,255,0.40);
}

/* ---------- Expander ---------- */
[data-testid="stExpander"] {
    background: var(--surface); border: 1px solid var(--border) !important;
    border-radius: 14px;
}

/* ---------- Alerts ---------- */
[data-testid="stAlert"] { border-radius: 12px; border: 1px solid var(--border); }

/* ---------- Badges ---------- */
.badge {
    display: inline-block; padding: 4px 12px; border-radius: 999px;
    font-size: 0.76rem; font-weight: 600; margin-right: 6px;
    border: 1px solid transparent;
}
.b-ok   { background: rgba(94,234,212,0.12);  color: #5EEAD4; border-color: rgba(94,234,212,0.3); }
.b-warn { background: rgba(245,185,113,0.12); color: #F5B971; border-color: rgba(245,185,113,0.3); }
.b-bad  { background: rgba(245,139,165,0.12); color: #F58BA5; border-color: rgba(245,139,165,0.3); }
.b-info { background: rgba(139,147,255,0.14); color: #AEB4FF; border-color: rgba(139,147,255,0.3); }

.profile-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 16px; padding: 22px; display: flex; align-items: center; gap: 18px;
}
.avatar {
    width: 58px; height: 58px; border-radius: 16px; display: grid; place-items: center;
    font-weight: 700; font-size: 1.25rem; color: #0A0E1A;
    background: linear-gradient(135deg, #8B93FF, #5EEAD4);
}
.p-name { font-size: 1.3rem; font-weight: 700; letter-spacing: -0.02em; }
.p-meta { color: var(--muted); font-size: 0.86rem; margin-top: 2px; }

.foot { text-align: center; color: var(--muted); font-size: 0.76rem; margin-top: 2.5rem; padding-top: 1.2rem; border-top: 1px solid var(--border); }

hr { border-color: var(--border); }
</style>
""", unsafe_allow_html=True)


# ---------- UI helpers ----------

def kpi(col, label, value, sub, icon, color):
    col.markdown(
        f"""<div class="kpi" style="--k:{color}">
            <div class="kpi-top"><span class="kpi-label">{label}</span>
            <span class="kpi-icon">{icon}</span></div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div></div>""",
        unsafe_allow_html=True,
    )


def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def hero(eyebrow, title, subtitle):
    st.markdown(
        f"""<div class="hero"><div class="eyebrow">{eyebrow}</div>
        <h1>{title}</h1><p>{subtitle}</p></div>""",
        unsafe_allow_html=True,
    )


def style_fig(fig, height=360, legend=True):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=MUTED, size=12),
        margin=dict(l=16, r=16, t=24, b=12),
        colorway=PALETTE,
        showlegend=legend,
        legend=dict(orientation="h", y=-0.2, x=0, title=None, font=dict(size=11)),
        hoverlabel=dict(bgcolor="#161C30", bordercolor="rgba(255,255,255,0.12)",
                        font=dict(family="Inter", color="#E6E9F2")),
        bargap=0.35,
    )
    fig.update_xaxes(showgrid=False, linecolor=GRID, title=None, zeroline=False)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, title=None)
    return fig


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
    "Maths": [85, 65, 92, 45, 78, 88, 76, 55, 96, 72,
              82, 60, 90, 48, 86, 68, 94, 75, 80, 58],
    "Science": [90, 70, 88, 50, 82, 92, 80, 62, 91, 76,
                85, 67, 93, 52, 89, 72, 96, 78, 84, 61],
    "English": [80, 75, 95, 60, 85, 86, 88, 70, 92, 81,
                90, 73, 89, 65, 94, 77, 91, 82, 87, 69],
    "Computer": [95, 80, 90, 55, 92, 98, 85, 68, 99, 83,
                 94, 75, 97, 60, 96, 79, 98, 86, 90, 72],
    "Attendance": [95, 80, 98, 65, 90, 96, 88, 72, 99, 85,
                   92, 78, 97, 68, 94, 81, 98, 89, 91, 75]
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
        lambda row: "Pass" if (row >= 35).all() else "Fail", axis=1
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

st.sidebar.markdown(
    """<div class="brand"><div class="brand-logo">🎓</div>
    <div><div class="brand-name">EduMetrics</div>
    <div class="brand-tag">Academic Analytics</div></div></div>""",
    unsafe_allow_html=True,
)

st.sidebar.markdown('<div class="side-label">Navigation</div>', unsafe_allow_html=True)

page = st.sidebar.radio(
    "NAVIGATION",
    ["Overview", "Student Records", "Analytics", "Student Profile"],
    label_visibility="collapsed",
)

# ==========================================
# 6. ADD AND EDIT STUDENTS
# ==========================================

hero_slot = st.container()

with st.expander("➕  Add or Edit Student Records"):
    st.caption("Manage student information and academic marks.")
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        width="stretch",
        hide_index=True,
    )

# ==========================================
# 7. VALIDATE STUDENT DATA
# ==========================================

valid = edited_df.copy()

for col in subjects + ["Attendance"]:
    valid[col] = pd.to_numeric(valid[col], errors="coerce")

valid = valid.dropna(subset=["Student", "Department"] + subjects + ["Attendance"])

valid = valid[
    valid[subjects + ["Attendance"]].ge(0).all(axis=1)
    & valid[subjects + ["Attendance"]].le(100).all(axis=1)
]

valid["Student"] = valid["Student"].astype(str).str.strip()
valid = valid[valid["Student"] != ""]

if valid.empty:
    st.warning("Please enter valid student records.")
    st.stop()

df = analyze(valid)

# ==========================================
# 8. SEARCH AND FILTERS
# ==========================================

st.sidebar.markdown('<div class="side-label">Filter Students</div>', unsafe_allow_html=True)

departments = st.sidebar.multiselect(
    "Department",
    sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique()),
)

grades = st.sidebar.multiselect(
    "Grade",
    sorted(df["Grade"].unique()),
    default=sorted(df["Grade"].unique()),
)

st.sidebar.markdown(
    '<div class="side-label" style="margin-top:28px">About</div>'
    '<div style="color:#8A93AB;font-size:.82rem;line-height:1.5">'
    'Monitor student performance, grades and attendance in one place.</div>',
    unsafe_allow_html=True,
)

filtered = df[
    df["Department"].isin(departments) & df["Grade"].isin(grades)
].copy()

if filtered.empty:
    st.warning("No students match the selected filters.")
    st.stop()

# ==========================================
# 9. PAGE HEADER
# ==========================================

HEADERS = {
    "Overview": ("Dashboard", "Performance Overview",
                 "Monitor academic progress, discover insights, improve outcomes."),
    "Student Records": ("Directory", "Student Database",
                        "Search, sort and export every student record."),
    "Analytics": ("Insights", "Academic Analytics",
                  "Compare departments, subjects and attendance patterns."),
    "Student Profile": ("Profile", "Individual Student Profile",
                        "A focused view of one student's academic standing."),
}

with hero_slot:
    hero(*HEADERS[page])

# ==========================================
# 10. OVERVIEW DASHBOARD
# ==========================================

if page == "Overview":

    total = len(filtered)
    average = filtered["Average"].mean()
    passed = (filtered["Result"] == "Pass").sum()
    pass_rate = passed / total * 100
    attendance = filtered["Attendance"].mean()

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Total Students", total, "In current selection", "👥", "#8B93FF")
    kpi(c2, "Average Score", f"{average:.1f}%", "Across all subjects", "📈", "#5EEAD4")
    kpi(c3, "Pass Rate", f"{pass_rate:.1f}%", f"{passed} of {total} passed", "✅", "#F5B971")
    kpi(c4, "Avg Attendance", f"{attendance:.1f}%", "Mean attendance", "🗓️", "#F58BA5")

    left, right = st.columns(2)

    with left:
        section("Subject Performance")
        subject_avg = filtered[subjects].mean().reset_index()
        subject_avg.columns = ["Subject", "Average Marks"]
        fig = px.bar(subject_avg, x="Subject", y="Average Marks",
                     color="Subject", color_discrete_sequence=PALETTE,
                     text=subject_avg["Average Marks"].round(1))
        fig.update_traces(textposition="outside", marker_cornerradius=8,
                          textfont=dict(color="#E6E9F2"))
        fig.update_yaxes(range=[0, 110])
        st.plotly_chart(style_fig(fig, legend=False), width="stretch")

    with right:
        section("Grade Distribution")
        grade_count = filtered["Grade"].value_counts().reset_index()
        grade_count.columns = ["Grade", "Students"]
        fig = px.pie(grade_count, names="Grade", values="Students",
                     hole=0.68, color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="label+percent", textfont_size=12,
                          marker=dict(line=dict(color="#0A0E1A", width=3)))
        fig.add_annotation(text=f"<b>{total}</b><br><span style='font-size:11px'>students</span>",
                           showarrow=False, font=dict(size=24, color="#fff"))
        st.plotly_chart(style_fig(fig), width="stretch")

    section("🏆 Top 5 Performers")
    top = filtered.nlargest(5, "Average")
    st.dataframe(
        top[["Student", "Department", "Average", "Grade", "Attendance"]],
        width="stretch", hide_index=True,
        column_config={
            "Average": st.column_config.ProgressColumn(
                "Average", min_value=0, max_value=100, format="%.1f"),
            "Attendance": st.column_config.ProgressColumn(
                "Attendance", min_value=0, max_value=100, format="%d%%"),
        },
    )

    section("Students Needing Attention")
    low = filtered[(filtered["Attendance"] < 75) | (filtered["Average"] < 50)]

    if low.empty:
        st.success("No students currently need attention.")
    else:
        st.dataframe(
            low[["Student", "Average", "Grade", "Attendance"]],
            width="stretch", hide_index=True,
            column_config={
                "Average": st.column_config.NumberColumn("Average", format="%.1f"),
                "Attendance": st.column_config.NumberColumn("Attendance", format="%d%%"),
            },
        )

# ==========================================
# 11. STUDENT RECORDS
# ==========================================

elif page == "Student Records":

    f1, f2 = st.columns([2, 1])
    search = f1.text_input("Search Student Name", placeholder="Type a name…")
    sort_by = f2.selectbox("Sort By", ["Average", "Attendance", "Student"])

    records = filtered.copy()
    if search:
        records = records[records["Student"].str.contains(search, case=False, na=False)]

    records = records.sort_values(sort_by, ascending=False)

    st.caption(f"{len(records)} student(s) shown")

    st.dataframe(
        records, width="stretch", hide_index=True,
        column_config={
            "Average": st.column_config.NumberColumn("Average", format="%.1f"),
            "Percentage": st.column_config.NumberColumn("Percentage", format="%.1f%%"),
            "Attendance": st.column_config.ProgressColumn(
                "Attendance", min_value=0, max_value=100, format="%d%%"),
        },
    )

    st.download_button(
        "⬇  Download Student Records",
        records.to_csv(index=False).encode("utf-8"),
        "EduMetrics_Records.csv",
        "text/csv",
    )

# ==========================================
# 12. ACADEMIC ANALYTICS
# ==========================================

elif page == "Analytics":

    left, right = st.columns(2)

    with left:
        section("Department Comparison")
        dept = filtered.groupby("Department")[subjects].mean().reset_index()
        fig = px.bar(dept, x="Department", y=subjects, barmode="group",
                     color_discrete_sequence=PALETTE)
        fig.update_traces(marker_cornerradius=6)
        st.plotly_chart(style_fig(fig), width="stretch")

    with right:
        section("Marks vs Attendance")
        fig = px.scatter(filtered, x="Attendance", y="Average",
                         color="Department", hover_name="Student",
                         color_discrete_sequence=PALETTE)
        fig.update_traces(marker=dict(size=12, opacity=0.85,
                                      line=dict(width=1.5, color="#0A0E1A")))
        fig = style_fig(fig)
        fig.update_xaxes(title="Attendance %", showgrid=True, gridcolor=GRID)
        fig.update_yaxes(title="Average %")
        st.plotly_chart(fig, width="stretch")

    section("Student Subject Comparison")
    selected_subject = st.selectbox("Select Subject", subjects)

    fig = px.bar(
        filtered.sort_values(selected_subject, ascending=False),
        x="Student", y=selected_subject, color="Department",
        color_discrete_sequence=PALETTE,
    )
    fig.update_traces(marker_cornerradius=6)
    fig = style_fig(fig, height=400)
    fig.update_layout(xaxis_tickangle=-40)
    st.plotly_chart(fig, width="stretch")

    section("Statistical Summary")
    st.dataframe(filtered[subjects].describe().round(2), width="stretch")

# ==========================================
# 13. INDIVIDUAL STUDENT PROFILE
# ==========================================

elif page == "Student Profile":

    selected = st.selectbox("Choose Student", filtered["Student"].tolist())
    person = filtered[filtered["Student"] == selected].iloc[0]

    initials = "".join(w[0] for w in selected.split()[:2]).upper()
    result_cls = "b-ok" if person["Result"] == "Pass" else "b-bad"
    att_cls = "b-warn" if person["Attendance"] < 75 else "b-ok"
    att_txt = "Low attendance" if person["Attendance"] < 75 else "Good attendance"

    st.markdown(
        f"""<div class="profile-card"><div class="avatar">{initials}</div>
        <div style="flex:1"><div class="p-name">{selected}</div>
        <div class="p-meta">Department of {person['Department']}</div></div>
        <div><span class="badge {result_cls}">{person['Result']}</span>
        <span class="badge {att_cls}">{att_txt}</span></div></div>""",
        unsafe_allow_html=True,
    )

    st.write("")
    a, b, c = st.columns(3)
    kpi(a, "Average Marks", f"{person['Average']:.1f}%", "All subjects", "📈", "#8B93FF")
    kpi(b, "Grade", person["Grade"], "Overall standing", "🏅", "#5EEAD4")
    kpi(c, "Attendance", f"{person['Attendance']:.0f}%", "Class presence", "🗓️", "#F5B971")

    section("Subject-wise Performance")

    profile_data = pd.DataFrame({
        "Subject": subjects,
        "Marks": [person[s] for s in subjects],
    })
    fig = px.bar(profile_data, x="Subject", y="Marks", color="Subject",
                 color_discrete_sequence=PALETTE, text="Marks")
    fig.update_traces(textposition="outside", marker_cornerradius=8,
                      textfont=dict(color="#E6E9F2"))
    fig.update_yaxes(range=[0, 110])
    st.plotly_chart(style_fig(fig, legend=False), width="stretch")

    section("Insights")

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

    st.write("")
    st.download_button(
        "⬇  Download Individual Report",
        pd.DataFrame([person]).to_csv(index=False).encode("utf-8"),
        f"{selected.replace(' ', '_')}_Report.csv",
        "text/csv",
    )

# ==========================================
# 14. FOOTER
# ==========================================

st.markdown(
    '<div class="foot">© 2026 EduMetrics · Student Performance Intelligence System<br>'
    'Built with Python · Streamlit · Pandas · Plotly</div>',
    unsafe_allow_html=True,
)
