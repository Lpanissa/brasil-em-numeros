// Dinheiro dos estados, direto do Tesouro Nacional (SICONFI, Relatório Resumido da Execução Orçamentária, Anexo 3).
// Para cada estado pega os últimos 12 meses de: Receita Corrente Líquida, ICMS e repasse do FPE.
// Guarda 1 dia em cache (o Tesouro só atualiza a cada bimestre).
const UF = { RO: 11, AC: 12, AM: 13, RR: 14, PA: 15, AP: 16, TO: 17, MA: 21, PI: 22, CE: 23, RN: 24, PB: 25, PE: 26, AL: 27, SE: 28, BA: 29, MG: 31, ES: 32, RJ: 33, SP: 35, PR: 41, SC: 42, RS: 43, MS: 50, MT: 51, GO: 52, DF: 53 };
const base = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2003";
const pega = async (ano, per, id) => {
  const r = await fetch(`${base}&an_exercicio=${ano}&nr_periodo=${per}&id_ente=${id}`);
  if (!r.ok) return null;
  const it = (await r.json()).items || [];
  const tot = it.filter(i => i.coluna === "TOTAL (ÚLTIMOS 12 MESES)");
  if (!tot.length) return null;
  const v = re => { const x = tot.find(i => re.test(i.conta)); return x ? +x.valor : null };
  return { rcl: v(/^RECEITA CORRENTE LÍQUIDA \(III\)/), icms: v(/^ICMS$/), fpe: v(/^Cota-Parte do FPE$/) };
};
export async function onRequestGet(ctx) {
  const cache = caches.default, chave = new Request("https://cache.raiox/estados-fin/v1");
  const guardado = await cache.match(chave);
  if (guardado) return guardado;
  // descobre o bimestre mais recente publicado, testando em São Paulo
  const hoje = new Date();
  let ano = hoje.getFullYear(), per = Math.min(6, Math.floor(hoje.getMonth() / 2)), achou = null;
  for (let k = 0; k < 4 && !achou; k++) {
    if (per < 1) { ano--; per = 6 }
    const sp = await pega(ano, per, 35);
    if (sp && sp.rcl) achou = { ano, per, sp }; else per--;
  }
  if (!achou) return new Response(JSON.stringify({ erro: "sem dados" }), { status: 502, headers: { "content-type": "application/json" } });
  const est = { SP: achou.sp };
  await Promise.all(Object.entries(UF).filter(([u]) => u !== "SP").map(async ([u, id]) => {
    est[u] = await pega(achou.ano, achou.per, id);
  }));
  const resp = new Response(JSON.stringify({ ano: achou.ano, bimestre: achou.per, estados: est }), {
    headers: { "content-type": "application/json", "cache-control": "public, max-age=86400" },
  });
  ctx.waitUntil(cache.put(chave, resp.clone()));
  return resp;
}
