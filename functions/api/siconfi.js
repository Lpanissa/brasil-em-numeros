// Ponte para a API do Tesouro (SICONFI): a API oficial não libera acesso direto do navegador (CORS).
// Só repassa consultas de leitura aos relatórios públicos e guarda 1 dia em cache.
const PERMITIDOS = new Set(["rreo", "rgf", "dca", "entes"]);
export async function onRequestGet(ctx) {
  const u = new URL(ctx.request.url), rel = u.searchParams.get("rel");
  if (!PERMITIDOS.has(rel)) return new Response("relatório não permitido", { status: 400 });
  u.searchParams.delete("rel");
  const alvo = `https://apidatalake.tesouro.gov.br/ords/siconfi/tt/${rel}?${u.searchParams}`;
  const cache = caches.default, chave = new Request(alvo);
  const guardado = await cache.match(chave);
  if (guardado) return guardado;
  const r = await fetch(alvo, { headers: { "User-Agent": "RaioXdoBrasil/1.0" } });
  const resp = new Response(r.body, { status: r.status, headers: { "content-type": "application/json", "cache-control": "public, max-age=86400" } });
  if (r.ok) ctx.waitUntil(cache.put(chave, resp.clone()));
  return resp;
}
