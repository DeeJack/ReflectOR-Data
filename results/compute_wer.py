# calcola_wer.py
import re


def normalize_text(s):
    s = s.lower()
    s = re.sub(r"\[.*?\]", " ", s)  # rimuovi timestamp
    s = re.sub(r".*\:", " ", s)  # rimuovi timestamp
    s = re.sub(r"[^a-zàèéìòù0-9\'\s]", " ", s)  # lascia lettere, numeri, apostrofo
    s = re.sub(r"\s+", " ", s).strip()
    return s


def wer_stats(ref, hyp):
    r = ref.split()
    h = hyp.split()
    n = len(r)
    # matrice DP
    D = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(1, len(r) + 1):
        D[i][0] = i
    for j in range(1, len(h) + 1):
        D[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + 1)
    # backtrace
    i, j = len(r), len(h)
    subs = dels = ins = 0
    while i > 0 or j > 0:
        if i > 0 and j > 0 and r[i - 1] == h[j - 1]:
            i -= 1
            j -= 1
        else:
            if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + 1:
                subs += 1
                i -= 1
                j -= 1
            elif i > 0 and D[i][j] == D[i - 1][j] + 1:
                dels += 1
                i -= 1
            elif j > 0 and D[i][j] == D[i][j - 1] + 1:
                ins += 1
                j -= 1
            else:
                # sicurezza
                if i > 0:
                    dels += 1
                    i -= 1
                elif j > 0:
                    ins += 1
                    j -= 1
    wer = (subs + dels + ins) / n if n > 0 else float("inf")
    return {"S": subs, "D": dels, "I": ins, "N": n, "WER": wer}


def align_texts(ref, hyp):
    """
    Allinea i testi di riferimento e ipotesi, restituendo le versioni con evidenziazioni.
    """
    r = ref.split()
    h = hyp.split()

    # matrice DP per tracciare il percorso ottimale
    D = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(1, len(r) + 1):
        D[i][0] = i
    for j in range(1, len(h) + 1):
        D[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + 1)

    # backtrace per ricostruire l'allineamento
    i, j = len(r), len(h)
    ref_aligned = []
    hyp_aligned = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and r[i - 1] == h[j - 1]:
            # parole uguali
            ref_aligned.insert(0, r[i - 1])
            hyp_aligned.insert(0, h[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + 1:
            # sostituzione
            ref_aligned.insert(0, r[i - 1])
            hyp_aligned.insert(0, f"**{h[j - 1]}**")
            i -= 1
            j -= 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            # cancellazione (parola nel riferimento ma non nell'ipotesi)
            # La parola dovrebbe essere nell'ipotesi ma manca
            ref_aligned.insert(0, r[i - 1])
            hyp_aligned.insert(0, f"**[MISSING: {r[i - 1]}]**")
            i -= 1
        elif j > 0 and D[i][j] == D[i][j - 1] + 1:
            # inserzione (parola nell'ipotesi ma non nel riferimento)
            # La parola è stata aggiunta erroneamente nell'ipotesi
            ref_aligned.insert(0, "")
            hyp_aligned.insert(0, f"**[EXTRA: {h[j - 1]}]**")
            j -= 1
        else:
            # caso di sicurezza
            if i > 0:
                ref_aligned.insert(0, r[i - 1])
                hyp_aligned.insert(0, f"**[MISSING: {r[i - 1]}]**")
                i -= 1
            elif j > 0:
                ref_aligned.insert(0, "")
                hyp_aligned.insert(0, f"**[EXTRA: {h[j - 1]}]**")
                j -= 1

    # filtra elementi vuoti per le inserzioni
    ref_clean = [word for word in ref_aligned if word != ""]

    return " ".join(ref_clean), " ".join(hyp_aligned)


def compute_from_files(ref_file, hyp_file):
    with open(ref_file, encoding="utf-8") as f:
        ref = f.read()
    with open(hyp_file, encoding="utf-8") as f:
        hyp = f.read()
    ref_n = normalize_text(ref)
    hyp_n = normalize_text(hyp)
    stats = wer_stats(ref_n, hyp_n)

    print("=== WER STATISTICS ===")
    print("Sostituzioni (S):", stats["S"])
    print("Cancellazioni (D):", stats["D"])
    print("Inserzioni (I):", stats["I"])
    print("N (parole riferimento):", stats["N"])
    print("WER = (S+D+I)/N =", f"{stats['WER']:.3f}", f"-> {stats['WER']*100:.1f}%")
    print()

    print("=== WORD DIFFERENCES ===")
    ref_aligned, hyp_aligned = align_texts(ref_n, hyp_n)
    print("Reference: ", ref_aligned)
    print("Automatic: ", hyp_aligned)
    print()

    print("=== FULL TEXT PREVIEW ===")
    print("Riferimento (prime 200 char):", ref_n[:200])
    print("Ipotetico (prime 200 char):", hyp_n[:200])


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Uso: python compute_wer.py ref.txt hyp.txt")
        sys.exit(1)
    compute_from_files(sys.argv[1], sys.argv[2])
