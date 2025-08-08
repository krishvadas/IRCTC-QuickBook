CLASS_CODE_MAP = {
    "Anubhuti Class (EA)": "EA", "AC First Class (1A)": "1A", "Vistadome AC (EV)": "EV",
    "Exec. Chair Car (EC)": "EC", "AC 2 Tier (2A)": "2A", "First Class (FC)": "FC",
    "AC 3 Tier (3A)": "3A", "AC 3 Economy (3E)": "3E", "Vistadome Chair Car (VC)": "VC",
    "AC Chair car (CC)": "CC", "Sleeper (SL)": "SL", "Vistadome Non AC (VS)": "VS",
    "Second Sitting (2S)": "2S", "All Classes": ""
}
QUOTA_CODE_MAP = {
    "GENERAL": "GN", "LADIES": "LD", "LOWER BERTH/SR.CITIZEN": "SS",
    "PERSON WITH DISABILITY": "HP", "DUTY PASS": "DP", "TATKAL": "TQ", "PREMIUM TATKAL": "PT"
}
CLASS_NAME_MAP = {
    'EA': 'Anubhuti Class (EA)', '1A': 'AC First Class (1A)', 'EV': 'Vistadome AC (EV)',
    'EC': 'Exec. Chair Car (EC)', '2A': 'AC 2 Tier (2A)', 'FC': 'First Class (FC)',
    '3A': 'AC 3 Tier (3A)', '3E': 'AC 3 Economy (3E)', 'VC': 'Vistadome Chair Car (VC)',
    'CC': 'AC Chair car (CC)', 'SL': 'Sleeper (SL)', 'VS': 'Vistadome Non AC (VS)',
    '2S': 'Second Sitting (2S)', '': 'All Classes'
}

AC_COACH =  ['Anubhuti Class (EA)', 'AC First Class (1A)', 'Exec. Chair Car (EC)', 'AC 2 Tier (2A)', 'AC 3 Tier (3A)', 'AC 3 Economy (3E)', 'AC Chair car (CC)', 'Vistadome AC (EV)']

selected_train_number = ''
selected_train_class = ''

selectors_to_block = [
    "#askDishaSdk",
    "#disha-image",
    "#div-gpt-ad-1695628181945-0",
    'div[id^="div-gpt-ad-"]',
    "#div-gpt-ad-9768185-0",
    "button[_ngcontent-dhi-c67][type][label][style]",
    "div.ng-tns-c19-2.ui-dialog-content.ui-widget-content",
    "div.ng-tns-c19-2.ui-dialog-mask.ui-widget-overlay.ui-dialog-visible.ui-dialog-mask-scrollblocker.ng-star-inserted[style]",
    "div.ng-tns-c19-3.ui-dialog-mask.ui-widget-overlay.ui-dialog-visible.ui-dialog-mask-scrollblocker.ng-star-inserted",
    "div.text-center.hidden-xs.footer-icons",
    "div.ui-dialog-titlebar.ui-widget-header.ui-helper-clearfix.ui-corner-top.ng-tns-c19-2.ng-star-inserted",
    "img.default-img",
    "#disha-placeholder-card",
    "#adg_cuboid_container",
    "#div-gpt-ad-4837041-0",
    "#dod",
    "#div-gpt-ad-9462678-0",
    "#google_ads_iframe_\\/37179215\\/GPT_NWEB_TRAIN_LIST_BOTTOM_1"
]

js_filter = """
(() => {
    const selectors = %s;

    function removeAll() {
        for (const selector of selectors) {
            try {
                const elements = document.querySelectorAll(selector);
                for (const el of elements) {
                    el.remove();
                }
            } catch (e) {}
        }

        // Iframes
        for (const frame of document.querySelectorAll("iframe")) {
            try {
                const doc = frame.contentDocument;
                if (doc) {
                    for (const selector of selectors) {
                        const elements = doc.querySelectorAll(selector);
                        for (const el of elements) {
                            el.remove();
                        }
                    }
                }
            } catch (e) {}
        }

        // Shadow DOM
        for (const el of document.querySelectorAll("*")) {
            if (el.shadowRoot) {
                for (const selector of selectors) {
                    try {
                        const matches = el.shadowRoot.querySelectorAll(selector);
                        for (const match of matches) {
                            match.remove();
                        }
                    } catch (e) {}
                }
            }
        }
    }

    // Initial cleanup
    removeAll();

    // MutationObserver for dynamic DOM changes
    const observer = new MutationObserver(() => {
        removeAll();
    });

    observer.observe(document, {
        childList: true,
        subtree: true
    });

    // Periodic cleanup every 2 seconds
    setInterval(removeAll, 2000);

    // Hook into fetch and XHR to clean after network activity
    const cleanAfterResponse = () => setTimeout(removeAll, 100);

    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        return originalFetch.apply(this, args).then(res => {
            cleanAfterResponse();
            return res;
        });
    };

    const originalXHR = window.XMLHttpRequest;
    window.XMLHttpRequest = class extends originalXHR {
        constructor() {
            super();
            this.addEventListener("loadend", cleanAfterResponse);
        }
    };
})();
""" % selectors_to_block

