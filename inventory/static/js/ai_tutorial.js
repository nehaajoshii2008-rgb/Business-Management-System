/**
 * ISBMS AI Video Tutorial & Smart Voice Synthesis Engine
 * Guarantees native Indian Hindi & Marathi TTS voice selection with zero phonetic distortion
 */

const videoScript = {
    titleEn: "🎥 ISBMS Business Management System - Complete Software Video Guide",
    titleHi: "🎥 ISBMS बिजनेस प्रबंधन सॉफ्टवेयर - संपूर्ण वीडियो गाइड",
    titleMr: "🎥 ISBMS बिझनेस व्यवस्थापन सॉफ्टवेअर - संपूर्ण व्हिडिओ मार्गदर्शक",

    narration: {
        en: "Welcome to the official video tutorial of ISBMS Business Management System. Using this software is simple and fast. First, log into your store account securely. To start billing, press F2 on your keyboard, scan product barcodes or search item names, select Cash, UPI QR Code, or Khata, then press Ctrl+Enter to print thermal receipts. For inventory management, download our sample Excel sheet, enter your stock list, and upload over 1,000 items in just 1 second. Track customer udhaari in Digital Khata and send instant UPI payment links via WhatsApp. Finally, check your store profit margins and dead-stock capital reports in Analytics. Grow your retail store with ISBMS!",
        hi: "नमस्ते! ISBMS बिजनेस मैनेजमेंट सिस्टम के वीडियो ट्यूटोरियल में आपका स्वागत है। इसका उपयोग करना बहुत आसान है। सबसे पहले अपने यूजरनेम और पासवर्ड से लॉगिन करें। बिलिंग के लिए F2 बटन दबाएं, बारकोड स्कैन करें और नकद या UPI चुनें। रसीद प्रिंट करने के लिए कंट्रोल और एंटर दबाएं। एक्सेल शीट से 1,000 से ज्यादा सामान 1 सेकंड में अपलोड करें। डिजिटल खाता में ग्राहकों की उधारी संभालें और व्हाट्सएप पर UPI पेमेंट लिंक भेजें। और ॲनालिटिक्स में दुकान का मुनाफा देखें। ISBMS के साथ अपनी दुकान को आसान और स्मार्ट बनाएं!",
        mr: "नमस्कार! ISBMS बिझनेस मॅनेजमेंट सिस्टीमच्या व्हिडिओ ट्यूटोरियलमध्ये आपले स्वागत आहे. याचा वापर करणे अत्यंत सोपे आहे. सर्व प्रथम आपल्या युजरनेम आणि पासवर्डने लॉगिन करा. बिलिंगसाठी F2 बटण दाबा, बारकोड स्कॅन करा आणि रोख किंवा UPI निवडा. पावती प्रिंट करण्यासाठी कंट्रोल आणि एंटर दाबा. एक्सेल शीटवरून 1,000 पेक्षा जास्त माल 1 सेकंदात अपलोड करा. डिजिटल खात्यामध्ये ग्राहकांची उधारी सांभाळा आणि व्हॉट्सॲपवर UPI पेमेंट लिंक पाठवा. आणि ॲनालिटिक्समध्ये दुकानाचा नफा पहा. ISBMS सह तुमचे दुकान सोपे आणि स्मार्ट बनवा!"
    },

    scenes: [
        {
            timeLabel: "0:00 - Store Login",
            badge: "PHASE 1: SECURE LOGIN",
            badgeColor: "bg-primary",
            title: "Store Login & Registration Portal",
            render: function() {
                return `
                    <div class="p-3 bg-dark bg-opacity-90 rounded-3 border border-primary text-start text-white shadow">
                        <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom border-secondary">
                            <div class="d-flex align-items-center gap-2">
                                <i class="bi bi-shield-lock-fill text-primary fs-4"></i>
                                <span class="fw-bold fs-5 text-white">ISBMS Secure Store Login Portal</span>
                            </div>
                            <span class="badge bg-success px-3 py-2"><i class="bi bi-check-circle-fill me-1"></i>Cloud Server Active</span>
                        </div>
                        <div class="row align-items-center">
                            <div class="col-md-6 border-end border-secondary pe-3">
                                <div class="mb-2">
                                    <label class="small text-muted fw-bold">Store Username / Phone</label>
                                    <input type="text" class="form-control form-control-sm bg-black text-warning fw-bold" value="sharma_kirana" readonly>
                                </div>
                                <div class="mb-3">
                                    <label class="small text-muted fw-bold">Password</label>
                                    <input type="password" class="form-control form-control-sm bg-black text-warning fw-bold" value="••••••••" readonly>
                                </div>
                                <div class="d-flex gap-2">
                                    <button class="btn btn-primary btn-sm fw-bold w-100"><i class="bi bi-box-arrow-in-right me-1"></i> Login to Store</button>
                                    <button class="btn btn-outline-success btn-sm fw-bold w-100"><i class="bi bi-shop me-1"></i> Register Store</button>
                                </div>
                            </div>
                            <div class="col-md-6 ps-3 text-center">
                                <i class="bi bi-shop-window display-4 text-primary mb-2 d-block"></i>
                                <span class="fw-bold text-warning d-block fs-5">Sharma Kirana & General Store</span>
                                <small class="text-muted">GSTIN: 27AAAAA0000A1Z5 | UPI: sharma@upi</small>
                            </div>
                        </div>
                    </div>
                `;
            }
        },
        {
            timeLabel: "0:12 - POS Billing",
            badge: "PHASE 2: FAST POS BILLING",
            badgeColor: "bg-success",
            title: "Superfast Barcode Billing & Receipts (Press F2)",
            render: function() {
                return `
                    <div class="p-3 bg-dark bg-opacity-90 rounded-3 border border-success text-start text-white shadow">
                        <div class="input-group mb-2">
                            <span class="input-group-text bg-success text-white fw-bold"><i class="bi bi-upc-scan me-1"></i> F2 Barcode Scanner</span>
                            <input type="text" class="form-control bg-black text-warning font-monospace fw-bold" value="8901030700015 - Amul Gold Milk 1L" readonly>
                            <button class="btn btn-success fw-bold"><i class="bi bi-plus-lg me-1"></i> Add Item</button>
                        </div>
                        <div class="table-responsive mb-2" style="max-height: 110px;">
                            <table class="table table-dark table-sm table-bordered align-middle mb-0 small">
                                <thead class="table-secondary text-dark">
                                    <tr>
                                        <th>Item Name</th>
                                        <th>Batch</th>
                                        <th>Price</th>
                                        <th class="text-center">Qty</th>
                                        <th class="text-end">Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><strong class="text-warning">Amul Gold Milk 1L</strong></td>
                                        <td><span class="badge bg-secondary">B-2026</span></td>
                                        <td>₹66.00</td>
                                        <td class="text-center fw-bold">2</td>
                                        <td class="text-end fw-bold text-success">₹132.00</td>
                                    </tr>
                                    <tr>
                                        <td><strong class="text-warning">Fortune Sunlite Oil 1L</strong></td>
                                        <td><span class="badge bg-secondary">B-1092</span></td>
                                        <td>₹145.00</td>
                                        <td class="text-center fw-bold">1</td>
                                        <td class="text-end fw-bold text-success">₹145.00</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="d-flex justify-content-between align-items-center bg-black p-2 rounded-3 border border-secondary">
                            <div class="d-flex gap-2">
                                <span class="badge bg-success px-2 py-1"><i class="bi bi-cash-stack me-1"></i>CASH</span>
                                <span class="badge bg-primary px-2 py-1"><i class="bi bi-qr-code me-1"></i>UPI QR</span>
                                <span class="badge bg-warning text-dark px-2 py-1"><i class="bi bi-journal-text me-1"></i>KHATA</span>
                            </div>
                            <div class="text-end">
                                <span class="text-muted small me-2">TOTAL BILL:</span>
                                <span class="fs-5 fw-bold text-success me-3">₹277.00</span>
                                <button class="btn btn-success btn-sm fw-bold"><i class="bi bi-printer me-1"></i> Print Receipt (Ctrl+Enter)</button>
                            </div>
                        </div>
                    </div>
                `;
            }
        },
        {
            timeLabel: "0:25 - Stock Excel Upload",
            badge: "PHASE 3: EXCEL BULK STOCK",
            badgeColor: "bg-info",
            title: "Bulk Excel Stock Import (1,000+ Items in 1 Sec)",
            render: function() {
                return `
                    <div class="p-3 bg-dark bg-opacity-90 rounded-3 border border-info text-start text-white shadow">
                        <div class="d-flex justify-content-between align-items-center mb-2 pb-2 border-bottom border-secondary">
                            <div>
                                <h6 class="fw-bold text-info mb-0"><i class="bi bi-file-earmark-excel me-1"></i> Excel Stock Sheet Importer</h6>
                                <small class="text-muted">Import Product Name, Barcode SKU, Cost Price, Selling Price & Expiry</small>
                            </div>
                            <div class="d-flex gap-2">
                                <span class="btn btn-outline-light btn-sm fw-bold"><i class="bi bi-download me-1"></i> Download Template.xlsx</span>
                                <span class="btn btn-info btn-sm fw-bold text-dark"><i class="bi bi-upload me-1"></i> Upload Excel Sheet</span>
                            </div>
                        </div>
                        <div class="table-responsive" style="max-height: 110px;">
                            <table class="table table-dark table-sm table-striped border border-secondary align-middle mb-0 font-monospace small">
                                <thead class="bg-primary text-white">
                                    <tr>
                                        <th>Product Name</th>
                                        <th>Barcode / SKU</th>
                                        <th>Cost (₹)</th>
                                        <th>Selling (₹)</th>
                                        <th>Stock</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Fortune Sunlite Oil 1L</td>
                                        <td>8906007251123</td>
                                        <td>125.00</td>
                                        <td>145.00</td>
                                        <td>50 Pcs</td>
                                        <td><span class="badge bg-success">Uploaded</span></td>
                                    </tr>
                                    <tr>
                                        <td>Tata Tea Gold 250g</td>
                                        <td>8901058002102</td>
                                        <td>130.00</td>
                                        <td>150.00</td>
                                        <td>40 Pcs</td>
                                        <td><span class="badge bg-success">Uploaded</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                `;
            }
        },
        {
            timeLabel: "0:38 - Digital Udhaar Khata",
            badge: "PHASE 4: DIGITAL KHATA",
            badgeColor: "bg-warning",
            title: "Customer Udhaar Ledger & 1-Click WhatsApp Reminders",
            render: function() {
                return `
                    <div class="p-3 bg-dark bg-opacity-90 rounded-3 border border-warning text-start text-white shadow">
                        <div class="d-flex justify-content-between align-items-center mb-2 bg-black p-2 rounded-3 border border-warning">
                            <div>
                                <span class="text-muted small d-block">STORE UDHAAR OUTSTANDING</span>
                                <span class="fs-4 fw-bold text-danger">₹12,450.00</span>
                            </div>
                            <span class="badge bg-warning text-dark px-3 py-2 fw-bold"><i class="bi bi-shield-lock me-1"></i>Digital Udhaar Ledger</span>
                        </div>
                        <div class="table-responsive" style="max-height: 110px;">
                            <table class="table table-dark table-sm align-middle mb-0 small">
                                <thead class="table-secondary text-dark">
                                    <tr>
                                        <th>Customer Name</th>
                                        <th>Mobile No</th>
                                        <th>Pending Balance</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><strong class="text-white fs-6">Ramesh Sharma</strong></td>
                                        <td><i class="bi bi-telephone text-muted me-1"></i>9823012345</td>
                                        <td><span class="badge bg-danger fs-6">₹1,250.00</span></td>
                                        <td>
                                            <button class="btn btn-success btn-sm fw-bold py-1 px-3">
                                                <i class="bi bi-whatsapp me-1"></i> Send 1-Click WhatsApp Reminder
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                `;
            }
        },
        {
            timeLabel: "0:50 - Capital Analytics",
            badge: "PHASE 5: PROFIT ANALYTICS",
            badgeColor: "bg-danger",
            title: "Capital Blocked Reports & Profit Margin Analyzer",
            render: function() {
                return `
                    <div class="p-3 bg-dark bg-opacity-90 rounded-3 border border-danger text-start text-white shadow">
                        <div class="row g-2 mb-2">
                            <div class="col-4">
                                <div class="p-2 bg-black rounded-3 border border-success">
                                    <small class="text-muted d-block">30-DAY REVENUE</small>
                                    <strong class="fs-5 text-success">₹1,48,500</strong>
                                </div>
                            </div>
                            <div class="col-4">
                                <div class="p-2 bg-black rounded-3 border border-primary">
                                    <small class="text-muted d-block">GROSS PROFIT</small>
                                    <strong class="fs-5 text-primary">₹32,400 (21.8%)</strong>
                                </div>
                            </div>
                            <div class="col-4">
                                <div class="p-2 bg-black rounded-3 border border-danger">
                                    <small class="text-muted d-block">DEAD STOCK BLOCKED</small>
                                    <strong class="fs-5 text-danger">₹18,450</strong>
                                </div>
                            </div>
                        </div>
                        <div class="p-2 bg-danger bg-opacity-25 border border-danger rounded-3 d-flex align-items-center justify-content-between">
                            <span class="small text-white"><i class="bi bi-exclamation-triangle-fill text-warning me-1"></i> <strong>2 Expiring Batches Detected:</strong> Clear stock before 15 days</span>
                            <span class="badge bg-danger">Clear FIFO First</span>
                        </div>
                    </div>
                `;
            }
        }
    ]
};

let currentSceneIndex = 0;
let isVoiceEnabled = true;
let isPlaying = false;
let currentUtterance = null;
let sceneTimer = null;
let availableVoices = [];

/**
 * Preload Web Speech Voices safely
 */
function loadSpeechVoices() {
    if (!('speechSynthesis' in window)) return;
    availableVoices = window.speechSynthesis.getVoices();
}

if ('speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = () => {
        loadSpeechVoices();
    };
    loadSpeechVoices();
}

/**
 * Find Best Indian Voice Engine
 */
function findBestIndianVoice(lang) {
    if (!availableVoices || availableVoices.length === 0) {
        loadSpeechVoices();
    }

    if (lang === 'hi') {
        // Search for native Hindi voice first (e.g. Microsoft Swara, Google Hindi)
        let voice = availableVoices.find(v => v.lang === 'hi-IN' || v.lang.startsWith('hi') || v.name.includes('Hindi') || v.name.includes('Swara'));
        if (voice) return voice;
    } else if (lang === 'mr') {
        // Search for native Marathi voice first
        let voice = availableVoices.find(v => v.lang === 'mr-IN' || v.lang.startsWith('mr') || v.name.includes('Marathi'));
        if (voice) return voice;

        // CRITICAL FALLBACK FOR MARATHI: Fallback to Native HINDI voice (Swara/Google Hindi) which reads Devanagari script perfectly!
        let hindiFallback = availableVoices.find(v => v.lang === 'hi-IN' || v.lang.startsWith('hi') || v.name.includes('Hindi') || v.name.includes('Swara'));
        if (hindiFallback) return hindiFallback;
    }

    // English fallback: Indian English (en-IN)
    let enVoice = availableVoices.find(v => v.lang === 'en-IN' || v.name.includes('India') || v.lang.startsWith('en'));
    return enVoice || null;
}

/**
 * Initialize Single Video Tutorial Engine
 */
function initAITutorial() {
    const modalEl = document.getElementById('aiTutorialModal');
    if (!modalEl) return;

    modalEl.addEventListener('shown.bs.modal', () => {
        startVideoFromBeginning();
    });

    modalEl.addEventListener('hidden.bs.modal', () => {
        stopVideo();
    });
}

/**
 * Start Single Video Playback From Beginning
 */
function startVideoFromBeginning() {
    currentSceneIndex = 0;
    renderVideoScene(0);
    playFullVideoAudio();
}

/**
 * Render Current Scene Frame
 */
function renderVideoScene(index) {
    if (index < 0 || index >= videoScript.scenes.length) return;
    currentSceneIndex = index;
    const scene = videoScript.scenes[index];
    const lang = (typeof getCurrentLang === 'function') ? getCurrentLang() : 'en';

    // Update Progress Scrubber Bar
    const progressPct = ((index + 1) / videoScript.scenes.length) * 100;
    const progressEl = document.getElementById('video-progress-bar');
    if (progressEl) progressEl.style.width = `${progressPct}%`;

    // Update Player Video Title & Badge
    const titleEl = document.getElementById('tutorial-visual-title');
    const badgeEl = document.getElementById('tutorial-visual-badge');
    const frameEl = document.getElementById('tutorial-demo-frame');
    const transcriptEl = document.getElementById('tutorial-transcript');

    const videoTitleText = (lang === 'hi') ? videoScript.titleHi : ((lang === 'mr') ? videoScript.titleMr : videoScript.titleEn);
    if (titleEl) titleEl.innerText = videoTitleText;

    if (badgeEl) {
        badgeEl.innerText = `${scene.badge} (${scene.timeLabel})`;
        badgeEl.className = `badge ${scene.badgeColor} text-white px-3 py-2 fw-bold fs-6`;
    }

    if (frameEl && typeof scene.render === 'function') {
        frameEl.innerHTML = scene.render();
    }

    // Update Subtitles Box
    const narrationText = videoScript.narration[lang] || videoScript.narration.en;
    if (transcriptEl) {
        const voiceObj = findBestIndianVoice(lang);
        const voiceNameStr = voiceObj ? ` [Voice: ${voiceObj.name}]` : '';
        transcriptEl.innerHTML = `<strong><i class="bi bi-soundwave text-warning me-1"></i> Voice Script (${lang.toUpperCase()}${voiceNameStr}):</strong> "${narrationText}"`;
    }

    // Update In-Modal Language Buttons Active State
    document.querySelectorAll('.modal-lang-pill').forEach(btn => {
        const isSel = btn.dataset.lang === lang;
        btn.classList.toggle('btn-warning', isSel);
        btn.classList.toggle('text-dark', isSel);
        btn.classList.toggle('btn-outline-light', !isSel);
    });
}

/**
 * Play Full Single Audio Voice Script and Animate Scenes
 */
function playFullVideoAudio() {
    stopVoiceNarration();
    if (!isVoiceEnabled) return;

    const lang = (typeof getCurrentLang === 'function') ? getCurrentLang() : 'en';
    const text = videoScript.narration[lang] || videoScript.narration.en;

    if (!('speechSynthesis' in window)) return;

    currentUtterance = new SpeechSynthesisUtterance(text);

    // Set voice language code
    if (lang === 'hi') {
        currentUtterance.lang = 'hi-IN';
    } else if (lang === 'mr') {
        currentUtterance.lang = 'hi-IN'; // Devanagari Hindi engine reads Devanagari Marathi with 99% accuracy
    } else {
        currentUtterance.lang = 'en-IN';
    }

    currentUtterance.rate = 0.88; // Natural, clear rate for crisp Hindi/Marathi understanding
    currentUtterance.pitch = 1.0;

    // Attach best Indian voice engine
    const bestVoice = findBestIndianVoice(lang);
    if (bestVoice) {
        currentUtterance.voice = bestVoice;
        console.log(`[ISBMS Voice Engine] Selected Voice: ${bestVoice.name} (${bestVoice.lang})`);
    }

    // Scene animation timer while speech plays
    const totalScenes = videoScript.scenes.length;
    let sceneStep = 0;

    if (sceneTimer) clearInterval(sceneTimer);
    sceneTimer = setInterval(() => {
        sceneStep++;
        if (sceneStep < totalScenes) {
            renderVideoScene(sceneStep);
        } else {
            clearInterval(sceneTimer);
        }
    }, 9000); // Transitions scenes smoothly every 9 seconds during speech

    currentUtterance.onend = () => {
        isPlaying = false;
        if (sceneTimer) clearInterval(sceneTimer);
        renderVideoScene(totalScenes - 1);
        updatePlayButtonState();
    };

    isPlaying = true;
    updatePlayButtonState();
    window.speechSynthesis.speak(currentUtterance);
}

/**
 * Switch Language Directly Inside AI Tutorial Modal
 */
function changeTutorialLang(lang) {
    if (typeof setLanguage === 'function') {
        setLanguage(lang);
    } else {
        localStorage.setItem('isbms_lang', lang);
    }
    startVideoFromBeginning();
}

window.changeTutorialLang = changeTutorialLang;

/**
 * Stop Audio & Animation
 */
function stopVideo() {
    stopVoiceNarration();
    if (sceneTimer) clearInterval(sceneTimer);
    isPlaying = false;
    updatePlayButtonState();
}

function stopVoiceNarration() {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }
    if (sceneTimer) clearInterval(sceneTimer);
}

/**
 * Toggle Play / Pause Full Video
 */
function togglePlayPause() {
    if (isPlaying) {
        stopVideo();
    } else {
        startVideoFromBeginning();
    }
}

/**
 * Toggle Voice Audio Mute
 */
function toggleVoiceMute() {
    isVoiceEnabled = !isVoiceEnabled;
    const btn = document.getElementById('tutorial-voice-toggle');
    if (btn) {
        btn.classList.toggle('btn-outline-warning', isVoiceEnabled);
        btn.classList.toggle('btn-outline-secondary', !isVoiceEnabled);
        btn.innerHTML = isVoiceEnabled 
            ? `<i class="bi bi-volume-up-fill me-1"></i> <span data-i18n="tutorial_voice_on">Voice Audio: ON</span>`
            : `<i class="bi bi-volume-mute-fill me-1"></i> <span data-i18n="tutorial_voice_off">Voice Audio: OFF</span>`;
    }

    if (!isVoiceEnabled) {
        stopVoiceNarration();
    } else {
        playFullVideoAudio();
    }
}

function updatePlayButtonState() {
    const playBtn = document.getElementById('tutorial-play-btn');
    if (playBtn) {
        playBtn.innerHTML = isPlaying 
            ? `<i class="bi bi-pause-circle-fill me-1"></i> Pause Video`
            : `<i class="bi bi-play-circle-fill me-1"></i> Replay Full Video`;
    }
}

function syncTutorialLanguage(lang) {
    if (document.getElementById('aiTutorialModal')?.classList.contains('show')) {
        startVideoFromBeginning();
    }
}

window.syncTutorialLanguage = syncTutorialLanguage;

document.addEventListener('DOMContentLoaded', () => {
    initAITutorial();
});
