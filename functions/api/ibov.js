// Ponte do Ibovespa: o navegador não consegue ler as fontes de bolsa direto (bloqueio de CORS),
// então esta função do Cloudflare busca o índice no servidor e entrega um JSON simples ao site.
// Guarda a resposta em cache por 5 minutos para não sobrecarregar a fonte.
const UA = { "User-Agent": "Mozilla/5.0 (compatible; RaioXdoBrasil/1.0; +https://raioxdobrasil.com.br)" };

async function yahoo() {
  const r = await fetch("https://query1.finance.yahoo.com/v8/finance/chart/%5EBVSP?interval=1d&range=1d", { headers: UA });
  if (!r.ok) throw new Error("yahoo " + r.status);
  const m = (await r.json()).chart.result[0].meta;
  const v = m.regularMarketPrice, ant = m.chartPreviousClose ?? m.previousClose;
  if (!v) throw new Error("yahoo sem valor");
  return { v, ant, t: m.regularMarketTime * 1000, fonte: "Yahoo Finance (B3, com atraso)" };
}

async function stooq() {
  const r = await fetch("https://stooq.com/q/l/?s=%5Ebvp&f=sd2t2ohlcp&h&e=csv", { headers: UA });
  if (!r.ok) throw new Error("stooq " + r.status);
  const [, linha] = (await r.text()).trim().split("\n");
  const [, data, hora, , , , fech, ant] = linha.split(",");
  const v = +fech;
  if (!v) throw new Error("stooq sem valor");
  return { v, ant: +ant || null, t: Date.parse(`${data}T${hora}Z`), fonte: "Stooq (B3, com atraso)" };
}

export async function onRequestGet(ctx) {
  const cache = caches.default, chave = new Request(new URL(ctx.request.url).origin + "/api/ibov");
  const guardado = await cache.match(chave);
  if (guardado) return guardado;
  let dados = null;
  for (const f of [yahoo, stooq]) { try { dados = await f(); break } catch (e) {} }
  if (!dados) return new Response(JSON.stringify({ erro: "indisponível" }), { status: 503, headers: { "content-type": "application/json" } });
  const p = dados.ant ? (dados.v / dados.ant - 1) * 100 : null;
  const resp = new Response(JSON.stringify({ ...dados, p }), {
    headers: { "content-type": "application/json", "cache-control": "public, max-age=300" },
  });
  ctx.waitUntil(cache.put(chave, resp.clone()));
  return resp;
}
