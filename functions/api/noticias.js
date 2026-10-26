// Últimas notícias de fontes públicas oficiais (IBGE, Agência Brasil, Agência Senado, Agência Câmara).
// Lê a API de notícias do IBGE e os feeds RSS das agências, junta tudo, marca o estado citado
// e guarda 15 minutos em cache. Só título, resumo curto, imagem e link: o texto completo fica na fonte.
const FEEDS = [
  { fonte: "Agência Brasil", url: "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml" },
  { fonte: "Agência Senado", url: "https://www12.senado.leg.br/noticias/feed/todasnoticias/RSS" },
  { fonte: "Agência Câmara", url: "https://www.camara.leg.br/noticias/rss/ultimas-noticias" },
];
const ESTADOS = { AC: "Acre", AL: "Alagoas", AP: "Amapá", AM: "Amazonas", BA: "Bahia", CE: "Ceará", DF: "Distrito Federal", ES: "Espírito Santo", GO: "Goiás", MA: "Maranhão", MT: "Mato Grosso", MS: "Mato Grosso do Sul", MG: "Minas Gerais", PA: "Pará", PB: "Paraíba", PR: "Paraná", PE: "Pernambuco", PI: "Piauí", RJ: "Rio de Janeiro", RN: "Rio Grande do Norte", RS: "Rio Grande do Sul", RO: "Rondônia", RR: "Roraima", SC: "Santa Catarina", SP: "São Paulo", SE: "Sergipe", TO: "Tocantins" };
const UA = { "User-Agent": "Mozilla/5.0 (compatible; RaioXdoBrasil/1.0; +https://raioxdobrasil.com.br)" };

const ent = s => s.replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1").replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
  .replace(/&quot;/g, '"').replace(/&#039;|&apos;/g, "'").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&");
const limpa = s => ent(s || "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
const corta = (s, n) => s.length > n ? s.slice(0, n).replace(/\s+\S*$/, "") + "…" : s;
const tag = (xml, t) => { const m = xml.match(new RegExp(`<${t}[^>]*>([\\s\\S]*?)</${t}>`, "i")); return m ? m[1] : "" };

function estados(txt) {
  const out = [];
  for (const [uf, nome] of Object.entries(ESTADOS)) {
    // "Pará" não pode casar com "para"; nomes compostos têm prioridade sobre os curtos
    if (new RegExp(`(^|[^\\p{L}])${nome}([^\\p{L}]|$)`, "u").test(txt)) out.push(uf);
  }
  if (out.includes("MS")) { const i = out.indexOf("MT"); if (i >= 0 && !/Mato Grosso(?! do Sul)/.test(txt)) out.splice(i, 1) }
  return out;
}

async function rss({ fonte, url }) {
  const r = await fetch(url, { headers: UA, cf: { cacheTtl: 600 } });
  if (!r.ok) return [];
  const xml = await r.text();
  return [...xml.matchAll(/<item[\s>][\s\S]*?<\/item>/gi)].slice(0, 15).map(([it]) => {
    const desc = tag(it, "description"), cont = tag(it, "content:encoded");
    const img = (it.match(/<enclosure[^>]+url="([^"]+)"/i) || it.match(/<media:(?:content|thumbnail)[^>]+url="([^"]+)"/i) || ent(desc + cont).match(/<img[^>]+src="([^"]+)"/i) || [])[1] || null;
    const titulo = limpa(tag(it, "title")), resumo = corta(limpa(desc), 260);
    const data = Date.parse(limpa(tag(it, "pubDate")) || limpa(tag(it, "dc:date"))) || 0;
    return { fonte, titulo, resumo, link: limpa(tag(it, "link")), img, data, uf: estados(titulo + " " + resumo) };
  }).filter(n => n.titulo && n.link);
}

async function ibge() {
  const r = await fetch("https://servicodados.ibge.gov.br/api/v3/noticias/?qtd=15", { headers: UA });
  if (!r.ok) return [];
  const j = await r.json();
  return (j.items || []).map(n => {
    let img = null;
    try { const i = JSON.parse(n.imagens || "{}"); if (i.image_intro) img = "https://agenciadenoticias.ibge.gov.br/" + i.image_intro.replace(/^\//, "") } catch (e) {}
    const [d, h] = (n.data_publicacao || "").split(" "), [dd, mm, aa] = (d || "").split("/");
    const resumo = corta(limpa(n.introducao), 260);
    return { fonte: "IBGE", titulo: limpa(n.titulo), resumo, link: n.link, img, data: Date.parse(`${aa}-${mm}-${dd}T${h || "00:00:00"}-03:00`) || 0, uf: estados(n.titulo + " " + resumo) };
  });
}

export async function onRequestGet(ctx) {
  const cache = caches.default, chave = new Request("https://cache.raiox/noticias/v1");
  const guardado = await cache.match(chave);
  if (guardado) return guardado;
  const listas = await Promise.all([ibge(), ...FEEDS.map(rss)].map(p => p.catch(() => [])));
  const vistos = new Set(), itens = listas.flat().filter(n => !vistos.has(n.link) && vistos.add(n.link)).sort((a, b) => b.data - a.data).slice(0, 60);
  const resp = new Response(JSON.stringify({ geradoEm: Date.now(), itens, fontes: listas.map((l, i) => ({ fonte: i ? FEEDS[i - 1].fonte : "IBGE", n: l.length })) }), {
    headers: { "content-type": "application/json", "cache-control": "public, max-age=900" },
  });
  ctx.waitUntil(cache.put(chave, resp.clone()));
  return resp;
}
