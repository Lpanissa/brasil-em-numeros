"""Fonte única dos dados do painel: gera seed.sql (Supabase) e painel.json (cópia local)."""
import json, pathlib

# chave: (categoria, nome, unidade, fonte, url, [(data_ref, periodo, valor, texto)])
IND = {}
def ind(chave, cat, nome, un, fonte, url, pontos, desc=None):
    IND[chave] = dict(categoria=cat, nome=nome, unidade=un, fonte=fonte, fonte_url=url, descricao=desc,
                      valores=[dict(data_ref=d, periodo=p, valor=v, valor_texto=t) for d, p, v, t in pontos])

BCB = "https://www.bcb.gov.br"
ANP = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos"
IBGE = "https://www.ibge.gov.br"
DIEESE = "https://www.dieese.org.br/analisecestabasica/2026/202609cestabasica.pdf"

# ---------- Juros e câmbio ----------
ind("selic", "Juros e câmbio", "Taxa Selic", "% a.a.", "Banco Central (Copom)", BCB + "/controleinflacao/taxaselic", [
    ("2025-12-10", "dez/2025", 15.00, "15,00%"), ("2026-06-17", "jun/2026", 14.25, "14,25%"),
    ("2026-08-06", "ago/2026", 14.00, "14,00%"), ("2026-09-17", "set/2026", 13.75, "13,75%")])
ind("cdi", "Juros e câmbio", "CDI", "% a.a.", "B3 / Banco Central", BCB, [
    ("2026-08-14", "14/08/2026", 13.90, "13,90%"), ("2026-10-09", "09/10/2026", 13.65, "13,65%")])
ind("poupanca", "Juros e câmbio", "Poupança (rendimento no mês)", "% a.m.", "Banco Central", BCB, [
    ("2026-10-01", "out/2026", 0.6698, "0,67% (≈ 8,3% ao ano)")])
ind("dolar", "Juros e câmbio", "Dólar PTAX", "R$", "Banco Central", BCB + "/estabilidadefinanceira/historicocotacoes", [
    ("2026-01-02", "02/01/2026", 5.4372, "R$ 5,44"), ("2026-05-11", "11/05/2026", 4.8973, "R$ 4,90"),
    ("2026-09-28", "28/09/2026", 5.2132, "R$ 5,21"), ("2026-10-02", "02/10/2026", 5.2238, "R$ 5,22"),
    ("2026-10-09", "09/10/2026", 4.9892, "R$ 4,99"), ("2026-10-16", "16/10/2026", 5.0826, "R$ 5,08"),
    ("2026-10-23", "23/10/2026", 5.0371, "R$ 5,04")])
ind("euro", "Juros e câmbio", "Euro comercial", "R$", "Mercado (fechamento)", None, [
    ("2026-08-14", "14/08/2026", 6.0390, "R$ 6,04"), ("2026-09-29", "29/09/2026", 5.9150, "R$ 5,92")])
ind("ibovespa", "Juros e câmbio", "Ibovespa", "pontos", "B3", "https://www.b3.com.br", [
    ("2026-08-14", "14/08/2026", 166934.20, "166.934"), ("2026-09-29", "29/09/2026", 183827.59, "183.828"),
    ("2026-10-09", "09/10/2026", 209066.90, "209.067")])
ind("bitcoin", "Juros e câmbio", "Bitcoin", "R$", "Mercado (corretoras)", None, [
    ("2026-06-27", "27/06/2026", 316120, "R$ 316.120"), ("2026-08-01", "01/08/2026", 322668, "R$ 322.668"),
    ("2026-09-15", "15/09/2026", 396591, "R$ 396.591"), ("2026-10-26", "26/10/2026", 403885, "R$ 403.885")])

# ---------- Inflação ----------
ipca12 = [4.44, 3.81, 4.14, 4.39, 4.72, 4.64, 4.44, 4.22, 4.58]
ipcam = [0.33, 0.70, 0.88, 0.67, 0.58, 0.16, 0.07, -0.32, 0.82]
mes = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set"]
br = lambda x, c=2: f"{x:.{c}f}".replace(".", ",")
ind("ipca_12m", "Inflação", "IPCA acumulado em 12 meses", "%", "IBGE", IBGE + "/explica/inflacao.php",
    [(f"2026-{i+1:02d}-01", f"{m}/2026", v, br(v) + "%") for i, (m, v) in enumerate(zip(mes, ipca12))])
ind("ipca_mes", "Inflação", "IPCA do mês", "%", "IBGE", IBGE + "/explica/inflacao.php",
    [(f"2026-{i+1:02d}-01", f"{m}/2026", v, br(v) + "%") for i, (m, v) in enumerate(zip(mes, ipcam))])
ind("inpc_12m", "Inflação", "INPC em 12 meses (corrige salários e INSS)", "%", "IBGE", IBGE, [
    ("2026-09-01", "set/2026", 4.29, "4,29%")])
ind("igpm_12m", "Inflação", "IGP-M em 12 meses (reajuste de aluguel)", "%", "FGV", "https://portalibre.fgv.br", [
    ("2026-09-01", "set/2026", 3.34, "3,34%")])

# ---------- Renda e trabalho ----------
ind("salario_minimo", "Renda e trabalho", "Salário mínimo nacional", "R$", "Governo federal", "https://www.planalto.gov.br", [
    ("2024-01-01", "2024", 1412, "R$ 1.412"), ("2025-01-01", "2025", 1518, "R$ 1.518"), ("2026-01-01", "2026", 1621, "R$ 1.621")])
ind("piso_sp", "Renda e trabalho", "Piso salarial paulista", "R$", "Lei estadual 18.471/2026",
    "https://www.al.sp.gov.br/repositorio/legislacao/lei/2026/lei-18471-27.05.2026.html", [
    ("2025-07-01", "jul/2025", 1804, "R$ 1.804"), ("2026-06-01", "jun/2026", 1874.36, "R$ 1.874,36")])
ind("salario_necessario", "Renda e trabalho", "Salário mínimo necessário (DIEESE)", "R$", "DIEESE", DIEESE, [
    ("2026-09-01", "set/2026", 7750.01, "R$ 7.750,01")], "Quanto uma família de 4 pessoas precisaria para cobrir as despesas básicas.")
ind("renda_media", "Renda e trabalho", "Rendimento médio do trabalhador", "R$", "IBGE – PNAD Contínua", IBGE, [
    ("2026-06-01", "tri. até jun/2026", 3738, "R$ 3.738"), ("2026-08-01", "tri. até ago/2026", 3777, "R$ 3.777")])
ind("desemprego", "Renda e trabalho", "Desemprego", "%", "IBGE – PNAD Contínua", IBGE, [
    ("2026-01-01", "tri. até jan/2026", 5.4, "5,4%"), ("2026-03-01", "tri. até mar/2026", 6.1, "6,1%"),
    ("2026-04-01", "tri. até abr/2026", 5.8, "5,8%"), ("2026-05-01", "tri. até mai/2026", 5.6, "5,6%"),
    ("2026-06-01", "tri. até jun/2026", 5.4, "5,4%"), ("2026-08-01", "tri. até ago/2026", 5.3, "5,3%")])
ind("informalidade", "Renda e trabalho", "Informalidade", "%", "IBGE – PNAD Contínua", IBGE, [
    ("2026-01-01", "tri. até jan/2026", 37.5, "37,5%"), ("2026-04-01", "tri. até abr/2026", 37.2, "37,2%"),
    ("2026-08-01", "tri. até ago/2026", 37.5, "37,5%")])
ind("empregos_formais", "Renda e trabalho", "Empregos com carteira (estoque)", "milhões", "Novo Caged / MTE", "https://www.gov.br/trabalho-e-emprego", [
    ("2026-08-01", "ago/2026", 48.24, "48,24 milhões")])
ind("meis", "Renda e trabalho", "MEIs ativos", "milhões", "Receita Federal", None, [
    ("2025-12-31", "2025", 17.8, "17,8 milhões"), ("2026-06-01", "jun/2026", 17.16, "17,16 milhões")])
ind("teto_inss", "Renda e trabalho", "Teto do INSS", "R$", "INSS", "https://www.gov.br/inss", [
    ("2026-01-01", "2026", 8475.55, "R$ 8.475,55")])
ind("bolsa_familia", "Renda e trabalho", "Bolsa Família (benefício médio)", "R$", "MDS", "https://www.gov.br/mds", [
    ("2025-12-01", "dez/2025", 691.37, "R$ 691,37"), ("2026-09-01", "set/2026", 678.18, "R$ 678,18"),
    ("2026-10-01", "out/2026", 777, "~R$ 777 (estimativa)")], "Reajuste de 15,04% a partir de outubro/2026; piso de R$ 691.")

# ---------- Mercado e cesta ----------
ind("cesta_sp", "Mercado e cesta básica", "Cesta básica São Paulo", "R$", "DIEESE / Conab", DIEESE, [
    ("2026-05-01", "mai/2026", 952.20, "R$ 952,20"), ("2026-08-01", "ago/2026", 900.59, "R$ 900,59"),
    ("2026-09-01", "set/2026", 922.51, "R$ 922,51")])
ind("cesta_brasil", "Mercado e cesta básica", "Cesta básica (média das capitais)", "R$", "DIEESE / Conab", DIEESE, [
    ("2026-09-01", "set/2026", 752.91, "R$ 752,91")])
ind("cesta_procon", "Mercado e cesta básica", "Cesta ampla SP (alimentos, limpeza e higiene)", "R$", "Procon-SP / DIEESE", None, [
    ("2026-07-01", "jul/2026", 1335.04, "R$ 1.335,04"), ("2026-08-01", "ago/2026", 1338.03, "R$ 1.338,03")])
ind("carne", "Mercado e cesta básica", "Carne de primeira (kg)", "R$/kg", "Procon-SP / DIEESE", None, [
    ("2026-07-01", "jul/2026", 48.54, "R$ 48,54"), ("2026-08-01", "ago/2026", 50.49, "R$ 50,49")])
ind("arroz", "Mercado e cesta básica", "Arroz (pacote 5 kg)", "R$", "Procon-SP / DIEESE", None, [
    ("2026-07-01", "jul/2026", 19.63, "R$ 19,63"), ("2026-08-01", "ago/2026", 20.59, "R$ 20,59")])
ind("batata", "Mercado e cesta básica", "Batata (kg)", "R$/kg", "Procon-SP / DIEESE", None, [
    ("2026-07-01", "jul/2026", 8.20, "R$ 8,20"), ("2026-08-01", "ago/2026", 6.41, "R$ 6,41")])
var12 = [("feijao", "Feijão carioca", 37.72), ("batata", "Batata", 56.33), ("tomate", "Tomate", 23.54),
         ("carne", "Carne de primeira", 11.85), ("leite", "Leite integral", 6.74), ("pao", "Pão francês", 4.38),
         ("oleo", "Óleo de soja", 0.76), ("manteiga", "Manteiga", 0.50), ("banana", "Banana", -1.30),
         ("farinha", "Farinha de trigo", -3.67), ("arroz", "Arroz", -5.25), ("cafe", "Café em pó", -17.57),
         ("acucar", "Açúcar", -23.53)]
for k, n, v in var12:
    ind(f"var12_{k}", "Cesta: alta em 12 meses (SP)", n, "% em 12 meses", "DIEESE / Conab", DIEESE,
        [("2026-09-01", "set/2026", v, ("+" if v > 0 else "") + br(v) + "%")])

# ---------- Moradia ----------
ind("aluguel_sp", "Moradia e contas", "Aluguel em São Paulo (m²)", "R$/m²", "FipeZAP", "https://www.fipe.org.br/pt-br/indices/fipezap/", [
    ("2026-09-01", "set/2026", 65.78, "R$ 65,78")])
ind("aluguel_br", "Moradia e contas", "Aluguel média Brasil (m²)", "R$/m²", "FipeZAP", "https://www.fipe.org.br/pt-br/indices/fipezap/", [
    ("2026-09-01", "set/2026", 54.77, "R$ 54,77")])
ind("aluguel_12m", "Moradia e contas", "Alta do aluguel em 12 meses (Brasil)", "%", "FipeZAP", "https://www.fipe.org.br/pt-br/indices/fipezap/", [
    ("2026-09-01", "set/2026", 9.13, "+9,13%")])
ind("energia", "Moradia e contas", "Energia Enel SP (kWh, sem impostos)", "R$/kWh", "ANEEL / Enel SP", "https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-energia-eletrica.html", [
    ("2026-07-04", "desde 04/07/2026", 0.789, "R$ 0,789 (~R$ 0,98 com impostos)")])
ind("agua", "Moradia e contas", "Água Sabesp (m³, residencial)", "R$/m³", "Sabesp / Governo de SP", None, [
    ("2026-01-01", "2026", 6.40, "R$ 6,40")])
ind("gas", "Moradia e contas", "Gás de cozinha (botijão 13 kg)", "R$", "ANP", ANP, [
    ("2026-07-04", "04/07/2026", 114.66, "R$ 114,66"), ("2026-07-11", "11/07/2026", 114.41, "R$ 114,41"),
    ("2026-08-14", "14/08/2026", 113.89, "R$ 113,89"), ("2026-09-12", "12/09/2026", 114.28, "R$ 114,28"),
    ("2026-10-10", "10/10/2026", 114.61, "R$ 114,61"), ("2026-10-17", "17/10/2026", 114.73, "R$ 114,73")])

# ---------- Transporte ----------
ind("gasolina", "Transporte", "Gasolina (média Brasil)", "R$/L", "ANP", ANP, [
    ("2026-07-04", "04/07/2026", 6.61, "R$ 6,61"), ("2026-07-11", "11/07/2026", 6.58, "R$ 6,58"),
    ("2026-08-14", "14/08/2026", 6.53, "R$ 6,53"), ("2026-09-12", "12/09/2026", 6.53, "R$ 6,53"),
    ("2026-10-17", "17/10/2026", 6.53, "R$ 6,53")])
ind("etanol", "Transporte", "Etanol (média Brasil)", "R$/L", "ANP", ANP, [
    ("2026-09-12", "12/09/2026", 4.04, "R$ 4,04"), ("2026-10-10", "10/10/2026", 4.14, "R$ 4,14"),
    ("2026-10-17", "17/10/2026", 4.11, "R$ 4,11")])
ind("etanol_sp", "Transporte", "Etanol (média SP)", "R$/L", "ANP", ANP, [
    ("2026-09-12", "12/09/2026", 3.76, "R$ 3,76"), ("2026-10-17", "17/10/2026", 3.86, "R$ 3,86")])
ind("diesel", "Transporte", "Diesel S-10 (média Brasil)", "R$/L", "ANP", ANP, [
    ("2026-07-04", "04/07/2026", 7.02, "R$ 7,02"), ("2026-07-11", "11/07/2026", 6.97, "R$ 6,97"),
    ("2026-08-14", "ago/2026", 6.949, "R$ 6,95"), ("2026-09-12", "12/09/2026", 6.97, "R$ 6,97")])
ind("gnv", "Transporte", "GNV (m³)", "R$/m³", "ANP", ANP, [("2026-08-01", "ago/2026", 4.90, "R$ 4,90")])
ind("onibus_sp", "Transporte", "Ônibus municipal SP", "R$", "SPTrans", "https://www.sptrans.com.br", [
    ("2025-01-06", "2025", 5.00, "R$ 5,00"), ("2026-01-06", "2026", 5.30, "R$ 5,30")])
ind("metro_sp", "Transporte", "Metrô / CPTM", "R$", "Governo de SP", "https://www.metro.sp.gov.br", [
    ("2025-01-06", "2025", 5.20, "R$ 5,20"), ("2026-01-06", "2026", 5.40, "R$ 5,40")])
ind("pedagio_ai", "Transporte", "Pedágio Anchieta-Imigrantes", "R$", "ARTESP", "https://www.artesp.sp.gov.br", [
    ("2025-07-01", "jul/2025", 38.70, "R$ 38,70"), ("2026-07-01", "jul/2026", 40.60, "R$ 40,60")])

# ---------- Crédito e dívidas ----------
ind("rotativo", "Crédito e dívidas", "Juros do cartão rotativo", "% a.a.", "Banco Central", BCB + "/estatisticas/estatisticasmonetariascredito", [
    ("2026-02-01", "fev/2026", 435.9, "435,9%"), ("2026-05-01", "mai/2026", 439.8, "439,8%"),
    ("2026-06-01", "jun/2026", 442.4, "442,4%"), ("2026-08-01", "ago/2026", 444.89, "444,9%")])
ind("credito_pessoal", "Crédito e dívidas", "Empréstimo pessoal (não consignado)", "% a.a.", "Banco Central", BCB, [
    ("2026-08-01", "ago/2026", 110.22, "110,2%")])
ind("credito_livre", "Crédito e dívidas", "Juro médio para famílias (crédito livre)", "% a.a.", "Banco Central", BCB, [
    ("2026-08-01", "ago/2026", 61.7, "61,7%")])
ind("inadimplencia", "Crédito e dívidas", "Inadimplência das famílias", "%", "Banco Central", BCB, [
    ("2026-08-01", "ago/2026", 6.0, "6,0%")])
ind("endividamento", "Crédito e dívidas", "Dívida das famílias / renda anual", "%", "Banco Central", BCB, [
    ("2025-12-01", "dez/2025", 49.7, "49,7%"), ("2026-07-01", "jul/2026", 49.9, "49,9%")])

# ---------- Saúde ----------
ind("plano_saude", "Saúde", "Reajuste máximo plano de saúde individual", "%", "ANS", "https://www.gov.br/ans", [
    ("2026-05-29", "2026", 5.11, "5,11%")])
ind("remedios", "Saúde", "Reajuste máximo de remédios", "%", "CMED / Anvisa", "https://www.gov.br/anvisa", [
    ("2026-03-31", "2026", 3.81, "3,81%")])

# ---------- Segurança SP ----------
ind("homicidios_sp", "Segurança (SP)", "Homicídios no estado de SP", "casos/ano", "SSP-SP", "https://www.ssp.sp.gov.br/estatistica", [
    ("2024-12-31", "2024", 2517, "2.517"), ("2025-12-31", "2025", 2438, "2.438")])
ind("celulares_sp", "Segurança (SP)", "Celulares roubados/furtados em SP", "casos/ano", "SSP-SP", "https://www.ssp.sp.gov.br/estatistica", [
    ("2024-12-31", "2024", 270488, "270.488"), ("2025-12-31", "2025", 254416, "254.416")])
ind("roubo_veiculos_sp", "Segurança (SP)", "Roubos de veículos em SP", "casos/ano", "SSP-SP", "https://www.ssp.sp.gov.br/estatistica", [
    ("2024-12-31", "2024", 31696, "31.696"), ("2025-12-31", "2025", 25024, "25.024")])

# ---------- atualização de 26/10/2026 ----------
def mais(chave, d, p, v, txt):
    IND[chave]["valores"].append(dict(data_ref=d, periodo=p, valor=v, valor_texto=txt))
mais("ibovespa", "2026-10-23", "23/10/2026", 205082.56, "205.083")
mais("euro", "2026-10-23", "23/10/2026", 5.589, "R$ 5,59")
mais("cdi", "2026-10-23", "23/10/2026", 13.65, "13,65%")
mais("diesel", "2026-10-17", "17/10/2026", 7.34, "R$ 7,34")
mais("cesta_procon", "2026-09-01", "set/2026", 1347.61, "R$ 1.347,61")
mais("arroz", "2026-09-01", "set/2026", 21.27, "R$ 21,27")
mais("batata", "2026-09-01", "set/2026", 7.77, "R$ 7,77")
IND["euro"]["fonte"] = "Banco Central / mercado (fechamento)"

# ---------- Estados ----------
# uf: (nome, região, coluna, linha no mapa em blocos)
UFS = {
 "RR": ("Roraima", "Norte", 3, 0), "AP": ("Amapá", "Norte", 5, 0),
 "AM": ("Amazonas", "Norte", 2, 1), "PA": ("Pará", "Norte", 4, 1), "MA": ("Maranhão", "Nordeste", 5, 1), "CE": ("Ceará", "Nordeste", 6, 1), "RN": ("Rio Grande do Norte", "Nordeste", 7, 1),
 "AC": ("Acre", "Norte", 1, 2), "RO": ("Rondônia", "Norte", 2, 2), "TO": ("Tocantins", "Norte", 4, 2), "PI": ("Piauí", "Nordeste", 5, 2), "PE": ("Pernambuco", "Nordeste", 6, 2), "PB": ("Paraíba", "Nordeste", 7, 2),
 "MT": ("Mato Grosso", "Centro-Oeste", 3, 3), "GO": ("Goiás", "Centro-Oeste", 4, 3), "BA": ("Bahia", "Nordeste", 5, 3), "AL": ("Alagoas", "Nordeste", 6, 3), "SE": ("Sergipe", "Nordeste", 7, 3),
 "MS": ("Mato Grosso do Sul", "Centro-Oeste", 3, 4), "DF": ("Distrito Federal", "Centro-Oeste", 4, 4), "MG": ("Minas Gerais", "Sudeste", 5, 4), "ES": ("Espírito Santo", "Sudeste", 6, 4),
 "PR": ("Paraná", "Sul", 3, 5), "SP": ("São Paulo", "Sudeste", 4, 5), "RJ": ("Rio de Janeiro", "Sudeste", 5, 5),
 "SC": ("Santa Catarina", "Sul", 3, 6), "RS": ("Rio Grande do Sul", "Sul", 2, 6)}
# vencedor e % do vencedor no 2º turno 2026 (TSE, via imprensa; arredondado onde a fonte arredondou)
# vencedor e % do vencedor no 2º turno de 25/10/2026, por UF (TSE, resultados oficiais, eleição 6258)
ELE = {"AC": ("PL", 66.57), "AL": ("PT", 60.77), "AM": ("PT", 54.02), "AP": ("PT", 52.88), "BA": ("PT", 71.31),
       "CE": ("PT", 68.93), "DF": ("PL", 54.28), "ES": ("PL", 56.37), "GO": ("PL", 59.66), "MA": ("PT", 69.54),
       "MG": ("PT", 50.43), "MS": ("PL", 59.60), "MT": ("PL", 66.06), "PA": ("PT", 55.02), "PB": ("PT", 67.46),
       "PE": ("PT", 69.20), "PI": ("PT", 75.88), "PR": ("PL", 62.58), "RJ": ("PL", 53.10), "RN": ("PT", 65.72),
       "RO": ("PL", 69.61), "RR": ("PL", 72.46), "RS": ("PL", 57.84), "SC": ("PL", 69.42), "SE": ("PT", 69.53),
       "SP": ("PL", 53.85), "TO": ("PL", 51.37)}
# governadores eleitos em 2022 (mandato 2023-2026), partido pelo qual foram eleitos (TSE)
GOV22 = {"AC": ("Gladson Cameli", "PP"), "AL": ("Paulo Dantas", "MDB"), "AP": ("Clécio Luís", "Solidariedade"),
         "AM": ("Wilson Lima", "União"), "BA": ("Jerônimo Rodrigues", "PT"), "CE": ("Elmano de Freitas", "PT"),
         "DF": ("Ibaneis Rocha", "MDB"), "ES": ("Renato Casagrande", "PSB"), "GO": ("Ronaldo Caiado", "União"),
         "MA": ("Carlos Brandão", "PSB"), "MT": ("Mauro Mendes", "União"), "MS": ("Eduardo Riedel", "PSDB"),
         "MG": ("Romeu Zema", "Novo"), "PA": ("Helder Barbalho", "MDB"), "PB": ("João Azevêdo", "PSB"),
         "PR": ("Ratinho Júnior", "PSD"), "PE": ("Raquel Lyra", "PSDB"), "PI": ("Rafael Fonteles", "PT"),
         "RJ": ("Cláudio Castro", "PL"), "RN": ("Fátima Bezerra", "PT"), "RS": ("Eduardo Leite", "PSDB"),
         "RO": ("Marcos Rocha", "União"), "RR": ("Antonio Denarium", "PP"), "SC": ("Jorginho Mello", "PL"),
         "SP": ("Tarcísio de Freitas", "Republicanos"), "SE": ("Fábio Mitidieri", "PSD"), "TO": ("Wanderlei Barbosa", "Republicanos")}
# governadores eleitos em 2026 (posse em 01/01/2027), partido do candidato (TSE, eleições 6259 e 6260)
GOV26 = {"AC": ("Mailza Assis", "PP"), "AL": ("JHC", "PSDB"), "AP": ("Dr. Furlan", "PSD"), "AM": ("Omar Aziz", "PSD"),
         "BA": ("Jerônimo Rodrigues", "PT"), "CE": ("Elmano de Freitas", "PT"), "DF": ("Celina Leão", "PP"),
         "ES": ("Lorenzo Pazolini", "Republicanos"), "GO": ("Daniel Vilela", "MDB"), "MA": ("Eduardo Braide", "PSD"),
         "MT": ("Otaviano Pivetta", "Republicanos"), "MS": ("Eduardo Riedel", "PP"), "MG": ("Cleitinho", "Republicanos"),
         "PA": ("Dr. Daniel", "Podemos"), "PB": ("Lucas Ribeiro", "PP"), "PR": ("Sergio Moro", "PL"),
         "PE": ("Raquel Lyra", "PSD"), "PI": ("Rafael Fonteles", "PT"), "RJ": ("Douglas Ruas", "PL"),
         "RN": ("Cadu de Lula", "PT"), "RS": ("Zucco", "PL"), "RO": ("Marcos Rogério", "PL"), "RR": ("Arthur Henrique", "PL"),
         "SC": ("Jorginho Mello", "PL"), "SP": ("Tarcísio", "Republicanos"), "SE": ("Fábio Mitidieri", "PSD"),
         "TO": ("Vicentinho Júnior", "PSDB")}
PIB = {"DF": 129790.44, "SP": 77566.27, "MT": 74620.05, "RJ": 73052.55, "SC": 67459.74, "MS": 66884.75, "RS": 59736.20,
       "PR": 58624.33, "ES": 54732.78, "RO": 48353.38, "GO": 47721.56, "MG": 47321.23, "TO": 42553.36, "AM": 41047.91,
       "RR": 39460.54, "AP": 38187.09, "AC": 31675.60, "PA": 31347.59, "RN": 30804.91, "BA": 30476.54, "PE": 29857.27,
       "AL": 28675.84, "SE": 27518.80, "CE": 26405.96, "PI": 24736.15, "PB": 24395.17, "MA": 22020.63}
MVI = {"AP": 42.5, "BA": 36.8, "CE": 34.7, "AL": 33.1, "PE": 33.0, "MA": 29.7, "RN": 29.1, "PA": 28.4, "RO": 28.1,
       "PB": 24.6, "MT": 22.9, "RJ": 22.6, "SE": 22.1, "ES": 22.0, "AC": 21.6, "MS": 20.2, "RR": 19.5, "TO": 19.3,
       "AM": 18.5, "PI": 17.1, "GO": 16.5, "PR": 15.5, "MG": 12.9, "RS": 11.3, "DF": 9.6, "SP": 7.8, "SC": 7.6}

RENDA = {"DF": 4538, "SP": 2956, "RS": 2839, "SC": 2809, "RJ": 2794, "PR": 2762, "MS": 2454, "GO": 2407, "MG": 2353,
         "MT": 2335, "ES": 2249, "TO": 2036, "RO": 1991, "RR": 1878, "RN": 1819, "AP": 1697, "SE": 1697, "PE": 1600,
         "PI": 1546, "PB": 1543, "AM": 1484, "BA": 1465, "AL": 1422, "PA": 1420, "AC": 1392, "CE": 1390, "MA": 1219}

# desemprego, 2º tri/2026 (IBGE, PNAD Contínua trimestral, SIDRA 4099, divulgado em 14/08/2026)
DESEMP = {"RO": 2.6, "AC": 6.6, "AM": 7.5, "RR": 5.0, "PA": 6.2, "AP": 9.8, "TO": 4.1, "MA": 6.0, "PI": 8.3, "CE": 6.6,
          "RN": 5.6, "PB": 5.4, "PE": 8.3, "AL": 7.9, "SE": 7.9, "BA": 9.1, "MG": 3.8, "ES": 2.3, "RJ": 7.1, "SP": 5.4,
          "PR": 3.1, "SC": 2.1, "RS": 4.2, "MS": 2.7, "MT": 2.2, "GO": 4.0, "DF": 6.5}
# analfabetismo 15 anos ou mais, 2025 (IBGE, PNAD Contínua Educação, SIDRA 7113, divulgado em 19/06/2026)
ANALF = {"RO": 5.1, "AC": 8.9, "AM": 4.3, "RR": 3.4, "PA": 6.2, "AP": 4.5, "TO": 6.8, "MA": 10.9, "PI": 13.1, "CE": 11.1,
         "RN": 9.3, "PB": 11.6, "PE": 10.1, "AL": 13.1, "SE": 10.3, "BA": 9.5, "MG": 3.8, "ES": 3.8, "RJ": 1.6, "SP": 1.9,
         "PR": 3.3, "SC": 1.5, "RS": 2.2, "MS": 3.9, "MT": 3.5, "GO": 3.5, "DF": 2.0}
# domicílios com Bolsa Família, 2025, em mil (IBGE, PNAD Contínua Rendimento de todas as fontes, SIDRA 7449 e 7450, divulgado em 08/05/2026)
BF_SIM = {"RO": 95, "AC": 91, "AM": 421, "RR": 42, "PA": 1061, "AP": 74, "TO": 103, "MA": 920, "PI": 448, "CE": 1042,
          "RN": 343, "PB": 493, "PE": 1062, "AL": 375, "SE": 255, "BA": 1791, "MG": 1078, "ES": 191, "RJ": 889, "SP": 1341,
          "PR": 359, "SC": 119, "RS": 347, "MS": 102, "MT": 169, "GO": 313, "DF": 115}
BF_NAO = {"RO": 535, "AC": 199, "AM": 855, "RR": 164, "PA": 1684, "AP": 176, "TO": 468, "MA": 1394, "PI": 719, "CE": 2264,
          "RN": 906, "PB": 1001, "PE": 2528, "AL": 768, "SE": 605, "BA": 3873, "MG": 7032, "ES": 1396, "RJ": 5915, "SP": 16213,
          "PR": 4158, "SC": 2967, "RS": 4176, "MS": 969, "MT": 1210, "GO": 2516, "DF": 974}
BF = {u: round(BF_SIM[u] / (BF_SIM[u] + BF_NAO[u]) * 100, 1) for u in BF_SIM}
# esperança de vida ao nascer, 2024 (IBGE, Projeções da População, revisão 2024, divulgado em 22/08/2024)
EXPEC = {"DF": 79.7, "SC": 78.3, "RN": 77.8, "MG": 77.5, "CE": 77.3, "ES": 77.2, "RS": 77.2, "SP": 77.0, "PI": 77.0,
         "PR": 76.8, "PB": 76.8, "GO": 76.8, "TO": 76.7, "SE": 76.4, "PA": 76.3, "RO": 76.0, "AC": 75.9, "BA": 75.8,
         "MT": 75.7, "RJ": 75.6, "MA": 75.6, "PE": 75.5, "AM": 75.5, "MS": 75.4, "AL": 74.4, "RR": 74.3, "AP": 74.3}
ESTADOS = []
for uf, (nome, reg, x, y) in UFS.items():
    v, pct = ELE[uf]
    ESTADOS.append(dict(uf=uf, nome=nome, regiao=reg, x=x, y=y, vencedor_2026=v, pct_vencedor_2026=pct,
                        pib_pc_2023=PIB[uf], mvi_2025=MVI[uf], renda_pc_2025=RENDA[uf], desemprego_2026t2=DESEMP[uf],
                        analfabetismo_2025=ANALF[uf], bolsa_familia_dom_2025=BF[uf], expectativa_2024=EXPEC[uf],
                        gov_2022=GOV22[uf][0], gov_2022_partido=GOV22[uf][1], gov_2026=GOV26[uf][0], gov_2026_partido=GOV26[uf][1]))

def q(s):
    return "null" if s is None else "'" + str(s).replace("'", "''") + "'"
def n(v):
    return "null" if v is None else repr(v)

def gerar(raiz):
    raiz = pathlib.Path(raiz)
    sql = ["delete from public.painel_valores; delete from public.painel_indicadores; delete from public.painel_estados;"]
    rows = []
    for o, (k, d) in enumerate(IND.items()):
        rows.append(f"({q(k)},{q(d['categoria'])},{q(d['nome'])},{q(d['unidade'])},{q(d['fonte'])},{q(d['fonte_url'])},{q(d['descricao'])},{o})")
    sql.append("insert into public.painel_indicadores (chave,categoria,nome,unidade,fonte,fonte_url,descricao,ordem) values\n" + ",\n".join(rows) + ";")
    rows = []
    for k, d in IND.items():
        for v in d["valores"]:
            rows.append(f"({q(k)},{q(v['data_ref'])},{q(v['periodo'])},{n(v['valor'])},{q(v['valor_texto'])})")
    sql.append("insert into public.painel_valores (chave,data_ref,periodo,valor,valor_texto) values\n" + ",\n".join(rows) + ";")
    rows = [f"({q(e['uf'])},{q(e['nome'])},{q(e['regiao'])},{e['x']},{e['y']},{q(e['vencedor_2026'])},{n(e['pct_vencedor_2026'])},{n(e['pib_pc_2023'])},{n(e['mvi_2025'])},{n(e['renda_pc_2025'])},{n(e['desemprego_2026t2'])},{n(e['analfabetismo_2025'])},{n(e['bolsa_familia_dom_2025'])},{n(e['expectativa_2024'])},{q(e['gov_2022'])},{q(e['gov_2022_partido'])},{q(e['gov_2026'])},{q(e['gov_2026_partido'])})" for e in ESTADOS]
    sql.append("insert into public.painel_estados (uf,nome,regiao,x,y,vencedor_2026,pct_vencedor_2026,pib_pc_2023,mvi_2025,renda_pc_2025,desemprego_2026t2,analfabetismo_2025,bolsa_familia_dom_2025,expectativa_2024,gov_2022,gov_2022_partido,gov_2026,gov_2026_partido) values\n" + ",\n".join(rows) + ";")
    (raiz / "scripts" / "seed_painel.sql").write_text("\n".join(sql), encoding="utf-8")
    js = dict(indicadores=[dict(chave=k, **{a: b for a, b in d.items() if a != "valores"}, ordem=i) for i, (k, d) in enumerate(IND.items())],
              valores=[dict(chave=k, **v) for k, d in IND.items() for v in d["valores"]], estados=ESTADOS,
              coletas=[dict(data_coleta="2026-10-26", rotulo="Base · 26/10/2026", base=True)],
              snapshot=[dict(data_coleta="2026-10-26", chave=k, valor=max(d["valores"], key=lambda x: x["data_ref"])["valor"],
                             valor_texto=max(d["valores"], key=lambda x: x["data_ref"])["valor_texto"],
                             periodo=max(d["valores"], key=lambda x: x["data_ref"])["periodo"]) for k, d in IND.items()])
    (raiz / "painel.json").write_text(json.dumps(js, ensure_ascii=False), encoding="utf-8")
    print(len(IND), "indicadores,", len(js["valores"]), "valores,", len(ESTADOS), "estados")

if __name__ == "__main__":
    gerar(pathlib.Path(__file__).resolve().parent.parent)
