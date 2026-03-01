import numpy as np

def ahp_weights(matrix: np.ndarray) -> np.ndarray:
    """Compute AHP weights using geometric mean method."""
    geom_means = np.prod(matrix, axis=1) ** (1.0 / matrix.shape[0])
    weights = geom_means / np.sum(geom_means)
    return weights

def consistency_ratio(matrix: np.ndarray) -> float:
    """Compute AHP consistency ratio CR."""
    n = matrix.shape[0]
    eigvals, _ = np.linalg.eig(matrix)
    max_eig = np.max(np.real(eigvals))
    ci = (max_eig - n) / (n - 1) if n > 1 else 0.0

    ri_dict = {1:0.00,2:0.00,3:0.58,4:0.90,5:1.12,6:1.24,7:1.32,8:1.41,9:1.45,10:1.49}
    ri = ri_dict.get(n, 1.49)
    cr = ci / ri if ri != 0 else 0.0
    return float(cr)

def score_alternatives(scores_matrix: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Normalize scores by column max and compute final score."""
    normalized = scores_matrix / np.max(scores_matrix, axis=0, keepdims=True)
    final = normalized.dot(weights)
    return final