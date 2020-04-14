import numpy as np
import pandas as pd


def factor_analyzer(X, factor_number):
    # calculate X mean and center X
    X_mean = np.mean(X.T, axis=1)
    X_center = X - X_mean
    X_covariance = np.cov(X_center.T)
    # produce eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(X_covariance)
    eigenvalues_selected = eigenvalues[:factor_number]  # keep selected eigenvalues only
    # produce eigenvalues diagonal matrix and eigenvalues diagonal matrix
    eigenvalues_diagonal = np.zeros((factor_number, factor_number), float)
    np.fill_diagonal(eigenvalues_diagonal, eigenvalues[:factor_number])
    # produce A_transpose and A
    eigenvalues_diagonal_sqrt = np.sqrt(eigenvalues_diagonal)
    A_transpose = eigenvectors[:, :factor_number].dot(eigenvalues_diagonal_sqrt)
    A = eigenvalues_diagonal_sqrt.dot(eigenvectors[:, :factor_number].T)
    #     print('A', A.shape)
    #     print('A_transpose', A_transpose.shape)
    # calculate Psi
    Psi = X_covariance - A_transpose.dot(A)
    #     print('Psi', Psi.shape)
    Psi_inverse = np.linalg.inv(Psi)
    #     print(Psi)
    #     print('X', X.shape)
    former = np.linalg.inv(A.dot(Psi_inverse).dot(A_transpose))
    #     factor = X.dot(Psi_inverse).dot(A_transpose).dot(former)
    factor = X.dot(Psi_inverse).dot(A_transpose).dot(former)
    # calculate communality vector
    communality_vector = X_covariance - Psi

    # print out summary
    print("========================== Output Summary ==========================\n【The loading matrix A】\n", A,
          "\n\n【Factor Matrix】\n", factor,
          "\n\n【Communality Matrix】\n", communality_vector,
          "\n\n【Uniqueness Vector】\n", Psi, "\n\n")

    # calculate contribution of each factor
    for i, j in enumerate(eigenvalues_selected):
        covarianve_total = np.sum(X_covariance)
        factor_contribution = np.around((j / covarianve_total), decimals=6)
        print('Contribution of factor', (i + 1), 'is', factor_contribution)

    return factor


if __name__ == '__main__':
    AutoMPG = pd.read_csv('./data/AutoMPG.csv')
    factor = factor_analyzer(AutoMPG, 2)