"""Gera o index.html a partir de src/app.html + src/dmc.txt.

Uso:  python3 build.py
Depois de mudar qualquer coisa em src/, rode de novo e faça o commit do index.html.
Também troca a versão do cache do sw.js para o iPad baixar a versão nova.
"""
import datetime
import hashlib
import pathlib
import re

raiz = pathlib.Path(__file__).parent
app = (raiz / "src/app.html").read_text(encoding="utf-8")
dmc = (raiz / "src/dmc.txt").read_text(encoding="utf-8").strip()

head_pwa = """<meta name="theme-color" content="#1c1c1f">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="Ponto Cruz">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="data:image/png;base64,__ICO180__">
<link rel="icon" type="image/png" href="data:image/png;base64,__ICO64__">
"""

sw = """<script>
if ('serviceWorker' in navigator && location.protocol === 'https:') {
  // Ao sair uma versão nova, o app instalado troca sozinho (recarrega uma vez).
  const tinhaControle = !!navigator.serviceWorker.controller;
  let recarregou = false;
  navigator.serviceWorker.addEventListener('controllerchange', () => { if (tinhaControle && !recarregou) { recarregou = true; location.reload(); } });
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').then((reg) => {
      const checar = () => reg.update().catch(() => {});
      document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') checar(); });
      setInterval(checar, 30 * 60 * 1000);
    }).catch(() => {});
  });
}
</script>
</body>"""

html = app.replace("/*DMC*/", dmc).replace("/*VERSAO*/", "v" + datetime.datetime.now().strftime("%d/%m %H:%M"))
html = html.replace("<title>", head_pwa + "<title>", 1)
html = html.replace("</body>", sw, 1)
import base64
ico = lambda f: base64.b64encode((raiz / "icons" / f).read_bytes()).decode()
# Ícones embutidos: o arquivo sozinho (ex.: cópia no Drive) também leva o ícone.
html = html.replace("__ICO180__", ico("apple-touch-icon.png")).replace("__ICO64__", ico("favicon-64.png"))
(raiz / "index.html").write_text(html, encoding="utf-8")

versao = hashlib.sha1(html.encode()).hexdigest()[:10]
sw_js = (raiz / "sw.js").read_text(encoding="utf-8")
sw_js = re.sub(r"const VERSAO = '[^']*';", f"const VERSAO = '{versao}';", sw_js)
(raiz / "sw.js").write_text(sw_js, encoding="utf-8")
print(f"index.html gerado ({len(html) // 1024} KB) · cache {versao}")
