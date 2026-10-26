// Últimas notícias de fontes públicas oficiais (IBGE, Agência Brasil, Agência Senado, Agência Câmara).
// Lê a API de notícias do IBGE e os feeds RSS das agências, junta tudo, marca o estado citado
// e guarda 15 minutos em cache. Só título, resumo curto, imagem e link: o texto completo fica na fonte.
const FEEDS = [
  { fonte: "Planalto", url: "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/noticias/RSS", peso: 2 },
  { fonte: "Agência Brasil", url: "https://agenciabrasil.ebc.com.br/rss/politica/feed.xml", peso: 1 },
  { fonte: "Agência Brasil", url: "https://agenciabrasil.ebc.com.br/rss/economia/feed.xml", peso: 1 },
  { fonte: "Agência Brasil", url: "https://agenciabrasil.ebc.com.br/rss/internacional/feed.xml", peso: 1 },
  { fonte: "Agência Brasil", url: "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml", peso: 0 },
  { fonte: "Agência Senado", url: "https://www12.senado.leg.br/noticias/feed/todasnoticias/RSS", peso: 0 },
  { fonte: "Agência Câmara", url: "https://www.camara.leg.br/noticias/rss/ultimas-noticias", peso: 0 },
];
// Relevância nacional: decisões e falas do presidente, governo federal, Congresso aprovando leis, STF, economia e diplomacia.
// Notícias locais, policiais, de esporte, agenda de comissões, áudios e vídeos ficam de fora.
const FORTE = /\b(presidente|Lula|Alckmin|Planalto|ministr[oa]s?|STF|Supremo|sanciona|sancion|veta|vet[oa]u|decreto|medida provisória|PEC|reforma|Congresso aprova|Senado aprova|Câmara aprova|aprovad[oa] (?:em|no|pelo) (?:Plenário|Senado)|Copom|Selic|inflação|IPCA|PIB|desemprego|salário mínimo|Banco Central|Tesouro|Orçamento|arcabouço|imposto|tarifa|exporta|importa|acordo|cúpula|diplomac|Itamaraty|embaixad|chanceler|G20|BRICS|Mercosul|ONU|Estados Unidos|China|União Europeia|guerra|eleiç|TSE|Petrobras|Bolsa Família|Previdência|INSS|SUS)/i;
const FORA = /^(áudio|vídeo|video|podcast|agenda)\b|\b(futebol|campeonato|Mega-Sena|loteria|Lotofácil|BBB|novela|horóscopo|ocorrências|detidos|PM registra|acidente|trânsito|show|festival|carnaval|celebridade)\b/i;
function relevancia(n, peso) {
  const t = n.titulo + " " + n.resumo;
  if (FORA.test(n.titulo)) return -1;
  const fortes = (t.match(new RegExp(FORTE.source, "gi")) || []).length;
  return peso + Math.min(fortes, 3) + (FORTE.test(n.titulo) ? 1 : 0);
}
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

async function rss({ fonte, url, peso }) {
  const r = await fetch(url, { headers: UA, cf: { cacheTtl: 600 } });
  if (!r.ok) return [];
  const xml = await r.text();
  return [...xml.matchAll(/<item[\s>][\s\S]*?<\/item>/gi)].slice(0, 15).map(([it]) => {
    const desc = tag(it, "description"), cont = tag(it, "content:encoded");
    let img = (it.match(/<enclosure[^>]+url="([^"]+)"/i) || it.match(/<media:(?:content|thumbnail)[^>]+url="([^"]+)"/i) || ent(desc + cont).match(/<img[^>]+src="([^"]+)"/i) || [])[1] || null;
    if (img && /logo|\.svg(\?|$)/i.test(img)) img = null; // logotipo da agência não é foto da notícia
    const titulo = limpa(tag(it, "title")), resumo = corta(limpa(desc), 260);
    const data = Date.parse(limpa(tag(it, "pubDate")) || limpa(tag(it, "dc:date"))) || 0;
    const n = { fonte, titulo, resumo, link: limpa(tag(it, "link")), img, data, uf: estados(titulo + " " + resumo) };
    n.rel = relevancia(n, peso);
    return n;
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
    const o = { fonte: "IBGE", titulo: limpa(n.titulo), resumo, link: n.link, img, data: Date.parse(`${aa}-${mm}-${dd}T${h || "00:00:00"}-03:00`) || 0, uf: estados(n.titulo + " " + resumo) };
    o.rel = relevancia(o, 0);
    return o;
  });
}

export async function onRequestGet(ctx) {
  const cache = caches.default, chave = new Request("https://cache.raiox/noticias/v3");
  const guardado = await cache.match(chave);
  if (guardado) return guardado;
  const listas = await Promise.all([ibge(), ...FEEDS.map(rss)].map(p => p.catch(() => [])));
  // só entra o que tem peso nacional (relevância 2 ou mais); as últimas 48 horas primeiro, mais relevantes na frente
  const vistos = new Set(), agora = Date.now();
  const itens = listas.flat().filter(n => n.rel >= 2 && !vistos.has(n.link) && vistos.add(n.link))
    .sort((a, b) => ((agora - b.data < 48 * 36e5) - (agora - a.data < 48 * 36e5)) || (b.rel - a.rel) || (b.data - a.data)).slice(0, 60);
  // notícias sem foto no feed: busca a imagem de capa (og:image) na própria página da notícia
  await Promise.all(itens.filter(n => !n.img).slice(0, 25).map(async n => {
    try {
      const r = await fetch(n.link, { headers: UA, cf: { cacheTtl: 3600 } });
      if (!r.ok) return;
      const h = (await r.text()).slice(0, 60000);
      const m = h.match(/<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']+)["']/i) || h.match(/<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:image["']/i);
      if (m && !/logo|\.svg(\?|$)/i.test(m[1])) n.img = ent(m[1]);
    } catch (e) {}
  }));
  const resp = new Response(JSON.stringify({ geradoEm: Date.now(), itens, fontes: listas.map((l, i) => ({ fonte: i ? FEEDS[i - 1].url : "IBGE", n: l.length, relevantes: l.filter(x => x.rel >= 2).length })) }), {
    headers: { "content-type": "application/json", "cache-control": "public, max-age=900" },
  });
  ctx.waitUntil(cache.put(chave, resp.clone()));
  return resp;
}
