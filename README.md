# Ponto Cruz — Planejador

Transforma imagens em gráficos de **ponto cruz (DMC)** ou **Hama Beads (Midi)**, com editor, legenda de cores, contagem de meadas/contas, marcação de pontos feitos e medidas da caixa com tampa de ponto cruz para o **3D Workbench**.

HTML, CSS e JS puro, num arquivo só, sem dependências. Funciona offline.

## Instalar no iPad

1. Abra o link do GitHub Pages no **Safari**.
2. Toque em **Compartilhar → Adicionar à Tela de Início**.
3. Abra pelo ícone: o app ocupa a tela inteira e funciona sem internet depois da primeira abertura.

Os projetos ficam salvos no próprio iPad. Use **Salvar .json** de vez em quando como cópia de segurança.

## Estrutura

| Arquivo | O que é |
|---|---|
| `index.html` | O app pronto (gerado — não edite à mão) |
| `src/app.html` | Código-fonte do app |
| `src/dmc.txt` | Catálogo de cores DMC (`código\|nome\|R G B`) |
| `build.py` | Junta `src/` em `index.html` e atualiza a versão do cache |
| `sw.js` | Service worker (modo offline) |
| `manifest.webmanifest`, `icons/` | Ícone e dados do app instalado |

## Atualizar

```bash
python3 build.py
git add -A && git commit -m "..." && git push
```

No iPad, abra o app com internet uma vez para ele pegar a versão nova (às vezes é preciso fechar e abrir de novo).

## Integração com o 3D Workbench

Na aba **Peça**, use **Exportar para o Workbench (.json)** e importe no Workbench em **Projetos salvos → Importar do Ponto Cruz**. Ele monta a caixa com tampa de ponto cruz no tamanho certo para todos os furos do desenho.
