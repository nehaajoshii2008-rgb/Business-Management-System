/**
 * ISBMS POS Offline Sync Engine (USP 1)
 * Leverages IndexedDB for zero-downtime offline queueing when cloud spins down or Wi-Fi drops.
 */

const DB_NAME = 'ISBMS_POS_DB';
const DB_VERSION = 1;
const STORE_NAME = 'offline_invoices';

let db = null;

// Initialize IndexedDB
function initOfflineDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onupgradeneeded = (event) => {
            const dbInstance = event.target.result;
            if (!dbInstance.objectStoreNames.contains(STORE_NAME)) {
                dbInstance.createObjectStore(STORE_NAME, { keyPath: 'client_invoice_id' });
            }
        };

        request.onsuccess = (event) => {
            db = event.target.result;
            console.log('IndexedDB ISBMS_POS_DB initialized successfully.');
            updateSyncStatusBadge();
            syncOfflineInvoicesToServer();
            resolve(db);
        };

        request.onerror = (event) => {
            console.error('IndexedDB Initialization error:', event.target.error);
            reject(event.target.error);
        };
    });
}

// Save Invoice payload to local queue when server is unreachable or offline
async function queueInvoiceOffline(invoiceData) {
    if (!db) await initOfflineDB();

    return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readwrite');
        const store = tx.objectStore(STORE_NAME);

        invoiceData.queued_at = new Date().toISOString();
        invoiceData.synced_from_offline = true;

        const request = store.put(invoiceData);

        request.onsuccess = () => {
            console.log('Invoice saved to IndexedDB offline queue:', invoiceData.client_invoice_id);
            updateSyncStatusBadge();
            resolve(true);
        };

        request.onerror = (event) => {
            console.error('Failed to queue invoice in IndexedDB:', event.target.error);
            reject(event.target.error);
        };
    });
}

// Fetch all queued offline invoices
async function getQueuedInvoices() {
    if (!db) await initOfflineDB();

    return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readonly');
        const store = tx.objectStore(STORE_NAME);
        const request = store.getAll();

        request.onsuccess = () => resolve(request.result || []);
        request.onerror = (event) => reject(event.target.error);
    });
}

// Remove an invoice from the local queue after successful server sync
async function removeQueuedInvoice(client_invoice_id) {
    if (!db) await initOfflineDB();

    return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readwrite');
        const store = tx.objectStore(STORE_NAME);
        const request = store.delete(client_invoice_id);

        request.onsuccess = () => {
            updateSyncStatusBadge();
            resolve(true);
        };
        request.onerror = (event) => reject(event.target.error);
    });
}

// Sync engine: Flushes queued transactions to server once online & awake
async function syncOfflineInvoicesToServer() {
    if (!navigator.onLine) {
        updateSyncStatusBadge();
        return;
    }

    try {
        const queuedInvoices = await getQueuedInvoices();
        if (queuedInvoices.length === 0) {
            updateSyncStatusBadge();
            return;
        }

        showToast(`Syncing ${queuedInvoices.length} offline bill(s) to cloud server...`, 'info');

        for (const invoice of queuedInvoices) {
            try {
                const response = await fetch('/api/pos/checkout/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(invoice)
                });

                if (response.ok) {
                    const resData = await response.json();
                    console.log('Successfully synced offline bill:', resData.invoice_number);
                    await removeQueuedInvoice(invoice.client_invoice_id);
                } else if (response.status >= 500) {
                    // Server might still be waking up from sleep, break loop and retry later
                    console.warn('Server waking up or temporary error. Retrying sync shortly.');
                    break;
                }
            } catch (err) {
                console.warn('Network issue during sync attempt:', err);
                break;
            }
        }

        const remaining = await getQueuedInvoices();
        if (remaining.length === 0) {
            showToast('All offline transactions successfully synced!', 'success');
        }
        updateSyncStatusBadge();
    } catch (err) {
        console.error('Error running offline sync engine:', err);
    }
}

// Update network status indicator badge on POS header
async function updateSyncStatusBadge() {
    const badgeEl = document.getElementById('sync-status-badge');
    if (!badgeEl) return;

    const queued = await getQueuedInvoices();
    const isOnline = navigator.onLine;

    if (!isOnline) {
        badgeEl.className = 'badge bg-warning text-dark';
        badgeEl.innerHTML = `<i class="bi bi-wifi-off me-1"></i> OFFLINE (${queued.length} Queued)`;
    } else if (queued.length > 0) {
        badgeEl.className = 'badge bg-info text-dark';
        badgeEl.innerHTML = `<i class="bi bi-arrow-repeat me-1"></i> SYNCING (${queued.length} Queued)`;
    } else {
        badgeEl.className = 'badge bg-success';
        badgeEl.innerHTML = `<i class="bi bi-wifi me-1"></i> ONLINE`;
    }
}

// Utility: Read Django CSRF Token Cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Utility UUID generator for client side idempotency
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3f | 0x80);
        return v.toString(16);
    });
}

// Event Listeners for network changes
window.addEventListener('online', () => {
    console.log('Connection restored. Triggering auto-sync...');
    syncOfflineInvoicesToServer();
});

window.addEventListener('offline', () => {
    updateSyncStatusBadge();
});

// Periodic heartbeat sync check every 20 seconds
setInterval(() => {
    syncOfflineInvoicesToServer();
}, 20000);

// Initialize DB on script load
document.addEventListener('DOMContentLoaded', () => {
    initOfflineDB();
});
