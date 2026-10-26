# Fontes e roteiro da coleta mensal

Coleta todo **dia 15** de cada mês. A primeira coleta (26/10/2026) é a **base** de comparação.
Cada coleta grava o valor mais recente de cada indicador em `painel_valores` (histórico oficial, por data de referência)
e uma fotografia em `painel_snapshot` (valor de cada indicador no dia da coleta), registrada em `painel_coletas`.

**Atualização ao vivo (sem coleta):** ao abrir o site, a página busca direto nas APIs públicas: dólar oficial PTAX (Banco Central, com hora do boletim), dólar comercial, euro e bitcoin (AwesomeAPI), CDI (SGS 4389), inflação do mês e em 12 meses (SGS 433 e 13522), INPC e IGP-M em 12 meses (SGS 188 e 189), juros do rotativo (SGS 22022), empréstimo pessoal (SGS 20742), inadimplência (SGS 21084), endividamento (SGS 29037), desemprego e renda média (IBGE SIDRA 6381 e 6390). O resto (DIEESE, ANP, FipeZAP, Procon, Sabesp, SSP etc.) não tem API e segue pela coleta do dia 15.

Regra: usar sempre o número oficial mais recente publicado até o dia da coleta. Se a fonte ainda não publicou dado novo,
repetir o último valor na fotografia do mês (o histórico oficial não muda).

| Grupo | Indicador (chave) | Fonte oficial | Onde achar | Atualiza |
|---|---|---|---|---|
| Juros e câmbio | Selic (`selic`) | Banco Central – Copom | bcb.gov.br/controleinflacao/taxaselic | a cada reunião (~45 dias) |
| | CDI (`cdi`) | B3 / Banco Central | b3.com.br | diário |
| | Poupança (`poupanca`) | Banco Central | bcb.gov.br (remuneração dos depósitos de poupança) | mensal |
| | Dólar PTAX (`dolar`) | Banco Central | bcb.gov.br/estabilidadefinanceira/historicocotacoes | diário |
| | Euro (`euro`) | Banco Central (PTAX) | idem | diário |
| | Ibovespa (`ibovespa`) | B3 | b3.com.br | diário |
| | Bitcoin (`bitcoin`) | Corretoras (cotação em R$) | Mercado Bitcoin / outras | diário |
| Inflação | IPCA 12 meses e do mês (`ipca_12m`, `ipca_mes`) | IBGE | ibge.gov.br/explica/inflacao.php | mensal, ~dia 10 |
| | INPC 12 meses (`inpc_12m`) | IBGE | ibge.gov.br | mensal, ~dia 10 |
| | IGP-M 12 meses (`igpm_12m`) | FGV | portalibre.fgv.br | mensal, fim do mês |
| Renda e trabalho | Salário mínimo (`salario_minimo`) | Governo federal (decreto) | planalto.gov.br | anual (janeiro) |
| | Piso paulista (`piso_sp`) | Lei estadual de SP | al.sp.gov.br | anual |
| | Salário mínimo necessário (`salario_necessario`) | DIEESE | dieese.org.br/analisecestabasica | mensal, ~dia 8–10 |
| | Rendimento médio, desemprego, informalidade (`renda_media`, `desemprego`, `informalidade`) | IBGE – PNAD Contínua | ibge.gov.br/estatisticas/sociais/trabalho.html | mensal (trimestre móvel), fim do mês |
| | Empregos com carteira (`empregos_formais`) | Novo Caged / MTE | gov.br/trabalho-e-emprego | mensal, fim do mês |
| | MEIs ativos (`meis`) | Receita Federal | Portal do Empreendedor / Receita | mensal |
| | Teto do INSS (`teto_inss`) | INSS / Ministério da Previdência | gov.br/inss | anual |
| | Bolsa Família (`bolsa_familia`) | MDS | gov.br/mds | mensal |
| Mercado e cesta | Cesta básica SP e média das capitais (`cesta_sp`, `cesta_brasil`) | DIEESE / Conab | dieese.org.br/analisecestabasica/AAAA/AAAAMMcestabasica.pdf | mensal, ~dia 8–10 |
| | Variação em 12 meses de cada item (`var12_*`) | DIEESE / Conab | mesmo boletim | mensal |
| | Cesta ampla SP, carne, arroz, batata (`cesta_procon`, `carne`, `arroz`, `batata`) | Procon-SP / DIEESE | procon.sp.gov.br | mensal |
| Moradia e contas | Aluguel (`aluguel_sp`, `aluguel_br`, `aluguel_12m`) | Índice FipeZAP | fipe.org.br/pt-br/indices/fipezap | mensal, ~dia 10 |
| | Energia Enel SP (`energia`) | ANEEL / Enel | enel.com.br (tarifas) | anual (julho) + bandeiras |
| | Água Sabesp (`agua`) | Sabesp / Governo de SP | sabesp.com.br | anual |
| | Gás de cozinha (`gas`) | ANP – levantamento semanal | gov.br/anp (preços) | semanal |
| Transporte | Gasolina, etanol, etanol SP, diesel S-10, GNV (`gasolina`, `etanol`, `etanol_sp`, `diesel`, `gnv`) | ANP | gov.br/anp (preços) | semanal |
| | Ônibus SP, Metrô/CPTM (`onibus_sp`, `metro_sp`) | SPTrans / Governo de SP | sptrans.com.br, metro.sp.gov.br | anual (janeiro) |
| | Pedágio Anchieta-Imigrantes (`pedagio_ai`) | ARTESP | artesp.sp.gov.br | anual (julho) |
| Crédito e dívidas | Rotativo, empréstimo pessoal, crédito livre, inadimplência, endividamento | Banco Central – Estatísticas monetárias e de crédito | bcb.gov.br/estatisticas/estatisticasmonetariascredito | mensal, fim do mês |
| Saúde | Reajuste de plano individual (`plano_saude`) | ANS | gov.br/ans | anual (maio/junho) |
| | Reajuste de remédios (`remedios`) | CMED / Anvisa | gov.br/anvisa | anual (março/abril) |
| Segurança SP | Homicídios, celulares, roubo de veículos | SSP-SP | ssp.sp.gov.br/estatistica | mensal/anual |
| Estados | Vencedor e % no 2º turno | TSE | resultados.tse.jus.br | a cada eleição |
| | PIB por pessoa | IBGE – Contas Regionais | ibge.gov.br | anual (novembro) |
| | Mortes violentas por 100 mil | Fórum Brasileiro de Segurança Pública – Anuário | forumseguranca.org.br | anual (julho) |
| | Renda por pessoa | IBGE – PNAD Contínua (renda domiciliar per capita) | agenciadenoticias.ibge.gov.br | anual (fevereiro) |
| | Desemprego por estado | IBGE – PNAD Contínua trimestral, SIDRA 4099 | sidra.ibge.gov.br/tabela/4099 | trimestral (meio de fev., mai., ago., nov.) |
| | Analfabetismo 15+ | IBGE – PNAD Contínua Educação, SIDRA 7113 | sidra.ibge.gov.br/tabela/7113 | anual (junho) |
| | % de casas com Bolsa Família | IBGE – PNAD Contínua Rendimento, SIDRA 7449 ÷ (7449 + 7450) | sidra.ibge.gov.br/tabela/7449 | anual (maio) |
| | Expectativa de vida | IBGE – Projeções da População (revisão 2024) e Tábuas de Mortalidade | ibge.gov.br (projeção da população) | anual (novembro, Tábuas) |

Mapa: fronteiras dos estados do projeto [geodata-br-states](https://github.com/giuliano-oliveira/geodata-br-states) (licença MIT), simplificadas em `mapa-br.json` por `scripts/gerar_mapa.py`.
