import streamlit as st
import numpy as np
from ahp import ahp_weights, consistency_ratio, score_alternatives

st.set_page_config(page_title="SIAD - AHP Decision Support", layout="wide")
st.title("📌 SIAD - AHP Decision Support (Streamlit)")

st.markdown("هذا تطبيق بسيط لاختيار أفضل بديل باستعمال **AHP** (Analytic Hierarchy Process).")

# Inputs
st.sidebar.header("⚙️ إعدادات")
n_alt = st.sidebar.number_input("عدد البدائل (Alternatives)", min_value=2, max_value=10, value=3)
n_crit = st.sidebar.number_input("عدد المعايير (Criteria)", min_value=2, max_value=10, value=3)

alts = [st.sidebar.text_input(f"بديل {i+1}", f"A{i+1}") for i in range(n_alt)]
crits = [st.sidebar.text_input(f"معيار {j+1}", f"C{j+1}") for j in range(n_crit)]

st.subheader("1) مصفوفة المقارنات الزوجية للمعايير (Pairwise Comparison Matrix)")

st.info("استعمل سلم AHP: 1 (متساوي) ... 3 (أفضل قليلاً) ... 5 ... 7 ... 9 (أفضل بزاف).")

matrix = np.ones((n_crit, n_crit), dtype=float)

cols = st.columns(n_crit)
for i in range(n_crit):
    for j in range(i + 1, n_crit):
        val = st.number_input(
            f"{crits[i]} مقارنة مع {crits[j]}",
            min_value=1.0, max_value=9.0, value=1.0, step=1.0
        )
        matrix[i, j] = val
        matrix[j, i] = 1.0 / val

weights = ahp_weights(matrix)
cr = consistency_ratio(matrix)

st.write("✅ **أوزان المعايير (Weights):**")
st.table({crits[i]: float(weights[i]) for i in range(n_crit)})

if cr <= 0.1:
    st.success(f"Consistency Ratio (CR) = {cr:.3f} ✅ (مقبول)")
else:
    st.warning(f"Consistency Ratio (CR) = {cr:.3f} ⚠️ (حاول حسن المقارنات باش تولي CR <= 0.1)")

st.subheader("2) تنقيط البدائل حسب كل معيار (Scores)")
scores = np.zeros((n_alt, n_crit), dtype=float)

for i, alt in enumerate(alts):
    st.markdown(f"### البديل: **{alt}**")
    row = []
    for j, crit in enumerate(crits):
        s = st.slider(f"Score ديال {alt} فـ {crit}", 1, 10, 5)
        scores[i, j] = s

if st.button("📊 احسب النتيجة النهائية"):
    final = score_alternatives(scores, weights)

    results = sorted(zip(alts, final), key=lambda x: x[1], reverse=True)
    st.subheader("🏁 النتائج")
    st.table({"Alternative": [r[0] for r in results], "Final Score": [float(r[1]) for r in results]})

    st.success(f"✅ أفضل اختيار هو: **{results[0][0]}**")