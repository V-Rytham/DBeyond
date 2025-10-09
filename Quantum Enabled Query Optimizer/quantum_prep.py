import numpy as np

class QuantumPrep:
    def __init__(self):
        self.feature_keys = ['joins', 'subqueries', 'aggregations', 'group_by', 'having', 'analytical_fn', 'length']

    def normalize_features(self, features):
        vector = []
        for key in self.feature_keys:
            val = features.get(key, 0)
            if isinstance(val, bool):
                val = 1 if val else 0
            vector.append(val)

        vector = np.array(vector, dtype=float)

        # Normalization to unit vector (quantum state representation)
        norm = np.linalg.norm(vector)
        if norm == 0:
            norm = 1
        normalized_vector = vector / norm
        return normalized_vector.tolist()

    def estimate_qubits(self, features):
        score = features.get("complexity_score", 0)
        if score <= 2:
            return 3
        elif score <= 5:
            return 5
        else:
            return 7

    def readiness_score(self, normalized_vector):
        # A heuristic: more uniform vectors are more "quantum-ready"
        entropy = -sum([x*np.log2(x+1e-9) for x in normalized_vector])
        readiness = np.clip(entropy / np.log2(len(normalized_vector)), 0, 1)
        return round(readiness, 3)

    def prepare_quantum_state(self, features):
        normalized_vector = self.normalize_features(features)
        qubits = self.estimate_qubits(features)
        readiness = self.readiness_score(normalized_vector)

        return {
            "quantum_state": normalized_vector,
            "estimated_qubits": qubits,
            "readiness_score": readiness
        }
