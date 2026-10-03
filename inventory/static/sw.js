const CACHE_NAME = 'isbms-pwa-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/static/images/bms_icon.svg',
  '/static/images/bms_logo.svg',
  '/static/images/bms_logo.png',
  '/static/js/i18n.js',
  '/static/js/ai_tutorial.js',
  '/static/js/offline_sync.js',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ISBMS ServiceWorker] Pre-caching static app shell');
      return cache.addAll(ASSETS_TO_CACHE).catch(err => console.warn('Cache add warning:', err));
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[ISBMS ServiceWorker] Removing old cache:', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Network first strategy with offline fallback
  if (event.request.method === 'GET') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Cache copy of response if successful
          if (response.status === 200 && event.request.url.startsWith('http')) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          // If offline, return from cache
          return caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
              return cachedResponse;
            }
            if (event.request.headers.get('accept').includes('text/html')) {
              return caches.match('/');
            }
          });
        })
    );
  }
});
