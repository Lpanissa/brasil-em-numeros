# Raio-X do Brasil

Site com dashboard do custo de vida e da economia no Brasil: juros, inflação, salários, cesta básica, contas da casa,
transporte, crédito, saúde e comparação entre estados (mapa PT × PL do 2º turno de 2026, PIB por pessoa e violência).
Inclui também a conferência do *Dossiê Socioeconômico e Eleitoral do Brasil*.

- **Dados:** Supabase (tabelas `painel_*` e `dossie_*`, leitura pública).
- **Coleta:** todo dia 15, com a coleta de 26/10/2026 como base. Fontes e roteiro em [FONTES.md](FONTES.md).
- **Hospedagem:** Cloudflare Pages (site estático, sem build).
- **Cópia de segurança:** `painel.json` e `dados-2026.json` são usados se o banco estiver fora do ar.

As cores do mapa mostram apenas quem venceu a eleição presidencial em cada estado; não indicam causa de riqueza ou violência.
