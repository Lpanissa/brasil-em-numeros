"""Atualiza painel.json com os dados oficiais mais recentes (Banco Central).

Roda todo dia pelo GitHub Actions (.github/workflows/atualizar-painel.yml).
Só acrescenta valores novos; nunca apaga o histórico que já existe.
"""
import json, pathlib, sys, urllib.request
from datetime import date, datetime

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAINEL = RAIZ / "painel.json"
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

# chave do painel -> (código SGS do Banco Central, formato do valor, unidade do texto)
SGS = {
    "selic": (432, "mes"),       # Taxa Selic meta (% a.a.), periodo "set/2026"
    "cdi": (4389, "dia"),        # CDI anualizado, periodo "09/10/2026"
    "ipca_mes": (433, "mes"),    # IPCA mensal, periodo "set/2026"
}


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "raioxdobrasil-atualizador/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def ultimo_valor_sgs(codigo):
    """Último valor publicado de uma série SGS: (data 'YYYY-MM-DD', valor float)."""
    j = get_json(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json")
    if not j:
        return None
    x = j[-1]
    dd, mm, aa = x["data"].split("/")
    return f"{aa}-{mm}-{dd}", float(x["valor"])


def dolar_ptax_dias(dias=10):
    """PTAX de venda do dólar nos últimos dias (boletim de fechamento de cada dia)."""
    fim = date.today()
    ini = date.fromordinal(fim.toordinal() - dias)
    f = lambda d: d.strftime("%m-%d-%Y")
    url = ("https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
           "CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
           f"?@moeda='USD'&@dataInicial='{f(ini)}'&@dataFinalCotacao='{f(fim)}'&$format=json")
    L = get_json(url).get("value", [])
    por_dia = {}
    for x in L:
        dia = x["dataHoraCotacao"][:10]
        if x.get("tipoBoletim") == "Fechamento" or dia not in por_dia:
            por_dia[dia] = float(x["cotacaoVenda"])
    return sorted(por_dia.items())  # [(YYYY-MM-DD, valor)]


def rotulo_periodo(data_iso, tipo="dia"):
    d = datetime.strptime(data_iso, "%Y-%m-%d")
    if tipo == "mes":
        return f"{MESES[d.month - 1]}/{d.year}"
    return f"{d.day:02d}/{d.month:02d}/{d.year}"


def acrescenta(painel, chave, data_ref, periodo, valor, texto):
    existe = [v for v in painel["valores"] if v["chave"] == chave and v["data_ref"] == data_ref]
    if existe:
        return False
    ultimo = max((v["data_ref"] for v in painel["valores"] if v["chave"] == chave), default="")
    if data_ref < ultimo:
        return False
    painel["valores"].append(dict(chave=chave, data_ref=data_ref, periodo=periodo,
                                  valor=valor, valor_texto=texto))
    return True


def main():
    painel = json.loads(PAINEL.read_text(encoding="utf-8"))
    mudou = 0
    erros = []

    # Dólar oficial (PTAX): dia a dia
    try:
        for dia, v in dolar_ptax_dias():
            if acrescenta(painel, "dolar", dia, rotulo_periodo(dia), round(v, 4),
                          "R$ " + f"{v:.2f}".replace(".", ",")):
                mudou += 1
    except Exception as e:
        erros.append(f"dolar: {e}")

    # Juros e inflação: último valor de cada série
    for chave, (codigo, tipo) in SGS.items():
        try:
            r = ultimo_valor_sgs(codigo)
            if not r:
                continue
            data_iso, v = r
            texto = f"{v:.2f}%".replace(".", ",")
            if acrescenta(painel, chave, data_iso, rotulo_periodo(data_iso, tipo), v, texto):
                mudou += 1
        except Exception as e:
            erros.append(f"{chave}: {e}")

    # Marca a data da última atualização automática
    if mudou:
        painel["atualizado_em"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        PAINEL.write_text(json.dumps(painel, ensure_ascii=False), encoding="utf-8")

    print(f"{mudou} valores novos")
    for e in erros:
        print("ERRO", e, file=sys.stderr)
    # Falha só se nada pôde ser lido, para não zerar o painel
    if erros and mudou == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
