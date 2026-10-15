# =============================================================================
#  SafeWork Analytics – AI-Powered Workplace Safety Analytics Dashboard
#  Author  : Anjali Kumari, Bakhtiyarpur College of Engineering
#  Purpose : Analyse fictional workplace safety reports and surface trends
#  NOTE    : All data is completely fictional. No real persons are represented.
#            This tool does not predict danger, prove misconduct, or guarantee
#            safety. Suggestions are general best-practice guidance only.
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import datetime

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SafeWork Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS – purple / navy / white theme ──────────────────────────────────
st.markdown("""
<style>
/* ── Global background ── */
.stApp { background-color: #0f172a; color: #e2e8f0; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #1e1b4b;
    border-right: 1px solid #312e81;
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* ── KPI card ── */
.kpi-card {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    border: 1px solid #4c1d95;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    margin-bottom: 12px;
}
.kpi-value {
    font-size: 2.4rem;
    font-weight: 700;
    color: #a78bfa;
    line-height: 1.1;
}
.kpi-label {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 4px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── Section headings ── */
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #a78bfa;
    border-left: 4px solid #7c3aed;
    padding-left: 10px;
    margin: 24px 0 12px 0;
}

/* ── Suggestion cards ── */
.suggestion-card {
    background-color: #1e1b4b;
    border-left: 4px solid #7c3aed;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
    color: #e2e8f0;
    font-size: 0.92rem;
    line-height: 1.6;
}

/* ── Disclaimer banner ── */
.disclaimer {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 8px;
}

/* ── AI section ── */
.ai-box {
    background-color: #0f172a;
    border: 1px dashed #7c3aed;
    border-radius: 10px;
    padding: 20px;
    margin-top: 8px;
}

/* ── Dataframe text ── */
.stDataFrame { background-color: #1e1b4b; }

/* ── Multiselect / select tags ── */
span[data-baseweb="tag"] { background-color: #4c1d95 !important; }
</style>
""", unsafe_allow_html=True)


# ── Helper: load data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str = "data/safety_reports.csv") -> pd.DataFrame:
    """Load the safety reports CSV and validate required columns."""
    required_cols = {
        "report_id", "month", "issue_category",
        "workplace_area", "severity", "resolution_status", "description",
    }
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        st.error("❌ Dataset not found. Please make sure `data/safety_reports.csv` exists.")
        st.stop()

    missing = required_cols - set(df.columns.str.lower())
    if missing:
        st.error(f"❌ The CSV is missing columns: {missing}")
        st.stop()

    df.columns = df.columns.str.lower().str.strip()
    df["month"] = df["month"].str.strip()
    df["issue_category"] = df["issue_category"].str.strip()
    df["severity"] = df["severity"].str.strip()
    df["resolution_status"] = df["resolution_status"].str.strip()
    return df


# ── Month ordering helper ─────────────────────────────────────────────────────
MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def sort_months(months: list) -> list:
    return sorted(months, key=lambda m: MONTH_ORDER.index(m) if m in MONTH_ORDER else 99)


# ── Chart colour palette ──────────────────────────────────────────────────────
PALETTE = ["#7c3aed", "#4f46e5", "#0ea5e9", "#8b5cf6", "#6366f1",
           "#a78bfa", "#38bdf8", "#c4b5fd", "#818cf8", "#e879f9"]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0", size=12),
    margin=dict(t=40, b=40, l=20, r=20),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0")),
)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────────────────────────────────────
def main():
    df_raw = load_data()

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 4px 0;'>
        <span style='font-size:2.6rem; font-weight:800; color:#a78bfa;'>🛡️ SafeWork Analytics</span><br>
        <span style='font-size:1.1rem; color:#94a3b8;'>
            AI-Powered Workplace Safety Analytics Dashboard
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='disclaimer'>
        ⚠️ <strong>Disclaimer:</strong> All data in this dashboard is <strong>completely fictional</strong>
        and does not represent any real individuals, organisations, or incidents.
        This tool does <strong>not</strong> predict danger, prove misconduct, or guarantee safety.
        Preventive suggestions are general best-practice guidance only.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Sidebar filters ───────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 🔍 Filters")
        st.markdown("Use the filters below to explore specific subsets of the data.")

        all_months = sort_months(df_raw["month"].unique().tolist())
        sel_months = st.multiselect("📅 Month", options=all_months, default=all_months)

        all_cats = sorted(df_raw["issue_category"].unique().tolist())
        sel_cats = st.multiselect("📋 Issue Category", options=all_cats, default=all_cats)

        all_sev = sorted(df_raw["severity"].unique().tolist(),
                         key=lambda x: ["Low", "Medium", "High"].index(x) if x in ["Low", "Medium", "High"] else 99)
        sel_sev = st.multiselect("⚡ Severity", options=all_sev, default=all_sev)

        all_status = sorted(df_raw["resolution_status"].unique().tolist())
        sel_status = st.multiselect("✅ Resolution Status", options=all_status, default=all_status)

        st.markdown("---")
        st.markdown(
            "<div style='font-size:0.75rem; color:#64748b;'>"
            "SafeWork Analytics · v1.0<br>"
            "Anjali Kumari · BCE"
            "</div>",
            unsafe_allow_html=True,
        )

    # ── Apply filters ─────────────────────────────────────────────────────────
    # Guard: if all filter lists are empty, show a warning and stop
    if not sel_months or not sel_cats or not sel_sev or not sel_status:
        st.warning("⚠️ No data matches your current filters. Please adjust the sidebar selections.")
        st.stop()

    df = df_raw[
        df_raw["month"].isin(sel_months) &
        df_raw["issue_category"].isin(sel_cats) &
        df_raw["severity"].isin(sel_sev) &
        df_raw["resolution_status"].isin(sel_status)
    ].copy()

    if df.empty:
        st.warning("⚠️ No records match the selected filters. Please broaden your selections.")
        st.stop()

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>📊 Key Metrics</div>", unsafe_allow_html=True)

    total        = len(df)
    unresolved   = len(df[df["resolution_status"] == "Unresolved"])
    high_sev     = len(df[df["severity"] == "High"])
    resolved_pct = round((len(df[df["resolution_status"] == "Resolved"]) / total) * 100, 1) if total > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, value, label in [
        (c1, total,          "Total Reports"),
        (c2, unresolved,     "Unresolved Reports"),
        (c3, high_sev,       "High-Severity Reports"),
        (c4, f"{resolved_pct}%", "Resolution Rate"),
    ]:
        col.markdown(
            f"<div class='kpi-card'>"
            f"<div class='kpi-value'>{value}</div>"
            f"<div class='kpi-label'>{label}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── Charts ────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>📈 Interactive Charts</div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    # Chart 1 – Incidents by Category (horizontal bar)
    with col_left:
        cat_counts = df["issue_category"].value_counts().reset_index()
        cat_counts.columns = ["Issue Category", "Count"]
        fig1 = px.bar(
            cat_counts,
            x="Count", y="Issue Category",
            orientation="h",
            title="Incidents by Category",
            color="Count",
            color_continuous_scale=["#4f46e5", "#7c3aed", "#a78bfa"],
            text="Count",
        )
        fig1.update_traces(textposition="outside", textfont_color="#e2e8f0")
        fig1.update_layout(**CHART_LAYOUT, coloraxis_showscale=False,
                           yaxis=dict(categoryorder="total ascending", gridcolor="#1e293b"),
                           xaxis=dict(gridcolor="#1e293b"))
        st.plotly_chart(fig1, use_container_width=True)

    # Chart 2 – Monthly Trend (line)
    with col_right:
        month_counts = df.groupby("month").size().reset_index(name="Reports")
        month_counts["month"] = pd.Categorical(
            month_counts["month"], categories=MONTH_ORDER, ordered=True
        )
        month_counts = month_counts.sort_values("month")
        fig2 = px.line(
            month_counts,
            x="month", y="Reports",
            title="Monthly Trend of Reports",
            markers=True,
            color_discrete_sequence=["#a78bfa"],
        )
        fig2.update_traces(line_width=3, marker_size=8)
        fig2.update_layout(**CHART_LAYOUT,
                           xaxis=dict(gridcolor="#1e293b"),
                           yaxis=dict(gridcolor="#1e293b"))
        st.plotly_chart(fig2, use_container_width=True)

    col_left2, col_right2 = st.columns(2)

    # Chart 3 – Severity Distribution (pie)
    with col_left2:
        sev_order   = ["High", "Medium", "Low"]
        sev_colors  = {"High": "#7c3aed", "Medium": "#4f46e5", "Low": "#0ea5e9"}
        sev_counts  = df["severity"].value_counts().reindex(sev_order).dropna().reset_index()
        sev_counts.columns = ["Severity", "Count"]
        fig3 = px.pie(
            sev_counts,
            names="Severity", values="Count",
            title="Severity Distribution",
            color="Severity",
            color_discrete_map=sev_colors,
            hole=0.35,
        )
        fig3.update_traces(textfont_color="#ffffff", textfont_size=13)
        fig3.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig3, use_container_width=True)

    # Chart 4 – Resolution Status (donut)
    with col_right2:
        res_counts = df["resolution_status"].value_counts().reset_index()
        res_counts.columns = ["Status", "Count"]
        res_colors = {"Resolved": "#10b981", "Unresolved": "#7c3aed"}
        fig4 = px.pie(
            res_counts,
            names="Status", values="Count",
            title="Resolution Status",
            color="Status",
            color_discrete_map=res_colors,
            hole=0.5,
        )
        fig4.update_traces(textfont_color="#ffffff", textfont_size=13)
        fig4.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig4, use_container_width=True)

    # ── Preventive Suggestions ────────────────────────────────────────────────
    st.markdown("<div class='section-title'>💡 Preventive Suggestions</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#94a3b8; font-size:0.88rem;'>"
        "The following suggestions are automatically generated based on the patterns found in the "
        "<strong>currently filtered</strong> data. These are general best-practice recommendations only."
        "</p>",
        unsafe_allow_html=True,
    )

    suggestions = []
    cats_present = df["issue_category"].unique().tolist()
    unresolved_cats = df[df["resolution_status"] == "Unresolved"]["issue_category"].value_counts()

    if "Inadequate Lighting" in cats_present:
        suggestions.append(
            "💡 <strong>Lighting Audit:</strong> Conduct a monthly walkthrough of all premises — "
            "parking lots, stairwells, corridors, and loading areas — to identify and repair non-functional lights. "
            "Consider installing motion-sensor lighting in low-traffic zones."
        )

    if "Unsafe Late-Shift Transport" in cats_present:
        suggestions.append(
            "🚌 <strong>Safe Transport Policy:</strong> Introduce a verified late-shift transport scheme for all "
            "staff working beyond 9 PM. Maintain a register of late workers and assign a dedicated security escort "
            "or cab service. Display emergency contact numbers at all exit points."
        )

    if "Inappropriate Behaviour" in cats_present:
        suggestions.append(
            "🤝 <strong>POSH Compliance:</strong> Ensure the Internal Complaints Committee (ICC) is active and "
            "visible. Conduct mandatory POSH (Prevention of Sexual Harassment) awareness training at least twice "
            "per year. Establish a confidential digital reporting channel."
        )

    if "Lack of Reporting Awareness" in cats_present:
        suggestions.append(
            "📢 <strong>Awareness Campaigns:</strong> Include safety and grievance reporting procedures in all "
            "employee induction programmes. Display poster guides in common areas explaining how to raise a concern "
            "anonymously. Run quarterly awareness drills."
        )

    if "Access Control Concerns" in cats_present:
        suggestions.append(
            "🔐 <strong>Access Control Review:</strong> Schedule monthly tests of all electronic access points. "
            "Implement a visitor management system at reception. Ensure all faulty locks and card readers are "
            "reported and repaired within 24 hours."
        )

    if unresolved > 0:
        top_unresolved = unresolved_cats.idxmax() if not unresolved_cats.empty else "unknown"
        suggestions.append(
            f"⚠️ <strong>Resolution Priority:</strong> {unresolved} report(s) remain unresolved in the current view. "
            f"The most frequent unresolved category is <strong>{top_unresolved}</strong>. "
            "Management should assign an owner and target resolution date for every open report."
        )

    if high_sev > 0:
        suggestions.append(
            f"🚨 <strong>High-Severity Action:</strong> {high_sev} high-severity report(s) are present. "
            "These should be escalated immediately to senior management and the safety committee. "
            "A root-cause analysis should be completed within 48 hours of each report."
        )

    if not suggestions:
        suggestions.append("✅ No specific concerns found for the current filter selection. Continue monitoring regularly.")

    for s in suggestions:
        st.markdown(f"<div class='suggestion-card'>{s}</div>", unsafe_allow_html=True)

    # ── Data Table ────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>📋 Filtered Data Records</div>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:#94a3b8; font-size:0.88rem;'>Showing <strong>{len(df)}</strong> "
        f"record(s) based on current filter selections.</p>",
        unsafe_allow_html=True,
    )

    display_cols = ["report_id", "month", "issue_category", "workplace_area", "severity", "resolution_status"]
    st.dataframe(
        df[display_cols].reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )

    # ── Download Buttons ──────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>⬇️ Download Options</div>", unsafe_allow_html=True)

    dl1, dl2 = st.columns(2)

    # Download 1 – filtered CSV
    csv_buffer = df.to_csv(index=False)
    dl1.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv_buffer,
        file_name="safework_filtered_reports.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # Download 2 – text summary report
    now = datetime.datetime.now().strftime("%d %B %Y, %H:%M")
    summary_lines = [
        "=" * 60,
        "  SAFEWORK ANALYTICS – SUMMARY REPORT",
        f"  Generated on: {now}",
        "=" * 60,
        "",
        "DISCLAIMER: All data is fictional. This report does not",
        "predict danger, prove misconduct, or guarantee safety.",
        "",
        "── ACTIVE FILTERS ─────────────────────────────────────",
        f"  Months           : {', '.join(sel_months)}",
        f"  Issue Categories : {', '.join(sel_cats)}",
        f"  Severity Levels  : {', '.join(sel_sev)}",
        f"  Resolution Status: {', '.join(sel_status)}",
        "",
        "── KEY METRICS ─────────────────────────────────────────",
        f"  Total Reports         : {total}",
        f"  Unresolved Reports    : {unresolved}",
        f"  High-Severity Reports : {high_sev}",
        f"  Resolution Rate       : {resolved_pct}%",
        "",
        "── INCIDENTS BY CATEGORY ───────────────────────────────",
    ]
    for _, row in df["issue_category"].value_counts().items():
        pass
    for cat, cnt in df["issue_category"].value_counts().items():
        summary_lines.append(f"  {cat:<35} : {cnt}")

    summary_lines += [
        "",
        "── PREVENTIVE SUGGESTIONS ──────────────────────────────",
    ]
    # Strip HTML tags for plain text
    import re
    for s in suggestions:
        clean = re.sub(r"<[^>]+>", "", s)
        summary_lines.append(f"  • {clean}")

    summary_lines += ["", "=" * 60, "  End of Report", "=" * 60]
    summary_text = "\n".join(summary_lines)

    dl2.download_button(
        label="📄 Download Summary Report (TXT)",
        data=summary_text,
        file_name="safework_summary_report.txt",
        mime="text/plain",
        use_container_width=True,
    )

    # ── Optional AI Feature ───────────────────────────────────────────────────
    st.markdown("<div class='section-title'>🤖 Optional AI Feature – Report Categoriser</div>",
                unsafe_allow_html=True)

    st.markdown("""
    <div class='ai-box'>
        <p style='color:#a78bfa; font-weight:600; margin-bottom:6px;'>
            ✨ Keyword-Based Report Category Suggester
        </p>
        <p style='color:#94a3b8; font-size:0.85rem; margin-bottom:14px;'>
            Type a brief description of a safety concern below.
            The tool will suggest the most likely issue category using keyword matching —
            <strong>no API key or internet connection required</strong>.
        </p>
    """, unsafe_allow_html=True)

    user_input = st.text_area(
        "Describe the safety concern:",
        placeholder="e.g. The corridor near the exit has no lights and feels unsafe at night...",
        height=100,
        key="ai_input",
    )

    # Input validation
    if st.button("🔍 Suggest Category", key="ai_btn"):
        if not user_input.strip():
            st.warning("⚠️ Please enter a description before clicking Suggest Category.")
        elif len(user_input.strip()) < 10:
            st.warning("⚠️ Description is too short. Please provide at least 10 characters.")
        else:
            text = user_input.lower()

            keyword_map = {
                "Inadequate Lighting": [
                    "light", "dark", "lighting", "bright", "lamp", "bulb",
                    "illuminate", "dim", "visibility", "cctv", "camera",
                ],
                "Unsafe Late-Shift Transport": [
                    "transport", "cab", "late", "shift", "bus", "night",
                    "commute", "travel", "vehicle", "escort", "pickup", "drop",
                ],
                "Inappropriate Behaviour": [
                    "behaviour", "behavior", "harass", "uncomfortable", "stare",
                    "comment", "follow", "intimidat", "pressure", "message",
                    "unwanted", "inappropriate", "abuse",
                ],
                "Lack of Reporting Awareness": [
                    "aware", "report", "complaint", "grievance", "icc",
                    "committee", "know", "training", "inform", "process",
                    "procedure", "induction",
                ],
                "Access Control Concerns": [
                    "access", "card", "lock", "door", "entry", "visitor",
                    "unauthor", "security", "gate", "badge", "swipe", "key",
                ],
            }

            scores = {cat: 0 for cat in keyword_map}
            for cat, keywords in keyword_map.items():
                for kw in keywords:
                    if kw in text:
                        scores[cat] += 1

            best_cat  = max(scores, key=scores.get)
            best_score = scores[best_cat]

            if best_score == 0:
                st.info(
                    "🤔 No clear category match found. "
                    "Try including more specific keywords such as 'lighting', 'transport', "
                    "'behaviour', 'reporting', or 'access'."
                )
            else:
                confidence = "High" if best_score >= 3 else ("Medium" if best_score >= 2 else "Low")
                conf_color = {"High": "#10b981", "Medium": "#f59e0b", "Low": "#ef4444"}[confidence]
                st.markdown(
                    f"<div style='background:#1e1b4b; border-left:4px solid #7c3aed; "
                    f"border-radius:8px; padding:16px; margin-top:8px;'>"
                    f"<p style='color:#a78bfa; font-weight:600; font-size:1rem; margin:0 0 6px 0;'>"
                    f"Suggested Category</p>"
                    f"<p style='color:#e2e8f0; font-size:1.3rem; font-weight:700; margin:0 0 8px 0;'>"
                    f"{best_cat}</p>"
                    f"<p style='color:#94a3b8; font-size:0.82rem; margin:0;'>"
                    f"Confidence: <span style='color:{conf_color}; font-weight:600;'>{confidence}</span> "
                    f"&nbsp;·&nbsp; Keyword matches: {best_score}"
                    f"</p></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<p style='color:#64748b; font-size:0.78rem; margin-top:8px;'>"
                    "ℹ️ This suggestion is based on keyword matching only and may not always be accurate. "
                    "Always verify with a human reviewer."
                    "</p>",
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align:center; color:#334155; font-size:0.78rem; "
        "border-top:1px solid #1e293b; padding-top:16px;'>"
        "SafeWork Analytics · Built with Python, Streamlit & Plotly · "
        "Anjali Kumari, Bakhtiyarpur College of Engineering · "
        "All data is fictional · For educational purposes only"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
