# Diário

Uma entrada por fase, sempre no mesmo formato: o que eu queria saber, o que pedi, o que a IA respondeu, como conferi, o que decidi e a fase em uma frase. O raciocínio completo de cada decisão está em `DECISOES.md`.

---

## Fase 0 — Preparação do ambiente (25/09/2026)

**O que eu queria saber.** Se dava para começar sem risco de estragar a entrega: pasta certa, nenhum arquivo indevido no PR e um ambiente que outra pessoa consiga reproduzir.

**O que pedi.** "Vamos começar o teste." O Claude Code leu o meu plano, preparou o ambiente e parou para eu decidir cada escolha.

**O que a IA respondeu.**
- O próprio repositório do desafio manda o git ignorar a pasta `submissions/` inteira (linha 16 do `.gitignore` da raiz). Sem forçar, nenhum arquivo da entrega entraria no PR. Forçando a pasta inteira, a base de 23 MB entraria junto.
- As pastas criadas antes não batiam com o plano.
- Gráfico em plotly pode não aparecer no notebook visto pelo GitHub. Sugeriu matplotlib, que grava o gráfico como imagem.
- A captura automática de tela falhou: o macOS não dá ao Claude Code permissão para gravar a tela.

**Como conferi.** Comandos e saídas estão no transcript.
- `git check-ignore -v` mostrou a regra `submissions/` na linha 16 do `.gitignore` da raiz.
- 21 PRs de outros candidatos alteraram esse arquivo. Não alterei: o `CONTRIBUTING.md` diz que PR com arquivo fora da pasta do candidato é rejeitado.
- O ambiente novo abriu a base inteira (52.214 linhas, 27 colunas), e as versões instaladas batem com o `requirements.txt`.
- Antes do commit, a lista de arquivos preparados tinha só três: `.gitignore`, `requirements.txt` e este diário.

**O que decidi.**
- Criar a minha cópia do repositório no GitHub (fork).
- Dependências enxutas, com matplotlib no lugar de plotly.
- E-mail "noreply" do GitHub nos commits, para não expor meu e-mail.
- Não mexer no `.gitignore` da raiz. Cada arquivo entra pelo nome.
- Screenshots só da aplicação.
- Aprovação manual durante a criação do fork e do ambiente. Depois disso, modo automático.

**Em uma frase.** Preparei o ambiente e descobri que o próprio repositório esconde a pasta de entrega do git, o que pede cuidado em cada commit.

**Transcript.** Sessão 1, em `evidencias/transcripts/`.
