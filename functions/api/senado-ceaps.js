// Gastos da cota parlamentar dos senadores (CEAPS), direto dos dados abertos do Senado.
// O arquivo oficial traz todas as notas do ano; aqui somamos por senador e por tipo
// e guardamos 6 horas em cache, para o site baixar só o resumo.
export async function onRequestGet(ctx) {
  const ano = new URL(ctx.request.url).searchParams.get("ano") || String(new Date().getFullYear());
  if (!/^20\d\d$/.test(ano)) return new Response("ano inválido", { status: 400 });
  const cache = caches.default, chave = new Request("https://cache.raiox/senado-ceaps/" + ano);
  const guardado = await cache.match(chave);
  if (guardado) return guardado;
  const r = await fetch(`https://adm.senado.gov.br/adm-dadosabertos/api/v1/senadores/despesas_ceaps/${ano}`);
  if (!r.ok) return new Response(JSON.stringify({ erro: r.status }), { status: 502, headers: { "content-type": "application/json" } });
  const notas = await r.json(), por = {};
  let ultimoMes = 0;
  for (const n of notas) {
    const s = (por[n.codSenador] ??= { nome: n.nomeSenador, total: 0, tipos: {} });
    const v = +n.valorReembolsado || 0;
    s.total += v;
    const t = (n.tipoDespesa || "Outros").split(",")[0].replace(/\.$/, "");
    s.tipos[t] = (s.tipos[t] || 0) + v;
    if (n.mes > ultimoMes) ultimoMes = n.mes;
  }
  const resp = new Response(JSON.stringify({ ano: +ano, ateMes: ultimoMes, senadores: por }), {
    headers: { "content-type": "application/json", "cache-control": "public, max-age=21600" },
  });
  ctx.waitUntil(cache.put(chave, resp.clone()));
  return resp;
}
