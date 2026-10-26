// Últimas votações nominais do Plenário da Câmara (Dados Abertos da Câmara), com o voto de cada deputado.
// Ficam de fora os requerimentos (votações de procedimento). Guarda 6 horas em cache.
const B = "https://dadosabertos.camara.leg.br/api/v2/";
const iso = d => d.toISOString().slice(0, 10);
const TIPOS = new Set(["PEC", "PL", "PLP", "MPV", "PDL", "PLN", "PLV"]);
const COD = { "Sim": "S", "Não": "N", "Abstenção": "A", "Obstrução": "O", "Artigo 17": "P" };

export async function onRequestGet(ctx) {
  const cache = caches.default, chave = new Request("https://cache.raiox/camara-votacoes/v1");
  const guardado = await cache.match(chave);
  if (guardado) return guardado;
  const hoje = new Date(), j1 = [iso(new Date(+hoje - 89 * 864e5)), iso(hoje)], j2 = [iso(new Date(+hoje - 179 * 864e5)), iso(new Date(+hoje - 90 * 864e5))];
  let lista = [];
  for (const [a, b] of [j1, j2]) {
    for (let p = 1; p <= 4; p++) {
      const r = await fetch(`${B}votacoes?idOrgao=180&dataInicio=${a}&dataFim=${b}&ordem=DESC&ordenarPor=dataHoraRegistro&itens=100&pagina=${p}`, { headers: { accept: "application/json" } });
      if (!r.ok) break;
      const d = (await r.json()).dados || [];
      lista = lista.concat(d);
      if (d.length < 100) break;
    }
    if (lista.filter(v => /Sim:\s*\d+/.test(v.descricao || "") && !/Requerimento/i.test(v.descricao || "")).length >= 12) break;
  }
  const sel = lista.filter(v => /Sim:\s*\d+/.test(v.descricao || "") && !/Requerimento/i.test(v.descricao || "")).slice(0, 12);
  const out = await Promise.all(sel.map(async v => {
    const [det, vt] = await Promise.all([
      fetch(B + "votacoes/" + v.id, { headers: { accept: "application/json" } }).then(r => r.json()).catch(() => ({})),
      fetch(B + "votacoes/" + v.id + "/votos", { headers: { accept: "application/json" } }).then(r => r.json()).catch(() => ({})),
    ]);
    const x = det.dados || {}, props = [...(x.proposicoesAfetadas || []), ...(x.objetosPossiveis || [])];
    const p = props.find(p => TIPOS.has(p.siglaTipo)) || props[0] || {};
    const votos = {}, partidos = {}, placar = {};
    for (const o of (vt.dados || [])) {
      const t = o.tipoVoto, dep = o.deputado_ || {};
      votos[dep.id] = COD[t] || "?";
      placar[t] = (placar[t] || 0) + 1;
      const pt = dep.siglaPartido || "Sem partido";
      (partidos[pt] ??= {})[t] = (partidos[pt][t] || 0) + 1;
    }
    return {
      id: v.id, data: v.data, descricao: (v.descricao || "").replace(/\s*Sim:.*$/, "").trim(), aprovada: v.aprovacao === 1,
      prop: p.siglaTipo ? `${p.siglaTipo} ${p.numero}/${p.ano}` : "", ementa: p.ementa || "", idProp: p.id || null,
      placar, partidos, votos,
    };
  }));
  const resp = new Response(JSON.stringify({ geradoEm: Date.now(), votacoes: out.filter(o => Object.keys(o.votos).length) }), {
    headers: { "content-type": "application/json", "cache-control": "public, max-age=21600" },
  });
  ctx.waitUntil(cache.put(chave, resp.clone()));
  return resp;
}
