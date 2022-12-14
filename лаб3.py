import numpy as np


def main():

    systemCoefficients = np.matrix([
        [26.3, 7.11, 0, 0, 0],
        [-2.9, 9.3, 2.4, 0, 0],
        [0, -2.2, -15, -3.4, 0],
        [0, 0, 6.8, 17.8, 6.3],
        [0, 0, 0, 1.6, 2.1]
    ])

    systemMembers = np.array([
        -15.09,
        -101.58,
        -40.8,
        79.26,
        -2.5
    ])
    print(f'\nИсходная матрица:\n{systemCoefficients}\n')

    lowerDiagonal = np.diag(systemCoefficients, -1)
    lowerDiagonal = np.insert(lowerDiagonal, 0, 0)
    upperDiagonal = np.diag(systemCoefficients, 1)
    upperDiagonal = np.append(upperDiagonal, 0)

    print('Нижняя побочная диагональ =', lowerDiagonal)
    print('Главная диагональ =', mainDiagonal := np.diag(systemCoefficients))
    print('Верхняя побочная диагональ =', upperDiagonal, '\n')

    for i in range(5):
        print(
            f'Диагональное преобладание в{"о" if i == 1 else ""} {i + 1} строке {"" if (abs(mainDiagonal[i]) >= abs(lowerDiagonal[i]) + abs(upperDiagonal[i])) else "не "}выполняется')
    print('\n')

    alphaCoefficient = np.zeros(5)
    bettaCoefficient = np.zeros(5)

    alphaCoefficient[0] = -upperDiagonal[0] / mainDiagonal[0]
    bettaCoefficient[0] = systemMembers[0] / mainDiagonal[0]

    for i in range(1, 5):
        alphaCoefficient[i] = -upperDiagonal[i] / (lowerDiagonal[i] * alphaCoefficient[i - 1] + mainDiagonal[i])
        bettaCoefficient[i] = (systemMembers[i] - lowerDiagonal[i] * bettaCoefficient[i - 1]) / (lowerDiagonal[i] * alphaCoefficient[i - 1] + mainDiagonal[i])

    print('Коэффициенты a =', alphaCoefficient)
    print('Коэффициенты b =', bettaCoefficient, '\n')

    X = np.zeros(5)

    X[4] = (systemMembers[4] - lowerDiagonal[4] * bettaCoefficient[3]) \
           / (lowerDiagonal[4] * alphaCoefficient[3] + mainDiagonal[4])

    for i in range(3, -1, -1):
        X[i] = alphaCoefficient[i] * X[i + 1] + bettaCoefficient[i]

    X = np.transpose(np.matrix(X))

    print('X =', X, '\n')
    print(f'Проверим полученные X:\n',  systemCoefficients.dot(X))


    recalculatedMembers = systemCoefficients * X
    deltaOfRecalculatedMembers = np.abs(np.transpose(np.matrix(systemMembers)) - recalculatedMembers)
    print("\ndelta d =", deltaOfRecalculatedMembers)
    absoluteError = np.linalg.norm(deltaOfRecalculatedMembers)
    print("\nАбсолютная погрешность =", absoluteError)
    relativeError = absoluteError / np.linalg.norm(systemMembers)
    print("Относительная погрешность =", relativeError)


if __name__ == "__main__":
    main()
