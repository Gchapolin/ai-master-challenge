# Como ler este process log

Uma página para quem não é da área técnica: o que foi feito, em que ordem e como conferir.

## O que foi feito, em ordem

1. **Pesquisa (sessão 0, cerca de 1 hora).** Li o desafio, os PRs dos outros candidatos e as reviews públicas do avaliador. Pedi um plano ao Claude, pedi a outro modelo que achasse as falhas dele e mandei refazer.
2. **Execução (sessão 1, cerca de 7 horas).** Sete fases: ambiente, baseline, laudo do dado, análise, estratégia, Radar e fechamento. A IA fez o trabalho braçal e parou em cada decisão que o plano marcava como minha.

## Onde está cada coisa

| Arquivo | O que tem |
|---|---|
| [`DIARIO.md`](DIARIO.md) | Uma entrada por fase: o que eu queria saber, o que pedi, o que a IA respondeu, como conferi e o que decidi |
| [`DECISOES.md`](DECISOES.md) | As decisões humanas, escritas por mim |
| [`evidencias/baseline/`](evidencias/baseline/) | O enunciado cru num Claude sem contexto, e onde a resposta dele erra |
| [`evidencias/screenshots/`](evidencias/screenshots/) | Prints das minhas respostas nas perguntas de decisão e das telas do Radar |
| [`evidencias/transcripts/`](evidencias/transcripts/) | As conversas inteiras com o Claude Code |

## Declarações

- **Pesquisa antes de começar.** Li o repositório, as reviews públicas do avaliador e as submissões anteriores, e usei isso para definir o critério de qualidade. A sessão de pesquisa está nos transcripts.
- **Modo de aprovação.** A pesquisa rodou em modo automático, só com leitura e planejamento. Na execução, a criação do fork e do ambiente teve aprovação manual; depois, decidi seguir em modo automático, com a IA parando nas decisões. O avaliador já apontou o modo automático como ponto negativo em outra submissão. Preferi declarar.
- **Screenshots.** A captura automática falhou, porque o macOS não deu ao Claude Code permissão para gravar a tela. Os prints são meus. Os transcripts mostram o resto.
- **Transcripts.** Cada sessão está em dois formatos: um Markdown legível, com pedidos, respostas e uma linha por ferramenta usada, e o registro completo em JSONL compactado. Um script removeu o meu e-mail, os caminhos da minha pasta pessoal, o meu arquivo de configuração pessoal do Claude (CLAUDE.md global), o ID da organização, a cópia do prompt de sistema do Claude Code e as imagens. O arquivo de instruções do projeto (CLAUDE.md do projeto) ficou, porque mostra as regras que dei à IA. Ele não faz parte da entrega.
- **Baseline.** Feito com o mesmo fornecedor de IA (Claude), em modo seguro, sem nenhum contexto meu: só o enunciado e o CSV. A primeira tentativa foi descartada, porque herdou as instruções do projeto.

## Como conferir

- Todo número do README aponta para o documento e a seção do notebook que o gera.
- Os testes automáticos rodam com `python -m pytest` (instruções no README).
- Os commits seguem a ordem das fases, um por etapa.

## Glossário

1. **Engajamento:** (likes + shares + comentários) / views.
2. **Célula:** uma combinação de plataforma, categoria e formato, como "TikTok, beauty, vídeo".
3. **Diferença:** quanto um grupo de posts rende acima ou abaixo de todos os outros.
4. **Intervalo de 95%:** a faixa onde a diferença real provavelmente está.
5. **Limiar de 10%:** a menor diferença que justifica mudar a estratégia. Foi definido antes de olhar os dados.
6. **Correção para muitas comparações (Benjamini-Hochberg):** com centenas de comparações, algumas parecem importantes por acaso. A correção tira esses falsos achados.
7. **Sinal e ruído:** sinal é a diferença acima de 10%, confiável depois da correção e com pelo menos 30 posts. O resto é ruído.
8. **Simulação:** efeitos de tamanho conhecido plantados numa cópia do dado, para provar que o método os acharia.
9. **Efeito mínimo detectável:** o menor efeito que um teste consegue enxergar com o número de posts disponível.
10. **Baseline:** a resposta de uma IA que recebe só o enunciado, sem nenhum trabalho meu, para comparar com a entrega.
