def auc(pred, label):
    n = len(pred)

    a = 0.
    score_prev = float('-inf')
    fp = tp = 0
    fp_prev = tp_prev = 0

    for i in range(n):
        if pred[i] != score_prev:
            a += trapezoid(fp, fp_prev, tp, tp_prev)
            score_prev = pred[i]
            fp_prev = fp
            tp_prev = tp

        if label[i] == 1.:
            tp += 1
        else:
            fp += 1

    return a, fp, tp, fp_prev, tp_prev


def trapezoid(x1, x2, y1, y2):
    base = abs(x1 - x2)
    height = (y1 + y2) / 2.
    return base * height


def single(pred, label):
    a, fp, tp, fp_prev, tp_prev = auc(pred, label)

    # get()
    a += trapezoid(fp, fp_prev, tp, tp_prev)
    return a / (tp * fp)


def multi(pred, label, sep=2):
    a1, fp1, tp1, fp_prev1, tp_prev1 = auc(pred[:sep], label[:sep])
    a2, fp2, tp2, fp_prev2, tp_prev2 = auc(pred[sep:], label[sep:])

    a1 += trapezoid(fp1, fp_prev1, tp1, tp_prev1)
    a2 += trapezoid(fp2, fp_prev2, tp2, tp_prev2)

    # merge()
    a = (a1 + a2) + trapezoid(fp1 + fp2, fp1, tp1, tp1)

    fp = fp1 + fp2
    tp = tp1 + tp2

    fp_prev = fp1 + fp_prev2
    tp_prev = tp1 + tp_prev2

    a -= trapezoid(fp, fp_prev, tp, tp_prev)

    # get()
    a += trapezoid(fp, fp_prev, tp, tp_prev)
    return a / (tp * fp)


if __name__ == '__main__':
    pred = [.8, .7, .5, .3, .2]
    label = [1, 1, 0, 1, 0]

    print('Single:', single(pred, label))

    for i in range(5):
        print('Multi', i, ':', multi(pred, label, sep=i))
