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
- Screenshots só da aplicação. Depois mudei: guardei também prints das minhas respostas nas perguntas de decisão.
- Aprovação manual durante a criação do fork e do ambiente. Depois disso, modo automático.

**Em uma frase.** Preparei o ambiente e descobri que o próprio repositório esconde a pasta de entrega do git, o que pede cuidado em cada commit.

**Transcript.** Sessão 1, em `evidencias/transcripts/`.

**Print.** `evidencias/screenshots/00-setup_01.png`: minhas respostas às perguntas sobre modo, fork, dependências e e-mail.

---

## Fase 2 — Métricas, método e laudo do dado (25/09/2026)

**O que eu queria saber.** Se o arquivo consegue dizer o que funciona e se o método de análise acharia um efeito caso ele existisse.

**O que pedi.** "Segue aí." O Claude Code executou a Fase 2 do plano, escrevendo cada teste automático antes do código.

**O que a IA respondeu.**
- Views, likes, shares e comentários se comportam como sorteio em torno de um valor fixo: nas quatro métricas, o desvio-padrão é igual à raiz da média.
- O número de seguidores é sorteado de novo a cada post. Os 5.000 creators mudam de tamanho de um post para outro, então a faixa do creator não é confiável.
- As proporções são redondas, o patrocinador não tem relação com o conteúdo e os textos são palavras sorteadas.
- Na simulação, um efeito de +15% vira sinal sempre, +10% em metade das vezes e +3% nunca, sem nenhum falso sinal.
- A camada de "alocação" do meu plano também sai de sorteio, e o achado "95% dos posts em creators de 50 mil ou mais" não se sustenta.

**Como conferi.** Comandos, testes e saídas estão no transcript.
- 43 testes automáticos, cada um escrito antes do código e visto falhando antes de passar.
- Um teste de fronteira pegou um erro da IA: ela implementou a regra como "10% ou mais", mas o plano diz "mais de 10%". Corrigido.
- A simulação desmentiu o próprio plano, que dizia que um efeito de +10% "deve ser encontrado". Na prática, 10% é a fronteira da regra, e esse efeito vira sinal em 51,5% das rodadas.
- Na revisão do laudo, a IA viu que uma conta dela ("nenhum grupo difere em mais de cerca de 1%") só vale para grupos grandes. Para um grupo com 0,2% dos posts, a mesma conta deixaria espaço para cerca de 13% em shares. A afirmação saiu do laudo e do notebook, e a medição grupo a grupo ficou para a análise.
- O notebook roda do zero, e cada número do laudo aponta para a seção que o gera.

**O que decidi.**
- Manter as duas camadas, reescritas: "Resultado: sem sinal. Operação: sem critério." O achado das faixas de creator sai.
- Manter a simulação com +15%, +10% e +3% e explicar que 10% é a fronteira.
- Manter o limiar de 10%.
- Fazer push para o meu fork no fim de cada fase.

**Em uma frase.** O arquivo não diz o que funciona, e o método provou que diria se houvesse algo a dizer.

**Transcript.** Sessão 1, em `evidencias/transcripts/`.

**Print.** `evidencias/screenshots/02-laudo_01.png`: minhas respostas sobre a tese, a simulação e o push.
