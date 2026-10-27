// Foto oficial de candidatura no TSE (DivulgaCandContas), servida pelo próprio site com cache longo.
// Evita que o navegador do visitante dependa do site do TSE (que às vezes bloqueia acesso direto).
export async function onRequestGet({ request, waitUntil }) {
  const u = new URL(request.url);
  const el = u.searchParams.get("el"), sq = u.searchParams.get("sq"), uf = (u.searchParams.get("uf") || "").toUpperCase();
  if (!/^\d{8,12}$/.test(el || "") || !/^\d{6,14}$/.test(sq || "") || !/^[A-Z]{2}$/.test(uf)) return new Response("parâmetros inválidos", { status: 400 });
  const cache = caches.default, chave = new Request(`https://cache.raiox/foto/${el}/${sq}/${uf}`);
  const g = await cache.match(chave); if (g) return g;
  const r = await fetch(`https://divulgacandcontas.tse.jus.br/divulga/rest/arquivo/img/${el}/${sq}/${uf}`, {
    headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36", "Accept": "image/*", "Referer": "https://divulgacandcontas.tse.jus.br/divulga/" },
    cf: { cacheTtl: 2592000 },
  });
  const tipo = r.headers.get("content-type") || "";
  if (!r.ok || !tipo.startsWith("image/")) return new Response("sem foto", { status: 404 });
  const resp = new Response(r.body, { headers: { "content-type": tipo, "cache-control": "public, max-age=2592000" } });
  waitUntil(cache.put(chave, resp.clone()));
  return resp;
}
