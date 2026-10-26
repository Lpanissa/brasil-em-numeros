// Impostos federais arrecadados no ano, pelo Tesouro Nacional (SICONFI, RREO Anexo 1 da União).
// Soma "Impostos, taxas e contribuições de melhoria" + "Contribuições" realizados até o último bimestre publicado
// e o ritmo médio do último bimestre, para o site estimar o valor ao vivo. Cache de 1 dia.
const B = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2001&id_ente=1";
const CONTAS = ["IMPOSTOS, TAXAS E CONTRIBUIÇÕES DE MELHORIA", "CONTRIBUIÇÕES"];

async function pega(ano, per) {
  const r = await fetch(`${B}&an_exercicio=${ano}&nr_periodo=${per}`);
  if (!r.ok) return null;
  const it = ((await r.json()).items || []).filter(i => CONTAS.includes(i.conta));
  const soma = col => it.filter(i => i.coluna === col).reduce((s, i) => s + (+i.valor || 0), 0);
  const acum = soma("Até o Bimestre (c)"), noBim = soma("No Bimestre (b)");
  return acum > 0 ? { acum, noBim } : null;
}

export async function onRequestGet(ctx) {
  const cache = caches.default, chave = new Request("https://cache.raiox/impostos/v1");
  const guardado = await cache.match(chave);
  if (guardado) return guardado;
  const hoje = new Date();
  let ano = hoje.getFullYear(), per = Math.min(6, Math.floor(hoje.getMonth() / 2)), d = null;
  for (let k = 0; k < 4 && !d; k++) {
    if (per < 1) { ano--; per = 6 }
    d = await pega(ano, per);
    if (!d) per--;
  }
  if (!d) return new Response(JSON.stringify({ erro: "sem dados" }), { status: 502, headers: { "content-type": "application/json" } });
  // fim do bimestre: último dia do mês 2*per, 23h59 de Brasília
  const fim = Date.UTC(ano, 2 * per, 1, 2, 59, 59) ; // 1º dia do mês seguinte, 02:59:59 UTC = 23:59:59 do último dia (UTC-3)
  const ini = Date.UTC(ano, 2 * per - 2, 1, 3, 0, 0);
  const porSegundo = d.noBim / ((fim - ini) / 1000);
  const resp = new Response(JSON.stringify({ ano, bimestre: per, acumulado: d.acum, fimBimestre: fim, porSegundo, fonte: "Tesouro Nacional · SICONFI · RREO da União" }), {
    headers: { "content-type": "application/json", "cache-control": "public, max-age=86400" },
  });
  ctx.waitUntil(cache.put(chave, resp.clone()));
  return resp;
}
