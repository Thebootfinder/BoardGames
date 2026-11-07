// Tablée service worker: works offline, refreshes the app in the background.
const CACHE = 'tablee-v6';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  if (req.mode === 'navigate') {
    // The page itself: network first so a new version shows on the first open, cache when offline or slow.
    e.respondWith(caches.open(CACHE).then(async cache => {
      const hit = () => cache.match(req, { ignoreSearch: true }).then(r => r || cache.match('./index.html'));
      try {
        const res = await Promise.race([fetch(req), new Promise((_, rej) => setTimeout(() => rej('slow'), 3500))]);
        if (res && res.ok) { cache.put(req, res.clone()); return res; }
        return (await hit()) || res;
      } catch (err) { return (await hit()) || Response.error(); }
    }));
    return;
  }
  // Other files: answer from cache instantly, refresh the cache from the network.
  e.respondWith(caches.open(CACHE).then(async cache => {
    const hit = await cache.match(req);
    const net = fetch(req).then(res => { if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone()); return res; }).catch(() => hit);
    return hit || net;
  }));
});
