/**
 * ISBMS Multi-Language (i18n) & Localization Engine
 * Supported Languages: English (en), Hindi (hi), Marathi (mr)
 */

const translations = {
    en: {
        // Navigation Bar
        nav_brand_title: "ISBMS",
        nav_brand_sub: "Business Management System",
        nav_pos: "POS Terminal",
        nav_inventory: "Stock Inventory & Excel Upload",
        nav_khata: "Digital Khata (Udhaari)",
        nav_analytics: "Capital Analytics",
        nav_admin: "Admin Portal",
        nav_ai_tutorial: "How to Use (AI Video)",
        nav_store_header: "Logged-in Store",
        nav_logout: "Logout Store",
        nav_online: "ONLINE",
        nav_offline: "OFFLINE",

        // Language Selector
        lang_english: "English 🇬🇧",
        lang_hindi: "हिंदी (Hindi) 🇮🇳",
        lang_marathi: "मराठी (Marathi) 🇮🇳",

        // AI Tutorial Modal
        tutorial_title: "🎥 How to Use ISBMS - AI Video Tutorial Guide",
        tutorial_subtitle: "Learn how to manage billing, inventory, digital khata, and analytics in 1 minute.",
        tutorial_tab_intro: "1. Intro & Setup",
        tutorial_tab_pos: "2. Fast POS Billing",
        tutorial_tab_inventory: "3. Stock & Excel Upload",
        tutorial_tab_khata: "4. Digital Udhaar Khata",
        tutorial_tab_analytics: "5. Profit & Risk Analytics",
        tutorial_btn_play: "Play Voice Guide",
        tutorial_btn_pause: "Pause Audio",
        tutorial_btn_prev: "Previous Step",
        tutorial_btn_next: "Next Step",
        tutorial_voice_on: "Voice Narration: ON",
        tutorial_voice_off: "Voice Narration: OFF",

        // POS Page
        pos_search_placeholder: "Scan Barcode or Search Product by Name (Press F2 to focus)...",
        pos_cart_title: "Current Invoice Cart",
        pos_clear_cart: "Clear Cart",
        pos_col_item: "Item Name",
        pos_col_batch: "Batch / Exp",
        pos_col_price: "Price (₹)",
        pos_col_qty: "Qty",
        pos_col_total: "Total (₹)",
        pos_empty_cart: "Scan a barcode or search products using input above (F2)",
        pos_customer_info: "Customer Information",
        pos_cust_phone: "Phone Number (Required for Khata)",
        pos_cust_name: "Customer Name (Walk-in)",
        pos_payment_mode: "Payment Mode",
        pos_pay_cash: "Cash Payment",
        pos_pay_upi: "UPI QR Code",
        pos_pay_khata: "Add to Khata (Udhaari)",
        pos_total_payable: "Total Amount Payable",
        pos_btn_checkout: "Complete Billing & Print Thermal Receipt (Ctrl+Enter)",

        // Inventory Page
        inv_title: "Inventory Stock Management",
        inv_subtitle: "Manage products, monitor stock counts, add batches manually, or bulk import via Excel/CSV.",
        inv_download_sample: "Download Sample Excel Template",
        inv_upload_excel: "Upload Excel / CSV Stock Sheet",
        inv_add_product: "Add Product Manually",
        inv_search_placeholder: "Search by Product Name or Barcode/SKU...",
        inv_col_name: "Product Name",
        inv_col_sku: "SKU / Barcode",
        inv_col_category: "Category",
        inv_col_unit: "Unit",
        inv_col_stock: "Total Stock",
        inv_col_selling: "Selling Price (₹)",
        inv_col_cost: "Cost Price (₹)",
        inv_col_batches: "Active Batches",
        inv_col_action: "Action",

        // Khata Page
        khata_title: "Digital Khata (Udhaari) Ledger",
        khata_subtitle: "Track customer pending balances and collect payments faster via 1-Click WhatsApp payment reminders.",
        khata_total_outstanding: "Total Store Udhaar Outstanding",
        khata_search_placeholder: "Search customer by Name or Phone Number...",
        khata_col_cust_name: "Customer Name",
        khata_col_phone: "Phone Number",
        khata_col_balance: "Pending Udhaar (₹)",
        khata_col_whatsapp: "1-Click WhatsApp Reminder",
        khata_col_action: "Action",
        khata_btn_whatsapp: "Send WhatsApp Reminder",
        khata_btn_settle: "Settle Payment",

        // Analytics Page
        analytics_title: "Inventory Risk & Profit Margin Analytics",
        analytics_subtitle: "Proactively identify blocked inventory capital, expiring batches for FIFO clearing, and view store profit margins.",
        analytics_gross_rev: "30-Day Gross Revenue",
        analytics_gross_profit: "30-Day Gross Profit",
        analytics_profit_margin: "Profit Margin",
        analytics_dead_stock: "Dead Stock Capital Blocked",
        analytics_dead_stock_sub: "Zero sales in last 30+ days",
        analytics_expiry_risk: "Expiry Risk Capital",
        analytics_expiry_risk_sub: "Batches expiring in ≤30 days",
        analytics_dead_stock_header: "Dead-Stock Risk Analyzer (30+ Days Inactive)",
        analytics_expiring_header: "Expiring Batches Analyzer (Clear FIFO First)",

        // Common Buttons
        btn_search: "Search",
        btn_cancel: "Cancel",
        btn_save: "Save",
        btn_close: "Close"
    },
    hi: {
        // Navigation Bar
        nav_brand_title: "ISBMS",
        nav_brand_sub: "व्यापार प्रबंधन प्रणाली",
        nav_pos: "POS बिलिंग काउंटर",
        nav_inventory: "स्टॉक इन्वेंटरी और एक्सेल",
        nav_khata: "डिजिटल खाता (उधारी)",
        nav_analytics: "मुनाफा और रिपोर्ट",
        nav_admin: "एडमिन पोर्टल",
        nav_ai_tutorial: "उपयोग कैसे करें (AI वीडियो)",
        nav_store_header: "लॉग-इन स्टोर",
        nav_logout: "लॉगआउट करें",
        nav_online: "ऑनलाइन",
        nav_offline: "ऑफलाइन",

        // Language Selector
        lang_english: "English 🇬🇧",
        lang_hindi: "हिंदी (Hindi) 🇮🇳",
        lang_marathi: "मराठी (Marathi) 🇮🇳",

        // AI Tutorial Modal
        tutorial_title: "🎥 ISBMS का उपयोग कैसे करें - AI वीडियो गाइड",
        tutorial_subtitle: "केवल 1 मिनट में बिलिंग, इन्वेंटरी, डिजिटल खाता और रिपोर्ट्स चलाना सीखें।",
        tutorial_tab_intro: "1. शुरुआत और परिचय",
        tutorial_tab_pos: "2. फास्ट POS बिलिंग",
        tutorial_tab_inventory: "3. स्टॉक व एक्सेल अपलोड",
        tutorial_tab_khata: "4. डिजिटल उधार खाता",
        tutorial_tab_analytics: "5. मुनाफा और रिस्क एनालिसिस",
        tutorial_btn_play: "आवाज में सुनें",
        tutorial_btn_pause: "ऑडियो रोकें",
        tutorial_btn_prev: "पिछला स्टेप",
        tutorial_btn_next: "अगला स्टेप",
        tutorial_voice_on: "आवाज (Voice): चालू",
        tutorial_voice_off: "आवाज (Voice): बंद",

        // POS Page
        pos_search_placeholder: "बारकोड स्कैन करें या प्रोडक्ट का नाम लिखें (F2 दबाएं)...",
        pos_cart_title: "वर्तमान बिल कार्ट",
        pos_clear_cart: "कार्ट खाली करें",
        pos_col_item: "सामान / आइटम",
        pos_col_batch: "बैच / एक्सपायरी",
        pos_col_price: "कीमत (₹)",
        pos_col_qty: "मात्रा (Qty)",
        pos_col_total: "कुल (₹)",
        pos_empty_cart: "ऊपर बारकोड स्कैन करें या प्रोडक्ट सर्च करें (F2)",
        pos_customer_info: "ग्राहक विवरण",
        pos_cust_phone: "मोबाइल नंबर (उधारी के लिए जरूरी)",
        pos_cust_name: "ग्राहक का नाम",
        pos_payment_mode: "भुगतान का तरीका",
        pos_pay_cash: "नकद (Cash)",
        pos_pay_upi: "UPI क्यूआर कोड (GPay/PhonePe)",
        pos_pay_khata: "खाते में जोड़ें (उधारी)",
        pos_total_payable: "कुल भुगतान राशि",
        pos_btn_checkout: "बिल पूरा करें और रसीद प्रिंट करें (Ctrl+Enter)",

        // Inventory Page
        inv_title: "स्टॉक इन्वेंटरी प्रबंधन",
        inv_subtitle: "प्रोडक्ट्स प्रबंधित करें, स्टॉक चेक करें, नए बैच जोड़ें या एक्सेल से एक साथ अपलोड करें।",
        inv_download_sample: "सैंपल एक्सेल शीट डाउनलोड करें",
        inv_upload_excel: "एक्सेल / CSV फाइल अपलोड करें",
        inv_add_product: "नया प्रोडक्ट जोड़ें",
        inv_search_placeholder: "प्रोडक्ट का नाम या बारकोड/SKU से खोजें...",
        inv_col_name: "प्रोडक्ट का नाम",
        inv_col_sku: "बारकोड / SKU",
        inv_col_category: "श्रेणी (Category)",
        inv_col_unit: "इकाई (Unit)",
        inv_col_stock: "कुल स्टॉक",
        inv_col_selling: "बिक्री मूल्य (₹)",
        inv_col_cost: "खरीद मूल्य (₹)",
        inv_col_batches: "एक्टिव बैच",
        inv_col_action: "कार्य",

        // Khata Page
        khata_title: "डिजिटल खाता (उधारी) लेजर",
        khata_subtitle: "ग्राहकों की बकाया राशि ट्रैक करें और व्हाट्सएप पर 1-क्लिक पेमेंट रिमाइंडर भेजकर तेजी से उधारी वसूलें।",
        khata_total_outstanding: "दुकान की कुल उधारी (Pending Balance)",
        khata_search_placeholder: "नाम या मोबाइल नंबर से ग्राहक खोजें...",
        khata_col_cust_name: "ग्राहक का नाम",
        khata_col_phone: "मोबाइल नंबर",
        khata_col_balance: "बाकी उधारी (₹)",
        khata_col_whatsapp: "1-क्लिक व्हाट्सएप रिमाइंडर",
        khata_col_action: "कार्य",
        khata_btn_whatsapp: "व्हाट्सएप रिमाइंडर भेजें",
        khata_btn_settle: "हिसाब चुकता करें",

        // Analytics Page
        analytics_title: "मुनाफा और इन्वेंटरी रिस्क एनालिसिस",
        analytics_subtitle: "अटका हुआ पैसा, एक्सपायरी वाला सामान और दुकान का शुद्ध मुनाफा तुरंत देखें।",
        analytics_gross_rev: "30-दिनों की कुल बिक्री",
        analytics_gross_profit: "30-दिनों का मुनाफा",
        analytics_profit_margin: "मुनाफा मार्जिन",
        analytics_dead_stock: "अटका हुआ सामान (Dead Stock)",
        analytics_dead_stock_sub: "पिछले 30+ दिनों से शून्य बिक्री",
        analytics_expiry_risk: "एक्सपायरी रिस्क राशि",
        analytics_expiry_risk_sub: "30 दिनों में एक्सपायर होने वाला स्टॉक",
        analytics_dead_stock_header: "अटके हुए सामान का विश्लेषण (30+ दिन पुराना)",
        analytics_expiring_header: "जल्द एक्सपायर होने वाले बैच (पहले बेचें)",

        // Common Buttons
        btn_search: "खोजें",
        btn_cancel: "रद्द करें",
        btn_save: "सुरक्षित करें",
        btn_close: "बंद करें"
    },
    mr: {
        // Navigation Bar
        nav_brand_title: "ISBMS",
        nav_brand_sub: "व्यवसाय व्यवस्थापन प्रणाली",
        nav_pos: "POS बिलिंग काउंटर",
        nav_inventory: "स्टॉक इन्व्हेंटरी आणि एक्सेल",
        nav_khata: "डिजिटल खाते (उधारी)",
        nav_analytics: "नफा आणि रिपोर्ट",
        nav_admin: "ॲडमिन पोर्टल",
        nav_ai_tutorial: "वापर कसा करावा (AI व्हिडिओ)",
        nav_store_header: "लॉग-इन दुकान",
        nav_logout: "लॉगआउट करा",
        nav_online: "ऑनलाइन",
        nav_offline: "ऑफलाइन",

        // Language Selector
        lang_english: "English 🇬🇧",
        lang_hindi: "हिंदी (Hindi) 🇮🇳",
        lang_marathi: "मराठी (Marathi) 🇮🇳",

        // AI Tutorial Modal
        tutorial_title: "🎥 ISBMS चा वापर कसा करावा - AI व्हिडिओ मार्गदर्शक",
        tutorial_subtitle: "फक्त १ मिनिटात बिलिंग, इन्व्हेंटरी, डिजिटल खाते आणि रिपोर्ट्स चालवायला शिका.",
        tutorial_tab_intro: "1. सुरुवात व परिचय",
        tutorial_tab_pos: "2. जलद POS बिलिंग",
        tutorial_tab_inventory: "3. स्टॉक व एक्सेल अपलोड",
        tutorial_tab_khata: "4. डिजिटल उधार खाते",
        tutorial_tab_analytics: "5. नफा व रिस्क ॲनालिटिक्स",
        tutorial_btn_play: "आवाजात ऐका",
        tutorial_btn_pause: "ऑडिओ थांबवा",
        tutorial_btn_prev: "मागील स्टेप",
        tutorial_btn_next: "पुढील स्टेप",
        tutorial_voice_on: "आवाज (Voice): चालू",
        tutorial_voice_off: "आवाज (Voice): बंद",

        // POS Page
        pos_search_placeholder: "बारकोड स्कॅन करा किंवा वस्तूचे नाव टाका (F2 दाबा)...",
        pos_cart_title: "चालू बिल कार्ट",
        pos_clear_cart: "कार्ट रिकामे करा",
        pos_col_item: "वस्तूचे नाव",
        pos_col_batch: "बॅच / एक्सपायरी",
        pos_col_price: "किंमत (₹)",
        pos_col_qty: "प्रमाण (Qty)",
        pos_col_total: "एकूण (₹)",
        pos_empty_cart: "वर बारकोड स्कॅन करा किंवा प्रॉडक्ट शोधा (F2)",
        pos_customer_info: "ग्राहकाची माहिती",
        pos_cust_phone: "मोबाईल नंबर (उधारीसाठी आवश्यक)",
        pos_cust_name: "ग्राहकाचे नाव",
        pos_payment_mode: "पैसे देण्याचा प्रकार",
        pos_pay_cash: "रोख (Cash)",
        pos_pay_upi: "UPI क्यूआर कोड (GPay/PhonePe)",
        pos_pay_khata: "खात्यात टाका (उधारी)",
        pos_total_payable: "एकूण देय रक्कम",
        pos_btn_checkout: "बिल पूर्ण करा व पावती प्रिंट करा (Ctrl+Enter)",

        // Inventory Page
        inv_title: "स्टॉक इन्व्हेंटरी व्यवस्थापन",
        inv_subtitle: "प्रॉडक्ट्स व्यवस्थापित करा, स्टॉक तपासा, नवीन बॅच जोडा किंवा एक्सेल वरून एकदम अपलोड करा.",
        inv_download_sample: "सैंपल एक्सेल शीट डाउनलोड करा",
        inv_upload_excel: "एक्सेल / CSV फाईल अपलोड करा",
        inv_add_product: "नवीन प्रॉडक्ट जोडा",
        inv_search_placeholder: "प्रॉडक्टचे नाव किंवा बारकोड/SKU ने शोधा...",
        inv_col_name: "प्रॉडक्टचे नाव",
        inv_col_sku: "बारकोड / SKU",
        inv_col_category: "वर्ग (Category)",
        inv_col_unit: "एकक (Unit)",
        inv_col_stock: "एकूण स्टॉक",
        inv_col_selling: "विक्री किंमत (₹)",
        inv_col_cost: "खरेदी किंमत (₹)",
        inv_col_batches: "ॲक्टिव्ह बॅच",
        inv_col_action: "कृती",

        // Khata Page
        khata_title: "डिजिटल खाते (उधारी) नोंदवही",
        khata_subtitle: "ग्राहकांची बाकी उधारी ट्रॅक करा आणि व्हॉट्सॲपवर १-क्लिक पेमेंट रिमाइंडर पाठवून जलद वसुली करा.",
        khata_total_outstanding: "दुकानाची एकूण उधारी (Pending Balance)",
        khata_search_placeholder: "नाव किंवा मोबाईल नंबरने ग्राहक शोधा...",
        khata_col_cust_name: "ग्राहकाचे नाव",
        khata_col_phone: "मोबाईल नंबर",
        khata_col_balance: "बाकी उधारी (₹)",
        khata_col_whatsapp: "१-क्लिक व्हॉट्सॲप रिमाइंडर",
        khata_col_action: "कृती",
        khata_btn_whatsapp: "व्हॉट्सॲप रिमाइंडर पाठवा",
        khata_btn_settle: "हिशोब पूर्ण करा",

        // Analytics Page
        analytics_title: "नफा आणि इन्व्हेंटरी रिस्क ॲनालिटिक्स",
        analytics_subtitle: "अडकलेला पैसा, एक्सपायरी माल आणि दुकानाचा निव्वळ नफा त्वरित पहा.",
        analytics_gross_rev: "३० दिवसांची एकूण विक्री",
        analytics_gross_profit: "३० दिवसांचा निव्वळ नफा",
        analytics_profit_margin: "नफा मार्जिन",
        analytics_dead_stock: "अडकलेला माल (Dead Stock)",
        analytics_dead_stock_sub: "गेल्या ३०+ दिवसांत शून्य विक्री",
        analytics_expiry_risk: "एक्सपायरी रिस्क रक्कम",
        analytics_expiry_risk_sub: "३० दिवसांत एक्सपायर होणारा स्टॉक",
        analytics_dead_stock_header: "अडकलेल्या मालाचे विश्लेषण (३०+ दिवस जुना)",
        analytics_expiring_header: "लवकर एक्सपायर होणाऱ्या बॅच (आधी विका)",

        // Common Buttons
        btn_search: "शोधा",
        btn_cancel: "रद्द करा",
        btn_save: "साठवा",
        btn_close: "बंद करा"
    }
};

/**
 * Get current language setting (default: 'en')
 */
function getCurrentLang() {
    return localStorage.getItem('isbms_lang') || 'en';
}

/**
 * Switch Application Language
 */
function setLanguage(lang) {
    if (!translations[lang]) lang = 'en';
    localStorage.setItem('isbms_lang', lang);
    document.documentElement.lang = lang;

    // Update active state in UI selectors if present
    document.querySelectorAll('.lang-select-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    const dict = translations[lang];

    // Update text content for elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            el.innerText = dict[key];
        }
    });

    // Update placeholders for inputs with data-i18n-placeholder
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (dict[key]) {
            el.setAttribute('placeholder', dict[key]);
        }
    });

    // Trigger AI tutorial language sync if open
    if (typeof window.syncTutorialLanguage === 'function') {
        window.syncTutorialLanguage(lang);
    }
}

/**
 * Translation helper function
 */
function t(key) {
    const lang = getCurrentLang();
    return (translations[lang] && translations[lang][key]) || (translations['en'] && translations['en'][key]) || key;
}

// Auto Initialize Language on Page Load
document.addEventListener('DOMContentLoaded', () => {
    setLanguage(getCurrentLang());
});
