import numpy as np
import pandas as pd


def factor_analyzer(X, factor_number, SummaryNeeded):
    # calculate X mean and center X
    X_mean = np.mean(X.T, axis=1)
    X_center = X - X_mean
    X_covariance = np.cov(X_center.T)

    # produce eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(X_covariance)
    eigenvalues_selected = eigenvalues[:factor_number]  # keep selected eigenvalues only

    # calculate variance(X) matrix by AT and A without dimension reduction
    eigenvalues_diagonal_total = np.zeros((eigenvalues.shape[0], eigenvalues.shape[0]), float)
    np.fill_diagonal(eigenvalues_diagonal_total, eigenvalues)
    eigenvalues_diagonal_total_sqrt = np.sqrt(eigenvalues_diagonal_total)
    A_transpose_full = eigenvectors.dot(eigenvalues_diagonal_total_sqrt)
    A_full = eigenvalues_diagonal_total_sqrt.dot(eigenvectors.T)
    X_variance = np.diag(np.diag(A_transpose_full.dot(A_full)))

    # produce eigenvalues diagonal matrix and eigenvalues diagonal matrix (by given factors needed)
    eigenvalues_diagonal = np.zeros((factor_number, factor_number), float)
    np.fill_diagonal(eigenvalues_diagonal, eigenvalues[:factor_number])

    # produce A_transpose and A
    eigenvalues_diagonal_sqrt = np.sqrt(eigenvalues_diagonal)
    A_transpose = eigenvectors[:, :factor_number].dot(eigenvalues_diagonal_sqrt)
    A = eigenvalues_diagonal_sqrt.dot(eigenvectors[:, :factor_number].T)
    #     print('A', A.shape)
    #     print('A_transpose', A_transpose.shape)

    # calculate Psi and factor
    Psi = X_variance - A_transpose.dot(A)
    #     print('Psi', Psi.shape)
    Psi_inverse = np.linalg.inv(Psi)
    #     print('X', X.shape)
    inner = np.linalg.inv(A.dot(Psi_inverse).dot(A_transpose))
    factor = X.dot(Psi_inverse).dot(A_transpose).dot(inner)

    # calculate communality vector
    communality_vector = A_transpose.dot(A)

    if SummaryNeeded:
        # print out summary
        print("========================== Output Summary ==========================\n【The loading matrix A】\n", A,
              "\n\n【Factor Matrix】\n", factor,
              "\n\n【Communality Matrix】\n", communality_vector,
              "\n\n【Uniqueness Vector】\n", Psi, "\n\n")

        # calculate contribution of each factor
        print("【Contribution of each factor】")
        explainable_ratio_list = []
        for i, j in enumerate(eigenvalues_selected):
            varianve_total = np.sum(X_variance)
            factor_contribution = np.around((j / varianve_total), decimals=6)
            explainable_ratio_list.append(factor_contribution)
            print('Contribution of factor', (i + 1), 'is', factor_contribution)
        print("\n")

        # calculate contribution
        total_explainable_ratio = 0
        components_needed_list = []
        for i, j in enumerate(explainable_ratio_list):
            total_explainable_ratio += j
            if total_explainable_ratio >= 0.9:
                if len(components_needed_list) < 5:
                    components_needed_list.append(i + 1)
                    print('90%:', str(i + 1), 'factors needed.')
                break
            elif total_explainable_ratio >= 0.8:
                if len(components_needed_list) < 4:
                    components_needed_list.append(i + 1)
                    print('80%:', str(i + 1), 'factors needed.')
            elif total_explainable_ratio >= 0.7:
                if len(components_needed_list) < 3:
                    components_needed_list.append(i + 1)
                    print('70%:', str(i + 1), 'factors needed.')
            elif total_explainable_ratio >= 0.6:
                if len(components_needed_list) < 2:
                    components_needed_list.append(i + 1)
                    print('60%:', str(i + 1), 'factors needed.')
            elif total_explainable_ratio >= 0.5:
                if len(components_needed_list) < 1:
                    components_needed_list.append(i + 1)
                    print('50%:', str(i + 1), 'factors needed.')

    return factor, A, A_transpose, Psi


if __name__ == '__main__':
    AutoMPG = pd.read_csv('./data/AutoMPG.csv')
    factor, A, A_transpose, Psi = factor_analyzer(AutoMPG, 2)
    ATA = A_transpose.dot(A) + Psi
    cov = np.cov(AutoMPG.to_numpy().T)
    print(ATA - cov)
