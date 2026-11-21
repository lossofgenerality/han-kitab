/* Han Kitab service worker: keeps the app working offline.
   VERSION is set by tools/make_app.py from the app's content, so installed copies update by themselves.
   © Computational Classnotes · CC BY-NC-SA 4.0 */
const VERSION = 'hankitab-441165d088';
const SHELL = ['./', './index.html', './manifest.webmanifest',
  './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png', './favicon-32.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;                       // HanKitabKernel calls are POSTs: never cached
  const url = new URL(req.url);
  if (req.mode === 'navigate') {                           // the app page: network first, cache when offline
    e.respondWith(fetch(req).then((res) => { const copy = res.clone(); caches.open(VERSION).then((c) => c.put(req, copy)); return res; })
      .catch(() => caches.match(req).then((hit) => hit || caches.match('./index.html'))));
    return;
  }
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith(caches.open(VERSION).then((c) => c.match(req).then((hit) => {
      const net = fetch(req).then((res) => { c.put(req, res.clone()); return res; }).catch(() => hit);
      return hit || net;
    })));
    return;
  }
  if (url.origin === self.location.origin) {
    // PDFs and original scans: straight from the network (too large to keep offline).
    if (/\.pdf$/i.test(url.pathname)) return;
    // Pages, plates, text files: cache after the first view, so what you have read works offline.
    e.respondWith(caches.open(VERSION).then((c) => c.match(req).then((hit) => hit || fetch(req).then((res) => {
      if (res.ok) c.put(req, res.clone()); return res; }))));
  }
});
