# Builds index.html (installable web app) from src.html (same source as the Claude Artifact prototype).
import re, pathlib
src = pathlib.Path('src.html').read_text()
title, rest = src.split('\n', 1)
head = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#EEF1F5" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F131B" media="(prefers-color-scheme: dark)">
<meta name="description" content="Compte les points de tes jeux de société : Skyjo, Flip 7, Uno, 6 qui prend et les autres.">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Tablée">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
''' + title + '''
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
'''
body_split = rest.index('<div id="app"')
styles = rest[:body_split]
body = rest[body_split:]
sw = '''<script>
if('serviceWorker' in navigator){
  window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').then(r=>r.update()).catch(()=>{}));
  // A new version took over: reload once, unless a round is being typed.
  let had = !!navigator.serviceWorker.controller, done = false;
  navigator.serviceWorker.addEventListener('controllerchange',()=>{
    if(!had){ had = true; return; } if(done) return; done = true;
    const busy = ()=>{ const s=document.getElementById('sheet'); return s && !s.hidden; };
    const go = ()=>{ if(busy()) setTimeout(go, 2000); else location.reload(); };
    go();
  });
}
try{ navigator.storage && navigator.storage.persist && navigator.storage.persist(); }catch(e){}
</script>
'''
out = head + styles + '</head>\n<body>\n' + body + sw + '</body>\n</html>\n'
pathlib.Path('index.html').write_text(out)
print('index.html', len(out))
