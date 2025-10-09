import streamlit as st
import sqlparse
from sqlparse.sql import Where, Function, Parenthesis
from sqlparse.tokens import Keyword
import quantum_prep
from quantum_prep import QuantumPrep

# -------------------------------
# Query Feature Extractor Class
# -------------------------------
class QueryFeatureExtractor:
    def __init__(self):
        self.weights = {
            'joins': 2,
            'subqueries': 3,
            'aggregations': 1,
            'group_by': 1,
            'having': 2,
            'analytical_fn': 3,
            'length': 1
        }
        self.threshold = 4

    def extract_features(self, query):
        query = query.strip()
        parsed = sqlparse.parse(query)

        if not parsed:
            return {"error": "Invalid SQL query"}

        stmt = parsed[0]

        features = {
            'joins': 0,
            'subqueries': 0,
            'aggregations': 0,
            'group_by': False,
            'having': False,
            'analytical_fn': False,
            'length': len(query)
        }

        for token in stmt.tokens:
            if token.ttype is Keyword and "JOIN" in token.value.upper():
                features['joins'] += 1

            if isinstance(token, Where):
                if "EXISTS" in token.value.upper() or "IN (" in token.value.upper():
                    features['subqueries'] += 1
            if isinstance(token, Parenthesis):
                if "SELECT" in token.value.upper():
                    features['subqueries'] += 1

            if isinstance(token, Function):
                func_name = token.get_name().upper() if token.get_name() else ""
                if func_name in ["COUNT", "SUM", "AVG", "MAX", "MIN"]:
                    features['aggregations'] += 1
                elif func_name in ["RANK", "DENSE_RANK", "ROW_NUMBER"]:
                    features['analytical_fn'] = True

            if token.ttype is Keyword and "GROUP BY" in token.value.upper():
                features['group_by'] = True
            if token.ttype is Keyword and "HAVING" in token.value.upper():
                features['having'] = True

        return features

    def compute_complexity(self, features):
        score = 0
        for key, weight in self.weights.items():
            val = features[key]
            if isinstance(val, bool):
                val = 1 if val else 0
            if key == 'length' and val <= 150:
                continue
            score += val * weight
        return score

    def classify(self, query):
        features = self.extract_features(query)
        if "error" in features:
            return features
        score = self.compute_complexity(features)
        features['complexity_score'] = score
        features['classification'] = "Complex" if score >= self.threshold else "Simple"
        return features


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Quantum Query Analyzer", page_icon="⚛️", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background-color: #0f172a;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    .stTextArea label {
        color: #a5b4fc;
        font-weight: 600;
    }
    .result-box {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        margin-top: 10px;
        box-shadow: 0 4px 10px rgba(255,255,255,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("⚛️ Quantum Query Analyzer")
st.caption("A modern SQL complexity visualizer for your Quantum-Enabled Query Optimizer")

extractor = QueryFeatureExtractor()

query = st.text_area("📝 Enter your SQL query below:", height=120)

if st.button("🔍 Analyze Query"):
    if not query.strip():
        st.warning("Please enter a valid SQL query.")
    else:
        result = extractor.classify(query)

        if "error" in result:
            st.error(result["error"])
        else:
            st.markdown("### 🧠 Query Complexity Report")
            st.markdown(f"<div class='result-box'>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Classification", result['classification'])
                st.metric("Complexity Score", result['complexity_score'])
            with col2:
                st.metric("Query Length", result['length'])
                st.metric("Joins", result['joins'])

            st.divider()
            st.markdown("**Feature Breakdown:**")
            st.json({
                "Subqueries": result["subqueries"],
                "Aggregations": result["aggregations"],
                "Group By": result["group_by"],
                "Having": result["having"],
                "Analytical Functions": result["analytical_fn"]
            })

            st.markdown("</div>", unsafe_allow_html=True)
            qprep = QuantumPrep()
            quantum_info = qprep.prepare_quantum_state(result)

            st.markdown("### ⚛️ Quantum Prep Stage")
            st.json(quantum_info)