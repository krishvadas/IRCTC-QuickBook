import os

LINUX_CHROME_PATH = "/usr/bin/google-chrome"
WINDOWS_CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = os.getcwd() + "/.chrome/user_profile"
DEBUG_URL = "http://localhost:9222"

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

CONFIG_TEMPLATE = { "username": "username", "password": "password", "upi_id": "your_upi_id", "saved_passengers": [], "source": "MGR CHENNAI CTL - MAS (CHENNAI)", "destination": "MORAPPUR - MAP", "coach": "Sleeper (SL)", "quota": "GENERAL", "date": "", "train_number": "" }

CLEANED_STATION_CODES = [
  {
    "sc": "NDLS",
    "en": "NEW DELHI",
    "ec": "NEW DELHI",
    "se": "DELHI",
    "tg": "NOIDA"
  },
  {
    "sc": "MAS",
    "en": "MGR CHENNAI CTL",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "HWH",
    "en": "HOWRAH JN",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SC",
    "en": "SECUNDERABAD JN",
    "ec": "SECUNDERABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "PUNE",
    "en": "PUNE JN",
    "ec": "PUNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SBC",
    "en": "KSR BENGALURU",
    "se": "KARNATAKA",
    "tg": "BANGALORE"
  },
  {
    "sc": "ADI",
    "en": "AHMEDABAD JN",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "LTT",
    "en": "LOKMANYATILAK T",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NZM",
    "en": "H NIZAMUDDIN",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "CSMT",
    "en": "C SHIVAJI MAH T",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JP",
    "en": "JAIPUR",
    "ec": "JAIPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ANVT",
    "en": "ANAND VIHAR TRM",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "MS",
    "en": "CHENNAI EGMORE",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "DLI",
    "en": "DELHI",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "ST",
    "en": "SURAT",
    "se": "GUJARAT"
  },
  {
    "sc": "BDTS",
    "en": "BANDRA TERMINUS",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BZA",
    "en": "VIJAYAWADA JN",
    "ec": "VIJAYAWADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VSKP",
    "en": "VISAKHAPATNAM",
    "ec": "VISAKHAPATNAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "YPR",
    "en": "YESVANTPUR JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "PNBE",
    "en": "PATNA JN",
    "se": "BIHAR"
  },
  {
    "sc": "MMCT",
    "en": "MUMBAI CENTRAL",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BPL",
    "en": "BHOPAL  JN",
    "ec": "BHOPAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NGP",
    "en": "NAGPUR",
    "ec": "NAGPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LKO",
    "en": "LUCKNOW NR",
    "ec": "LUCKNOW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BVI",
    "en": "BORIVALI",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BSB",
    "en": "VARANASI JN",
    "ec": "BANARAS",
    "se": "UTTAR PRADESH",
    "tg": "KASHI"
  },
  {
    "sc": "KYN",
    "en": "KALYAN JN",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CNB",
    "en": "KANPUR CENTRAL",
    "ec": "KANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBS",
    "en": "BHUBANESWAR",
    "ec": "BHUBANESWAR",
    "se": "ODISHA"
  },
  {
    "sc": "CBE",
    "en": "COIMBATORE JN",
    "ec": "COIMBATORE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SDAH",
    "en": "SEALDAH",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TVC",
    "en": "TRIVANDRUM CNTL",
    "ec": "THIRUVANANTHAPURAM",
    "se": "KERALA"
  },
  {
    "sc": "BRC",
    "en": "VADODARA JN",
    "ec": "VADODARA",
    "se": "GUJARAT"
  },
  {
    "sc": "GKP",
    "en": "GORAKHPUR JN",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JAT",
    "en": "JAMMU TAWI",
    "ec": "Jammu",
    "se": "JAMMU AND KASHMIR",
    "tg": "VAISHNODEVI"
  },
  {
    "sc": "JBP",
    "en": "JABALPUR",
    "ec": "JABALPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "INDB",
    "en": "INDORE JN BG",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TNA",
    "en": "THANE",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PRYJ",
    "en": "PRAYAGRAJ JN.",
    "ec": "PRAYAGRAJ",
    "se": "UTTAR PRADESH",
    "tg": "ALLAHABAD"
  },
  {
    "sc": "LJN",
    "en": "LUCKNOW NE",
    "ec": "LUCKNOW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KOTA",
    "en": "KOTA JN",
    "ec": "KOTA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JU",
    "en": "JODHPUR JN",
    "ec": "JODHPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DEE",
    "en": "DELHI S ROHILLA",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "TBM",
    "en": "TAMBARAM",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TPTY",
    "en": "TIRUPATI",
    "ec": "TIRUPATI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GWL",
    "en": "GWALIOR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "R",
    "en": "RAIPUR JN",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DR",
    "en": "DADAR",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CDG",
    "en": "CHANDIGARH",
    "se": "CHANDIGARH"
  },
  {
    "sc": "ERS",
    "en": "ERNAKULAM JN",
    "ec": "KOCHI / ERNAKULAM",
    "se": "KERALA"
  },
  {
    "sc": "GHY",
    "en": "GUWAHATI",
    "ec": "GUWAHATI",
    "se": "ASSAM"
  },
  {
    "sc": "TATA",
    "en": "TATANAGAR JN",
    "ec": "TATANAGAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "KCG",
    "en": "KACHEGUDA",
    "ec": "SECUNDERABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "CLT",
    "en": "KOZHIKKODE",
    "se": "KERALA"
  },
  {
    "sc": "MDU",
    "en": "MADURAI JN",
    "ec": "KODAIKANAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TPJ",
    "en": "TIRUCHCHIRAPALI",
    "ec": "TIRUCHCHIRAPALI/SRIRANGAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "RNC",
    "en": "RANCHI",
    "ec": "HATIA/RANCHI",
    "se": "JHARKHAND"
  },
  {
    "sc": "KJM",
    "en": "KRISHNARAJAPURM",
    "se": "KARNATAKA"
  },
  {
    "sc": "VGLJ",
    "en": "V LAKSHMIBAIJHS",
    "ec": "JHANSI",
    "se": "UTTAR PRADESH",
    "tg": "JHANSI"
  },
  {
    "sc": "GZB",
    "en": "GHAZIABAD",
    "ec": "NEW DELHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ASR",
    "en": "AMRITSAR JN",
    "ec": "AMRITSAR",
    "se": "PUNJAB"
  },
  {
    "sc": "LDH",
    "en": "LUDHIANA JN",
    "ec": "LUDHIANA",
    "se": "PUNJAB"
  },
  {
    "sc": "AII",
    "en": "AJMER JN",
    "ec": "AJMER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TCR",
    "en": "THRISUR",
    "se": "KERALA"
  },
  {
    "sc": "KOAA",
    "en": "KOLKATA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SUR",
    "en": "SOLAPUR JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AGC",
    "en": "AGRA CANTT",
    "ec": "AGRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NJP",
    "en": "NEW JALPAIGURI",
    "ec": "NEW JALPAIGURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MTJ",
    "en": "MATHURA JN",
    "ec": "MATHURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UMB",
    "en": "AMBALA CANT JN",
    "ec": "AMBALA",
    "se": "HARYANA"
  },
  {
    "sc": "MYS",
    "en": "MYSURU JN",
    "ec": "MYSURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "HYB",
    "en": "HYDERABAD DECAN",
    "ec": "SECUNDERABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "NK",
    "en": "NASHIK ROAD",
    "ec": "NASHIK",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RKMP",
    "en": "RANI KAMALAPATI",
    "ec": "BHOPAL",
    "se": "MADHYA PRADESH",
    "tg": "HABIBGUNJ"
  },
  {
    "sc": "UBL",
    "en": "SSS HUBBALLI JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "RJY",
    "en": "RAJAHMUNDRY",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ED",
    "en": "ERODE JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "BSP",
    "en": "BILASPUR JN",
    "ec": "BILASPUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KPD",
    "en": "KATPADI JN",
    "ec": "VELLORE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SA",
    "en": "SALEM JN",
    "ec": "SALEM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MAO",
    "en": "MADGAON",
    "ec": "MADGAON",
    "se": "GOA",
    "tg": "GOA"
  },
  {
    "sc": "MFP",
    "en": "MUZAFFARPUR JN",
    "se": "BIHAR"
  },
  {
    "sc": "AWB",
    "en": "AURANGABAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GNT",
    "en": "GUNTUR JN",
    "ec": "GUNTUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RJPB",
    "en": "RAJENDRANAGAR T",
    "se": "BIHAR"
  },
  {
    "sc": "NED",
    "en": "H SAHIB NANDED",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HW",
    "en": "HARIDWAR JN",
    "ec": "HARIDWAR",
    "se": "UTTARAKHAND",
    "tg": "BADRINATH,KEDARNATH"
  },
  {
    "sc": "BSBS",
    "en": "BANARAS",
    "ec": "BANARAS",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ERN",
    "en": "ERNAKULAM TOWN",
    "ec": "KOCHI / ERNAKULAM",
    "se": "KERALA"
  },
  {
    "sc": "PNVL",
    "en": "PANVEL",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VAPI",
    "en": "VAPI",
    "se": "GUJARAT"
  },
  {
    "sc": "DDU",
    "en": "DD UPADHYAYA JN",
    "se": "UTTAR PRADESH",
    "tg": "MUGHALSARAI"
  },
  {
    "sc": "BKN",
    "en": "BIKANER JN",
    "ec": "BIKANER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "UJN",
    "en": "UJJAIN JN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PURI",
    "en": "PURI",
    "ec": "PURI",
    "se": "ODISHA"
  },
  {
    "sc": "UDZ",
    "en": "UDAIPUR CITY",
    "ec": "UDAIPUR CITY",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BE",
    "en": "BAREILLY",
    "ec": "BAREILLY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KGP",
    "en": "KHARAGPUR JN",
    "ec": "KHARAGPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CAN",
    "en": "KANNUR",
    "se": "KERALA"
  },
  {
    "sc": "TEN",
    "en": "TIRUNELVELI JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ACND",
    "en": "A N DEV NAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ASBS",
    "en": "A S BHALE SULTN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ABB",
    "en": "ABADA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AHA",
    "en": "ABHAIPUR",
    "ec": "JAMALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "AVP",
    "en": "ABHANPUR JN",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "AYU",
    "en": "ABHAYAPURI ASAM",
    "se": "ASSAM"
  },
  {
    "sc": "ABS",
    "en": "ABOHAR",
    "se": "PUNJAB"
  },
  {
    "sc": "ABR",
    "en": "ABU ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ABW",
    "en": "ABUTARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ULD",
    "en": "ACHALDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ACH",
    "en": "ACHALGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ELP",
    "en": "ACHALPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ACK",
    "en": "ACHARAPAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ACG",
    "en": "ACHEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AH",
    "en": "ACHHNERA JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ACRN",
    "en": "ACHIRNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ADX",
    "en": "ADAPUR",
    "se": "BIHAR"
  },
  {
    "sc": "ADE",
    "en": "ADARI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "AKI",
    "en": "ADARKI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AHO",
    "en": "ADARSHNAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ADD",
    "en": "ADAS ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "ADVI",
    "en": "ADAVALI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AEX",
    "en": "ADDERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "AAR",
    "en": "ADESAR",
    "se": "GUJARAT"
  },
  {
    "sc": "ABZ",
    "en": "ADGAON BUZURG",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ADTL",
    "en": "ADHARTAL",
    "ec": "JABALPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ACN",
    "en": "ADHICHCHANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ADQ",
    "en": "ADHIKARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AHZ",
    "en": "ADHINPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AKNR",
    "en": "ADHYATMIK NAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ADST",
    "en": "ADI SAPTAGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ACCI",
    "en": "ADICHUNCHANGIRI",
    "se": "KARNATAKA"
  },
  {
    "sc": "ADHL",
    "en": "ADIHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "ADB",
    "en": "ADILABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "ADF",
    "en": "ADINA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AI",
    "en": "ADIPUR",
    "ec": "GANDHIDHAM",
    "se": "GUJARAT"
  },
  {
    "sc": "APQ",
    "en": "ADITPARA",
    "se": "GUJARAT"
  },
  {
    "sc": "ADTP",
    "en": "ADITYAPUR",
    "ec": "TATANAGAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "AYM",
    "en": "ADIYAKKAMUNGALM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AD",
    "en": "ADONI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ADRA",
    "en": "ADRA JN",
    "ec": "ADRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AJM",
    "en": "ADRAJ MOTI",
    "se": "GUJARAT"
  },
  {
    "sc": "ANDI",
    "en": "ADRSH NGR DELHI",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "ADT",
    "en": "ADUTURAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AGM",
    "en": "AGARAM SIBBANDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AGP",
    "en": "AGARPARA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL",
    "tg": "HOWRAH, KOLKATA"
  },
  {
    "sc": "AGTL",
    "en": "AGARTALA",
    "se": "TRIPURA"
  },
  {
    "sc": "AGAS",
    "en": "AGAS",
    "se": "GUJARAT"
  },
  {
    "sc": "AGD",
    "en": "AGASOD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AGX",
    "en": "AGASTIYAMPALLI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AWP",
    "en": "AGHWANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AGMN",
    "en": "AGOMONI",
    "se": "ASSAM"
  },
  {
    "sc": "AGY",
    "en": "AGORI KHAS",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AGA",
    "en": "AGRA CITY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AF",
    "en": "AGRA FORT",
    "ec": "AGRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AGAE",
    "en": "AGRADWIP",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AGDL",
    "en": "AGRAN DHULGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AUL",
    "en": "AGSAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AGT",
    "en": "AGTHORI",
    "se": "ASSAM"
  },
  {
    "sc": "AHLR",
    "en": "AHALYAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AHQ",
    "en": "AHERA HALT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AHD",
    "en": "AHERWADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AHM",
    "en": "AHIMANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AHN",
    "en": "AHIRAN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AHU",
    "en": "AHIRAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AHJU",
    "en": "AHJU",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "AHH",
    "en": "AHMADGARH",
    "se": "PUNJAB"
  },
  {
    "sc": "ANG",
    "en": "AHMADNAGAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AMP",
    "en": "AHMADPUR JN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ADIJ",
    "en": "AHMEDABAD MG",
    "se": "GUJARAT"
  },
  {
    "sc": "ARW",
    "en": "AHRAURA ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AILM",
    "en": "AILAM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ASH",
    "en": "AISHBAGH",
    "ec": "LUCKNOW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AIT",
    "en": "AIT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ATMO",
    "en": "AITHAL",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "AYN",
    "en": "AIYANAPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AJR",
    "en": "AJAIBPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AJK",
    "en": "AJAKOLLU",
    "se": "TELANGANA"
  },
  {
    "sc": "ANI",
    "en": "AJANTI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AIA",
    "en": "AJARAKA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "AJ",
    "en": "AJGAIN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AJH",
    "en": "AJHAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AJIT",
    "en": "AJIT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "AJKI",
    "en": "AJIT KHERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AJTM",
    "en": "AJITGILL MATTA",
    "se": "PUNJAB"
  },
  {
    "sc": "AJL",
    "en": "AJITWAL",
    "se": "PUNJAB"
  },
  {
    "sc": "AJP",
    "en": "AJJAMPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "AJNI",
    "en": "AJNI",
    "ec": "NAGPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AJN",
    "en": "AJNOD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AJWA",
    "en": "AJWA",
    "se": "GUJARAT"
  },
  {
    "sc": "AKIP",
    "en": "AKAIPUR HALT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AKOR",
    "en": "AKALKOT ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AKT",
    "en": "AKALTARA",
    "ec": "CHAMPA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "AKE",
    "en": "AKANAPET JN",
    "se": "TELANGANA"
  },
  {
    "sc": "AKZ",
    "en": "AKASHI",
    "se": "JHARKHAND"
  },
  {
    "sc": "AMY",
    "en": "AKATHUMURI",
    "se": "KERALA"
  },
  {
    "sc": "AKN",
    "en": "AKBARNAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "ABP",
    "en": "AKBARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AKVD",
    "en": "AKIVIDU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "AKAT",
    "en": "AKKAMPET",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "API",
    "en": "AKKARAIPPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AKK",
    "en": "AKKIHEBBAIU",
    "se": "KARNATAKA"
  },
  {
    "sc": "AKY",
    "en": "AKKURTI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "AKLA",
    "en": "AKLERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "AKD",
    "en": "AKODIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AK",
    "en": "AKOLA JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AKR",
    "en": "AKOLNER",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AKW",
    "en": "AKORA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AKOT",
    "en": "AKOT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AKRA",
    "en": "AKRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AYRN",
    "en": "AKSHAYWAT R NGR",
    "se": "BIHAR"
  },
  {
    "sc": "AKRD",
    "en": "AKURDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ALAI",
    "en": "ALAI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ALK",
    "en": "ALAKKUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ALAL",
    "en": "ALAL",
    "se": "PUNJAB"
  },
  {
    "sc": "ALM",
    "en": "ALAMANDA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "AMG",
    "en": "ALAMNAGAR",
    "ec": "LUCKNOW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ALMR",
    "en": "ALAMPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "ALPR",
    "en": "ALAMPUR ROAD",
    "se": "TELANGANA"
  },
  {
    "sc": "ALN",
    "en": "ALANDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AAU",
    "en": "ALAPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ALP",
    "en": "ALAPAKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ATB",
    "en": "ALATTAMBADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AWL",
    "en": "ALAWALPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "AIH",
    "en": "ALAWALPUR I PUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ALER",
    "en": "ALER",
    "se": "TELANGANA"
  },
  {
    "sc": "AWH",
    "en": "ALEWAHI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ALGP",
    "en": "ALGAPUR",
    "se": "ASSAM"
  },
  {
    "sc": "AIG",
    "en": "ALGAWAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ALB",
    "en": "ALIA BADA",
    "se": "GUJARAT"
  },
  {
    "sc": "ALJ",
    "en": "ALIGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ALJN",
    "en": "ALIGARH JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ATX",
    "en": "ALINAGAR TOLA",
    "se": "BIHAR"
  },
  {
    "sc": "AIR",
    "en": "ALINDRA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "APD",
    "en": "ALIPUR DUAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "APDC",
    "en": "ALIPUR DUAR CRT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "APDJ",
    "en": "ALIPUR DUAR JN",
    "ec": "ALIPUR DUAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ARPR",
    "en": "ALIRAJPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AYB",
    "en": "ALIYABAD"
  },
  {
    "sc": "ALLP",
    "en": "ALLEPPEY",
    "se": "KERALA"
  },
  {
    "sc": "AXR",
    "en": "ALLURU ROAD",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "LMT",
    "en": "ALMATTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "ALMW",
    "en": "ALMAW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LWR",
    "en": "ALNAVAR JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "ALNI",
    "en": "ALNIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ATM",
    "en": "ALTAGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AUB",
    "en": "ALUABARI ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ALUR",
    "en": "ALUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "AWY",
    "en": "ALUVA",
    "se": "KERALA"
  },
  {
    "sc": "ALW",
    "en": "ALWAL",
    "se": "TELANGANA"
  },
  {
    "sc": "AWR",
    "en": "ALWAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "AWT",
    "en": "ALWAR TIRUNAGRI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AGZ",
    "en": "AMAGURA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "AN",
    "en": "AMALNER",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AMLP",
    "en": "AMALPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "AML",
    "en": "AMALSAD",
    "se": "GUJARAT"
  },
  {
    "sc": "AMW",
    "en": "AMAN VADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AVC",
    "en": "AMARAVATHI CLNY",
    "se": "KARNATAKA"
  },
  {
    "sc": "AMVA",
    "en": "AMARAVILA",
    "se": "KERALA"
  },
  {
    "sc": "ARD",
    "en": "AMARDA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "AGR",
    "en": "AMARGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AGL",
    "en": "AMARGOL",
    "se": "KARNATAKA"
  },
  {
    "sc": "APJ",
    "en": "AMARPUR JORASI",
    "se": "HARYANA"
  },
  {
    "sc": "APA",
    "en": "AMARPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "AMPR",
    "en": "AMARPURA RATHAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "AXA",
    "en": "AMARSAR",
    "se": "GUJARAT"
  },
  {
    "sc": "ARNB",
    "en": "AMARUN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AMS",
    "en": "AMAUSI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AADR",
    "en": "AMB  ANDAURA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "AGB",
    "en": "AMBAGAON",
    "se": "ODISHA"
  },
  {
    "sc": "UBC",
    "en": "AMBALA CITY",
    "ec": "AMBALA",
    "se": "HARYANA"
  },
  {
    "sc": "AMPA",
    "en": "AMBALAPPUZHA",
    "se": "KERALA"
  },
  {
    "sc": "ABLE",
    "en": "AMBALE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ABGM",
    "en": "AMBALGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ABX",
    "en": "AMBARI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ABFC",
    "en": "AMBARI FALAKATA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ABH",
    "en": "AMBARNATH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ABSA",
    "en": "AMBASA",
    "se": "TRIPURA"
  },
  {
    "sc": "ASD",
    "en": "AMBASAMUDRAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ABU",
    "en": "AMBATTUR",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ABI",
    "en": "AMBATURAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AAV",
    "en": "AMBAV",
    "se": "GUJARAT"
  },
  {
    "sc": "AVA",
    "en": "AMBEWADI",
    "se": "KARNATAKA"
  },
  {
    "sc": "AAP",
    "en": "AMBIAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ABKA",
    "en": "AMBIKA KALNA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AMBR",
    "en": "AMBIKA ROHINA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ABKP",
    "en": "AMBIKAPUR",
    "ec": "AMBIKAPUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "ABY",
    "en": "AMBIVLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ABD",
    "en": "AMBLI ROAD",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "UMN",
    "en": "AMBLIYASAN",
    "se": "GUJARAT"
  },
  {
    "sc": "AMB",
    "en": "AMBODALA",
    "se": "ODISHA"
  },
  {
    "sc": "AB",
    "en": "AMBUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "UDR",
    "en": "AMDARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AME",
    "en": "AMETHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AGN",
    "en": "AMGAON",
    "ec": "GONDIA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AHT",
    "en": "AMGHATA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AGI",
    "en": "AMGURI",
    "se": "ASSAM"
  },
  {
    "sc": "ARH",
    "en": "AMHERA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AMD",
    "en": "AMILA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AMIN",
    "en": "AMIN",
    "se": "HARYANA"
  },
  {
    "sc": "AMLA",
    "en": "AMLA JN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AAL",
    "en": "AMLAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AMX",
    "en": "AMLAKHURD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ALE",
    "en": "AMLETHA",
    "se": "GUJARAT"
  },
  {
    "sc": "AMLI",
    "en": "AMLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ALS",
    "en": "AMLORI SARSAR",
    "se": "BIHAR"
  },
  {
    "sc": "ANB",
    "en": "AMMANABROLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "AMNR",
    "en": "AMMANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AMT",
    "en": "AMMAPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AMSA",
    "en": "AMMASANDRA",
    "se": "KARNATAKA"
  },
  {
    "sc": "AMQ",
    "en": "AMMUGUDA",
    "se": "TELANGANA"
  },
  {
    "sc": "ANQ",
    "en": "AMNAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AMOD",
    "en": "AMOD",
    "se": "GUJARAT"
  },
  {
    "sc": "AMO",
    "en": "AMOLWA",
    "se": "BIHAR"
  },
  {
    "sc": "AONI",
    "en": "AMONI",
    "se": "ASSAM"
  },
  {
    "sc": "AMI",
    "en": "AMRAVATI",
    "ec": "AMARAVATI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AE",
    "en": "AMRELI",
    "se": "GUJARAT"
  },
  {
    "sc": "AEP",
    "en": "AMRELI PARA",
    "se": "GUJARAT"
  },
  {
    "sc": "AMC",
    "en": "AMRITAPURA",
    "se": "KARNATAKA"
  },
  {
    "sc": "AVL",
    "en": "AMRITVEL",
    "se": "GUJARAT"
  },
  {
    "sc": "AMRO",
    "en": "AMROHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ANM",
    "en": "ANAIMALAI ROAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AKP",
    "en": "ANAKAPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ANKI",
    "en": "ANAKHI",
    "se": "GUJARAT"
  },
  {
    "sc": "AKL",
    "en": "ANAKHOL",
    "se": "GUJARAT"
  },
  {
    "sc": "ANND",
    "en": "ANAND JN",
    "se": "GUJARAT"
  },
  {
    "sc": "ANDN",
    "en": "ANAND NAGAR",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ANVR",
    "en": "ANAND VIHAR",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "ANF",
    "en": "ANANDAPURAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "ANSB",
    "en": "ANANDPUR SAHIB",
    "se": "PUNJAB"
  },
  {
    "sc": "ANP",
    "en": "ANANDTANDAVPUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ANU",
    "en": "ANANGUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AEH",
    "en": "ANANT PAITH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ATP",
    "en": "ANANTAPUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ANE",
    "en": "ANANTARAJUPET",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ANT",
    "en": "ANANTNAG",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "APT",
    "en": "ANAPARTI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ANR",
    "en": "ANARA",
    "ec": "ADRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ANAS",
    "en": "ANAS",
    "se": "GUJARAT"
  },
  {
    "sc": "AVN",
    "en": "ANAVARDIKHANPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ANW",
    "en": "ANAWAL",
    "se": "GUJARAT"
  },
  {
    "sc": "ACL",
    "en": "ANCHELI",
    "se": "GUJARAT"
  },
  {
    "sc": "UDL",
    "en": "ANDAL JN",
    "ec": "ANDAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AND",
    "en": "ANDAMPALIAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "APE",
    "en": "ANDANAPPETTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ADH",
    "en": "ANDHERI",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ADPT",
    "en": "ANDIPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ADL",
    "en": "ANDUL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AEK",
    "en": "ANEKAL ROAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "AGCI",
    "en": "ANGADI",
    "se": "GUJARAT"
  },
  {
    "sc": "AAM",
    "en": "ANGADIPPURAM",
    "se": "KERALA"
  },
  {
    "sc": "AGE",
    "en": "ANGAI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "AKU",
    "en": "ANGALAKUDURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "AFK",
    "en": "ANGAMALI",
    "se": "KERALA"
  },
  {
    "sc": "AAG",
    "en": "ANGAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ARG",
    "en": "ANGAR GHAT",
    "se": "BIHAR"
  },
  {
    "sc": "ANGL",
    "en": "ANGUL",
    "se": "ODISHA"
  },
  {
    "sc": "APU",
    "en": "ANIPUR",
    "se": "ASSAM"
  },
  {
    "sc": "ANJ",
    "en": "ANJANGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ANO",
    "en": "ANJANI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AJE",
    "en": "ANJAR",
    "se": "GUJARAT"
  },
  {
    "sc": "AJI",
    "en": "ANJHI SHAHABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ANKX",
    "en": "ANK MMR DIRECT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ANK",
    "en": "ANKAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AAK",
    "en": "ANKAI KILA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ALV",
    "en": "ANKLAV",
    "se": "GUJARAT"
  },
  {
    "sc": "AKV",
    "en": "ANKLESHWAR JN",
    "se": "GUJARAT"
  },
  {
    "sc": "ANKL",
    "en": "ANKOLA",
    "se": "KARNATAKA"
  },
  {
    "sc": "ANH",
    "en": "ANKORAH AKORHA",
    "se": "BIHAR"
  },
  {
    "sc": "AKSP",
    "en": "ANKSAPUR",
    "se": "TELANGANA"
  },
  {
    "sc": "AKS",
    "en": "ANKUSPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ANNG",
    "en": "ANNA NAGAR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ANV",
    "en": "ANNAVARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ANC",
    "en": "ANNECHAKANAHALI",
    "se": "KARNATAKA"
  },
  {
    "sc": "NGR",
    "en": "ANNIGERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "ANPR",
    "en": "ANPARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ANPD",
    "en": "ANPARA ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AAGH",
    "en": "ANTAGARH",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "ATH",
    "en": "ANTAH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ARI",
    "en": "ANTRI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ANL",
    "en": "ANTROLI",
    "se": "GUJARAT"
  },
  {
    "sc": "AUBR",
    "en": "ANUGRAHA N ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "ANPM",
    "en": "ANUPALEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "APG",
    "en": "ANUPGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "APH",
    "en": "ANUPGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "APB",
    "en": "ANUPPAMBATTU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "APR",
    "en": "ANUPPUR JN",
    "ec": "ANUPPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AUS",
    "en": "ANUPSHAHR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "AO",
    "en": "AONLA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "APL",
    "en": "APPIKATLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "APTA",
    "en": "APTA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ARA",
    "en": "ARA JN",
    "se": "BIHAR"
  },
  {
    "sc": "ARAG",
    "en": "ARAG",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AJJ",
    "en": "ARAKKONAM JN",
    "ec": "KANCHIPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ARK",
    "en": "ARAKU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ARGP",
    "en": "ARALAGUPPE",
    "se": "KARNATAKA"
  },
  {
    "sc": "AAY",
    "en": "ARALVAYMOZHI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AKM",
    "en": "ARAMBAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ARN",
    "en": "ARAND",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "ANMD",
    "en": "ARANG MAHANADI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "AG",
    "en": "ARANGHATA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ATQ",
    "en": "ARANTANGI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AON",
    "en": "ARAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ARR",
    "en": "ARARIYA",
    "se": "BIHAR"
  },
  {
    "sc": "ARQ",
    "en": "ARARIYA COURT",
    "se": "BIHAR"
  },
  {
    "sc": "ARU",
    "en": "ARASALU",
    "se": "KARNATAKA"
  },
  {
    "sc": "ARL",
    "en": "ARAUL MAKANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AVRD",
    "en": "ARAVALI ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AVLI",
    "en": "ARAVALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "AVK",
    "en": "ARAVANKADU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ARX",
    "en": "ARELI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ARPL",
    "en": "AREPALLI HALT",
    "se": "TELANGANA"
  },
  {
    "sc": "AOR",
    "en": "ARGORA",
    "se": "JHARKHAND"
  },
  {
    "sc": "ARGL",
    "en": "ARGUL",
    "ec": "KHURDA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "ARGD",
    "en": "ARIGADA",
    "se": "JHARKHAND"
  },
  {
    "sc": "ALU",
    "en": "ARIYALUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AS",
    "en": "ARJANSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ARNH",
    "en": "ARJUNAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "AJU",
    "en": "ARJUNI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ARMU",
    "en": "ARMUR",
    "se": "TELANGANA"
  },
  {
    "sc": "AEJ",
    "en": "ARNEJ",
    "se": "GUJARAT"
  },
  {
    "sc": "ARE",
    "en": "ARNETHA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ARV",
    "en": "ARNI ROAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ARNA",
    "en": "ARNIA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ASI",
    "en": "ARSENI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ASK",
    "en": "ARSIKERE JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "ATC",
    "en": "ARTS COLLEGE",
    "se": "TELANGANA"
  },
  {
    "sc": "ANY",
    "en": "ARUMUGANERI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ARCL",
    "en": "ARUNACHAL",
    "se": "ASSAM"
  },
  {
    "sc": "APK",
    "en": "ARUPPUKKOTTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ARVI",
    "en": "ARVI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AYV",
    "en": "ARYANKAVU",
    "se": "KERALA"
  },
  {
    "sc": "AFR",
    "en": "ASAFPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ACT",
    "en": "ASAKALATTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "JOB",
    "en": "ASALPUR JOBNER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ASAN",
    "en": "ASAN",
    "se": "HARYANA"
  },
  {
    "sc": "ASB",
    "en": "ASANBONI",
    "se": "JHARKHAND"
  },
  {
    "sc": "ASO",
    "en": "ASANGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ASN",
    "en": "ASANSOL JN",
    "ec": "ASANSOL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AST",
    "en": "ASAOTI",
    "se": "HARYANA"
  },
  {
    "sc": "ASM",
    "en": "ASARMA",
    "se": "GUJARAT"
  },
  {
    "sc": "ASV",
    "en": "ASARVA JN",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "ASE",
    "en": "ASAUDAH",
    "se": "HARYANA"
  },
  {
    "sc": "AQG",
    "en": "ASHAPURA GOMAT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ASKN",
    "en": "ASHOK NAGAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ASKR",
    "en": "ASHOK NAGAR RD",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AP",
    "en": "ASHOKAPURAM",
    "ec": "MYSURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "ASTG",
    "en": "ASHTEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AHI",
    "en": "ASHTI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ASAF",
    "en": "ASIFABAD ROAD",
    "se": "TELANGANA"
  },
  {
    "sc": "AGQ",
    "en": "ASIRGARH ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ANA",
    "en": "ASLANA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ASL",
    "en": "ASLAODA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ASLU",
    "en": "ASLU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "AT",
    "en": "ASNOTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "AXK",
    "en": "ASOKHAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ASP",
    "en": "ASPARI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "AAS",
    "en": "ASRANADA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ABO",
    "en": "ASTHAL BOHAR",
    "se": "HARYANA"
  },
  {
    "sc": "AV",
    "en": "ASVALI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AWS",
    "en": "ASWANI HALT",
    "se": "BIHAR"
  },
  {
    "sc": "AWM",
    "en": "ASWAPURAM",
    "se": "TELANGANA"
  },
  {
    "sc": "ATA",
    "en": "ATA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AMA",
    "en": "ATAMANDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ATT",
    "en": "ATARI",
    "se": "PUNJAB"
  },
  {
    "sc": "AA",
    "en": "ATARIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ATE",
    "en": "ATARRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AEL",
    "en": "ATELI",
    "se": "HARYANA"
  },
  {
    "sc": "ATG",
    "en": "ATGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ATL",
    "en": "ATHMAL GOLA",
    "se": "BIHAR"
  },
  {
    "sc": "ASCE",
    "en": "ATHSARAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AMM",
    "en": "ATIRAMPATTINAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ATDA",
    "en": "ATLADARA",
    "se": "GUJARAT"
  },
  {
    "sc": "ARP",
    "en": "ATRAMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AUR",
    "en": "ATRAULI ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ATRR",
    "en": "ATRAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ATRI",
    "en": "ATRI PH",
    "se": "ODISHA"
  },
  {
    "sc": "ATRU",
    "en": "ATRU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ATS",
    "en": "ATTABIRA",
    "se": "ODISHA"
  },
  {
    "sc": "ATR",
    "en": "ATTAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "AL",
    "en": "ATTILI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "AIP",
    "en": "ATTIPPATTU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ATU",
    "en": "ATTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ATUL",
    "en": "ATUL",
    "se": "GUJARAT"
  },
  {
    "sc": "ATKS",
    "en": "ATWA KURSATH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AJRE",
    "en": "AUJARI",
    "se": "ASSAM"
  },
  {
    "sc": "AED",
    "en": "AULENDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AUNG",
    "en": "AUNG",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "OND",
    "en": "AUNLAJORI JN",
    "se": "ODISHA"
  },
  {
    "sc": "ARJ",
    "en": "AUNRIHAR JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ANAH",
    "en": "AUNTA HALT",
    "se": "BIHAR"
  },
  {
    "sc": "AUI",
    "en": "AURAHI",
    "se": "BIHAR"
  },
  {
    "sc": "AUN",
    "en": "AURANG NAGAR",
    "se": "HARYANA"
  },
  {
    "sc": "OSA",
    "en": "AUSA ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AVS",
    "en": "AUVANESWSAREM",
    "se": "KERALA"
  },
  {
    "sc": "AUWA",
    "en": "AUWA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "AVD",
    "en": "AVADI",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AVT",
    "en": "AVATIHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "AVH",
    "en": "AVIDHA",
    "se": "GUJARAT"
  },
  {
    "sc": "ALAT",
    "en": "AVULADATLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "AWG",
    "en": "AWA GARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ATPA",
    "en": "AWANTIPURA",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "AWPR",
    "en": "AWAPUR",
    "se": "BIHAR"
  },
  {
    "sc": "ATNR",
    "en": "AWATARNAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "AYD",
    "en": "AYANDUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AYI",
    "en": "AYINGUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AYC",
    "en": "AYODHYA CANTT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AY",
    "en": "AYODHYA DHAM JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "APN",
    "en": "AYODHYAPATTANAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AYR",
    "en": "AYYALUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AZP",
    "en": "AYYAMPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "AMH",
    "en": "AZAMGARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AZR",
    "en": "AZAMNAGAR ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "AZA",
    "en": "AZARA",
    "ec": "GUWAHATI",
    "se": "ASSAM"
  },
  {
    "sc": "AZK",
    "en": "AZHWARKURICHI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ACLE",
    "en": "AZIMGANJ CITY",
    "se": "WEST BENGAL"
  },
  {
    "sc": "AZ",
    "en": "AZIMGANJ JN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BEY",
    "en": "B CEMENT NAGAR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BBLK",
    "en": "B L DASPURI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BGNR",
    "en": "B.G.NAGAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "BBKR",
    "en": "BABA BAKALARAYA",
    "se": "PUNJAB"
  },
  {
    "sc": "BBSL",
    "en": "BABA SODHALNAGR",
    "se": "PUNJAB"
  },
  {
    "sc": "BBJ",
    "en": "BABAGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBDE",
    "en": "BABARPUR",
    "se": "HARYANA"
  },
  {
    "sc": "BTP",
    "en": "BABATPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BV",
    "en": "BABHNAN",
    "ec": "BASTI/SITAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBV",
    "en": "BABHULGOAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BAB",
    "en": "BABINA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBD",
    "en": "BABLAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "BBA",
    "en": "BABRALA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBO",
    "en": "BABUGARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BUPH",
    "en": "BABUPETH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BBPR",
    "en": "BABUPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BCHR",
    "en": "BACHAR",
    "se": "GUJARAT"
  },
  {
    "sc": "BCHL",
    "en": "BACHELI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BCN",
    "en": "BACHHRAWAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BCA",
    "en": "BACHWARA JN",
    "se": "BIHAR"
  },
  {
    "sc": "BAD",
    "en": "BAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BDBA",
    "en": "BADABANDHA",
    "se": "ODISHA"
  },
  {
    "sc": "BDPA",
    "en": "BADALPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BDM",
    "en": "BADAMI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BMPR",
    "en": "BADAMPAHAR",
    "se": "ODISHA"
  },
  {
    "sc": "BPY",
    "en": "BADAMPUDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BDGP",
    "en": "BADANAGUPPE",
    "se": "KARNATAKA"
  },
  {
    "sc": "BPB",
    "en": "BADARPUR JN",
    "se": "ASSAM"
  },
  {
    "sc": "BDWS",
    "en": "BADARWAS",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BUS",
    "en": "BADAUSA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BWZ",
    "en": "BADDOWAL",
    "se": "PUNJAB"
  },
  {
    "sc": "BDXX",
    "en": "BADE ARAPUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BDHA",
    "en": "BADHADA",
    "se": "GUJARAT"
  },
  {
    "sc": "BDBG",
    "en": "BADHAI BALAMGRH",
    "se": "PUNJAB"
  },
  {
    "sc": "BDHL",
    "en": "BADHAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BHK",
    "en": "BADHARI KALAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BDWA",
    "en": "BADHWA BARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BDZ",
    "en": "BADKULLA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BHB",
    "en": "BADLA GHAT",
    "se": "BIHAR"
  },
  {
    "sc": "BUD",
    "en": "BADLAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BHD",
    "en": "BADLI",
    "se": "DELHI"
  },
  {
    "sc": "BUDM",
    "en": "BADMAL",
    "ec": "BALANGIR",
    "se": "ODISHA"
  },
  {
    "sc": "BDU",
    "en": "BADNAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BD",
    "en": "BADNERA JN",
    "ec": "AMARAVATI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BDDR",
    "en": "BADODAR",
    "se": "GUJARAT"
  },
  {
    "sc": "BNZ",
    "en": "BADSHAHNAGAR",
    "ec": "LUCKNOW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BSE",
    "en": "BADSHAHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BLPR",
    "en": "BADULIPAR",
    "se": "ASSAM"
  },
  {
    "sc": "BWS",
    "en": "BADWASI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BUG",
    "en": "BAGAHA",
    "se": "BIHAR"
  },
  {
    "sc": "BCJ",
    "en": "BAGAHABISHUNPUR",
    "se": "BIHAR"
  },
  {
    "sc": "BGHI",
    "en": "BAGAHAI ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BGA",
    "en": "BAGALIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BGK",
    "en": "BAGALKOT",
    "se": "KARNATAKA"
  },
  {
    "sc": "BGBR",
    "en": "BAGBAHRA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BEH",
    "en": "BAGDIHI",
    "se": "ODISHA"
  },
  {
    "sc": "BGPA",
    "en": "BAGESHAPURA",
    "se": "KARNATAKA"
  },
  {
    "sc": "BSRX",
    "en": "BAGEVADI RD",
    "se": "KARNATAKA"
  },
  {
    "sc": "BGWD",
    "en": "BAGEWADI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BGJT",
    "en": "BAGHA JATIN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BGH",
    "en": "BAGHAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BORA",
    "en": "BAGHDOGRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BBE",
    "en": "BAGHI BARDIHA",
    "se": "BIHAR"
  },
  {
    "sc": "BFX",
    "en": "BAGHI GHAUSPUR",
    "se": "BIHAR"
  },
  {
    "sc": "BGRA",
    "en": "BAGHNAPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BHKH",
    "en": "BAGHOIKUSA",
    "se": "BIHAR"
  },
  {
    "sc": "BJQ",
    "en": "BAGHORA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BGPL",
    "en": "BAGHUAPAL",
    "se": "ODISHA"
  },
  {
    "sc": "BGF",
    "en": "BAGILA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BGND",
    "en": "BAGINADI",
    "se": "ASSAM"
  },
  {
    "sc": "BMA",
    "en": "BAGMAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BZN",
    "en": "BAGNAN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BPM",
    "en": "BAGPAT ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BGTA",
    "en": "BAGRA TAWA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRQ",
    "en": "BAGRAKOT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BQN",
    "en": "BAGRI NAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BGX",
    "en": "BAGRI SAJJANPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BGL",
    "en": "BAGULA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BGMR",
    "en": "BAGUMRA",
    "se": "GUJARAT"
  },
  {
    "sc": "BAGD",
    "en": "BAGWADA (HALT)",
    "se": "GUJARAT"
  },
  {
    "sc": "BWB",
    "en": "BAGWALI",
    "se": "PUNJAB"
  },
  {
    "sc": "HAB",
    "en": "BAH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BSS",
    "en": "BAHADUR SINGH W",
    "se": "PUNJAB"
  },
  {
    "sc": "BGZ",
    "en": "BAHADURGARH",
    "se": "HARYANA"
  },
  {
    "sc": "BPD",
    "en": "BAHADURPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BYQ",
    "en": "BAHAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BDO",
    "en": "BAHALDA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "BNBR",
    "en": "BAHANAGA BAZAR",
    "se": "ODISHA"
  },
  {
    "sc": "BARU",
    "en": "BAHARU",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BFE",
    "en": "BAHAWAL BASI",
    "se": "PUNJAB"
  },
  {
    "sc": "BFV",
    "en": "BAHELIA BUZURG",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHI",
    "en": "BAHERI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BOA",
    "en": "BAHERIYA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "BIP",
    "en": "BAHILPURWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BAHW",
    "en": "BAHIR KHANDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BJ",
    "en": "BAHJOI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BWX",
    "en": "BAHMAN DIWANA",
    "se": "PUNJAB"
  },
  {
    "sc": "BVW",
    "en": "BAHMINIWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "BHCL",
    "en": "BAHORA CHANDIL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRK",
    "en": "BAHRAICH",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHM",
    "en": "BAHRAM",
    "se": "PUNJAB"
  },
  {
    "sc": "BPUR",
    "en": "BAIDPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBAE",
    "en": "BAIDYABATI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BDME",
    "en": "BAIDYANATHDHAM",
    "ec": "JASIDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "BGUA",
    "en": "BAIGUDA",
    "se": "ODISHA"
  },
  {
    "sc": "BIZ",
    "en": "BAIHATA",
    "se": "ASSAM"
  },
  {
    "sc": "BATL",
    "en": "BAIHATOLA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "VDNP",
    "en": "BAIJNATH ANDOLI",
    "se": "BIHAR"
  },
  {
    "sc": "BJMR",
    "en": "BAIJNATH MANDIR",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "BJPL",
    "en": "BAIJNATHPAPROLA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "BYP",
    "en": "BAIJNATHPUR",
    "se": "BIHAR"
  },
  {
    "sc": "BKTH",
    "en": "BAIKUNTH P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BRH",
    "en": "BAIKUNTHPUR RD",
    "ec": "AMBIKAPUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BOI",
    "en": "BAINCHI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BCGM",
    "en": "BAINCHIGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BGU",
    "en": "BAIRAGNIA",
    "se": "BIHAR"
  },
  {
    "sc": "BSGD",
    "en": "BAIS GODAM",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BSWA",
    "en": "BAISWARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BALR",
    "en": "BAITALPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BTV",
    "en": "BAITARANI ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "BYPL",
    "en": "BAIYYAPPANAHALI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BLA",
    "en": "BAJALTA",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "BAJN",
    "en": "BAJANA",
    "se": "GUJARAT"
  },
  {
    "sc": "BJKN",
    "en": "BAJEKAN",
    "se": "HARYANA"
  },
  {
    "sc": "BJPD",
    "en": "BAJIPADA",
    "se": "ODISHA"
  },
  {
    "sc": "BJT",
    "en": "BAJPATTI",
    "se": "BIHAR"
  },
  {
    "sc": "BJG",
    "en": "BAJRANGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRGP",
    "en": "BAJRANGPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "BJUD",
    "en": "BAJUD",
    "se": "GUJARAT"
  },
  {
    "sc": "BJW",
    "en": "BAJVA",
    "se": "GUJARAT"
  },
  {
    "sc": "BAKL",
    "en": "BAKAL",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BQE",
    "en": "BAKANIAN BHAUNR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BKKS",
    "en": "BAKAS",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BKPR",
    "en": "BAKASPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "BKWA",
    "en": "BAKAYANWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "BQQ",
    "en": "BAKHLETA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "VKD",
    "en": "BAKHRABAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BKHR",
    "en": "BAKHRI",
    "se": "BIHAR"
  },
  {
    "sc": "BKSA",
    "en": "BAKHSHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BKP",
    "en": "BAKHTIYARPUR JN",
    "se": "BIHAR"
  },
  {
    "sc": "BAKK",
    "en": "BAKKAL",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "BK",
    "en": "BAKRA ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BKRL",
    "en": "BAKROL",
    "se": "GUJARAT"
  },
  {
    "sc": "BKT",
    "en": "BAKSHI KA TALAB",
    "ec": "LUCKNOW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BKTL",
    "en": "BAKTAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BKLE",
    "en": "BAKUDI",
    "se": "JHARKHAND"
  },
  {
    "sc": "BKLA",
    "en": "BAKULHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BLRD",
    "en": "BALA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "BBPM",
    "en": "BALABHADRAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BGAE",
    "en": "BALAGARH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BTC",
    "en": "BALAGHAT JN",
    "ec": "GONDIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BLM",
    "en": "BALAMU JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BABR",
    "en": "BALANAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "BLGR",
    "en": "BALANGIR",
    "ec": "BALANGIR",
    "se": "ODISHA"
  },
  {
    "sc": "BLPE",
    "en": "BALAPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BRAM",
    "en": "BALARAMAPURAM",
    "se": "KERALA"
  },
  {
    "sc": "BLAE",
    "en": "BALARAMBATI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BLRG",
    "en": "BALASIRING",
    "se": "JHARKHAND"
  },
  {
    "sc": "BLDK",
    "en": "BALAUDA TAKUN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BLW",
    "en": "BALAWALI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BLDR",
    "en": "BALDANA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "BALE",
    "en": "BALE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BLPL",
    "en": "BALEL PIPARIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "BLS",
    "en": "BALESHWAR",
    "ec": "BALASORE",
    "se": "ODISHA"
  },
  {
    "sc": "BLR",
    "en": "BALGANUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "BGNA",
    "en": "BALGONA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BPQ",
    "en": "BALHARSHAH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BAE",
    "en": "BALIAKHERI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BCK",
    "en": "BALICHAK",
    "ec": "KHARAGPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BTZ",
    "en": "BALIMARA",
    "se": "ASSAM"
  },
  {
    "sc": "BVU",
    "en": "BALIPARA",
    "se": "ASSAM"
  },
  {
    "sc": "BVH",
    "en": "BALLABGARH",
    "se": "HARYANA"
  },
  {
    "sc": "BQZ",
    "en": "BALLALPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BYC",
    "en": "BALLARI CANTT",
    "ec": "BALLARI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BAY",
    "en": "BALLARI JN",
    "ec": "BALLARI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BAHI",
    "en": "BALLENAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BLLI",
    "en": "BALLI",
    "se": "GOA"
  },
  {
    "sc": "BUI",
    "en": "BALLIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BAPR",
    "en": "BALLUPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BLY",
    "en": "BALLY",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BLYG",
    "en": "BALLY GHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BLN",
    "en": "BALLYGUNGE JN",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BXA",
    "en": "BALOD",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BLT",
    "en": "BALOTRA JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BPRH",
    "en": "BALPUR HALT",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BBL",
    "en": "BALRAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BLP",
    "en": "BALRAMPUR",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BLSD",
    "en": "BALSAMAND",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BALU",
    "en": "BALUGAON",
    "se": "ODISHA"
  },
  {
    "sc": "BLGT",
    "en": "BALURGHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "WAB",
    "en": "BALWA",
    "se": "GUJARAT"
  },
  {
    "sc": "BAWA",
    "en": "BALWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BMG",
    "en": "BAMANGACHHI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BMGR",
    "en": "BAMANGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BXT",
    "en": "BAMANHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BMHR",
    "en": "BAMANHERI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BMNI",
    "en": "BAMANI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BMX",
    "en": "BAMANKUWA",
    "se": "GUJARAT"
  },
  {
    "sc": "BMNL",
    "en": "BAMANWALI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BMWS",
    "en": "BAMANWAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BMW",
    "en": "BAMHANI P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BIV",
    "en": "BAMHNI BANJAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BMU",
    "en": "BAMHRAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BMY",
    "en": "BAMIANA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BMLL",
    "en": "BAMLA",
    "se": "HARYANA"
  },
  {
    "sc": "BMI",
    "en": "BAMNIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BMZ",
    "en": "BAMOUR GAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BMB",
    "en": "BAMRA",
    "se": "ODISHA"
  },
  {
    "sc": "BMSN",
    "en": "BAMSIN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BAMR",
    "en": "BAMUR",
    "se": "ODISHA"
  },
  {
    "sc": "BGNP",
    "en": "BANAGANAPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BYN",
    "en": "BANAHI",
    "se": "BIHAR"
  },
  {
    "sc": "BPF",
    "en": "BANAPURA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BNO",
    "en": "BANAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BNQ",
    "en": "BANARHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BNS",
    "en": "BANAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BSN",
    "en": "BANASANDRA",
    "se": "KARNATAKA"
  },
  {
    "sc": "BAND",
    "en": "BANASWADI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BVR",
    "en": "BANAVAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "BNSA",
    "en": "BANBASA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "BNCR",
    "en": "BANCHARI",
    "se": "HARYANA"
  },
  {
    "sc": "BAHP",
    "en": "BAND HAMIRPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BNDA",
    "en": "BANDA JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BNU",
    "en": "BANDAKPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BDW",
    "en": "BANDANWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BXK",
    "en": "BANDARKHAL",
    "se": "ASSAM"
  },
  {
    "sc": "BDPL",
    "en": "BANDARUPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BDC",
    "en": "BANDEL JN",
    "ec": "Howrah / Kolkata  &  BANDEL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BR",
    "en": "BANDH BARETA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BNF",
    "en": "BANDHUA",
    "se": "BIHAR"
  },
  {
    "sc": "BDKN",
    "en": "BANDHUA KALAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BKI",
    "en": "BANDIKUI JN",
    "se": "RAJASTHAN",
    "tg": "MEHANDIPUR BALAJI"
  },
  {
    "sc": "BA",
    "en": "BANDRA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BSW",
    "en": "BANESWAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BXB",
    "en": "BANGA",
    "se": "PUNJAB"
  },
  {
    "sc": "BGAN",
    "en": "BANGAIN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BJY",
    "en": "BANGALBAREE",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BNJ",
    "en": "BANGAON JN",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BWT",
    "en": "BANGARAPET",
    "se": "KARNATAKA"
  },
  {
    "sc": "BGAR",
    "en": "BANGARI",
    "se": "BIHAR"
  },
  {
    "sc": "BGMU",
    "en": "BANGARMAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BNLS",
    "en": "BANGI NIHALSNGH",
    "se": "PUNJAB"
  },
  {
    "sc": "BGY",
    "en": "BANGRIPOSI",
    "se": "ODISHA"
  },
  {
    "sc": "BOD",
    "en": "BANGROD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BGKA",
    "en": "BANGURKELA",
    "se": "ODISHA"
  },
  {
    "sc": "BNBH",
    "en": "BANI BIHAR",
    "ec": "BHUBANESWAR",
    "se": "ODISHA"
  },
  {
    "sc": "BAHL",
    "en": "BANIHAL",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "BS",
    "en": "BANISAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BSDA",
    "en": "BANIYA SANDA DH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BIYA",
    "en": "BANIYANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BAKA",
    "en": "BANKA",
    "ec": "BHAGALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "BKG",
    "en": "BANKA GHAT",
    "se": "BIHAR"
  },
  {
    "sc": "BCF",
    "en": "BANKAPASI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BNKT",
    "en": "BANKAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BTK",
    "en": "BANKATA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BKH",
    "en": "BANKHEDI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BQA",
    "en": "BANKURA",
    "ec": "BISHNUPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BNKI",
    "en": "BANMANKHI JN",
    "se": "BIHAR"
  },
  {
    "sc": "BAO",
    "en": "BANMOR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BNA",
    "en": "BANNI KOPPA",
    "se": "KARNATAKA"
  },
  {
    "sc": "BNHT",
    "en": "BANNIHATTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BANO",
    "en": "BANO",
    "se": "JHARKHAND"
  },
  {
    "sc": "BASA",
    "en": "BANOSA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BPS",
    "en": "BANPAS",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BPN",
    "en": "BANPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BSDR",
    "en": "BANSADHARA",
    "se": "ODISHA"
  },
  {
    "sc": "BNSP",
    "en": "BANSAPAHAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BCD",
    "en": "BANSDIH ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BSAE",
    "en": "BANSH BARIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BSBR",
    "en": "BANSHLAI BRIDGE",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BYE",
    "en": "BANSI BOHERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BIQ",
    "en": "BANSI PAHARPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BNSL",
    "en": "BANSINALA HALT",
    "se": "BIHAR"
  },
  {
    "sc": "BSQP",
    "en": "BANSIPUR",
    "se": "BIHAR"
  },
  {
    "sc": "BZS",
    "en": "BANSJORA",
    "se": "JHARKHAND"
  },
  {
    "sc": "BSKO",
    "en": "BANSKHO",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BSPX",
    "en": "BANSPANI",
    "se": "ODISHA"
  },
  {
    "sc": "BNLW",
    "en": "BANSTHALI NIWAI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BNB",
    "en": "BANSTOLA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BGG",
    "en": "BANTA RNATHGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BLL",
    "en": "BANTANAHAL",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BNTL",
    "en": "BANTAWALA",
    "se": "KARNATAKA"
  },
  {
    "sc": "BTRA",
    "en": "BANTHRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BATA",
    "en": "BANTVA",
    "se": "GUJARAT"
  },
  {
    "sc": "BWC",
    "en": "BANWALI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BAOL",
    "en": "BAOLI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BOTI",
    "en": "BAORI THIKRIA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BAF",
    "en": "BAP",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BPP",
    "en": "BAPATLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BMKI",
    "en": "BAPUDM MOTIHARI",
    "se": "BIHAR"
  },
  {
    "sc": "BAR",
    "en": "BAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BRLF",
    "en": "BAR LANGFER S",
    "se": "ASSAM"
  },
  {
    "sc": "BGD",
    "en": "BARA GUDAH",
    "se": "HARYANA"
  },
  {
    "sc": "BJMD",
    "en": "BARA JAMDA",
    "ec": "BARABIL",
    "se": "JHARKHAND"
  },
  {
    "sc": "BRM",
    "en": "BARABAMBO",
    "se": "JHARKHAND"
  },
  {
    "sc": "BBK",
    "en": "BARABANKI JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BFF",
    "en": "BARABHATI P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BBM",
    "en": "BARABHUM",
    "ec": "PURULIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BBN",
    "en": "BARABIL",
    "ec": "BARABIL",
    "se": "ODISHA"
  },
  {
    "sc": "BCQ",
    "en": "BARACHAK",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BRDA",
    "en": "BARADIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "BUA",
    "en": "BARADWAR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BNM",
    "en": "BARAGAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BAGL",
    "en": "BARAGOPAL",
    "se": "BIHAR"
  },
  {
    "sc": "BHLE",
    "en": "BARAHAT",
    "se": "BIHAR"
  },
  {
    "sc": "BRHU",
    "en": "BARAHU",
    "se": "ASSAM"
  },
  {
    "sc": "BJLP",
    "en": "BARAI JALALPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRGM",
    "en": "BARAIGRAM JN",
    "se": "ASSAM"
  },
  {
    "sc": "BQW",
    "en": "BARAKALAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRR",
    "en": "BARAKAR",
    "ec": "ASANSOL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BARL",
    "en": "BARAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BAA",
    "en": "BARALA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BRMT",
    "en": "BARAMATI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BRML",
    "en": "BARAMULA",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "BAZ",
    "en": "BARAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BARN",
    "en": "BARANAGAR ROAD",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BRAG",
    "en": "BARANG",
    "ec": "BHUBANESWAR",
    "se": "ODISHA"
  },
  {
    "sc": "BRPS",
    "en": "BARAPALASI",
    "se": "JHARKHAND"
  },
  {
    "sc": "RAA",
    "en": "BARARA",
    "se": "HARYANA"
  },
  {
    "sc": "BRRZ",
    "en": "BARARA BUZURG",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BT",
    "en": "BARASAT",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BJU",
    "en": "BARAUNI JN",
    "se": "BIHAR"
  },
  {
    "sc": "BTU",
    "en": "BARAUT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBTR",
    "en": "BARBATPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRBR",
    "en": "BARBERA",
    "se": "JHARKHAND"
  },
  {
    "sc": "BCRD",
    "en": "BARCHI ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRDB",
    "en": "BARDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BWN",
    "en": "BARDDHAMAN JN",
    "ec": "BARDDHAMAN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BRDH",
    "en": "BARDHANA HALT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BDHT",
    "en": "BARDI HALT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BIY",
    "en": "BARDOLI",
    "se": "GUJARAT"
  },
  {
    "sc": "BRY",
    "en": "BAREILLY",
    "ec": "BAREILLY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRYC",
    "en": "BAREILLY CANTT",
    "ec": "BAREILLY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BC",
    "en": "BAREILLY CITY",
    "ec": "BAREILLY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BJD",
    "en": "BAREJADI",
    "se": "GUJARAT"
  },
  {
    "sc": "BQM",
    "en": "BARELIPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRZ",
    "en": "BARETA",
    "se": "PUNJAB"
  },
  {
    "sc": "BET",
    "en": "BARETH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRGJ",
    "en": "BARGAON GUJAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRG",
    "en": "BARGARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRGA",
    "en": "BARGARH ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "BRGW",
    "en": "BARGAWAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BUQ",
    "en": "BARGI",
    "ec": "JABALPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BGLI",
    "en": "BARGOLAI",
    "se": "ASSAM"
  },
  {
    "sc": "BARH",
    "en": "BARH",
    "se": "BIHAR"
  },
  {
    "sc": "BHJ",
    "en": "BARHAJ BAZAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRN",
    "en": "BARHAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHHT",
    "en": "BARHARA",
    "se": "BIHAR"
  },
  {
    "sc": "BAKT",
    "en": "BARHARA KOTHI",
    "se": "BIHAR"
  },
  {
    "sc": "BAGJ",
    "en": "BARHARAGANI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHW",
    "en": "BARHARWA JN",
    "ec": "SAHIBGANJ",
    "se": "JHARKHAND"
  },
  {
    "sc": "BRHI",
    "en": "BARHI",
    "se": "JHARKHAND"
  },
  {
    "sc": "BRYA",
    "en": "BARHIYA",
    "se": "BIHAR"
  },
  {
    "sc": "BNY",
    "en": "BARHNI",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRHM",
    "en": "BARHRAGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BARI",
    "en": "BARI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BBMN",
    "en": "BARI BRAHMAN",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "BKTU",
    "en": "BARI KHATU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BI",
    "en": "BARI SADRI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BUP",
    "en": "BARIARPUR",
    "ec": "JAMALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "BPO",
    "en": "BARIPADA",
    "se": "ODISHA"
  },
  {
    "sc": "BRPM",
    "en": "BARIPUR MANDALA",
    "se": "GUJARAT"
  },
  {
    "sc": "BPRA",
    "en": "BARIPURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRTG",
    "en": "BARITHENGARH",
    "se": "ODISHA"
  },
  {
    "sc": "BRW",
    "en": "BARIWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "BADK",
    "en": "BARKA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRKA",
    "en": "BARKA KANA",
    "se": "JHARKHAND"
  },
  {
    "sc": "BKA",
    "en": "BARKHERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BSYA",
    "en": "BARKISALALYA",
    "se": "BIHAR"
  },
  {
    "sc": "BKJ",
    "en": "BARKUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "BLAX",
    "en": "BARLAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BLNG",
    "en": "BARLANGA",
    "se": "JHARKHAND"
  },
  {
    "sc": "BME",
    "en": "BARMER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BRMX",
    "en": "BARMI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BNG",
    "en": "BARNAGAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BNN",
    "en": "BARNALA",
    "se": "PUNJAB"
  },
  {
    "sc": "NDBH",
    "en": "BARODA HOUSE"
  },
  {
    "sc": "BOF",
    "en": "BAROG",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "BRPL",
    "en": "BARPALI",
    "se": "ODISHA"
  },
  {
    "sc": "BXP",
    "en": "BARPATHAR",
    "se": "ASSAM"
  },
  {
    "sc": "BPRD",
    "en": "BARPETA ROAD",
    "se": "ASSAM"
  },
  {
    "sc": "BP",
    "en": "BARRACKPORE",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BJR",
    "en": "BARRAJPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BYS",
    "en": "BARSALI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BARS",
    "en": "BARSANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BSY",
    "en": "BARSATHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BSQ",
    "en": "BARSI TAKLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BTW",
    "en": "BARSI TOWN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BOE",
    "en": "BARSOI JN",
    "se": "BIHAR"
  },
  {
    "sc": "BZO",
    "en": "BARSOLA",
    "se": "HARYANA"
  },
  {
    "sc": "BXF",
    "en": "BARSUAN",
    "se": "ODISHA"
  },
  {
    "sc": "BBGN",
    "en": "BARUA BAMUNGAON",
    "se": "ASSAM"
  },
  {
    "sc": "BRCK",
    "en": "BARUA CHAK",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRNR",
    "en": "BARUANAGAR",
    "se": "ASSAM"
  },
  {
    "sc": "BRUD",
    "en": "BARUD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRPA",
    "en": "BARUIPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BRP",
    "en": "BARUIPUR JN",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BUE",
    "en": "BARUNA",
    "se": "BIHAR"
  },
  {
    "sc": "BNDI",
    "en": "BARUNDANI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BAV",
    "en": "BARUVA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BRSA",
    "en": "BARWA KALAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BWR",
    "en": "BARWA SAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRWD",
    "en": "BARWADIH JN",
    "se": "JHARKHAND"
  },
  {
    "sc": "BWW",
    "en": "BARWAHA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BXC",
    "en": "BARWALA",
    "se": "HARYANA"
  },
  {
    "sc": "BRL",
    "en": "BARWALA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "BYHA",
    "en": "BARYA RAM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRHL",
    "en": "BARYAL HIMACHAL",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "BZY",
    "en": "BASAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BDXT",
    "en": "BASAI DHANKOT",
    "se": "HARYANA"
  },
  {
    "sc": "BSPL",
    "en": "BASAMPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BSTP",
    "en": "BASANTAPUR",
    "se": "ODISHA"
  },
  {
    "sc": "BSX",
    "en": "BASAR",
    "se": "TELANGANA"
  },
  {
    "sc": "BSRI",
    "en": "BASARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BSI",
    "en": "BASBARI",
    "se": "ASSAM"
  },
  {
    "sc": "BED",
    "en": "BASERI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BTG",
    "en": "BASHARATGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BSKR",
    "en": "BASI KIRATPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBQ",
    "en": "BASIN BRIDGE JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "BSHT",
    "en": "BASIRHAT",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BSCP",
    "en": "BASKATWA B. H.",
    "se": "BIHAR"
  },
  {
    "sc": "BMF",
    "en": "BASMAT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BANE",
    "en": "BASNI",
    "ec": "JODHPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BAI",
    "en": "BASSI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BSSL",
    "en": "BASSI BERISAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BSPN",
    "en": "BASSI PATHANAM",
    "se": "PUNJAB"
  },
  {
    "sc": "BTS",
    "en": "BASTA",
    "se": "ODISHA"
  },
  {
    "sc": "BST",
    "en": "BASTI",
    "ec": "BASTI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BDBP",
    "en": "BASUDEBPUR H",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BSGN",
    "en": "BASUGAON",
    "se": "ASSAM"
  },
  {
    "sc": "BSKH",
    "en": "BASUKINATH",
    "se": "JHARKHAND"
  },
  {
    "sc": "BSD",
    "en": "BASULDANGA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BU",
    "en": "BASWA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BAT",
    "en": "BATALA JN",
    "ec": "AMRITSAR",
    "se": "PUNJAB"
  },
  {
    "sc": "BATM",
    "en": "BATALA SUGAR ML",
    "se": "PUNJAB"
  },
  {
    "sc": "BTSI",
    "en": "BATASI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BSLE",
    "en": "BATASPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BTIC",
    "en": "BATHINDA CANTT.",
    "se": "PUNJAB"
  },
  {
    "sc": "BTI",
    "en": "BATHINDA JN",
    "se": "PUNJAB"
  },
  {
    "sc": "BTF",
    "en": "BATHNAHA",
    "se": "BIHAR"
  },
  {
    "sc": "BTM",
    "en": "BATTULAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BTVA",
    "en": "BATUVA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BUDR",
    "en": "BAUDPUR",
    "se": "ODISHA"
  },
  {
    "sc": "BVA",
    "en": "BAURIA JN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "VLA",
    "en": "BAVLA",
    "se": "GUJARAT"
  },
  {
    "sc": "BWL",
    "en": "BAWAL",
    "se": "HARYANA"
  },
  {
    "sc": "BWK",
    "en": "BAWANI KHERA",
    "se": "HARYANA"
  },
  {
    "sc": "BYO",
    "en": "BAYALUVADDIGERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BXN",
    "en": "BAYANA JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BUT",
    "en": "BAYTU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BVM",
    "en": "BAYYAVARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BZLE",
    "en": "BAZARSAU",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BZJT",
    "en": "BAZIDA JATAN",
    "se": "HARYANA"
  },
  {
    "sc": "BPZ",
    "en": "BAZPUR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "BZGT",
    "en": "BAZURGHAT",
    "se": "ASSAM"
  },
  {
    "sc": "EPR",
    "en": "BB ELPHNSTNE RD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MORD",
    "en": "BB MHDALI RD CB",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CHG",
    "en": "BBY CHINCHPKILI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CTGN",
    "en": "BBY COTTON GREN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DKRD",
    "en": "BBY DOCKYARD RD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MX",
    "en": "BBY MAHALAKSHMI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BEAS",
    "en": "BEAS",
    "se": "PUNJAB"
  },
  {
    "sc": "BER",
    "en": "BEAWAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BEE",
    "en": "BEBEJIA",
    "se": "ASSAM"
  },
  {
    "sc": "BHRJ",
    "en": "BECHARJI",
    "se": "GUJARAT"
  },
  {
    "sc": "BHWA",
    "en": "BECHHIWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BDK",
    "en": "BEDAG",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BVV",
    "en": "BEDETTI",
    "se": "ASSAM"
  },
  {
    "sc": "BEDM",
    "en": "BEDHAM",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BMT",
    "en": "BEGAMPET",
    "ec": "SECUNDERABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "BGS",
    "en": "BEGU SARAI",
    "se": "BIHAR"
  },
  {
    "sc": "BPAE",
    "en": "BEGUMPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BYZA",
    "en": "BEGUNIA",
    "se": "ODISHA"
  },
  {
    "sc": "BEHJ",
    "en": "BEHAJ",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BEG",
    "en": "BEHTAGOKUL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHLA",
    "en": "BEHULA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BJN",
    "en": "BEJNAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BFR",
    "en": "BEKAL FORT",
    "se": "KERALA"
  },
  {
    "sc": "BELA",
    "en": "BELA",
    "se": "BIHAR"
  },
  {
    "sc": "BBHL",
    "en": "BELA BELA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BTX",
    "en": "BELA TAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BGM",
    "en": "BELAGAVI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BLGA",
    "en": "BELAGULA",
    "se": "KARNATAKA"
  },
  {
    "sc": "BLK",
    "en": "BELAKOBA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BZL",
    "en": "BELANAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BLRR",
    "en": "BELANDUR ROAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "BLNK",
    "en": "BELANKI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BAP",
    "en": "BELAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BEPR",
    "en": "BELAPUR CBD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BLSR",
    "en": "BELASAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BEX",
    "en": "BELBONI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BLDA",
    "en": "BELDA",
    "ec": "KHARAGPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BEB",
    "en": "BELDANGA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BQY",
    "en": "BELERHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BIG",
    "en": "BELGAHNA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BLH",
    "en": "BELGHARIA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BYL",
    "en": "BELHA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BGRD",
    "en": "BELIAGHATA ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BZC",
    "en": "BELIATOR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BELD",
    "en": "BELKHERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BMKD",
    "en": "BELLAMKONDA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BPA",
    "en": "BELLAMPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "BNHL",
    "en": "BELLENAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BMAE",
    "en": "BELMURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BENA",
    "en": "BELONIA",
    "se": "TRIPURA"
  },
  {
    "sc": "BPH",
    "en": "BELPAHAR",
    "ec": "JHARSUGUDA",
    "se": "ODISHA"
  },
  {
    "sc": "BXM",
    "en": "BELRAYAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BLRE",
    "en": "BELSIRI",
    "se": "ASSAM"
  },
  {
    "sc": "BLSN",
    "en": "BELSONDA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BLTR",
    "en": "BELTHARA ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BEQ",
    "en": "BELUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BWD",
    "en": "BELVANDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BEML",
    "en": "BEML NAGAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "BPE",
    "en": "BENAPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BFQ",
    "en": "BENDI",
    "se": "JHARKHAND"
  },
  {
    "sc": "BNC",
    "en": "BENGALURU CANT",
    "se": "KARNATAKA",
    "tg": "BANGALORE"
  },
  {
    "sc": "BNCE",
    "en": "BENGALURU EAST",
    "se": "KARNATAKA",
    "tg": "BANGALORE"
  },
  {
    "sc": "BEJ",
    "en": "BENIGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BENL",
    "en": "BENL",
    "se": "KARNATAKA"
  },
  {
    "sc": "BEHI",
    "en": "BENNEHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BNOD",
    "en": "BENODA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BEHR",
    "en": "BEOHARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRNA",
    "en": "BERAWANYA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BCH",
    "en": "BERCHHA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BPC",
    "en": "BERHAMPORE CRT",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BRDT",
    "en": "BERIA DAULAT",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "BRMO",
    "en": "BERMO",
    "se": "JHARKHAND"
  },
  {
    "sc": "BERO",
    "en": "BERO",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BSRL",
    "en": "BESROLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BMH",
    "en": "BETAMCHERLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BEW",
    "en": "BETAVAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BYXA",
    "en": "BETGARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BTPD",
    "en": "BETHAMPUDI JN",
    "se": "TELANGANA"
  },
  {
    "sc": "BTY",
    "en": "BETHUADAHARI",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BTQ",
    "en": "BETNOTI",
    "se": "ODISHA"
  },
  {
    "sc": "BTGH",
    "en": "BETTADNAGENHALI",
    "se": "KARNATAKA"
  },
  {
    "sc": "TLS",
    "en": "BETTAHALSOOR",
    "se": "KARNATAKA"
  },
  {
    "sc": "BTH",
    "en": "BETTIAH",
    "se": "BIHAR"
  },
  {
    "sc": "BZU",
    "en": "BETUL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BTRB",
    "en": "BETUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BVAR",
    "en": "BEVARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BNL",
    "en": "BEVINAHALU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BWBN",
    "en": "BEWAR BHOJAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BAH",
    "en": "BHABHAR",
    "se": "GUJARAT"
  },
  {
    "sc": "BFT",
    "en": "BHABTA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BBU",
    "en": "BHABUA ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "BCOB",
    "en": "BHACHAU BG",
    "se": "GUJARAT"
  },
  {
    "sc": "BBC",
    "en": "BHACHHBAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BDN",
    "en": "BHADAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BUU",
    "en": "BHADANPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BWH",
    "en": "BHADAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BVB",
    "en": "BHADBHADAGHAT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BBAI",
    "en": "BHADBHUNJA",
    "se": "GUJARAT"
  },
  {
    "sc": "BADR",
    "en": "BHADER",
    "se": "GUJARAT"
  },
  {
    "sc": "BDI",
    "en": "BHADLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BOY",
    "en": "BHADOHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BDCR",
    "en": "BHADRACHALAM RD",
    "se": "TELANGANA"
  },
  {
    "sc": "BHC",
    "en": "BHADRAK",
    "ec": "BHADRAK",
    "se": "ODISHA"
  },
  {
    "sc": "BDRN",
    "en": "BHADRAN",
    "se": "GUJARAT"
  },
  {
    "sc": "BDRI",
    "en": "BHADRAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BDRD",
    "en": "BHADRAVADI",
    "se": "GUJARAT"
  },
  {
    "sc": "BDVT",
    "en": "BHADRAVATI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BHR",
    "en": "BHADRESHWAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BHDR",
    "en": "BHADRI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBY",
    "en": "BHADROLI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BDKE",
    "en": "BHADSIVNI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BAWD",
    "en": "BHADWAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VAA",
    "en": "BHAGA JN",
    "se": "JHARKHAND"
  },
  {
    "sc": "BGP",
    "en": "BHAGALPUR",
    "ec": "BHAGALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "BGKT",
    "en": "BHAGAT KI KOTHI",
    "ec": "JODHPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BJM",
    "en": "BHAGAVATHIPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "BGR",
    "en": "BHAGDARA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BAGA",
    "en": "BHAGEGA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BHGP",
    "en": "BHAGIRATHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BSGR",
    "en": "BHAGSAR",
    "se": "PUNJAB"
  },
  {
    "sc": "BGTN",
    "en": "BHAGTANWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "BQG",
    "en": "BHAGWANGOLA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BNR",
    "en": "BHAGWANPUR",
    "se": "BIHAR"
  },
  {
    "sc": "BGDS",
    "en": "BHAGWANPUR DESU",
    "se": "BIHAR"
  },
  {
    "sc": "BGPR",
    "en": "BHAGWANPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BALI",
    "en": "BHAILI",
    "se": "GUJARAT"
  },
  {
    "sc": "BZK",
    "en": "BHAINI KHURD",
    "se": "HARYANA"
  },
  {
    "sc": "BSA",
    "en": "BHAINSA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BSBH",
    "en": "BHAINSBODH P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BASN",
    "en": "BHAINSWAN",
    "se": "HARYANA"
  },
  {
    "sc": "BHRB",
    "en": "BHAIRABI",
    "se": "MIZORAM"
  },
  {
    "sc": "BHGH",
    "en": "BHAIRGACHHI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BRU",
    "en": "BHAIROGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "BOG",
    "en": "BHAIRONGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BIF",
    "en": "BHAIRONPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BSAR",
    "en": "BHAIYASAR",
    "se": "GUJARAT"
  },
  {
    "sc": "BJRA",
    "en": "BHAJERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BKPT",
    "en": "BHAKARAPET",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BHKL",
    "en": "BHAKRAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BKNG",
    "en": "BHAKTI NAGAR",
    "ec": "RAJKOT",
    "se": "GUJARAT"
  },
  {
    "sc": "BAJ",
    "en": "BHALEJ",
    "se": "GUJARAT"
  },
  {
    "sc": "BHLK",
    "en": "BHALKI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BFM",
    "en": "BHALUI",
    "se": "BIHAR"
  },
  {
    "sc": "BKRD",
    "en": "BHALUKA ROAD F",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BLMR",
    "en": "BHALUKMARA",
    "se": "ASSAM"
  },
  {
    "sc": "BHNG",
    "en": "BHALUKPONG",
    "se": "ARUNACHAL PRADESH"
  },
  {
    "sc": "BUL",
    "en": "BHALULATA",
    "se": "ODISHA"
  },
  {
    "sc": "BLMK",
    "en": "BHALUMASKA",
    "se": "ODISHA"
  },
  {
    "sc": "BLNI",
    "en": "BHALWANI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BAK",
    "en": "BHAN KARI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BNP",
    "en": "BHANAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "VNN",
    "en": "BHANAUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHA",
    "en": "BHANDAI JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BUX",
    "en": "BHANDAK",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BRD",
    "en": "BHANDARA ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BHME",
    "en": "BHANDARIDAH",
    "se": "JHARKHAND"
  },
  {
    "sc": "BDKD",
    "en": "BHANDARKUND",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BFZ",
    "en": "BHANDARTIKURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BDGN",
    "en": "BHANDEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BHU",
    "en": "BHANDU MOTIDAU",
    "se": "GUJARAT"
  },
  {
    "sc": "BND",
    "en": "BHANDUP",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BNDR",
    "en": "BHANDURI",
    "se": "GUJARAT"
  },
  {
    "sc": "BANR",
    "en": "BHANER",
    "se": "GUJARAT"
  },
  {
    "sc": "BXG",
    "en": "BHANGA",
    "se": "ASSAM"
  },
  {
    "sc": "BNGL",
    "en": "BHANGALA",
    "se": "PUNJAB"
  },
  {
    "sc": "VZR",
    "en": "BHANJPUR",
    "se": "ODISHA"
  },
  {
    "sc": "BKD",
    "en": "BHANKODA",
    "se": "GUJARAT"
  },
  {
    "sc": "BHNS",
    "en": "BHANSI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BNLY",
    "en": "BHANUPLI",
    "se": "PUNJAB"
  },
  {
    "sc": "BPTP",
    "en": "BHANUPRATAPPUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BNVD",
    "en": "BHANVAD",
    "se": "GUJARAT"
  },
  {
    "sc": "BHTK",
    "en": "BHANWAR TONK",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BNWS",
    "en": "BHANWASA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BTKP",
    "en": "BHARAT KUP",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BARJ",
    "en": "BHARATGARH",
    "se": "PUNJAB"
  },
  {
    "sc": "BPZA",
    "en": "BHARATHAPUZHA",
    "se": "KERALA"
  },
  {
    "sc": "BTKD",
    "en": "BHARATKUND",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BTE",
    "en": "BHARATPUR JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BWRA",
    "en": "BHARATWADA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BRMR",
    "en": "BHARMAR",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "BHRL",
    "en": "BHAROLI",
    "se": "PUNJAB"
  },
  {
    "sc": "BPGJ",
    "en": "BHARPURA PGT JN",
    "se": "BIHAR"
  },
  {
    "sc": "BSDL",
    "en": "BHARSENDI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRTL",
    "en": "BHARTHALI",
    "se": "GUJARAT"
  },
  {
    "sc": "BNT",
    "en": "BHARTHANA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BH",
    "en": "BHARUCH JN",
    "se": "GUJARAT"
  },
  {
    "sc": "BZ",
    "en": "BHARUR",
    "se": "PUNJAB"
  },
  {
    "sc": "BSZ",
    "en": "BHARWA SUMERPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRE",
    "en": "BHARWARI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BSLA",
    "en": "BHASILA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BMM",
    "en": "BHASKARPARA",
    "se": "GUJARAT"
  },
  {
    "sc": "BYT",
    "en": "BHATAPARA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BTRH",
    "en": "BHATAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BHTS",
    "en": "BHATASA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHTL",
    "en": "BHATEL",
    "se": "GUJARAT"
  },
  {
    "sc": "BOV",
    "en": "BHATGAON",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BHAL",
    "en": "BHATIEL",
    "se": "GUJARAT"
  },
  {
    "sc": "BTIA",
    "en": "BHATINDA CBA",
    "se": "PUNJAB"
  },
  {
    "sc": "BTSD",
    "en": "BHATISUDA(HALT)",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BHTA",
    "en": "BHATIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "BTJL",
    "en": "BHATKAL",
    "ec": "KARWAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "BTT",
    "en": "BHATNI JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHG",
    "en": "BHATON KI GALI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BHTR",
    "en": "BHATPAR RANI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BTPR",
    "en": "BHATPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "BATS",
    "en": "BHATSAR",
    "se": "GUJARAT"
  },
  {
    "sc": "BQU",
    "en": "BHATTIPROLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BHT",
    "en": "BHATTU",
    "se": "HARYANA"
  },
  {
    "sc": "BPU",
    "en": "BHAUPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BVP",
    "en": "BHAVANAGAR PARA",
    "ec": "BHAVNAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "BVNR",
    "en": "BHAVANI NAGAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BOTR",
    "en": "BHAVDHARI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BVC",
    "en": "BHAVNAGAR TRMUS",
    "se": "GUJARAT"
  },
  {
    "sc": "BHVP",
    "en": "BHAVPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "BWM",
    "en": "BHAWANI MANDI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BWIP",
    "en": "BHAWANIPATNA",
    "se": "ODISHA"
  },
  {
    "sc": "BWP",
    "en": "BHAWANIPUR KALN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BCW",
    "en": "BHAWI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BYR",
    "en": "BHAYANDAR",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BHY",
    "en": "BHAYAVADAR",
    "se": "GUJARAT"
  },
  {
    "sc": "BHNA",
    "en": "BHAYNA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BDH",
    "en": "BHEDIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BXL",
    "en": "BHEDUASOL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BIPR",
    "en": "BHEEMPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BEP",
    "en": "BHEERPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHJA",
    "en": "BHEJA",
    "se": "ODISHA"
  },
  {
    "sc": "BLV",
    "en": "BHELWA",
    "se": "BIHAR"
  },
  {
    "sc": "BSWD",
    "en": "BHEMSWADI",
    "se": "GUJARAT"
  },
  {
    "sc": "BRGT",
    "en": "BHERAGHAT",
    "ec": "JABALPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BFY",
    "en": "BHESANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BSKN",
    "en": "BHESANA MANKNAJ",
    "se": "GUJARAT"
  },
  {
    "sc": "BILA",
    "en": "BHESLANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BHET",
    "en": "BHESTAN",
    "se": "GUJARAT"
  },
  {
    "sc": "VTG",
    "en": "BHETAGURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BETI",
    "en": "BHETASI",
    "se": "GUJARAT"
  },
  {
    "sc": "BGVN",
    "en": "BHIGWAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BKC",
    "en": "BHIKAMKOR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BKHP",
    "en": "BHIKHAMPUR"
  },
  {
    "sc": "BKF",
    "en": "BHIKHNA THORI",
    "se": "BIHAR"
  },
  {
    "sc": "BKU",
    "en": "BHIKNUR",
    "se": "TELANGANA"
  },
  {
    "sc": "BLD",
    "en": "BHILAD",
    "se": "GUJARAT"
  },
  {
    "sc": "BIA",
    "en": "BHILAI",
    "ec": "DURG",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BPHB",
    "en": "BHILAI PWR HS",
    "ec": "DURG",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BQR",
    "en": "BHILAINAGAR",
    "ec": "DURG",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BVQ",
    "en": "BHILAVDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BLDI",
    "en": "BHILDI",
    "se": "GUJARAT"
  },
  {
    "sc": "BHGN",
    "en": "BHILGAON",
    "se": "ASSAM"
  },
  {
    "sc": "BHL",
    "en": "BHILWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BMD",
    "en": "BHIMADOLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BIML",
    "en": "BHIMAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BMC",
    "en": "BHIMALGONDI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BMN",
    "en": "BHIMANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BMQ",
    "en": "BHIMARLAI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BMSR",
    "en": "BHIMASAR",
    "se": "GUJARAT"
  },
  {
    "sc": "BMSB",
    "en": "BHIMASAR BG",
    "se": "GUJARAT"
  },
  {
    "sc": "BVRM",
    "en": "BHIMAVARAM JN",
    "ec": "BHIMAVARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BVRT",
    "en": "BHIMAVARAM TOWN",
    "ec": "BHIMAVARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BMGA",
    "en": "BHIMGARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BMKJ",
    "en": "BHIMKHOJ",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BNH",
    "en": "BHIMNATH",
    "se": "GUJARAT"
  },
  {
    "sc": "BMRN",
    "en": "BHIMRANA",
    "se": "GUJARAT"
  },
  {
    "sc": "BZM",
    "en": "BHIMSEN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BIX",
    "en": "BHIND",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BNNR",
    "en": "BHINDAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BWA",
    "en": "BHINWALIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BIK",
    "en": "BHIRA KHERI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRI",
    "en": "BHIRINGI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BTO",
    "en": "BHITAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BYH",
    "en": "BHITI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHTN",
    "en": "BHITONI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BVS",
    "en": "BHIVPURI ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BIRD",
    "en": "BHIWANDI ROAD",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BNW",
    "en": "BHIWANI",
    "se": "HARYANA"
  },
  {
    "sc": "BNWC",
    "en": "BHIWANI CITY",
    "se": "HARYANA"
  },
  {
    "sc": "BWV",
    "en": "BHIWAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BDMJ",
    "en": "BHODWAL MAJRI",
    "se": "HARYANA"
  },
  {
    "sc": "BOP",
    "en": "BHOGPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BPRS",
    "en": "BHOGPUR SIRWAL",
    "se": "PUNJAB"
  },
  {
    "sc": "BHOJ",
    "en": "BHOJ PADRA",
    "se": "GUJARAT"
  },
  {
    "sc": "BOX",
    "en": "BHOJASAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BPR",
    "en": "BHOJIPURA JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BOJ",
    "en": "BHOJO",
    "se": "ASSAM"
  },
  {
    "sc": "BHAS",
    "en": "BHOJRAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BJE",
    "en": "BHOJUDIH JN",
    "se": "JHARKHAND"
  },
  {
    "sc": "BOKR",
    "en": "BHOKAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BOKE",
    "en": "BHOKE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BLME",
    "en": "BHOLIDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "BHV",
    "en": "BHOMA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BHNE",
    "en": "BHONE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BGQ",
    "en": "BHONGAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BG",
    "en": "BHONGIR",
    "se": "TELANGANA"
  },
  {
    "sc": "BPKA",
    "en": "BHOPALKA",
    "se": "GUJARAT"
  },
  {
    "sc": "BFPA",
    "en": "BHOPATPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BFJ",
    "en": "BHORAS BUDRUKH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BRTK",
    "en": "BHORTEX",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BHAN",
    "en": "BHOYANI",
    "se": "GUJARAT"
  },
  {
    "sc": "BON",
    "en": "BHOnra",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BHUA",
    "en": "BHUA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBSN",
    "en": "BHUBANESWAR NEW",
    "se": "ODISHA"
  },
  {
    "sc": "BCU",
    "en": "BHUCHCHU",
    "se": "PUNJAB"
  },
  {
    "sc": "BDHP",
    "en": "BHUDPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BPK",
    "en": "BHUGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BHUJ",
    "en": "BHUJ",
    "se": "GUJARAT"
  },
  {
    "sc": "BUJA",
    "en": "BHUJIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BKKA",
    "en": "BHUKARKA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BHLP",
    "en": "BHULANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHN",
    "en": "BHULI",
    "se": "JHARKHAND"
  },
  {
    "sc": "BLO",
    "en": "BHULON",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BSJ",
    "en": "BHUPALSAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BEF",
    "en": "BHUPDEOPUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "VPO",
    "en": "BHUPIA MAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BUGN",
    "en": "BHURJIHA BARAGN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHKD",
    "en": "BHURKUNDA",
    "se": "JHARKHAND"
  },
  {
    "sc": "BSDP",
    "en": "BHUSANDPUR",
    "se": "ODISHA"
  },
  {
    "sc": "BSL",
    "en": "BHUSAVAL JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BUBR",
    "en": "BHUTAKIA BHIMSA",
    "se": "GUJARAT"
  },
  {
    "sc": "BTSR",
    "en": "BHUTESHWAR",
    "ec": "MATHURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BHRH",
    "en": "BHUYAR P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BSPD",
    "en": "BIASPIND",
    "se": "PUNJAB"
  },
  {
    "sc": "BN",
    "en": "BIBINAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "BHPI",
    "en": "BICHHUPALI",
    "se": "ODISHA"
  },
  {
    "sc": "BIC",
    "en": "BICHIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BCP",
    "en": "BICHPURI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BID",
    "en": "BIDADI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BDNP",
    "en": "BIDANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BIDR",
    "en": "BIDAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "BNXR",
    "en": "BIDHAN NAGAR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BIDD",
    "en": "BIDIYAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BIGA",
    "en": "BIGGA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BGRM",
    "en": "BIGGABAS RAMSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BQP",
    "en": "BIGHAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BEHS",
    "en": "BIHAR SHARIF",
    "se": "BIHAR"
  },
  {
    "sc": "BHZ",
    "en": "BIHARA",
    "se": "ASSAM"
  },
  {
    "sc": "BHGJ",
    "en": "BIHARIGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "BEA",
    "en": "BIHIYA",
    "se": "BIHAR"
  },
  {
    "sc": "BTA",
    "en": "BIHTA",
    "se": "BIHAR"
  },
  {
    "sc": "BJNR",
    "en": "BIJAINAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BJPR",
    "en": "BIJAIPUR ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BJI",
    "en": "BIJAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BJV",
    "en": "BIJAURIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "VST",
    "en": "BIJAYSOTA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BJBA",
    "en": "BIJBIARA",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "BJF",
    "en": "BIJNI",
    "se": "ASSAM"
  },
  {
    "sc": "BJO",
    "en": "BIJNOR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BIJR",
    "en": "BIJOOR",
    "se": "KARNATAKA"
  },
  {
    "sc": "BJK",
    "en": "BIJORA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BJIH",
    "en": "BIJULI HALT",
    "se": "BIHAR"
  },
  {
    "sc": "BJRI",
    "en": "BIJURI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BWSN",
    "en": "BIJWASAN",
    "se": "DELHI"
  },
  {
    "sc": "BVL",
    "en": "BIKKAVOLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BKNO",
    "en": "BIKNA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BKSL",
    "en": "BIKRAM SHILA",
    "se": "BIHAR"
  },
  {
    "sc": "XBKJ",
    "en": "BIKRAMGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "BMR",
    "en": "BIKRAMPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BARA",
    "en": "BILARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BLPA",
    "en": "BILASIPARA",
    "se": "ASSAM"
  },
  {
    "sc": "BLQR",
    "en": "BILASPUR ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BILD",
    "en": "BILDI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BLWR",
    "en": "BILESHWAR",
    "se": "GUJARAT"
  },
  {
    "sc": "BZG",
    "en": "BILGA",
    "se": "PUNJAB"
  },
  {
    "sc": "BLG",
    "en": "BILHAR GHAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BLU",
    "en": "BILHAUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BIM",
    "en": "BILIMORA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "BILK",
    "en": "BILKHA",
    "se": "GUJARAT"
  },
  {
    "sc": "BXLL",
    "en": "BILLI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BFP",
    "en": "BILOCHPURA AGRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BLPU",
    "en": "BILPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BWI",
    "en": "BILWAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BMBE",
    "en": "BIMBARI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BINA",
    "en": "BINA JN",
    "ec": "BINA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MAKR",
    "en": "BINA MALKHEDI",
    "ec": "BINA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "VNK",
    "en": "BINAIKI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BNAR",
    "en": "BINAUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BUR",
    "en": "BINDAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BDYK",
    "en": "BINDAYAKA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BKO",
    "en": "BINDKI ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BNOI",
    "en": "BINDORI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BKTB",
    "en": "BINDUKURI",
    "se": "ASSAM"
  },
  {
    "sc": "BNGO",
    "en": "BINGAON",
    "se": "JHARKHAND"
  },
  {
    "sc": "BNJN",
    "en": "BINJANA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BNJL",
    "en": "BINJHOL",
    "se": "HARYANA"
  },
  {
    "sc": "BKIT",
    "en": "BINKADAKATTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BNV",
    "en": "BINNAGURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BIR",
    "en": "BIR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BSBP",
    "en": "BIR SHIBPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BIRA",
    "en": "BIRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BDWL",
    "en": "BIRADHWAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BRBL",
    "en": "BIRAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BAMA",
    "en": "BIRAMBAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BRMD",
    "en": "BIRAMDIH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BRSR",
    "en": "BIRANARSINGHPUR",
    "se": "ODISHA"
  },
  {
    "sc": "BMK",
    "en": "BIRANG KHERA",
    "se": "PUNJAB"
  },
  {
    "sc": "BRPT",
    "en": "BIRAPATTI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBT",
    "en": "BIRATI",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BRBS",
    "en": "BIRBANS",
    "se": "JHARKHAND"
  },
  {
    "sc": "BLNR",
    "en": "BIRLANAGAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRMP",
    "en": "BIRMITRAPUR",
    "se": "ODISHA"
  },
  {
    "sc": "BIJ",
    "en": "BIRNAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BEO",
    "en": "BIROHE",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRLY",
    "en": "BIROLIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BIB",
    "en": "BIRPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRST",
    "en": "BIRPUSHATTAMPUR",
    "se": "ODISHA"
  },
  {
    "sc": "BRS",
    "en": "BIRSINGHPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BRA",
    "en": "BIRSOLA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RRB",
    "en": "BIRUR JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "BLHI",
    "en": "BISALEHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BSUR",
    "en": "BISALPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BIWK",
    "en": "BISALWAS KALAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BSM",
    "en": "BISANATTAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "BRKH",
    "en": "BISAPURKALAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BLGH",
    "en": "BISHALGARH",
    "se": "TRIPURA"
  },
  {
    "sc": "BSPH",
    "en": "BISHANPUR HRYNA",
    "se": "HARYANA"
  },
  {
    "sc": "BISH",
    "en": "BISHENGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BEU",
    "en": "BISHESHWARGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "VSU",
    "en": "BISHNUPUR",
    "ec": "BISHNUPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BHRM",
    "en": "BISHRAMGANJ",
    "se": "TRIPURA"
  },
  {
    "sc": "BSPR",
    "en": "BISHRAMPUR",
    "ec": "AMBIKAPUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BSPK",
    "en": "BISPUR",
    "se": "ODISHA"
  },
  {
    "sc": "BZR",
    "en": "BISRA",
    "se": "ODISHA"
  },
  {
    "sc": "BMCK",
    "en": "BISSAMCUTTACK",
    "se": "ODISHA"
  },
  {
    "sc": "BUB",
    "en": "BISSAU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BGSF",
    "en": "BISUGIRSHARIF",
    "se": "TELANGANA"
  },
  {
    "sc": "BIS",
    "en": "BISWA BRIDGE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BVN",
    "en": "BISWAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BTHL",
    "en": "BITHAULI",
    "se": "BIHAR"
  },
  {
    "sc": "BTTR",
    "en": "BITRAGUNTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BTRI",
    "en": "BITROI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BW",
    "en": "BIWAI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BRRG",
    "en": "BIYAVRA RAJGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CYR",
    "en": "BMBY CHARNI RD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CCG",
    "en": "BMBY CHURCH GTE",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CRD",
    "en": "BMBY CURREY RD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GBO",
    "en": "BMBY GIRGAUM CB",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MMO",
    "en": "BMBY MAHIM CBO",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MM",
    "en": "BMBY MAHIM JN",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MEL",
    "en": "BMBY MARINE LNS",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MRU",
    "en": "BMBY MATUNGA RD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BOBS",
    "en": "BOBAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "VBL",
    "en": "BOBBILI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BCHN",
    "en": "BOCHASAN JN",
    "se": "GUJARAT"
  },
  {
    "sc": "BBW",
    "en": "BODARWAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BDVR",
    "en": "BODDAVARA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BDE",
    "en": "BODELI",
    "se": "GUJARAT"
  },
  {
    "sc": "BHBK",
    "en": "BODHADI BUJRUG",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BDHN",
    "en": "BODHAN",
    "se": "TELANGANA"
  },
  {
    "sc": "BDNK",
    "en": "BODINAYAKKANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "BDWD",
    "en": "BODWAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BVO",
    "en": "BOGOLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BGO",
    "en": "BOGRI ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BHLI",
    "en": "BOHALI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BNE",
    "en": "BOHANI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BONA",
    "en": "BOINDA",
    "se": "ODISHA"
  },
  {
    "sc": "BOR",
    "en": "BOISAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BJWS",
    "en": "BOJAWAS",
    "se": "HARYANA"
  },
  {
    "sc": "BXJ",
    "en": "BOKAJAN",
    "se": "ASSAM"
  },
  {
    "sc": "BKSC",
    "en": "BOKARO STL CITY",
    "ec": "BOKARO STEEL CITY",
    "se": "JHARKHAND"
  },
  {
    "sc": "BKRO",
    "en": "BOKARO THERMAL",
    "se": "JHARKHAND"
  },
  {
    "sc": "BORD",
    "en": "BOLAGARH ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "BLX",
    "en": "BOLAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BMO",
    "en": "BOLARUM",
    "se": "TELANGANA"
  },
  {
    "sc": "BOZ",
    "en": "BOLARUM BAZAR",
    "se": "TELANGANA"
  },
  {
    "sc": "BLC",
    "en": "BOLDA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BLND",
    "en": "BOLINNA DOABA",
    "se": "PUNJAB"
  },
  {
    "sc": "BHP",
    "en": "BOLPUR S NIKTN",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BLSA",
    "en": "BOLSA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BLWD",
    "en": "BOLWAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BOM",
    "en": "BOMADRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BCL",
    "en": "BOMBAY CNTRL L"
  },
  {
    "sc": "GLOB",
    "en": "BOMBAY GO CB",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PDGR",
    "en": "BOMBAY GR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GTR",
    "en": "BOMBAY GRNT RD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KCE",
    "en": "BOMBAY KC",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PL",
    "en": "BOMBAY L.PAREL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MSD",
    "en": "BOMBAY MASJID",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MTN",
    "en": "BOMBAY MATUNGA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PR",
    "en": "BOMBAY PAREL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RVJ",
    "en": "BOMBAY RAVLI JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RRD",
    "en": "BOMBAY REAY RD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SIN",
    "en": "BOMBAY SION",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SVE",
    "en": "BOMBY SEWRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BUM",
    "en": "BOMMASAMUDRAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BQI",
    "en": "BOMMIDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "BKL",
    "en": "BONA KALU",
    "se": "TELANGANA"
  },
  {
    "sc": "BNDM",
    "en": "BONDAMUNDA",
    "ec": "ROURKELA",
    "se": "ODISHA"
  },
  {
    "sc": "BNPL",
    "en": "BONDAPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BNGN",
    "en": "BONGAIGAON",
    "ec": "BONGAIGAON",
    "se": "ASSAM"
  },
  {
    "sc": "BDAG",
    "en": "BONIDANGA",
    "se": "JHARKHAND"
  },
  {
    "sc": "BXO",
    "en": "BOPARAI",
    "se": "PUNJAB"
  },
  {
    "sc": "BRKY",
    "en": "BORAKI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BOW",
    "en": "BORAWAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BXY",
    "en": "BORDHAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BIO",
    "en": "BORDI",
    "se": "GUJARAT"
  },
  {
    "sc": "BRRD",
    "en": "BORDI ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BDLN",
    "en": "BORDOLONI",
    "se": "ASSAM"
  },
  {
    "sc": "BDT",
    "en": "BORDUBI ROAD",
    "se": "ASSAM"
  },
  {
    "sc": "BGN",
    "en": "BORGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BFD",
    "en": "BORHAT",
    "se": "ASSAM"
  },
  {
    "sc": "BRB",
    "en": "BORIBIAL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BRND",
    "en": "BORIDAND",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BII",
    "en": "BORIDRA",
    "se": "GUJARAT"
  },
  {
    "sc": "BOK",
    "en": "BORKHEDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BOT",
    "en": "BOROTI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BGHU",
    "en": "BORRAGUHALLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BO",
    "en": "BORSAD",
    "se": "GUJARAT"
  },
  {
    "sc": "BTL",
    "en": "BORTALAO",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "BRVR",
    "en": "BORVIHIR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BTD",
    "en": "BOTAD JN",
    "se": "GUJARAT"
  },
  {
    "sc": "BOUH",
    "en": "BOUDH",
    "se": "ODISHA"
  },
  {
    "sc": "BWCN",
    "en": "BOWAICHANDI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BXHT",
    "en": "BOXIRHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "XXXX",
    "en": "BPT STATION"
  },
  {
    "sc": "BRJ",
    "en": "BRACE BRIDGE",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BJL",
    "en": "BRAHMAJAN",
    "se": "ASSAM"
  },
  {
    "sc": "BMGM",
    "en": "BRAHMANAGUDEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BMPL",
    "en": "BRAHMANPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "BMDI",
    "en": "BRAHMANWADA",
    "se": "GUJARAT"
  },
  {
    "sc": "BAM",
    "en": "BRAHMAPUR",
    "ec": "BRAHMAPUR",
    "se": "ODISHA"
  },
  {
    "sc": "BRT",
    "en": "BRAHMAVART",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BRJN",
    "en": "BRAJRAJNAGAR",
    "ec": "JHARSUGUDA",
    "se": "ODISHA"
  },
  {
    "sc": "BMP",
    "en": "BRAMHAPURI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BRSQ",
    "en": "BRAR SQUARE",
    "se": "DELHI"
  },
  {
    "sc": "BRLA",
    "en": "BRAYLA CHAURASI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BMJ",
    "en": "BRIDGMANGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BINR",
    "en": "BRIJ NAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BDPR",
    "en": "BRINDABANPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BXQ",
    "en": "BRUNDAMAL",
    "ec": "JHARSUGUDA",
    "se": "ODISHA"
  },
  {
    "sc": "BDGU",
    "en": "BUDAGUMPA",
    "se": "KARNATAKA"
  },
  {
    "sc": "BAL",
    "en": "BUDALUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "BEM",
    "en": "BUDAUN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BDY",
    "en": "BUDDIREDDIPPATI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "BDGM",
    "en": "BUDGAM",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "BPKH",
    "en": "BUDHA PUSHKAR H",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BKDE",
    "en": "BUDHAKHERA",
    "se": "HARYANA"
  },
  {
    "sc": "BDHY",
    "en": "BUDHI",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "BLZ",
    "en": "BUDHLADA",
    "se": "PUNJAB"
  },
  {
    "sc": "BDMA",
    "en": "BUDHMA",
    "se": "BIHAR"
  },
  {
    "sc": "BDSW",
    "en": "BUDHSINGHWALA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BNI",
    "en": "BUDNI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BDQ",
    "en": "BUDORA",
    "se": "JHARKHAND"
  },
  {
    "sc": "BDVL",
    "en": "BUDVEL",
    "se": "TELANGANA"
  },
  {
    "sc": "BFN",
    "en": "BUGANA",
    "se": "HARYANA"
  },
  {
    "sc": "BUGY",
    "en": "BUGIA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BUGL",
    "en": "BUGLANWALI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BSC",
    "en": "BULANDSHAHR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BBCE",
    "en": "BULBULCHANDI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BHX",
    "en": "BULLUANA",
    "se": "PUNJAB"
  },
  {
    "sc": "BUDI",
    "en": "BUNDI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "BEK",
    "en": "BUNDKI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BNDP",
    "en": "BUNIADPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BYKT",
    "en": "BURAKAYALAKOTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BWO",
    "en": "BURAMARA",
    "se": "ODISHA"
  },
  {
    "sc": "BRGL",
    "en": "BURGULA HALT",
    "se": "TELANGANA"
  },
  {
    "sc": "BAU",
    "en": "BURHANPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BDPK",
    "en": "BURHAPANKA",
    "se": "ODISHA"
  },
  {
    "sc": "BUH",
    "en": "BURHAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BUW",
    "en": "BURHWAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BJMA",
    "en": "BURJ MOHAR",
    "se": "PUNJAB"
  },
  {
    "sc": "BURN",
    "en": "BURNPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BTR",
    "en": "BUTARI",
    "se": "PUNJAB"
  },
  {
    "sc": "BWF",
    "en": "BUTEWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "BTBR",
    "en": "BUTI BORI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BXR",
    "en": "BUXAR",
    "se": "BIHAR"
  },
  {
    "sc": "SNRD",
    "en": "BY SANDHURST RD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BDRL",
    "en": "BYADARAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BYD",
    "en": "BYADGI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BFW",
    "en": "BYATRAYANHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "BY",
    "en": "BYCULLA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BYY",
    "en": "BYREE",
    "se": "ODISHA"
  },
  {
    "sc": "CBU",
    "en": "C BABUSAMUDRAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CRQ",
    "en": "C RLY QUOTA",
    "se": "BIHAR"
  },
  {
    "sc": "KOP",
    "en": "C SHAHUMHARAJ T",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CSTM",
    "en": "C SHIVAJI MAH T",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CM",
    "en": "CAMPIERGANJ",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CNO",
    "en": "CANCONA",
    "se": "GOA"
  },
  {
    "sc": "CS",
    "en": "CANNANORE SOUTH",
    "se": "KERALA"
  },
  {
    "sc": "CG",
    "en": "CANNING",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CSM",
    "en": "CANSAULIM",
    "se": "GOA"
  },
  {
    "sc": "CQS",
    "en": "CAPPER QUARRY",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CRLM",
    "en": "CARMELARAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "CRX",
    "en": "CARRON",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CLR",
    "en": "CASTLE ROCK",
    "se": "KARNATAKA"
  },
  {
    "sc": "CV",
    "en": "CAUVERY",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CVB",
    "en": "CAVALRY BARRCKS",
    "se": "TELANGANA"
  },
  {
    "sc": "CHB",
    "en": "CHABUA",
    "se": "ASSAM"
  },
  {
    "sc": "CBK",
    "en": "CHACHAURA BNGJ",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CHCR",
    "en": "CHACHER",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CDQ",
    "en": "CHADOTAR",
    "se": "GUJARAT"
  },
  {
    "sc": "CU",
    "en": "CHAGALLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CBSA",
    "en": "CHAIBASA",
    "ec": "RAJKHARSAWAN",
    "se": "JHARKHAND"
  },
  {
    "sc": "CNPR",
    "en": "CHAINPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "CW",
    "en": "CHAINWA",
    "se": "BIHAR"
  },
  {
    "sc": "CJW",
    "en": "CHAJAWA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CJL",
    "en": "CHAJLI",
    "se": "PUNJAB"
  },
  {
    "sc": "CKLA",
    "en": "CHAK BANWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "CKKN",
    "en": "CHAK KALAN",
    "se": "PUNJAB"
  },
  {
    "sc": "CKLT",
    "en": "CHAK KALI LAIT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CKA",
    "en": "CHAK PAKHHEWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "CRWL",
    "en": "CHAK RAKHWAL",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "CSR",
    "en": "CHAK SIKANDAR",
    "se": "BIHAR"
  },
  {
    "sc": "CKH",
    "en": "CHAKAND",
    "se": "BIHAR"
  },
  {
    "sc": "CHBT",
    "en": "CHAKARBHATA P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "CRDA",
    "en": "CHAKARDAHA HALT",
    "se": "BIHAR"
  },
  {
    "sc": "CPL",
    "en": "CHAKARLAPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CKK",
    "en": "CHAKARPUR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "CDH",
    "en": "CHAKDAHA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CKDL",
    "en": "CHAKDAYALA",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "CHK",
    "en": "CHAKERI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CAA",
    "en": "CHAKIA",
    "se": "BIHAR"
  },
  {
    "sc": "BTPH",
    "en": "CHAKIA T HALT",
    "se": "BIHAR"
  },
  {
    "sc": "CFG",
    "en": "CHAKITING",
    "se": "ASSAM"
  },
  {
    "sc": "CHKB",
    "en": "CHAKKI BANK",
    "ec": "PATHANKOT"
  },
  {
    "sc": "CKRD",
    "en": "CHAKMAKRAND",
    "se": "BIHAR"
  },
  {
    "sc": "CKYD",
    "en": "CHAKRA ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CKP",
    "en": "CHAKRADHARPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "CAJ",
    "en": "CHAKRAJ MAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CKOD",
    "en": "CHAKROD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CKS",
    "en": "CHAKSU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CKU",
    "en": "CHAKULIA",
    "ec": "JHARGRAM",
    "se": "JHARKHAND"
  },
  {
    "sc": "CKX",
    "en": "CHAKUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CKI",
    "en": "CHALAKUDI",
    "se": "KERALA"
  },
  {
    "sc": "CLC",
    "en": "CHALALA",
    "se": "GUJARAT"
  },
  {
    "sc": "CMZ",
    "en": "CHALAMA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CLI",
    "en": "CHALGERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "CSN",
    "en": "CHALISGAON JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CKW",
    "en": "CHALKHOA",
    "se": "ASSAM"
  },
  {
    "sc": "CHKE",
    "en": "CHALLAKERE",
    "se": "KARNATAKA"
  },
  {
    "sc": "CLPE",
    "en": "CHALLAVARIPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CLD",
    "en": "CHALSA JN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CHM",
    "en": "CHALTHAN",
    "se": "GUJARAT"
  },
  {
    "sc": "CMX",
    "en": "CHAMAGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CMK",
    "en": "CHAMAK",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CJR",
    "en": "CHAMARAJ",
    "se": "GUJARAT"
  },
  {
    "sc": "CMNR",
    "en": "CHAMARAJANAGAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "CMJ",
    "en": "CHAMARAJAPURAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "CPH",
    "en": "CHAMPA JN",
    "ec": "CHAMPA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "CHT",
    "en": "CHAMPAHATI",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CJQ",
    "en": "CHAMPAJHARAM",
    "se": "ODISHA"
  },
  {
    "sc": "CPN",
    "en": "CHAMPANER RD JN",
    "se": "GUJARAT"
  },
  {
    "sc": "CQR",
    "en": "CHAMPAPUKUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CHU",
    "en": "CHAMPION",
    "se": "KARNATAKA"
  },
  {
    "sc": "CHRU",
    "en": "CHAMRAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CMR",
    "en": "CHAMROLA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CAMU",
    "en": "CHAMUA",
    "se": "BIHAR"
  },
  {
    "sc": "CMMG",
    "en": "CHAMUNDA MARG",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "CNKP",
    "en": "CHANAKYAPURI",
    "se": "DELHI"
  },
  {
    "sc": "CSMA",
    "en": "CHANASMA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "CCL",
    "en": "CHANCHELAV",
    "se": "GUJARAT"
  },
  {
    "sc": "CBX",
    "en": "CHAND BHAN",
    "se": "PUNJAB"
  },
  {
    "sc": "CPS",
    "en": "CHAND SIAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CAF",
    "en": "CHANDA FORT",
    "ec": "BALHARSHAH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CGR",
    "en": "CHANDAN NAGAR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CTPE",
    "en": "CHANDANATTOP",
    "se": "KERALA"
  },
  {
    "sc": "CDAE",
    "en": "CHANDANPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CNR",
    "en": "CHANDAR",
    "se": "GOA"
  },
  {
    "sc": "CNBI",
    "en": "CHANDARI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CDV",
    "en": "CHANDARWA",
    "se": "GUJARAT"
  },
  {
    "sc": "CDMR",
    "en": "CHANDAULI MJHWR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CH",
    "en": "CHANDAUSI JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CNL",
    "en": "CHANDAWAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CDRA",
    "en": "CHANDERA",
    "se": "KERALA"
  },
  {
    "sc": "CNA",
    "en": "CHANDERIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CDMA",
    "en": "CHANDESHWAR STH",
    "se": "BIHAR"
  },
  {
    "sc": "CNDM",
    "en": "CHANDI MANDIR",
    "se": "HARYANA"
  },
  {
    "sc": "CHD",
    "en": "CHANDIA ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CIKR",
    "en": "CHANDIKHOLE RD",
    "se": "ODISHA"
  },
  {
    "sc": "CNI",
    "en": "CHANDIL JN",
    "ec": "TATANAGAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "CPE",
    "en": "CHANDIPOSI",
    "se": "ODISHA"
  },
  {
    "sc": "CDS",
    "en": "CHANDISAR",
    "se": "GUJARAT"
  },
  {
    "sc": "CDK",
    "en": "CHANDKHERA ROAD",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "CHBN",
    "en": "CHANDKHIRABAGAN",
    "se": "ASSAM"
  },
  {
    "sc": "CLDY",
    "en": "CHANDLODIYA",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "CDI",
    "en": "CHANDNI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CDD",
    "en": "CHANDOD",
    "se": "GUJARAT"
  },
  {
    "sc": "CNK",
    "en": "CHANDOK",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CDP",
    "en": "CHANDPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CGI",
    "en": "CHANDRAGIRI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CGKR",
    "en": "CHANDRAGIRI KOP",
    "se": "KARNATAKA"
  },
  {
    "sc": "CDGR",
    "en": "CHANDRAKONA RD",
    "ec": "SALBONI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CRPM",
    "en": "CHANDRAMPALEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CNE",
    "en": "CHANDRANATHPUR",
    "se": "ASSAM"
  },
  {
    "sc": "CD",
    "en": "CHANDRAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CRP",
    "en": "CHANDRAPURA JN",
    "ec": "BOKARO STEEL CITY",
    "se": "JHARKHAND"
  },
  {
    "sc": "CDSL",
    "en": "CHANDRESAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CXA",
    "en": "CHANDSARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CND",
    "en": "CHANDUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CNDB",
    "en": "CHANDUR BAZAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CHTI",
    "en": "CHANETI"
  },
  {
    "sc": "CGY",
    "en": "CHANGANASERI",
    "se": "KERALA"
  },
  {
    "sc": "CGLA",
    "en": "CHANGOTOLA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CBD",
    "en": "CHANGRABANDHA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CGS",
    "en": "CHANGSARI",
    "se": "ASSAM"
  },
  {
    "sc": "CHNN",
    "en": "CHANNANI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CPT",
    "en": "CHANNAPATNA",
    "se": "KARNATAKA"
  },
  {
    "sc": "CNPA",
    "en": "CHANNARAYAPATNA",
    "se": "KARNATAKA"
  },
  {
    "sc": "CX",
    "en": "CHANOL",
    "se": "GUJARAT"
  },
  {
    "sc": "CAI",
    "en": "CHANPATIA",
    "se": "BIHAR"
  },
  {
    "sc": "CHAA",
    "en": "CHAPAR",
    "se": "ASSAM"
  },
  {
    "sc": "CPK",
    "en": "CHAPARMUKH JN",
    "ec": "CHAPARMUKH",
    "se": "ASSAM"
  },
  {
    "sc": "CPQ",
    "en": "CHAPRAKATA",
    "se": "ASSAM"
  },
  {
    "sc": "CGF",
    "en": "CHARALI",
    "se": "ASSAM"
  },
  {
    "sc": "CJS",
    "en": "CHARAMULA KUSUM",
    "se": "ODISHA"
  },
  {
    "sc": "SMD",
    "en": "CHARANMAHADEVI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CRW",
    "en": "CHARAUD",
    "se": "HARYANA"
  },
  {
    "sc": "CBT",
    "en": "CHARBATIA",
    "se": "ODISHA"
  },
  {
    "sc": "CBG",
    "en": "CHARBHUJA ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CRN",
    "en": "CHAREGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CGX",
    "en": "CHARGOLA",
    "se": "ASSAM"
  },
  {
    "sc": "CRC",
    "en": "CHARKHARI ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CRK",
    "en": "CHARKHERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CKD",
    "en": "CHARKHI DADRI",
    "se": "HARYANA"
  },
  {
    "sc": "CHZ",
    "en": "CHARLAPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "CHAR",
    "en": "CHARMAL",
    "se": "ODISHA"
  },
  {
    "sc": "CHRD",
    "en": "CHARODIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "CHV",
    "en": "CHARVATTUR",
    "se": "KERALA"
  },
  {
    "sc": "CAS",
    "en": "CHAS ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CHJ",
    "en": "CHATA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CTHT",
    "en": "CHATAR HALT",
    "se": "BIHAR"
  },
  {
    "sc": "CTLI",
    "en": "CHATOULI",
    "se": "PUNJAB"
  },
  {
    "sc": "CTR",
    "en": "CHATRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CHPT",
    "en": "CHATRAPPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CAP",
    "en": "CHATRAPUR",
    "ec": "BRAHMAPUR",
    "se": "ODISHA"
  },
  {
    "sc": "CAPC",
    "en": "CHATRAPUR COURT",
    "se": "ODISHA"
  },
  {
    "sc": "CAT",
    "en": "CHATTAR HAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CTS",
    "en": "CHATTRIPUT",
    "se": "ODISHA"
  },
  {
    "sc": "CMU",
    "en": "CHAU MAHLA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CBH",
    "en": "CHAUBE",
    "se": "JHARKHAND"
  },
  {
    "sc": "CBR",
    "en": "CHAUBEPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CDB",
    "en": "CHAUDHRIBANDH",
    "se": "JHARKHAND"
  },
  {
    "sc": "CAZ",
    "en": "CHAUHANI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CHOK",
    "en": "CHAUK",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CHH",
    "en": "CHAUKHANDI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CKM",
    "en": "CHAUKI MAN",
    "se": "PUNJAB"
  },
  {
    "sc": "CNH",
    "en": "CHAUNRAH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CTZ",
    "en": "CHAUNTRA BHATER",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "CUX",
    "en": "CHAURA",
    "se": "BIHAR"
  },
  {
    "sc": "CAO",
    "en": "CHAURADANO",
    "se": "BIHAR"
  },
  {
    "sc": "CRKR",
    "en": "CHAURAKHERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CHBR",
    "en": "CHAURE BAZAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CC",
    "en": "CHAURI CHAURA",
    "ec": "DEORIA SADAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CSA",
    "en": "CHAUSA",
    "se": "BIHAR"
  },
  {
    "sc": "CROA",
    "en": "CHAUTARA",
    "se": "ASSAM"
  },
  {
    "sc": "CKB",
    "en": "CHAUTH KA BRWRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CVD",
    "en": "CHAVADIPALAIYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CVJ",
    "en": "CHAVAJ",
    "se": "GUJARAT"
  },
  {
    "sc": "CHLK",
    "en": "CHAVALKHEDE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CHA",
    "en": "CHAWAPALL",
    "se": "PUNJAB"
  },
  {
    "sc": "CGON",
    "en": "CHAYGAON",
    "se": "ASSAM"
  },
  {
    "sc": "CEL",
    "en": "CHEBROL",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CEME",
    "en": "CHEGRO",
    "se": "JHARKHAND"
  },
  {
    "sc": "CGTA",
    "en": "CHEGUNTA",
    "se": "TELANGANA"
  },
  {
    "sc": "CEM",
    "en": "CHEKATE G PALEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CMC",
    "en": "CHEMANCHERI",
    "se": "KERALA"
  },
  {
    "sc": "CMBR",
    "en": "CHEMBUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CGL",
    "en": "CHENGALPATTU JN",
    "ec": "KANCHIPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CNGR",
    "en": "CHENGANNUR",
    "se": "KERALA"
  },
  {
    "sc": "CGA",
    "en": "CHENGEL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MSB",
    "en": "CHENNAI BEACH",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MSC",
    "en": "CHENNAI CHETPAT",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MSF",
    "en": "CHENNAI FORT",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MPK",
    "en": "CHENNAI PARK",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CSDR",
    "en": "CHENNASANDRA",
    "se": "KARNATAKA"
  },
  {
    "sc": "COI",
    "en": "CHEOKI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CYN",
    "en": "CHERIYANAD",
    "se": "KERALA"
  },
  {
    "sc": "SRTL",
    "en": "CHERTHALA",
    "se": "KERALA"
  },
  {
    "sc": "CQA",
    "en": "CHERUKARA",
    "se": "KERALA"
  },
  {
    "sc": "CKV",
    "en": "CHERUKUVADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CVV",
    "en": "CHERUVU MADHWRM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CTQ",
    "en": "CHETAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "CTND",
    "en": "CHETTINAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CII",
    "en": "CHETTIYAPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CAG",
    "en": "CHHABRA GUGOR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CCHR",
    "en": "CHHACHHAR",
    "se": "GUJARAT"
  },
  {
    "sc": "CHDX",
    "en": "CHHADA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CHLR",
    "en": "CHHALESAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CHNR",
    "en": "CHHAN ARORIAN",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "CDRL",
    "en": "CHHANDRAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CAER",
    "en": "CHHANERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CASA",
    "en": "CHHANSARA",
    "se": "GUJARAT"
  },
  {
    "sc": "CHP",
    "en": "CHHAPI",
    "se": "GUJARAT"
  },
  {
    "sc": "CPR",
    "en": "CHHAPRA",
    "se": "BIHAR"
  },
  {
    "sc": "CI",
    "en": "CHHAPRA KACHERI",
    "ec": "CHHAPRA",
    "se": "BIHAR"
  },
  {
    "sc": "CKKD",
    "en": "CHHARKHERA KURD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CE",
    "en": "CHHARODI",
    "se": "GUJARAT"
  },
  {
    "sc": "CHRA",
    "en": "CHHARRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CATA",
    "en": "CHHATA ASCHAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CTJ",
    "en": "CHHATAINI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CTU",
    "en": "CHHATAPUR ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "CJN",
    "en": "CHHATNA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CTRL",
    "en": "CHHATRAL",
    "se": "GUJARAT"
  },
  {
    "sc": "CYI",
    "en": "CHHAYAPURI",
    "ec": "VADODARA",
    "se": "GUJARAT"
  },
  {
    "sc": "CIA",
    "en": "CHHEHARTA",
    "se": "PUNJAB"
  },
  {
    "sc": "CGO",
    "en": "CHHIDGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CHN",
    "en": "CHHINA",
    "se": "PUNJAB"
  },
  {
    "sc": "CWA",
    "en": "CHHINDWARA JN",
    "ec": "CHHINDWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CTW",
    "en": "CHHINTANWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "CPDR",
    "en": "CHHIPADOHAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "CAM",
    "en": "CHHOTA AMBANA",
    "se": "JHARKHAND"
  },
  {
    "sc": "COD",
    "en": "CHHOTA GUDHA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CTD",
    "en": "CHHOTA UDEPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "COO",
    "en": "CHHOTI ODAI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CCP",
    "en": "CHHUCHHAPURA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "CLF",
    "en": "CHHULHA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CNF",
    "en": "CHIANKI",
    "se": "JHARKHAND"
  },
  {
    "sc": "CCK",
    "en": "CHICHAKI",
    "se": "JHARKHAND"
  },
  {
    "sc": "CCO",
    "en": "CHICHOLI P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CCD",
    "en": "CHICHONDA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CIP",
    "en": "CHICHPALLI"
  },
  {
    "sc": "CASK",
    "en": "CHICKASHELIKERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "CDM",
    "en": "CHIDAMBARAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CCA",
    "en": "CHIGICHERLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CEU",
    "en": "CHIHERU",
    "se": "PUNJAB"
  },
  {
    "sc": "CBP",
    "en": "CHIK BALLAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "BAW",
    "en": "CHIK BANAVAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "CTH",
    "en": "CHIKALTHAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CKHS",
    "en": "CHIKHLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CIO",
    "en": "CHIKHLI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "CHLI",
    "en": "CHIKHLOLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JRU",
    "en": "CHIKJAJUR JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "CKBK",
    "en": "CHIKKABENAKAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "CMGR",
    "en": "CHIKKAMAGALURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "CKVD",
    "en": "CHIKKANDAWADI",
    "se": "KARNATAKA"
  },
  {
    "sc": "CKNA",
    "en": "CHIKNA",
    "se": "BIHAR"
  },
  {
    "sc": "CKNI",
    "en": "CHIKNI ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CKR",
    "en": "CHIKODI ROAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "CIK",
    "en": "CHIKSANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CK",
    "en": "CHIKSUGAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "CHLT",
    "en": "CHILAHATI"
  },
  {
    "sc": "CLU",
    "en": "CHILAKALAPUDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CIL",
    "en": "CHILBILA JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CIH",
    "en": "CHILHIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CLDR",
    "en": "CHILIKIDARA",
    "se": "ODISHA"
  },
  {
    "sc": "CLKA",
    "en": "CHILKA",
    "se": "ODISHA"
  },
  {
    "sc": "CHR",
    "en": "CHILKAHAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CLO",
    "en": "CHILO",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CLVR",
    "en": "CHILUVUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CLW",
    "en": "CHILWARIYA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CMW",
    "en": "CHIMALPAHAD",
    "se": "TELANGANA"
  },
  {
    "sc": "CMDP",
    "en": "CHIMIDIPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CNC",
    "en": "CHINCHLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "CPD",
    "en": "CHINCHPADA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CCH",
    "en": "CHINCHVAD",
    "ec": "PUNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CGV",
    "en": "CHINGAVANAM",
    "se": "KERALA"
  },
  {
    "sc": "CNHL",
    "en": "CHINK HILL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CJM",
    "en": "CHINNA GANJAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CHSM",
    "en": "CHINNA SALEM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CGHD",
    "en": "CHINNADAGUDIHDI",
    "se": "KARNATAKA"
  },
  {
    "sc": "CNKH",
    "en": "CHINNAKOTE HALT",
    "se": "KARNATAKA"
  },
  {
    "sc": "CIV",
    "en": "CHINNARAVURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CCI",
    "en": "CHINNEKUNTAPALI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CPLE",
    "en": "CHINPAI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CKN",
    "en": "CHINTA KANI",
    "se": "TELANGANA"
  },
  {
    "sc": "CLE",
    "en": "CHINTALPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "CNN",
    "en": "CHINTAMAN GANES",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CMY",
    "en": "CHINTAMANI",
    "se": "KARNATAKA"
  },
  {
    "sc": "CHMG",
    "en": "CHINTPURNI MARG",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "CHI",
    "en": "CHIPLUN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CPP",
    "en": "CHIPURUPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CHIB",
    "en": "CHIRAI BG",
    "se": "GUJARAT"
  },
  {
    "sc": "CID",
    "en": "CHIRAIDONGRI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CQL",
    "en": "CHIRAKKAL",
    "se": "KERALA"
  },
  {
    "sc": "CLX",
    "en": "CHIRALA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CRWA",
    "en": "CHIRAWA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CRY",
    "en": "CHIRAYINKEEZH",
    "se": "KERALA"
  },
  {
    "sc": "CGN",
    "en": "CHIRGAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CHRM",
    "en": "CHIRMIRI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "CBN",
    "en": "CHIT BARAGAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CTHR",
    "en": "CHITAHRA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CTL",
    "en": "CHITAL",
    "se": "GUJARAT"
  },
  {
    "sc": "CHLD",
    "en": "CHITALDA",
    "se": "GUJARAT"
  },
  {
    "sc": "CIT",
    "en": "CHITALI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CTF",
    "en": "CHITGIDDA",
    "se": "TELANGANA"
  },
  {
    "sc": "CHTT",
    "en": "CHITHARI HALT",
    "se": "KARNATAKA"
  },
  {
    "sc": "CTA",
    "en": "CHITRADURG",
    "se": "KARNATAKA"
  },
  {
    "sc": "CKTD",
    "en": "CHITRAKUTDHAM K",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CTTP",
    "en": "CHITRAPUR (H)",
    "se": "KARNATAKA"
  },
  {
    "sc": "CTT",
    "en": "CHITRASANI",
    "se": "GUJARAT"
  },
  {
    "sc": "CTRD",
    "en": "CHITRAWAD",
    "se": "GUJARAT"
  },
  {
    "sc": "COE",
    "en": "CHITROD",
    "se": "GUJARAT"
  },
  {
    "sc": "CT",
    "en": "CHITTAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "CRJ",
    "en": "CHITTARANJAN",
    "ec": "ASANSOL",
    "se": "JHARKHAND"
  },
  {
    "sc": "COR",
    "en": "CHITTAURGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CTRE",
    "en": "CHITTERI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CTO",
    "en": "CHITTOOR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CTYL",
    "en": "CHITYALA",
    "se": "TELANGANA"
  },
  {
    "sc": "CDL",
    "en": "CHODIALA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "CKE",
    "en": "CHOKI SORATH",
    "se": "GUJARAT"
  },
  {
    "sc": "CHL",
    "en": "CHOLA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CGH",
    "en": "CHOLANG",
    "se": "PUNJAB"
  },
  {
    "sc": "CPM",
    "en": "CHOLAPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "COM",
    "en": "CHOMUN SAMOD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CWI",
    "en": "CHONDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CJA",
    "en": "CHONGAJAN",
    "se": "ASSAM"
  },
  {
    "sc": "CPU",
    "en": "CHOPAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CRL",
    "en": "CHORAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CRND",
    "en": "CHORANDA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "CRE",
    "en": "CHORGHATPIPARIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CHRG",
    "en": "CHORGI",
    "se": "KARNATAKA"
  },
  {
    "sc": "CVR",
    "en": "CHORVAD ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "CTKT",
    "en": "CHOTI KHATU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CUE",
    "en": "CHOUPALE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CHUA",
    "en": "CHOURAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "CWR",
    "en": "CHOVVARA",
    "se": "KERALA"
  },
  {
    "sc": "CWT",
    "en": "CHOWHATTA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CKG",
    "en": "CHOWKA GHAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CWLE",
    "en": "CHOWRIGACHA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CMP",
    "en": "CHROMEPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CNS",
    "en": "CHUCHURA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CDA",
    "en": "CHUDA",
    "se": "GUJARAT"
  },
  {
    "sc": "CRU",
    "en": "CHUDAWA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CWDA",
    "en": "CHUHRIWALA DHAN",
    "se": "PUNJAB"
  },
  {
    "sc": "CUL",
    "en": "CHULI",
    "se": "GUJARAT"
  },
  {
    "sc": "CAR",
    "en": "CHUNAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CHF",
    "en": "CHUNNABHATTI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CBZ",
    "en": "CHURAIBARI",
    "se": "TRIPURA"
  },
  {
    "sc": "CRG",
    "en": "CHURAMAN NAGRI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CHTL",
    "en": "CHURARU TAKARLA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "CRV",
    "en": "CHUREB",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CUK",
    "en": "CHURK",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CUR",
    "en": "CHURU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CRA",
    "en": "CHURULIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CMA",
    "en": "CINNAMARA",
    "se": "ASSAM"
  },
  {
    "sc": "CBJ",
    "en": "CLUTTERBUCKGANJ",
    "ec": "BAREILLY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CHTS",
    "en": "COCHIN HRBR TMS",
    "ec": "KOCHI / ERNAKULAM",
    "se": "KERALA"
  },
  {
    "sc": "CBF",
    "en": "COIMBATORE NRTH",
    "ec": "COIMBATORE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "CLJ",
    "en": "COLONELGANJ",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CNT",
    "en": "CONTAI ROAD"
  },
  {
    "sc": "COB",
    "en": "COOCH BEHAR",
    "ec": "NEW COACHBEHAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ONR",
    "en": "COONOOR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "COL",
    "en": "CORAMANDAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "CSZ",
    "en": "COSSIMBAZAR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "CUPJ",
    "en": "CUDDALORE PORT",
    "ec": "CUDDALORE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "HX",
    "en": "CUDDAPAH JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CBM",
    "en": "CUMBUM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CTC",
    "en": "CUTTACK",
    "ec": "CUTTACK",
    "se": "ODISHA"
  },
  {
    "sc": "DWF",
    "en": "D SAGAR WTR FLS",
    "se": "GOA"
  },
  {
    "sc": "DSVS",
    "en": "D SAMUDHRAVALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "DBOU",
    "en": "DABHAU",
    "se": "GUJARAT"
  },
  {
    "sc": "DBR",
    "en": "DABHAURA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DBO",
    "en": "DABHODA",
    "se": "GUJARAT"
  },
  {
    "sc": "DB",
    "en": "DABHOI JN",
    "se": "GUJARAT"
  },
  {
    "sc": "DBV",
    "en": "DABILPUR",
    "se": "TELANGANA"
  },
  {
    "sc": "DQR",
    "en": "DABIRPURA",
    "se": "TELANGANA"
  },
  {
    "sc": "DBKA",
    "en": "DABKA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DBLA",
    "en": "DABLA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DBI",
    "en": "DABLI RATHAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DBM",
    "en": "DABOLIM",
    "se": "GOA"
  },
  {
    "sc": "DBF",
    "en": "DABPAL",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DBA",
    "en": "DABRA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DUB",
    "en": "DABTARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DDR",
    "en": "DADAR",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DDZ",
    "en": "DADGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DHM",
    "en": "DADHAL INAM",
    "se": "GUJARAT"
  },
  {
    "sc": "DPH",
    "en": "DADHAPARA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DDV",
    "en": "DADHDEVI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DPX",
    "en": "DADPUR",
    "se": "BIHAR"
  },
  {
    "sc": "DER",
    "en": "DADRI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DRHI",
    "en": "DAGARHKERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DAO",
    "en": "DAGHORA",
    "se": "ODISHA"
  },
  {
    "sc": "DAP",
    "en": "DAGMAGPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DGS",
    "en": "DAGORI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DAU",
    "en": "DAGRU",
    "se": "PUNJAB"
  },
  {
    "sc": "DRD",
    "en": "DAHANU ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DKBJ",
    "en": "DAHAR KA BALAJI",
    "ec": "JAIPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DAE",
    "en": "DAHEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DZB",
    "en": "DAHINA ZAINABAD",
    "se": "HARYANA"
  },
  {
    "sc": "DAC",
    "en": "DAHINSARA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "DIC",
    "en": "DAHISAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DHD",
    "en": "DAHOD",
    "se": "GUJARAT"
  },
  {
    "sc": "DWA",
    "en": "DAILWARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DHAE",
    "en": "DAINHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DKCH",
    "en": "DAKACHA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DKNT",
    "en": "DAKANIYA TALAV",
    "ec": "KOTA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DAKE",
    "en": "DAKHINESWAR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DK",
    "en": "DAKOR",
    "se": "GUJARAT"
  },
  {
    "sc": "DBT",
    "en": "DAKSHIN BARASAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DKDP",
    "en": "DAKSHIN DURGAPR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DCP",
    "en": "DAL CHAPRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DL",
    "en": "DALADI",
    "se": "GUJARAT"
  },
  {
    "sc": "DLF",
    "en": "DALAN",
    "se": "BIHAR"
  },
  {
    "sc": "DLD",
    "en": "DALAUDA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DVM",
    "en": "DALBHUMGARH",
    "se": "JHARKHAND"
  },
  {
    "sc": "DLDE",
    "en": "DALDALI",
    "se": "ASSAM"
  },
  {
    "sc": "DLQ",
    "en": "DALELNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DLO",
    "en": "DALGAON",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DAL",
    "en": "DALIGANJ",
    "ec": "LUCKNOW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DLX",
    "en": "DALIMGAON",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DLK",
    "en": "DALKOLHA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DRZ",
    "en": "DALLI RAJHARA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DMW",
    "en": "DALMAU JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DLC",
    "en": "DALMERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DPT",
    "en": "DALPAT SINGHPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DLP",
    "en": "DALPATPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DNU",
    "en": "DALSANUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "DSS",
    "en": "DALSINGH SARAI",
    "se": "BIHAR"
  },
  {
    "sc": "DTO",
    "en": "DALTONGANJ",
    "se": "JHARKHAND"
  },
  {
    "sc": "DDM",
    "en": "DAM DIM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DCU",
    "en": "DAMALCHERUVU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DMNJ",
    "en": "DAMANJODI",
    "se": "ODISHA"
  },
  {
    "sc": "DMCA",
    "en": "DAMARACHERLA",
    "se": "TELANGANA"
  },
  {
    "sc": "DCA",
    "en": "DAMCHERA",
    "se": "ASSAM"
  },
  {
    "sc": "DMLI",
    "en": "DAMLAI",
    "se": "GUJARAT"
  },
  {
    "sc": "DME",
    "en": "DAMNAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "DMA",
    "en": "DAMODAR JN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DMO",
    "en": "DAMOH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DNR",
    "en": "DANAPUR",
    "se": "BIHAR"
  },
  {
    "sc": "DPL",
    "en": "DANAULI PHLWRIA",
    "se": "BIHAR"
  },
  {
    "sc": "DED",
    "en": "DANDELI",
    "se": "KARNATAKA"
  },
  {
    "sc": "DNQ",
    "en": "DANDKHORA",
    "se": "BIHAR"
  },
  {
    "sc": "DNEA",
    "en": "DANEA",
    "se": "JHARKHAND"
  },
  {
    "sc": "DNGI",
    "en": "DANGARI",
    "se": "ASSAM"
  },
  {
    "sc": "DNW",
    "en": "DANGARWA",
    "se": "GUJARAT"
  },
  {
    "sc": "DGD",
    "en": "DANGIDHAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DPS",
    "en": "DANGOAPOSI",
    "se": "JHARKHAND"
  },
  {
    "sc": "DTX",
    "en": "DANGTAL",
    "se": "ASSAM"
  },
  {
    "sc": "DSPT",
    "en": "DANISHPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "DNWH",
    "en": "DANIYAWAN BZR H",
    "se": "BIHAR"
  },
  {
    "sc": "DKDE",
    "en": "DANKAUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DKAE",
    "en": "DANKUNI",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DNT",
    "en": "DANTAN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DWZ",
    "en": "DANTEWARA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DTF",
    "en": "DANTLA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DTRA",
    "en": "DANTRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DAR",
    "en": "DANWAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DJA",
    "en": "DAOTUHAJA",
    "se": "ASSAM"
  },
  {
    "sc": "DAPD",
    "en": "DAPODI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DHPR",
    "en": "DAPPAR",
    "se": "PUNJAB"
  },
  {
    "sc": "DPSR",
    "en": "DAPSAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DARA",
    "en": "DARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DRGJ",
    "en": "DARAGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DSM",
    "en": "DARASURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "DRV",
    "en": "DARAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DZP",
    "en": "DARAZPUR",
    "se": "HARYANA"
  },
  {
    "sc": "DBK",
    "en": "DARBARI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DBG",
    "en": "DARBHANGA JN",
    "se": "BIHAR"
  },
  {
    "sc": "DKS",
    "en": "DAREKASA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DAYG",
    "en": "DARIYAGANJ",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DJ",
    "en": "DARJEELING",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DPC",
    "en": "DARLIPUT",
    "se": "ODISHA"
  },
  {
    "sc": "DTL",
    "en": "DARRITOLA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DRG",
    "en": "DARSHANNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DWM",
    "en": "DARWHA M BGH JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DYD",
    "en": "DARYABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DRO",
    "en": "DARYAOGONJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DYP",
    "en": "DARYAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DTD",
    "en": "DASALWADA A RD",
    "se": "GUJARAT"
  },
  {
    "sc": "DST",
    "en": "DASAMPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "DSME",
    "en": "DASARA",
    "se": "JHARKHAND"
  },
  {
    "sc": "DRTP",
    "en": "DASHARATHPUR",
    "se": "BIHAR"
  },
  {
    "sc": "DSNR",
    "en": "DASHNAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DLM",
    "en": "DASKALGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DS",
    "en": "DASNA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DSPL",
    "en": "DASPALLA",
    "se": "ODISHA"
  },
  {
    "sc": "DZA",
    "en": "DASUYA",
    "ec": "JALANDHAR",
    "se": "PUNJAB"
  },
  {
    "sc": "DTW",
    "en": "DATEWAS",
    "se": "PUNJAB"
  },
  {
    "sc": "DAA",
    "en": "DATIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DTVL",
    "en": "DATIVLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DTK",
    "en": "DATTAPUKUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DAQ",
    "en": "DAUD KHAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DDP",
    "en": "DAUDPUR",
    "se": "BIHAR"
  },
  {
    "sc": "DQV",
    "en": "DAULA KOT BHAI",
    "se": "PUNJAB"
  },
  {
    "sc": "DLB",
    "en": "DAULATABAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DLPC",
    "en": "DAULATPUR CHAUK",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "DLPH",
    "en": "DAULATPUR HAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DULP",
    "en": "DAULATPUR HRYNA",
    "se": "HARYANA"
  },
  {
    "sc": "DOC",
    "en": "DAUN KALAN",
    "se": "PUNJAB"
  },
  {
    "sc": "DDCC",
    "en": "DAUND CHORD LIN",
    "ec": "DAUND",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DD",
    "en": "DAUND JN",
    "ec": "DAUND",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DNJ",
    "en": "DAUNDAJ",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DOZ",
    "en": "DAURAI",
    "ec": "AJMER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DRLA",
    "en": "DAURALA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DMH",
    "en": "DAURAM MADHPURA",
    "se": "BIHAR"
  },
  {
    "sc": "DO",
    "en": "DAUSA JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DSNI",
    "en": "DAUSNI",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "DVG",
    "en": "DAVANGERE",
    "se": "KARNATAKA"
  },
  {
    "sc": "DOW",
    "en": "DAVOL",
    "se": "GUJARAT"
  },
  {
    "sc": "DBSI",
    "en": "DAYABASTI",
    "se": "DELHI"
  },
  {
    "sc": "DAY",
    "en": "DAYADARA",
    "se": "GUJARAT"
  },
  {
    "sc": "DLPR",
    "en": "DAYALPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DYE",
    "en": "DAYANAND NAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "DEB",
    "en": "DEBAGRAM",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DRB",
    "en": "DEBARI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DBP",
    "en": "DEBIPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DDWA",
    "en": "DEEDWANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DEEG",
    "en": "DEEG",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DDDM",
    "en": "DEEN DAYAL DHAM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DEPI",
    "en": "DEENAPATTI",
    "se": "BIHAR"
  },
  {
    "sc": "DF",
    "en": "DEFENCE OS QT"
  },
  {
    "sc": "DNA",
    "en": "DEGANA JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DDN",
    "en": "DEHRADUN",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "DOS",
    "en": "DEHRI ON SONE",
    "se": "BIHAR"
  },
  {
    "sc": "DEHR",
    "en": "DEHU ROAD",
    "ec": "PUNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DKGN",
    "en": "DEKARGAON",
    "ec": "DEKARGAON",
    "se": "ASSAM"
  },
  {
    "sc": "DEG",
    "en": "DELANG",
    "ec": "PURI",
    "se": "ODISHA"
  },
  {
    "sc": "DAZ",
    "en": "DELHI AZADPUR",
    "se": "DELHI"
  },
  {
    "sc": "DEC",
    "en": "DELHI CANTT",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "DKZ",
    "en": "DELHI KISHANGNJ",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "DSJ",
    "en": "DELHI SAFDARJNG",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "DSA",
    "en": "DELHI SHAHDARA",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "DVA",
    "en": "DELVADA",
    "se": "GUJARAT"
  },
  {
    "sc": "DEMU",
    "en": "DEMU",
    "se": "JHARKHAND"
  },
  {
    "sc": "DEL",
    "en": "DENDULURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DBD",
    "en": "DEOBAND",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DFR",
    "en": "DEOGAN ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "DGHR",
    "en": "DEOGHAR",
    "ec": "JASIDIH & ASANSOL",
    "se": "JHARKHAND"
  },
  {
    "sc": "DJHR",
    "en": "DEOJHAR",
    "se": "ODISHA"
  },
  {
    "sc": "DEO",
    "en": "DEOKALI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DNH",
    "en": "DEONAGAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "DRBR",
    "en": "DEORAHA BABA RD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DELO",
    "en": "DEORAKOT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DRN",
    "en": "DEORANIAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DOE",
    "en": "DEORI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DEOS",
    "en": "DEORIA SADAR",
    "ec": "DEORIA SADAR / KUSHINAGR / KASIYA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DOTL",
    "en": "DEOTALA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DEP",
    "en": "DEPALSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DPUR",
    "en": "DEPUR PH",
    "se": "ODISHA"
  },
  {
    "sc": "DBNK",
    "en": "DERABABA NANAK",
    "se": "PUNJAB"
  },
  {
    "sc": "DRL",
    "en": "DEROL",
    "se": "GUJARAT"
  },
  {
    "sc": "DRWN",
    "en": "DEROWAN P. H.",
    "se": "JHARKHAND"
  },
  {
    "sc": "DSX",
    "en": "DESANG",
    "se": "ASSAM"
  },
  {
    "sc": "DSRD",
    "en": "DESAR ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "DES",
    "en": "DESARI",
    "se": "BIHAR"
  },
  {
    "sc": "DSLP",
    "en": "DESHALPAR",
    "se": "GUJARAT"
  },
  {
    "sc": "DSPN",
    "en": "DESHAPRAN P.H.",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DSO",
    "en": "DESHNOK",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DUR",
    "en": "DESUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "DSL",
    "en": "DESWAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DET",
    "en": "DET",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DHLI",
    "en": "DETHLI",
    "se": "GUJARAT"
  },
  {
    "sc": "DTJ",
    "en": "DETROJ",
    "se": "GUJARAT"
  },
  {
    "sc": "D",
    "en": "DEULA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DTE",
    "en": "DEULTI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DKO",
    "en": "DEVAKOTTAI ROAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "DAV",
    "en": "DEVALGAON AUCHR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DVY",
    "en": "DEVALIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "DHL",
    "en": "DEVANAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "DKN",
    "en": "DEVANGONTHI",
    "se": "KARNATAKA"
  },
  {
    "sc": "VNR",
    "en": "DEVANUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "DPE",
    "en": "DEVARAPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DEV",
    "en": "DEVARAYI",
    "se": "KARNATAKA"
  },
  {
    "sc": "DAD",
    "en": "DEVARGUDDA",
    "se": "KARNATAKA"
  },
  {
    "sc": "DKC",
    "en": "DEVARKADRA JN",
    "se": "TELANGANA"
  },
  {
    "sc": "DBEC",
    "en": "DEVBALODA CHRDA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DVGM",
    "en": "DEVGAM",
    "se": "GUJARAT"
  },
  {
    "sc": "DOHM",
    "en": "DEVGARH MADRIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DVH",
    "en": "DEVI HALT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DGZ",
    "en": "DEVIGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "DVL",
    "en": "DEVLALI",
    "ec": "NASHIK",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DPZ",
    "en": "DEVPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DRPH",
    "en": "DEVRI P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DEU",
    "en": "DEVSANA",
    "se": "GUJARAT"
  },
  {
    "sc": "DVN",
    "en": "DEVTHANA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DEWA",
    "en": "DEWA",
    "se": "GUJARAT"
  },
  {
    "sc": "DEW",
    "en": "DEWALGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DWT",
    "en": "DEWAN HAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DWG",
    "en": "DEWANGANJ",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DWX",
    "en": "DEWAS",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DABN",
    "en": "DHABAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DBN",
    "en": "DHABLAN",
    "se": "PUNJAB"
  },
  {
    "sc": "DHCZ",
    "en": "DHACA RETURN"
  },
  {
    "sc": "DGF",
    "en": "DHAGARIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DAKA",
    "en": "DHAKA"
  },
  {
    "sc": "DACT",
    "en": "DHAKA CANTT"
  },
  {
    "sc": "DOT",
    "en": "DHAKIA TIWARI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DHK",
    "en": "DHAKURIA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DQL",
    "en": "DHALAIBIL",
    "se": "ASSAM"
  },
  {
    "sc": "DLGN",
    "en": "DHALGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DHRY",
    "en": "DHALPUKHURI",
    "se": "ASSAM"
  },
  {
    "sc": "DMGN",
    "en": "DHAMALGAON",
    "se": "ASSAM"
  },
  {
    "sc": "DMN",
    "en": "DHAMANGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DHT",
    "en": "DHAMARA GHAT",
    "se": "BIHAR"
  },
  {
    "sc": "DHMA",
    "en": "DHAMARDA",
    "se": "GUJARAT"
  },
  {
    "sc": "DDX",
    "en": "DHAMDHAMIA",
    "se": "JHARKHAND"
  },
  {
    "sc": "DNE",
    "en": "DHAMNI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DAM",
    "en": "DHAMORA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DPR",
    "en": "DHAMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DTN",
    "en": "DHAMTAN SAHIB",
    "se": "HARYANA"
  },
  {
    "sc": "DTR",
    "en": "DHAMTARI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DMU",
    "en": "DHAMUA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DXK",
    "en": "DHANA KHERLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DZL",
    "en": "DHANA LADANPUR",
    "se": "HARYANA"
  },
  {
    "sc": "DKW",
    "en": "DHANAKWADA",
    "se": "GUJARAT"
  },
  {
    "sc": "DNK",
    "en": "DHANAKYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DHNL",
    "en": "DHANALA",
    "se": "GUJARAT"
  },
  {
    "sc": "DIR",
    "en": "DHANAPUR ORISSA",
    "se": "ODISHA"
  },
  {
    "sc": "DN",
    "en": "DHANARI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DNRE",
    "en": "DHANAURI",
    "se": "BIHAR"
  },
  {
    "sc": "DHVR",
    "en": "DHANAWALA WADA",
    "se": "GUJARAT"
  },
  {
    "sc": "DHN",
    "en": "DHANBAD JN",
    "se": "JHARKHAND"
  },
  {
    "sc": "DDL",
    "en": "DHANDARI KALAN",
    "ec": "LUDHIANA",
    "se": "PUNJAB"
  },
  {
    "sc": "DNRA",
    "en": "DHANDHERA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "DCK",
    "en": "DHANDHUKA",
    "se": "GUJARAT"
  },
  {
    "sc": "DQN",
    "en": "DHANERA",
    "se": "GUJARAT"
  },
  {
    "sc": "DAN",
    "en": "DHANETA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DAG",
    "en": "DHANG",
    "se": "BIHAR"
  },
  {
    "sc": "DKQ",
    "en": "DHANI KASAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DCX",
    "en": "DHANICHHA",
    "se": "BIHAR"
  },
  {
    "sc": "DNM",
    "en": "DHANMANDAL",
    "se": "ODISHA"
  },
  {
    "sc": "DNL",
    "en": "DHANOLI P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DHNR",
    "en": "DHANORA DECCAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DNZ",
    "en": "DHANORI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DNPR",
    "en": "DHANPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "DQS",
    "en": "DHANSAR"
  },
  {
    "sc": "DIM",
    "en": "DHANSIMLA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DSR",
    "en": "DHANSIRI",
    "se": "ASSAM"
  },
  {
    "sc": "DSPR",
    "en": "DHANSIRIPAR",
    "se": "NAGALAND"
  },
  {
    "sc": "DNX",
    "en": "DHANSU",
    "se": "HARYANA"
  },
  {
    "sc": "DAVM",
    "en": "DHANUVACHAPURAM",
    "se": "KERALA"
  },
  {
    "sc": "DNWR",
    "en": "DHANWAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "DPDP",
    "en": "DHAPDHAPI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DPW",
    "en": "DHAPEWARA P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DHQ",
    "en": "DHARAKHOH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DMPR",
    "en": "DHARAMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DML",
    "en": "DHARAMTUL",
    "se": "ASSAM"
  },
  {
    "sc": "DXG",
    "en": "DHARANGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DRSV",
    "en": "DHARASHIV",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DRS",
    "en": "DHARESHWAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DRW",
    "en": "DHAREWADA",
    "se": "GUJARAT"
  },
  {
    "sc": "DRH",
    "en": "DHARHARA",
    "ec": "JAMALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "DARI",
    "en": "DHARI JN",
    "se": "GUJARAT"
  },
  {
    "sc": "DHW",
    "en": "DHARIWAL",
    "se": "PUNJAB"
  },
  {
    "sc": "DAB",
    "en": "DHARMABAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DMD",
    "en": "DHARMADAM",
    "se": "KERALA"
  },
  {
    "sc": "DMJ",
    "en": "DHARMAJ",
    "se": "GUJARAT"
  },
  {
    "sc": "DMR",
    "en": "DHARMANAGAR",
    "se": "TRIPURA"
  },
  {
    "sc": "DPJ",
    "en": "DHARMAPURI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "DMM",
    "en": "DHARMAVARAM JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DRQ",
    "en": "DHARMINIYA",
    "se": "BIHAR"
  },
  {
    "sc": "DKI",
    "en": "DHARMKUNDI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DMP",
    "en": "DHARMPUR HMCHL",
    "ec": "KALKA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "DHR",
    "en": "DHARNAODA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DHY",
    "en": "DHARODI",
    "se": "HARYANA"
  },
  {
    "sc": "DIH",
    "en": "DHARUADIHI",
    "se": "ODISHA"
  },
  {
    "sc": "DRR",
    "en": "DHARUR",
    "se": "TELANGANA"
  },
  {
    "sc": "DWR",
    "en": "DHARWAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "DAS",
    "en": "DHASA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "DHAT",
    "en": "DHAT",
    "se": "PUNJAB"
  },
  {
    "sc": "DTAE",
    "en": "DHATRIGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DLMH",
    "en": "DHAULIMUHAN",
    "se": "ODISHA"
  },
  {
    "sc": "DHO",
    "en": "DHAULPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DWLE",
    "en": "DHAUNI",
    "se": "BIHAR"
  },
  {
    "sc": "DUA",
    "en": "DHAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DUM",
    "en": "DHAURMUI JAGHNA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DUO",
    "en": "DHAURSALAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DHS",
    "en": "DHAVALAS",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DHA",
    "en": "DHEENA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DKJR",
    "en": "DHEKIAJULI ROAD",
    "se": "ASSAM"
  },
  {
    "sc": "DWD",
    "en": "DHEKVAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DMC",
    "en": "DHEMAJI",
    "se": "ASSAM"
  },
  {
    "sc": "DGPP",
    "en": "DHENGLI PP GOAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DNKL",
    "en": "DHENKANAL",
    "se": "ODISHA"
  },
  {
    "sc": "DGW",
    "en": "DHIGAWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DIW",
    "en": "DHILWAN",
    "se": "PUNJAB"
  },
  {
    "sc": "DMSR",
    "en": "DHIMSIRI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DHND",
    "en": "DHINDA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DNHK",
    "en": "DHINDHORA HKMKD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DDK",
    "en": "DHINDSA",
    "se": "PUNJAB"
  },
  {
    "sc": "DHJ",
    "en": "DHINOJ",
    "se": "GUJARAT"
  },
  {
    "sc": "DHRR",
    "en": "DHIRERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DHRJ",
    "en": "DHIRGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DPP",
    "en": "DHIRPUR",
    "se": "HARYANA"
  },
  {
    "sc": "DHKR",
    "en": "DHODA KHEDI",
    "se": "HARYANA"
  },
  {
    "sc": "DOD",
    "en": "DHODHAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DOH",
    "en": "DHODRA MOHAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DRE",
    "en": "DHOGRI",
    "se": "PUNJAB"
  },
  {
    "sc": "DKY",
    "en": "DHOKI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DLJ",
    "en": "DHOLA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "DHMZ",
    "en": "DHOLA MAZRA",
    "se": "HARYANA"
  },
  {
    "sc": "DLZ",
    "en": "DHOLBAZA",
    "se": "BIHAR"
  },
  {
    "sc": "DOL",
    "en": "DHOLI",
    "se": "BIHAR"
  },
  {
    "sc": "DOLK",
    "en": "DHOLIKUA",
    "se": "GUJARAT"
  },
  {
    "sc": "DPK",
    "en": "DHOLIPAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DOK",
    "en": "DHOLKA",
    "se": "GUJARAT"
  },
  {
    "sc": "DDD",
    "en": "DHONDHA DIH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DNDI",
    "en": "DHONDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DHNE",
    "en": "DHONE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DJI",
    "en": "DHORAJI",
    "se": "GUJARAT"
  },
  {
    "sc": "DHG",
    "en": "DHRANGDHRA",
    "se": "GUJARAT"
  },
  {
    "sc": "DRMT",
    "en": "DHRUMATH",
    "se": "GUJARAT"
  },
  {
    "sc": "DKRA",
    "en": "DHUANKHERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DBB",
    "en": "DHUBRI",
    "se": "ASSAM"
  },
  {
    "sc": "DHU",
    "en": "DHUBULIA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DBQ",
    "en": "DHULABARI",
    "se": "BIHAR"
  },
  {
    "sc": "DHI",
    "en": "DHULE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DGT",
    "en": "DHULGHAT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DGLE",
    "en": "DHULIAN GANGA",
    "ec": "MALDA TOWN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DUP",
    "en": "DHULIPALLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DKT",
    "en": "DHULKOT",
    "se": "HARYANA"
  },
  {
    "sc": "DQG",
    "en": "DHUPGURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DHRN",
    "en": "DHURANA",
    "se": "HARYANA"
  },
  {
    "sc": "DUI",
    "en": "DHURI JN",
    "se": "PUNJAB"
  },
  {
    "sc": "DRSN",
    "en": "DHURWASIN P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DTV",
    "en": "DHUTRA",
    "se": "ODISHA"
  },
  {
    "sc": "DV",
    "en": "DHUVA",
    "se": "GUJARAT"
  },
  {
    "sc": "DWL",
    "en": "DHUWALA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DH",
    "en": "DIAMOND HARBOUR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DIB",
    "en": "DIBAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DBNR",
    "en": "DIBNAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DBLG",
    "en": "DIBOLONG",
    "se": "ASSAM"
  },
  {
    "sc": "DBRG",
    "en": "DIBRUGARH",
    "se": "ASSAM"
  },
  {
    "sc": "DBRT",
    "en": "DIBRUGARH TOWN",
    "se": "ASSAM"
  },
  {
    "sc": "DHP",
    "en": "DICHPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "DJD",
    "en": "DIDARGANJ ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DIA",
    "en": "DIDWANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DGU",
    "en": "DIGARU",
    "se": "ASSAM"
  },
  {
    "sc": "DBY",
    "en": "DIGBOI",
    "se": "ASSAM"
  },
  {
    "sc": "DGHA",
    "en": "DIGHA",
    "ec": "DIGHA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DGBH",
    "en": "DIGHA BRIDGE H",
    "se": "BIHAR"
  },
  {
    "sc": "DGY",
    "en": "DIGHORI BUZURG",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DWDI",
    "en": "DIGHWA DUBAULI",
    "se": "BIHAR"
  },
  {
    "sc": "DGA",
    "en": "DIGHWARA",
    "se": "BIHAR"
  },
  {
    "sc": "DTG",
    "en": "DIGNAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DXD",
    "en": "DIGOD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DXR",
    "en": "DIGSAR",
    "se": "GUJARAT"
  },
  {
    "sc": "DMT",
    "en": "DIGUVAMETTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DKE",
    "en": "DIHAKHO",
    "se": "ASSAM"
  },
  {
    "sc": "DJB",
    "en": "DIJAOBRA",
    "se": "ASSAM"
  },
  {
    "sc": "DKM",
    "en": "DIKOM",
    "se": "ASSAM"
  },
  {
    "sc": "DIL",
    "en": "DILAWARNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DLN",
    "en": "DILDARNAGAR JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DVJ",
    "en": "DILLIDEWANGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "DMK",
    "en": "DILMILI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DLW",
    "en": "DILWA",
    "ec": "BANARAS",
    "se": "BIHAR"
  },
  {
    "sc": "DMV",
    "en": "DIMAPUR",
    "se": "NAGALAND"
  },
  {
    "sc": "DNN",
    "en": "DINA NAGAR",
    "se": "PUNJAB"
  },
  {
    "sc": "DIQ",
    "en": "DINAGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DG",
    "en": "DINDIGUL JN",
    "ec": "KODAIKANAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "DGB",
    "en": "DINDU G PURAM H",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DING",
    "en": "DING",
    "se": "HARYANA"
  },
  {
    "sc": "DWI",
    "en": "DINGWAHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DHH",
    "en": "DINHATA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DCH",
    "en": "DINHATTA CLGE H",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DKGS",
    "en": "DINKAR GRAM SIM",
    "se": "BIHAR"
  },
  {
    "sc": "DPU",
    "en": "DIPHU",
    "se": "ASSAM"
  },
  {
    "sc": "DPLN",
    "en": "DIPLANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DIP",
    "en": "DIPORE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DISA",
    "en": "DISA",
    "se": "GUJARAT"
  },
  {
    "sc": "DTC",
    "en": "DITOKCHERRA",
    "se": "ASSAM"
  },
  {
    "sc": "DIVA",
    "en": "DIVA",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DINR",
    "en": "DIVINE NAGAR",
    "se": "KERALA"
  },
  {
    "sc": "DTP",
    "en": "DIVITI PALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "DWNA",
    "en": "DIWANA",
    "se": "HARYANA"
  },
  {
    "sc": "DWV",
    "en": "DIWANKHAVATI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DTRD",
    "en": "DIYATARA ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DYW",
    "en": "DIYAWAN HALT",
    "se": "BIHAR"
  },
  {
    "sc": "DEOR",
    "en": "DIYODAR",
    "se": "GUJARAT"
  },
  {
    "sc": "DYU",
    "en": "DIYURI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DBS",
    "en": "DOBBSPET",
    "se": "KARNATAKA"
  },
  {
    "sc": "DHE",
    "en": "DOBHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DBU",
    "en": "DODBALLAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "DBL",
    "en": "DODBELE",
    "se": "KARNATAKA"
  },
  {
    "sc": "DPI",
    "en": "DODDAMPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "DODH",
    "en": "DODH",
    "se": "PUNJAB"
  },
  {
    "sc": "DJL",
    "en": "DODJALA H",
    "se": "KARNATAKA"
  },
  {
    "sc": "DOX",
    "en": "DOHNA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DIT",
    "en": "DOHRIGHAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DKLU",
    "en": "DOIKALLU",
    "se": "ODISHA"
  },
  {
    "sc": "DWO",
    "en": "DOIWALA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "DKWA",
    "en": "DOKWA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DJKR",
    "en": "DOLAJI KA KHERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DLV",
    "en": "DOLAVALI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DI",
    "en": "DOMBIVILI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DMG",
    "en": "DOMINGARH",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DKD",
    "en": "DONAKONDA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DDE",
    "en": "DONDAICHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DGN",
    "en": "DONGARGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DGG",
    "en": "DONGARGARH",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DGBZ",
    "en": "DONGRI BUZURG",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DOGL",
    "en": "DONIGAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "DNV",
    "en": "DONKINAVALASA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DON",
    "en": "DONTA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DOA",
    "en": "DORAHA",
    "se": "PUNJAB"
  },
  {
    "sc": "DVR",
    "en": "DORAVART CHTRAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DOY",
    "en": "DORNAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "DKJ",
    "en": "DORNAKAL JN",
    "se": "TELANGANA"
  },
  {
    "sc": "DPD",
    "en": "DOSAPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DSD",
    "en": "DOSVADA",
    "se": "GUJARAT"
  },
  {
    "sc": "DADN",
    "en": "DR AMBEDKAR NGR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DSKG",
    "en": "DRSKSN GARHPURA",
    "se": "BIHAR"
  },
  {
    "sc": "DUBH",
    "en": "DUBAHA",
    "se": "BIHAR"
  },
  {
    "sc": "DBW",
    "en": "DUBIA",
    "se": "ASSAM"
  },
  {
    "sc": "DUJ",
    "en": "DUBRAJPUR",
    "ec": "ASANSOL & ANDAL",
    "se": "WEST BENGAL",
    "tg": "ASANSOL,ANDAL"
  },
  {
    "sc": "DUE",
    "en": "DUDAHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DXN",
    "en": "DUDDHINAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DUD",
    "en": "DUDHANI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DDNA",
    "en": "DUDHAUNDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DYK",
    "en": "DUDHIA KHURD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DDNI",
    "en": "DUDHNOI",
    "se": "ASSAM"
  },
  {
    "sc": "DKX",
    "en": "DUDHWAKHARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DUK",
    "en": "DUDIA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DDW",
    "en": "DUDWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DDY",
    "en": "DUDWINDI",
    "se": "PUNJAB"
  },
  {
    "sc": "DUGA",
    "en": "DUGA",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "DUN",
    "en": "DUGANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DDGA",
    "en": "DUGDA",
    "se": "JHARKHAND"
  },
  {
    "sc": "DGQ",
    "en": "DUGDOL",
    "se": "GUJARAT"
  },
  {
    "sc": "DIG",
    "en": "DUGGIRALA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DXH",
    "en": "DUHAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DXU",
    "en": "DUHRU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DOKY",
    "en": "DUKHERI",
    "se": "HARYANA"
  },
  {
    "sc": "DUQ",
    "en": "DUKHNAWARAN",
    "se": "PUNJAB"
  },
  {
    "sc": "DLPT",
    "en": "DULAKHAPATNA PH",
    "se": "ODISHA"
  },
  {
    "sc": "DRA",
    "en": "DULARIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DJG",
    "en": "DULIAJAN",
    "se": "ASSAM"
  },
  {
    "sc": "DLCR",
    "en": "DULLABCHERRA",
    "se": "ASSAM"
  },
  {
    "sc": "DLR",
    "en": "DULLAHAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "DUS",
    "en": "DULRASAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DDJ",
    "en": "DUM DUM",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DDC",
    "en": "DUM DUM CANT",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DUT",
    "en": "DUM DUMA TOWN",
    "se": "ASSAM"
  },
  {
    "sc": "DY",
    "en": "DUMARIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DMZ",
    "en": "DUMDANGI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DMF",
    "en": "DUMERTA",
    "se": "ODISHA"
  },
  {
    "sc": "DUY",
    "en": "DUMIYANI",
    "se": "GUJARAT"
  },
  {
    "sc": "DUMK",
    "en": "DUMKA",
    "ec": "ASANSOL & DEOGHAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "DURE",
    "en": "DUMRAON",
    "se": "BIHAR"
  },
  {
    "sc": "DMBR",
    "en": "DUMRI BIHAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "DMRX",
    "en": "DUMRI HALT",
    "se": "BIHAR"
  },
  {
    "sc": "DRI",
    "en": "DUMRI JUARA",
    "se": "BIHAR"
  },
  {
    "sc": "DKU",
    "en": "DUMRI KHURD P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "DMLE",
    "en": "DUMURDAHA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DMRT",
    "en": "DUMURIPUT",
    "se": "ODISHA"
  },
  {
    "sc": "DOR",
    "en": "DUNDARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DDCE",
    "en": "DUNDI",
    "ec": "DAUND",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DOB",
    "en": "DUNDLOD MKDGRH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DGJ",
    "en": "DUNGAR JN",
    "se": "GUJARAT"
  },
  {
    "sc": "DNGD",
    "en": "DUNGARDA",
    "se": "GUJARAT"
  },
  {
    "sc": "DNRP",
    "en": "DUNGARPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DUV",
    "en": "DUNGGARPUR QURY",
    "se": "GUJARAT"
  },
  {
    "sc": "DGI",
    "en": "DUNGRI",
    "se": "GUJARAT"
  },
  {
    "sc": "DJX",
    "en": "DUNGRIPALI",
    "se": "ODISHA"
  },
  {
    "sc": "DUU",
    "en": "DUPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DDA",
    "en": "DURAUNDHA JN",
    "se": "BIHAR"
  },
  {
    "sc": "DURG",
    "en": "DURG",
    "ec": "DURG",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "DZK",
    "en": "DURGACHAK",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DZKT",
    "en": "DURGACHAK TOWN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DGDG",
    "en": "DURGADA GATE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DGNR",
    "en": "DURGANAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DGR",
    "en": "DURGAPUR",
    "ec": "DURGAPUR & ASANSOL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DPA",
    "en": "DURGAPURA",
    "ec": "JAIPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DGO",
    "en": "DURGAUTI",
    "se": "BIHAR"
  },
  {
    "sc": "DAJ",
    "en": "DUROJI",
    "se": "KARNATAKA"
  },
  {
    "sc": "DUSI",
    "en": "DUSI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DSK",
    "en": "DUSKHEDA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BARD",
    "en": "DUVRI KALAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "DVD",
    "en": "DUVVADA",
    "ec": "VISAKHAPATNAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DWP",
    "en": "DWARAPUDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DWK",
    "en": "DWARKA",
    "se": "GUJARAT"
  },
  {
    "sc": "DWJ",
    "en": "DWARKAGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "EDN",
    "en": "EDAMANN",
    "se": "KERALA"
  },
  {
    "sc": "EDP",
    "en": "EDAPALAYAM",
    "se": "KERALA"
  },
  {
    "sc": "EVA",
    "en": "EDAVAI",
    "se": "KERALA"
  },
  {
    "sc": "EDD",
    "en": "EDDULADODDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "EKM",
    "en": "EKAMBARAKUPPAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "EKR",
    "en": "EKANGARSARAI",
    "se": "BIHAR"
  },
  {
    "sc": "EKC",
    "en": "EKCHARI",
    "se": "BIHAR"
  },
  {
    "sc": "EKL",
    "en": "EKDIL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "EKI",
    "en": "EKLAKHI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "EKMA",
    "en": "EKMA",
    "se": "BIHAR"
  },
  {
    "sc": "EKNR",
    "en": "EKTA NAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "EL",
    "en": "ELAMANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ETR",
    "en": "ELATTUR",
    "se": "KERALA"
  },
  {
    "sc": "ELR",
    "en": "ELAVUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ELM",
    "en": "ELIMALA",
    "se": "KERALA"
  },
  {
    "sc": "YLM",
    "en": "ELLAMANCHILI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ENB",
    "en": "ELLENABAD",
    "se": "HARYANA"
  },
  {
    "sc": "EE",
    "en": "ELURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ENR",
    "en": "ENNORE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ELL",
    "en": "ERALIGU",
    "se": "ASSAM"
  },
  {
    "sc": "ERL",
    "en": "ERANIEL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ERC",
    "en": "ERICH ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "EDU",
    "en": "ERIODU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "YP",
    "en": "ERRUPALEM",
    "se": "TELANGANA"
  },
  {
    "sc": "ETAH",
    "en": "ETAH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ETK",
    "en": "ETAKKOT",
    "se": "KERALA"
  },
  {
    "sc": "ETW",
    "en": "ETAWAH JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ETUE",
    "en": "ETMADPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ETP",
    "en": "ETTAPUR ROAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ETMD",
    "en": "ETTIMADAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ETM",
    "en": "ETTUMANUR",
    "se": "KERALA"
  },
  {
    "sc": "EKN",
    "en": "EZHUKONE",
    "se": "KERALA"
  },
  {
    "sc": "FYZ",
    "en": "FAIZULLAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FAP",
    "en": "FAKHARPUR HALT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FKB",
    "en": "FAKHRABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "FKM",
    "en": "FAKIRAGRAM JN",
    "se": "ASSAM"
  },
  {
    "sc": "FLK",
    "en": "FALAKATA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "FM",
    "en": "FALAKNUMA",
    "se": "TELANGANA"
  },
  {
    "sc": "FLM",
    "en": "FALIMARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "FA",
    "en": "FALNA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "FSR",
    "en": "FAQARSAR",
    "se": "PUNJAB"
  },
  {
    "sc": "FAR",
    "en": "FARAH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FHT",
    "en": "FARAH TOWN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FRN",
    "en": "FARENI",
    "se": "GUJARAT"
  },
  {
    "sc": "FRH",
    "en": "FARHATNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FRD",
    "en": "FARHEDI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FDB",
    "en": "FARIDABAD",
    "se": "HARYANA"
  },
  {
    "sc": "FDN",
    "en": "FARIDABAD NW TN",
    "se": "HARYANA"
  },
  {
    "sc": "FRDH",
    "en": "FARIDAHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FDK",
    "en": "FARIDKOT",
    "se": "PUNJAB"
  },
  {
    "sc": "FNG",
    "en": "FARIDNAGAR",
    "se": "PUNJAB"
  },
  {
    "sc": "FRG",
    "en": "FARINGAPETTA",
    "se": "KARNATAKA"
  },
  {
    "sc": "FBD",
    "en": "FARRUKHABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FRTK",
    "en": "FARTIKUI",
    "se": "GUJARAT"
  },
  {
    "sc": "FN",
    "en": "FARUKHNAGAR",
    "se": "HARYANA"
  },
  {
    "sc": "FSP",
    "en": "FATEH SINGHPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "FSW",
    "en": "FATEH SINGHWALA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "FAB",
    "en": "FATEHABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FTD",
    "en": "FATEHABAD CH.JN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "FGR",
    "en": "FATEHGARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FGH",
    "en": "FATEHGARH HRYNA",
    "se": "HARYANA"
  },
  {
    "sc": "FGSB",
    "en": "FATEHGARH SAHIB",
    "se": "PUNJAB"
  },
  {
    "sc": "FAN",
    "en": "FATEHNAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "FTP",
    "en": "FATEHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FTC",
    "en": "FATEHPUR CHURSI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FTS",
    "en": "FATEHPUR SIKRI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FPS",
    "en": "FATEHPUR SKHWTI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "FUT",
    "en": "FATUHA JN",
    "se": "BIHAR"
  },
  {
    "sc": "FTH",
    "en": "FATUHI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "FZL",
    "en": "FAZALPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FKA",
    "en": "FAZILKA",
    "ec": "FIROZPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "FK",
    "en": "FEROK",
    "se": "KERALA"
  },
  {
    "sc": "PHS",
    "en": "FEROZESHAH",
    "se": "PUNJAB"
  },
  {
    "sc": "FGCN",
    "en": "FETEHGARH CHURN",
    "se": "PUNJAB"
  },
  {
    "sc": "FZD",
    "en": "FIROZABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "FZR",
    "en": "FIROZPUR CANT",
    "ec": "FIROZPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "FZP",
    "en": "FIROZPUR CITY",
    "ec": "FIROZPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "FBG",
    "en": "FORBESGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "FKG",
    "en": "FURKATING JN",
    "ec": "GOLAGHAT",
    "se": "ASSAM"
  },
  {
    "sc": "GUGD",
    "en": "G GORKHNATH DHM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GDPL",
    "en": "G POCHAMPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "GRCP",
    "en": "G.RAMACHANDRAPU",
    "se": "ODISHA"
  },
  {
    "sc": "GCH",
    "en": "GACHHIPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GHLE",
    "en": "GADADHARPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GDG",
    "en": "GADAG JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "GAR",
    "en": "GADARWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GDSN",
    "en": "GADHADA SWAMI",
    "se": "GUJARAT"
  },
  {
    "sc": "GKD",
    "en": "GADHAKDA",
    "se": "GUJARAT"
  },
  {
    "sc": "GDW",
    "en": "GADHWALA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GNR",
    "en": "GADIGANURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "GDD",
    "en": "GADRA ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GWD",
    "en": "GADWAL JN",
    "se": "TELANGANA"
  },
  {
    "sc": "GAX",
    "en": "GAGANAPOSH",
    "se": "ODISHA"
  },
  {
    "sc": "GGY",
    "en": "GAGARIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GLTA",
    "en": "GAHLOTA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GMR",
    "en": "GAHMAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GNZ",
    "en": "GAHNDRAN",
    "se": "PUNJAB"
  },
  {
    "sc": "GHB",
    "en": "GAHRI BHAGI",
    "se": "PUNJAB"
  },
  {
    "sc": "GAO",
    "en": "GAIGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GAW",
    "en": "GAINJAHWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GIR",
    "en": "GAINSARI JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GAE",
    "en": "GAIPURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GIL",
    "en": "GAISAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GPI",
    "en": "GAJAPATINAGARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GAJB",
    "en": "GAJARA BAHARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GJJ",
    "en": "GAJJELAKONDA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GJN",
    "en": "GAJNER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GJL",
    "en": "GAJRAULA JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GJS",
    "en": "GAJSINGHPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GLE",
    "en": "GAJULAGUDEM",
    "se": "TELANGANA"
  },
  {
    "sc": "GJW",
    "en": "GAJUWALA",
    "se": "HARYANA"
  },
  {
    "sc": "GJWL",
    "en": "GAJWEL",
    "se": "TELANGANA"
  },
  {
    "sc": "GAA",
    "en": "GALAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GAGA",
    "en": "GALGALIA",
    "se": "BIHAR"
  },
  {
    "sc": "GLI",
    "en": "GALSI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GUD",
    "en": "GALUDIH",
    "ec": "TATANAGAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "GVV",
    "en": "GALVAV",
    "se": "GUJARAT"
  },
  {
    "sc": "GRF",
    "en": "GAMBHIRI ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GHI",
    "en": "GAMBHIRPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "GMH",
    "en": "GAMHARIA",
    "ec": "TATANAGAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "GUR",
    "en": "GANAGAPUR ROAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "GNU",
    "en": "GANAUR",
    "se": "HARYANA"
  },
  {
    "sc": "GNV",
    "en": "GANDEVI",
    "se": "GUJARAT"
  },
  {
    "sc": "GIMB",
    "en": "GANDHIDHAM BG",
    "ec": "GANDHIDHAM",
    "se": "GUJARAT"
  },
  {
    "sc": "GG",
    "en": "GANDHIGRAM",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "GNC",
    "en": "GANDHINAGAR CAP",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "GADJ",
    "en": "GANDHINAGAR JPR",
    "ec": "JAIPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GHPU",
    "en": "GANDHIPURAM HAL",
    "se": "TELANGANA"
  },
  {
    "sc": "GSX",
    "en": "GANDHISMARAK RD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GNST",
    "en": "GANDHISMRITI",
    "se": "GUJARAT"
  },
  {
    "sc": "GAJ",
    "en": "GANESHGANJ",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GADM",
    "en": "GANGA DHAM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GGAR",
    "en": "GANGADHARA",
    "se": "GUJARAT"
  },
  {
    "sc": "GNGD",
    "en": "GANGADHARPUR",
    "se": "ODISHA"
  },
  {
    "sc": "GANG",
    "en": "GANGAGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GAG",
    "en": "GANGAGHAT",
    "se": "JHARKHAND"
  },
  {
    "sc": "GDN",
    "en": "GANGAIKONDAN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "GJ",
    "en": "GANGAJHARI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GNH",
    "en": "GANGAKHER",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GGNP",
    "en": "GANGANAPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GNNA",
    "en": "GANGANI",
    "se": "BIHAR"
  },
  {
    "sc": "GGC",
    "en": "GANGAPUR CITY",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GRMP",
    "en": "GANGARAMPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GGLE",
    "en": "GANGATIKURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GNGT",
    "en": "GANGATOLIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GNGL",
    "en": "GANGAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GGVT",
    "en": "GANGAVATHI",
    "se": "KARNATAKA"
  },
  {
    "sc": "GPY",
    "en": "GANGAYAPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GNN",
    "en": "GANGINENI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GNW",
    "en": "GANGIWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GGP",
    "en": "GANGNAPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GRP",
    "en": "GANGPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GGR",
    "en": "GANGRAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GJUT",
    "en": "GANGSAR JAITU",
    "se": "PUNJAB"
  },
  {
    "sc": "GVA",
    "en": "GANGUVADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BAQ",
    "en": "GANJ BASODA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GWA",
    "en": "GANJ DUNDWARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GAQ",
    "en": "GANJ KHAWAJA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GAM",
    "en": "GANJAM",
    "ec": "BRAHMAPUR",
    "se": "ODISHA"
  },
  {
    "sc": "GJMB",
    "en": "GANJMURADABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GALE",
    "en": "GANKAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GKT",
    "en": "GANKHERA P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GJT",
    "en": "GANNAGHATTA",
    "se": "KARNATAKA"
  },
  {
    "sc": "GWM",
    "en": "GANNAVARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GNPT",
    "en": "GANPATPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "GRBH",
    "en": "GAREA BIHAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "GBN",
    "en": "GARH BANAILI",
    "se": "BIHAR"
  },
  {
    "sc": "GEB",
    "en": "GARH BARUARI",
    "se": "BIHAR"
  },
  {
    "sc": "GRB",
    "en": "GARH DHRUBESWAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GUG",
    "en": "GARH JAIPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GGGS",
    "en": "GARHA GOODS SHE",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GQN",
    "en": "GARHANI",
    "se": "BIHAR"
  },
  {
    "sc": "GHX",
    "en": "GARHARA",
    "se": "BIHAR"
  },
  {
    "sc": "GBA",
    "en": "GARHBETA",
    "ec": "SALBONI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GHH",
    "en": "GARHI HARSARU",
    "se": "HARYANA"
  },
  {
    "sc": "GRMR",
    "en": "GARHI MANIKPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GIS",
    "en": "GARHI SANDRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GRM",
    "en": "GARHMAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GMS",
    "en": "GARHMUKTESAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GGB",
    "en": "GARHMUKTESAR BR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GSR",
    "en": "GARHSHANKAR",
    "se": "PUNJAB"
  },
  {
    "sc": "GHQ",
    "en": "GARHWA",
    "se": "JHARKHAND"
  },
  {
    "sc": "GIA",
    "en": "GARIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GFAE",
    "en": "GARIFA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GVI",
    "en": "GARIVIDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "JRJE",
    "en": "GARJEE",
    "se": "TRIPURA"
  },
  {
    "sc": "GRAK",
    "en": "GARKHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GLA",
    "en": "GARLA",
    "se": "TELANGANA"
  },
  {
    "sc": "GDE",
    "en": "GARLADINNE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GM",
    "en": "GARMADI",
    "se": "GUJARAT"
  },
  {
    "sc": "GSB",
    "en": "GARNA SAHIB",
    "se": "PUNJAB"
  },
  {
    "sc": "GRU",
    "en": "GAROPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GOH",
    "en": "GAROT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GPH",
    "en": "GARPOS",
    "se": "ODISHA"
  },
  {
    "sc": "GRHX",
    "en": "GARRA P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GSDH",
    "en": "GARSANDA HALT",
    "se": "BIHAR"
  },
  {
    "sc": "GRBL",
    "en": "GARUDUBILLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GHD",
    "en": "GARWA ROAD",
    "se": "JHARKHAND"
  },
  {
    "sc": "GVP",
    "en": "GATE VANAMPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "GTW",
    "en": "GATORA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "GRJ",
    "en": "GATRA P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GDGN",
    "en": "GAUDGAON.",
    "se": "KARNATAKA"
  },
  {
    "sc": "GAUR",
    "en": "GAUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GRX",
    "en": "GAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GB",
    "en": "GAURI BAZAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GBD",
    "en": "GAURIBIDANUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "GNG",
    "en": "GAURIGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GUP",
    "en": "GAURIPUR",
    "se": "ASSAM"
  },
  {
    "sc": "GMU",
    "en": "GAURIYAMAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GWS",
    "en": "GAUSHALA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "GATD",
    "en": "GAUTAMDHARA",
    "se": "JHARKHAND"
  },
  {
    "sc": "GPX",
    "en": "GAUTAMPURA ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GTST",
    "en": "GAUTAMSTHAN",
    "se": "BIHAR"
  },
  {
    "sc": "GAV",
    "en": "GAVADAKA",
    "se": "GUJARAT"
  },
  {
    "sc": "GAH",
    "en": "GAWNAHA",
    "se": "BIHAR"
  },
  {
    "sc": "GAYA",
    "en": "GAYA JN",
    "se": "BIHAR",
    "tg": "BODHGAYA"
  },
  {
    "sc": "GBE",
    "en": "GAYABARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GZKA",
    "en": "GAZIKA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GZO",
    "en": "GAZOLE",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GZL",
    "en": "GAZULAPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GEDE",
    "en": "GEDE",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GEK",
    "en": "GEGAL AKHRI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GXG",
    "en": "GEONG",
    "se": "HARYANA"
  },
  {
    "sc": "GER",
    "en": "GERATPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "GTKD",
    "en": "GERITA KOLVADA",
    "se": "GUJARAT"
  },
  {
    "sc": "GTJT",
    "en": "GETOR JAGATPURA",
    "ec": "JAIPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GOI",
    "en": "GEVARAI HALT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GAD",
    "en": "GEVRA ROAD",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "GELA",
    "en": "GHADELA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GHG",
    "en": "GHAGGHAR",
    "se": "PUNJAB"
  },
  {
    "sc": "GHT",
    "en": "GHAGHARA CHAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GHAA",
    "en": "GHAGHRA",
    "se": "JHARKHAND"
  },
  {
    "sc": "GHGL",
    "en": "GHAGWAL",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "GKX",
    "en": "GHAI KALAN",
    "se": "PUNJAB"
  },
  {
    "sc": "GHLU",
    "en": "GHALLU",
    "se": "PUNJAB"
  },
  {
    "sc": "GANL",
    "en": "GHANAULI",
    "se": "PUNJAB"
  },
  {
    "sc": "GNP",
    "en": "GHANPUR",
    "se": "TELANGANA"
  },
  {
    "sc": "GNS",
    "en": "GHANSORE",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GTH",
    "en": "GHANTA",
    "se": "GUJARAT"
  },
  {
    "sc": "GHNH",
    "en": "GHANTIKHAL NDPR",
    "se": "ODISHA"
  },
  {
    "sc": "GHTI",
    "en": "GHANTOLI",
    "se": "GUJARAT"
  },
  {
    "sc": "GRA",
    "en": "GHARAUNDA",
    "se": "HARYANA"
  },
  {
    "sc": "GYL",
    "en": "GHARYALA",
    "se": "PUNJAB"
  },
  {
    "sc": "GSY",
    "en": "GHASHYAMGADH RD",
    "se": "GUJARAT"
  },
  {
    "sc": "GSO",
    "en": "GHASO",
    "se": "HARYANA"
  },
  {
    "sc": "GPA",
    "en": "GHASPURA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GC",
    "en": "GHAT KOPAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GTU",
    "en": "GHAT NANDUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GKB",
    "en": "GHATAKA VARANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GTM",
    "en": "GHATAMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GEA",
    "en": "GHATERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GHAI",
    "en": "GHATIGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GT",
    "en": "GHATKESAR",
    "se": "TELANGANA"
  },
  {
    "sc": "GAL",
    "en": "GHATLA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GATL",
    "en": "GHATOLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GPC",
    "en": "GHATPINDRAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GPB",
    "en": "GHATPRABHA",
    "se": "KARNATAKA"
  },
  {
    "sc": "GTP",
    "en": "GHATPURI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GTS",
    "en": "GHATSILA",
    "ec": "TATANAGAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "GTWD",
    "en": "GHATWAD",
    "se": "GUJARAT"
  },
  {
    "sc": "GPW",
    "en": "GHAUNSPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "GSGJ",
    "en": "GHAUSGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GCT",
    "en": "GHAZIPUR CITY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GZT",
    "en": "GHAZIPUR GHAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GLD",
    "en": "GHELDA",
    "se": "GUJARAT"
  },
  {
    "sc": "GHE",
    "en": "GHEVRA",
    "se": "DELHI"
  },
  {
    "sc": "GILA",
    "en": "GHIALA",
    "se": "PUNJAB"
  },
  {
    "sc": "GGA",
    "en": "GHOGA",
    "se": "BIHAR"
  },
  {
    "sc": "GGH",
    "en": "GHOGARDIHA",
    "se": "BIHAR"
  },
  {
    "sc": "GOE",
    "en": "GHOGRAPUR",
    "se": "ASSAM"
  },
  {
    "sc": "GDX",
    "en": "GHOKSADANGA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GVD",
    "en": "GHOLVAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GDYA",
    "en": "GHORADONGRI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GGTA",
    "en": "GHORAGHATA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GRH",
    "en": "GHORASAHAN",
    "se": "BIHAR"
  },
  {
    "sc": "GRWD",
    "en": "GHORAWADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GRMA",
    "en": "GHORMARA",
    "se": "JHARKHAND"
  },
  {
    "sc": "GPR",
    "en": "GHORPURI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GSI",
    "en": "GHOSI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GOPA",
    "en": "GHOSIPURA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GOS",
    "en": "GHOSRANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GSD",
    "en": "GHOSUNDA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GO",
    "en": "GHOTI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GH",
    "en": "GHUGHULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GGS",
    "en": "GHUGUS",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GHUM",
    "en": "GHUM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GUS",
    "en": "GHUMASAN",
    "se": "GUJARAT"
  },
  {
    "sc": "GUNS",
    "en": "GHUNAS",
    "se": "PUNJAB"
  },
  {
    "sc": "GGT",
    "en": "GHUNGHUTI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GNWA",
    "en": "GHUNWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GTI",
    "en": "GHUTAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GOF",
    "en": "GHUTIARI SHARIF",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GTK",
    "en": "GHUTKU",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "GIZ",
    "en": "GIDAM",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "GOD",
    "en": "GIDARPINDI",
    "se": "PUNJAB"
  },
  {
    "sc": "GID",
    "en": "GIDDALUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GDB",
    "en": "GIDDARBAHA",
    "se": "PUNJAB"
  },
  {
    "sc": "GHR",
    "en": "GIDHAUR",
    "se": "BIHAR"
  },
  {
    "sc": "GDH",
    "en": "GIDNAHALI",
    "se": "KARNATAKA"
  },
  {
    "sc": "GII",
    "en": "GIDNI",
    "ec": "JHARGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GILL",
    "en": "GILL",
    "se": "PUNJAB"
  },
  {
    "sc": "GIN",
    "en": "GINIGERA",
    "se": "KARNATAKA"
  },
  {
    "sc": "GEG",
    "en": "GIR GADHARA",
    "se": "GUJARAT"
  },
  {
    "sc": "GRHM",
    "en": "GIR HADMATIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "GIW",
    "en": "GIRDHARPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GRD",
    "en": "GIRIDIH",
    "ec": "MADHUPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "GMDN",
    "en": "GIRIMAIDAN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GW",
    "en": "GIRWAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GADH",
    "en": "GOALDIH",
    "se": "ODISHA"
  },
  {
    "sc": "GLPT",
    "en": "GOALPARA TOWN",
    "se": "ASSAM"
  },
  {
    "sc": "GBG",
    "en": "GOBARDANGA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GBRI",
    "en": "GOBARWAHI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GOX",
    "en": "GOBINDPUR DUGLI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GDQ",
    "en": "GODAMGURA",
    "se": "TELANGANA"
  },
  {
    "sc": "GVN",
    "en": "GODAVARI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GBQ",
    "en": "GODBHAGA",
    "se": "ODISHA"
  },
  {
    "sc": "GODA",
    "en": "GODDA",
    "ec": "BHAGALPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "GDHA",
    "en": "GODHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GS",
    "en": "GODHANESHWAR",
    "se": "GUJARAT"
  },
  {
    "sc": "GDA",
    "en": "GODHRA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "GAMI",
    "en": "GOGAMERI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GOM",
    "en": "GOGAMUKH",
    "se": "ASSAM"
  },
  {
    "sc": "GPE",
    "en": "GOGI POTHIA",
    "se": "BIHAR"
  },
  {
    "sc": "GOA",
    "en": "GOHAD ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GHNA",
    "en": "GOHANA",
    "se": "HARYANA"
  },
  {
    "sc": "GRV",
    "en": "GOHLWAR VARPAL",
    "se": "PUNJAB"
  },
  {
    "sc": "GPZ",
    "en": "GOHPUR",
    "se": "ASSAM"
  },
  {
    "sc": "GOL",
    "en": "GOILKERA",
    "se": "JHARKHAND"
  },
  {
    "sc": "GWSB",
    "en": "GOINDWAL SAHIB",
    "se": "PUNJAB"
  },
  {
    "sc": "GPS",
    "en": "GOJAPUR SANKDHA",
    "se": "GUJARAT"
  },
  {
    "sc": "GJR",
    "en": "GOJHARIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "GKK",
    "en": "GOKAK ROAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "GOK",
    "en": "GOKARNA ROAD",
    "ec": "KARWAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "GKL",
    "en": "GOKULPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GK",
    "en": "GOLA GOKARANATH",
    "ec": "LAKHIMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GRE",
    "en": "GOLA ROAD",
    "se": "JHARKHAND"
  },
  {
    "sc": "GLBA",
    "en": "GOLABAI",
    "se": "ODISHA"
  },
  {
    "sc": "GLGT",
    "en": "GOLAGHAT",
    "ec": "GOLAGHAT",
    "se": "ASSAM"
  },
  {
    "sc": "GKJ",
    "en": "GOLAKGANJ",
    "se": "ASSAM"
  },
  {
    "sc": "GLNA",
    "en": "GOLANA HALT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GTA",
    "en": "GOLANTHRA",
    "se": "ODISHA"
  },
  {
    "sc": "GTY",
    "en": "GOLAPATTI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GJH",
    "en": "GOLDINGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "GOLE",
    "en": "GOLE"
  },
  {
    "sc": "GHA",
    "en": "GOLEHWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "GHL",
    "en": "GOLHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "GLY",
    "en": "GOLLAPALLY",
    "se": "TELANGANA"
  },
  {
    "sc": "GLP",
    "en": "GOLLAPROLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GOZ",
    "en": "GOLSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GMGM",
    "en": "GOMANGALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "GTNR",
    "en": "GOMATI NAGAR",
    "ec": "LUCKNOW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GTT",
    "en": "GOMTA",
    "se": "GUJARAT"
  },
  {
    "sc": "GMI",
    "en": "GOND UMRI P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GD",
    "en": "GONDA JN",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GDK",
    "en": "GONDA KACHAHRI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GDL",
    "en": "GONDAL",
    "se": "GUJARAT"
  },
  {
    "sc": "G",
    "en": "GONDIA JN",
    "ec": "GONDIA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GNVR",
    "en": "GONDWANAVISAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GNA",
    "en": "GONEANA B JAGTA",
    "se": "PUNJAB"
  },
  {
    "sc": "GNL",
    "en": "GONGLE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GY",
    "en": "GOOTY",
    "ec": "GUNTAKAL",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GYF",
    "en": "GOOTY FORT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GOP",
    "en": "GOP JAM",
    "se": "GUJARAT"
  },
  {
    "sc": "GPMA",
    "en": "GOP MOTA",
    "se": "GUJARAT"
  },
  {
    "sc": "GN",
    "en": "GOPAL NAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GPT",
    "en": "GOPALAPATNAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GOPG",
    "en": "GOPALGANJ",
    "ec": "SIWAN",
    "se": "BIHAR"
  },
  {
    "sc": "GPPR",
    "en": "GOPALPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "GBK",
    "en": "GOPALPUR BALKDA",
    "se": "ODISHA"
  },
  {
    "sc": "GPLG",
    "en": "GOPALPURGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GOR",
    "en": "GOPINATHPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GGM",
    "en": "GORA GHUMA",
    "se": "GUJARAT"
  },
  {
    "sc": "GRKN",
    "en": "GORAKHNATH",
    "se": "ODISHA"
  },
  {
    "sc": "GKC",
    "en": "GORAKHPUR CANT",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GGO",
    "en": "GORAM GHAT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GPJ",
    "en": "GORAPUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GRTA",
    "en": "GORATIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "GRL",
    "en": "GORAUL",
    "se": "BIHAR"
  },
  {
    "sc": "GRY",
    "en": "GORAYA",
    "se": "PUNJAB"
  },
  {
    "sc": "GEBL",
    "en": "GOREBAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "GNO",
    "en": "GOREGAON ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GMN",
    "en": "GOREGOAN",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GVR",
    "en": "GORESWAR",
    "se": "ASSAM"
  },
  {
    "sc": "GRJA",
    "en": "GORINJA",
    "se": "GUJARAT"
  },
  {
    "sc": "GOTD",
    "en": "GORINTADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GIO",
    "en": "GORIYAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GUMI",
    "en": "GORUMAHISANI",
    "se": "ODISHA"
  },
  {
    "sc": "GSPR",
    "en": "GOSALPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GGJ",
    "en": "GOSHAINGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GOGH",
    "en": "GOSSAIGAON HAT",
    "se": "ASSAM"
  },
  {
    "sc": "GOT",
    "en": "GOT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GOTN",
    "en": "GOTAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GTE",
    "en": "GOTHAJ",
    "se": "GUJARAT"
  },
  {
    "sc": "GTX",
    "en": "GOTHANGAM",
    "se": "GUJARAT"
  },
  {
    "sc": "GTLM",
    "en": "GOTLAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GTRA",
    "en": "GOTRA HALT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GZM",
    "en": "GOUR MALDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GNI",
    "en": "GOURANDI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GTD",
    "en": "GOURINATHDHAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GV",
    "en": "GOVANDAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GDO",
    "en": "GOVERDHAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GVH",
    "en": "GOVINDGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GGKR",
    "en": "GOVINDGARH KHKR",
    "se": "PUNJAB"
  },
  {
    "sc": "GND",
    "en": "GOVINDGARH MALK",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GGWT",
    "en": "GOVINDGARH WTGR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GVMR",
    "en": "GOVINDI MARWAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GOVR",
    "en": "GOVINDNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GBX",
    "en": "GOVINDPUR ROAD",
    "se": "JHARKHAND"
  },
  {
    "sc": "GOY",
    "en": "GOVINDPURI",
    "ec": "KANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GWV",
    "en": "GOWDAVALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "GUA",
    "en": "GUA",
    "ec": "BARABIL",
    "se": "JHARKHAND"
  },
  {
    "sc": "GBB",
    "en": "GUBBI",
    "se": "KARNATAKA"
  },
  {
    "sc": "GDPT",
    "en": "GUDAPARTI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GDI",
    "en": "GUDGERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "GA",
    "en": "GUDHA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GMA",
    "en": "GUDIMETTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GPDE",
    "en": "GUDIPUDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GDV",
    "en": "GUDIVADA JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GYM",
    "en": "GUDIYATTAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "GVL",
    "en": "GUDLAVALLERU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GDM",
    "en": "GUDMA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GDU",
    "en": "GUDRU HALT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GUDM",
    "en": "GUDUM P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "GDP",
    "en": "GUDUPULLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GDR",
    "en": "GUDUR JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GI",
    "en": "GUDUVANCHERI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "GDY",
    "en": "GUINDY",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "GSQ",
    "en": "GUIR SARANGA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GJD",
    "en": "GUJHANDI",
    "se": "JHARKHAND"
  },
  {
    "sc": "GUL",
    "en": "GUJJANGIVALASA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GLBN",
    "en": "GUJRAN BALWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GLG",
    "en": "GULABHGANJ",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GBP",
    "en": "GULABPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GLH",
    "en": "GULAOTHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GPU",
    "en": "GULAPALYAMU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GUB",
    "en": "GULARBHOJ",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "GUH",
    "en": "GULDHAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GED",
    "en": "GULEDAGUDDA RD",
    "se": "KARNATAKA"
  },
  {
    "sc": "GULR",
    "en": "GULER",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "GGD",
    "en": "GULLAGUDA",
    "se": "TELANGANA"
  },
  {
    "sc": "GLU",
    "en": "GULLIPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GLMA",
    "en": "GULMA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GLV",
    "en": "GULVANCHI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GZH",
    "en": "GULZARBAGH",
    "se": "BIHAR"
  },
  {
    "sc": "GUMA",
    "en": "GUMA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GMDA",
    "en": "GUMADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GMAN",
    "en": "GUMANI",
    "se": "JHARKHAND"
  },
  {
    "sc": "GMG",
    "en": "GUMGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GMIA",
    "en": "GUMIA",
    "se": "JHARKHAND"
  },
  {
    "sc": "GMM",
    "en": "GUMMAN",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "GME",
    "en": "GUMMANDEV",
    "se": "GUJARAT"
  },
  {
    "sc": "GPD",
    "en": "GUMMIDIPUNDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "GTF",
    "en": "GUMTHAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GMTO",
    "en": "GUMTO",
    "se": "ARUNACHAL PRADESH"
  },
  {
    "sc": "GUNA",
    "en": "GUNA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GALA",
    "en": "GUNADALA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GDJ",
    "en": "GUNDA ROAD JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "GDZ",
    "en": "GUNDARDEHI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "GKM",
    "en": "GUNDLA KAMMA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GUU",
    "en": "GUNDRATIMADUGU",
    "se": "TELANGANA"
  },
  {
    "sc": "GVB",
    "en": "GUNERU BAMORI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GNGR",
    "en": "GUNGRANA",
    "se": "PUNJAB"
  },
  {
    "sc": "GUJ",
    "en": "GUNJA",
    "se": "GUJARAT"
  },
  {
    "sc": "GEOR",
    "en": "GUNJARIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GNJ",
    "en": "GUNJI",
    "se": "KARNATAKA"
  },
  {
    "sc": "GTL",
    "en": "GUNTAKAL JN",
    "ec": "GUNTAKAL",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GUK",
    "en": "GUNTAKODURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GNPR",
    "en": "GUNUPUR",
    "se": "ODISHA"
  },
  {
    "sc": "GPAE",
    "en": "GUPTIPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GRMT",
    "en": "GUR MARKET",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GMD",
    "en": "GURAMKHEDI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GRAE",
    "en": "GURAP",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GRRU",
    "en": "GURARU",
    "se": "BIHAR"
  },
  {
    "sc": "GSP",
    "en": "GURDASPUR",
    "ec": "AMRITSAR",
    "se": "PUNJAB"
  },
  {
    "sc": "GGN",
    "en": "GURGAON",
    "ec": "NEW DELHI",
    "se": "HARYANA"
  },
  {
    "sc": "GRKA",
    "en": "GURHA KEMLA",
    "se": "HARYANA"
  },
  {
    "sc": "GRNA",
    "en": "GURHANWA",
    "se": "BIHAR"
  },
  {
    "sc": "GUX",
    "en": "GURHI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GRI",
    "en": "GURIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GQL",
    "en": "GURLA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "GRRG",
    "en": "GURLI RAMGARHWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GMX",
    "en": "GURMURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GRN",
    "en": "GURNAY",
    "se": "PUNJAB"
  },
  {
    "sc": "GAP",
    "en": "GURPA",
    "se": "BIHAR"
  },
  {
    "sc": "GRO",
    "en": "GURRA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GHJ",
    "en": "GURSAHAIGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GSW",
    "en": "GURSAR SHNEWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "GRZ",
    "en": "GURTHURI",
    "se": "PUNJAB"
  },
  {
    "sc": "GHS",
    "en": "GURU HARSAHAI",
    "se": "PUNJAB"
  },
  {
    "sc": "GTBN",
    "en": "GURU T B NAGAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GURN",
    "en": "GURUDAS NAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GJTA",
    "en": "GURUDIJHATIA",
    "se": "ODISHA"
  },
  {
    "sc": "GZA",
    "en": "GURUJALA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GRS",
    "en": "GURUSAR SUTLANI",
    "se": "PUNJAB"
  },
  {
    "sc": "GUV",
    "en": "GURUVAYUR",
    "se": "KERALA"
  },
  {
    "sc": "GKH",
    "en": "GUSKARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GRG",
    "en": "GUWARIGHAT",
    "ec": "JABALPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GWO",
    "en": "GWALIOR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GYN",
    "en": "GYANPUR ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "GZS",
    "en": "GZ SANDHWAN",
    "se": "PUNJAB"
  },
  {
    "sc": "HWX",
    "en": "HABAIPUR",
    "se": "ASSAM"
  },
  {
    "sc": "HHT",
    "en": "HABANGHATA",
    "se": "KARNATAKA"
  },
  {
    "sc": "HBE",
    "en": "HABIBPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HBW",
    "en": "HABIBWALA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HB",
    "en": "HABRA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HLB",
    "en": "HADALA BHAL",
    "se": "GUJARAT"
  },
  {
    "sc": "HAK",
    "en": "HADALA KHARI",
    "se": "GUJARAT"
  },
  {
    "sc": "HDP",
    "en": "HADAPSAR",
    "ec": "PUNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HDD",
    "en": "HADDINAGUNDU",
    "se": "KARNATAKA"
  },
  {
    "sc": "HDGR",
    "en": "HADGAON ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HYA",
    "en": "HADIAYA",
    "se": "PUNJAB"
  },
  {
    "sc": "HRM",
    "en": "HADMADIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "HM",
    "en": "HADMATIYA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "HBF",
    "en": "HADOBHANGI",
    "se": "ODISHA"
  },
  {
    "sc": "HYL",
    "en": "HADYAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HFZ",
    "en": "HAFIZPETA",
    "se": "TELANGANA"
  },
  {
    "sc": "HZR",
    "en": "HAFIZPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HGI",
    "en": "HAGARI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HYT",
    "en": "HAIAGHAT",
    "se": "BIHAR"
  },
  {
    "sc": "HBN",
    "en": "HAIBARGAON",
    "ec": "CHAPARMUKH",
    "se": "ASSAM"
  },
  {
    "sc": "HDN",
    "en": "HAIDARNAGAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "HGH",
    "en": "HAIDERGARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HKD",
    "en": "HAILAKANDI",
    "se": "ASSAM"
  },
  {
    "sc": "HIH",
    "en": "HAJIGARH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HJP",
    "en": "HAJIPUR JN",
    "se": "BIHAR"
  },
  {
    "sc": "HKP",
    "en": "HAKIMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HLKT",
    "en": "HALAKATTA"
  },
  {
    "sc": "HBU",
    "en": "HALBARGA",
    "se": "KARNATAKA"
  },
  {
    "sc": "HLDR",
    "en": "HALDAUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HLP",
    "en": "HALDHARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HLDD",
    "en": "HALDI ROAD",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "HLZ",
    "en": "HALDIA",
    "ec": "HALDIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HDB",
    "en": "HALDIBARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HIP",
    "en": "HALDIPADA",
    "se": "ODISHA"
  },
  {
    "sc": "HOD",
    "en": "HALDITA BIHAR",
    "se": "BIHAR"
  },
  {
    "sc": "HDW",
    "en": "HALDWANI",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "HLGR",
    "en": "HALGERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HLR",
    "en": "HALISAHAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HLV",
    "en": "HALIYURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "HAG",
    "en": "HALLIGUDI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HLKH",
    "en": "HALLIKHED B",
    "se": "KARNATAKA"
  },
  {
    "sc": "HIKD",
    "en": "HALLIKHED K",
    "se": "KARNATAKA"
  },
  {
    "sc": "HLD",
    "en": "HALUDPUKUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "HVD",
    "en": "HALVAD",
    "se": "GUJARAT"
  },
  {
    "sc": "HMRR",
    "en": "HAMARAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HMPR",
    "en": "HAMARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HOJ",
    "en": "HAMILTONGANJ",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HMR",
    "en": "HAMIRA",
    "se": "PUNJAB"
  },
  {
    "sc": "HMG",
    "en": "HAMIRGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HAM",
    "en": "HAMIRHATI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HAR",
    "en": "HAMIRPUR ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HPM",
    "en": "HAMPAPATNAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "HPA",
    "en": "HAMPAPURA",
    "se": "KARNATAKA"
  },
  {
    "sc": "HME",
    "en": "HAMRE",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "HVM",
    "en": "HAMSAVARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "HNK",
    "en": "HANAKERE",
    "se": "KARNATAKA"
  },
  {
    "sc": "HAPR",
    "en": "HANAMAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "HNPA",
    "en": "HANDAPA",
    "se": "ODISHA"
  },
  {
    "sc": "HDK",
    "en": "HANDIA KHAS",
    "ec": "PRAYAGRAJ RAMBHAG",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HNR",
    "en": "HANSARA",
    "se": "ASSAM"
  },
  {
    "sc": "HSDA",
    "en": "HANSDIHA",
    "se": "JHARKHAND"
  },
  {
    "sc": "HNS",
    "en": "HANSI JN",
    "se": "HARYANA"
  },
  {
    "sc": "HSWS",
    "en": "HANSIAWAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HNMN",
    "en": "HANUMAN STATION",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "HNH",
    "en": "HANUMANAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HMH",
    "en": "HANUMANGARH JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HMO",
    "en": "HANUMANGARHTOWN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HPH",
    "en": "HANUMAPURA",
    "se": "KARNATAKA"
  },
  {
    "sc": "HWT",
    "en": "HANWANT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HAPA",
    "en": "HAPA",
    "ec": "JAMNAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "HPRD",
    "en": "HAPA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "HPU",
    "en": "HAPUR",
    "ec": "HAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HNN",
    "en": "HARANA KALAN",
    "se": "HARYANA"
  },
  {
    "sc": "HJO",
    "en": "HARANGAJAO"
  },
  {
    "sc": "HGL",
    "en": "HARANGUL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HKH",
    "en": "HARANYA KHERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "HPHI",
    "en": "HARAPANAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HRN",
    "en": "HARAUNI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HCP",
    "en": "HARCHANDPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HD",
    "en": "HARDA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "HDE",
    "en": "HARDAS BIGHA",
    "se": "BIHAR"
  },
  {
    "sc": "HDT",
    "en": "HARDATTPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HRI",
    "en": "HARDOI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HDWL",
    "en": "HARDORAWAL",
    "se": "PUNJAB"
  },
  {
    "sc": "HDU",
    "en": "HARDUA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "HGJ",
    "en": "HARDUAGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HA",
    "en": "HARGAON",
    "ec": "LAKHIMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HRF",
    "en": "HARHRAS QILAH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HCNR",
    "en": "HARICHANDANPUR",
    "se": "ODISHA"
  },
  {
    "sc": "HDS",
    "en": "HARIDASPUR",
    "se": "ODISHA"
  },
  {
    "sc": "HRR",
    "en": "HARIHAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "HIR",
    "en": "HARINAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "HRNS",
    "en": "HARINSING",
    "se": "JHARKHAND"
  },
  {
    "sc": "HPL",
    "en": "HARIPAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HAD",
    "en": "HARIPPAD",
    "se": "KERALA"
  },
  {
    "sc": "HP",
    "en": "HARIPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HPGM",
    "en": "HARIPURGRAM  JN",
    "ec": "KHURDA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "HCR",
    "en": "HARISCHANDRPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HSK",
    "en": "HARISHANKER RD",
    "se": "ODISHA"
  },
  {
    "sc": "HHP",
    "en": "HARISHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HRSN",
    "en": "HARISINGA",
    "se": "ASSAM"
  },
  {
    "sc": "HKL",
    "en": "HARKIA KHAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RLP",
    "en": "HARLAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "HRLI",
    "en": "HARLAYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HMY",
    "en": "HARMUTI",
    "se": "ASSAM"
  },
  {
    "sc": "HNHL",
    "en": "HARNAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HRT",
    "en": "HARNAUT",
    "se": "BIHAR"
  },
  {
    "sc": "HRPG",
    "en": "HARPALGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HPP",
    "en": "HARPALPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "HR",
    "en": "HARPALU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HRV",
    "en": "HARRAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "HRW",
    "en": "HARRAWALA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "HRB",
    "en": "HARRI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "HRDR",
    "en": "HARSAR DEHRI",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "HSI",
    "en": "HARSAULI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HSY",
    "en": "HARSINGPUR GOBA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HRH",
    "en": "HARTHALA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HRO",
    "en": "HARUA ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HAA",
    "en": "HARWADA",
    "se": "KARNATAKA"
  },
  {
    "sc": "HNB",
    "en": "HASANABAD",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HSP",
    "en": "HASANPARTI RD",
    "se": "TELANGANA"
  },
  {
    "sc": "HPO",
    "en": "HASANPUR ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "HSA",
    "en": "HASIMARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HAS",
    "en": "HASSAN",
    "se": "KARNATAKA"
  },
  {
    "sc": "HAQ",
    "en": "HASTAVARAMU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "HN",
    "en": "HATHBANDH",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "HTZ",
    "en": "HATHIDAH JN",
    "se": "BIHAR"
  },
  {
    "sc": "HTZU",
    "en": "HATHIDAH UPPER",
    "se": "BIHAR"
  },
  {
    "sc": "HTGR",
    "en": "HATHIGADH",
    "se": "GUJARAT"
  },
  {
    "sc": "HTC",
    "en": "HATHRAS CITY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HRS",
    "en": "HATHRAS JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HTJ",
    "en": "HATHRAS ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HTW",
    "en": "HATHUA",
    "ec": "SIWAN",
    "se": "BIHAR"
  },
  {
    "sc": "HAT",
    "en": "HATHURAN",
    "se": "GUJARAT"
  },
  {
    "sc": "HTE",
    "en": "HATIA",
    "ec": "HATIA/RANCHI",
    "se": "JHARKHAND"
  },
  {
    "sc": "HATB",
    "en": "HATIBARI",
    "se": "ODISHA"
  },
  {
    "sc": "HTL",
    "en": "HATIKHALI",
    "se": "ASSAM"
  },
  {
    "sc": "HTK",
    "en": "HATKANAGALE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HPLE",
    "en": "HATPURAINI",
    "se": "BIHAR"
  },
  {
    "sc": "HTT",
    "en": "HATRA ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "HTD",
    "en": "HATUNDI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HWR",
    "en": "HATWAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HAUR",
    "en": "HAUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HSM",
    "en": "HAUSNAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HZD",
    "en": "HAZARIBAGH RD",
    "se": "JHARKHAND"
  },
  {
    "sc": "HZBN",
    "en": "HAZARIBAGH TOWN",
    "se": "JHARKHAND"
  },
  {
    "sc": "HZH",
    "en": "HAZRATHPUR HLT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HBLN",
    "en": "HBL NAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "HEB",
    "en": "HEBBAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "HBS",
    "en": "HEBSUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "HEI",
    "en": "HEGGERE H",
    "se": "KARNATAKA"
  },
  {
    "sc": "HJL",
    "en": "HEJJALA",
    "se": "KARNATAKA"
  },
  {
    "sc": "HK",
    "en": "HELAK",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HML",
    "en": "HELEM",
    "se": "ASSAM"
  },
  {
    "sc": "HGR",
    "en": "HEMAGIRI",
    "se": "ODISHA"
  },
  {
    "sc": "HMP",
    "en": "HEMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HNDR",
    "en": "HENDEGIR",
    "se": "JHARKHAND"
  },
  {
    "sc": "HEN",
    "en": "HENRYA P H",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HER",
    "en": "HER",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HET",
    "en": "HETAMPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "HBI",
    "en": "HGRIBOMANAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HIJ",
    "en": "HIJLI",
    "ec": "KHARAGPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HLX",
    "en": "HILARA",
    "se": "ASSAM"
  },
  {
    "sc": "HLG",
    "en": "HILLIGROVE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "HIL",
    "en": "HILSA",
    "se": "BIHAR"
  },
  {
    "sc": "HEM",
    "en": "HIMAYATNAGAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HMI",
    "en": "HIMMATANA",
    "se": "PUNJAB"
  },
  {
    "sc": "HMT",
    "en": "HIMMATNAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "HMQ",
    "en": "HIMMATPURA",
    "se": "HARYANA"
  },
  {
    "sc": "HNM",
    "en": "HINAUTARAMBAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "HIND",
    "en": "HIND",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HMZ",
    "en": "HIND MOTOR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HAN",
    "en": "HINDAUN CITY",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HND",
    "en": "HINDOL ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "HMK",
    "en": "HINDUMALKOTE",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HUP",
    "en": "HINDUPUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "HGT",
    "en": "HINGANGHAT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HNL",
    "en": "HINGOLI DECCAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HPKA",
    "en": "HINOTIAPPLKHEDA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "HRNR",
    "en": "HIRA NAGAR",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "HKG",
    "en": "HIRAKUD",
    "ec": "SAMBALPUR",
    "se": "ODISHA"
  },
  {
    "sc": "HNG",
    "en": "HIRANGAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "HPR",
    "en": "HIRAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HRG",
    "en": "HIRDAGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "HDM",
    "en": "HIRDAMALI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HESK",
    "en": "HIRE SHELLIKERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HHL",
    "en": "HIREHALI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HQR",
    "en": "HIRENANDURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "HISE",
    "en": "HIRISAVE",
    "se": "KARNATAKA"
  },
  {
    "sc": "HLW",
    "en": "HIRNAWALI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HDA",
    "en": "HIRNODA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HRE",
    "en": "HIRODIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "HSR",
    "en": "HISAR",
    "se": "HARYANA"
  },
  {
    "sc": "HSL",
    "en": "HISVAHAL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HTNL",
    "en": "HITNAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "HKR",
    "en": "HIWARKHED",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HDL",
    "en": "HODAL",
    "se": "HARYANA"
  },
  {
    "sc": "HGA",
    "en": "HOGLA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HJI",
    "en": "HOJAI",
    "se": "ASSAM"
  },
  {
    "sc": "HOL",
    "en": "HOL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HLK",
    "en": "HOLALKERE",
    "se": "KARNATAKA"
  },
  {
    "sc": "HUK",
    "en": "HOLAMBI KALAN",
    "se": "DELHI"
  },
  {
    "sc": "HLAR",
    "en": "HOLE ALUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "HLN",
    "en": "HOLE NARSIPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "HBL",
    "en": "HOMBAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "HOH",
    "en": "HONAGANAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HVL",
    "en": "HONNAVALLI RD",
    "se": "KARNATAKA"
  },
  {
    "sc": "HNA",
    "en": "HONNAVAR",
    "ec": "KARWAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "HGY",
    "en": "HOOGHLY",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HYG",
    "en": "HOOGHLY GHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HRTK",
    "en": "HORTOKI",
    "se": "MIZORAM"
  },
  {
    "sc": "HAH",
    "en": "HOSA AGRAHARA",
    "se": "KARNATAKA"
  },
  {
    "sc": "HPT",
    "en": "HOSAPETE JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "HSD",
    "en": "HOSDURGA ROAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "HSX",
    "en": "HOSHIARPUR",
    "ec": "JALANDHAR",
    "se": "PUNJAB"
  },
  {
    "sc": "HSRA",
    "en": "HOSUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "HT",
    "en": "HOTAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HG",
    "en": "HOTGI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "HBG",
    "en": "HOWBADH JABLPUR"
  },
  {
    "sc": "HHR",
    "en": "HRIDAYPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "HCM",
    "en": "HRSCHNDRAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "HUD",
    "en": "HUDUKULA",
    "se": "KARNATAKA"
  },
  {
    "sc": "HJLI",
    "en": "HUGRAJULI",
    "se": "ASSAM"
  },
  {
    "sc": "LKT",
    "en": "HULKOTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HMA",
    "en": "HUMMA",
    "se": "ODISHA"
  },
  {
    "sc": "HMBD",
    "en": "HUMNABAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "HUN",
    "en": "HUNSENAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "HHD",
    "en": "HUNSIHADGIL",
    "se": "KARNATAKA"
  },
  {
    "sc": "HPG",
    "en": "HUPPUGUDA",
    "se": "TELANGANA"
  },
  {
    "sc": "HSW",
    "en": "HUSAINIWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "HSQ",
    "en": "HUSAINPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "IB",
    "en": "IB",
    "se": "ODISHA"
  },
  {
    "sc": "IMR",
    "en": "IBRAHIMPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "ICL",
    "en": "ICHAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "IPM",
    "en": "ICHCHPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "IP",
    "en": "ICHHAPUR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "IDJ",
    "en": "IDALHOND",
    "se": "KARNATAKA"
  },
  {
    "sc": "IPL",
    "en": "IDAPLLI",
    "se": "KERALA"
  },
  {
    "sc": "IDAR",
    "en": "IDAR",
    "se": "GUJARAT"
  },
  {
    "sc": "IDH",
    "en": "IDGAH AGRA JN",
    "ec": "AGRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "IGP",
    "en": "IGATPURI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "IKD",
    "en": "IKDORI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "IKK",
    "en": "IKKAR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "IKR",
    "en": "IKLEHRA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "IKRA",
    "en": "IKRA JN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "IK",
    "en": "IKRAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "IVL",
    "en": "ILAVELANGAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ILO",
    "en": "ILLOO",
    "se": "WEST BENGAL"
  },
  {
    "sc": "IMAM",
    "en": "IMAMPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "IMLI",
    "en": "IMLI",
    "se": "BIHAR"
  },
  {
    "sc": "IHP",
    "en": "INCHHAPURI",
    "se": "HARYANA"
  },
  {
    "sc": "IDL",
    "en": "INDALVAI",
    "se": "TELANGANA"
  },
  {
    "sc": "INP",
    "en": "INDAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "IAA",
    "en": "INDARA JN",
    "ec": "MAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "IDGH",
    "en": "INDARGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "IDG",
    "en": "INDARGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "INS",
    "en": "INDAS",
    "se": "WEST BENGAL"
  },
  {
    "sc": "IDM",
    "en": "INDEMAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "IDR",
    "en": "INDI ROAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "INDR",
    "en": "INDIRA NAGAR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "INDM",
    "en": "INDORE JN MG",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "IBL",
    "en": "INDRABIL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "IDP",
    "en": "INDUPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "IGTA",
    "en": "INGOHTA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "IGR",
    "en": "INGUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "INJ",
    "en": "INNANJE",
    "se": "KARNATAKA"
  },
  {
    "sc": "INK",
    "en": "INTEKANNE",
    "se": "TELANGANA"
  },
  {
    "sc": "ITE",
    "en": "INTIYATHOK",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "IPG",
    "en": "IPPAGUDA",
    "se": "TELANGANA"
  },
  {
    "sc": "IPPM",
    "en": "IPURUPALEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "IQG",
    "en": "IQBAL GADH",
    "se": "GUJARAT"
  },
  {
    "sc": "IQB",
    "en": "IQBALPUR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "IDGJ",
    "en": "IRADATGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "EGU",
    "en": "IRANAGALLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "IRP",
    "en": "IRAVIPURAM",
    "se": "KERALA"
  },
  {
    "sc": "IRN",
    "en": "IRGAON",
    "se": "JHARKHAND"
  },
  {
    "sc": "IGL",
    "en": "IRINGAL",
    "se": "KERALA"
  },
  {
    "sc": "IJK",
    "en": "IRINJALAKUDA",
    "se": "KERALA"
  },
  {
    "sc": "IGU",
    "en": "IRUGUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "EN",
    "en": "ISAND",
    "se": "GUJARAT"
  },
  {
    "sc": "ISA",
    "en": "ISARDA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ISH",
    "en": "ISARWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ISHN",
    "en": "ISHANAGAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "IDS",
    "en": "ISHARDASPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ESV",
    "en": "ISIVI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "IPR",
    "en": "ISLAMPUR",
    "se": "BIHAR"
  },
  {
    "sc": "ISM",
    "en": "ISMAILA HARYANA",
    "se": "HARYANA"
  },
  {
    "sc": "IMGE",
    "en": "ISMAILPUR",
    "se": "BIHAR"
  },
  {
    "sc": "IRA",
    "en": "ISRANA",
    "se": "HARYANA"
  },
  {
    "sc": "ET",
    "en": "ITARSI JN",
    "ec": "PIPARIYA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "IJ",
    "en": "ITAUNJA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "AAH",
    "en": "ITEHAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "IKI",
    "en": "ITIKYALA",
    "se": "TELANGANA"
  },
  {
    "sc": "ITKY",
    "en": "ITKY",
    "se": "JHARKHAND"
  },
  {
    "sc": "ITA",
    "en": "ITOLA",
    "se": "GUJARAT"
  },
  {
    "sc": "IZN",
    "en": "IZZATNAGAR",
    "ec": "BAREILLY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JBU",
    "en": "JAABUGAM",
    "se": "GUJARAT"
  },
  {
    "sc": "JBGD",
    "en": "JABBALGUDDA",
    "se": "KARNATAKA"
  },
  {
    "sc": "JBL",
    "en": "JABLI",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "JBX",
    "en": "JABRI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JDP",
    "en": "JADABPUR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JADR",
    "en": "JADAR",
    "se": "GUJARAT"
  },
  {
    "sc": "JCL",
    "en": "JADCHERLA",
    "se": "TELANGANA"
  },
  {
    "sc": "JBS",
    "en": "JADOLI KA BAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JFG",
    "en": "JAFARGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JUD",
    "en": "JAGADHRI",
    "ec": "JAGADHRI"
  },
  {
    "sc": "JUDW",
    "en": "JAGADHRI WSHOP",
    "ec": "JAGADHRI",
    "se": "HARYANA"
  },
  {
    "sc": "JGD",
    "en": "JAGADISHPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "JNP",
    "en": "JAGANNATHPUR",
    "se": "ODISHA"
  },
  {
    "sc": "JTB",
    "en": "JAGATBELA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JDB",
    "en": "JAGDALPUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "JDL",
    "en": "JAGDEVWALA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JGJ",
    "en": "JAGESHARGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JID",
    "en": "JAGI ROAD",
    "se": "ASSAM"
  },
  {
    "sc": "JGN",
    "en": "JAGRAON",
    "se": "PUNJAB"
  },
  {
    "sc": "JDN",
    "en": "JAGUDAN",
    "se": "GUJARAT"
  },
  {
    "sc": "JHDC",
    "en": "JAHANBAD COURT",
    "se": "BIHAR"
  },
  {
    "sc": "JBR",
    "en": "JAHANGIRABAD RJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JKH",
    "en": "JAHANIKHERA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JJT",
    "en": "JAI JAI WANTI",
    "se": "HARYANA"
  },
  {
    "sc": "JYM",
    "en": "JAI SAMAND ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JCU",
    "en": "JAICHOLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JJJ",
    "en": "JAIJON DOABA",
    "se": "PUNJAB"
  },
  {
    "sc": "JMM",
    "en": "JAIMURTINAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "JNT",
    "en": "JAINTIPURA",
    "se": "PUNJAB"
  },
  {
    "sc": "JRMG",
    "en": "JAIRAMNAGAR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "JAIC",
    "en": "JAIS CITY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JSM",
    "en": "JAISALMER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JSD",
    "en": "JAISINGDER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JTI",
    "en": "JAITHARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JTU",
    "en": "JAITIPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JTKN",
    "en": "JAITPUR KALAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JATP",
    "en": "JAITPURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JES",
    "en": "JAITSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JTW",
    "en": "JAITWAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JJA",
    "en": "JAJAN PATTI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JJ",
    "en": "JAJAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JWL",
    "en": "JAJIWAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JJKR",
    "en": "JAJPUR K ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "JAK",
    "en": "JAKANUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "JHL",
    "en": "JAKHAL JN",
    "se": "HARYANA"
  },
  {
    "sc": "JKB",
    "en": "JAKHALABANDHA",
    "se": "ASSAM"
  },
  {
    "sc": "JLN",
    "en": "JAKHALAUN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JKN",
    "en": "JAKHANIAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JKPR",
    "en": "JAKHAPURA",
    "se": "ODISHA"
  },
  {
    "sc": "JHA",
    "en": "JAKHAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JHN",
    "en": "JAKHIM",
    "se": "BIHAR"
  },
  {
    "sc": "JKHI",
    "en": "JAKHODLKHERA",
    "se": "HARYANA"
  },
  {
    "sc": "JKA",
    "en": "JAKHVADA",
    "se": "GUJARAT"
  },
  {
    "sc": "JKO",
    "en": "JAKKALACHERUVU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "JKAR",
    "en": "JAKLAIR",
    "se": "TELANGANA"
  },
  {
    "sc": "JK",
    "en": "JAKOLARI",
    "se": "PUNJAB"
  },
  {
    "sc": "JPR",
    "en": "JAKPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JKS",
    "en": "JAKSI",
    "se": "GUJARAT"
  },
  {
    "sc": "JLL",
    "en": "JALALGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JAG",
    "en": "JALALGARH",
    "se": "BIHAR"
  },
  {
    "sc": "JGP",
    "en": "JALALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "JPD",
    "en": "JALALPUR DHAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JM",
    "en": "JALAMB JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JRC",
    "en": "JALANDHAR CANT",
    "ec": "JALANDHAR",
    "se": "PUNJAB"
  },
  {
    "sc": "JUC",
    "en": "JALANDHAR CITY",
    "ec": "JALANDHAR",
    "se": "PUNJAB"
  },
  {
    "sc": "JSC",
    "en": "JALESAR CITY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JLS",
    "en": "JALESAR ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JER",
    "en": "JALESWAR",
    "ec": "BALASORE",
    "se": "ODISHA"
  },
  {
    "sc": "JL",
    "en": "JALGAON JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JIL",
    "en": "JALILA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "JNRI",
    "en": "JALINDRI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JA",
    "en": "JALIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "JALD",
    "en": "JALIYA DEVANI",
    "se": "GUJARAT"
  },
  {
    "sc": "JLM",
    "en": "JALIYA MATH",
    "se": "GUJARAT"
  },
  {
    "sc": "JBD",
    "en": "JALLALABD",
    "ec": "FIROZPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "J",
    "en": "JALNA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JOR",
    "en": "JALOR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JPG",
    "en": "JALPAIGURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JPE",
    "en": "JALPAIGURI ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JLQ",
    "en": "JALPUR"
  },
  {
    "sc": "JAC",
    "en": "JALSU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JACN",
    "en": "JALSU NANAK",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JDH",
    "en": "JAM JODHPUR JN",
    "se": "GUJARAT"
  },
  {
    "sc": "WTJ",
    "en": "JAM WANTHALI",
    "se": "GUJARAT"
  },
  {
    "sc": "JAMA",
    "en": "JAMA",
    "se": "JHARKHAND"
  },
  {
    "sc": "JBO",
    "en": "JAMADOBU",
    "se": "JHARKHAND"
  },
  {
    "sc": "JOO",
    "en": "JAMAI OSMANIA",
    "se": "TELANGANA"
  },
  {
    "sc": "JMP",
    "en": "JAMALPUR JN",
    "ec": "JAMALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "JMV",
    "en": "JAMBARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JBB",
    "en": "JAMBUR",
    "se": "GUJARAT"
  },
  {
    "sc": "JMB",
    "en": "JAMBUSAR",
    "se": "GUJARAT"
  },
  {
    "sc": "JMBC",
    "en": "JAMBUSAR CITY",
    "se": "GUJARAT"
  },
  {
    "sc": "JMD",
    "en": "JAMDHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JMG",
    "en": "JAMGA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "JGZ",
    "en": "JAMGAON P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JMI",
    "en": "JAMGURI",
    "se": "ASSAM"
  },
  {
    "sc": "JMKT",
    "en": "JAMIKUNTA",
    "se": "TELANGANA"
  },
  {
    "sc": "JMRA",
    "en": "JAMIRA",
    "se": "ASSAM"
  },
  {
    "sc": "JMQ",
    "en": "JAMIRGHATA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JMDG",
    "en": "JAMMALAMADUGU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "JAM",
    "en": "JAMNAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "JMNR",
    "en": "JAMNER",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JMS",
    "en": "JAMSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JME",
    "en": "JAMSHER KHAS",
    "se": "PUNJAB"
  },
  {
    "sc": "JSE",
    "en": "JAMSOLE",
    "se": "ODISHA"
  },
  {
    "sc": "JMT",
    "en": "JAMTARA",
    "ec": "ASANSOL",
    "se": "JHARKHAND"
  },
  {
    "sc": "JAUA",
    "en": "JAMUA",
    "se": "JHARKHAND"
  },
  {
    "sc": "JMN",
    "en": "JAMUAWAN",
    "se": "BIHAR"
  },
  {
    "sc": "JMU",
    "en": "JAMUI",
    "se": "BIHAR"
  },
  {
    "sc": "JMK",
    "en": "JAMUNAMUKH",
    "se": "ASSAM"
  },
  {
    "sc": "JMX",
    "en": "JAMUNI",
    "se": "JHARKHAND"
  },
  {
    "sc": "JMKL",
    "en": "JAMUNIA KALAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JMA",
    "en": "JAMURIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JVL",
    "en": "JAMWALA",
    "se": "GUJARAT"
  },
  {
    "sc": "JOX",
    "en": "JANAI ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JNKR",
    "en": "JANAKINAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "JNR",
    "en": "JANAKPUR ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "JNL",
    "en": "JANDIALA",
    "se": "PUNJAB"
  },
  {
    "sc": "JDK",
    "en": "JANDOKE",
    "se": "PUNJAB"
  },
  {
    "sc": "JAQ",
    "en": "JANDRAPETA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "JWKA",
    "en": "JANDWALA KHARTA",
    "se": "PUNJAB"
  },
  {
    "sc": "ZN",
    "en": "JANGAON",
    "se": "TELANGANA"
  },
  {
    "sc": "JNH",
    "en": "JANGHAI JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JGG",
    "en": "JANGIGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JRLE",
    "en": "JANGIPUR ROAD",
    "ec": "MALDA TOWN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JNE",
    "en": "JANIYANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NIA",
    "en": "JANJGIR NAILA",
    "ec": "CHAMPA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "JKM",
    "en": "JANKAMPET JN",
    "se": "TELANGANA"
  },
  {
    "sc": "JKDP",
    "en": "JANKIDAIPUR",
    "se": "ODISHA"
  },
  {
    "sc": "JNN",
    "en": "JANUNIATNA",
    "se": "JHARKHAND"
  },
  {
    "sc": "JOA",
    "en": "JANWAL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JAO",
    "en": "JAORA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JPL",
    "en": "JAPLA",
    "se": "JHARKHAND"
  },
  {
    "sc": "JRA",
    "en": "JARAIKELA",
    "se": "ODISHA"
  },
  {
    "sc": "JSV",
    "en": "JARANDESHWAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JAN",
    "en": "JARANGDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "JRPD",
    "en": "JARAPADA",
    "se": "ODISHA"
  },
  {
    "sc": "JUA",
    "en": "JARAUNA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JRJ",
    "en": "JARGAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JARI",
    "en": "JARI",
    "se": "GUJARAT"
  },
  {
    "sc": "JGX",
    "en": "JARIAGARH",
    "se": "JHARKHAND"
  },
  {
    "sc": "JD",
    "en": "JAROD",
    "se": "GUJARAT"
  },
  {
    "sc": "JRLI",
    "en": "JAROLI",
    "se": "ODISHA"
  },
  {
    "sc": "JRT",
    "en": "JARTI",
    "se": "ODISHA"
  },
  {
    "sc": "JDW",
    "en": "JARUDA NARAA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JAW",
    "en": "JARWA"
  },
  {
    "sc": "JLD",
    "en": "JARWAL ROAD",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JSA",
    "en": "JASAI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JSI",
    "en": "JASALI",
    "se": "GUJARAT"
  },
  {
    "sc": "JAS",
    "en": "JASDAN",
    "se": "GUJARAT"
  },
  {
    "sc": "JSS",
    "en": "JASIA",
    "se": "HARYANA"
  },
  {
    "sc": "JSME",
    "en": "JASIDIH JN",
    "ec": "JASIDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "JDA",
    "en": "JASODA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JSPN",
    "en": "JASPALON",
    "se": "PUNJAB"
  },
  {
    "sc": "JSR",
    "en": "JASRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JSL",
    "en": "JASSOWAL",
    "se": "PUNJAB"
  },
  {
    "sc": "JSH",
    "en": "JASWANTGARH"
  },
  {
    "sc": "JGR",
    "en": "JASWANTNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JSKA",
    "en": "JATAULA SAMPHKA",
    "se": "HARYANA"
  },
  {
    "sc": "JTRD",
    "en": "JATH ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JTG",
    "en": "JATINGA"
  },
  {
    "sc": "JGLP",
    "en": "JATINGA LUMPUR",
    "se": "ASSAM"
  },
  {
    "sc": "JTR",
    "en": "JATKANHAR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "JTX",
    "en": "JATPIPLI",
    "se": "GUJARAT"
  },
  {
    "sc": "JTS",
    "en": "JATUSANA",
    "se": "HARYANA"
  },
  {
    "sc": "JW",
    "en": "JATWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JRAE",
    "en": "JAUGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JUK",
    "en": "JAULKA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JKR",
    "en": "JAULKHERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JOP",
    "en": "JAUNPUR CITY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JNU",
    "en": "JAUNPUR JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JVA",
    "en": "JAVALE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JWO",
    "en": "JAWAD ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JWNR",
    "en": "JAWAHARNAGAR",
    "se": "TRIPURA"
  },
  {
    "sc": "JWB",
    "en": "JAWAI BANDH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JAL",
    "en": "JAWALI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JWLS",
    "en": "JAWANWALA SHAHR",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "JMKR",
    "en": "JAWLMUKHI ROAD",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "JSP",
    "en": "JAYASINGPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JYG",
    "en": "JAYNAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "JNM",
    "en": "JAYNGR MAJLIPUR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JHD",
    "en": "JEHANABAD",
    "se": "BIHAR"
  },
  {
    "sc": "JJR",
    "en": "JEJURI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JKT",
    "en": "JEKOT",
    "se": "GUJARAT"
  },
  {
    "sc": "JNZ",
    "en": "JENAL",
    "se": "GUJARAT"
  },
  {
    "sc": "JEN",
    "en": "JENAPUR",
    "se": "ODISHA"
  },
  {
    "sc": "JONR",
    "en": "JEONARA P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JEP",
    "en": "JEONATHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JDD",
    "en": "JERTHI DADHIA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JRK",
    "en": "JERUWA KHERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JLR",
    "en": "JETALSAR JN",
    "se": "GUJARAT"
  },
  {
    "sc": "JTV",
    "en": "JETALVAD",
    "se": "GUJARAT"
  },
  {
    "sc": "JCH",
    "en": "JETHA CHNDAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JDDA",
    "en": "JETHA P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "JTY",
    "en": "JETHI",
    "se": "GUJARAT"
  },
  {
    "sc": "JHK",
    "en": "JETHUKE",
    "se": "PUNJAB"
  },
  {
    "sc": "JTP",
    "en": "JETPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "JEUR",
    "en": "JEUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JYP",
    "en": "JEYPORE",
    "se": "ODISHA"
  },
  {
    "sc": "JBK",
    "en": "JGMBLA KSHNPRM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "JGE",
    "en": "JGNTH TMPL GTE",
    "se": "KERALA"
  },
  {
    "sc": "JBW",
    "en": "JHABELWALI",
    "se": "PUNJAB"
  },
  {
    "sc": "JPI",
    "en": "JHADUPUDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "JGI",
    "en": "JHAGADIYA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "JAJ",
    "en": "JHAJHA",
    "se": "BIHAR"
  },
  {
    "sc": "ZR",
    "en": "JHAJHPOR",
    "se": "GUJARAT"
  },
  {
    "sc": "JHJ",
    "en": "JHAJJAR",
    "se": "HARYANA"
  },
  {
    "sc": "JLWC",
    "en": "JHALAWAR CITY",
    "ec": "RAMGANJ MANDI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JHW",
    "en": "JHALAWAR ROAD",
    "ec": "RAMGANJ MANDI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JAA",
    "en": "JHALIDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JHH",
    "en": "JHALRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JAPN",
    "en": "JHALRAPATAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JLW",
    "en": "JHALWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JLT",
    "en": "JHAMAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JJP",
    "en": "JHANJHARPUR",
    "se": "BIHAR"
  },
  {
    "sc": "JCO",
    "en": "JHANSI C B",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JPH",
    "en": "JHANTIPAHARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JPQ",
    "en": "JHAPANDANGA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JTL",
    "en": "JHAPATER DHAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JHAR",
    "en": "JHAR",
    "se": "GUJARAT"
  },
  {
    "sc": "JRMA",
    "en": "JHARAMUNDA",
    "se": "ODISHA"
  },
  {
    "sc": "JREA",
    "en": "JHAREDA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JKP",
    "en": "JHAREKAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JGM",
    "en": "JHARGRAM",
    "ec": "KHARAGPUR/JHARGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JRI",
    "en": "JHARIA"
  },
  {
    "sc": "JRL",
    "en": "JHARILI",
    "se": "HARYANA"
  },
  {
    "sc": "JKNI",
    "en": "JHARKHANDI",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JRQ",
    "en": "JHAROKHAS",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ZAR",
    "en": "JHAROLA",
    "se": "GUJARAT"
  },
  {
    "sc": "JDI",
    "en": "JHARRADIH",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "JSG",
    "en": "JHARSUGUDA JN",
    "ec": "JHARSUGUDA",
    "se": "ODISHA"
  },
  {
    "sc": "JSGR",
    "en": "JHARSUGUDA ROAD",
    "ec": "JHARSUGUDA",
    "se": "ODISHA"
  },
  {
    "sc": "JRTB",
    "en": "JHARTARBHA",
    "se": "ODISHA"
  },
  {
    "sc": "JWS",
    "en": "JHARWASAA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JAU",
    "en": "JHAUA",
    "se": "BIHAR"
  },
  {
    "sc": "JHWR",
    "en": "JHAWAR",
    "se": "PUNJAB"
  },
  {
    "sc": "JLHI",
    "en": "JHILAHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JLY",
    "en": "JHILMILI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JLLO",
    "en": "JHILO",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JHMR",
    "en": "JHIMRI",
    "se": "JHARKHAND"
  },
  {
    "sc": "JHG",
    "en": "JHINGURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JJK",
    "en": "JHINJHAK",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JNK",
    "en": "JHINKPANI",
    "se": "JHARKHAND"
  },
  {
    "sc": "JHIR",
    "en": "JHIR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JTK",
    "en": "JHITKIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JTH",
    "en": "JHOKTAHAL SING",
    "se": "PUNJAB"
  },
  {
    "sc": "JUL",
    "en": "JHULASAN",
    "se": "GUJARAT"
  },
  {
    "sc": "JN",
    "en": "JHUND",
    "se": "GUJARAT"
  },
  {
    "sc": "JJN",
    "en": "JHUNJHUNUN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JUP",
    "en": "JHUNPA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JI",
    "en": "JHUSI",
    "ec": "PRAYAGRAJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JJG",
    "en": "JIAGANJ",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JVT",
    "en": "JIBANTI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JIA",
    "en": "JIGNA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JGKS",
    "en": "JIGNI KHAS",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JMPT",
    "en": "JIMIDIPETA",
    "se": "ODISHA"
  },
  {
    "sc": "JCY",
    "en": "JIND CITY",
    "se": "HARYANA"
  },
  {
    "sc": "JIND",
    "en": "JIND JN",
    "se": "HARYANA"
  },
  {
    "sc": "JNTR",
    "en": "JINTI ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JIR",
    "en": "JIRA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "ZRDE",
    "en": "JIRADEI",
    "se": "BIHAR"
  },
  {
    "sc": "JRNA",
    "en": "JIRANIA",
    "se": "TRIPURA"
  },
  {
    "sc": "JIT",
    "en": "JIRAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JRBM",
    "en": "JIRIBAM",
    "se": "MANIPUR"
  },
  {
    "sc": "JRO",
    "en": "JIRON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JXN",
    "en": "JIRONA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JRWN",
    "en": "JIRWAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JKZ",
    "en": "JITAKHERI",
    "se": "HARYANA"
  },
  {
    "sc": "JITE",
    "en": "JITE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JEO",
    "en": "JITODA",
    "se": "GUJARAT"
  },
  {
    "sc": "JWN",
    "en": "JIWA ARAIN",
    "se": "PUNJAB"
  },
  {
    "sc": "JDR",
    "en": "JIWDHARA",
    "se": "BIHAR"
  },
  {
    "sc": "JPM",
    "en": "JIYAPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "JPP",
    "en": "JLALPR PANWARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JPS",
    "en": "JMLPR SHAIKHAN",
    "se": "HARYANA"
  },
  {
    "sc": "JHBN",
    "en": "JMTPUR BAHARAN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JPV",
    "en": "JMTRA PARASWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JNUK",
    "en": "JNPUR KUTCHERRY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JO",
    "en": "JO JAGABOR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JOBA",
    "en": "JOBA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JOK",
    "en": "JODHKA",
    "se": "HARYANA"
  },
  {
    "sc": "JUCT",
    "en": "JODHPUR CANTT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JOL",
    "en": "JOGAL",
    "se": "ODISHA"
  },
  {
    "sc": "JBN",
    "en": "JOGBANI",
    "se": "BIHAR"
  },
  {
    "sc": "JGNR",
    "en": "JOGENDRANAGAR",
    "se": "TRIPURA"
  },
  {
    "sc": "JOS",
    "en": "JOGESHVARI",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JGBR",
    "en": "JOGESWAR BIHAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "JOM",
    "en": "JOGI MAGRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JGA",
    "en": "JOGIARA",
    "se": "BIHAR"
  },
  {
    "sc": "JGF",
    "en": "JOGIDIH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JPZ",
    "en": "JOGIGHOPA",
    "se": "ASSAM"
  },
  {
    "sc": "JDNX",
    "en": "JOGINDER NAGAR",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "JGW",
    "en": "JOGIWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "JJW",
    "en": "JOJWA",
    "se": "GUJARAT"
  },
  {
    "sc": "JTJ",
    "en": "JOLARPETTAI JN",
    "ec": "JOLARPETTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "JYK",
    "en": "JONE KARRANG",
    "se": "ASSAM"
  },
  {
    "sc": "JON",
    "en": "JONHA",
    "se": "JHARKHAND"
  },
  {
    "sc": "JPO",
    "en": "JORA ALAPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JOQ",
    "en": "JORAI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JRW",
    "en": "JORAMOW",
    "se": "JHARKHAND"
  },
  {
    "sc": "JRZ",
    "en": "JORANDA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "JVN",
    "en": "JORAVARNAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "JRS",
    "en": "JORAVASAN",
    "se": "GUJARAT"
  },
  {
    "sc": "JTTN",
    "en": "JORHAT TOWN",
    "ec": "JORHAT",
    "se": "ASSAM"
  },
  {
    "sc": "JRKN",
    "en": "JORKIAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JTN",
    "en": "JOTANA",
    "se": "GUJARAT"
  },
  {
    "sc": "JOC",
    "en": "JOYCHANDI PAHAR",
    "ec": "ADRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "JCNR",
    "en": "JUCHANDRA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JRR",
    "en": "JUGAUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JGJN",
    "en": "JUGIJAN",
    "se": "ASSAM"
  },
  {
    "sc": "JRG",
    "en": "JUGPURA",
    "se": "ODISHA"
  },
  {
    "sc": "JOH",
    "en": "JUHARPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JUJA",
    "en": "JUJUMURA",
    "se": "ODISHA"
  },
  {
    "sc": "JKE",
    "en": "JUKEHI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JNA",
    "en": "JULANA",
    "se": "HARYANA"
  },
  {
    "sc": "JLG",
    "en": "JULGAON DECCAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "JML",
    "en": "JUMNAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "JRV",
    "en": "JUNA RAJUVADIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "JND",
    "en": "JUNAGADH JN",
    "se": "GUJARAT"
  },
  {
    "sc": "JNRD",
    "en": "JUNAGARH ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "JAKA",
    "en": "JUNAKHERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "JHT",
    "en": "JUNEHTA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JBG",
    "en": "JUNG BAHADURGNJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JCN",
    "en": "JUNICHAVAND",
    "se": "GUJARAT"
  },
  {
    "sc": "JNO",
    "en": "JUNNOR DEO",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "JTO",
    "en": "JUTOGH",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "JUR",
    "en": "JUTURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "JWP",
    "en": "JWALAPUR",
    "ec": "HARIDWAR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "JWK",
    "en": "JWHRPUR KAMSAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KIAD",
    "en": "K I AIRPORT H",
    "se": "KARNATAKA"
  },
  {
    "sc": "KBPR",
    "en": "KABAKAPUTTUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KBR",
    "en": "KABRAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KCHV",
    "en": "KACHCHANVILAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KWN",
    "en": "KACHEWANI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KCO",
    "en": "KACHHIA BRIDGE",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KCU",
    "en": "KACHHIAA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KEQ",
    "en": "KACHHPURA",
    "ec": "JABALPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KWH",
    "en": "KACHHWA ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KAU",
    "en": "KACHNA",
    "se": "BIHAR"
  },
  {
    "sc": "KHNR",
    "en": "KACHNARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KCNR",
    "en": "KACHNARA ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KNRA",
    "en": "KACHNARIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KOX",
    "en": "KACHUJOR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KDAA",
    "en": "KADA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KVU",
    "en": "KADAKAVUR",
    "se": "KERALA"
  },
  {
    "sc": "KDO",
    "en": "KADAKOLA",
    "se": "KARNATAKA"
  },
  {
    "sc": "KN",
    "en": "KADALUNDI",
    "se": "KERALA"
  },
  {
    "sc": "KMBK",
    "en": "KADAMBANKULAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KBT",
    "en": "KADAMBATTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KDU",
    "en": "KADAMBUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KDRA",
    "en": "KADAMPURA",
    "se": "BIHAR"
  },
  {
    "sc": "KDYA",
    "en": "KADARPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "KDVI",
    "en": "KADAVAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KVDU",
    "en": "KADAVAKUDURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KDNL",
    "en": "KADAYANALLUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KDTN",
    "en": "KADETHAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KADI",
    "en": "KADI",
    "se": "GUJARAT"
  },
  {
    "sc": "KDQ",
    "en": "KADIPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KRY",
    "en": "KADIRI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KADR",
    "en": "KADIYADRA",
    "se": "GUJARAT"
  },
  {
    "sc": "KYM",
    "en": "KADIYAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KLM",
    "en": "KADLIMATTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KRYP",
    "en": "KADRIDEVARPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "DRU",
    "en": "KADUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KFPR",
    "en": "KAFURPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KAGR",
    "en": "KAGANGARH",
    "se": "PUNJAB"
  },
  {
    "sc": "KEY",
    "en": "KAGANKARAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KGWD",
    "en": "KAGWAD",
    "se": "GUJARAT"
  },
  {
    "sc": "CLG",
    "en": "KAHALGAON",
    "ec": "BHAGALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "KRAI",
    "en": "KAHET",
    "se": "GUJARAT"
  },
  {
    "sc": "KH",
    "en": "KAHILIYA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KIV",
    "en": "KAIALSA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KCY",
    "en": "KAICHAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KKAE",
    "en": "KAIKALA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KKLR",
    "en": "KAIKALUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KKRM",
    "en": "KAIKORAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KYT",
    "en": "KAILAHAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KQS",
    "en": "KAILARAS",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KLPM",
    "en": "KAILASAPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KALI",
    "en": "KAILI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KMA",
    "en": "KAIMA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KMJ",
    "en": "KAIMGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KPXR",
    "en": "KAIPADA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "KAI",
    "en": "KAIRLA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KCZ",
    "en": "KAIRON",
    "se": "PUNJAB"
  },
  {
    "sc": "KLE",
    "en": "KAITHAL",
    "se": "HARYANA"
  },
  {
    "sc": "KTCH",
    "en": "KAITHALKUCHI",
    "se": "ASSAM"
  },
  {
    "sc": "KYSD",
    "en": "KAIYAL SEDHAVI",
    "se": "GUJARAT"
  },
  {
    "sc": "KJ",
    "en": "KAJGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KJTW",
    "en": "KAJGAON TERHWAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KJME",
    "en": "KAJORAGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KJH",
    "en": "KAJRA",
    "ec": "JAMALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "KYF",
    "en": "KAJRAT NAWADIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "KFT",
    "en": "KAJRI",
    "se": "JHARKHAND"
  },
  {
    "sc": "KAPE",
    "en": "KAKAPORA",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "KKHT",
    "en": "KAKARGHATTI",
    "se": "BIHAR"
  },
  {
    "sc": "COA",
    "en": "KAKINADA PORT",
    "ec": "KAKINADA PORT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CCT",
    "en": "KAKINADA TOWN",
    "ec": "KAKINADA PORT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KKGM",
    "en": "KAKIRIGUMMA",
    "se": "ODISHA"
  },
  {
    "sc": "KKLU",
    "en": "KAKLUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KAKI",
    "en": "KAKNI HALT",
    "se": "JHARKHAND"
  },
  {
    "sc": "KKJ",
    "en": "KAKORI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KARH",
    "en": "KAKRAHA RST HSE",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KKRL",
    "en": "KAKRALA",
    "se": "PUNJAB"
  },
  {
    "sc": "KQE",
    "en": "KALA AKHAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KKL",
    "en": "KALA BAKRA",
    "se": "PUNJAB"
  },
  {
    "sc": "KLBG",
    "en": "KALABURAGI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KQI",
    "en": "KALACHAND",
    "se": "ASSAM"
  },
  {
    "sc": "KDHI",
    "en": "KALADEHI P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KLGA",
    "en": "KALAGAR",
    "se": "ODISHA"
  },
  {
    "sc": "KKQ",
    "en": "KALAIKUNDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KMH",
    "en": "KALAMALLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KLMR",
    "en": "KALAMASSERI",
    "se": "KERALA"
  },
  {
    "sc": "KMRD",
    "en": "KALAMB ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KLBN",
    "en": "KALAMBANI BUDRK",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KLBA",
    "en": "KALAMBHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KLMG",
    "en": "KALAMBOLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KLMC",
    "en": "KALAMBOLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KAV",
    "en": "KALAMNA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KALN",
    "en": "KALANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KLAD",
    "en": "KALANAD",
    "se": "KERALA"
  },
  {
    "sc": "KLNK",
    "en": "KALANAUR KALAN",
    "se": "HARYANA"
  },
  {
    "sc": "KLGN",
    "en": "KALANGANI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KNZ",
    "en": "KALANOUR",
    "se": "HARYANA"
  },
  {
    "sc": "KNL",
    "en": "KALANWALI",
    "se": "HARYANA"
  },
  {
    "sc": "KPP",
    "en": "KALAPIPAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KALS",
    "en": "KALASA H",
    "se": "KARNATAKA"
  },
  {
    "sc": "KCM",
    "en": "KALASAMUDRAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KLSR",
    "en": "KALASAR",
    "se": "GUJARAT"
  },
  {
    "sc": "KLVD",
    "en": "KALAVAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KIY",
    "en": "KALAYAT",
    "se": "HARYANA"
  },
  {
    "sc": "KCF",
    "en": "KALCHINI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KLDI",
    "en": "KALDHARI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KLDA",
    "en": "KALEDIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "KM",
    "en": "KALEEM",
    "se": "GOA"
  },
  {
    "sc": "KCP",
    "en": "KALGUPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KAH",
    "en": "KALHAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KLMJ",
    "en": "KALHE MAJRA",
    "se": "PUNJAB"
  },
  {
    "sc": "KLRD",
    "en": "KALI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KSH",
    "en": "KALI SINDH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KXE",
    "en": "KALIAN CHAK",
    "se": "JHARKHAND"
  },
  {
    "sc": "KAP",
    "en": "KALIANPUR",
    "ec": "KANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KLKR",
    "en": "KALIKAPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KCI",
    "en": "KALIKIRI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KLNP",
    "en": "KALINARYNPUR JN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KPK",
    "en": "KALIPAHARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KISN",
    "en": "KALISEN PH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KLWD",
    "en": "KALITALAVDI",
    "se": "GUJARAT"
  },
  {
    "sc": "KAJ",
    "en": "KALIYAGANJ",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KLK",
    "en": "KALKA",
    "ec": "KALKA",
    "se": "HARYANA"
  },
  {
    "sc": "KKGT",
    "en": "KALKALIGHAT",
    "se": "ASSAM"
  },
  {
    "sc": "KKD",
    "en": "KALKUND",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KLKD",
    "en": "KALLADAKA",
    "se": "GUJARAT"
  },
  {
    "sc": "KLGM",
    "en": "KALLAGAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KKPM",
    "en": "KALLAKKUDI PLGH",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KAL",
    "en": "KALLAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KUL",
    "en": "KALLAYI",
    "se": "KERALA"
  },
  {
    "sc": "KIC",
    "en": "KALLIDAIKURICHI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KGD",
    "en": "KALLIGUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KLYH",
    "en": "KALLUR YEDAHLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KLU",
    "en": "KALLURU JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KSWR",
    "en": "KALMESHWAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KLTR",
    "en": "KALMITAR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KLL",
    "en": "KALOL",
    "se": "GUJARAT"
  },
  {
    "sc": "KFC",
    "en": "KALPATTICHATRAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KPI",
    "en": "KALPI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KVS",
    "en": "KALSUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KTHY",
    "en": "KALTHURUTHY",
    "se": "KERALA"
  },
  {
    "sc": "KAO",
    "en": "KALUBATHAN",
    "se": "JHARKHAND"
  },
  {
    "sc": "KLG",
    "en": "KALUNGA",
    "se": "ODISHA"
  },
  {
    "sc": "KAPG",
    "en": "KALUPARA GHAT",
    "se": "ODISHA"
  },
  {
    "sc": "KMB",
    "en": "KALV AMBA",
    "se": "GUJARAT"
  },
  {
    "sc": "KLVA",
    "en": "KALVA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KLWN",
    "en": "KALWAN",
    "se": "HARYANA"
  },
  {
    "sc": "KYND",
    "en": "KALYANADURGA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KYI",
    "en": "KALYANI",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KYNT",
    "en": "KALYANKOT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KYP",
    "en": "KALYANPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KPRD",
    "en": "KALYANPUR ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "KYB",
    "en": "KALYAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KYQ",
    "en": "KAMAKHYA",
    "ec": "GUWAHATI",
    "se": "ASSAM"
  },
  {
    "sc": "KAMG",
    "en": "KAMAKHYAGURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KMPU",
    "en": "KAMALAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KKM",
    "en": "KAMALAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KLJ",
    "en": "KAMALGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KMNR",
    "en": "KAMALNAGAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KAMP",
    "en": "KAMALPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KLPG",
    "en": "KAMALPURGRAM",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KMLR",
    "en": "KAMALUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KARD",
    "en": "KAMAN ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KXL",
    "en": "KAMARBANDHA ALI",
    "se": "ASSAM"
  },
  {
    "sc": "KMC",
    "en": "KAMAREDDI",
    "se": "TELANGANA"
  },
  {
    "sc": "KQU",
    "en": "KAMARKUNDU",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KSM",
    "en": "KAMASAMUDRAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "KMAH",
    "en": "KAMATHE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KBBP",
    "en": "KAMBIRON",
    "se": "MANIPUR"
  },
  {
    "sc": "KBI",
    "en": "KAMBRGANVI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KPH",
    "en": "KAMEPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KMP",
    "en": "KAMLAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KMLI",
    "en": "KAMLI",
    "se": "GUJARAT"
  },
  {
    "sc": "KMRA",
    "en": "KAMNARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KXF",
    "en": "KAMPIL ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KP",
    "en": "KAMPTEE",
    "ec": "NAGPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KWM",
    "en": "KAMPUR",
    "se": "ASSAM"
  },
  {
    "sc": "KKET",
    "en": "KAMRUP KHETRI",
    "se": "ASSAM"
  },
  {
    "sc": "KMST",
    "en": "KAMSHET",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KML",
    "en": "KAMTAUL",
    "se": "BIHAR"
  },
  {
    "sc": "KNAD",
    "en": "KANAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KNBR",
    "en": "KANAIBAZAR",
    "se": "ASSAM"
  },
  {
    "sc": "KNKT",
    "en": "KANAKOT",
    "se": "GUJARAT"
  },
  {
    "sc": "KKU",
    "en": "KANAKPURA",
    "ec": "JAIPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KNLS",
    "en": "KANALAS JN",
    "se": "GUJARAT"
  },
  {
    "sc": "KNLE",
    "en": "KANALE",
    "se": "KARNATAKA"
  },
  {
    "sc": "KNLP",
    "en": "KANAMALO PALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KNRN",
    "en": "KANAROAN",
    "se": "JHARKHAND"
  },
  {
    "sc": "KASR",
    "en": "KANAS ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "KNSR",
    "en": "KANASAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KUT",
    "en": "KANAUTA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KNS",
    "en": "KANCHAUSI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CJ",
    "en": "KANCHIPURAM",
    "ec": "KANCHIPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KPA",
    "en": "KANCHRAPARA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KDZ",
    "en": "KANDAGHAT",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "KDMD",
    "en": "KANDAMBAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KNPL",
    "en": "KANDANUR P VAYA",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KNDR",
    "en": "KANDARI",
    "se": "GUJARAT"
  },
  {
    "sc": "KDRP",
    "en": "KANDARPUR",
    "se": "ODISHA"
  },
  {
    "sc": "KDLR",
    "en": "KANDEL ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "KQL",
    "en": "KANDHLA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KILE",
    "en": "KANDIVLI",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KAND",
    "en": "KANDLA",
    "se": "GUJARAT"
  },
  {
    "sc": "KDLP",
    "en": "KANDLA PORT",
    "se": "GUJARAT"
  },
  {
    "sc": "KND",
    "en": "KANDRA",
    "se": "JHARKHAND"
  },
  {
    "sc": "KNDI",
    "en": "KANDRORI",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "KGKD",
    "en": "KANG KHURD",
    "se": "PUNJAB"
  },
  {
    "sc": "KNGM",
    "en": "KANGAM",
    "se": "GUJARAT"
  },
  {
    "sc": "KGX",
    "en": "KANGINHAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "KGRA",
    "en": "KANGRA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "KGMR",
    "en": "KANGRA MANDIR",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "KNHP",
    "en": "KANHAIPUR",
    "se": "BIHAR"
  },
  {
    "sc": "KNHN",
    "en": "KANHAN JN",
    "ec": "NAGPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KZE",
    "en": "KANHANGAD",
    "se": "KERALA"
  },
  {
    "sc": "KNRG",
    "en": "KANHARGAON NAKA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KNHE",
    "en": "KANHE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KNGN",
    "en": "KANHEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KANJ",
    "en": "KANIL",
    "se": "GUJARAT"
  },
  {
    "sc": "KNNK",
    "en": "KANINA KHAS",
    "se": "HARYANA"
  },
  {
    "sc": "KNYR",
    "en": "KANIURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "KNVH",
    "en": "KANIVEHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KWB",
    "en": "KANIWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KNB",
    "en": "KANIYAMBADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KXP",
    "en": "KANIYAPURAM",
    "se": "KERALA"
  },
  {
    "sc": "KBRV",
    "en": "KANJARI BORIYAV",
    "se": "GUJARAT"
  },
  {
    "sc": "KNU",
    "en": "KANJH",
    "se": "GUJARAT"
  },
  {
    "sc": "KJKD",
    "en": "KANJIKODE",
    "se": "KERALA"
  },
  {
    "sc": "KPTM",
    "en": "KANJIRAMITTAM",
    "se": "KERALA"
  },
  {
    "sc": "KXB",
    "en": "KANJIYA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KKAH",
    "en": "KANKAHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KHE",
    "en": "KANKATHER",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KKW",
    "en": "KANKAVALI",
    "ec": "RATNAGIRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KKA",
    "en": "KANKI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KNR",
    "en": "KANKINARA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KMZA",
    "en": "KANKRA MIRZANGR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KDL",
    "en": "KANKROLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KMM",
    "en": "KANNAMANGALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KPQ",
    "en": "KANNAPURAM",
    "se": "KERALA"
  },
  {
    "sc": "KJN",
    "en": "KANNAUJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KJNC",
    "en": "KANNAUJ CITY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KANO",
    "en": "KANOH",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "KFN",
    "en": "KANOR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CPA",
    "en": "KANPUR ANWRGANJ",
    "ec": "KANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CPB",
    "en": "KANPUR BGE L BK",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CPSM",
    "en": "KANPUR SMU CBSA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KXN",
    "en": "KANSHBAHAL",
    "se": "ODISHA"
  },
  {
    "sc": "KANS",
    "en": "KANSIYA NES",
    "se": "GUJARAT"
  },
  {
    "sc": "KSQ",
    "en": "KANSPUR GUGAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "QSR",
    "en": "KANSRAO",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "KIZ",
    "en": "KANSUDHI",
    "se": "GUJARAT"
  },
  {
    "sc": "KBJ",
    "en": "KANTABANJI",
    "se": "ODISHA"
  },
  {
    "sc": "KTD",
    "en": "KANTADIH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KPL",
    "en": "KANTAKAPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KNHL",
    "en": "KANTENAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KNT",
    "en": "KANTH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KNTR",
    "en": "KANTHARIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "KATI",
    "en": "KANTHI P H",
    "ec": "DIGHA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KTI",
    "en": "KANTI",
    "se": "BIHAR"
  },
  {
    "sc": "KIW",
    "en": "KANWALPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KUW",
    "en": "KANWAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KAWT",
    "en": "KANWAT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "CAPE",
    "en": "KANYAKUMARI",
    "ec": "KANYAKUMARI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KAOT",
    "en": "KAOTHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KVNJ",
    "en": "KAPADVANJ",
    "se": "GUJARAT"
  },
  {
    "sc": "KPLD",
    "en": "KAPALI ROAD PH",
    "se": "ODISHA"
  },
  {
    "sc": "KPNA",
    "en": "KAPAN P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KVC",
    "en": "KAPARPURA",
    "se": "BIHAR"
  },
  {
    "sc": "KIN",
    "en": "KAPASAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KIS",
    "en": "KAPILAS ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "KFI",
    "en": "KAPPIL",
    "se": "KERALA"
  },
  {
    "sc": "KPZ",
    "en": "KAPREN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KEH",
    "en": "KAPSETI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CPJ",
    "en": "KAPTANGANJ JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KPDH",
    "en": "KAPURDHA HALT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KXH",
    "en": "KAPURTHALA",
    "ec": "JALANDHAR",
    "se": "PUNJAB"
  },
  {
    "sc": "KTNI",
    "en": "KAPUSTALNI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRBO",
    "en": "KARABOH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KRD",
    "en": "KARAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CRR",
    "en": "KARAGOLA ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "KKRH",
    "en": "KARAHIYA HALT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KIK",
    "en": "KARAIKAL",
    "ec": "NAGAPPATTINAM/VELANKANNI/KARAIKAL",
    "se": "PUDUCHERRY"
  },
  {
    "sc": "KKDI",
    "en": "KARAIKKUDI JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KARK",
    "en": "KARAIKKURICHI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KRLR",
    "en": "KARAILA ROAD JN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KAY",
    "en": "KARAIMADAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KHV",
    "en": "KARAINTHI",
    "se": "HARYANA"
  },
  {
    "sc": "KJG",
    "en": "KARAJGI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KKB",
    "en": "KARAK BEL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KRKD",
    "en": "KARAKAD",
    "se": "KERALA"
  },
  {
    "sc": "KVLS",
    "en": "KARAKAVALASA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KEB",
    "en": "KARAMBELI",
    "se": "GUJARAT"
  },
  {
    "sc": "KRSH",
    "en": "KARAMGARH SDRGH",
    "se": "PUNJAB"
  },
  {
    "sc": "KMS",
    "en": "KARAMNASA",
    "se": "BIHAR"
  },
  {
    "sc": "KRYR",
    "en": "KARAMSAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KRMA",
    "en": "KARAMTOLA",
    "se": "JHARKHAND"
  },
  {
    "sc": "KANG",
    "en": "KARAN NAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "KRNH",
    "en": "KARANAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KRJA",
    "en": "KARANJA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRJT",
    "en": "KARANJA TOWN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KFD",
    "en": "KARANJADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KAJG",
    "en": "KARANJGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KPTO",
    "en": "KARANPUR ATO",
    "se": "JHARKHAND"
  },
  {
    "sc": "KPO",
    "en": "KARANPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KNWS",
    "en": "KARANWAS",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KFY",
    "en": "KARAPGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KRQ",
    "en": "KARARI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KSGL",
    "en": "KARASANGAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KTGG",
    "en": "KARATAGI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KRDN",
    "en": "KARAUNDHANA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KWO",
    "en": "KARAUTA",
    "se": "BIHAR"
  },
  {
    "sc": "KRV",
    "en": "KARAVADI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KBN",
    "en": "KARBIGWAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KCN",
    "en": "KARCHANA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KDHA",
    "en": "KARCHHA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KYW",
    "en": "KARCHHUE",
    "se": "BIHAR"
  },
  {
    "sc": "KCHA",
    "en": "KARCHIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "RDI",
    "en": "KARDI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KBGH",
    "en": "KAREA KDMBGACHI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KY",
    "en": "KARELI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KEG",
    "en": "KARENGI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KRA",
    "en": "KAREPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "KRPR",
    "en": "KAREPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KGB",
    "en": "KARGI ROAD",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KAHL",
    "en": "KARHAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KYX",
    "en": "KARHIYA BHADELI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KGW",
    "en": "KARIGANURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "KYY",
    "en": "KARIHA",
    "se": "PUNJAB"
  },
  {
    "sc": "KXJ",
    "en": "KARIMGANJ JN",
    "ec": "KARIMGANJ",
    "se": "ASSAM"
  },
  {
    "sc": "KRMR",
    "en": "KARIMNAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "KMDR",
    "en": "KARIMUDDIN PUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KRS",
    "en": "KARISATH",
    "se": "BIHAR"
  },
  {
    "sc": "KXY",
    "en": "KARIYAPATTINAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KJRA",
    "en": "KARJANA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KJRM",
    "en": "KARJANAGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KJT",
    "en": "KARJAT",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRJD",
    "en": "KARJODA",
    "se": "GUJARAT"
  },
  {
    "sc": "KKI",
    "en": "KARKELI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KRKN",
    "en": "KARKEND",
    "se": "JHARKHAND"
  },
  {
    "sc": "KEK",
    "en": "KARKHELI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRMB",
    "en": "KARMABAD",
    "se": "JHARKHAND"
  },
  {
    "sc": "KMV",
    "en": "KARMAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRMI",
    "en": "KARMALI",
    "ec": "MADGAON",
    "se": "GOA"
  },
  {
    "sc": "KRMY",
    "en": "KARMALIYAPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "KAR",
    "en": "KARNA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KNSN",
    "en": "KARNA SUBARNA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KUN",
    "en": "KARNAL",
    "se": "HARYANA"
  },
  {
    "sc": "KOA",
    "en": "KARONDA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KJZ",
    "en": "KARONJI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KPGM",
    "en": "KARPURIGRAM",
    "se": "BIHAR"
  },
  {
    "sc": "KRRA",
    "en": "KARRA",
    "se": "JHARKHAND"
  },
  {
    "sc": "KSDE",
    "en": "KARSINDHU",
    "se": "HARYANA"
  },
  {
    "sc": "KRE",
    "en": "KARTARPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "KRTL",
    "en": "KARTAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KUC",
    "en": "KARUKKUTTY",
    "se": "KERALA"
  },
  {
    "sc": "KPY",
    "en": "KARUNAGAPALLI",
    "se": "KERALA"
  },
  {
    "sc": "KGZ",
    "en": "KARUNGUZHI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KYR",
    "en": "KARUPPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KPPR",
    "en": "KARUPPUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KRR",
    "en": "KARUR JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KVLR",
    "en": "KARUVALLI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KWD",
    "en": "KARWANDIA",
    "se": "BIHAR"
  },
  {
    "sc": "KAWR",
    "en": "KARWAR",
    "ec": "KARWAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KSRA",
    "en": "KASARA",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KGQ",
    "en": "KASARAGOD",
    "se": "KERALA"
  },
  {
    "sc": "KUB",
    "en": "KASBA",
    "se": "BIHAR"
  },
  {
    "sc": "KBSN",
    "en": "KASBE SUKENE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KEE",
    "en": "KASEETAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "KSJ",
    "en": "KASGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KHST",
    "en": "KASHANATTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KEI",
    "en": "KASHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KSC",
    "en": "KASHI CHAK",
    "se": "BIHAR"
  },
  {
    "sc": "KNGR",
    "en": "KASHINAGAR",
    "se": "ODISHA"
  },
  {
    "sc": "KPV",
    "en": "KASHIPUR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "KSPR",
    "en": "KASHIPURA SARAR",
    "se": "GUJARAT"
  },
  {
    "sc": "KSTH",
    "en": "KASHTI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KSK",
    "en": "KASIMKOTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KSTA",
    "en": "KASTHA",
    "se": "BIHAR"
  },
  {
    "sc": "KTBR",
    "en": "KASTURBA NAGAR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KSR",
    "en": "KASTURI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KASU",
    "en": "KASU",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KBU",
    "en": "KASU BEGU",
    "se": "PUNJAB"
  },
  {
    "sc": "KXX",
    "en": "KATA ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KTHE",
    "en": "KATAHRI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KTDD",
    "en": "KATAIYA DANDI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KTX",
    "en": "KATAKHAL JN",
    "se": "ASSAM"
  },
  {
    "sc": "KGE",
    "en": "KATANGI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KTKD",
    "en": "KATANGI KHURD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KZW",
    "en": "KATAR SINGHWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "KTRH",
    "en": "KATAREAH",
    "se": "BIHAR"
  },
  {
    "sc": "KATR",
    "en": "KATARIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "KTP",
    "en": "KATEPURNA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KKT",
    "en": "KATH KUIYAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KTAL",
    "en": "KATHAL",
    "se": "GUJARAT"
  },
  {
    "sc": "KTPR",
    "en": "KATHAL PUKHURI",
    "se": "ASSAM"
  },
  {
    "sc": "KTNA",
    "en": "KATHANA",
    "se": "GUJARAT"
  },
  {
    "sc": "KTRR",
    "en": "KATHARA ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KGF",
    "en": "KATHGHAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KGM",
    "en": "KATHGODAM",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "KEJ",
    "en": "KATHLEEGHAT",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "KTHL",
    "en": "KATHOLA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KTHU",
    "en": "KATHUA",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "KNG",
    "en": "KATHUNANGAL",
    "se": "PUNJAB"
  },
  {
    "sc": "KTWS",
    "en": "KATHUWAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KIR",
    "en": "KATIHAR JN",
    "ec": "KATIHAR",
    "se": "BIHAR"
  },
  {
    "sc": "KATA",
    "en": "KATILI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KFK",
    "en": "KATKA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KTLA",
    "en": "KATKOLA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "KKMP",
    "en": "KATLAKUNTA MEDI",
    "se": "TELANGANA"
  },
  {
    "sc": "KLCR",
    "en": "KATLICHERRA",
    "se": "ASSAM"
  },
  {
    "sc": "KTE",
    "en": "KATNI",
    "ec": "KATNI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KMZ",
    "en": "KATNI MURWARA",
    "ec": "KATNI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KTES",
    "en": "KATNI SOUTH",
    "ec": "KATNI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KTCE",
    "en": "KATOGHAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KATL",
    "en": "KATOL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KTO",
    "en": "KATORA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KTRD",
    "en": "KATOSAN ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KFH",
    "en": "KATPHAL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KEA",
    "en": "KATRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KTH",
    "en": "KATRASGARH",
    "se": "JHARKHAND"
  },
  {
    "sc": "KTAI",
    "en": "KATTALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "CTM",
    "en": "KATTANGULATTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KTTR",
    "en": "KATTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KTDA",
    "en": "KATUDA",
    "se": "GUJARAT"
  },
  {
    "sc": "KWAE",
    "en": "KATWA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KWF",
    "en": "KATWA"
  },
  {
    "sc": "KWBR",
    "en": "KATWAR BAZAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KQQ",
    "en": "KAUKUNTLA",
    "se": "TELANGANA"
  },
  {
    "sc": "KLI",
    "en": "KAULI",
    "se": "PUNJAB"
  },
  {
    "sc": "KLSX",
    "en": "KAULSERI",
    "se": "PUNJAB"
  },
  {
    "sc": "KAA",
    "en": "KAURARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KUF",
    "en": "KAURHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JKI",
    "en": "KAURIAA JUNGLE",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KYA",
    "en": "KAURIYA",
    "se": "BIHAR"
  },
  {
    "sc": "KPE",
    "en": "KAUWAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KVE",
    "en": "KAVALANDE",
    "se": "KARNATAKA"
  },
  {
    "sc": "KVZ",
    "en": "KAVALI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KVN",
    "en": "KAVANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KVP",
    "en": "KAVARAIPPETTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KVA",
    "en": "KAVAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KVK",
    "en": "KAVATHE MAHANKL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KAVI",
    "en": "KAVI",
    "se": "GUJARAT"
  },
  {
    "sc": "KVM",
    "en": "KAVUTARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KWGN",
    "en": "KAWARGAON",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KWNI",
    "en": "KAWNPUI",
    "se": "MIZORAM"
  },
  {
    "sc": "KZY",
    "en": "KAYALPATTINAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "QMRS",
    "en": "KAYAMSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KYJ",
    "en": "KAYANKULAM JN",
    "se": "KERALA"
  },
  {
    "sc": "KAYR",
    "en": "KAYAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KTGM",
    "en": "KAYASTHAGRAM",
    "se": "ASSAM"
  },
  {
    "sc": "KV",
    "en": "KAYAVAROHAN",
    "se": "GUJARAT"
  },
  {
    "sc": "KZK",
    "en": "KAZHAKUTTAM",
    "se": "KERALA"
  },
  {
    "sc": "KZPR",
    "en": "KAZIPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KZJ",
    "en": "KAZIPET JN",
    "ec": "WARANGAL",
    "se": "TELANGANA"
  },
  {
    "sc": "KCKI",
    "en": "KECKHI",
    "se": "JHARKHAND"
  },
  {
    "sc": "KDG",
    "en": "KEDGAON",
    "ec": "PUNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRUR",
    "en": "KEERANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KKG",
    "en": "KEKATUMAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KEV",
    "en": "KELA DEVI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KMLM",
    "en": "KELAMANGALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KEP",
    "en": "KELANPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "KLY",
    "en": "KELAVLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KLOD",
    "en": "KELOD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KLV",
    "en": "KELVA ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KEZ",
    "en": "KELZAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KEM",
    "en": "KEM",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KEMR",
    "en": "KEMRI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KNPS",
    "en": "KENDPOSI",
    "se": "JHARKHAND"
  },
  {
    "sc": "KENP",
    "en": "KENDRAPARA",
    "se": "ODISHA"
  },
  {
    "sc": "KNPR",
    "en": "KENDRAPARA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "KDRI",
    "en": "KENDRI P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KED",
    "en": "KENDUAPADA",
    "se": "ODISHA"
  },
  {
    "sc": "KDJR",
    "en": "KENDUJHARGARH",
    "se": "ODISHA"
  },
  {
    "sc": "KDKN",
    "en": "KENDUKANA",
    "se": "ASSAM"
  },
  {
    "sc": "KGI",
    "en": "KENGERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KLZ",
    "en": "KEOLARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KKMI",
    "en": "KERAKALAMATTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KPJG",
    "en": "KEREJANGA",
    "se": "ODISHA"
  },
  {
    "sc": "KRBR",
    "en": "KERKHABARI",
    "se": "ASSAM"
  },
  {
    "sc": "KDM",
    "en": "KESAMUDRAM",
    "se": "TELANGANA"
  },
  {
    "sc": "KXZ",
    "en": "KESARIYA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KSVM",
    "en": "KESAVARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KVJ",
    "en": "KESHAVGANJ",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KSD",
    "en": "KESHOD",
    "se": "GUJARAT"
  },
  {
    "sc": "KOLI",
    "en": "KESHOLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KPTN",
    "en": "KESHORAI PATAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KSHR",
    "en": "KESHWARI BH",
    "se": "JHARKHAND"
  },
  {
    "sc": "KEC",
    "en": "KESIMPA",
    "se": "GUJARAT"
  },
  {
    "sc": "KSNG",
    "en": "KESINGA",
    "se": "ODISHA"
  },
  {
    "sc": "KES",
    "en": "KESRI",
    "se": "HARYANA"
  },
  {
    "sc": "KESR",
    "en": "KESRI SINGHPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KHLL",
    "en": "KETOHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KDY",
    "en": "KETTANDAPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KXT",
    "en": "KETTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KTGA",
    "en": "KEUTGUDA",
    "se": "ODISHA"
  },
  {
    "sc": "KR",
    "en": "KEVDI",
    "se": "GUJARAT"
  },
  {
    "sc": "KVO",
    "en": "KEVDI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KBKN",
    "en": "KHABRA KALAN",
    "se": "HARYANA"
  },
  {
    "sc": "KHRA",
    "en": "KHACHERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KUH",
    "en": "KHACHROD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KZA",
    "en": "KHADA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KDPA",
    "en": "KHADAPA",
    "se": "ODISHA"
  },
  {
    "sc": "KDT",
    "en": "KHADARPET",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KDV",
    "en": "KHADAVLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KK",
    "en": "KHADKI",
    "ec": "PUNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KDSB",
    "en": "KHADUR SAHIB",
    "se": "PUNJAB"
  },
  {
    "sc": "KB",
    "en": "KHAERTABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KGA",
    "en": "KHAGA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KGG",
    "en": "KHAGARIA JN",
    "se": "BIHAR"
  },
  {
    "sc": "KGLE",
    "en": "KHAGRAGHAT ROAD",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KIQ",
    "en": "KHAI PHEMEKI",
    "se": "PUNJAB"
  },
  {
    "sc": "KHA",
    "en": "KHAIGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KRRI",
    "en": "KHAIR RANJI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KYH",
    "en": "KHAIRAH",
    "se": "BIHAR"
  },
  {
    "sc": "KHRY",
    "en": "KHAIRAHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KID",
    "en": "KHAIRAR JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KQD",
    "en": "KHAIRATABAD",
    "ec": "SECUNDERABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "KYBR",
    "en": "KHAIRATIYA BH R",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KRH",
    "en": "KHAIRTHAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KJI",
    "en": "KHAJAULI",
    "se": "BIHAR"
  },
  {
    "sc": "KJDI",
    "en": "KHAJJIDONI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KHJ",
    "en": "KHAJRAHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KURJ",
    "en": "KHAJURAHO",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KJA",
    "en": "KHAJURHAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KAW",
    "en": "KHAJURI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KJW",
    "en": "KHAJWANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KKK",
    "en": "KHAKHARIA",
    "se": "GUJARAT"
  },
  {
    "sc": "KAK",
    "en": "KHAKHI JALIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "KKR",
    "en": "KHAKHRALA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KHXB",
    "en": "KHAKHRECHI BG",
    "se": "GUJARAT"
  },
  {
    "sc": "KLGR",
    "en": "KHALAIGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KLRE",
    "en": "KHALARI",
    "se": "JHARKHAND"
  },
  {
    "sc": "KLD",
    "en": "KHALILABAD",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KIP",
    "en": "KHALILPUR",
    "se": "HARYANA"
  },
  {
    "sc": "KHPL",
    "en": "KHALIPALI",
    "se": "ODISHA"
  },
  {
    "sc": "KSF",
    "en": "KHALISPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KIT",
    "en": "KHALLIKOT",
    "se": "ODISHA"
  },
  {
    "sc": "KTJ",
    "en": "KHALTIPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KMNN",
    "en": "KHAMANON",
    "se": "PUNJAB"
  },
  {
    "sc": "KMAE",
    "en": "KHAMARGACHHI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KMBL",
    "en": "KHAMBHALIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "CBY",
    "en": "KHAMBHAT",
    "se": "GUJARAT"
  },
  {
    "sc": "KVH",
    "en": "KHAMBHEL",
    "se": "GUJARAT"
  },
  {
    "sc": "KMN",
    "en": "KHAMGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KBK",
    "en": "KHAMIL GHAT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KMKD",
    "en": "KHAMKHED",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KMT",
    "en": "KHAMMAM",
    "se": "TELANGANA"
  },
  {
    "sc": "KBV",
    "en": "KHAN BHANKRI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KAN",
    "en": "KHANA JN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KJGY",
    "en": "KHANALAMPURA GY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KWT",
    "en": "KHANALAMPURA WT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KNP",
    "en": "KHANAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KHNP",
    "en": "KHANAPUR JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "KAD",
    "en": "KHANDALA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KBH",
    "en": "KHANDBAARA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KNDL",
    "en": "KHANDEL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KHDI",
    "en": "KHANDERI",
    "se": "GUJARAT"
  },
  {
    "sc": "KHDA",
    "en": "KHANDIA",
    "se": "GUJARAT"
  },
  {
    "sc": "KYO",
    "en": "KHANDIKAR",
    "se": "ASSAM"
  },
  {
    "sc": "KNDP",
    "en": "KHANDIP",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KZI",
    "en": "KHANDRAWALI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KNW",
    "en": "KHANDWA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KHJA",
    "en": "KHANJA HALT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KNN",
    "en": "KHANNA",
    "se": "PUNJAB"
  },
  {
    "sc": "KHBJ",
    "en": "KHANNA BANJARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KNAR",
    "en": "KHANPUR AHIR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KHF",
    "en": "KHANTAPARA",
    "se": "ODISHA"
  },
  {
    "sc": "KNF",
    "en": "KHANUDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "KHN",
    "en": "KHANYAN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KPKD",
    "en": "KHAPRI KHEDA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRI",
    "en": "KHAPTI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KHAR",
    "en": "KHAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRXA",
    "en": "KHARA P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KOD",
    "en": "KHARAGHODA",
    "se": "GUJARAT"
  },
  {
    "sc": "KGPW",
    "en": "KHARAGPUR WKSHP",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KRHT",
    "en": "KHARAHAT",
    "se": "ASSAM"
  },
  {
    "sc": "KHRK",
    "en": "KHARAK",
    "se": "HARYANA"
  },
  {
    "sc": "KARR",
    "en": "KHARAR",
    "se": "PUNJAB"
  },
  {
    "sc": "KRZ",
    "en": "KHARAWAR",
    "se": "HARYANA"
  },
  {
    "sc": "KHBV",
    "en": "KHARBAV",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KDH",
    "en": "KHARDAHA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KE",
    "en": "KHARDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRPN",
    "en": "KHAREPATAN ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KHRS",
    "en": "KHARESHWAR ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KHGP",
    "en": "KHARGAPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KARI",
    "en": "KHARI",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "KIA",
    "en": "KHARI AMRAPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "KJLU",
    "en": "KHARI JHALU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KXG",
    "en": "KHARIA KHANGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KRAR",
    "en": "KHARIAR ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "KHQ",
    "en": "KHARIK",
    "se": "BIHAR"
  },
  {
    "sc": "KQY",
    "en": "KHARIKATIA",
    "se": "ASSAM"
  },
  {
    "sc": "KARO",
    "en": "KHARIO P.H.",
    "se": "JHARKHAND"
  },
  {
    "sc": "KHRI",
    "en": "KHARKHARI",
    "se": "JHARKHAND"
  },
  {
    "sc": "KXK",
    "en": "KHARKHAUDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KPB",
    "en": "KHARPOKHRA",
    "se": "BIHAR"
  },
  {
    "sc": "KRSA",
    "en": "KHARSALIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "KHS",
    "en": "KHARSIA",
    "ec": "RAIGARH",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KRW",
    "en": "KHARWA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KRCD",
    "en": "KHARWA CHANDA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KSA",
    "en": "KHASA",
    "se": "PUNJAB"
  },
  {
    "sc": "KHAT",
    "en": "KHAT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KTLN",
    "en": "KHAT LABANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KAT",
    "en": "KHATAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KHTG",
    "en": "KHATGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KHMA",
    "en": "KHATIMA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "KWP",
    "en": "KHATIPURA",
    "ec": "JAIPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KHHJ",
    "en": "KHATKAR KALAN J",
    "se": "PUNJAB"
  },
  {
    "sc": "KHTU",
    "en": "KHATU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KHED",
    "en": "KHED",
    "ec": "RATNAGIRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KDBM",
    "en": "KHED BRAHMA",
    "se": "GUJARAT"
  },
  {
    "sc": "KHTX",
    "en": "KHED TEMPLE HLT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KQW",
    "en": "KHEDULI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KEX",
    "en": "KHEKRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KEMK",
    "en": "KHEM KARAN",
    "se": "PUNJAB"
  },
  {
    "sc": "KLH",
    "en": "KHEMLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KHKN",
    "en": "KHERA KALAN",
    "se": "DELHI"
  },
  {
    "sc": "KRU",
    "en": "KHERALU",
    "se": "GUJARAT"
  },
  {
    "sc": "KSW",
    "en": "KHERI SALWA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KL",
    "en": "KHERLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KHW",
    "en": "KHERODA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KOY",
    "en": "KHEROL",
    "se": "GUJARAT"
  },
  {
    "sc": "KW",
    "en": "KHERVADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KWKC",
    "en": "KHERWA KOCHA",
    "se": "JHARKHAND"
  },
  {
    "sc": "KS",
    "en": "KHETA SARAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KSHT",
    "en": "KHETIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KHSN",
    "en": "KHHERA SANDHAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KJV",
    "en": "KHIJADIYA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "KLYN",
    "en": "KHILERIYAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KZQ",
    "en": "KHIMEL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KNNA",
    "en": "KHINANIYAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KHAI",
    "en": "KHIRAI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KIE",
    "en": "KHIRIA KHURD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KKN",
    "en": "KHIRKIYA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KUX",
    "en": "KHIRSADOH JN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KHD",
    "en": "KHODIYAR",
    "se": "GUJARAT"
  },
  {
    "sc": "KHDB",
    "en": "KHODIYAR",
    "se": "GUJARAT"
  },
  {
    "sc": "KOI",
    "en": "KHODRI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KSIH",
    "en": "KHODSEONI P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KHOH",
    "en": "KHOH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KBY",
    "en": "KHOIRABARI",
    "se": "ASSAM"
  },
  {
    "sc": "KJP",
    "en": "KHOJEEPURA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KWJ",
    "en": "KHOJEWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "KGBP",
    "en": "KHONGSANG",
    "se": "MANIPUR"
  },
  {
    "sc": "KGS",
    "en": "KHONGSARA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KCR",
    "en": "KHONKER",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KHPI",
    "en": "KHOPOLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KHC",
    "en": "KHORANA",
    "se": "GUJARAT"
  },
  {
    "sc": "KRND",
    "en": "KHORASON ROAD",
    "ec": "AZAMGARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KORI",
    "en": "KHORI",
    "se": "HARYANA"
  },
  {
    "sc": "KHKT",
    "en": "KHOTKHOTI",
    "se": "ASSAM"
  },
  {
    "sc": "KBGN",
    "en": "KHUBAGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KDJ",
    "en": "KHUDAGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KZX",
    "en": "KHUDDA KORALA",
    "se": "PUNJAB"
  },
  {
    "sc": "KRBP",
    "en": "KHUDIRAM B PUSA",
    "se": "BIHAR"
  },
  {
    "sc": "KHDP",
    "en": "KHUDLAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KUKA",
    "en": "KHUI KHERA",
    "se": "PUNJAB"
  },
  {
    "sc": "KLNB",
    "en": "KHULNA"
  },
  {
    "sc": "KJL",
    "en": "KHUMGAON BURTI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KUTI",
    "en": "KHUMTAI",
    "se": "ASSAM"
  },
  {
    "sc": "KDF",
    "en": "KHUNDAUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KKNA",
    "en": "KHUNKHUNA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KHUT",
    "en": "KHUNTLA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KHND",
    "en": "KHUNVAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KRT",
    "en": "KHURAHAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KYE",
    "en": "KHURAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KUR",
    "en": "KHURDA ROAD JN",
    "ec": "KHURDA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "KURT",
    "en": "KHURDA TOWN",
    "se": "ODISHA"
  },
  {
    "sc": "KUPR",
    "en": "KHURDPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "KHU",
    "en": "KHURHAND",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KWE",
    "en": "KHURIAL",
    "se": "BIHAR"
  },
  {
    "sc": "KJY",
    "en": "KHURJA CITY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KRJ",
    "en": "KHURJA JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KRMP",
    "en": "KHURRAMPUR",
    "se": "BIHAR"
  },
  {
    "sc": "KSNR",
    "en": "KHUSHAL NAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KOO",
    "en": "KHUSROPUR",
    "se": "BIHAR"
  },
  {
    "sc": "KSBG",
    "en": "KHUSTA BUZURG",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KTHA",
    "en": "KHUTAHA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KHTN",
    "en": "KHUTAUNA",
    "se": "BIHAR"
  },
  {
    "sc": "KTT",
    "en": "KHUTBAV",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KTZ",
    "en": "KHUTWANSA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KHH",
    "en": "KICHHA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "KYG",
    "en": "KIDIYANAGA",
    "se": "GUJARAT"
  },
  {
    "sc": "KKRD",
    "en": "KIKAKUI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KKY",
    "en": "KILA KADAIYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "QRP",
    "en": "KILA RAIPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "KZH",
    "en": "KILA ZAFARGARH",
    "se": "HARYANA"
  },
  {
    "sc": "KLWL",
    "en": "KILANWALI PUNJB",
    "se": "PUNJAB"
  },
  {
    "sc": "KLQ",
    "en": "KILIKOLLUR",
    "se": "KERALA"
  },
  {
    "sc": "KII",
    "en": "KILLE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KIM",
    "en": "KIM",
    "se": "GUJARAT"
  },
  {
    "sc": "KIU",
    "en": "KINANA",
    "se": "HARYANA"
  },
  {
    "sc": "CNV",
    "en": "KINATTUKKADAVU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KQV",
    "en": "KINKHED",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KNVT",
    "en": "KINWAT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KCT",
    "en": "KIRAKAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KRDL",
    "en": "KIRANDUL",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KLB",
    "en": "KIRAOLI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KRTH",
    "en": "KIRATGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KAPU",
    "en": "KIRATPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KART",
    "en": "KIRATPUR SAHIB",
    "se": "PUNJAB"
  },
  {
    "sc": "KRBU",
    "en": "KIRIBURU",
    "se": "JHARKHAND"
  },
  {
    "sc": "KER",
    "en": "KIRIHRAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KOV",
    "en": "KIRLOSKARVADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KMMD",
    "en": "KIRMITI MENDHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KNHR",
    "en": "KIRNAHAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KRC",
    "en": "KIRODA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KDTR",
    "en": "KIRODIMALNAGAR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KRTN",
    "en": "KIRTINAGAR",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "KTNR",
    "en": "KIRTYANAND NGR",
    "se": "BIHAR"
  },
  {
    "sc": "KMNP",
    "en": "KISHAN MANPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KNE",
    "en": "KISHANGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "KSG",
    "en": "KISHANGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KSP",
    "en": "KISHANPUR",
    "se": "BIHAR"
  },
  {
    "sc": "KGBS",
    "en": "KISHENGARH BLWS",
    "se": "HARYANA"
  },
  {
    "sc": "KONY",
    "en": "KISONI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KSTE",
    "en": "KISTAMSETIPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KITA",
    "en": "KITA",
    "se": "JHARKHAND"
  },
  {
    "sc": "KXM",
    "en": "KITHAM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KIUL",
    "en": "KIUL JN",
    "se": "BIHAR"
  },
  {
    "sc": "KWI",
    "en": "KIVARLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KIB",
    "en": "KIZHA AMBUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KYZ",
    "en": "KIZHA PULIYUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KVL",
    "en": "KIZHVELUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KAG",
    "en": "KODAGANUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KQN",
    "en": "KODAIKANAL ROAD",
    "ec": "KODAIKANAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MKK",
    "en": "KODAMBAKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KJJ",
    "en": "KODAVALURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KQR",
    "en": "KODERMA JN",
    "se": "JHARKHAND"
  },
  {
    "sc": "KODI",
    "en": "KODI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KDGH",
    "en": "KODIGEHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KOM",
    "en": "KODIKKALPALAIYM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KDBA",
    "en": "KODIMBALA",
    "se": "KARNATAKA"
  },
  {
    "sc": "KODR",
    "en": "KODINAR",
    "se": "GUJARAT"
  },
  {
    "sc": "KDMR",
    "en": "KODIYAR MANDIR",
    "se": "GUJARAT"
  },
  {
    "sc": "KODN",
    "en": "KODUMMUNDA",
    "se": "KERALA"
  },
  {
    "sc": "KMD",
    "en": "KODUMUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KOU",
    "en": "KODURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KWR",
    "en": "KOELWAR",
    "se": "BIHAR"
  },
  {
    "sc": "KFU",
    "en": "KOHAND",
    "se": "HARYANA"
  },
  {
    "sc": "KRSW",
    "en": "KOHAR SINGHWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "KDK",
    "en": "KOHDAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KOHR",
    "en": "KOHIR DECCAN",
    "se": "TELANGANA"
  },
  {
    "sc": "KOHL",
    "en": "KOHLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KLKA",
    "en": "KOILAKUNTLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KEPR",
    "en": "KOIRIPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KOKA",
    "en": "KOKA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KXD",
    "en": "KOKALDA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KKPR",
    "en": "KOKPARA",
    "se": "JHARKHAND"
  },
  {
    "sc": "KOJ",
    "en": "KOKRAJHAR",
    "se": "ASSAM"
  },
  {
    "sc": "KOL",
    "en": "KOLAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "QGT",
    "en": "KOLAGHAT",
    "ec": "MECHEDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KLX",
    "en": "KOLAKALUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CNY",
    "en": "KOLANALLI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KAQ",
    "en": "KOLANUKONDA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KQZ",
    "en": "KOLAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KLRS",
    "en": "KOLARAS",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KLS",
    "en": "KOLATUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KLYT",
    "en": "KOLAYAT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KFF",
    "en": "KOLDA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "CP",
    "en": "KOLKATA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "QLN",
    "en": "KOLLAM JN",
    "se": "KERALA"
  },
  {
    "sc": "KLGD",
    "en": "KOLLENGODE",
    "se": "KERALA"
  },
  {
    "sc": "CLN",
    "en": "KOLLIDAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KKTA",
    "en": "KOLLIKHUTAHA",
    "se": "BIHAR"
  },
  {
    "sc": "KOLR",
    "en": "KOLNUR",
    "se": "TELANGANA"
  },
  {
    "sc": "KVGM",
    "en": "KOLVAGRAM",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KMK",
    "en": "KOMAKHAN",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KMQA",
    "en": "KOMALI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KMPR",
    "en": "KOMARPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KMX",
    "en": "KOMATIPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KMLP",
    "en": "KOMMARAPUDI JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KNH",
    "en": "KONCH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KQA",
    "en": "KONDAGUNTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KI",
    "en": "KONDAPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KDP",
    "en": "KONDAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KNKP",
    "en": "KONDIKOPPA",
    "se": "KARNATAKA"
  },
  {
    "sc": "KDRL",
    "en": "KONDRAPOLE HALT",
    "se": "TELANGANA"
  },
  {
    "sc": "KOG",
    "en": "KONNAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KONN",
    "en": "KONNUR",
    "se": "TELANGANA"
  },
  {
    "sc": "KPS",
    "en": "KOPA SAMHOTA",
    "se": "BIHAR"
  },
  {
    "sc": "KPJ",
    "en": "KOPAGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KPLE",
    "en": "KOPAI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KOPR",
    "en": "KOPAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KPG",
    "en": "KOPARGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KFA",
    "en": "KOPARIA",
    "se": "BIHAR"
  },
  {
    "sc": "KPLR",
    "en": "KOPARLAHAR",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "KBL",
    "en": "KOPPAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "KORA",
    "en": "KORA",
    "se": "GUJARAT"
  },
  {
    "sc": "KDE",
    "en": "KORADACHERI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KRDH",
    "en": "KORADIH P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRHA",
    "en": "KORAHIA",
    "se": "BIHAR"
  },
  {
    "sc": "KRIH",
    "en": "KORAI HALT",
    "se": "ODISHA"
  },
  {
    "sc": "KRPU",
    "en": "KORAPUT",
    "se": "ODISHA"
  },
  {
    "sc": "KURO",
    "en": "KORARI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KRLA",
    "en": "KORATLA",
    "se": "TELANGANA"
  },
  {
    "sc": "KRAN",
    "en": "KORATTI ANGADI",
    "se": "KERALA"
  },
  {
    "sc": "KOTR",
    "en": "KORATTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KRVL",
    "en": "KORAVANGALA",
    "se": "KARNATAKA"
  },
  {
    "sc": "KRBA",
    "en": "KORBA",
    "ec": "CHAMPA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KRG",
    "en": "KOREGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KOK",
    "en": "KORUKKUPET JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KUK",
    "en": "KORUKONDA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KSE",
    "en": "KOSAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KSAE",
    "en": "KOSAI",
    "se": "TELANGANA"
  },
  {
    "sc": "KSB",
    "en": "KOSAMBA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "KO",
    "en": "KOSGI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KSV",
    "en": "KOSI KALAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KVQ",
    "en": "KOSIARA",
    "se": "JHARKHAND"
  },
  {
    "sc": "KSI",
    "en": "KOSLI",
    "se": "HARYANA"
  },
  {
    "sc": "KOZ",
    "en": "KOSMA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KTF",
    "en": "KOT FATTEH",
    "se": "PUNJAB"
  },
  {
    "sc": "KKP",
    "en": "KOT KAPURA",
    "ec": "KOT KAPURA",
    "se": "PUNJAB"
  },
  {
    "sc": "KBM",
    "en": "KOTABOMMALI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KTKA",
    "en": "KOTAKADRA",
    "se": "TELANGANA"
  },
  {
    "sc": "KEN",
    "en": "KOTALA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KLP",
    "en": "KOTALPUKUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "KTOA",
    "en": "KOTANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KPRR",
    "en": "KOTAPAR ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "KRL",
    "en": "KOTARLIA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KDBS",
    "en": "KOTDA BAVISHI",
    "se": "GUJARAT"
  },
  {
    "sc": "KTW",
    "en": "KOTDWARA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "KOH",
    "en": "KOTESHWAR",
    "se": "GUJARAT"
  },
  {
    "sc": "KTGD",
    "en": "KOTH GANGAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KTPK",
    "en": "KOTHA PAKKI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KTCR",
    "en": "KOTHACHERUVU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KTR",
    "en": "KOTHAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "QTR",
    "en": "KOTHARA",
    "se": "GUJARAT"
  },
  {
    "sc": "KTHD",
    "en": "KOTHARI ROAD",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "RKY",
    "en": "KOTHARIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "KOTI",
    "en": "KOTI",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "KQK",
    "en": "KOTIKULAM",
    "se": "KERALA"
  },
  {
    "sc": "KOLA",
    "en": "KOTLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KTGN",
    "en": "KOTLA GUJRAN",
    "se": "PUNJAB"
  },
  {
    "sc": "KTKH",
    "en": "KOTLAKHERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KTKL",
    "en": "KOTLI KALAN",
    "se": "PUNJAB"
  },
  {
    "sc": "KTMA",
    "en": "KOTMA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KTSH",
    "en": "KOTMI SONAR P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KTRA",
    "en": "KOTRA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KSX",
    "en": "KOTSHILA",
    "ec": "BOKARO STEEL CITY",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KPLL",
    "en": "KOTTA PNDLPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KTYR",
    "en": "KOTTAIYUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KOHA",
    "en": "KOTTAKOTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KYOP",
    "en": "KOTTAPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "KKZ",
    "en": "KOTTARAKARA",
    "se": "KERALA"
  },
  {
    "sc": "KTV",
    "en": "KOTTAVALASA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KTYM",
    "en": "KOTTAYAM",
    "se": "KERALA"
  },
  {
    "sc": "KOTT",
    "en": "KOTTUR HALT",
    "se": "TELANGANA"
  },
  {
    "sc": "KTPM",
    "en": "KOTTURPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KTY",
    "en": "KOTTURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "CVP",
    "en": "KOVILPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KVR",
    "en": "KOVVUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KYV",
    "en": "KOYILVENNI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KSN",
    "en": "KRISHNA",
    "se": "TELANGANA"
  },
  {
    "sc": "KBSH",
    "en": "KRISHNA BALLABH",
    "se": "JHARKHAND"
  },
  {
    "sc": "KCC",
    "en": "KRISHNA CANAL",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KCV",
    "en": "KRISHNA CH PURA",
    "se": "ODISHA"
  },
  {
    "sc": "KEF",
    "en": "KRISHNAMMAKONA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KRP",
    "en": "KRISHNAPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KPU",
    "en": "KRISHNAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KJS",
    "en": "KRISHNARAJASGRA",
    "se": "KARNATAKA"
  },
  {
    "sc": "KRNR",
    "en": "KRISHNARAJNAGAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KRSL",
    "en": "KRISHNASHILLA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KNJ",
    "en": "KRISHNGR CTY JN",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KSTS",
    "en": "KRISNAMSETIPALI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KXA",
    "en": "KUANRIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KRMD",
    "en": "KUARMUNDA",
    "se": "ODISHA"
  },
  {
    "sc": "KBP",
    "en": "KUBERPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KUCE",
    "en": "KUCHAI",
    "se": "ODISHA"
  },
  {
    "sc": "KMNC",
    "en": "KUCHAMAN CITY",
    "se": "RAJASTHAN"
  },
  {
    "sc": "QXR",
    "en": "KUCHESAR ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KCA",
    "en": "KUCHMAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KDR",
    "en": "KUDA SALT SDG",
    "se": "GUJARAT"
  },
  {
    "sc": "KUD",
    "en": "KUDACHI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KUDL",
    "en": "KUDAL",
    "ec": "RATNAGIRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KSAR",
    "en": "KUDALA SANGAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "KON",
    "en": "KUDALNAGAR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KDN",
    "en": "KUDATINI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KDGI",
    "en": "KUDGI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KXO",
    "en": "KUDIKADU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KUDN",
    "en": "KUDNI",
    "se": "HARYANA"
  },
  {
    "sc": "KTQ",
    "en": "KUDRA",
    "se": "BIHAR"
  },
  {
    "sc": "KDSD",
    "en": "KUDSAD",
    "se": "GUJARAT"
  },
  {
    "sc": "KUHI",
    "en": "KUHI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KUU",
    "en": "KUHURI",
    "ec": "KHURDA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "KANR",
    "en": "KUKANUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KKRV",
    "en": "KUKARVADA",
    "se": "GUJARAT"
  },
  {
    "sc": "KEMA",
    "en": "KUKMA",
    "se": "GUJARAT"
  },
  {
    "sc": "KFP",
    "en": "KUKRA KHAPA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KUI",
    "en": "KULALI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KIJ",
    "en": "KULDIHA",
    "se": "ODISHA"
  },
  {
    "sc": "QLM",
    "en": "KULEM",
    "se": "GOA"
  },
  {
    "sc": "KGY",
    "en": "KULGACHIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KUA",
    "en": "KULHARIA",
    "se": "BIHAR"
  },
  {
    "sc": "KU",
    "en": "KULIKARAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KUY",
    "en": "KULIPALAIYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KLT",
    "en": "KULITALAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KZT",
    "en": "KULITTHURAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KZTW",
    "en": "KULITTURAI WEST",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KLNC",
    "en": "KULLANCHAVADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KLAR",
    "en": "KULPAHAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ULT",
    "en": "KULTI",
    "ec": "ASANSOL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KZC",
    "en": "KULUKKALUR",
    "se": "KERALA"
  },
  {
    "sc": "KLA",
    "en": "KULWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KMGE",
    "en": "KUMAHU",
    "se": "BIHAR"
  },
  {
    "sc": "KMSD",
    "en": "KUMAR SADRA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KRMG",
    "en": "KUMARAMANGALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KFQ",
    "en": "KUMARANALLUR",
    "se": "KERALA"
  },
  {
    "sc": "KPM",
    "en": "KUMARAPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KUMB",
    "en": "KUMARBAGH",
    "se": "BIHAR"
  },
  {
    "sc": "KMME",
    "en": "KUMARDUBI",
    "ec": "ASANSOL",
    "se": "JHARKHAND"
  },
  {
    "sc": "KMRJ",
    "en": "KUMARGANJ",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KUGT",
    "en": "KUMARGHAT",
    "se": "TRIPURA"
  },
  {
    "sc": "KMTI",
    "en": "KUMARHATTI",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "KMU",
    "en": "KUMBAKONAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KUMM",
    "en": "KUMBALAM",
    "se": "KERALA"
  },
  {
    "sc": "KHRJ",
    "en": "KUMBHRAJ",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KMQ",
    "en": "KUMBLA",
    "se": "KERALA"
  },
  {
    "sc": "KDPR",
    "en": "KUMEDPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KMND",
    "en": "KUMENDI",
    "se": "JHARKHAND"
  },
  {
    "sc": "KMEZ",
    "en": "KUMHAR MARENGA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KMI",
    "en": "KUMHARI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KBQ",
    "en": "KUMRABAD ROHINI",
    "se": "JHARKHAND"
  },
  {
    "sc": "KMRL",
    "en": "KUMRUL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KMSI",
    "en": "KUMSI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KT",
    "en": "KUMTA",
    "ec": "KARWAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "KTKR",
    "en": "KUMTHA KHURD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KUND",
    "en": "KUND",
    "se": "HARYANA"
  },
  {
    "sc": "KHNM",
    "en": "KUNDA HARNAMGNJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KDLG",
    "en": "KUNDALGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KUDA",
    "en": "KUNDAPURA",
    "ec": "UDUPI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KUV",
    "en": "KUNDARA",
    "se": "KERALA"
  },
  {
    "sc": "KFV",
    "en": "KUNDARA EAST",
    "se": "KERALA"
  },
  {
    "sc": "KD",
    "en": "KUNDARKHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KNO",
    "en": "KUNDGOL",
    "se": "KARNATAKA"
  },
  {
    "sc": "KDHL",
    "en": "KUNDHELA",
    "se": "GUJARAT"
  },
  {
    "sc": "KDI",
    "en": "KUNDLI",
    "se": "GUJARAT"
  },
  {
    "sc": "KWC",
    "en": "KUNDWA CHAINPUR",
    "se": "BIHAR"
  },
  {
    "sc": "KVG",
    "en": "KUNEANGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KNRT",
    "en": "KUNERU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KIGL",
    "en": "KUNIGAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "KKV",
    "en": "KUNKAVAV JN",
    "se": "GUJARAT"
  },
  {
    "sc": "KVT",
    "en": "KUNKAVAV TOWN",
    "se": "GUJARAT"
  },
  {
    "sc": "KZU",
    "en": "KUNKI",
    "se": "JHARKHAND"
  },
  {
    "sc": "KNNT",
    "en": "KUNNATHUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KJU",
    "en": "KUNTIGHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KNRI",
    "en": "KUNURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KUP",
    "en": "KUP",
    "se": "PUNJAB"
  },
  {
    "sc": "KGL",
    "en": "KUPGAL",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KPN",
    "en": "KUPPAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KBA",
    "en": "KURABALAKOTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KORL",
    "en": "KURAL",
    "se": "GUJARAT"
  },
  {
    "sc": "KRLI",
    "en": "KURALI",
    "se": "PUNJAB"
  },
  {
    "sc": "KUM",
    "en": "KURAM",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRGA",
    "en": "KURANGA",
    "se": "GUJARAT"
  },
  {
    "sc": "KKS",
    "en": "KURASTI KALAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KRO",
    "en": "KURAWAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KWV",
    "en": "KURDUVADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KBE",
    "en": "KUREBHAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KUQ",
    "en": "KURETHA",
    "se": "BIHAR"
  },
  {
    "sc": "KQT",
    "en": "KURGUNTA",
    "se": "KARNATAKA"
  },
  {
    "sc": "KHI",
    "en": "KURHANI",
    "se": "BIHAR"
  },
  {
    "sc": "KIF",
    "en": "KURI",
    "se": "KERALA"
  },
  {
    "sc": "KCD",
    "en": "KURICHEDU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KFE",
    "en": "KURIKAD",
    "se": "KERALA"
  },
  {
    "sc": "KJPD",
    "en": "KURINIJIPADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KRKR",
    "en": "KURKURA",
    "se": "JHARKHAND"
  },
  {
    "sc": "CLA",
    "en": "KURLA JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KRLS",
    "en": "KURLAS",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KRNT",
    "en": "KURNOOL CITY",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "KRYA",
    "en": "KURRAIYA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KUE",
    "en": "KURSELA",
    "se": "BIHAR"
  },
  {
    "sc": "KGN",
    "en": "KURSEONG",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KRX",
    "en": "KURUD P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KKDE",
    "en": "KURUKSHETRA JN",
    "se": "HARYANA"
  },
  {
    "sc": "KZB",
    "en": "KURUMBUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KXI",
    "en": "KURUMURTHI",
    "se": "TELANGANA"
  },
  {
    "sc": "KRPP",
    "en": "KURUPPAN TARA",
    "se": "KERALA"
  },
  {
    "sc": "KIKA",
    "en": "KURWAI KETHORA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "KLSP",
    "en": "KUSHAL PURA",
    "se": "HARYANA"
  },
  {
    "sc": "KHTI",
    "en": "KUSHTAGI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KTA",
    "en": "KUSHTALA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KSU",
    "en": "KUSHTAUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "KSY",
    "en": "KUSIARGAON",
    "se": "BIHAR"
  },
  {
    "sc": "KCB",
    "en": "KUSLAMB",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "KHM",
    "en": "KUSMHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KUG",
    "en": "KUSUGALI",
    "se": "KARNATAKA"
  },
  {
    "sc": "KVX",
    "en": "KUSUMBHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KYS",
    "en": "KUSUMKASA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "KDS",
    "en": "KUSUNDA JN",
    "se": "JHARKHAND"
  },
  {
    "sc": "KWW",
    "en": "KUSWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "KOQ",
    "en": "KUTHUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KKTI",
    "en": "KUTTAKUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KTM",
    "en": "KUTTALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "KTU",
    "en": "KUTTIPPURAM",
    "se": "KERALA"
  },
  {
    "sc": "KTRK",
    "en": "KUTURUKHAMAR PH",
    "se": "ODISHA"
  },
  {
    "sc": "KUTL",
    "en": "KUWANTHAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KRKP",
    "en": "KYARKOP",
    "se": "KARNATAKA"
  },
  {
    "sc": "KTK",
    "en": "KYATANEAKERI RD",
    "se": "KARNATAKA"
  },
  {
    "sc": "KIAT",
    "en": "KYATSANDRA",
    "se": "KARNATAKA"
  },
  {
    "sc": "LKSH",
    "en": "L NARAYANAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "LBN",
    "en": "LABAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LAV",
    "en": "LABHA",
    "se": "BIHAR"
  },
  {
    "sc": "LBP",
    "en": "LABPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "LAC",
    "en": "LACHHIPURA"
  },
  {
    "sc": "LNH",
    "en": "LACHHMANGARH SK",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LMN",
    "en": "LACHHMANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LCME",
    "en": "LACHMANPUR ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "LIR",
    "en": "LACHMIPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LHN",
    "en": "LACHYAN",
    "se": "KARNATAKA"
  },
  {
    "sc": "LDX",
    "en": "LADDA",
    "se": "ODISHA"
  },
  {
    "sc": "LDVD",
    "en": "LADDIVADI HALT",
    "se": "TAMIL NADU"
  },
  {
    "sc": "LDW",
    "en": "LADHOWAL",
    "se": "PUNJAB"
  },
  {
    "sc": "LDK",
    "en": "LADHUKA",
    "se": "PUNJAB"
  },
  {
    "sc": "LDD",
    "en": "LADKHED",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LAU",
    "en": "LADNUN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LR",
    "en": "LADPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LGCE",
    "en": "LAGARGAWAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LHB",
    "en": "LAHABON",
    "se": "BIHAR"
  },
  {
    "sc": "LT",
    "en": "LAHAVIT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LSI",
    "en": "LAHERIA SARAI",
    "se": "BIHAR"
  },
  {
    "sc": "LH",
    "en": "LAHING",
    "se": "ASSAM"
  },
  {
    "sc": "LHLL",
    "en": "LAHLI",
    "se": "HARYANA"
  },
  {
    "sc": "LHL",
    "en": "LAHOAL",
    "se": "ASSAM"
  },
  {
    "sc": "LHK",
    "en": "LAIHRA KHANA",
    "se": "PUNJAB"
  },
  {
    "sc": "LMM",
    "en": "LAILAKH MAMLKHA",
    "se": "BIHAR"
  },
  {
    "sc": "LPNR",
    "en": "LAJPAT NAGAR",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "LKZ",
    "en": "LAKADIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "LKBL",
    "en": "LAKHABAWAL",
    "se": "GUJARAT"
  },
  {
    "sc": "LMC",
    "en": "LAKHAMANCHI",
    "se": "GUJARAT"
  },
  {
    "sc": "LKE",
    "en": "LAKHERI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LKW",
    "en": "LAKHEWALI",
    "se": "PUNJAB"
  },
  {
    "sc": "LMP",
    "en": "LAKHIMPUR",
    "ec": "LAKHIMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LKY",
    "en": "LAKHMAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "LKN",
    "en": "LAKHMINIA",
    "se": "BIHAR"
  },
  {
    "sc": "LKNA",
    "en": "LAKHNA",
    "se": "ODISHA"
  },
  {
    "sc": "LNQ",
    "en": "LAKHNAURIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LAK",
    "en": "LAKHO",
    "se": "BIHAR"
  },
  {
    "sc": "LAE",
    "en": "LAKHOLI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "LAA",
    "en": "LAKHPAT",
    "se": "GUJARAT"
  },
  {
    "sc": "LKNR",
    "en": "LAKHPAT NAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LPU",
    "en": "LAKHPURI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LTR",
    "en": "LAKHTAR",
    "se": "GUJARAT"
  },
  {
    "sc": "LKKD",
    "en": "LAKKADKOT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LVK",
    "en": "LAKKAVARAPUKOTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "LDY",
    "en": "LAKKITI",
    "se": "KERALA"
  },
  {
    "sc": "LKD",
    "en": "LAKODARA",
    "se": "GUJARAT"
  },
  {
    "sc": "LRJ",
    "en": "LAKSAR JN",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "LXD",
    "en": "LAKSHANNATH RD",
    "se": "ODISHA"
  },
  {
    "sc": "LMNR",
    "en": "LAKSHMIBAI NGR",
    "ec": "INDORE",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LIJ",
    "en": "LAKSHMIGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LKPR",
    "en": "LAKSHMIKANTPUR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "LKX",
    "en": "LAKSHMIPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "LXA",
    "en": "LAKSWA",
    "se": "ASSAM"
  },
  {
    "sc": "LLKN",
    "en": "LAL KALAN",
    "se": "PUNJAB"
  },
  {
    "sc": "LKU",
    "en": "LAL KUAN",
    "ec": "KATHGODAM",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "LGDH",
    "en": "LALAGUDA GATE",
    "se": "TELANGANA"
  },
  {
    "sc": "LP",
    "en": "LALAPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "LLD",
    "en": "LALAWADI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LBZ",
    "en": "LALBAGH",
    "se": "JHARKHAND"
  },
  {
    "sc": "LCAE",
    "en": "LALBAGH CRT RD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "LLBR",
    "en": "LALBAZAR",
    "se": "ASSAM"
  },
  {
    "sc": "LLJ",
    "en": "LALGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LBT",
    "en": "LALGARH BIHAR H",
    "se": "JHARKHAND"
  },
  {
    "sc": "LGH",
    "en": "LALGARH JN",
    "ec": "BIKANER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LGL",
    "en": "LALGOLA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "LGO",
    "en": "LALGOPALGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LLI",
    "en": "LALGUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "LLP",
    "en": "LALIT GRAM",
    "se": "BIHAR"
  },
  {
    "sc": "LLPR",
    "en": "LALIT LAKSHMIPR",
    "se": "BIHAR"
  },
  {
    "sc": "LLTG",
    "en": "LALITAGIRI",
    "se": "ODISHA"
  },
  {
    "sc": "LAR",
    "en": "LALITPUR JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LLR",
    "en": "LALPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LCN",
    "en": "LALPUR CHANDRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LPJ",
    "en": "LALPUR JAM",
    "se": "GUJARAT"
  },
  {
    "sc": "LRU",
    "en": "LALPUR UMRI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LLU",
    "en": "LALRU",
    "se": "PUNJAB"
  },
  {
    "sc": "LLST",
    "en": "LALSOT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LUA",
    "en": "LALURI KHERA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LNA",
    "en": "LAMANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LBA",
    "en": "LAMBHUA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LMA",
    "en": "LAMBIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LKG",
    "en": "LAMSAKHANG",
    "se": "ASSAM"
  },
  {
    "sc": "LTA",
    "en": "LAMTA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LDR",
    "en": "LANDAURA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "LGI",
    "en": "LANGAL",
    "se": "ASSAM"
  },
  {
    "sc": "LNP",
    "en": "LANGARPETH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LCT",
    "en": "LANGCHOLIET",
    "se": "ASSAM"
  },
  {
    "sc": "LNJ",
    "en": "LANGHNA",
    "se": "GUJARAT"
  },
  {
    "sc": "LGT",
    "en": "LANGTING",
    "se": "ASSAM"
  },
  {
    "sc": "LJR",
    "en": "LANJIGARH ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "LKA",
    "en": "LANKA",
    "se": "ASSAM"
  },
  {
    "sc": "LKDU",
    "en": "LANKALAKODERU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "LPN",
    "en": "LAOPANI",
    "se": "ASSAM"
  },
  {
    "sc": "LPG",
    "en": "LAPANGA",
    "ec": "JHARSUGUDA",
    "se": "ODISHA"
  },
  {
    "sc": "LRD",
    "en": "LAR ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LRB",
    "en": "LARABAD BH",
    "se": "JHARKHAND"
  },
  {
    "sc": "LS",
    "en": "LASALGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LSE",
    "en": "LASERI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LSN",
    "en": "LASINA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LSR",
    "en": "LASUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LTHR",
    "en": "LATEHAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "LAT",
    "en": "LATHI",
    "se": "GUJARAT"
  },
  {
    "sc": "LTD",
    "en": "LATHIDAD",
    "se": "GUJARAT"
  },
  {
    "sc": "LTK",
    "en": "LATHIKATA",
    "se": "ODISHA"
  },
  {
    "sc": "LPA",
    "en": "LATIPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "LTI",
    "en": "LATTERI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "LUR",
    "en": "LATUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LTRR",
    "en": "LATUR ROAD JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LKQ",
    "en": "LAUKAHA BAZAR",
    "se": "BIHAR"
  },
  {
    "sc": "LAUL",
    "en": "LAUL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LUN",
    "en": "LAVANPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "LSG",
    "en": "LAWA SARDARGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LKMR",
    "en": "LAXMIPUR ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "LYD",
    "en": "LAYABAD",
    "se": "JHARKHAND"
  },
  {
    "sc": "LDM",
    "en": "LEDARMER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LEDO",
    "en": "LEDO",
    "se": "ASSAM"
  },
  {
    "sc": "LGN",
    "en": "LEHGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LER",
    "en": "LEHRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LHA",
    "en": "LEHRA GAGA",
    "se": "PUNJAB"
  },
  {
    "sc": "LHM",
    "en": "LEHRA MUHABBAT",
    "se": "PUNJAB"
  },
  {
    "sc": "LOD",
    "en": "LEKODA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LLGM",
    "en": "LELIGUMA",
    "se": "ODISHA"
  },
  {
    "sc": "LDA",
    "en": "LIDHORA KHURD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LRI",
    "en": "LIHURI",
    "se": "ODISHA"
  },
  {
    "sc": "LBI",
    "en": "LILABARI",
    "se": "ASSAM"
  },
  {
    "sc": "LPR",
    "en": "LILAPUR ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "LMO",
    "en": "LILIYA MOTA",
    "se": "GUJARAT"
  },
  {
    "sc": "LLH",
    "en": "LILUAH",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "LMU",
    "en": "LIMARUA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LMB",
    "en": "LIMBARA",
    "se": "GUJARAT"
  },
  {
    "sc": "LM",
    "en": "LIMBDI",
    "se": "GUJARAT"
  },
  {
    "sc": "LBG",
    "en": "LIMBGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LBD",
    "en": "LIMBODRA",
    "se": "GUJARAT"
  },
  {
    "sc": "LMK",
    "en": "LIMKHEDA",
    "se": "GUJARAT"
  },
  {
    "sc": "LCH",
    "en": "LINCH",
    "se": "GUJARAT"
  },
  {
    "sc": "LING",
    "en": "LING",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LIG",
    "en": "LINGA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LIN",
    "en": "LINGAMGUNTLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "LPI",
    "en": "LINGAMPALLI",
    "ec": "SECUNDERABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "LPJL",
    "en": "LINGAMPET JAGIT",
    "se": "TELANGANA"
  },
  {
    "sc": "LNBI",
    "en": "LINGANABANDI",
    "se": "KARNATAKA"
  },
  {
    "sc": "LMD",
    "en": "LINGANENIDODDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "LGTR",
    "en": "LINGARAJ TMP RD",
    "ec": "BHUBANESWAR",
    "se": "ODISHA"
  },
  {
    "sc": "LGRE",
    "en": "LINGIRI",
    "se": "KARNATAKA"
  },
  {
    "sc": "LNT",
    "en": "LINGTI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LOM",
    "en": "LODHMA",
    "se": "JHARKHAND"
  },
  {
    "sc": "LDCY",
    "en": "LODI COLONY",
    "se": "DELHI"
  },
  {
    "sc": "LDP",
    "en": "LODIPUR BISHNPR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LRA",
    "en": "LODNA",
    "se": "GUJARAT"
  },
  {
    "sc": "LOHA",
    "en": "LOHA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LAP",
    "en": "LOHAPUR",
    "ec": "RAMPUR HAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "LAD",
    "en": "LOHARDAGA",
    "se": "JHARKHAND"
  },
  {
    "sc": "LPW",
    "en": "LOHARPURWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LHU",
    "en": "LOHARU",
    "se": "HARYANA"
  },
  {
    "sc": "LHW",
    "en": "LOHARWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LOG",
    "en": "LOHGARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LGB",
    "en": "LOHGARH ABUB"
  },
  {
    "sc": "LNK",
    "en": "LOHIAN KHAS JN",
    "se": "PUNJAB"
  },
  {
    "sc": "LNO",
    "en": "LOHNA ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "LHD",
    "en": "LOHOGAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LOT",
    "en": "LOHTA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LSX",
    "en": "LOISINGHA",
    "se": "ODISHA"
  },
  {
    "sc": "LDE",
    "en": "LOKDHIKHERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LKMN",
    "en": "LOKMANYA NAGAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LOK",
    "en": "LOKNATH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "LCR",
    "en": "LOKUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "LVR",
    "en": "LOKVIDYAPTH NGR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LOL",
    "en": "LOLIEM",
    "se": "GOA"
  },
  {
    "sc": "LO",
    "en": "LOLIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "LNN",
    "en": "LONAND",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LNL",
    "en": "LONAVALA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LD",
    "en": "LONDA JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "LPTA",
    "en": "LONGPATIA",
    "se": "ASSAM"
  },
  {
    "sc": "LONI",
    "en": "LONI",
    "ec": "PUNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LOA",
    "en": "LORHA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LW",
    "en": "LORWADA",
    "se": "GUJARAT"
  },
  {
    "sc": "LAN",
    "en": "LOTANA",
    "se": "GUJARAT"
  },
  {
    "sc": "LPH",
    "en": "LOTAPAHAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "LTV",
    "en": "LOTARVA",
    "se": "GUJARAT"
  },
  {
    "sc": "LHBK",
    "en": "LOTHAL BHURKHL",
    "se": "GUJARAT"
  },
  {
    "sc": "LOGH",
    "en": "LOTTEGOLAHALI H",
    "se": "KARNATAKA"
  },
  {
    "sc": "LOV",
    "en": "LOVEDALE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "LFG",
    "en": "LOWER HAFLONG"
  },
  {
    "sc": "LWJ",
    "en": "LOWJEE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "LKR",
    "en": "LUCKEESARAI JN",
    "se": "BIHAR"
  },
  {
    "sc": "AMV",
    "en": "LUCKNOW ALAMBGH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LC",
    "en": "LUCKNOW CITY",
    "ec": "LUCKNOW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LNWT",
    "en": "LUCKNOW WEST (A",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LWS",
    "en": "LUKWASA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LMG",
    "en": "LUMDING JN",
    "se": "ASSAM"
  },
  {
    "sc": "LNV",
    "en": "LUNAVADA",
    "se": "GUJARAT"
  },
  {
    "sc": "LUNI",
    "en": "LUNI JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LNR",
    "en": "LUNI RICHHA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "LDU",
    "en": "LUNIDHAR",
    "se": "GUJARAT"
  },
  {
    "sc": "LKS",
    "en": "LUNKARANSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "LXR",
    "en": "LUNSERIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "LUSA",
    "en": "LUSA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "LSD",
    "en": "LUSADIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "LAL",
    "en": "LUSHALA",
    "se": "GUJARAT"
  },
  {
    "sc": "LKK",
    "en": "LYALLPUR KC HLT",
    "se": "PUNJAB"
  },
  {
    "sc": "MABM",
    "en": "M AHORWA B DHAM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MBDP",
    "en": "MA BELHADEVI DP",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MCDA",
    "en": "MA CHANDIKA D D",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MKDM",
    "en": "MA KALIKAN DHAM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MBDD",
    "en": "MAA BARAHI D DH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MABN",
    "en": "MABAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MCV",
    "en": "MACHARYA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MCVM",
    "en": "MACHAVARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MSL",
    "en": "MACHCHALANDAPUR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MCLA",
    "en": "MACHERLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MKRD",
    "en": "MACHHAKUNDA",
    "se": "ODISHA"
  },
  {
    "sc": "MCY",
    "en": "MACHHRIAWAN",
    "se": "BIHAR"
  },
  {
    "sc": "MTM",
    "en": "MACHILIPATNAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MAC",
    "en": "MACHIYALA",
    "se": "GUJARAT"
  },
  {
    "sc": "MHWL",
    "en": "MACHROWAR",
    "se": "PUNJAB"
  },
  {
    "sc": "MML",
    "en": "MADAN MAHAL",
    "ec": "JABALPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MPL",
    "en": "MADANAPALLE RD",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MNC",
    "en": "MADANKATA",
    "se": "JHARKHAND"
  },
  {
    "sc": "MPJ",
    "en": "MADANPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MD",
    "en": "MADAR"
  },
  {
    "sc": "MDJN",
    "en": "MADAR JN",
    "ec": "AJMER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MFX",
    "en": "MADARAHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MDT",
    "en": "MADARIHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MDRR",
    "en": "MADAVNAGAR ROAD",
    "ec": "KATNI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MKR",
    "en": "MADDIKERA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MAD",
    "en": "MADDUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "MADU",
    "en": "MADDURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MA",
    "en": "MADHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MDBP",
    "en": "MADHABPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MDHA",
    "en": "MADHADA",
    "se": "GUJARAT"
  },
  {
    "sc": "MADP",
    "en": "MADHAPUR ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "MDVR",
    "en": "MADHAVNAGAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MID",
    "en": "MADHI",
    "se": "GUJARAT"
  },
  {
    "sc": "MDR",
    "en": "MADHIRA",
    "se": "TELANGANA"
  },
  {
    "sc": "MAH",
    "en": "MADHOGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MDPB",
    "en": "MADHOPUR PUNJAB",
    "se": "PUNJAB"
  },
  {
    "sc": "MBS",
    "en": "MADHOSINGH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MDSE",
    "en": "MADHU SUDANPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MBI",
    "en": "MADHUBANI",
    "se": "BIHAR"
  },
  {
    "sc": "MDKD",
    "en": "MADHUKUNDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MDP",
    "en": "MADHUPUR JN",
    "ec": "MADHUPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "MDUN",
    "en": "MADHURANAGAR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MMG",
    "en": "MADHYAMGRAM",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MPN",
    "en": "MADHYAMPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MCL",
    "en": "MADIMANGALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MLDE",
    "en": "MADLAUDA",
    "se": "HARYANA"
  },
  {
    "sc": "MPD",
    "en": "MADPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MDKI",
    "en": "MADUKARAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MES",
    "en": "MADURAI EAST",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MMK",
    "en": "MADURANTAKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MADR",
    "en": "MADURE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MWRN",
    "en": "MADWARANI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "MWF",
    "en": "MAGARDAHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MGRD",
    "en": "MAGARDOH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MGRR",
    "en": "MAGARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MGW",
    "en": "MAGARWARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MHH",
    "en": "MAGHAR",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MGND",
    "en": "MAGNAD",
    "se": "GUJARAT"
  },
  {
    "sc": "MUG",
    "en": "MAGRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MGT",
    "en": "MAGRA HAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "DC",
    "en": "MAGUDANCHAVADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MBLP",
    "en": "MAH BIJLI PASI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MCZ",
    "en": "MAHABUANG",
    "se": "JHARKHAND"
  },
  {
    "sc": "MHBT",
    "en": "MAHABUBNAGAR TO",
    "se": "TELANGANA"
  },
  {
    "sc": "MMH",
    "en": "MAHADANAPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MDVK",
    "en": "MAHADEOKHEDI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MHBG",
    "en": "MAHADEVA BUZRUG",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MHDP",
    "en": "MAHADEVPARA",
    "se": "GUJARAT"
  },
  {
    "sc": "MXW",
    "en": "MAHADEVSAL",
    "se": "JHARKHAND"
  },
  {
    "sc": "MAGN",
    "en": "MAHAGAON",
    "se": "KARNATAKA"
  },
  {
    "sc": "MHJ",
    "en": "MAHAJAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MFM",
    "en": "MAHALAM",
    "se": "PUNJAB"
  },
  {
    "sc": "MMV",
    "en": "MAHALI MARUP",
    "se": "JHARKHAND"
  },
  {
    "sc": "MMC",
    "en": "MAHAMANDIR",
    "ec": "JODHPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MHN",
    "en": "MAHANADI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MANG",
    "en": "MAHANAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MBC",
    "en": "MAHANANDA BGE",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MWR",
    "en": "MAHANSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MGZ",
    "en": "MAHARAJGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "MSMD",
    "en": "MAHASAMUND",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "MABD",
    "en": "MAHBUBABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "MBNR",
    "en": "MAHBUBNAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "MAHE",
    "en": "MAHE",
    "se": "KERALA"
  },
  {
    "sc": "MYJ",
    "en": "MAHEJI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MHRG",
    "en": "MAHENDRAGARH",
    "se": "HARYANA"
  },
  {
    "sc": "MSK",
    "en": "MAHES KHUNT",
    "se": "BIHAR"
  },
  {
    "sc": "MSH",
    "en": "MAHESANA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "MSSD",
    "en": "MAHESHARI SNDHN",
    "se": "PUNJAB"
  },
  {
    "sc": "MSGJ",
    "en": "MAHESHGANJ",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MVV",
    "en": "MAHESHI",
    "se": "BIHAR"
  },
  {
    "sc": "MMD",
    "en": "MAHESHMUNDA",
    "se": "JHARKHAND"
  },
  {
    "sc": "MHSA",
    "en": "MAHESHPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "MHSP",
    "en": "MAHESPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MHHR",
    "en": "MAHESRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MEP",
    "en": "MAHIDPUR ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MHMB",
    "en": "MAHIMBA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MPLE",
    "en": "MAHIPAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MPLR",
    "en": "MAHIPAL ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MSDL",
    "en": "MAHISADAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MGO",
    "en": "MAHISGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MWZ",
    "en": "MAHISHADAHARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MHPR",
    "en": "MAHIYARPUR",
    "se": "BIHAR"
  },
  {
    "sc": "MKZ",
    "en": "MAHKEPAR RD P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MMB",
    "en": "MAHMUDABAD AVDH",
    "ec": "SITAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MZN",
    "en": "MAHMUDPUR SRYN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MGWD",
    "en": "MAHNGARWL DOABA",
    "se": "PUNJAB"
  },
  {
    "sc": "MBA",
    "en": "MAHOBA JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MAHO",
    "en": "MAHOLI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MHO",
    "en": "MAHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MHRL",
    "en": "MAHRAIL",
    "se": "BIHAR"
  },
  {
    "sc": "MWP",
    "en": "MAHRANI PACHHIM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MFH",
    "en": "MAHRAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MWUE",
    "en": "MAHRAWAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MFQ",
    "en": "MAHROI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MMLN",
    "en": "MAHUAMILAN",
    "se": "JHARKHAND"
  },
  {
    "sc": "MXY",
    "en": "MAHUARIYA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MUUA",
    "en": "MAHUAWA KHURD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MHQ",
    "en": "MAHUDA",
    "ec": "BOKARO STEEL CITY",
    "se": "JHARKHAND"
  },
  {
    "sc": "MHUA",
    "en": "MAHUDHA",
    "se": "GUJARAT"
  },
  {
    "sc": "MUGA",
    "en": "MAHUGARHA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MZB",
    "en": "MAHULI P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MXR",
    "en": "MAHUR",
    "se": "ASSAM"
  },
  {
    "sc": "MHV",
    "en": "MAHUVA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "MHUL",
    "en": "MAHUWALA HALT",
    "se": "HARYANA"
  },
  {
    "sc": "MWW",
    "en": "MAHWA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MHL",
    "en": "MAHWAL",
    "se": "BIHAR"
  },
  {
    "sc": "MBG",
    "en": "MAIBONG",
    "se": "ASSAM"
  },
  {
    "sc": "MYR",
    "en": "MAIHAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MIR",
    "en": "MAIJAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MINJ",
    "en": "MAIKALGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MTL",
    "en": "MAILAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MLN",
    "en": "MAILANI",
    "ec": "LAKHIMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MWY",
    "en": "MAILARAM",
    "se": "TELANGANA"
  },
  {
    "sc": "MNQ",
    "en": "MAINPURI JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MPUE",
    "en": "MAINPURI KACHRI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MW",
    "en": "MAIRWA",
    "se": "BIHAR"
  },
  {
    "sc": "MASK",
    "en": "MAISAR KHANA",
    "se": "PUNJAB"
  },
  {
    "sc": "MSSN",
    "en": "MAISHASHAN",
    "se": "ASSAM"
  },
  {
    "sc": "MTO",
    "en": "MAITHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MVRD",
    "en": "MAIVADI ROAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MJHL",
    "en": "MAJADA HALT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MJBT",
    "en": "MAJBAT",
    "se": "ASSAM"
  },
  {
    "sc": "MJT",
    "en": "MAJERHAT",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MZQ",
    "en": "MAJGAON ASSAM",
    "se": "ASSAM"
  },
  {
    "sc": "MJG",
    "en": "MAJHAGAWAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MNHL",
    "en": "MAJHAIRAN HMCHL",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "MIJ",
    "en": "MAJHDIA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MAJ",
    "en": "MAJHERGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MJHR",
    "en": "MAJHIARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MJZ",
    "en": "MAJHOLA PAKARYA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MJL",
    "en": "MAJHOWLIA",
    "se": "BIHAR"
  },
  {
    "sc": "MJTA",
    "en": "MAJITHA",
    "se": "PUNJAB"
  },
  {
    "sc": "MJO",
    "en": "MAJORDA",
    "se": "GOA"
  },
  {
    "sc": "MJRI",
    "en": "MAJRI JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MJKN",
    "en": "MAJRI KHADAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MJNL",
    "en": "MAJRI NANGAL",
    "se": "HARYANA"
  },
  {
    "sc": "MAYA",
    "en": "MAKAKHAD",
    "se": "GUJARAT"
  },
  {
    "sc": "MU",
    "en": "MAKANSAR",
    "se": "GUJARAT"
  },
  {
    "sc": "MPR",
    "en": "MAKARPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "MKWI",
    "en": "MAKARWADI HALT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MDE",
    "en": "MAKHDUMPUR GAYA",
    "se": "BIHAR"
  },
  {
    "sc": "MKHI",
    "en": "MAKHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MXH",
    "en": "MAKHU",
    "se": "PUNJAB"
  },
  {
    "sc": "MKJ",
    "en": "MAKKAJIPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MNR",
    "en": "MAKKHANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MKL",
    "en": "MAKLIDRUG",
    "se": "KARNATAKA"
  },
  {
    "sc": "MKN",
    "en": "MAKRANA JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MQP",
    "en": "MAKRANDPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MKLI",
    "en": "MAKRAULI",
    "se": "HARYANA"
  },
  {
    "sc": "MKRA",
    "en": "MAKRERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MKRN",
    "en": "MAKRONIA",
    "ec": "SAUGOR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MKC",
    "en": "MAKSI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MKDI",
    "en": "MAKUDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MJN",
    "en": "MAKUM JN",
    "se": "ASSAM"
  },
  {
    "sc": "MALA",
    "en": "MALA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MDD",
    "en": "MALAD",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MFZ",
    "en": "MALAHAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MVA",
    "en": "MALAKAVEMULA H",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MKH",
    "en": "MALAKHERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MXT",
    "en": "MALAKPET",
    "ec": "SECUNDERABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "MLNH",
    "en": "MALANCHA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MLAR",
    "en": "MALANPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MLZ",
    "en": "MALARNA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MLS",
    "en": "MALASA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MLTJ",
    "en": "MALATAJ",
    "se": "GUJARAT"
  },
  {
    "sc": "MLT",
    "en": "MALATIPATPUR",
    "ec": "PURI",
    "se": "ODISHA"
  },
  {
    "sc": "MPE",
    "en": "MALATIPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MVY",
    "en": "MALAVI",
    "se": "KARNATAKA"
  },
  {
    "sc": "MVL",
    "en": "MALAVLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MLFC",
    "en": "MALDA COURT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MLDT",
    "en": "MALDA TOWN",
    "ec": "MALDA TOWN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MGVK",
    "en": "MALEGAON P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MET",
    "en": "MALERKOTLA",
    "se": "PUNJAB"
  },
  {
    "sc": "MEQ",
    "en": "MALETHU KANAK",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MAAR",
    "en": "MALHAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MLG",
    "en": "MALHARGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ML",
    "en": "MALHOUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MVG",
    "en": "MALIGURA",
    "se": "ODISHA"
  },
  {
    "sc": "MLD",
    "en": "MALIHABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MHTR",
    "en": "MALIHATI TBR RD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MKPT",
    "en": "MALIKPETH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MLKP",
    "en": "MALIKPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MLPR",
    "en": "MALIPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MALX",
    "en": "MALIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "MLHA",
    "en": "MALIYA HATINA",
    "se": "GUJARAT"
  },
  {
    "sc": "MALB",
    "en": "MALIYA MIYANA",
    "se": "GUJARAT"
  },
  {
    "sc": "MJF",
    "en": "MALKAJGIRI",
    "ec": "SECUNDERABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "MKU",
    "en": "MALKAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MALK",
    "en": "MALKAPUR ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MLK",
    "en": "MALKAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MLQ",
    "en": "MALKERA JN",
    "se": "JHARKHAND"
  },
  {
    "sc": "MQR",
    "en": "MALKHAID ROAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "MLR",
    "en": "MALKHED",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MLC",
    "en": "MALKISAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MNKR",
    "en": "MALLANKINAR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MQW",
    "en": "MALLANNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MWX",
    "en": "MALLANWALA KHAS",
    "se": "PUNJAB"
  },
  {
    "sc": "MLW",
    "en": "MALLANWAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MLGT",
    "en": "MALLAPPA GATE H",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MLP",
    "en": "MALLAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "MLV",
    "en": "MALLARPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MLSA",
    "en": "MALLASANDRA",
    "se": "KARNATAKA"
  },
  {
    "sc": "MVRM",
    "en": "MALLAVARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MLMG",
    "en": "MALLEMADUGU",
    "se": "TELANGANA"
  },
  {
    "sc": "MWM",
    "en": "MALLESWARAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "MKRH",
    "en": "MALLICKPUR HAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MAK",
    "en": "MALLIKPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MVW",
    "en": "MALLIVIDU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MYL",
    "en": "MALLIYALA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MY",
    "en": "MALLIYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MALR",
    "en": "MALLUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MOT",
    "en": "MALOUT",
    "se": "PUNJAB"
  },
  {
    "sc": "MLSU",
    "en": "MALSAILU",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MLSR",
    "en": "MALSAR",
    "se": "GUJARAT"
  },
  {
    "sc": "MQS",
    "en": "MALSIAN SHAHKHT",
    "se": "PUNJAB"
  },
  {
    "sc": "MTDI",
    "en": "MALTEKDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MLM",
    "en": "MALTHAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MLU",
    "en": "MALUGUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MLKA",
    "en": "MALUKA",
    "se": "JHARKHAND"
  },
  {
    "sc": "MXP",
    "en": "MALUPOTA",
    "se": "PUNJAB"
  },
  {
    "sc": "MLO",
    "en": "MALUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "MWH",
    "en": "MALWAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MBW",
    "en": "MALWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MOM",
    "en": "MAMAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MRM",
    "en": "MAMANDURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MBM",
    "en": "MAMBALAM",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MMP",
    "en": "MAMBALAPPATTU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MMPR",
    "en": "MAMDAPUR HALT",
    "se": "TELANGANA"
  },
  {
    "sc": "MIDP",
    "en": "MAMIDIPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "MANA",
    "en": "MANA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MVF",
    "en": "MANABAR",
    "se": "ODISHA"
  },
  {
    "sc": "MKG",
    "en": "MANAK NAGAR",
    "ec": "LUCKNOW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MNSR",
    "en": "MANAKSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MNM",
    "en": "MANAMADURAI JN",
    "ec": "RAMESWARAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MNZ",
    "en": "MANANI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MNP",
    "en": "MANANPUR",
    "se": "BIHAR"
  },
  {
    "sc": "MOW",
    "en": "MANANWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "MPA",
    "en": "MANAPARAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MRE",
    "en": "MANAURI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MCS",
    "en": "MANCHESWAR",
    "ec": "BHUBANESWAR",
    "se": "ODISHA"
  },
  {
    "sc": "MCLE",
    "en": "MANCHILI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MCI",
    "en": "MANCHIRYAL",
    "se": "TELANGANA"
  },
  {
    "sc": "MNF",
    "en": "MANDA ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MGF",
    "en": "MANDAGERE",
    "se": "KARNATAKA"
  },
  {
    "sc": "MDL",
    "en": "MANDAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MLGH",
    "en": "MANDALGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MDG",
    "en": "MANDALGHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MMZ",
    "en": "MANDAMARI",
    "se": "TELANGANA"
  },
  {
    "sc": "MDPD",
    "en": "MANDAPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MMM",
    "en": "MANDAPAM",
    "ec": "RAMESWARAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MC",
    "en": "MANDAPAM CAMP",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MDLE",
    "en": "MANDAR HILL",
    "ec": "BHAGALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "MMS",
    "en": "MANDASA ROAD",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MDS",
    "en": "MANDASOR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MDVD",
    "en": "MANDAVAD",
    "se": "GUJARAT"
  },
  {
    "sc": "MDVL",
    "en": "MANDAVALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MNDY",
    "en": "MANDAVELI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MURD",
    "en": "MANDAWAR M RD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MDWI",
    "en": "MANDAWARI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MNDV",
    "en": "MANDAWARIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MYD",
    "en": "MANDERDISA",
    "se": "ASSAM"
  },
  {
    "sc": "MYE",
    "en": "MANDHALI",
    "se": "PUNJAB"
  },
  {
    "sc": "MDA",
    "en": "MANDHANA JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MDH",
    "en": "MANDHAR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "ADR",
    "en": "MANDI ADAMPUR",
    "se": "HARYANA"
  },
  {
    "sc": "MABA",
    "en": "MANDI BAMORA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MBY",
    "en": "MANDI DABWALI",
    "se": "HARYANA"
  },
  {
    "sc": "MNDR",
    "en": "MANDI DHANAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MDDP",
    "en": "MANDI DIP",
    "ec": "BHOPAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "GVG",
    "en": "MANDIGOVINDGARH",
    "se": "PUNJAB"
  },
  {
    "sc": "MNDH",
    "en": "MANDIR HASAUD",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "MFR",
    "en": "MANDLA FORT",
    "ec": "NAINPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MDB",
    "en": "MANDOR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MXK",
    "en": "MANDRAK",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MAND",
    "en": "MANDURAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MWA",
    "en": "MANDWA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MYA",
    "en": "MANDYA",
    "se": "KARNATAKA"
  },
  {
    "sc": "MDGR",
    "en": "MANENDRAGARH",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "MANE",
    "en": "MANESWAR",
    "se": "ODISHA"
  },
  {
    "sc": "MAM",
    "en": "MANGAL MAHUDI",
    "se": "GUJARAT"
  },
  {
    "sc": "MAG",
    "en": "MANGALAGIRI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MPT",
    "en": "MANGALAMPETA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MLI",
    "en": "MANGALIYAWAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MAQ",
    "en": "MANGALURU CNTL",
    "ec": "MANGALURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "MAJN",
    "en": "MANGALURU JN",
    "ec": "MANGALURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "MNX",
    "en": "MANGANALLUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MNI",
    "en": "MANGAON",
    "ec": "RATNAGIRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MUM",
    "en": "MANGAPATNAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MGPM",
    "en": "MANGAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MGL",
    "en": "MANGELA",
    "se": "KARNATAKA"
  },
  {
    "sc": "MGG",
    "en": "MANGLIYA GAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MGLP",
    "en": "MANGOLPURI",
    "se": "DELHI"
  },
  {
    "sc": "MAZ",
    "en": "MANGRA",
    "se": "JHARKHAND"
  },
  {
    "sc": "MGRL",
    "en": "MANGROLLA",
    "se": "GUJARAT"
  },
  {
    "sc": "MXJ",
    "en": "MANGURJAN",
    "se": "BIHAR"
  },
  {
    "sc": "MHU",
    "en": "MANHERU",
    "se": "HARYANA"
  },
  {
    "sc": "MNMU",
    "en": "MANI MAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MIA",
    "en": "MANIA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MGI",
    "en": "MANIGACHI",
    "se": "BIHAR"
  },
  {
    "sc": "MGLE",
    "en": "MANIGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MHI",
    "en": "MANIHARI",
    "ec": "KATIHAR",
    "se": "BIHAR"
  },
  {
    "sc": "MCF",
    "en": "MANIK CHAUREE H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "MAGH",
    "en": "MANIKGARH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MKP",
    "en": "MANIKPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MAKP",
    "en": "MANIKPURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MIK",
    "en": "MANIKUL",
    "se": "JHARKHAND"
  },
  {
    "sc": "MAN",
    "en": "MANINAGAR",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "MIM",
    "en": "MANIRAM",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MGKP",
    "en": "MANISINGH K P",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MJBK",
    "en": "MANJARI BUDRUK",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MCJ",
    "en": "MANJATTIDAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MJS",
    "en": "MANJESHWAR",
    "se": "KERALA"
  },
  {
    "sc": "MJV",
    "en": "MANJHAGARH",
    "se": "BIHAR"
  },
  {
    "sc": "MHT",
    "en": "MANJHI",
    "se": "BIHAR"
  },
  {
    "sc": "MNJR",
    "en": "MANJHLEPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MJPB",
    "en": "MANJHRA PURAB",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MZW",
    "en": "MANJHWE",
    "se": "BIHAR"
  },
  {
    "sc": "MJRL",
    "en": "MANJROL",
    "se": "GUJARAT"
  },
  {
    "sc": "MZZ",
    "en": "MANJURI ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "MUR",
    "en": "MANKAPUR JN",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MNAE",
    "en": "MANKAR",
    "ec": "ASANSOL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MNY",
    "en": "MANKARAI",
    "se": "KERALA"
  },
  {
    "sc": "MKB",
    "en": "MANKATHA",
    "se": "BIHAR"
  },
  {
    "sc": "MNKD",
    "en": "MANKHURD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MANK",
    "en": "MANKI",
    "se": "KARNATAKA"
  },
  {
    "sc": "MUU",
    "en": "MANKUNDU",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MMR",
    "en": "MANMAD JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MNUR",
    "en": "MANNANUR",
    "se": "KERALA"
  },
  {
    "sc": "MQ",
    "en": "MANNARGUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MOB",
    "en": "MANOHARABAD JN",
    "se": "TELANGANA"
  },
  {
    "sc": "MNJ",
    "en": "MANOHARGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MOU",
    "en": "MANOHARPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "MOA",
    "en": "MANOPAD",
    "se": "TELANGANA"
  },
  {
    "sc": "MPO",
    "en": "MANPUR JN",
    "se": "BIHAR"
  },
  {
    "sc": "MPG",
    "en": "MANPUR NAGARIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MSZ",
    "en": "MANSA",
    "se": "PUNJAB"
  },
  {
    "sc": "MNS",
    "en": "MANSHAHI",
    "se": "BIHAR"
  },
  {
    "sc": "MNE",
    "en": "MANSI JN",
    "se": "BIHAR"
  },
  {
    "sc": "MSP",
    "en": "MANSURPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MMPL",
    "en": "MANTAPAMPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MVH",
    "en": "MANTATTI",
    "se": "TELANGANA"
  },
  {
    "sc": "MALM",
    "en": "MANTHRALAYAM RD",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MUBR",
    "en": "MANU BAZAR",
    "se": "TRIPURA"
  },
  {
    "sc": "MBL",
    "en": "MANUBOLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MUGR",
    "en": "MANUGURU",
    "se": "TELANGANA"
  },
  {
    "sc": "MRD",
    "en": "MANUND",
    "se": "GUJARAT"
  },
  {
    "sc": "MAF",
    "en": "MANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MANW",
    "en": "MANWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MNVL",
    "en": "MANWAL",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "MKBH",
    "en": "MANWALA KOT BAK",
    "se": "PUNJAB"
  },
  {
    "sc": "MVO",
    "en": "MANWATH ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MQN",
    "en": "MANYAMKONDA",
    "se": "TELANGANA"
  },
  {
    "sc": "MZGI",
    "en": "MANZURGARHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MADA",
    "en": "MAONDA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MQJ",
    "en": "MARADAM HALT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MHA",
    "en": "MARAHRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MJY",
    "en": "MARAMJHIRI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MRPL",
    "en": "MARAMPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MZU",
    "en": "MARANDAHALLI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MAKM",
    "en": "MARARIKULAM",
    "se": "KERALA"
  },
  {
    "sc": "MXA",
    "en": "MARAUDA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "MRG",
    "en": "MARGHERITA",
    "se": "ASSAM"
  },
  {
    "sc": "MEW",
    "en": "MARHAURA",
    "ec": "CHHAPRA",
    "se": "BIHAR"
  },
  {
    "sc": "MAY",
    "en": "MARIAHU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MAV",
    "en": "MARIAMMANKOVIL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MXN",
    "en": "MARIANI JN",
    "ec": "JORHAT",
    "se": "ASSAM"
  },
  {
    "sc": "MRC",
    "en": "MARICHETHAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "MRKL",
    "en": "MARIKAL",
    "se": "TELANGANA"
  },
  {
    "sc": "MKM",
    "en": "MARIKUPPAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "MIU",
    "en": "MARIPAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MMI",
    "en": "MARIYAMANAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "MQQ",
    "en": "MARKAHANDI U HT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MRK",
    "en": "MARKAPUR ROAD",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MKO",
    "en": "MARKONA",
    "se": "ODISHA"
  },
  {
    "sc": "MKD",
    "en": "MARKUNDI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MRH",
    "en": "MARMAGAO",
    "se": "GOA"
  },
  {
    "sc": "MRL",
    "en": "MAROLI",
    "se": "GUJARAT"
  },
  {
    "sc": "MRF",
    "en": "MARPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "MIPM",
    "en": "MARRIPALEM PH",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MSGR",
    "en": "MARSHAGHAI ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "MRV",
    "en": "MARSUL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MPLM",
    "en": "MARTHIPALAYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MR",
    "en": "MARTUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "MUQ",
    "en": "MARUDUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MUGI",
    "en": "MARUGUTTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "MBGA",
    "en": "MARWAR BAGRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MBSK",
    "en": "MARWAR BALIA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MBNL",
    "en": "MARWAR BHINMAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MBT",
    "en": "MARWAR BIRTHI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MCPE",
    "en": "MARWAR CHAPRI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MJ",
    "en": "MARWAR JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MKHR",
    "en": "MARWAR KHARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KOF",
    "en": "MARWAR KORI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MWT",
    "en": "MARWAR LOHWAT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MMY",
    "en": "MARWAR MATHANYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MDW",
    "en": "MARWAR MUNDWA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MRWS",
    "en": "MARWAR RANAWAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MSQ",
    "en": "MARWAR RATANPRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MWJ",
    "en": "MARWASGRAM",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SO",
    "en": "MAS SLT COTAURS",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MSAE",
    "en": "MASAGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ME",
    "en": "MASAIPET",
    "se": "TELANGANA"
  },
  {
    "sc": "MUO",
    "en": "MASANGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MSE",
    "en": "MASANI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MSWA",
    "en": "MASANIWALA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MSS",
    "en": "MASARAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "MST",
    "en": "MASIT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MSW",
    "en": "MASKANWA",
    "ec": "BASTI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MSDH",
    "en": "MASNADIH",
    "se": "BIHAR"
  },
  {
    "sc": "MSOD",
    "en": "MASODHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MXD",
    "en": "MASOR ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "MHC",
    "en": "MASRAKH",
    "ec": "CHHAPRA",
    "se": "BIHAR"
  },
  {
    "sc": "MSDN",
    "en": "MASUDAN",
    "se": "BIHAR"
  },
  {
    "sc": "MSR",
    "en": "MASUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MTV",
    "en": "MATALKUNTA",
    "se": "TELANGANA"
  },
  {
    "sc": "MABG",
    "en": "MATANA BUZURG",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MRQ",
    "en": "MATARI",
    "se": "JHARKHAND"
  },
  {
    "sc": "MZX",
    "en": "MATARILA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MTH",
    "en": "MATAUNDH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MT",
    "en": "MATERA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MHBA",
    "en": "MATHABHANGA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MTA",
    "en": "MATHELA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MAE",
    "en": "MATHERAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MTBG",
    "en": "MATHIA BARGHAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MTUR",
    "en": "MATHUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MRT",
    "en": "MATHURA CANT",
    "ec": "MATHURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MRT",
    "en": "MATHURA CANT",
    "ec": "MATHURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MUW",
    "en": "MATHURAPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "MRPM",
    "en": "MATHURAPUR MOR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MPRD",
    "en": "MATHURAPUR RD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MTRA",
    "en": "MATIGARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MTB",
    "en": "MATLABPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MTU",
    "en": "MATMARI",
    "se": "KARNATAKA"
  },
  {
    "sc": "MQA",
    "en": "MATODA",
    "se": "GUJARAT"
  },
  {
    "sc": "MTNC",
    "en": "MATTANCHERI HLT",
    "se": "KERALA"
  },
  {
    "sc": "MEM",
    "en": "MAU AIMMA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MAU",
    "en": "MAU JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MRPR",
    "en": "MAU RANIPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MZH",
    "en": "MAUHARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MLY",
    "en": "MAULA ALI",
    "se": "TELANGANA"
  },
  {
    "sc": "MAUR",
    "en": "MAUR",
    "se": "PUNJAB"
  },
  {
    "sc": "MRGM",
    "en": "MAURIGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MAA",
    "en": "MAVAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MVLK",
    "en": "MAVELIKARA",
    "se": "KERALA"
  },
  {
    "sc": "MVPM",
    "en": "MAVELIPALAIYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MVC",
    "en": "MAVINKERE",
    "se": "KARNATAKA"
  },
  {
    "sc": "MVJ",
    "en": "MAVLI JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MARD",
    "en": "MAVUR ROAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MWAI",
    "en": "MAWAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MYK",
    "en": "MAYAKONDA",
    "se": "KARNATAKA"
  },
  {
    "sc": "MYU",
    "en": "MAYANOOR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MAYR",
    "en": "MAYAR",
    "se": "HARYANA"
  },
  {
    "sc": "MV",
    "en": "MAYILADUTURAI J",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MYGD",
    "en": "MAYNAGURI ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MYY",
    "en": "MAYYANAD",
    "se": "KERALA"
  },
  {
    "sc": "MGME",
    "en": "MCCLUSKIEGANJ",
    "se": "JHARKHAND"
  },
  {
    "sc": "MCSC",
    "en": "MCS CHHATARPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MCA",
    "en": "MECHEDA",
    "ec": "MECHEDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MCRD",
    "en": "MECHERI ROAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MDAK",
    "en": "MEDAK",
    "se": "TELANGANA"
  },
  {
    "sc": "MPU",
    "en": "MEDAPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MED",
    "en": "MEDCHAL",
    "se": "TELANGANA"
  },
  {
    "sc": "MDRA",
    "en": "MEDRA",
    "se": "GUJARAT"
  },
  {
    "sc": "MUT",
    "en": "MEERUT CANT",
    "ec": "MEERUT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MTC",
    "en": "MEERUT CITY",
    "ec": "MEERUT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MGRP",
    "en": "MEGH RAJ PURA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "MGN",
    "en": "MEGHNAGAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MGHP",
    "en": "MEGHPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "MGTD",
    "en": "MEGHPURTITODI",
    "se": "GUJARAT"
  },
  {
    "sc": "MNO",
    "en": "MEHNAR ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "MAI",
    "en": "MEHSI",
    "se": "BIHAR"
  },
  {
    "sc": "MJA",
    "en": "MEJA ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MKY",
    "en": "MEKKUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MMKB",
    "en": "MEKRA MEMERKHAB",
    "se": "BIHAR"
  },
  {
    "sc": "MEKM",
    "en": "MELAKKONNAKKULM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MEH",
    "en": "MELALATHUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MLTR",
    "en": "MELATTUR",
    "se": "KERALA"
  },
  {
    "sc": "MLMR",
    "en": "MELMARUVATTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MLYR",
    "en": "MELNARIYAPANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MPI",
    "en": "MELPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MELH",
    "en": "MELUSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MYM",
    "en": "MEMARI",
    "ec": "BARDDHAMAN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MNDP",
    "en": "MENDIPATHAR",
    "se": "MEGHALAYA"
  },
  {
    "sc": "MEU",
    "en": "MENDU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MQX",
    "en": "MERALGRAM",
    "se": "JHARKHAND"
  },
  {
    "sc": "MRDL",
    "en": "MERAMANDOLIL",
    "se": "ODISHA"
  },
  {
    "sc": "MPX",
    "en": "MERPANAIKKADU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MEC",
    "en": "MERTA CITY",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MTD",
    "en": "MERTA ROAD JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MESR",
    "en": "MESRA",
    "se": "JHARKHAND"
  },
  {
    "sc": "MSVN",
    "en": "MESWAN",
    "se": "GUJARAT"
  },
  {
    "sc": "MEE",
    "en": "METHAI",
    "se": "BIHAR"
  },
  {
    "sc": "METR",
    "en": "METHI TIKUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MTPI",
    "en": "METPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "MER",
    "en": "METPANJRA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MTE",
    "en": "METTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MTP",
    "en": "METUPALAIYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MTDM",
    "en": "METUR DAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MYX",
    "en": "METYAL SOHAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MVLI",
    "en": "MEVLI",
    "se": "GUJARAT"
  },
  {
    "sc": "MWE",
    "en": "MEWA NAWADA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MZA",
    "en": "MEZENGA S",
    "se": "ASSAM"
  },
  {
    "sc": "MWD",
    "en": "MHASAVAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MSDG",
    "en": "MHASODA DONGAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MHD",
    "en": "MHMDVD KHEDA RD",
    "se": "GUJARAT"
  },
  {
    "sc": "MHOW",
    "en": "MHOW"
  },
  {
    "sc": "MIAN",
    "en": "MIANGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MDN",
    "en": "MIDNAPORE",
    "ec": "KHARAGPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MIW",
    "en": "MIGHAUNA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MGE",
    "en": "MIGRENDISA",
    "se": "ASSAM"
  },
  {
    "sc": "MIN",
    "en": "MIHINPURWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MIH",
    "en": "MIHRAWAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MIL",
    "en": "MILAK",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MQG",
    "en": "MILANGARH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MVN",
    "en": "MILAVITTAN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MN",
    "en": "MINAMBAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MNPR",
    "en": "MINAPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "MXM",
    "en": "MINATCHIPURAM",
    "se": "KERALA"
  },
  {
    "sc": "MNL",
    "en": "MINCHNAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "MWG",
    "en": "MINDALA P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MNHA",
    "en": "MINDHA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MJR",
    "en": "MINJUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MPLI",
    "en": "MINNAMPALLI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MIRA",
    "en": "MIRA ROAD",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MRJ",
    "en": "MIRAJ JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MK",
    "en": "MIRANPUR KATRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MCQ",
    "en": "MIRCHADHORI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MIQ",
    "en": "MIRHAKUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MRJN",
    "en": "MIRJAN",
    "se": "KARNATAKA"
  },
  {
    "sc": "MQL",
    "en": "MIRKHAL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MRTL",
    "en": "MIRTHAL",
    "se": "PUNJAB"
  },
  {
    "sc": "MRGA",
    "en": "MIRYALAGUDA",
    "se": "TELANGANA"
  },
  {
    "sc": "MZC",
    "en": "MIRZA CHEUKI",
    "se": "JHARKHAND"
  },
  {
    "sc": "MZL",
    "en": "MIRZAPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "MZP",
    "en": "MIRZAPUR",
    "ec": "MIRZAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MBV",
    "en": "MIRZAPUR BCHAUD",
    "se": "HARYANA"
  },
  {
    "sc": "MBE",
    "en": "MIRZAPUR BNKIPR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MSMI",
    "en": "MISAMARI",
    "se": "ASSAM"
  },
  {
    "sc": "MSTH",
    "en": "MISRIKH TIRATH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MSO",
    "en": "MISROD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MTI",
    "en": "MITAWAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MITA",
    "en": "MITHA",
    "se": "GUJARAT"
  },
  {
    "sc": "MTHP",
    "en": "MITHAPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "MTLP",
    "en": "MITHILA DEEP",
    "se": "BIHAR"
  },
  {
    "sc": "MYGL",
    "en": "MIYAGAM K JN NG",
    "se": "GUJARAT"
  },
  {
    "sc": "MYG",
    "en": "MIYAGAM KARJAN",
    "se": "GUJARAT"
  },
  {
    "sc": "MINA",
    "en": "MIYANA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MNKB",
    "en": "MIYONKA BARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "HVR",
    "en": "MMAILARA HAVERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "MOBD",
    "en": "MOABUND",
    "se": "ASSAM"
  },
  {
    "sc": "MBH",
    "en": "MOBHA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "MG",
    "en": "MODELGRAM",
    "se": "PUNJAB"
  },
  {
    "sc": "MDNR",
    "en": "MODINAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MLB",
    "en": "MODNIMB",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MDPR",
    "en": "MODPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "MON",
    "en": "MODRAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MDKU",
    "en": "MODUKURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MOGA",
    "en": "MOGA",
    "ec": "LUDHIANA",
    "se": "PUNJAB"
  },
  {
    "sc": "MXZ",
    "en": "MOHADARA P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MHAD",
    "en": "MOHADI PRGN LNG",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MQE",
    "en": "MOHAMMADKHERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MNGR",
    "en": "MOHAN NAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MOJ",
    "en": "MOHANA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MLJ",
    "en": "MOHANLALGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MHUR",
    "en": "MOHANPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "MOPR",
    "en": "MOHANPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MONR",
    "en": "MOHANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MPML",
    "en": "MOHAPANI MAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MJP",
    "en": "MOHARAJPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "MHF",
    "en": "MOHARI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MBP",
    "en": "MOHIBULLAPUR",
    "ec": "LUCKNOW",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MOP",
    "en": "MOHITNAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MOG",
    "en": "MOHIUDDINNAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "MUZ",
    "en": "MOHIUDDINPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MHKT",
    "en": "MOHKHUTI",
    "se": "ASSAM"
  },
  {
    "sc": "MO",
    "en": "MOHOL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MHPE",
    "en": "MOHOPE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MOY",
    "en": "MOHRI",
    "se": "HARYANA"
  },
  {
    "sc": "MKSR",
    "en": "MOKALSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MKA",
    "en": "MOKAMEH JN",
    "se": "BIHAR"
  },
  {
    "sc": "MVP",
    "en": "MOKHASA KALVPDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MXL",
    "en": "MOKHOLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MGV",
    "en": "MOLAGAVALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MOMU",
    "en": "MOLAKALMURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "MIO",
    "en": "MOLISAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MFC",
    "en": "MONABARI",
    "se": "ASSAM"
  },
  {
    "sc": "MNCR",
    "en": "MONACHERRA",
    "se": "ASSAM"
  },
  {
    "sc": "MOF",
    "en": "MONDH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MGR",
    "en": "MONGHYR",
    "se": "BIHAR"
  },
  {
    "sc": "MANU",
    "en": "MONU",
    "se": "TRIPURA"
  },
  {
    "sc": "BYNR",
    "en": "MOOKAMBIKA ROAD",
    "ec": "UDUPI",
    "se": "KARNATAKA"
  },
  {
    "sc": "MOR",
    "en": "MOR",
    "se": "BIHAR"
  },
  {
    "sc": "MROA",
    "en": "MORA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MB",
    "en": "MORADABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MORA",
    "en": "MORAIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "MKX",
    "en": "MORAK",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MOD",
    "en": "MORAMPUDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MOX",
    "en": "MORAN",
    "se": "ASSAM"
  },
  {
    "sc": "MRHT",
    "en": "MORANHAT",
    "ec": "SIMALUGURI",
    "se": "ASSAM"
  },
  {
    "sc": "MAP",
    "en": "MORAPPUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MVI",
    "en": "MORBI",
    "se": "GUJARAT"
  },
  {
    "sc": "MWK",
    "en": "MORDAD TANDA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MRDD",
    "en": "MORDAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MRA",
    "en": "MORENA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MGAE",
    "en": "MORGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MOI",
    "en": "MORI BERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MRND",
    "en": "MORINDA",
    "se": "PUNJAB"
  },
  {
    "sc": "MKDN",
    "en": "MORKADHANA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MRSH",
    "en": "MORSHI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MRTD",
    "en": "MORTAD",
    "se": "TELANGANA"
  },
  {
    "sc": "MXO",
    "en": "MORTHALA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MRN",
    "en": "MORWANI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MSU",
    "en": "MOSUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MOTA",
    "en": "MOTA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MQZ",
    "en": "MOTA JADRA",
    "se": "GUJARAT"
  },
  {
    "sc": "MNGV",
    "en": "MOTA MIYA MNGRL",
    "se": "GUJARAT"
  },
  {
    "sc": "MTSK",
    "en": "MOTA SURKA",
    "se": "GUJARAT"
  },
  {
    "sc": "MWQ",
    "en": "MOTARI HALT",
    "se": "ODISHA"
  },
  {
    "sc": "MOTH",
    "en": "MOTH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MTHH",
    "en": "MOTHALA HALT",
    "se": "GUJARAT"
  },
  {
    "sc": "MTKD",
    "en": "MOTI KHAWDI",
    "se": "GUJARAT"
  },
  {
    "sc": "MKRL",
    "en": "MOTI KORAL",
    "se": "GUJARAT"
  },
  {
    "sc": "MOTC",
    "en": "MOTICHUR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "MOTG",
    "en": "MOTIGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MCO",
    "en": "MOTIHARI COURT",
    "se": "BIHAR"
  },
  {
    "sc": "MTJL",
    "en": "MOTIJHEEL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MTR",
    "en": "MOTIPUR",
    "se": "BIHAR"
  },
  {
    "sc": "MTPC",
    "en": "MOTIPURA CHAUKI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MTMI",
    "en": "MOTUMARI",
    "se": "TELANGANA"
  },
  {
    "sc": "OTR",
    "en": "MOTURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MWAD",
    "en": "MOWAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MCTM",
    "en": "MTYR C TUSHAR M",
    "ec": "Jammu",
    "se": "JAMMU AND KASHMIR",
    "tg": "VAISHNODEVI"
  },
  {
    "sc": "MAKG",
    "en": "MUALKHANG",
    "se": "MIZORAM"
  },
  {
    "sc": "MDLL",
    "en": "MUDDALINGAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "MOO",
    "en": "MUDDANURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MGB",
    "en": "MUDIGUBBA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MUE",
    "en": "MUDKHED",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MUDI",
    "en": "MUDUDI",
    "se": "KARNATAKA"
  },
  {
    "sc": "MFJ",
    "en": "MUFTIGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MGD",
    "en": "MUGAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "MUY",
    "en": "MUGAIYUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MGC",
    "en": "MUGAT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MMU",
    "en": "MUGMA",
    "se": "JHARKHAND"
  },
  {
    "sc": "MMA",
    "en": "MUHAMMADABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MDJ",
    "en": "MUHAMMADGANJ",
    "se": "JHARKHAND"
  },
  {
    "sc": "MHP",
    "en": "MUHAMMADPUR",
    "se": "BIHAR"
  },
  {
    "sc": "MPF",
    "en": "MUIRPUR ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MJE",
    "en": "MUJNAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MEX",
    "en": "MUKERIAN",
    "ec": "JALANDHAR",
    "se": "PUNJAB"
  },
  {
    "sc": "MKSP",
    "en": "MUKHASA PARUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MKT",
    "en": "MUKHTIAR BALWAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MUKE",
    "en": "MUKKALI",
    "se": "KERALA"
  },
  {
    "sc": "MKPR",
    "en": "MUKTAPUR",
    "se": "BIHAR"
  },
  {
    "sc": "MPM",
    "en": "MUKTAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MKS",
    "en": "MUKTSAR",
    "ec": "KOT KAPURA",
    "se": "PUNJAB"
  },
  {
    "sc": "MCN",
    "en": "MUKUNDARAYAPURM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MKDD",
    "en": "MUKUNDAWADI HA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MFA",
    "en": "MUKURIA",
    "se": "BIHAR"
  },
  {
    "sc": "MME",
    "en": "MUL MARORA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MCU",
    "en": "MULACALACHERUVU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MGK",
    "en": "MULAGUNNATHUKVU",
    "se": "KERALA"
  },
  {
    "sc": "MNTT",
    "en": "MULANTURUTTI",
    "se": "KERALA"
  },
  {
    "sc": "MAR",
    "en": "MULANUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MLKH",
    "en": "MULEWAL KHAIHRA",
    "se": "PUNJAB"
  },
  {
    "sc": "MOL",
    "en": "MULI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "MULK",
    "en": "MULKI",
    "ec": "UDUPI",
    "se": "KARNATAKA"
  },
  {
    "sc": "MLX",
    "en": "MULLANPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "MUC",
    "en": "MULLURCARAI",
    "se": "KERALA"
  },
  {
    "sc": "MTY",
    "en": "MULTAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MLND",
    "en": "MULUND",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MVD",
    "en": "MULVAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "BCT",
    "en": "MUMBAI CENTRAL",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MBQ",
    "en": "MUMBRA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MBF",
    "en": "MUNABAO",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MGPA",
    "en": "MUNDA GOPAL ASH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MDLM",
    "en": "MUNDALARAM",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MND",
    "en": "MUNDERWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MPH",
    "en": "MUNDHA PANDE",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MVE",
    "en": "MUNDHEWADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MNU",
    "en": "MUNDIKOTA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MYP",
    "en": "MUNDILYAMPAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MQC",
    "en": "MUNDKA",
    "se": "DELHI"
  },
  {
    "sc": "MDLA",
    "en": "MUNDLANA",
    "se": "HARYANA"
  },
  {
    "sc": "MNV",
    "en": "MUNGAOLI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "MGKM",
    "en": "MUNGIAKAMI",
    "se": "TRIPURA"
  },
  {
    "sc": "MNPT",
    "en": "MUNGILIPATTU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MNGD",
    "en": "MUNIGUDA",
    "se": "ODISHA"
  },
  {
    "sc": "MRB",
    "en": "MUNIRABAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "MQO",
    "en": "MUNROTURUTTU",
    "se": "KERALA"
  },
  {
    "sc": "MUK",
    "en": "MUNUMAKA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MUPA",
    "en": "MUPA",
    "se": "ASSAM"
  },
  {
    "sc": "MDF",
    "en": "MURADI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MUD",
    "en": "MURADNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MGM",
    "en": "MURAGACHA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MRHA",
    "en": "MURAHARA",
    "se": "BIHAR"
  },
  {
    "sc": "MRTA",
    "en": "MURAITHA",
    "se": "BIHAR"
  },
  {
    "sc": "MRR",
    "en": "MURARAI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MPY",
    "en": "MURARPUR",
    "se": "BIHAR"
  },
  {
    "sc": "MRDW",
    "en": "MURDESHWAR",
    "ec": "KARWAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "MMVR",
    "en": "MURGAMAHADEV RD",
    "se": "ODISHA"
  },
  {
    "sc": "MSRP",
    "en": "MURHESI RAMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MUP",
    "en": "MURHIPAR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "MURI",
    "en": "MURI",
    "se": "JHARKHAND"
  },
  {
    "sc": "MRBL",
    "en": "MURIBAHAL",
    "se": "ODISHA"
  },
  {
    "sc": "MZS",
    "en": "MURKONGSELEK",
    "se": "ASSAM"
  },
  {
    "sc": "MRIJ",
    "en": "MURLIGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "MSN",
    "en": "MURSAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MSDR",
    "en": "MURSHADPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MBB",
    "en": "MURSHIDABAD",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MZR",
    "en": "MURTAJAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MZRT",
    "en": "MURTAJAPUR TOWN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MUH",
    "en": "MURTHIHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MRTY",
    "en": "MURTI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MRX",
    "en": "MURUD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MQU",
    "en": "MURUKKAMPUZHA",
    "se": "KERALA"
  },
  {
    "sc": "MFKA",
    "en": "MUSAFIR KHANA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MSBR",
    "en": "MUSAHIBPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "MUA",
    "en": "MUSRA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "MBD",
    "en": "MUSTABADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "MFB",
    "en": "MUSTAFABAD",
    "se": "HARYANA"
  },
  {
    "sc": "MFCK",
    "en": "MUSTAPHA CHAK",
    "se": "WEST BENGAL"
  },
  {
    "sc": "MSV",
    "en": "MUSTARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MMDA",
    "en": "MUTHALAMADA",
    "se": "KERALA"
  },
  {
    "sc": "MTGE",
    "en": "MUTHANI",
    "se": "BIHAR"
  },
  {
    "sc": "MPC",
    "en": "MUTTAMPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MTNL",
    "en": "MUTTARASANALLUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MTT",
    "en": "MUTUPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "MUVL",
    "en": "MUVAL TANK",
    "se": "GUJARAT"
  },
  {
    "sc": "MOZ",
    "en": "MUZAFFARNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "MZM",
    "en": "MUZZAMPUR NRYN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NCBD",
    "en": "N CHANGRABANDHA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "GZN",
    "en": "N GHAZIABAD",
    "ec": "NEW DELHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NJM",
    "en": "N J RAMANAL"
  },
  {
    "sc": "NMBR",
    "en": "N MAYURBHANJ RD",
    "se": "ODISHA"
  },
  {
    "sc": "NSS",
    "en": "N S DOABA JN",
    "ec": "PHAGWARA",
    "se": "PUNJAB"
  },
  {
    "sc": "NPK",
    "en": "N. PANAKUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NDAE",
    "en": "NABADWIP DHAM",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NDF",
    "en": "NABADWIP GHAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NBAE",
    "en": "NABAGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NBA",
    "en": "NABHA",
    "se": "PUNJAB"
  },
  {
    "sc": "NBG",
    "en": "NABINAGAR ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "NIU",
    "en": "NABIPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "NCN",
    "en": "NACHINDA P H",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NADA",
    "en": "NADA",
    "se": "GUJARAT"
  },
  {
    "sc": "NAU",
    "en": "NADAPURAM ROAD",
    "se": "KERALA"
  },
  {
    "sc": "NDU",
    "en": "NADAUJ",
    "se": "BIHAR"
  },
  {
    "sc": "NBI",
    "en": "NADBAI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NDG",
    "en": "NADGAM",
    "se": "GUJARAT"
  },
  {
    "sc": "ND",
    "en": "NADIAD JN",
    "se": "GUJARAT"
  },
  {
    "sc": "NPU",
    "en": "NADIAPUR",
    "se": "TRIPURA"
  },
  {
    "sc": "NDKD",
    "en": "NADIKUDI JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NDW",
    "en": "NADWAN",
    "se": "BIHAR"
  },
  {
    "sc": "NGL",
    "en": "NAGAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NPL",
    "en": "NAGALAPALLE",
    "se": "TELANGANA"
  },
  {
    "sc": "NVC",
    "en": "NAGALWANCHA",
    "se": "TELANGANA"
  },
  {
    "sc": "NHY",
    "en": "NAGANAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "NGS",
    "en": "NAGANSUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NGAN",
    "en": "NAGAON",
    "ec": "CHAPARMUKH",
    "se": "ASSAM"
  },
  {
    "sc": "NGT",
    "en": "NAGAPPATTINAM",
    "ec": "NAGAPPATTINAM/VELANKANNI/KARAIKAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NGE",
    "en": "NAGAR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "NUQ",
    "en": "NAGAR UNTARI",
    "se": "JHARKHAND"
  },
  {
    "sc": "NGD",
    "en": "NAGARDEVLA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NAG",
    "en": "NAGARGALI",
    "se": "KARNATAKA"
  },
  {
    "sc": "NG",
    "en": "NAGARI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NGI",
    "en": "NAGARI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NRS",
    "en": "NAGARIA SADAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NGF",
    "en": "NAGARNABI",
    "se": "JHARKHAND"
  },
  {
    "sc": "NSL",
    "en": "NAGARSOL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NRR",
    "en": "NAGARUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NWA",
    "en": "NAGARWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NGM",
    "en": "NAGASAMUDRAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NGO",
    "en": "NAGAUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NVF",
    "en": "NAGAVANGALA",
    "se": "KARNATAKA"
  },
  {
    "sc": "NAB",
    "en": "NAGBHIR JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NAD",
    "en": "NAGDA JN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NJT",
    "en": "NAGER COIL TOWN",
    "ec": "KANYAKUMARI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NCJ",
    "en": "NAGERCOIL JN",
    "ec": "KANYAKUMARI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NGHW",
    "en": "NAGESHWADI HALT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NGG",
    "en": "NAGINA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NRDP",
    "en": "NAGIREDDIPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "NJA",
    "en": "NAGJUA",
    "se": "JHARKHAND"
  },
  {
    "sc": "NGLT",
    "en": "NAGLATULA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NCR",
    "en": "NAGORE",
    "ec": "NAGAPPATTINAM/VELANKANNI/KARAIKAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NGTN",
    "en": "NAGOTHANE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NPRD",
    "en": "NAGPUR ROAD P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "NKB",
    "en": "NAGRAKOTA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NGRT",
    "en": "NAGROTA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "NGRS",
    "en": "NAGROTA SURIYAM",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "NXR",
    "en": "NAGSAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NRH",
    "en": "NAHARGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NHK",
    "en": "NAHARKATIYA",
    "se": "ASSAM"
  },
  {
    "sc": "NHLN",
    "en": "NAHARLAGUN",
    "se": "ARUNACHAL PRADESH"
  },
  {
    "sc": "NAH",
    "en": "NAHIYER",
    "se": "GUJARAT"
  },
  {
    "sc": "NIG",
    "en": "NAIGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NH",
    "en": "NAIHATI JN",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NAKD",
    "en": "NAIK DIH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NKI",
    "en": "NAIKHERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NIT",
    "en": "NAIKOT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NLN",
    "en": "NAILALUNG",
    "se": "ASSAM"
  },
  {
    "sc": "NM",
    "en": "NAIMISHARANYA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NYN",
    "en": "NAINI",
    "ec": "PRAYAGRAJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NIR",
    "en": "NAINPUR JN",
    "ec": "NAINPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NBD",
    "en": "NAJIBABAD JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NCH",
    "en": "NAKACHARI",
    "se": "ASSAM"
  },
  {
    "sc": "JEA",
    "en": "NAKAHA JUNGLE",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NKDO",
    "en": "NAKKANADODDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NRO",
    "en": "NAKODAR JN",
    "se": "PUNJAB"
  },
  {
    "sc": "NAK",
    "en": "NAKSALBARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NKX",
    "en": "NAKTISEMRA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "NAL",
    "en": "NAL HALT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NLD",
    "en": "NALANDA",
    "se": "BIHAR"
  },
  {
    "sc": "NLV",
    "en": "NALBARI",
    "se": "ASSAM"
  },
  {
    "sc": "NLDA",
    "en": "NALGONDA",
    "se": "TELANGANA"
  },
  {
    "sc": "NHT",
    "en": "NALHATI JN",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NKL",
    "en": "NALIKUL",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NLY",
    "en": "NALIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "NLC",
    "en": "NALIYA CANTT",
    "se": "GUJARAT"
  },
  {
    "sc": "NLKT",
    "en": "NALKATA",
    "se": "TRIPURA"
  },
  {
    "sc": "NSP",
    "en": "NALLA SOPARA",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NCU",
    "en": "NALLACHERUVU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NLPD",
    "en": "NALLAPADU JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NLL",
    "en": "NALLI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "BVZ",
    "en": "NALOI BARWA",
    "se": "HARYANA"
  },
  {
    "sc": "NALR",
    "en": "NALPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NW",
    "en": "NALWAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "NMKL",
    "en": "NAMAKKAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NMN",
    "en": "NAMANASAMUDRAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NBR",
    "en": "NAMBURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NMKA",
    "en": "NAMKHANA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NKM",
    "en": "NAMKON",
    "ec": "HATIA/RANCHI",
    "se": "JHARKHAND"
  },
  {
    "sc": "NLI",
    "en": "NAMLI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NAM",
    "en": "NAMRUP",
    "se": "ASSAM"
  },
  {
    "sc": "NMT",
    "en": "NAMTIALI",
    "se": "ASSAM"
  },
  {
    "sc": "NANA",
    "en": "NANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NBHM",
    "en": "NANA BHAMODRA",
    "se": "GUJARAT"
  },
  {
    "sc": "NNKR",
    "en": "NANAKSAR",
    "se": "PUNJAB"
  },
  {
    "sc": "NNX",
    "en": "NANAUTA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NLA",
    "en": "NANCHERLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NRE",
    "en": "NANDALUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NNNL",
    "en": "NANDANI LAGUNIA",
    "se": "BIHAR"
  },
  {
    "sc": "NDPR",
    "en": "NANDAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NDKH",
    "en": "NANDARKHA",
    "se": "GUJARAT"
  },
  {
    "sc": "NDR",
    "en": "NANDESARI",
    "se": "GUJARAT"
  },
  {
    "sc": "NDJ",
    "en": "NANDGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NGN",
    "en": "NANDGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NAN",
    "en": "NANDGAON ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NAND",
    "en": "NANDIKOOR",
    "se": "KARNATAKA"
  },
  {
    "sc": "NDLH",
    "en": "NANDLALEE HALT",
    "se": "BIHAR"
  },
  {
    "sc": "NHM",
    "en": "NANDOL DEHEGAM",
    "se": "GUJARAT"
  },
  {
    "sc": "NDBT",
    "en": "NANDPR BHATAULI",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "NDE",
    "en": "NANDRE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NN",
    "en": "NANDURA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NDB",
    "en": "NANDURBAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NDL",
    "en": "NANDYAL JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NLDM",
    "en": "NANGAL DAM",
    "se": "PUNJAB"
  },
  {
    "sc": "NDRT",
    "en": "NANGAL DEGROTA",
    "se": "HARYANA"
  },
  {
    "sc": "NNU",
    "en": "NANGAL MUNDI",
    "se": "HARYANA"
  },
  {
    "sc": "NLQ",
    "en": "NANGAL PATHANI",
    "se": "HARYANA"
  },
  {
    "sc": "NAI",
    "en": "NANGI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NRWN",
    "en": "NANGL RAJAWATAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NNO",
    "en": "NANGLOI",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "NNN",
    "en": "NANGUNERI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NBRL",
    "en": "NANI BARAL",
    "se": "GUJARAT"
  },
  {
    "sc": "NTW",
    "en": "NANJANGUD TOWN",
    "se": "KARNATAKA"
  },
  {
    "sc": "NNM",
    "en": "NANNILAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NNP",
    "en": "NANPARA JN",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NWN",
    "en": "NANWAN",
    "se": "HARYANA"
  },
  {
    "sc": "NJN",
    "en": "NAOJAN",
    "se": "ASSAM"
  },
  {
    "sc": "NPS",
    "en": "NAPASAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NAR",
    "en": "NAR",
    "se": "GUJARAT"
  },
  {
    "sc": "NTN",
    "en": "NAR TOWN",
    "se": "GUJARAT"
  },
  {
    "sc": "NRK",
    "en": "NARAIKKINAR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NRI",
    "en": "NARAINA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NRVR",
    "en": "NARAINA VIHAR",
    "se": "DELHI"
  },
  {
    "sc": "NQR",
    "en": "NARAJ MARTHAPUR",
    "ec": "CUTTACK",
    "se": "ODISHA"
  },
  {
    "sc": "NNGE",
    "en": "NARANGI",
    "se": "ASSAM"
  },
  {
    "sc": "NRGR",
    "en": "NARANJIPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NANR",
    "en": "NARANPUR",
    "se": "ODISHA"
  },
  {
    "sc": "NBU",
    "en": "NARASAMBUDHI",
    "se": "KARNATAKA"
  },
  {
    "sc": "NS",
    "en": "NARASAPUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NRT",
    "en": "NARASARAOPET",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NPT",
    "en": "NARASINGAMPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NASP",
    "en": "NARASINGAPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NSGR",
    "en": "NARASINGHGARH",
    "se": "ODISHA"
  },
  {
    "sc": "NRSP",
    "en": "NARASMHAPURA"
  },
  {
    "sc": "NRYP",
    "en": "NARAYANAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NYDO",
    "en": "NARAYANDOHO",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NYA",
    "en": "NARAYANGARH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NRPD",
    "en": "NARAYANPET ROAD"
  },
  {
    "sc": "NNR",
    "en": "NARAYANPUR",
    "se": "BIHAR"
  },
  {
    "sc": "NPBR",
    "en": "NARAYANPURBAZAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NRPA",
    "en": "NARAYNPUR ANANT",
    "se": "BIHAR"
  },
  {
    "sc": "NDN",
    "en": "NARDANA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NUR",
    "en": "NARELA",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "NRUR",
    "en": "NARESHWAR ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "NRGO",
    "en": "NARGANJO",
    "se": "BIHAR"
  },
  {
    "sc": "NRN",
    "en": "NARHAN",
    "se": "BIHAR"
  },
  {
    "sc": "NRKE",
    "en": "NARI KHETRI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NROD",
    "en": "NARI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "NOI",
    "en": "NARIAOLI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NKK",
    "en": "NARIKKUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NRJ",
    "en": "NARIMOGARU",
    "se": "KARNATAKA"
  },
  {
    "sc": "NPX",
    "en": "NARINDARPURA",
    "se": "PUNJAB"
  },
  {
    "sc": "NRV",
    "en": "NARIYAR",
    "se": "BIHAR"
  },
  {
    "sc": "NKE",
    "en": "NARKATIAGANJ JN",
    "se": "BIHAR"
  },
  {
    "sc": "NKPL",
    "en": "NARKETPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "NRKR",
    "en": "NARKHER",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NRKP",
    "en": "NARKOPI",
    "se": "JHARKHAND"
  },
  {
    "sc": "NDPM",
    "en": "NARMADAPURAM",
    "ec": "PIPARIYA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NNL",
    "en": "NARNAUL",
    "se": "HARYANA"
  },
  {
    "sc": "NRD",
    "en": "NARODA",
    "se": "GUJARAT"
  },
  {
    "sc": "NPV",
    "en": "NARPATGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "NU",
    "en": "NARSINGHPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NRP",
    "en": "NARSIPATNAM RD",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NSX",
    "en": "NARSIPURAM HALT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NTM",
    "en": "NARTHAMALAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NHX",
    "en": "NARTHAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NRW",
    "en": "NARWANA JN",
    "se": "HARYANA"
  },
  {
    "sc": "NRWI",
    "en": "NARWASI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NSO",
    "en": "NASHIPUR ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NSF",
    "en": "NASIBPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NSD",
    "en": "NASIRABAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NSN",
    "en": "NASIRPUR HALT",
    "se": "DELHI"
  },
  {
    "sc": "NSKL",
    "en": "NASKHAL",
    "se": "TELANGANA"
  },
  {
    "sc": "NAS",
    "en": "NASRALA",
    "se": "PUNJAB"
  },
  {
    "sc": "NSW",
    "en": "NASWADI",
    "se": "GUJARAT"
  },
  {
    "sc": "NES",
    "en": "NATESAR",
    "se": "BIHAR"
  },
  {
    "sc": "NTT",
    "en": "NATHAPETTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NDT",
    "en": "NATHDWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NGY",
    "en": "NATHGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "NAT",
    "en": "NATHNAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "NT",
    "en": "NATHPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "NKH",
    "en": "NATHUKHERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NTZ",
    "en": "NATHWANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NNA",
    "en": "NAUGACHIA",
    "se": "BIHAR"
  },
  {
    "sc": "NGW",
    "en": "NAUGANWAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NLH",
    "en": "NAULTHA",
    "se": "HARYANA"
  },
  {
    "sc": "NWP",
    "en": "NAUPADA JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NTV",
    "en": "NAUTANWA",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NBM",
    "en": "NAVABPALEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NVRD",
    "en": "NAVADE ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NUD",
    "en": "NAVAGADH",
    "se": "GUJARAT"
  },
  {
    "sc": "NVLN",
    "en": "NAVALGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NVD",
    "en": "NAVALGUND RD",
    "se": "KARNATAKA"
  },
  {
    "sc": "NVU",
    "en": "NAVALUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "NANH",
    "en": "NAVANAGAR HALT",
    "se": "KARNATAKA"
  },
  {
    "sc": "NWU",
    "en": "NAVAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NVT",
    "en": "NAVIPET",
    "se": "TELANGANA"
  },
  {
    "sc": "NLK",
    "en": "NAVLAKHI",
    "se": "GUJARAT"
  },
  {
    "sc": "NVS",
    "en": "NAVSARI",
    "se": "GUJARAT"
  },
  {
    "sc": "NAC",
    "en": "NAWA CITY",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NGB",
    "en": "NAWABGANJ GONDA",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NWD",
    "en": "NAWADAH",
    "se": "BIHAR"
  },
  {
    "sc": "NADI",
    "en": "NAWADGI",
    "se": "KARNATAKA"
  },
  {
    "sc": "NWDH",
    "en": "NAWADIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "NVG",
    "en": "NAWAGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NWH",
    "en": "NAWALGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NAWN",
    "en": "NAWAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NAW",
    "en": "NAWANDGI",
    "se": "TELANGANA"
  },
  {
    "sc": "NPD",
    "en": "NAWAPARA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "NYK",
    "en": "NAYA KHARADIA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NWC",
    "en": "NAYA NAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "NNGL",
    "en": "NAYA NANGAL",
    "se": "PUNJAB"
  },
  {
    "sc": "NBT",
    "en": "NAYABAGIRTHIPUR",
    "se": "ODISHA"
  },
  {
    "sc": "NYO",
    "en": "NAYAGAON",
    "se": "BIHAR"
  },
  {
    "sc": "NYG",
    "en": "NAYAGARH",
    "se": "ODISHA"
  },
  {
    "sc": "NYGT",
    "en": "NAYAGARH TOWN",
    "se": "ODISHA"
  },
  {
    "sc": "NYH",
    "en": "NAYANDAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "NYT",
    "en": "NAYATOLA",
    "se": "BIHAR"
  },
  {
    "sc": "NI",
    "en": "NAYDONGRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NYP",
    "en": "NAYUDUPETA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NZG",
    "en": "NAZARBAG",
    "se": "GUJARAT"
  },
  {
    "sc": "NZT",
    "en": "NAZARETH",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NZR",
    "en": "NAZIRA",
    "se": "ASSAM"
  },
  {
    "sc": "NAZJ",
    "en": "NAZIRGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "NMO",
    "en": "NEDI MOLLYANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NKD",
    "en": "NEKONDA",
    "se": "TELANGANA"
  },
  {
    "sc": "NMGA",
    "en": "NELAMANGALA",
    "se": "KARNATAKA"
  },
  {
    "sc": "NYI",
    "en": "NELLAYI",
    "se": "KERALA"
  },
  {
    "sc": "NPM",
    "en": "NELLIKUPPAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NML",
    "en": "NELLIMARIA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NLR",
    "en": "NELLORE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NLS",
    "en": "NELLORE SOUTH",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NLPI",
    "en": "NEMALIPURI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NEP",
    "en": "NENPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "NEI",
    "en": "NEOLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NEO",
    "en": "NEORA",
    "se": "BIHAR"
  },
  {
    "sc": "NPR",
    "en": "NEPALGANJ ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NPNR",
    "en": "NEPANAGAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NRL",
    "en": "NERAL",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NRF",
    "en": "NERALAKATTE",
    "se": "KARNATAKA"
  },
  {
    "sc": "NRG",
    "en": "NERGUNDI",
    "se": "ODISHA"
  },
  {
    "sc": "NERI",
    "en": "NERI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NTWL",
    "en": "NETAWAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NTA",
    "en": "NETRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NET",
    "en": "NETRANG",
    "se": "GUJARAT"
  },
  {
    "sc": "NOQ",
    "en": "NEW ALIPURDUAR",
    "ec": "ALIPUR DUAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NAVI",
    "en": "NEW AMRAVATI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "AYVN",
    "en": "NEW ARYANKAVU",
    "se": "KERALA"
  },
  {
    "sc": "NAHT",
    "en": "NEW ASHTI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NBPH",
    "en": "NEW BALARAMPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NBS",
    "en": "NEW BANESWAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NBJU",
    "en": "NEW BARAUNI JN",
    "se": "BIHAR"
  },
  {
    "sc": "NBE",
    "en": "NEW BARRACKPORE",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NBVJ",
    "en": "NEW BHUJ",
    "ec": "BHUJ"
  },
  {
    "sc": "NBQ",
    "en": "NEW BONGAIGAON",
    "ec": "BONGAIGAON",
    "se": "ASSAM"
  },
  {
    "sc": "NCB",
    "en": "NEW COOCH BEHAR",
    "ec": "NEW COACHBEHAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NDNR",
    "en": "NEW DHANORA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NQH",
    "en": "NEW DOMOHANI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NFK",
    "en": "NEW FARAKKA JN",
    "ec": "MALDA TOWN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NGRH",
    "en": "NEW GIRIDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "NGTG",
    "en": "NEW GITLDADA JN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NGNT",
    "en": "NEW GUNTUR",
    "ec": "GUNTUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NHLG",
    "en": "NEW HAFLONG",
    "se": "ASSAM"
  },
  {
    "sc": "NHGJ",
    "en": "NEW HARANGAJAO",
    "se": "ASSAM"
  },
  {
    "sc": "NJPS",
    "en": "NEW JALPAIGURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NKMG",
    "en": "NEW KARIMGANJ",
    "ec": "KARIMGANJ",
    "se": "ASSAM"
  },
  {
    "sc": "NKJ",
    "en": "NEW KATNI JN",
    "ec": "KATNI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NLNI",
    "en": "NEW LONI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NMZ",
    "en": "NEW MAL JN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NMX",
    "en": "NEW MAYNAGURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NMM",
    "en": "NEW MISAMARI",
    "se": "ASSAM"
  },
  {
    "sc": "NMDA",
    "en": "NEW MORINDA",
    "se": "PUNJAB"
  },
  {
    "sc": "NSBG",
    "en": "NEW SISIBORGAON",
    "se": "ASSAM"
  },
  {
    "sc": "NTSK",
    "en": "NEW TINSUKIA JN",
    "ec": "TINSUKIA",
    "se": "ASSAM"
  },
  {
    "sc": "NEA",
    "en": "NEYKKARAPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NVL",
    "en": "NEYVELI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NYY",
    "en": "NEYYATTINKARA",
    "se": "KERALA"
  },
  {
    "sc": "NBP",
    "en": "NIBHAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NBUE",
    "en": "NIBKARORI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NDD",
    "en": "NIDADAVOLU JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NMJ",
    "en": "NIDAMANGALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NDM",
    "en": "NIDAMANURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NDNI",
    "en": "NIDHANI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NIDI",
    "en": "NIDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NDZ",
    "en": "NIDIGALLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NDO",
    "en": "NIDUBROLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NID",
    "en": "NIDUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NDV",
    "en": "NIDVANDA",
    "se": "KARNATAKA"
  },
  {
    "sc": "NGX",
    "en": "NIGAN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NTU",
    "en": "NIGATPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NIQ",
    "en": "NIGAURA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NHN",
    "en": "NIGOHAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NOH",
    "en": "NIGOHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NHF",
    "en": "NIHASTA HALT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NJB",
    "en": "NIJBARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NSI",
    "en": "NIKURSINI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NIIJ",
    "en": "NILAJE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NKW",
    "en": "NILAKANTHESWAR",
    "se": "ODISHA"
  },
  {
    "sc": "NLBR",
    "en": "NILAMBAZAR",
    "se": "ASSAM"
  },
  {
    "sc": "NIL",
    "en": "NILAMBUR ROAD",
    "se": "KERALA"
  },
  {
    "sc": "NLE",
    "en": "NILESHWAR",
    "se": "KERALA"
  },
  {
    "sc": "NGRD",
    "en": "NILGIRI ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "NLKR",
    "en": "NILOKHERI",
    "se": "HARYANA"
  },
  {
    "sc": "NMK",
    "en": "NIM KA THANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NIMG",
    "en": "NIMA GOPALPUR H",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NMH",
    "en": "NIMACH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NKR",
    "en": "NIMAR KHERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NBH",
    "en": "NIMBAHERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NBL",
    "en": "NIMBAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "NB",
    "en": "NIMBHORA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NIM",
    "en": "NIMDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "NMG",
    "en": "NIMIAGHAT",
    "se": "JHARKHAND"
  },
  {
    "sc": "NMP",
    "en": "NIMPURA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NILE",
    "en": "NIMTITA",
    "ec": "MALDA TOWN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NDH",
    "en": "NINDHAR BENAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NGA",
    "en": "NINGALA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "NPW",
    "en": "NIPANI VADGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NPI",
    "en": "NIPANIA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "NR",
    "en": "NIPHAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NIRA",
    "en": "NIRA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NKP",
    "en": "NIRAKARPUR",
    "ec": "KHURDA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "NMA",
    "en": "NIRMALI",
    "se": "BIHAR"
  },
  {
    "sc": "NXL",
    "en": "NIROL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NRLM",
    "en": "NIROLGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NSA",
    "en": "NISHANGARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NSZ",
    "en": "NISHATPURA",
    "ec": "BHOPAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NSU",
    "en": "NISUI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NTR",
    "en": "NITTUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "NEW",
    "en": "NIVARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NIV",
    "en": "NIVASAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NWR",
    "en": "NIWAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NWB",
    "en": "NIWAS ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NOL",
    "en": "NIYOL",
    "se": "GUJARAT"
  },
  {
    "sc": "NZB",
    "en": "NIZAMABAD JN",
    "se": "TELANGANA"
  },
  {
    "sc": "NIP",
    "en": "NIZAMPUR",
    "se": "HARYANA"
  },
  {
    "sc": "NBX",
    "en": "NIZBARGANJ",
    "se": "ASSAM"
  },
  {
    "sc": "NCA",
    "en": "NIZCHATIA",
    "se": "ASSAM"
  },
  {
    "sc": "NCE",
    "en": "NLACHRVURU EAST",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NMGT",
    "en": "NMG TAMDALGE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NRX",
    "en": "NOADAR DHAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NOMD",
    "en": "NOAMUNDI",
    "ec": "BARABIL",
    "se": "JHARKHAND"
  },
  {
    "sc": "NOB",
    "en": "NOBANDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "NGWN",
    "en": "NOGANWAN",
    "se": "PUNJAB"
  },
  {
    "sc": "NHB",
    "en": "NOH BACHHAMDI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NHR",
    "en": "NOHAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NOK",
    "en": "NOKHA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NKRA",
    "en": "NOKHRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NOLI",
    "en": "NOLI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NMD",
    "en": "NOMODA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NNPR",
    "en": "NONAPAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NNE",
    "en": "NONERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NNHT",
    "en": "NONIHAT",
    "se": "JHARKHAND"
  },
  {
    "sc": "NRLR",
    "en": "NORLA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "NLP",
    "en": "NORTH LAKHIMPUR",
    "se": "ASSAM"
  },
  {
    "sc": "NOA",
    "en": "NOSARIA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NOSM",
    "en": "NOSSAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NBGH",
    "en": "NOWBAGH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "NRZB",
    "en": "NOWROZABAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NOY",
    "en": "NOYAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NSVP",
    "en": "NPA SHVRAMPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "NRPM",
    "en": "NRP MURLI HALT",
    "se": "BIHAR"
  },
  {
    "sc": "NNW",
    "en": "NRYNPUR TATWAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NITR",
    "en": "NSC BOSE ITWARI",
    "ec": "NAGPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GMO",
    "en": "NSC BOSE J GOMO",
    "se": "JHARKHAND"
  },
  {
    "sc": "NUA",
    "en": "NUA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NUGN",
    "en": "NUAGAN",
    "se": "ODISHA"
  },
  {
    "sc": "NXN",
    "en": "NUAGAON",
    "se": "ODISHA"
  },
  {
    "sc": "NXNR",
    "en": "NUAGAON ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "NDPU",
    "en": "NUDURUPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NUJ",
    "en": "NUJELLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NLNR",
    "en": "NULEMURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "NMUE",
    "en": "NUMAISNGAH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NMGY",
    "en": "NUMALIGARH",
    "se": "ASSAM"
  },
  {
    "sc": "NBK",
    "en": "NUNGAMBAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "NRA",
    "en": "NUNKHAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NUB",
    "en": "NURABAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NRM",
    "en": "NURMAHAL",
    "se": "PUNJAB"
  },
  {
    "sc": "NRNR",
    "en": "NURNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "NUPR",
    "en": "NURPUR ROAD",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "NPH",
    "en": "NURPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "NZD",
    "en": "NUZVID",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "NKN",
    "en": "NYOLI KALAN",
    "se": "HARYANA"
  },
  {
    "sc": "NRY",
    "en": "NYORIYA HUSENPU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "OTN",
    "en": "OATING",
    "se": "ASSAM"
  },
  {
    "sc": "ODG",
    "en": "OBAIDULLA GANJ",
    "ec": "BHOPAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "OBM",
    "en": "OBALAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "OCH",
    "en": "OBHANIYA CHACHE",
    "se": "RAJASTHAN"
  },
  {
    "sc": "OBR",
    "en": "OBRA DAM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "OBVP",
    "en": "OBULAVARIPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "OCR",
    "en": "OCHIRA",
    "se": "KERALA"
  },
  {
    "sc": "OD",
    "en": "OD",
    "se": "GUJARAT"
  },
  {
    "sc": "ODC",
    "en": "ODDANCHATRAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ORH",
    "en": "ODDARAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "OEA",
    "en": "ODELA",
    "se": "TELANGANA"
  },
  {
    "sc": "ODHA",
    "en": "ODHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ODUR",
    "en": "ODUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "OEL",
    "en": "OEL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BPTO",
    "en": "OIL DEPOT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "OKHA",
    "en": "OKHA",
    "se": "GUJARAT"
  },
  {
    "sc": "OKD",
    "en": "OKHA MADHI",
    "se": "GUJARAT"
  },
  {
    "sc": "OKA",
    "en": "OKHLA",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "OLA",
    "en": "OLAKUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "OLP",
    "en": "OLAPUR",
    "se": "BIHAR"
  },
  {
    "sc": "OMLF",
    "en": "OLD MALDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "OLR",
    "en": "OLLUR",
    "se": "KERALA"
  },
  {
    "sc": "OML",
    "en": "OMALUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "OM",
    "en": "OMKARESHWAR RD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ODM",
    "en": "ONDAGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "OGL",
    "en": "ONGOLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "OPM",
    "en": "ONNUPURAM H",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VNM",
    "en": "ONTIMITTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ODB",
    "en": "OODLABARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "OGM",
    "en": "OORGAUM",
    "se": "KARNATAKA"
  },
  {
    "sc": "OTD",
    "en": "OOTWAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ORAI",
    "en": "ORAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ORC",
    "en": "ORCHHA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ORGA",
    "en": "ORGA",
    "se": "JHARKHAND"
  },
  {
    "sc": "ORKI",
    "en": "ORKI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ORR",
    "en": "ORR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "ORW",
    "en": "ORWARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "OSN",
    "en": "OSIYAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "OSRA",
    "en": "OSRA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "OV",
    "en": "OTIVAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "OKL",
    "en": "OTTAKKAL",
    "se": "KERALA"
  },
  {
    "sc": "OTK",
    "en": "OTTAKOVIL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "OTP",
    "en": "OTTAPPALAM",
    "se": "KERALA"
  },
  {
    "sc": "PAVP",
    "en": "P AVATAPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PBD",
    "en": "P BRAHMADEVAM H",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PAI",
    "en": "PABAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PBAP",
    "en": "PABBAPURAM HALT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PQY",
    "en": "PABLI KHAS",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PCKM",
    "en": "PACHACHAKUPAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PCGN",
    "en": "PACHAGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PNDI",
    "en": "PACHANDI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PCMK",
    "en": "PACHARMALIKPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PCH",
    "en": "PACHHAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "PFR",
    "en": "PACHOR ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PC",
    "en": "PACHORA JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PPW",
    "en": "PACHPERWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PPK",
    "en": "PACHPOKHARIA",
    "se": "BIHAR"
  },
  {
    "sc": "PCK",
    "en": "PACHRUKHI",
    "se": "BIHAR"
  },
  {
    "sc": "PNWN",
    "en": "PACHWAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PDH",
    "en": "PADADHARI",
    "se": "GUJARAT"
  },
  {
    "sc": "PTM",
    "en": "PADALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PDF",
    "en": "PADAMPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "PARH",
    "en": "PADARKHEDA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PDGN",
    "en": "PADHEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PADI",
    "en": "PADI HALT",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PAQ",
    "en": "PADIYA NAGLA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PDQ",
    "en": "PADLA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PDPK",
    "en": "PADMAPUKAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PDNR",
    "en": "PADNUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "PDRA",
    "en": "PADRA",
    "se": "GUJARAT"
  },
  {
    "sc": "POU",
    "en": "PADRAUNA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PNJ",
    "en": "PADRIGANJ",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PSS",
    "en": "PADSALI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PDP",
    "en": "PADSE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PFU",
    "en": "PADUA",
    "se": "ODISHA"
  },
  {
    "sc": "PDD",
    "en": "PADUBIDRI",
    "se": "KARNATAKA"
  },
  {
    "sc": "PGU",
    "en": "PADUGUPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PWI",
    "en": "PADWANIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "PGA",
    "en": "PAGARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PGL",
    "en": "PAGDHAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PGDP",
    "en": "PAGIDIPALLI JN",
    "se": "TELANGANA"
  },
  {
    "sc": "PCX",
    "en": "PAGLA CHANDI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PHE",
    "en": "PAHALEJA HALT",
    "se": "BIHAR"
  },
  {
    "sc": "PRE",
    "en": "PAHARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PRP",
    "en": "PAHARPUR",
    "se": "BIHAR"
  },
  {
    "sc": "PRSR",
    "en": "PAHARSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PHU",
    "en": "PAHUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PMI",
    "en": "PAIMAR",
    "se": "BIHAR"
  },
  {
    "sc": "PPE",
    "en": "PAINTEPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PJA",
    "en": "PAJIAN",
    "se": "PUNJAB"
  },
  {
    "sc": "PAK",
    "en": "PAKALA JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PKRD",
    "en": "PAKARA ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PKNA",
    "en": "PAKHNA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PKX",
    "en": "PAKHRULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PQM",
    "en": "PAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PKK",
    "en": "PAKKI",
    "se": "PUNJAB"
  },
  {
    "sc": "PK",
    "en": "PAKNI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PKC",
    "en": "PAKRA",
    "se": "JHARKHAND"
  },
  {
    "sc": "PKR",
    "en": "PAKUR",
    "ec": "Howrah / Kolkata",
    "se": "JHARKHAND"
  },
  {
    "sc": "PAAL",
    "en": "PALA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PCLI",
    "en": "PALACHAURI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PLHL",
    "en": "PALAHALLI HALT",
    "se": "KARNATAKA"
  },
  {
    "sc": "PALM",
    "en": "PALAIYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PGT",
    "en": "PALAKKAD JN",
    "ec": "PALAKKAD",
    "se": "KERALA"
  },
  {
    "sc": "PLKN",
    "en": "PALAKKANUTHU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PCV",
    "en": "PALAKKODU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PKO",
    "en": "PALAKOLLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PM",
    "en": "PALAM",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "PLMX",
    "en": "PALAMPUR HMCHL",
    "ec": "PATHANKOT",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "PAE",
    "en": "PALANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PLNI",
    "en": "PALANI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PNU",
    "en": "PALANPUR JN",
    "se": "GUJARAT"
  },
  {
    "sc": "PLPM",
    "en": "PALAPPURAM",
    "se": "KERALA"
  },
  {
    "sc": "PUE",
    "en": "PALARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PSA",
    "en": "PALASA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PDI",
    "en": "PALASHARI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PLSG",
    "en": "PALASINGI",
    "se": "ODISHA"
  },
  {
    "sc": "PAL",
    "en": "PALASNER",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PSME",
    "en": "PALASTHALI",
    "se": "JHARKHAND"
  },
  {
    "sc": "PZA",
    "en": "PALAVANTHANGAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PCO",
    "en": "PALAYANKOTTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PYV",
    "en": "PALAYASIVARAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PLD",
    "en": "PALDHI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PLJ",
    "en": "PALEJ",
    "se": "GUJARAT"
  },
  {
    "sc": "PLG",
    "en": "PALGHAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PGTN",
    "en": "PALGHAT TOWN",
    "ec": "PALAKKAD",
    "se": "KERALA"
  },
  {
    "sc": "PALI",
    "en": "PALI",
    "se": "HARYANA"
  },
  {
    "sc": "PAIL",
    "en": "PALI A",
    "se": "BIHAR"
  },
  {
    "sc": "PMY",
    "en": "PALI MARWAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PLA",
    "en": "PALIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PLK",
    "en": "PALIA KALAN",
    "ec": "LAKHIMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PBV",
    "en": "PALIBA",
    "se": "ODISHA"
  },
  {
    "sc": "PLGH",
    "en": "PALIGARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PIT",
    "en": "PALITANA",
    "se": "GUJARAT"
  },
  {
    "sc": "PAC",
    "en": "PALIYARD ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "PRAE",
    "en": "PALLA ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PV",
    "en": "PALLAVARAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PLVA",
    "en": "PALLEVADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "POA",
    "en": "PALLIKONA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PUM",
    "en": "PALLIPPURAM",
    "se": "KERALA"
  },
  {
    "sc": "PYD",
    "en": "PALLIYADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PXR",
    "en": "PALPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PLSN",
    "en": "PALSANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PCP",
    "en": "PALSAP",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PLV",
    "en": "PALSI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PLAE",
    "en": "PALSIT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PSO",
    "en": "PALSORA MAKRAWA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PTF",
    "en": "PALTA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PALR",
    "en": "PALUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PLVI",
    "en": "PALUVAYI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PWL",
    "en": "PALWAL",
    "se": "HARYANA"
  },
  {
    "sc": "PMN",
    "en": "PAMAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PBM",
    "en": "PAMBAN JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PMD",
    "en": "PAMIDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PMPE",
    "en": "PAMPORE",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "PAN",
    "en": "PANAGARH",
    "ec": "ASANSOL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PNMB",
    "en": "PANAMBURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "PNGI",
    "en": "PANANGUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PAM",
    "en": "PANAPAKAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PNB",
    "en": "PANBARI",
    "se": "ASSAM"
  },
  {
    "sc": "PCN",
    "en": "PANCH PIPILA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PHRH",
    "en": "PANCH RUKHI",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "PCLM",
    "en": "PANCHALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PNCB",
    "en": "PANCHEBERIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PGC",
    "en": "PANCHGACHIA",
    "se": "BIHAR"
  },
  {
    "sc": "PNGM",
    "en": "PANCHGRAM",
    "se": "ASSAM"
  },
  {
    "sc": "PHC",
    "en": "PANCHOT",
    "se": "GUJARAT"
  },
  {
    "sc": "PCR",
    "en": "PANCHRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PCT",
    "en": "PANCHTALAVDA RD",
    "se": "GUJARAT"
  },
  {
    "sc": "PAW",
    "en": "PANDABESWAR",
    "ec": "ASANSOL & ANDAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PDV",
    "en": "PANDARAVADAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PDW",
    "en": "PANDAUL",
    "se": "BIHAR"
  },
  {
    "sc": "PANP",
    "en": "PANDAVAPURA",
    "se": "KARNATAKA"
  },
  {
    "sc": "PVR",
    "en": "PANDHARPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PAR",
    "en": "PANDHURNA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PNY",
    "en": "PANDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PDM",
    "en": "PANDIKANMOI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PNDP",
    "en": "PANDILLAPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "PYM",
    "en": "PANDIYAPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PMO",
    "en": "PANDOLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PNDR",
    "en": "PANDORI",
    "se": "GUJARAT"
  },
  {
    "sc": "PRSL",
    "en": "PANDRASALI",
    "se": "JHARKHAND"
  },
  {
    "sc": "PME",
    "en": "PANDU MAWAS",
    "se": "GUJARAT"
  },
  {
    "sc": "PPDE",
    "en": "PANDU PINDARA",
    "se": "HARYANA"
  },
  {
    "sc": "PGP",
    "en": "PANDURANGAPURAM",
    "se": "TELANGANA"
  },
  {
    "sc": "PLM",
    "en": "PANELI MOTI",
    "se": "GUJARAT"
  },
  {
    "sc": "PNV",
    "en": "PANEVADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PNF",
    "en": "PANGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PJR",
    "en": "PANGRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PNHI",
    "en": "PANHAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PNN",
    "en": "PANI MINES",
    "se": "GUJARAT"
  },
  {
    "sc": "PNYA",
    "en": "PANIAHWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PJB",
    "en": "PANIAJOB",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "PNRA",
    "en": "PANIARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PNHR",
    "en": "PANIHAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PHI",
    "en": "PANIKHAITI",
    "se": "ASSAM"
  },
  {
    "sc": "PNP",
    "en": "PANIPAT JN",
    "se": "HARYANA"
  },
  {
    "sc": "PASG",
    "en": "PANISAGAR",
    "se": "TRIPURA"
  },
  {
    "sc": "PNT",
    "en": "PANITOLA",
    "se": "ASSAM"
  },
  {
    "sc": "PJK",
    "en": "PANJ KOSI",
    "se": "PUNJAB"
  },
  {
    "sc": "PJGM",
    "en": "PANJGAM",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "PJN",
    "en": "PANJHAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PJP",
    "en": "PANJIPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PNMA",
    "en": "PANJUM O A",
    "ec": "MADGAON"
  },
  {
    "sc": "PJLE",
    "en": "PANJWARA ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "PNKD",
    "en": "PANKI DHAM",
    "ec": "KANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PH",
    "en": "PANOH",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "PAO",
    "en": "PANOLI",
    "se": "GUJARAT"
  },
  {
    "sc": "PNPL",
    "en": "PANPALI",
    "se": "ODISHA"
  },
  {
    "sc": "PPO",
    "en": "PANPOSH",
    "se": "ODISHA"
  },
  {
    "sc": "PRT",
    "en": "PANRUTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PN",
    "en": "PANSAR",
    "se": "GUJARAT"
  },
  {
    "sc": "PKU",
    "en": "PANSKURA",
    "ec": "KHARAGPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PBW",
    "en": "PANTNAGAR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "PNM",
    "en": "PANYAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PML",
    "en": "PAPANASAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PPY",
    "en": "PAPATAPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "PKL",
    "en": "PAPINAYAKNAHALI",
    "se": "KARNATAKA"
  },
  {
    "sc": "PPNS",
    "en": "PAPPINISSERI",
    "se": "KERALA"
  },
  {
    "sc": "PPEA",
    "en": "PAPRERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PDG",
    "en": "PARADGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PRDP",
    "en": "PARADIP",
    "se": "ODISHA"
  },
  {
    "sc": "PRDL",
    "en": "PARADOL",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "PSK",
    "en": "PARADSINGA HALT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PRY",
    "en": "PARAIYA",
    "se": "BIHAR"
  },
  {
    "sc": "PAJ",
    "en": "PARAJ",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PLH",
    "en": "PARALAKHEMUNDI",
    "se": "ODISHA"
  },
  {
    "sc": "PMK",
    "en": "PARAMAKKUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PO",
    "en": "PARANGIPETTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PMH",
    "en": "PARAO MAHNA",
    "se": "PUNJAB"
  },
  {
    "sc": "PS",
    "en": "PARAS",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PASA",
    "en": "PARASHSHALA",
    "se": "KERALA"
  },
  {
    "sc": "PUX",
    "en": "PARASIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PNME",
    "en": "PARASNATH",
    "se": "JHARKHAND",
    "tg": "SHIKHARJI"
  },
  {
    "sc": "PRN",
    "en": "PARAUNA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PVU",
    "en": "PARAVUR",
    "se": "KERALA"
  },
  {
    "sc": "PRB",
    "en": "PARBATI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PBB",
    "en": "PARBATONIA",
    "se": "JHARKHAND"
  },
  {
    "sc": "PBN",
    "en": "PARBHANI JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PHQ",
    "en": "PARDHANDE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PAD",
    "en": "PARDI",
    "se": "GUJARAT"
  },
  {
    "sc": "PRWD",
    "en": "PAREWADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PRGT",
    "en": "PARGOTHAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PQU",
    "en": "PARHANA MAU",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PIH",
    "en": "PARHIHARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PQN",
    "en": "PARIAWAN K.K.RD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PIC",
    "en": "PARICHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PRKA",
    "en": "PARIKHA",
    "se": "GUJARAT"
  },
  {
    "sc": "PRKL",
    "en": "PARIKKAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PSL",
    "en": "PARISAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PQS",
    "en": "PARK CIRCUS",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PRKH",
    "en": "PARKANHATTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "PRK",
    "en": "PARKHAM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PLL",
    "en": "PARLI",
    "se": "KERALA"
  },
  {
    "sc": "PRLI",
    "en": "PARLI VAIJNATH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PRU",
    "en": "PARLU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PMS",
    "en": "PARMALKASA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "PMU",
    "en": "PARMANANDPUR",
    "se": "BIHAR"
  },
  {
    "sc": "PMQ",
    "en": "PARNA NAND",
    "se": "PUNJAB"
  },
  {
    "sc": "PRAR",
    "en": "PAROR",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "PGI",
    "en": "PARPANANGADI",
    "se": "KERALA"
  },
  {
    "sc": "PRZ",
    "en": "PARSA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PRBZ",
    "en": "PARSA BAZAR",
    "se": "BIHAR"
  },
  {
    "sc": "PKRA",
    "en": "PARSA KHERA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PRSN",
    "en": "PARSA NAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "PSB",
    "en": "PARSABAD",
    "se": "JHARKHAND"
  },
  {
    "sc": "PSZ",
    "en": "PARSAUNI",
    "se": "BIHAR"
  },
  {
    "sc": "PMM",
    "en": "PARSEHRA MAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PSN",
    "en": "PARSENDI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PRF",
    "en": "PARSIPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PSV",
    "en": "PARSNEU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PSD",
    "en": "PARSODA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PSLI",
    "en": "PARSOLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PPB",
    "en": "PARTABPURA",
    "se": "PUNJAB"
  },
  {
    "sc": "PRTP",
    "en": "PARTAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PTU",
    "en": "PARTUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PVP",
    "en": "PARVATIPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PVPT",
    "en": "PARVATIPURAM TN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PBC",
    "en": "PARVATSAR CITY",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PVZ",
    "en": "PARVEZPUR",
    "se": "HARYANA"
  },
  {
    "sc": "PSLP",
    "en": "PASALAPUDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PSDA",
    "en": "PASIVEDALA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PSR",
    "en": "PASRAHA",
    "se": "BIHAR"
  },
  {
    "sc": "PVL",
    "en": "PASUPATIKOVIL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PAS",
    "en": "PASUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PATA",
    "en": "PATA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PLU",
    "en": "PATAKOTTACHERU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PTP",
    "en": "PATAL PANI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PTN",
    "en": "PATAN",
    "se": "GUJARAT"
  },
  {
    "sc": "PTS",
    "en": "PATANSAONGI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PSX",
    "en": "PATANSAONGI TWN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PHM",
    "en": "PATAPATNAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PTRE",
    "en": "PATARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PAA",
    "en": "PATAS",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PSJ",
    "en": "PATASAHI",
    "se": "ODISHA"
  },
  {
    "sc": "PTRD",
    "en": "PATAUDI ROAD",
    "se": "HARYANA"
  },
  {
    "sc": "PU",
    "en": "PATCHUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PTR",
    "en": "PATDI",
    "se": "GUJARAT"
  },
  {
    "sc": "PTNR",
    "en": "PATELNAGAR",
    "se": "DELHI"
  },
  {
    "sc": "PEE",
    "en": "PATERHI",
    "se": "BIHAR"
  },
  {
    "sc": "PHX",
    "en": "PATHAKPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PTK",
    "en": "PATHANKOT",
    "ec": "PATHANKOT",
    "se": "PUNJAB"
  },
  {
    "sc": "PTKC",
    "en": "PATHANKOT CANTT",
    "ec": "PATHANKOT",
    "se": "PUNJAB"
  },
  {
    "sc": "PEH",
    "en": "PATHARDIH JN",
    "se": "JHARKHAND"
  },
  {
    "sc": "PHA",
    "en": "PATHARIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PTKD",
    "en": "PATHARKANDI",
    "se": "ASSAM"
  },
  {
    "sc": "PKB",
    "en": "PATHARKHOLA S",
    "se": "ASSAM"
  },
  {
    "sc": "PTLI",
    "en": "PATHAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PARD",
    "en": "PATHRAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PTRL",
    "en": "PATHRALA",
    "se": "PUNJAB"
  },
  {
    "sc": "PRI",
    "en": "PATHRI",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "PTRT",
    "en": "PATHROT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PBL",
    "en": "PATHSALA",
    "se": "ASSAM"
  },
  {
    "sc": "PTA",
    "en": "PATIALA",
    "ec": "AMBALA",
    "se": "PUNJAB"
  },
  {
    "sc": "PTE",
    "en": "PATIALA CANT",
    "se": "PUNJAB"
  },
  {
    "sc": "PTI",
    "en": "PATIALI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PTLD",
    "en": "PATILADAHA",
    "se": "ASSAM"
  },
  {
    "sc": "PTYR",
    "en": "PATIYARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PT",
    "en": "PATLI",
    "se": "HARYANA"
  },
  {
    "sc": "PPTA",
    "en": "PATLIPUTRA",
    "se": "BIHAR"
  },
  {
    "sc": "PNC",
    "en": "PATNA SAHEB",
    "se": "BIHAR"
  },
  {
    "sc": "PTHD",
    "en": "PATOHAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PTH",
    "en": "PATRANGA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PSF",
    "en": "PATRASAF",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PTRU",
    "en": "PATRATU",
    "se": "JHARKHAND"
  },
  {
    "sc": "PTZ",
    "en": "PATSUL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PAB",
    "en": "PATTABIRAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PTB",
    "en": "PATTAMBI",
    "se": "KERALA"
  },
  {
    "sc": "PTTN",
    "en": "PATTAN",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "PAX",
    "en": "PATTI",
    "se": "PUNJAB"
  },
  {
    "sc": "PKQ",
    "en": "PATTIKKAD",
    "se": "KERALA"
  },
  {
    "sc": "PKT",
    "en": "PATTUKOTTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PTAE",
    "en": "PATULI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PUW",
    "en": "PATUWAS MEHRANA",
    "se": "HARYANA"
  },
  {
    "sc": "PTWA",
    "en": "PATWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PUF",
    "en": "PAUTA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PVG",
    "en": "PAVAGARH",
    "se": "GUJARAT"
  },
  {
    "sc": "PAVI",
    "en": "PAVI",
    "se": "GUJARAT"
  },
  {
    "sc": "PVN",
    "en": "PAVUNUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PCM",
    "en": "PAVURCHATRAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "POE",
    "en": "PAWAPURI ROAD H",
    "se": "BIHAR"
  },
  {
    "sc": "PDR",
    "en": "PAYAGPUR",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PAZ",
    "en": "PAYANGADI",
    "se": "KERALA"
  },
  {
    "sc": "PYI",
    "en": "PAYLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PDX",
    "en": "PAYRADANGA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PAY",
    "en": "PAYYANUR",
    "se": "KERALA"
  },
  {
    "sc": "PYOL",
    "en": "PAYYOLI",
    "se": "KERALA"
  },
  {
    "sc": "PBJM",
    "en": "PBNWA JASMHNDAR",
    "se": "HARYANA"
  },
  {
    "sc": "PDGP",
    "en": "PDGM GANESHPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "PDKN",
    "en": "PEDAKAKANI HALT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PAV",
    "en": "PEDANA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PDKM",
    "en": "PEDANYKNPALAYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PYA",
    "en": "PEDAPARIYA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PDNA",
    "en": "PEDDADINNE",
    "se": "TELANGANA"
  },
  {
    "sc": "PKPU",
    "en": "PEDDAKURAPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PPZ",
    "en": "PEDDAMPET",
    "se": "TELANGANA"
  },
  {
    "sc": "PDPL",
    "en": "PEDDAPALLI JN",
    "se": "TELANGANA"
  },
  {
    "sc": "PDSN",
    "en": "PEDDASANA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PVD",
    "en": "PEDDAVADLAPUDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PHWR",
    "en": "PEHOWA ROAD",
    "se": "HARYANA"
  },
  {
    "sc": "PBP",
    "en": "PEMBARTI",
    "se": "TELANGANA"
  },
  {
    "sc": "PEN",
    "en": "PEN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PCG",
    "en": "PENCH"
  },
  {
    "sc": "PEC",
    "en": "PENCHARTHAL",
    "se": "TRIPURA"
  },
  {
    "sc": "PDL",
    "en": "PENDEKALLU JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PDMI",
    "en": "PENDLIMARRI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PND",
    "en": "PENDRA ROAD",
    "ec": "ANUPPUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "PDT",
    "en": "PENDURTI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PGG",
    "en": "PENGANGA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PAGM",
    "en": "PENNADA AGRHRM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PNDM",
    "en": "PENNADAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PKD",
    "en": "PENUKONDA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PUMU",
    "en": "PENUMARRU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "POKL",
    "en": "PEOKOL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PJ",
    "en": "PEPPEGANJ",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PEM",
    "en": "PERALAM JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PER",
    "en": "PERAMBUR",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PCW",
    "en": "PERAMBUR CRG WK",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PEW",
    "en": "PERAMBUR LCO WK",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PEI",
    "en": "PERANI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PEU",
    "en": "PERASHSHANNUR",
    "se": "KERALA"
  },
  {
    "sc": "PVI",
    "en": "PERAVURANI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PRCA",
    "en": "PERECHERLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PG",
    "en": "PERGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PRND",
    "en": "PERINAD",
    "se": "KERALA"
  },
  {
    "sc": "PERN",
    "en": "PERNEM",
    "se": "GOA"
  },
  {
    "sc": "PGN",
    "en": "PERUGAMANI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PY",
    "en": "PERUNDURAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PRGD",
    "en": "PERUNGUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PRGL",
    "en": "PERUNGULATTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PGZ",
    "en": "PERUNGUZHI",
    "se": "KERALA"
  },
  {
    "sc": "PTD",
    "en": "PETLAD JN",
    "se": "GUJARAT"
  },
  {
    "sc": "PTPL",
    "en": "PETRAPOL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PEA",
    "en": "PETTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PLI",
    "en": "PETTAIVAYATALAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PYX",
    "en": "PEYANAPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PGW",
    "en": "PHAGWARA JN",
    "ec": "PHAGWARA",
    "se": "PUNJAB"
  },
  {
    "sc": "PKGM",
    "en": "PHAKHOAGRAM",
    "se": "ASSAM"
  },
  {
    "sc": "PLCJ",
    "en": "PHALODI JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PUD",
    "en": "PHANDA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PFM",
    "en": "PHAPHAMAU JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PHD",
    "en": "PHAPHUND",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PD",
    "en": "PHARADAHAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PHY",
    "en": "PHARIHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PEP",
    "en": "PHEPHNA JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PES",
    "en": "PHESAR",
    "se": "BIHAR"
  },
  {
    "sc": "PDJ",
    "en": "PHIDING",
    "se": "ASSAM"
  },
  {
    "sc": "PHR",
    "en": "PHILLAUR JN",
    "se": "PUNJAB"
  },
  {
    "sc": "PPM",
    "en": "PHIRANGIPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PHOP",
    "en": "PHOOP",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "FLD",
    "en": "PHULAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PUY",
    "en": "PHULAGURI",
    "se": "ASSAM"
  },
  {
    "sc": "FL",
    "en": "PHULERA JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "FLR",
    "en": "PHULESWAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "FLU",
    "en": "PHULIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PLP",
    "en": "PHULPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PWS",
    "en": "PHULWARI SHARIF",
    "se": "BIHAR"
  },
  {
    "sc": "PLJE",
    "en": "PHULWARTANR",
    "se": "JHARKHAND"
  },
  {
    "sc": "FSG",
    "en": "PHURSUNGI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PUS",
    "en": "PHUSRO",
    "se": "JHARKHAND"
  },
  {
    "sc": "PLF",
    "en": "PIALI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PBA",
    "en": "PIARDOBA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "BXS",
    "en": "PICHCHANDARKOVL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PCQ",
    "en": "PICHKURIRDHAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PGRL",
    "en": "PIDUGURALLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PGRN",
    "en": "PIDUGURALLA NEW",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PIJ",
    "en": "PIJ",
    "se": "GUJARAT"
  },
  {
    "sc": "PLMD",
    "en": "PILAMEDU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PIL",
    "en": "PILER",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PGK",
    "en": "PILI BANGAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PBE",
    "en": "PILIBHIT JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PDZ",
    "en": "PILIODA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PKY",
    "en": "PILKHANI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PKW",
    "en": "PILKHUA",
    "ec": "HAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PIO",
    "en": "PILOL",
    "se": "GUJARAT"
  },
  {
    "sc": "PKDE",
    "en": "PILU KHERA",
    "se": "HARYANA"
  },
  {
    "sc": "PLDR",
    "en": "PILUDRA",
    "se": "GUJARAT"
  },
  {
    "sc": "PWR",
    "en": "PILWAL ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "PMGN",
    "en": "PIMPALGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PMKT",
    "en": "PIMPALKHUTI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PKE",
    "en": "PIMPAR KHED",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PMP",
    "en": "PIMPRI",
    "ec": "PUNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PRGR",
    "en": "PINARGARIA",
    "se": "JHARKHAND"
  },
  {
    "sc": "PDS",
    "en": "PINDARSI",
    "se": "HARYANA"
  },
  {
    "sc": "PQL",
    "en": "PINDIAL",
    "se": "TELANGANA"
  },
  {
    "sc": "PQH",
    "en": "PINDKEPAR P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PDRD",
    "en": "PINDRA ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PDE",
    "en": "PINDRAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PDWA",
    "en": "PINDWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PLW",
    "en": "PINGLESHWAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PIZ",
    "en": "PINGLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PNGR",
    "en": "PINGORA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "POL",
    "en": "PINJRAPOL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "POR",
    "en": "PIPALDA ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PLS",
    "en": "PIPALSANA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PCY",
    "en": "PIPAR CITY",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PPR",
    "en": "PIPAR ROAD JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PPRH",
    "en": "PIPARAHAN HALT",
    "se": "BIHAR"
  },
  {
    "sc": "PED",
    "en": "PIPARDAHI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PID",
    "en": "PIPARDI",
    "se": "GUJARAT"
  },
  {
    "sc": "PPI",
    "en": "PIPARIYA",
    "ec": "PIPARIYA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PPU",
    "en": "PIPARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "POF",
    "en": "PIPARSAND",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PPS",
    "en": "PIPILIYA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "PQA",
    "en": "PIPLA P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PPLA",
    "en": "PIPLAI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PPF",
    "en": "PIPLAJ",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PLE",
    "en": "PIPLEE",
    "se": "GUJARAT"
  },
  {
    "sc": "PPLI",
    "en": "PIPLI",
    "se": "GUJARAT"
  },
  {
    "sc": "PIP",
    "en": "PIPLIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PPD",
    "en": "PIPLOD JN",
    "se": "GUJARAT"
  },
  {
    "sc": "PPG",
    "en": "PIPLODA BAGLA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PPA",
    "en": "PIPRA",
    "se": "BIHAR"
  },
  {
    "sc": "PPC",
    "en": "PIPRAICH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PIA",
    "en": "PIPRAIGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PFL",
    "en": "PIPRALA",
    "se": "GUJARAT"
  },
  {
    "sc": "PPH",
    "en": "PIPRI DIH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PUO",
    "en": "PIR UMROD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PVRD",
    "en": "PIRAVAM ROAD",
    "se": "KERALA"
  },
  {
    "sc": "PRDH",
    "en": "PIRDULESHA HALT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PJH",
    "en": "PIRJHALAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PIRO",
    "en": "PIRO",
    "se": "BIHAR"
  },
  {
    "sc": "PPT",
    "en": "PIRPAINTI",
    "se": "BIHAR"
  },
  {
    "sc": "PRTL",
    "en": "PIRTALA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PLT",
    "en": "PIRTHALA LLAUDA",
    "se": "HARYANA"
  },
  {
    "sc": "PHV",
    "en": "PIRTHIGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PRM",
    "en": "PIRUMADARA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "PW",
    "en": "PIRWA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PIS",
    "en": "PISKA",
    "ec": "HATIA/RANCHI",
    "se": "JHARKHAND"
  },
  {
    "sc": "PMR",
    "en": "PITAMBARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PAP",
    "en": "PITHAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PLY",
    "en": "PLASSEY",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PBKS",
    "en": "PMBAKVL SHANDY",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PCZ",
    "en": "POCHARAM",
    "se": "TELANGANA"
  },
  {
    "sc": "PTJ",
    "en": "PODANUR JN",
    "ec": "COIMBATORE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "POHE",
    "en": "POHE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "POK",
    "en": "POKARAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PKNS",
    "en": "POKHARNI NRSNHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PHN",
    "en": "POKHRAYAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PKF",
    "en": "POKLA",
    "se": "JHARKHAND"
  },
  {
    "sc": "PEL",
    "en": "POLIREDDIPALEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "POY",
    "en": "POLLACHI JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PRL",
    "en": "POLUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PDGL",
    "en": "PONDUGULA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PDU",
    "en": "PONDURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "GOC",
    "en": "PONMLAI GLD RCK",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PON",
    "en": "PONNERI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "POI",
    "en": "PONPADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PDO",
    "en": "POODOOR",
    "se": "TELANGANA"
  },
  {
    "sc": "PPJ",
    "en": "POPHLAJ",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PBZ",
    "en": "PORABAZAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PBR",
    "en": "PORBANDAR",
    "se": "GUJARAT"
  },
  {
    "sc": "POD",
    "en": "PORDA BHATERA",
    "se": "GUJARAT"
  },
  {
    "sc": "PRNR",
    "en": "PORJANPUR",
    "se": "ODISHA"
  },
  {
    "sc": "PST",
    "en": "POSOTIA",
    "se": "JHARKHAND"
  },
  {
    "sc": "PFT",
    "en": "POTHAHI",
    "se": "BIHAR"
  },
  {
    "sc": "POT",
    "en": "POTHIA",
    "se": "BIHAR"
  },
  {
    "sc": "PTKP",
    "en": "POTKAPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "POO",
    "en": "POTLAPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "POZ",
    "en": "POTUL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PRKD",
    "en": "POWERKHEDA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PRH",
    "en": "POWERPET",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PKZ",
    "en": "PPLI PKHI KALAN",
    "se": "PUNJAB"
  },
  {
    "sc": "PCC",
    "en": "PRACHI ROAD JN",
    "se": "GUJARAT"
  },
  {
    "sc": "PKA",
    "en": "PRADHANKHUNTA",
    "se": "JHARKHAND"
  },
  {
    "sc": "PQD",
    "en": "PRANPUR ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "PRJ",
    "en": "PRANTIJ",
    "se": "GUJARAT"
  },
  {
    "sc": "PNE",
    "en": "PRANTIK",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PRSP",
    "en": "PRASADPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PSPY",
    "en": "PRASANNAYANAPAL",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PRBG",
    "en": "PRATAP BAGH P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PPV",
    "en": "PRATAPGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "PRTN",
    "en": "PRATAPNAGAR",
    "ec": "VADODARA",
    "se": "GUJARAT"
  },
  {
    "sc": "PTPU",
    "en": "PRATTIAPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PRG",
    "en": "PRAYAG",
    "ec": "PRAYAGRAJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PYQ",
    "en": "PRAYAGPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "PCOI",
    "en": "PRAYAGRAJCHEOKI",
    "ec": "PRAYAGRAJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PRRB",
    "en": "PRAYAGRAJRAMBAG",
    "ec": "PRAYAGRAJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PYGS",
    "en": "PRAYAGRAJSANGAM",
    "ec": "PRAYAGRAJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PYHT",
    "en": "PRAYAHAT HALT",
    "se": "JHARKHAND"
  },
  {
    "sc": "PMPR",
    "en": "PREMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PRNG",
    "en": "PRITAM NAGAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PRUR",
    "en": "PRITHWIRAJPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PRDT",
    "en": "PRODDATUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PKM",
    "en": "PRYANKNPALAYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PUDI",
    "en": "PUDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PUC",
    "en": "PUDUCHATIRAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PCTM",
    "en": "PUDUCHATRAM H",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PDY",
    "en": "PUDUCHERRY",
    "ec": "PONDICHERRY/PUDUCHERRY",
    "se": "PUDUCHERRY"
  },
  {
    "sc": "PUK",
    "en": "PUDUKAD",
    "se": "KERALA"
  },
  {
    "sc": "PDKT",
    "en": "PUDUKKOTTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PDGM",
    "en": "PUDUNAGARAM",
    "se": "KERALA"
  },
  {
    "sc": "PGR",
    "en": "PUGALUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PRV",
    "en": "PUKKIRIVARI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PLQ",
    "en": "PULAKURTHI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PLO",
    "en": "PULGAON JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PCL",
    "en": "PULICHERLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PUA",
    "en": "PULLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PMB",
    "en": "PULLAMBADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PMT",
    "en": "PULLAMPET",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PUU",
    "en": "PUNALUR",
    "se": "KERALA"
  },
  {
    "sc": "PHK",
    "en": "PUNARAKH",
    "se": "BIHAR"
  },
  {
    "sc": "PNW",
    "en": "PUNDHAG",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PUN",
    "en": "PUNDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PQZ",
    "en": "PUNDIBARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PDA",
    "en": "PUNDOOAH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PUG",
    "en": "PUNGGUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PQT",
    "en": "PUNIYAVANT",
    "se": "GUJARAT"
  },
  {
    "sc": "PNQ",
    "en": "PUNKUNNAM",
    "se": "KERALA"
  },
  {
    "sc": "PPN",
    "en": "PUNPUN",
    "se": "BIHAR"
  },
  {
    "sc": "PNSA",
    "en": "PUNSIA",
    "se": "BIHAR"
  },
  {
    "sc": "PB",
    "en": "PUNTAMBA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "POM",
    "en": "PUNTHOTTAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PBS",
    "en": "PURAB SARAI",
    "ec": "JAMALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "PNI",
    "en": "PURAINI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PDPR",
    "en": "PURANDARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PUQ",
    "en": "PURANIGUDAM",
    "se": "ASSAM"
  },
  {
    "sc": "PP",
    "en": "PURANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PSAE",
    "en": "PURBASTHALI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PAU",
    "en": "PURNA JN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PRNA",
    "en": "PURNEA JN",
    "se": "BIHAR"
  },
  {
    "sc": "PRNC",
    "en": "PURNIA COURT",
    "se": "BIHAR"
  },
  {
    "sc": "PRKE",
    "en": "PURUA KHERA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "PRR",
    "en": "PURULIA JN",
    "ec": "PURULIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "PUKK",
    "en": "PURUNAKATAK",
    "se": "ODISHA"
  },
  {
    "sc": "PNPI",
    "en": "PURUNAPANI",
    "se": "ODISHA"
  },
  {
    "sc": "PSE",
    "en": "PUSAULI",
    "se": "BIHAR"
  },
  {
    "sc": "PUHT",
    "en": "PUSHKAR TERMINU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PPTR",
    "en": "PUSHPATTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "PUSA",
    "en": "PUSLA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "PTT",
    "en": "PUTALAPATTU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PRTR",
    "en": "PUTARRA P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "PCU",
    "en": "PUTLACHERUVU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "PUT",
    "en": "PUTTUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "QDN",
    "en": "QADIAN",
    "se": "PUNJAB"
  },
  {
    "sc": "KPKI",
    "en": "QASIMPUR KHERI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "QG",
    "en": "QAZIGUND",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "QRS",
    "en": "QUARRY SDG",
    "se": "ODISHA"
  },
  {
    "sc": "QTP",
    "en": "QUATABPUR",
    "se": "HARYANA"
  },
  {
    "sc": "QBW",
    "en": "QUBARWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "QLD",
    "en": "QUILANDI",
    "se": "KERALA"
  },
  {
    "sc": "RCG",
    "en": "RACHAGUNNERI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RDV",
    "en": "RADHA BALAMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RDF",
    "en": "RADHAGAON",
    "se": "JHARKHAND"
  },
  {
    "sc": "RQP",
    "en": "RADHAKISHOREPUR",
    "se": "ODISHA"
  },
  {
    "sc": "RAKD",
    "en": "RADHAKUND",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RDU",
    "en": "RADHAMOHANPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RDHP",
    "en": "RADHANPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "RDP",
    "en": "RADHIKAPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RBL",
    "en": "RAE BARELI JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RF",
    "en": "RAFALESHWAR",
    "se": "GUJARAT"
  },
  {
    "sc": "RFJ",
    "en": "RAFIGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "RFR",
    "en": "RAFINAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RGU",
    "en": "RAGAUL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RGPM",
    "en": "RAGHAVAPURAM",
    "se": "TELANGANA"
  },
  {
    "sc": "RGG",
    "en": "RAGHOGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RGV",
    "en": "RAGHOPUR",
    "se": "BIHAR"
  },
  {
    "sc": "RGLI",
    "en": "RAGHOULI HALT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RBN",
    "en": "RAGHUBANS NAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "RGX",
    "en": "RAGHUNATHBARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RGP",
    "en": "RAGHUNATHPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "RPR",
    "en": "RAGHUNATHPUR",
    "se": "BIHAR"
  },
  {
    "sc": "RCTC",
    "en": "RAGHUNATHPUR",
    "se": "ODISHA"
  },
  {
    "sc": "RRS",
    "en": "RAGHURAJ SINGH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RAHA",
    "en": "RAHA",
    "se": "ASSAM"
  },
  {
    "sc": "RHMA",
    "en": "RAHAMA",
    "se": "ODISHA"
  },
  {
    "sc": "RTWS",
    "en": "RAHATWAS",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RNBT",
    "en": "RAHENBATA",
    "se": "ODISHA"
  },
  {
    "sc": "RBD",
    "en": "RAHIMABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RMP",
    "en": "RAHIMATPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RMNR",
    "en": "RAHMATNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RHU",
    "en": "RAHON",
    "se": "PUNJAB"
  },
  {
    "sc": "RRE",
    "en": "RAHUI ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "RRI",
    "en": "RAHURI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RSNR",
    "en": "RAI SINGH NAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RAI",
    "en": "RAIBHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RBJ",
    "en": "RAIBOJHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RC",
    "en": "RAICHUR JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "RGQ",
    "en": "RAIGADH ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "RGJ",
    "en": "RAIGANJ",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RIG",
    "en": "RAIGARH",
    "ec": "RAIGARH",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "RAG",
    "en": "RAIGIR",
    "se": "TELANGANA"
  },
  {
    "sc": "RKB",
    "en": "RAIKA BAGH P JN",
    "ec": "JODHPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RLR",
    "en": "RAILA ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "MTPR",
    "en": "RAIMEHATPUR",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "RNGR",
    "en": "RAINAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RCT",
    "en": "RAIPUR CITY",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "RAIR",
    "en": "RAIRAKHOL",
    "se": "ODISHA"
  },
  {
    "sc": "RRP",
    "en": "RAIRANGPUR",
    "se": "ODISHA"
  },
  {
    "sc": "RSJ",
    "en": "RAISERJAGIR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RSI",
    "en": "RAISI",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "RWL",
    "en": "RAIWALA",
    "ec": "HARIDWAR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "RJGR",
    "en": "RAJ ATHGARH",
    "se": "ODISHA"
  },
  {
    "sc": "RJN",
    "en": "RAJ NANDGAON",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "RJD",
    "en": "RAJ PARDI",
    "se": "GUJARAT"
  },
  {
    "sc": "RVK",
    "en": "RAJA BHAT KHAWA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RJK",
    "en": "RAJA KA SAHASPR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RKM",
    "en": "RAJA KI MANDI",
    "ec": "AGRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RTB",
    "en": "RAJA TALAB",
    "ec": "BANARAS",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RJB",
    "en": "RAJABERA",
    "se": "JHARKHAND"
  },
  {
    "sc": "RAGM",
    "en": "RAJAGAMBIRAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "RJR",
    "en": "RAJALDESAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RJA",
    "en": "RAJANAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "RNN",
    "en": "RAJANKUNTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "RJPM",
    "en": "RAJAPALAYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "RPV",
    "en": "RAJAPATTI",
    "se": "BIHAR"
  },
  {
    "sc": "RJAP",
    "en": "RAJAPUR",
    "se": "TELANGANA"
  },
  {
    "sc": "RAJP",
    "en": "RAJAPUR ROAD",
    "ec": "RATNAGIRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RJI",
    "en": "RAJAWARI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RBH",
    "en": "RAJBANDH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RCD",
    "en": "RAJCHANDRAPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RJO",
    "en": "RAJENDRA PUL",
    "se": "BIHAR"
  },
  {
    "sc": "RJQ",
    "en": "RAJENDRANAGAR",
    "ec": "INDORE",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RJW",
    "en": "RAJEVADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "GP",
    "en": "RAJGANGPUR",
    "se": "ODISHA"
  },
  {
    "sc": "RHG",
    "en": "RAJGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RGT",
    "en": "RAJGHAT",
    "se": "ODISHA"
  },
  {
    "sc": "RG",
    "en": "RAJGHAT NARORA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RGD",
    "en": "RAJGIR",
    "se": "BIHAR"
  },
  {
    "sc": "RJG",
    "en": "RAJGRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RHR",
    "en": "RAJHURA",
    "se": "JHARKHAND"
  },
  {
    "sc": "RIM",
    "en": "RAJIM",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "RJS",
    "en": "RAJIYASAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RKSN",
    "en": "RAJKHARSAWAN JN",
    "ec": "RAJKHARSAWAN",
    "se": "JHARKHAND"
  },
  {
    "sc": "RKZ",
    "en": "RAJKIAWAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RJT",
    "en": "RAJKOT JN",
    "se": "GUJARAT"
  },
  {
    "sc": "RJLA",
    "en": "RAJLA HALT",
    "se": "BIHAR"
  },
  {
    "sc": "RUG",
    "en": "RAJLU GARHI",
    "se": "HARYANA"
  },
  {
    "sc": "RJL",
    "en": "RAJMAHAL",
    "ec": "SAHIBGANJ",
    "se": "JHARKHAND"
  },
  {
    "sc": "RJMP",
    "en": "RAJMALPUR ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RM",
    "en": "RAJMANE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RJAK",
    "en": "RAJNAGAR K HALT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RJMA",
    "en": "RAJOMAJRA",
    "se": "PUNJAB"
  },
  {
    "sc": "ROS",
    "en": "RAJOSI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RAJ",
    "en": "RAJPIPLA",
    "se": "GUJARAT"
  },
  {
    "sc": "RPJ",
    "en": "RAJPURA JN",
    "se": "PUNJAB"
  },
  {
    "sc": "RJC",
    "en": "RAJSITAPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "RSKA",
    "en": "RAJSUNAKHALA",
    "se": "ODISHA"
  },
  {
    "sc": "RJU",
    "en": "RAJULA CITY",
    "se": "GUJARAT"
  },
  {
    "sc": "RLA",
    "en": "RAJULA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "ROL",
    "en": "RAJULI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RAJR",
    "en": "RAJUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RHE",
    "en": "RAKHA MINES",
    "ec": "TATANAGAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "RHI",
    "en": "RAKHI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RKJE",
    "en": "RAKHITPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "RKH",
    "en": "RAKHIYAL",
    "se": "GUJARAT"
  },
  {
    "sc": "RBQ",
    "en": "RAM BISHANPUR",
    "se": "BIHAR"
  },
  {
    "sc": "RMC",
    "en": "RAM CHAURA ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RD",
    "en": "RAM DAYALU NAGR",
    "se": "BIHAR"
  },
  {
    "sc": "RMJK",
    "en": "RAM NAGAR J K",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "RCP",
    "en": "RAMACHANDRAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RBCS",
    "en": "RAMACHANDRAPURM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RDM",
    "en": "RAMAGUNDAM",
    "se": "TELANGANA"
  },
  {
    "sc": "RMO",
    "en": "RAMAKONA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RAMR",
    "en": "RAMALPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RMN",
    "en": "RAMAN",
    "se": "PUNJAB"
  },
  {
    "sc": "RMGM",
    "en": "RAMANAGARAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "RMD",
    "en": "RAMANATHAPURAM",
    "ec": "RAMESWARAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "RMNP",
    "en": "RAMANNAPETA",
    "se": "TELANGANA"
  },
  {
    "sc": "RLX",
    "en": "RAMANUJAMPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RAM",
    "en": "RAMAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RRJ",
    "en": "RAMARAJU PALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RMV",
    "en": "RAMAVARAPPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RBA",
    "en": "RAMBHA",
    "se": "ODISHA"
  },
  {
    "sc": "RBZ",
    "en": "RAMBHADDARPUR",
    "se": "BIHAR"
  },
  {
    "sc": "RCRA",
    "en": "RAMCHAURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RDS",
    "en": "RAMDAS",
    "se": "PUNJAB"
  },
  {
    "sc": "RDRA",
    "en": "RAMDEVRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RMM",
    "en": "RAMESWARAM",
    "ec": "RAMESWARAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "RMGD",
    "en": "RAMGAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "RSC",
    "en": "RAMGANAGA SC"
  },
  {
    "sc": "RGB",
    "en": "RAMGANGA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RMGJ",
    "en": "RAMGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RMA",
    "en": "RAMGANJ MANDI",
    "ec": "RAMGANJ MANDI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RAH",
    "en": "RAMGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RMT",
    "en": "RAMGARH CANT",
    "se": "JHARKHAND"
  },
  {
    "sc": "RGH",
    "en": "RAMGARHWA",
    "se": "BIHAR"
  },
  {
    "sc": "RGI",
    "en": "RAMGIRI",
    "se": "KARNATAKA"
  },
  {
    "sc": "RYM",
    "en": "RAMIDI HALT",
    "se": "PUNJAB"
  },
  {
    "sc": "RKI",
    "en": "RAMKANALI JN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RKAE",
    "en": "RAMKISTOPORE",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RKL",
    "en": "RAMKOLA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RAK",
    "en": "RAMKOT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RANG",
    "en": "RAMLING",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RMF",
    "en": "RAMNA",
    "se": "JHARKHAND"
  },
  {
    "sc": "RMR",
    "en": "RAMNAGAR",
    "ec": "RAMNAGAR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "RMRB",
    "en": "RAMNAGAR BENGAL",
    "ec": "DIGHA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RTR",
    "en": "RAMNATHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RMPH",
    "en": "RAMPAHARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RA",
    "en": "RAMPARDA",
    "se": "GUJARAT"
  },
  {
    "sc": "RMU",
    "en": "RAMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RMPB",
    "en": "RAMPUR BAZAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RDUM",
    "en": "RAMPUR DUMRA",
    "se": "BIHAR"
  },
  {
    "sc": "RMPR",
    "en": "RAMPUR HALT",
    "se": "BIHAR"
  },
  {
    "sc": "RPH",
    "en": "RAMPUR HAT",
    "ec": "RAMPUR HAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RPMN",
    "en": "RAMPUR MANIHARN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RMB",
    "en": "RAMPURA BERI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "PUL",
    "en": "RAMPURA PHUL",
    "se": "PUNJAB"
  },
  {
    "sc": "RMJ",
    "en": "RAMRAJATALA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RMQ",
    "en": "RAMRI"
  },
  {
    "sc": "RSG",
    "en": "RAMSAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RXN",
    "en": "RAMSAN",
    "se": "GUJARAT"
  },
  {
    "sc": "RMX",
    "en": "RAMSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RMSR",
    "en": "RAMSINGHPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RTK",
    "en": "RAMTEK",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RNBD",
    "en": "RANA BORDI",
    "se": "GUJARAT"
  },
  {
    "sc": "RHA",
    "en": "RANAGHAT JN",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RNL",
    "en": "RANALA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RPZ",
    "en": "RANAPRATAPNAGAR",
    "ec": "UDAIPUR CITY",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RWO",
    "en": "RANAVAV",
    "se": "GUJARAT"
  },
  {
    "sc": "RRME",
    "en": "RANCHI ROAD",
    "se": "JHARKHAND"
  },
  {
    "sc": "RLD",
    "en": "RANDALA",
    "se": "GUJARAT"
  },
  {
    "sc": "RDJ",
    "en": "RANDHEJA",
    "se": "GUJARAT"
  },
  {
    "sc": "RNGG",
    "en": "RANGALITING",
    "se": "ASSAM"
  },
  {
    "sc": "RXR",
    "en": "RANGAPAHAR",
    "se": "ASSAM"
  },
  {
    "sc": "RXRX",
    "en": "RANGAPAHAR CRS",
    "se": "NAGALAND"
  },
  {
    "sc": "RNI",
    "en": "RANGAPANI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RPAN",
    "en": "RANGAPARA NORTH",
    "ec": "DEKARGAON",
    "se": "ASSAM"
  },
  {
    "sc": "RGM",
    "en": "RANGAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RRGA",
    "en": "RANGAREDDY GUDA",
    "se": "TELANGANA"
  },
  {
    "sc": "RNY",
    "en": "RANGIYA JN",
    "se": "ASSAM"
  },
  {
    "sc": "RMH",
    "en": "RANGMAHAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RTG",
    "en": "RANGTONG",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RANI",
    "en": "RANI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RGBP",
    "en": "RANI GAIDINLIU",
    "se": "MANIPUR"
  },
  {
    "sc": "RNR",
    "en": "RANIBENNUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "RNG",
    "en": "RANIGANJ",
    "ec": "ASANSOL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RKR",
    "en": "RANIKUND RARAH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RNX",
    "en": "RANIPATRA",
    "se": "BIHAR"
  },
  {
    "sc": "RNRD",
    "en": "RANIPUR ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RNTL",
    "en": "RANITAL",
    "se": "ODISHA"
  },
  {
    "sc": "RNV",
    "en": "RANIWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RNJD",
    "en": "RANJANGAON RD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RNE",
    "en": "RANJANI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RW",
    "en": "RANKUA",
    "se": "GUJARAT"
  },
  {
    "sc": "RNO",
    "en": "RANOLI",
    "se": "GUJARAT"
  },
  {
    "sc": "RNIS",
    "en": "RANOLISHISHU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RUR",
    "en": "RANPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "RNB",
    "en": "RANPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RTJ",
    "en": "RANTEJ",
    "se": "GUJARAT"
  },
  {
    "sc": "RNT",
    "en": "RANTHAMBHORE",
    "ec": "SAWAI MADHOPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RPP",
    "en": "RANU PIPRI",
    "se": "GUJARAT"
  },
  {
    "sc": "RUJ",
    "en": "RANUJ",
    "se": "GUJARAT"
  },
  {
    "sc": "RCJ",
    "en": "RANYAL JASMIYA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RTI",
    "en": "RAOTI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RPRL",
    "en": "RAPARLA HALT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RAS",
    "en": "RAS",
    "se": "GUJARAT"
  },
  {
    "sc": "RSNA",
    "en": "RASANA",
    "se": "GUJARAT"
  },
  {
    "sc": "RSYI",
    "en": "RASAYANI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RDK",
    "en": "RASHODPURA KHRI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RASP",
    "en": "RASIPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "RSM",
    "en": "RASMARA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "RSR",
    "en": "RASRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RUB",
    "en": "RASULABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RES",
    "en": "RASULL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RSLR",
    "en": "RASULPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RPGU",
    "en": "RASULPURGOGAMAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RYS",
    "en": "RASURIYA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RSME",
    "en": "RASWAN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RTBR",
    "en": "RATABARI",
    "se": "ASSAM"
  },
  {
    "sc": "RTU",
    "en": "RATAN SARAI",
    "se": "BIHAR"
  },
  {
    "sc": "RSH",
    "en": "RATAN SHAHR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RTGN",
    "en": "RATANGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RTGH",
    "en": "RATANGARH JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RXW",
    "en": "RATANGARH WEST",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RKK",
    "en": "RATANGRH KNKWAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RPUR",
    "en": "RATANPUR",
    "se": "BIHAR"
  },
  {
    "sc": "RTP",
    "en": "RATANPURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RCR",
    "en": "RATAR CHATTAR",
    "se": "PUNJAB"
  },
  {
    "sc": "RDDE",
    "en": "RATHDHANA",
    "se": "HARYANA"
  },
  {
    "sc": "RKN",
    "en": "RATI KA NAGLA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RIKA",
    "en": "RATIKHEDA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RTM",
    "en": "RATLAM JN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RTMN",
    "en": "RATLAM NEW",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RN",
    "en": "RATNAGIRI",
    "ec": "RATNAGIRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RTGR",
    "en": "RATNAGIRI ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "RUT",
    "en": "RATNAL",
    "se": "GUJARAT"
  },
  {
    "sc": "RNU",
    "en": "RATNAPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RKG",
    "en": "RATTOKE GUDWARA",
    "se": "PUNJAB"
  },
  {
    "sc": "RAU",
    "en": "RAU",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RUL",
    "en": "RAULI",
    "se": "ODISHA"
  },
  {
    "sc": "RWA",
    "en": "RAUTARA",
    "se": "BIHAR"
  },
  {
    "sc": "RZN",
    "en": "RAUZAGAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RPK",
    "en": "RAVALPALI KALAN",
    "se": "TELANGANA"
  },
  {
    "sc": "RVS",
    "en": "RAVANASAMUDRAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "RV",
    "en": "RAVER",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RVD",
    "en": "RAVIKAMPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RVKH",
    "en": "RAVINDRAKHANI",
    "se": "TELANGANA"
  },
  {
    "sc": "RDT",
    "en": "RAVTHA ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RWJ",
    "en": "RAWANIA DUNGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RJ",
    "en": "RAWAT GANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RPO",
    "en": "RAWATPUR",
    "ec": "KANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RXL",
    "en": "RAXAUL JN",
    "se": "BIHAR"
  },
  {
    "sc": "RAY",
    "en": "RAY",
    "se": "JHARKHAND"
  },
  {
    "sc": "RAYA",
    "en": "RAYA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RDG",
    "en": "RAYADRUG",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RGDA",
    "en": "RAYAGADA",
    "se": "ODISHA"
  },
  {
    "sc": "RY",
    "en": "RAYAKA",
    "se": "GUJARAT"
  },
  {
    "sc": "RYC",
    "en": "RAYAKKOTTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "RLO",
    "en": "RAYALCHERUVU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RYP",
    "en": "RAYANAPADU",
    "ec": "VIJAYAWADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RRU",
    "en": "RAYARU",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RBG",
    "en": "RAYBAG",
    "se": "KARNATAKA"
  },
  {
    "sc": "RZJ",
    "en": "RAZAGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RJP",
    "en": "RAZAMPETA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RCF",
    "en": "RCF HALT",
    "se": "PUNJAB"
  },
  {
    "sc": "RECH",
    "en": "RECHNI ROAD",
    "se": "TELANGANA"
  },
  {
    "sc": "REM",
    "en": "REDDIGUDEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "REP",
    "en": "REDDIPALEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RPL",
    "en": "REDDIPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RDY",
    "en": "REDIPALAYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "RLL",
    "en": "REGADIPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "REG",
    "en": "REGUPALEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RTS",
    "en": "REHTA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "REJ",
    "en": "REJINAGAR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RLG",
    "en": "RELANGI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "REN",
    "en": "REN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RGL",
    "en": "RENGALI",
    "se": "ODISHA"
  },
  {
    "sc": "RENH",
    "en": "RENHAT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RU",
    "en": "RENIGUNTA JN",
    "ec": "TIRUPATI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RCA",
    "en": "RENTACHINTALA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RET",
    "en": "RENTIA",
    "se": "GUJARAT"
  },
  {
    "sc": "RNQ",
    "en": "RENUKUT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RNW",
    "en": "RENWAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ROI",
    "en": "REOTI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RBK",
    "en": "REOTI B KHERA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RAL",
    "en": "REPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RTN",
    "en": "RETANG",
    "ec": "KHURDA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "RAKL",
    "en": "RETHORAKALAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "REWA",
    "en": "REWA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RE",
    "en": "REWARI",
    "se": "HARYANA"
  },
  {
    "sc": "RRL",
    "en": "REWRAL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RHW",
    "en": "RHRA GHALUGHRA",
    "se": "PUNJAB"
  },
  {
    "sc": "REAI",
    "en": "RIASI",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "RBR",
    "en": "RIBADA",
    "se": "GUJARAT"
  },
  {
    "sc": "RR",
    "en": "RICHHA ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RCGT",
    "en": "RICHUGHUTU",
    "se": "JHARKHAND"
  },
  {
    "sc": "RID",
    "en": "RIDHORE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RIGA",
    "en": "RIGA",
    "se": "BIHAR"
  },
  {
    "sc": "RDD",
    "en": "RIKHABDEV ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RGS",
    "en": "RINGAS JN",
    "ec": "KHATU SHYAM",
    "se": "RAJASTHAN",
    "tg": "KHATU SHYAM"
  },
  {
    "sc": "RSA",
    "en": "RISAMA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "RKSH",
    "en": "RISHIKESH",
    "ec": "HARIDWAR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "RIS",
    "en": "RISHRA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RS",
    "en": "RISIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "REI",
    "en": "RITHI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RSWT",
    "en": "RMGRH SHEKHWATI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RKO",
    "en": "RMKRSHNAPRM GTE",
    "se": "TELANGANA"
  },
  {
    "sc": "RLS",
    "en": "RMNA ALBEL SNGH",
    "se": "PUNJAB"
  },
  {
    "sc": "RQJ",
    "en": "RNINGR JLPAIGRI",
    "ec": "NEW JALPAIGURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ROB",
    "en": "ROBERTSON",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "ROHA",
    "en": "ROHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ROHN",
    "en": "ROHAD NAGAR",
    "se": "HARYANA"
  },
  {
    "sc": "RLK",
    "en": "ROHAL KHURD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RNA",
    "en": "ROHANA KALAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RT",
    "en": "ROHAT",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RHNE",
    "en": "ROHINI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ROK",
    "en": "ROHTAK JN",
    "se": "HARYANA"
  },
  {
    "sc": "RML",
    "en": "ROMPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RPCA",
    "en": "ROMPICHERLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RK",
    "en": "ROORKEE",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "RORA",
    "en": "RORA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RRW",
    "en": "RORANWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "RMW",
    "en": "ROSHAN MAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RHN",
    "en": "ROSHANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RGO",
    "en": "ROTEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ROU",
    "en": "ROURKELA",
    "ec": "ROURKELA",
    "se": "ODISHA"
  },
  {
    "sc": "RMZ",
    "en": "ROUTHPURAM HALT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "RWH",
    "en": "ROWRIAH SDG",
    "se": "ASSAM"
  },
  {
    "sc": "RWTB",
    "en": "ROWTA BAGAN",
    "se": "ASSAM"
  },
  {
    "sc": "RPM",
    "en": "ROYAPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "ROZA",
    "en": "ROZA JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RDN",
    "en": "RUDAIN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RDL",
    "en": "RUDAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RUPC",
    "en": "RUDRAPUR CITY",
    "ec": "KATHGODAM",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "RKD",
    "en": "RUKADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "RKX",
    "en": "RUKHI",
    "se": "HARYANA"
  },
  {
    "sc": "RMY",
    "en": "RUKMAPUR",
    "se": "TELANGANA"
  },
  {
    "sc": "RUI",
    "en": "RUKNI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RDE",
    "en": "RUNDHI",
    "se": "HARYANA"
  },
  {
    "sc": "RNJ",
    "en": "RUNIJA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RNH",
    "en": "RUNKHERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RNKA",
    "en": "RUNKUTA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RUSD",
    "en": "RUNNI SAIDPUR",
    "se": "BIHAR"
  },
  {
    "sc": "RPI",
    "en": "RUPAHELI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RPY",
    "en": "RUPAI",
    "se": "ASSAM"
  },
  {
    "sc": "RUM",
    "en": "RUPAMAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RPB",
    "en": "RUPASIBARI",
    "se": "ASSAM"
  },
  {
    "sc": "RPLY",
    "en": "RUPAULI",
    "se": "BIHAR"
  },
  {
    "sc": "RPD",
    "en": "RUPAUND",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "RBS",
    "en": "RUPBAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "RPAR",
    "en": "RUPNAGAR",
    "se": "PUNJAB"
  },
  {
    "sc": "RNPR",
    "en": "RUPNARAYANPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "RPRD",
    "en": "RUPRA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "ROP",
    "en": "RUPSA JN",
    "ec": "BALASORE",
    "se": "ODISHA"
  },
  {
    "sc": "RURA",
    "en": "RURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RRAL",
    "en": "RURE ASAL",
    "se": "PUNJAB"
  },
  {
    "sc": "ROA",
    "en": "RUSERA GHAT",
    "se": "BIHAR"
  },
  {
    "sc": "RTA",
    "en": "RUTHIYAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SPAK",
    "en": "S ARNIYA KHURD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SBV",
    "en": "S BAKHTIYARPUR",
    "se": "BIHAR"
  },
  {
    "sc": "SHRN",
    "en": "S HIRDARAMNAGAR",
    "ec": "BHOPAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "BIH",
    "en": "S HIRDARAMNAGAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "NGZ",
    "en": "S K NAGJIHARI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SKAP",
    "en": "S K PARA",
    "se": "TRIPURA"
  },
  {
    "sc": "SPAM",
    "en": "S PANAMBAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SVPM",
    "en": "S VENKTESWRPALM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SUPP",
    "en": "S.UPPALAPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SBL",
    "en": "SABALGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SBIB",
    "en": "SABARMATI BG",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "SBI",
    "en": "SABARMATI JN",
    "se": "GUJARAT"
  },
  {
    "sc": "SBT",
    "en": "SABARMATI JN",
    "se": "GUJARAT"
  },
  {
    "sc": "SBO",
    "en": "SABAUR",
    "se": "BIHAR"
  },
  {
    "sc": "SBDP",
    "en": "SABDALPUR JN.",
    "se": "BIHAR"
  },
  {
    "sc": "SZZ",
    "en": "SABIRA",
    "se": "ODISHA"
  },
  {
    "sc": "SR",
    "en": "SABLI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "SBRM",
    "en": "SABROOM",
    "se": "TRIPURA"
  },
  {
    "sc": "SCH",
    "en": "SACHIN",
    "se": "GUJARAT"
  },
  {
    "sc": "SNA",
    "en": "SADANAPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "DSB",
    "en": "SADAR BAZAR",
    "se": "DELHI"
  },
  {
    "sc": "SSPR",
    "en": "SADASHIBAPUR",
    "se": "ODISHA"
  },
  {
    "sc": "SSPD",
    "en": "SADASHIVAPET RD",
    "se": "TELANGANA"
  },
  {
    "sc": "SDT",
    "en": "SADAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SSZ",
    "en": "SADDA SINGHWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "SHL",
    "en": "SADHLI",
    "se": "GUJARAT"
  },
  {
    "sc": "SDY",
    "en": "SADHOO GARH",
    "se": "PUNJAB"
  },
  {
    "sc": "SDE",
    "en": "SADISOPUR",
    "se": "BIHAR"
  },
  {
    "sc": "SADL",
    "en": "SADLA",
    "se": "GUJARAT"
  },
  {
    "sc": "SPJB",
    "en": "SADPR JALALABAD",
    "se": "PUNJAB"
  },
  {
    "sc": "SDLP",
    "en": "SADULPUR JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SDS",
    "en": "SADULSHAHR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SDUA",
    "en": "SADURA",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "SGJ",
    "en": "SAFDARGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SFH",
    "en": "SAFEDABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SFQ",
    "en": "SAFEDPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "SFS",
    "en": "SAFIASARAI",
    "se": "BIHAR"
  },
  {
    "sc": "SFDE",
    "en": "SAFIDON",
    "se": "HARYANA"
  },
  {
    "sc": "SFX",
    "en": "SAFILGUDA",
    "se": "TELANGANA"
  },
  {
    "sc": "SFPR",
    "en": "SAFIPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SFR",
    "en": "SAFRAI",
    "se": "ASSAM"
  },
  {
    "sc": "SGDP",
    "en": "SAGADAPATA",
    "se": "ODISHA"
  },
  {
    "sc": "SRF",
    "en": "SAGAR JAMBAGARU",
    "se": "KARNATAKA"
  },
  {
    "sc": "SDI",
    "en": "SAGARDIGHI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "STE",
    "en": "SAGARKATTE",
    "se": "KARNATAKA"
  },
  {
    "sc": "SVI",
    "en": "SAGARPALI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SGL",
    "en": "SAGAULI JN",
    "se": "BIHAR"
  },
  {
    "sc": "SAGM",
    "en": "SAGMA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SAO",
    "en": "SAGONI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SXA",
    "en": "SAGPHATA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SDG",
    "en": "SAHADAI BUZURG",
    "se": "BIHAR"
  },
  {
    "sc": "SRE",
    "en": "SAHARANPUR",
    "ec": "SAHARANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SHC",
    "en": "SAHARSA JN",
    "se": "BIHAR"
  },
  {
    "sc": "SHKY",
    "en": "SAHARSA KACHERI",
    "se": "BIHAR"
  },
  {
    "sc": "SHSK",
    "en": "SAHARSRAKUND",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SHJ",
    "en": "SAHASPUR ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "STW",
    "en": "SAHATWAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SWRT",
    "en": "SAHAWAR TOWN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SAHL",
    "en": "SAHELI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SAHR",
    "en": "SAHERI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SBB",
    "en": "SAHIBABAD",
    "ec": "NEW DELHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SBG",
    "en": "SAHIBGANJ JN",
    "ec": "SAHIBGANJ",
    "se": "JHARKHAND"
  },
  {
    "sc": "SKJ",
    "en": "SAHIBPUR KAMAL",
    "se": "BIHAR"
  },
  {
    "sc": "SASN",
    "en": "SAHIBZADA ASNGR",
    "se": "PUNJAB"
  },
  {
    "sc": "SAHP",
    "en": "SAHIJPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "SWA",
    "en": "SAHJANWA",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SAJH",
    "en": "SAHJHA HALT",
    "se": "BIHAR"
  },
  {
    "sc": "SHWL",
    "en": "SAHUWALA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SSPN",
    "en": "SAI P NILAYAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SDC",
    "en": "SAIDABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SWX",
    "en": "SAIDANWALA",
    "se": "PUNJAB"
  },
  {
    "sc": "SP",
    "en": "SAIDAPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SADP",
    "en": "SAIDAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "SYK",
    "en": "SAIDKHANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SYJ",
    "en": "SAIDRAJA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SHRD",
    "en": "SAIJ SERTHA RD",
    "se": "GUJARAT"
  },
  {
    "sc": "SQJ",
    "en": "SAILA KHURD",
    "se": "PUNJAB"
  },
  {
    "sc": "SNSI",
    "en": "SAINAGAR SHIRDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SFC",
    "en": "SAINTALA",
    "se": "ODISHA"
  },
  {
    "sc": "SNT",
    "en": "SAINTHIA",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SIPI",
    "en": "SAIPHAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SANG",
    "en": "SAIRANG",
    "se": "MIZORAM"
  },
  {
    "sc": "SYH",
    "en": "SAIYEDPUR BHTRI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SYWN",
    "en": "SAIYID SARAWAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SJF",
    "en": "SAJANVAR ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "SVJ",
    "en": "SAJIYAVADAR",
    "se": "GUJARAT"
  },
  {
    "sc": "SJM",
    "en": "SAJUMA",
    "se": "HARYANA"
  },
  {
    "sc": "SAK",
    "en": "SAK BAHADURPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "SLD",
    "en": "SAKALDIHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SKAR",
    "en": "SAKARIYA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SHYP",
    "en": "SAKHARAYAPATNA",
    "se": "KARNATAKA"
  },
  {
    "sc": "SIL",
    "en": "SAKHI GOPAL",
    "ec": "PURI",
    "se": "ODISHA"
  },
  {
    "sc": "SKF",
    "en": "SAKHOTI TANDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SKR",
    "en": "SAKHPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "SK",
    "en": "SAKHUN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SKLR",
    "en": "SAKLESHPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "SKI",
    "en": "SAKRI JN",
    "se": "BIHAR"
  },
  {
    "sc": "SLJ",
    "en": "SAKRIGALI JN",
    "se": "JHARKHAND"
  },
  {
    "sc": "SKGH",
    "en": "SAKTESGARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SKT",
    "en": "SAKTI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SKG",
    "en": "SAKTIGARH",
    "ec": "BARDDHAMAN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SQQ",
    "en": "SALAGAON",
    "se": "ODISHA"
  },
  {
    "sc": "SYA",
    "en": "SALAIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SLKX",
    "en": "SALAKATI",
    "se": "ASSAM"
  },
  {
    "sc": "SMT",
    "en": "SALAMATPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SLS",
    "en": "SALANPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SALE",
    "en": "SALAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SLRP",
    "en": "SALARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SLNA",
    "en": "SALAUNA",
    "se": "BIHAR"
  },
  {
    "sc": "SZ",
    "en": "SALAWAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SXX",
    "en": "SALBARI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SLB",
    "en": "SALBONI",
    "ec": "SALBONI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SCA",
    "en": "SALCHAPRA",
    "se": "ASSAM"
  },
  {
    "sc": "SKS",
    "en": "SALEKASA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SAMT",
    "en": "SALEM MARKET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SXT",
    "en": "SALEM TOWN",
    "ec": "SALEM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SJSM",
    "en": "SALEMGARHMASANI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SRU",
    "en": "SALEMPUR JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SHIT",
    "en": "SALHAITOLA P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SLHA",
    "en": "SALHANA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SALI",
    "en": "SALI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SCKR",
    "en": "SALICHAUKA ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SMBH",
    "en": "SALIMPUR BIHAR",
    "se": "BIHAR"
  },
  {
    "sc": "SMM",
    "en": "SALIYAMANGALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SJD",
    "en": "SALJADA",
    "se": "GUJARAT"
  },
  {
    "sc": "SLKR",
    "en": "SALKAROAD",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SAF",
    "en": "SALKHAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SRI",
    "en": "SALMARI",
    "se": "BIHAR"
  },
  {
    "sc": "SLR",
    "en": "SALOGRA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "SLP",
    "en": "SALPA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SYL",
    "en": "SALPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SALR",
    "en": "SALUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SAL",
    "en": "SALWA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SMGR",
    "en": "SAMAGURI",
    "se": "ASSAM"
  },
  {
    "sc": "SIOB",
    "en": "SAMAKHIALI B G",
    "se": "GUJARAT"
  },
  {
    "sc": "SAML",
    "en": "SAMAL",
    "se": "ODISHA"
  },
  {
    "sc": "SMK",
    "en": "SAMALKHA",
    "se": "HARYANA"
  },
  {
    "sc": "SLO",
    "en": "SAMALKOT JN",
    "ec": "KAKINADA PORT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SLY",
    "en": "SAMALPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SMF",
    "en": "SAMAR GOPALPUR",
    "se": "HARYANA"
  },
  {
    "sc": "SQE",
    "en": "SAMARALA HALT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SPJ",
    "en": "SAMASTIPUR JN",
    "se": "BIHAR"
  },
  {
    "sc": "SMSR",
    "en": "SAMASWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SER",
    "en": "SAMAYANALLUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SMBX",
    "en": "SAMBA",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "SBP",
    "en": "SAMBALPUR",
    "ec": "SAMBALPUR",
    "se": "ODISHA"
  },
  {
    "sc": "SBPY",
    "en": "SAMBALPUR CITY",
    "ec": "SAMBALPUR",
    "se": "ODISHA"
  },
  {
    "sc": "SBPD",
    "en": "SAMBALPUR ROAD",
    "ec": "SAMBALPUR",
    "se": "ODISHA"
  },
  {
    "sc": "SHTS",
    "en": "SAMBHAL HTM SAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SBR",
    "en": "SAMBHAR LAKE",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SBTI",
    "en": "SAMBHETI",
    "se": "GUJARAT"
  },
  {
    "sc": "SMU",
    "en": "SAMBHU",
    "se": "PUNJAB"
  },
  {
    "sc": "SXB",
    "en": "SAMBRE",
    "se": "KARNATAKA"
  },
  {
    "sc": "SMR",
    "en": "SAMDHARI JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SHW",
    "en": "SAMHON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SMLA",
    "en": "SAMLAYA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "SMLT",
    "en": "SAMLOTI",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "SMC",
    "en": "SAMNAPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SPGR",
    "en": "SAMPIGE ROAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "SPZ",
    "en": "SAMPLA",
    "se": "HARYANA"
  },
  {
    "sc": "SMRL",
    "en": "SAMRALA",
    "se": "PUNJAB"
  },
  {
    "sc": "SRK",
    "en": "SAMRAU",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SM",
    "en": "SAMSI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SMAE",
    "en": "SAMUDRAGARH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SMDM",
    "en": "SAMUDRAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SMTA",
    "en": "SAMUKTALA ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SNL",
    "en": "SANAHWAL",
    "se": "PUNJAB"
  },
  {
    "sc": "SAU",
    "en": "SANAND",
    "se": "GUJARAT"
  },
  {
    "sc": "SAPD",
    "en": "SANAPADAR",
    "se": "ODISHA"
  },
  {
    "sc": "SNF",
    "en": "SANAT NAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "SNTL",
    "en": "SANATHAL",
    "se": "GUJARAT"
  },
  {
    "sc": "SWU",
    "en": "SANAURA",
    "se": "PUNJAB"
  },
  {
    "sc": "SWD",
    "en": "SANAWAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SCI",
    "en": "SANCHI",
    "ec": "BHOPAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SNDY",
    "en": "SANDAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SLKN",
    "en": "SANDAL KALAN",
    "se": "HARYANA"
  },
  {
    "sc": "SLV",
    "en": "SANDALPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SDSL",
    "en": "SANDASAL",
    "se": "GUJARAT"
  },
  {
    "sc": "SDHR",
    "en": "SANDHANIDHAR",
    "se": "GUJARAT"
  },
  {
    "sc": "SNDA",
    "en": "SANDHIA",
    "se": "GUJARAT"
  },
  {
    "sc": "SAN",
    "en": "SANDILA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SNX",
    "en": "SANEH ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SGDN",
    "en": "SANGALDAN",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "SGNL",
    "en": "SANGANAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "SNGN",
    "en": "SANGANER",
    "ec": "JAIPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SNGR",
    "en": "SANGANNAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SGRR",
    "en": "SANGAR",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "SGRA",
    "en": "SANGARIA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SGF",
    "en": "SANGAT",
    "se": "PUNJAB"
  },
  {
    "sc": "SLI",
    "en": "SANGLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SGR",
    "en": "SANGMESHWAR",
    "ec": "RATNAGIRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SGLA",
    "en": "SANGOLA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SNU",
    "en": "SANGRAMPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SBS",
    "en": "SANGRANA SAHIB",
    "se": "PUNJAB"
  },
  {
    "sc": "SAG",
    "en": "SANGRUR",
    "se": "PUNJAB"
  },
  {
    "sc": "SWQ",
    "en": "SANGWI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SFA",
    "en": "SANHERA HALT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SAC",
    "en": "SANICHARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SNAD",
    "en": "SANIYAD",
    "se": "GUJARAT"
  },
  {
    "sc": "SNJL",
    "en": "SANJALI",
    "se": "GUJARAT"
  },
  {
    "sc": "SJMA",
    "en": "SANJAMALA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SJN",
    "en": "SANJAN",
    "se": "GUJARAT"
  },
  {
    "sc": "SJER",
    "en": "SANJARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SJJ",
    "en": "SANJHA",
    "se": "BIHAR"
  },
  {
    "sc": "SJDA",
    "en": "SANJUJE DA AREY",
    "se": "GOA"
  },
  {
    "sc": "SANK",
    "en": "SANK",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SNKR",
    "en": "SANKA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SLGM",
    "en": "SANKARALINGAPRM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SNKL",
    "en": "SANKARANKOVIL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SGE",
    "en": "SANKARIDURG",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SNQ",
    "en": "SANKARPUR",
    "se": "JHARKHAND"
  },
  {
    "sc": "SNHR",
    "en": "SANKHAI",
    "se": "GUJARAT"
  },
  {
    "sc": "SNKP",
    "en": "SANKHALPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "SXP",
    "en": "SANKOPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SEL",
    "en": "SANKRALL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SKVL",
    "en": "SANKVAL",
    "se": "GOA"
  },
  {
    "sc": "SFE",
    "en": "SANODIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SNSR",
    "en": "SANOSARA NANDRA",
    "se": "GUJARAT"
  },
  {
    "sc": "SOA",
    "en": "SANOSRA",
    "se": "GUJARAT"
  },
  {
    "sc": "SNRR",
    "en": "SANSARPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SAT",
    "en": "SANT ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "STC",
    "en": "SANTA CRUZ",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SNTD",
    "en": "SANTALDIH",
    "ec": "ADRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SNLR",
    "en": "SANTALPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "SAB",
    "en": "SANTAMAGULUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "STRB",
    "en": "SANTIR BAZAR",
    "se": "TRIPURA"
  },
  {
    "sc": "SSP",
    "en": "SANTOSHPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SRC",
    "en": "SANTRAGACHI JN",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SNVR",
    "en": "SANVATSAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SVM",
    "en": "SANVERDAM CHUCH",
    "se": "GOA"
  },
  {
    "sc": "SVO",
    "en": "SANVRAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SNRA",
    "en": "SANWARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SONR",
    "en": "SAONER",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SZH",
    "en": "SAONGA HALT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SGC",
    "en": "SAONGI P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SOF",
    "en": "SAOTA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SPX",
    "en": "SAPATGRAM",
    "se": "ASSAM"
  },
  {
    "sc": "SPDA",
    "en": "SAPDA",
    "se": "GUJARAT"
  },
  {
    "sc": "SAPE",
    "en": "SAPE WAMNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SPK",
    "en": "SAPEKHATI",
    "se": "ASSAM"
  },
  {
    "sc": "SAH",
    "en": "SAPHALE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SDH",
    "en": "SARADHNA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SRDA",
    "en": "SARADIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "SGRD",
    "en": "SARAGAON RD P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SRBA",
    "en": "SARAGBUNDIA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SGV",
    "en": "SARAGCHNI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SRGP",
    "en": "SARAGIPALI",
    "se": "ODISHA"
  },
  {
    "sc": "SAI",
    "en": "SARAI",
    "se": "BIHAR"
  },
  {
    "sc": "SBJ",
    "en": "SARAI BANJARA",
    "se": "PUNJAB"
  },
  {
    "sc": "SB",
    "en": "SARAI BHOPAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SYC",
    "en": "SARAI CHANDI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SPGL",
    "en": "SARAI GOPAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SVZ",
    "en": "SARAI HARKHU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SQN",
    "en": "SARAI KANSRAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SMZ",
    "en": "SARAI MIR",
    "ec": "AZAMGARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "RKS",
    "en": "SARAI RANI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SFW",
    "en": "SARANGPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SAPR",
    "en": "SARANGPUR ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "SRWN",
    "en": "SARASWATINAGAR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SYU",
    "en": "SARAYAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SRGR",
    "en": "SARAYGARH",
    "se": "BIHAR"
  },
  {
    "sc": "SBRA",
    "en": "SARBAHARA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SDPR",
    "en": "SARDAR PATEL RD",
    "se": "DELHI"
  },
  {
    "sc": "SRZ",
    "en": "SARDARGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SDGM",
    "en": "SARDARGRAM",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "SANR",
    "en": "SARDARNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SRDR",
    "en": "SARDARSHAHR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SUA",
    "en": "SARDIHA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SGAM",
    "en": "SAREIGRAM",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SSR",
    "en": "SARERI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SUJ",
    "en": "SARJU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SKNP",
    "en": "SARKANPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SKX",
    "en": "SARKARA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "SEJ",
    "en": "SARKHEJ",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "SIQ",
    "en": "SARKONI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SMND",
    "en": "SARMATANR",
    "se": "JHARKHAND"
  },
  {
    "sc": "SRM",
    "en": "SARNA",
    "se": "PUNJAB"
  },
  {
    "sc": "SRNT",
    "en": "SARNATH",
    "ec": "BANARAS",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SOJ",
    "en": "SAROJINI NAGAR",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "SRL",
    "en": "SAROLA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SZB",
    "en": "SARONA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SZA",
    "en": "SAROTRA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "SRDH",
    "en": "SARSADH",
    "se": "HARYANA"
  },
  {
    "sc": "SSW",
    "en": "SARSAWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SRSI",
    "en": "SARSI",
    "se": "BIHAR"
  },
  {
    "sc": "SSKI",
    "en": "SARSOKI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SPY",
    "en": "SARSONPURI P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SZR",
    "en": "SARUPATHAR",
    "se": "ASSAM"
  },
  {
    "sc": "SRPR",
    "en": "SARUPSAR JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SVD",
    "en": "SARWARI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SSU",
    "en": "SASA MUSA",
    "se": "BIHAR"
  },
  {
    "sc": "SLU",
    "en": "SASALU",
    "se": "KARNATAKA"
  },
  {
    "sc": "SASG",
    "en": "SASAN GIR",
    "se": "GUJARAT"
  },
  {
    "sc": "SSM",
    "en": "SASARAM",
    "se": "BIHAR"
  },
  {
    "sc": "SNS",
    "en": "SASNI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SSN",
    "en": "SASON",
    "se": "ODISHA"
  },
  {
    "sc": "STKT",
    "en": "SASTHANKOTTA",
    "se": "KERALA"
  },
  {
    "sc": "SSV",
    "en": "SASVAD ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "STDR",
    "en": "SATADHAR",
    "se": "GUJARAT"
  },
  {
    "sc": "STR",
    "en": "SATARA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SZF",
    "en": "SATBAHINI",
    "se": "JHARKHAND"
  },
  {
    "sc": "SNIE",
    "en": "SATH NARAINI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "STJT",
    "en": "SATHAJAGAT",
    "se": "BIHAR"
  },
  {
    "sc": "SAHI",
    "en": "SATHI",
    "se": "BIHAR"
  },
  {
    "sc": "SAA",
    "en": "SATHIAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SWF",
    "en": "SATHIN ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SSPH",
    "en": "SATISH SAMNT HT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "STA",
    "en": "SATNA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "STNL",
    "en": "SATNALI",
    "se": "HARYANA"
  },
  {
    "sc": "STZ",
    "en": "SATRAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "STD",
    "en": "SATROD",
    "se": "HARYANA"
  },
  {
    "sc": "SAP",
    "en": "SATTENAPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SQD",
    "en": "SATTIRAKKUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "STUR",
    "en": "SATULUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SCO",
    "en": "SATUNA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SRT",
    "en": "SATUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "STVA",
    "en": "SATYAVADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SGO",
    "en": "SAUGOR",
    "ec": "SAUGOR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SUAL",
    "en": "SAUNDAL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SNH",
    "en": "SAUNSHI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SASR",
    "en": "SAUSAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SYM",
    "en": "SAVALYAPURAM JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SVNR",
    "en": "SAVANUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "SVX",
    "en": "SAVARDA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SVKD",
    "en": "SAVARKUNDLA",
    "se": "GUJARAT"
  },
  {
    "sc": "SAV",
    "en": "SAVDA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SVLI",
    "en": "SAVLI",
    "se": "GUJARAT"
  },
  {
    "sc": "SVB",
    "en": "SAVNI",
    "se": "GUJARAT"
  },
  {
    "sc": "SWM",
    "en": "SAWAI MADHOPUR",
    "ec": "SAWAI MADHOPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SVG",
    "en": "SAWALGI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SWKE",
    "en": "SAWALKOT",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "SWV",
    "en": "SAWANTWADI ROAD",
    "ec": "RATNAGIRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SAY",
    "en": "SAYAMA",
    "se": "GUJARAT"
  },
  {
    "sc": "SYN",
    "en": "SAYAN",
    "se": "GUJARAT"
  },
  {
    "sc": "SBBJ",
    "en": "SBB JOGULAMBA H",
    "se": "TELANGANA"
  },
  {
    "sc": "SBW",
    "en": "SBEWBABUDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "JET",
    "en": "SECBAD JAMES ST",
    "se": "TELANGANA"
  },
  {
    "sc": "SDPT",
    "en": "SEDARAMPATTU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SEW",
    "en": "SEHAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SRBZ",
    "en": "SEHARA BAZAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SEH",
    "en": "SEHORE",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SW",
    "en": "SEHRAMAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SKKE",
    "en": "SEKERKOTE",
    "se": "TRIPURA"
  },
  {
    "sc": "SEQ",
    "en": "SEKHA",
    "se": "PUNJAB"
  },
  {
    "sc": "SLX",
    "en": "SELENG HAT",
    "se": "ASSAM"
  },
  {
    "sc": "SLOR",
    "en": "SELOO ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SELU",
    "en": "SELU",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SYF",
    "en": "SEMAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SMO",
    "en": "SEMAPUR",
    "se": "BIHAR"
  },
  {
    "sc": "SES",
    "en": "SEMARI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SRKI",
    "en": "SEMARKHERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SE",
    "en": "SEMLA",
    "se": "GUJARAT"
  },
  {
    "sc": "SRA",
    "en": "SEMRA",
    "se": "BIHAR"
  },
  {
    "sc": "SEN",
    "en": "SENAPURA",
    "se": "KARNATAKA"
  },
  {
    "sc": "SCE",
    "en": "SENCHOA JN",
    "se": "ASSAM"
  },
  {
    "sc": "SEU",
    "en": "SENDRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SNDI",
    "en": "SENDURAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SCT",
    "en": "SENGOTTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SGLM",
    "en": "SENGULAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SEO",
    "en": "SEOHARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SEY",
    "en": "SEONI",
    "ec": "CHHINDWARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SHE",
    "en": "SEORAPHULI",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SEPN",
    "en": "SEPON",
    "se": "ASSAM"
  },
  {
    "sc": "SEM",
    "en": "SERAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "SRP",
    "en": "SERAMPORE",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SXR",
    "en": "SERNDANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SEX",
    "en": "SERONI ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "STH",
    "en": "SETHAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SF",
    "en": "SETTIGUNTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SET",
    "en": "SETTIHALLY",
    "se": "KARNATAKA"
  },
  {
    "sc": "SEGM",
    "en": "SEVAGRAM",
    "ec": "WARDHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SVL",
    "en": "SEVALIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "SVUR",
    "en": "SEVUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SVR",
    "en": "SEVVAPET ROAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SWNR",
    "en": "SEWA NAGAR",
    "se": "DELHI"
  },
  {
    "sc": "SWPR",
    "en": "SEWAPURI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SWAR",
    "en": "SEWAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SDNR",
    "en": "SEYDUNGANALLUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SJL",
    "en": "SGM JAGARLAMUDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SHDR",
    "en": "SHADHORAGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SHNR",
    "en": "SHADNAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "SDB",
    "en": "SHAHABAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "SMDP",
    "en": "SHAHABAD MD.PUR",
    "se": "DELHI"
  },
  {
    "sc": "SHAD",
    "en": "SHAHAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SMG",
    "en": "SHAHAMATGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SHDM",
    "en": "SHAHBAD MARKNDA",
    "se": "HARYANA"
  },
  {
    "sc": "SBK",
    "en": "SHAHBAZ KULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SZN",
    "en": "SHAHBAZNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SDL",
    "en": "SHAHDOL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SHRA",
    "en": "SHAHERA",
    "se": "GUJARAT"
  },
  {
    "sc": "SHG",
    "en": "SHAHGANJ JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SG",
    "en": "SHAHGARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SSC",
    "en": "SHAHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SZP",
    "en": "SHAHJAHANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SPN",
    "en": "SHAHJEHANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SWW",
    "en": "SHAHNAGAR TMNS",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SPP",
    "en": "SHAHPUR PATOREE",
    "se": "BIHAR"
  },
  {
    "sc": "SAR",
    "en": "SHAHZAD NAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "STSN",
    "en": "SHAITANSINGHNGR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SXK",
    "en": "SHAJAHANPURCORT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SFY",
    "en": "SHAJAPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SKNR",
    "en": "SHAKAR NAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "SKTN",
    "en": "SHAKTI NAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SSB",
    "en": "SHAKURBASTI",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "SHLT",
    "en": "SHALASHAH THANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SHM",
    "en": "SHALIMAR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SCQ",
    "en": "SHAM CHAURASI",
    "se": "PUNJAB"
  },
  {
    "sc": "SMKR",
    "en": "SHAM KAURIA",
    "se": "BIHAR"
  },
  {
    "sc": "SMP",
    "en": "SHAMBHUPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SGZ",
    "en": "SHAMGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SJS",
    "en": "SHAMLAJI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "SMQL",
    "en": "SHAMLI",
    "ec": "SAHARANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SPHL",
    "en": "SHAMPURHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SSD",
    "en": "SHAMSABAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SSDT",
    "en": "SHAMSHABAD TOWN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SBTJ",
    "en": "SHANIDEV D SBTJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SQK",
    "en": "SHANKAR",
    "se": "PUNJAB"
  },
  {
    "sc": "SRJ",
    "en": "SHANKARGARH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SKP",
    "en": "SHANKARPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "SKLP",
    "en": "SHANKARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SHKL",
    "en": "SHANKRUL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SIGA",
    "en": "SHANTIGRAMA",
    "se": "KARNATAKA"
  },
  {
    "sc": "STB",
    "en": "SHANTIPUR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SHH",
    "en": "SHAPUR JN",
    "se": "GUJARAT"
  },
  {
    "sc": "SHRM",
    "en": "SHARMA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SSRD",
    "en": "SHASAN ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SAS",
    "en": "SHDSPRA PADMPRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SED",
    "en": "SHEDBAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "SDBR",
    "en": "SHEDUBHAR",
    "se": "GUJARAT"
  },
  {
    "sc": "SEG",
    "en": "SHEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SKW",
    "en": "SHEIKHUPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SHK",
    "en": "SHEIKPURA",
    "se": "BIHAR"
  },
  {
    "sc": "SLGH",
    "en": "SHELGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SEI",
    "en": "SHENDRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SDRN",
    "en": "SHENDURNI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SNE",
    "en": "SHENOLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SHNX",
    "en": "SHEO SINGH PURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SPDR",
    "en": "SHEOPRASADNAGER",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SOE",
    "en": "SHEOPUR KALAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SRKN",
    "en": "SHEREKAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SNZ",
    "en": "SHERGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SGA",
    "en": "SHERGARH",
    "se": "PUNJAB"
  },
  {
    "sc": "SEPR",
    "en": "SHERPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SHBL",
    "en": "SHIBLUN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SKY",
    "en": "SHIKARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SKB",
    "en": "SHIKOHABAD JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SOC",
    "en": "SHILLONG O A"
  },
  {
    "sc": "SMLG",
    "en": "SHIMILIAGUDA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "BEI",
    "en": "SHIMOGA BIDARE",
    "se": "KARNATAKA"
  },
  {
    "sc": "SHIV",
    "en": "SHINDAWANE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SXH",
    "en": "SHINGATGERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SHMI",
    "en": "SHIROOR",
    "se": "KARNATAKA"
  },
  {
    "sc": "SIW",
    "en": "SHIRRAVDE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SS",
    "en": "SHIRSOLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SHF",
    "en": "SHIRUD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SRVA",
    "en": "SHIRVA",
    "se": "GUJARAT"
  },
  {
    "sc": "SHEO",
    "en": "SHISHO",
    "se": "BIHAR"
  },
  {
    "sc": "SSG",
    "en": "SHIU SAGAR ROAD",
    "se": "BIHAR"
  },
  {
    "sc": "SOP",
    "en": "SHIUPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "CSB",
    "en": "SHIVAJI BRIDGE",
    "se": "DELHI"
  },
  {
    "sc": "SVJR",
    "en": "SHIVAJINAGAR",
    "ec": "PUNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SLPM",
    "en": "SHIVALINGAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SME",
    "en": "SHIVAMOGGA H",
    "se": "KARNATAKA"
  },
  {
    "sc": "SMET",
    "en": "SHIVAMOGGA TOWN",
    "ec": "SHIVAMOGGA TOWN",
    "se": "KARNATAKA"
  },
  {
    "sc": "SVRP",
    "en": "SHIVANARAYANPUR",
    "se": "BIHAR"
  },
  {
    "sc": "SHV",
    "en": "SHIVANI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SVTN",
    "en": "SHIVATHAN",
    "se": "KARNATAKA"
  },
  {
    "sc": "SIA",
    "en": "SHIVLANKHA",
    "se": "GUJARAT"
  },
  {
    "sc": "SHNG",
    "en": "SHIVNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SVW",
    "en": "SHIVNI SHIVAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SVT",
    "en": "SHIVPURA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SVPI",
    "en": "SHIVPURI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SVU",
    "en": "SHIVRAJPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "SWC",
    "en": "SHIVRAMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SWT",
    "en": "SHIVWALA TEHU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SVDK",
    "en": "SHMATA VD KATRA",
    "ec": "Jammu",
    "se": "JAMMU AND KASHMIR",
    "tg": "VAISHNODEVI"
  },
  {
    "sc": "SXS",
    "en": "SHOBHASAN",
    "se": "GUJARAT"
  },
  {
    "sc": "SGS",
    "en": "SHOGHI",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "SOT",
    "en": "SHOHRATGARH",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SHLK",
    "en": "SHOLAKA",
    "se": "HARYANA"
  },
  {
    "sc": "SDN",
    "en": "SHOLAVANDAN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SHU",
    "en": "SHOLINGHUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SRR",
    "en": "SHORANUR JN",
    "se": "KERALA"
  },
  {
    "sc": "SBGA",
    "en": "SHRAVANBELAGOLA",
    "se": "KARNATAKA"
  },
  {
    "sc": "SIM",
    "en": "SHRI AMIRGADH",
    "se": "GUJARAT"
  },
  {
    "sc": "SBLJ",
    "en": "SHRI BALAJI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SBHN",
    "en": "SHRI BHAVNATH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SGNR",
    "en": "SHRI GANGANAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SHGN",
    "en": "SHRI GHASINAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SRW",
    "en": "SHRI KARANPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SMPR",
    "en": "SHRI MADHOPUR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SMVJ",
    "en": "SHRI MAHAVEERJI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SHRG",
    "en": "SHRI RAMGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SBNR",
    "en": "SHRI VIJAINAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SBLT",
    "en": "SHRIBDRYA LATHI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SRID",
    "en": "SHRIDHAM",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SGND",
    "en": "SHRIGONDA ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SKPA",
    "en": "SHRIKALYANPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SIZ",
    "en": "SHRIKHANDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SRDW",
    "en": "SHRIMAD DWKPURI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SPS",
    "en": "SHRIPAT SHRKHND",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SAGR",
    "en": "SHRIRAJNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "S",
    "en": "SHRIRANGAPATNA",
    "se": "KARNATAKA"
  },
  {
    "sc": "SVGL",
    "en": "SHRIVAGILU",
    "se": "KARNATAKA"
  },
  {
    "sc": "SUP",
    "en": "SHRUNGAVARPUKTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SPPR",
    "en": "SHUDNIPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SJT",
    "en": "SHUJAATPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SJP",
    "en": "SHUJALPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SHX",
    "en": "SHUKARULLAHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SMCK",
    "en": "SHYAM CHAK",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SNR",
    "en": "SHYAMNAGAR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SMPA",
    "en": "SHYAMPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SHMR",
    "en": "SHYAMSUNDER",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SWJ",
    "en": "SIAJULI",
    "se": "ASSAM"
  },
  {
    "sc": "SHBC",
    "en": "SIBAICHANDI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SRTN",
    "en": "SIBSAGAR TOWN",
    "ec": "SIMALUGURI",
    "se": "ASSAM"
  },
  {
    "sc": "SIE",
    "en": "SIDDAMPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SIDG",
    "en": "SIDDAPUR GRAMA",
    "se": "KARNATAKA"
  },
  {
    "sc": "SIDP",
    "en": "SIDDAPUR H",
    "se": "KARNATAKA"
  },
  {
    "sc": "SDDN",
    "en": "SIDDHARTH NAGAR",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SID",
    "en": "SIDDHPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "SIPT",
    "en": "SIDDIPET",
    "se": "TELANGANA"
  },
  {
    "sc": "SD",
    "en": "SIDHAULI",
    "ec": "SITAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SDHS",
    "en": "SIDHIRSAI",
    "se": "JHARKHAND"
  },
  {
    "sc": "SQW",
    "en": "SIDHWALIA",
    "se": "BIHAR"
  },
  {
    "sc": "SWG",
    "en": "SIDHWAN",
    "se": "PUNJAB"
  },
  {
    "sc": "IDT",
    "en": "SIDLAGATTA",
    "se": "KARNATAKA"
  },
  {
    "sc": "SDMK",
    "en": "SIDMUKH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SXD",
    "en": "SIDULI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SGDM",
    "en": "SIGADAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SQS",
    "en": "SIGSIGI",
    "se": "JHARKHAND"
  },
  {
    "sc": "SIPR",
    "en": "SIHAPAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SIHO",
    "en": "SIHO",
    "se": "BIHAR"
  },
  {
    "sc": "SOJN",
    "en": "SIHOR GUJARAT",
    "se": "GUJARAT"
  },
  {
    "sc": "SHR",
    "en": "SIHORA ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SIJU",
    "en": "SIJU",
    "se": "ODISHA"
  },
  {
    "sc": "SJA",
    "en": "SIJUA",
    "se": "JHARKHAND"
  },
  {
    "sc": "SKQ",
    "en": "SIKANDARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SKA",
    "en": "SIKANDRA RAO",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SIKR",
    "en": "SIKAR JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SKIP",
    "en": "SIKARIPARA",
    "se": "JHARKHAND"
  },
  {
    "sc": "SKPI",
    "en": "SIKARPAI",
    "se": "ODISHA"
  },
  {
    "sc": "SKPR",
    "en": "SIKARPUR P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SFK",
    "en": "SIKIR",
    "se": "ODISHA"
  },
  {
    "sc": "SIKA",
    "en": "SIKKA",
    "se": "GUJARAT"
  },
  {
    "sc": "SKK",
    "en": "SIKKAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SKSO",
    "en": "SIKOSA P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SKU",
    "en": "SIKRODA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SIKD",
    "en": "SIKRODA KWANRI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "STF",
    "en": "SIKTA",
    "se": "BIHAR"
  },
  {
    "sc": "ILA",
    "en": "SILAIMAN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SZY",
    "en": "SILAK JHORI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SOB",
    "en": "SILANIBARI",
    "se": "ASSAM"
  },
  {
    "sc": "SILO",
    "en": "SILAO",
    "se": "BIHAR"
  },
  {
    "sc": "SPTR",
    "en": "SILAPATHAR",
    "se": "ASSAM"
  },
  {
    "sc": "SILR",
    "en": "SILARI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SLT",
    "en": "SILAUT",
    "se": "BIHAR"
  },
  {
    "sc": "SLWR",
    "en": "SILAWAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SCL",
    "en": "SILCHAR",
    "se": "ASSAM"
  },
  {
    "sc": "SHTT",
    "en": "SILGHAT TOWN",
    "se": "ASSAM"
  },
  {
    "sc": "SLH",
    "en": "SILIARI",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SGUD",
    "en": "SILIGURI"
  },
  {
    "sc": "SGUJ",
    "en": "SILIGURI JN",
    "ec": "NEW JALPAIGURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SGUT",
    "en": "SILIGURI TOWN",
    "ec": "NEW JALPAIGURI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SLTH",
    "en": "SILLAKKUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SLF",
    "en": "SILLI",
    "se": "JHARKHAND"
  },
  {
    "sc": "SPRA",
    "en": "SILLIPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SILP",
    "en": "SILPARA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SLGR",
    "en": "SIMALUGURI JN",
    "ec": "SIMALUGURI",
    "se": "ASSAM"
  },
  {
    "sc": "SMTL",
    "en": "SIMARIATAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SMBL",
    "en": "SIMBHOOLI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SMCP",
    "en": "SIMEN CHAPARI",
    "se": "ASSAM"
  },
  {
    "sc": "SCM",
    "en": "SIMHACHALAM",
    "ec": "VISAKHAPATNAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SML",
    "en": "SIMLA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "SLG",
    "en": "SIMLAGARH",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SMDR",
    "en": "SIMODARA",
    "se": "GUJARAT"
  },
  {
    "sc": "SMH",
    "en": "SIMRAHA",
    "se": "BIHAR"
  },
  {
    "sc": "STL",
    "en": "SIMULTALA",
    "ec": "ASANSOL & DEOGHAR",
    "se": "BIHAR"
  },
  {
    "sc": "SMX",
    "en": "SIMURALI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SYE",
    "en": "SINDEWAHI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SNNR",
    "en": "SINDHANUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "SDZ",
    "en": "SINDHAR",
    "se": "PUNJAB"
  },
  {
    "sc": "SDD",
    "en": "SINDHAWADAR",
    "se": "GUJARAT"
  },
  {
    "sc": "SNDD",
    "en": "SINDHUDURG",
    "ec": "RATNAGIRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SNI",
    "en": "SINDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SNK",
    "en": "SINDKHEDA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SDPN",
    "en": "SINDPAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SDBH",
    "en": "SINDRIBLOCK HUT",
    "se": "JHARKHAND"
  },
  {
    "sc": "SYW",
    "en": "SINDURWA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SHI",
    "en": "SINGANALLUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SKL",
    "en": "SINGAPERUMLKOIL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SPRD",
    "en": "SINGAPURAM ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "SGRM",
    "en": "SINGARAM",
    "se": "ODISHA"
  },
  {
    "sc": "SKM",
    "en": "SINGARAYAKONDA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SYI",
    "en": "SINGARENI COLRS"
  },
  {
    "sc": "SNPR",
    "en": "SINGARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SQB",
    "en": "SINGHABAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SGRP",
    "en": "SINGHIRAMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SNGI",
    "en": "SINGHNALI",
    "se": "GUJARAT"
  },
  {
    "sc": "SIPA",
    "en": "SINGHOOKHARIA",
    "se": "JHARKHAND"
  },
  {
    "sc": "SNGP",
    "en": "SINGHPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SPDM",
    "en": "SINGHPUR DUMRA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SGRL",
    "en": "SINGRAULI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SIU",
    "en": "SINGUR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SGW",
    "en": "SINGWAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SYQ",
    "en": "SINHAN",
    "se": "GUJARAT"
  },
  {
    "sc": "SINI",
    "en": "SINI JN",
    "se": "JHARKHAND"
  },
  {
    "sc": "SINR",
    "en": "SINOR",
    "se": "GUJARAT"
  },
  {
    "sc": "SPYA",
    "en": "SIPAYA",
    "se": "BIHAR"
  },
  {
    "sc": "SRJN",
    "en": "SIRAJNAGAR  H",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SRY",
    "en": "SIRARI",
    "se": "BIHAR"
  },
  {
    "sc": "SRAS",
    "en": "SIRAS",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SRO",
    "en": "SIRATHU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SIRD",
    "en": "SIRD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SIRA",
    "en": "SIRHILTARA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SIR",
    "en": "SIRHIND JN",
    "se": "PUNJAB"
  },
  {
    "sc": "SRPM",
    "en": "SIRIPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SRJM",
    "en": "SIRJAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SY",
    "en": "SIRKAZHI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SIF",
    "en": "SIRLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SRMT",
    "en": "SIRMUTTRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SCP",
    "en": "SIRNAPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "SOH",
    "en": "SIROHI ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SYO",
    "en": "SIROLIYA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SKZR",
    "en": "SIRPUR KAGAZNGR",
    "se": "TELANGANA"
  },
  {
    "sc": "SRUR",
    "en": "SIRPUR TOWN",
    "se": "TELANGANA"
  },
  {
    "sc": "SIRN",
    "en": "SIRRAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SIY",
    "en": "SIRRI P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SSA",
    "en": "SIRSA",
    "se": "HARYANA"
  },
  {
    "sc": "SSL",
    "en": "SIRSAUL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SRMP",
    "en": "SIRSI MUKHDUMPR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SSF",
    "en": "SIRSUPHAL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SRVT",
    "en": "SIRUVATTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SSKA",
    "en": "SISARKA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SISN",
    "en": "SISAUNA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SBGN",
    "en": "SISIBARGAON",
    "se": "ASSAM"
  },
  {
    "sc": "SVHE",
    "en": "SISVINHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SBZ",
    "en": "SISWA BAZAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "STBJ",
    "en": "SITABINJ",
    "se": "ODISHA"
  },
  {
    "sc": "STPD",
    "en": "SITAFAL MANDI",
    "se": "TELANGANA"
  },
  {
    "sc": "STNR",
    "en": "SITALNAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "STLR",
    "en": "SITALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "STLB",
    "en": "SITALPUR BENGAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SMI",
    "en": "SITAMARHI",
    "se": "BIHAR"
  },
  {
    "sc": "STPT",
    "en": "SITAMPET",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SNM",
    "en": "SITANAGARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "STP",
    "en": "SITAPUR",
    "ec": "SITAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SCC",
    "en": "SITAPUR CANT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SPC",
    "en": "SITAPUR CITY",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SPRM",
    "en": "SITAPURAM",
    "se": "ODISHA"
  },
  {
    "sc": "STN",
    "en": "SITARAMPUR",
    "ec": "ASANSOL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SEV",
    "en": "SITHALAVAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "STLI",
    "en": "SITHOULI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SII",
    "en": "SITIMANI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SURI",
    "en": "SIURI",
    "ec": "ANDAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SVDC",
    "en": "SIVADEVUNICHKLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SZV",
    "en": "SIVADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SVGA",
    "en": "SIVAGANGA",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SVKS",
    "en": "SIVAKASI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SPV",
    "en": "SIVAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "SVK",
    "en": "SIVARAKOTTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SVQ",
    "en": "SIVOK",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SVN",
    "en": "SIVUNGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SWDE",
    "en": "SIWAHA",
    "se": "HARYANA"
  },
  {
    "sc": "SWE",
    "en": "SIWAITH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SV",
    "en": "SIWAN JN",
    "se": "BIHAR"
  },
  {
    "sc": "SVC",
    "en": "SIWAN KACHARI",
    "se": "BIHAR"
  },
  {
    "sc": "SWNI",
    "en": "SIWANI",
    "se": "HARYANA"
  },
  {
    "sc": "SBD",
    "en": "SLEEMANABAD RD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SMVB",
    "en": "SMVT BENGALURU",
    "se": "KARNATAKA",
    "tg": "BANGALORE"
  },
  {
    "sc": "SNC",
    "en": "SNARAYAN CHAPIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SFZ",
    "en": "SNDRYA KACHARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SXF",
    "en": "SOBHAPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SEP",
    "en": "SODPUR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SGAC",
    "en": "SOGARIA",
    "ec": "KOTA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SOGR",
    "en": "SOGRA",
    "se": "ODISHA"
  },
  {
    "sc": "SGP",
    "en": "SOHAGPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SOHL",
    "en": "SOHAL",
    "se": "PUNJAB"
  },
  {
    "sc": "SAWN",
    "en": "SOHANSRA",
    "se": "HARYANA"
  },
  {
    "sc": "SLW",
    "en": "SOHWAL",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SOD",
    "en": "SOJAT ROAD",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SJTR",
    "en": "SOJITRA",
    "se": "GUJARAT"
  },
  {
    "sc": "SOZ",
    "en": "SOLADI",
    "se": "GUJARAT"
  },
  {
    "sc": "SOL",
    "en": "SOLAN",
    "ec": "KALKA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "SBY",
    "en": "SOLAN BREWERY",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "SURM",
    "en": "SOLAPUR JN"
  },
  {
    "sc": "SPWI",
    "en": "SOLAPURWADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SLZ",
    "en": "SOLARI",
    "se": "ODISHA"
  },
  {
    "sc": "SDVL",
    "en": "SOLDEVANAHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SGM",
    "en": "SOLGAMPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SOLR",
    "en": "SOLUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "SLM",
    "en": "SOMALAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SKPT",
    "en": "SOMANAYAKKANPTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SMKT",
    "en": "SOMANKATTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SNO",
    "en": "SOMANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SOS",
    "en": "SOMESAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SMWA",
    "en": "SOMESHWARA",
    "se": "KARNATAKA"
  },
  {
    "sc": "SDV",
    "en": "SOMIDEVIPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SOM",
    "en": "SOMNA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SMNH",
    "en": "SOMNATH",
    "ec": "VERAVAL",
    "se": "GUJARAT"
  },
  {
    "sc": "SPT",
    "en": "SOMPETA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SOQ",
    "en": "SOMPUR ROAD",
    "se": "KARNATAKA"
  },
  {
    "sc": "SOAE",
    "en": "SOMRA BAZAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SMNE",
    "en": "SOMTANE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SMTN",
    "en": "SOMTHAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SEB",
    "en": "SON NAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "SNAP",
    "en": "SONA ARJUNPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SAD",
    "en": "SONADA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SVH",
    "en": "SONADANGA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SOR",
    "en": "SONAGIR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SYZ",
    "en": "SONAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SI",
    "en": "SONAILI",
    "se": "BIHAR"
  },
  {
    "sc": "SXN",
    "en": "SONAKHAN",
    "se": "ODISHA"
  },
  {
    "sc": "SONA",
    "en": "SONAMUKHI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SZE",
    "en": "SONARDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "SOI",
    "en": "SONARIPUR"
  },
  {
    "sc": "SPR",
    "en": "SONARPUR JN",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SNSN",
    "en": "SONASAN",
    "se": "GUJARAT"
  },
  {
    "sc": "SBM",
    "en": "SONBARSA KCHERI",
    "se": "BIHAR"
  },
  {
    "sc": "SBDR",
    "en": "SONBHADRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SNV",
    "en": "SONDAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SXC",
    "en": "SONDALIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SCN",
    "en": "SONDHA ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SND",
    "en": "SONDIMRA",
    "se": "JHARKHAND"
  },
  {
    "sc": "SNN",
    "en": "SONEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SNPU",
    "en": "SONEPUR",
    "se": "ODISHA"
  },
  {
    "sc": "SGD",
    "en": "SONGADH",
    "se": "GUJARAT"
  },
  {
    "sc": "SONI",
    "en": "SONI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SIC",
    "en": "SONIK",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SNP",
    "en": "SONIPAT",
    "se": "HARYANA"
  },
  {
    "sc": "SEE",
    "en": "SONPUR JN",
    "se": "BIHAR"
  },
  {
    "sc": "SNSL",
    "en": "SONSHELU",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SQL",
    "en": "SONTALAI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SNTH",
    "en": "SONTHALIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SWR",
    "en": "SONUA",
    "se": "JHARKHAND"
  },
  {
    "sc": "SNBR",
    "en": "SONUABARI",
    "se": "ASSAM"
  },
  {
    "sc": "SWO",
    "en": "SONWARA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "SRTE",
    "en": "SOOROTHEE",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SXZM",
    "en": "SOPORE",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "WTS",
    "en": "SORATH VANTHIL",
    "se": "GUJARAT"
  },
  {
    "sc": "SBE",
    "en": "SORBHOG",
    "se": "ASSAM"
  },
  {
    "sc": "SORO",
    "en": "SORO",
    "se": "ODISHA"
  },
  {
    "sc": "SRNK",
    "en": "SORON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SPQ",
    "en": "SORUPETA",
    "se": "ASSAM"
  },
  {
    "sc": "SRVN",
    "en": "SRAVANUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "SDGH",
    "en": "SRI DUNGARGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "KHT",
    "en": "SRI KALAHASTI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "CHE",
    "en": "SRIKAKULAM ROAD",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SXO",
    "en": "SRIKONA",
    "se": "ASSAM"
  },
  {
    "sc": "SKN",
    "en": "SRIKRISHN NAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SNAR",
    "en": "SRINAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SINA",
    "en": "SRINAGAR",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "SHAN",
    "en": "SRINIVASA NAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "SVS",
    "en": "SRINIVASAPURA",
    "se": "KARNATAKA"
  },
  {
    "sc": "SRPN",
    "en": "SRIPANI",
    "se": "ASSAM"
  },
  {
    "sc": "SPGN",
    "en": "SRIPURIAGAON",
    "se": "ASSAM"
  },
  {
    "sc": "SRNM",
    "en": "SRIRAMANAGAR H",
    "se": "KARNATAKA"
  },
  {
    "sc": "SRNR",
    "en": "SRIRAMNAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "SRPB",
    "en": "SRIRAMPUR ASSAM",
    "se": "ASSAM"
  },
  {
    "sc": "SRMR",
    "en": "SRIRAMPURAM",
    "se": "TELANGANA"
  },
  {
    "sc": "SRGM",
    "en": "SRIRANGAM",
    "ec": "TIRUCHCHIRAPALI/SRIRANGAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SVV",
    "en": "SRIVAIKUNTAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SVPR",
    "en": "SRIVILLIPUTTUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SGKM",
    "en": "SRUNGAVRUKSHAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "STM",
    "en": "ST THOMAS MOUNT",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SPF",
    "en": "STUARTPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SXQ",
    "en": "SUAHERI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SUZ",
    "en": "SUBANSIRI",
    "se": "ASSAM"
  },
  {
    "sc": "SBNM",
    "en": "SUBARNAMRIGI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SFG",
    "en": "SUBEDARGANJ",
    "ec": "PRAYAGRAJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SUBR",
    "en": "SUBHAGPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SBGR",
    "en": "SUBHAS GRAM",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SBHR",
    "en": "SUBRAHMANYA RD",
    "se": "KARNATAKA"
  },
  {
    "sc": "SZM",
    "en": "SUBZI MANDI",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "SHN",
    "en": "SUCHAN KOTLI",
    "se": "HARYANA"
  },
  {
    "sc": "SDMD",
    "en": "SUDAMDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "SUD",
    "en": "SUDHANI",
    "se": "BIHAR"
  },
  {
    "sc": "SDRA",
    "en": "SUDHRANA",
    "se": "HARYANA"
  },
  {
    "sc": "SUX",
    "en": "SUDIYUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SDF",
    "en": "SUDSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SGPA",
    "en": "SUGAPAHARI HALT",
    "se": "JHARKHAND"
  },
  {
    "sc": "SOW",
    "en": "SUHSARAI",
    "se": "BIHAR"
  },
  {
    "sc": "SUI",
    "en": "SUI",
    "se": "HARYANA"
  },
  {
    "sc": "SSIA",
    "en": "SUISA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SJPA",
    "en": "SUJALPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SUJH",
    "en": "SUJANGARH",
    "se": "RAJASTHAN",
    "tg": "SALASAR BALAJI"
  },
  {
    "sc": "SJNP",
    "en": "SUJANPUR",
    "se": "PUNJAB"
  },
  {
    "sc": "SPLE",
    "en": "SUJNIPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SUJR",
    "en": "SUJRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SCV",
    "en": "SUKHCHAIN",
    "se": "HARYANA"
  },
  {
    "sc": "SUW",
    "en": "SUKHISEWANIYAN",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SKHV",
    "en": "SUKHOVI",
    "se": "NAGALAND"
  },
  {
    "sc": "SRHA",
    "en": "SUKHPAR ROHA",
    "se": "GUJARAT"
  },
  {
    "sc": "SUKP",
    "en": "SUKHPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "SKND",
    "en": "SUKINDA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "SKLI",
    "en": "SUKLI P H",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SN",
    "en": "SUKNA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SOY",
    "en": "SUKRIMANGELA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SQF",
    "en": "SUKRITIPUR",
    "se": "ASSAM"
  },
  {
    "sc": "SUKU",
    "en": "SUKU",
    "se": "ODISHA"
  },
  {
    "sc": "SUL",
    "en": "SULADHAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "SLHP",
    "en": "SULAH HMCHL PDH",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "SBH",
    "en": "SULEBHAVI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SUH",
    "en": "SULEHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SLGE",
    "en": "SULERJAVALGE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SGRE",
    "en": "SULGARE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SULH",
    "en": "SULHANI",
    "se": "PUNJAB"
  },
  {
    "sc": "SIKI",
    "en": "SULIKERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SPE",
    "en": "SULLURUPETA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SGG",
    "en": "SULTANGANJ",
    "ec": "BHAGALPUR",
    "se": "BIHAR"
  },
  {
    "sc": "SLN",
    "en": "SULTANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SLNK",
    "en": "SULTANPUR KARNA",
    "se": "KARNATAKA"
  },
  {
    "sc": "SQR",
    "en": "SULTANPUR LODI",
    "se": "PUNJAB"
  },
  {
    "sc": "SUU",
    "en": "SULUR ROAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SMBR",
    "en": "SUMBAR",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "SUMR",
    "en": "SUMER",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SUDV",
    "en": "SUMMADEVI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "SHZ",
    "en": "SUMMER HILL",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "SUM",
    "en": "SUMMIT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "SMRR",
    "en": "SUMRERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SUC",
    "en": "SUNAK"
  },
  {
    "sc": "SNKN",
    "en": "SUNAKHANI",
    "se": "ODISHA"
  },
  {
    "sc": "SFM",
    "en": "SUNAM",
    "se": "PUNJAB"
  },
  {
    "sc": "SFMU",
    "en": "SUNAM UDHAM S W",
    "se": "PUNJAB"
  },
  {
    "sc": "SPL",
    "en": "SUNDARAPRMLKOIL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SUND",
    "en": "SUNDARNA",
    "se": "GUJARAT"
  },
  {
    "sc": "SNBD",
    "en": "SUNDERABAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SDAM",
    "en": "SUNDHIAMAU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SDLK",
    "en": "SUNDLAK",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SNKE",
    "en": "SUNEHTI KHARKHR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SFF",
    "en": "SUNERA PIRKHERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SOU",
    "en": "SUPAUL",
    "se": "BIHAR"
  },
  {
    "sc": "SPD",
    "en": "SUPEDI",
    "se": "GUJARAT"
  },
  {
    "sc": "SAKD",
    "en": "SUPRAKANDI",
    "se": "ASSAM"
  },
  {
    "sc": "SZK",
    "en": "SUR KHAND KA KH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SORD",
    "en": "SUR ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "SRX",
    "en": "SURA NUSSI",
    "se": "PUNJAB"
  },
  {
    "sc": "SIP",
    "en": "SURAIMANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SUIA",
    "en": "SURAINCHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SRJK",
    "en": "SURAJ KUNDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SRGH",
    "en": "SURAJGARH",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SUPR",
    "en": "SURAJPUR",
    "se": "HARYANA"
  },
  {
    "sc": "SJQ",
    "en": "SURAJPUR ROAD",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "SU",
    "en": "SURAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SDM",
    "en": "SURAREDDIPALEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "STCB",
    "en": "SURAT CITY CB",
    "se": "GUJARAT"
  },
  {
    "sc": "SOG",
    "en": "SURATGARH JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SL",
    "en": "SURATHKAL",
    "ec": "UDUPI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SURP",
    "en": "SURATPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SRVX",
    "en": "SURAVALI",
    "se": "GOA"
  },
  {
    "sc": "SRBR",
    "en": "SURBARI",
    "se": "GUJARAT"
  },
  {
    "sc": "SURL",
    "en": "SURELI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SUNR",
    "en": "SURENDRANAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "SRGT",
    "en": "SURENDRANAGAR G",
    "se": "GUJARAT"
  },
  {
    "sc": "SRRG",
    "en": "SURER",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SURR",
    "en": "SURERA",
    "se": "HARYANA"
  },
  {
    "sc": "SGBJ",
    "en": "SURGAON BANJARI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SAW",
    "en": "SURIAWAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SJKL",
    "en": "SURJA KAMAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SJPR",
    "en": "SURJYAPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SLRD",
    "en": "SURLA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "SPO",
    "en": "SURPURA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SSKL",
    "en": "SUSKAL",
    "se": "GUJARAT"
  },
  {
    "sc": "SUT",
    "en": "SUTLANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "SWS",
    "en": "SUWANSA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SVA",
    "en": "SUWASRA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "SDLE",
    "en": "SWADINPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "SWPS",
    "en": "SWAMI PARAMHANS",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "SMLI",
    "en": "SWAMIHALLI",
    "se": "KARNATAKA"
  },
  {
    "sc": "SWI",
    "en": "SWAMIMALAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "SRPJ",
    "en": "SWARUPGANJ",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TADA",
    "en": "TADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TPY",
    "en": "TADAKALPUDI",
    "se": "TELANGANA"
  },
  {
    "sc": "TAE",
    "en": "TADALI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TDD",
    "en": "TADEPALLIGUDEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TU",
    "en": "TADIPATRI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TAA",
    "en": "TADLA PUSAPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "TDK",
    "en": "TADUKU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TVL",
    "en": "TADWAL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TID",
    "en": "TAGDI",
    "se": "GUJARAT"
  },
  {
    "sc": "THP",
    "en": "TAHERPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TSD",
    "en": "TAHSIL BHADRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TSF",
    "en": "TAHSIL FATEHPUR",
    "ec": "SITAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TBR",
    "en": "TAIABPUR",
    "se": "BIHAR"
  },
  {
    "sc": "TJH",
    "en": "TAJGADH",
    "se": "GUJARAT"
  },
  {
    "sc": "TJP",
    "en": "TAJPUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TJD",
    "en": "TAJPUR DEHMA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TAKL",
    "en": "TAKAL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TKR",
    "en": "TAKARI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TKHE",
    "en": "TAKARKHEDE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TKHA",
    "en": "TAKHA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TKF",
    "en": "TAKI ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TQA",
    "en": "TAKIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TKP",
    "en": "TAKIPUR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TKO",
    "en": "TAKKOLAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TKI",
    "en": "TAKLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TKLB",
    "en": "TAKLIBANSALI PH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TKMY",
    "en": "TAKLIMIYA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TSL",
    "en": "TAKSAL",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "TAKU",
    "en": "TAKU",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TABU",
    "en": "TALABURU",
    "se": "JHARKHAND"
  },
  {
    "sc": "TVS",
    "en": "TALAIVASAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TAY",
    "en": "TALAIYUTHU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TLKL",
    "en": "TALAKAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "TLKH",
    "en": "TALAKHAJURI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TAV",
    "en": "TALALA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "TMC",
    "en": "TALAMANCHI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TLNR",
    "en": "TALANALLUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TLO",
    "en": "TALANDU",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TLL",
    "en": "TALAP",
    "se": "ASSAM"
  },
  {
    "sc": "TLRA",
    "en": "TALARA",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "TLZ",
    "en": "TALAVLI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TBT",
    "en": "TALBAHAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TLHR",
    "en": "TALCHER",
    "ec": "TALCHAR ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "TLHD",
    "en": "TALCHER ROAD",
    "ec": "TALCHAR ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "TLC",
    "en": "TALCHHAPAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TLX",
    "en": "TALDI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TGN",
    "en": "TALEGAON",
    "ec": "PUNE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TLE",
    "en": "TALGARIA",
    "se": "JHARKHAND"
  },
  {
    "sc": "TLGP",
    "en": "TALGUPPA",
    "se": "KARNATAKA"
  },
  {
    "sc": "THJ",
    "en": "TALHERI BUZURG",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TIT",
    "en": "TALIT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TLJ",
    "en": "TALJHARI",
    "se": "JHARKHAND"
  },
  {
    "sc": "TALL",
    "en": "TALL JN",
    "se": "BIHAR"
  },
  {
    "sc": "TSS",
    "en": "TALLI SAIDASAHU",
    "se": "PUNJAB"
  },
  {
    "sc": "TMD",
    "en": "TALMADLA",
    "se": "TELANGANA"
  },
  {
    "sc": "TLMG",
    "en": "TALMADUGU",
    "se": "TELANGANA"
  },
  {
    "sc": "TLN",
    "en": "TALNI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TOD",
    "en": "TALOD",
    "se": "GUJARAT"
  },
  {
    "sc": "TUD",
    "en": "TALODHI ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TPND",
    "en": "TALOJA PANCHAND",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TLV",
    "en": "TALVADYA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TWB",
    "en": "TALWANDI",
    "se": "PUNJAB"
  },
  {
    "sc": "TLI",
    "en": "TALWARA JHIL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TMP",
    "en": "TAMARAIPADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TBMS",
    "en": "TAMBARAM SNTRM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TOI",
    "en": "TAMKUHI ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TMZ",
    "en": "TAMLUK",
    "ec": "HALDIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TAO",
    "en": "TAMNA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TMA",
    "en": "TAMURIA",
    "se": "BIHAR"
  },
  {
    "sc": "TKU",
    "en": "TANAKALLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TPU",
    "en": "TANAKPUR",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "TCA",
    "en": "TANCHHA",
    "se": "GUJARAT"
  },
  {
    "sc": "TD",
    "en": "TANDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TDO",
    "en": "TANDA URMAR",
    "se": "PUNJAB"
  },
  {
    "sc": "TNI",
    "en": "TANDARAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TXM",
    "en": "TANDAVAPURA",
    "se": "KARNATAKA"
  },
  {
    "sc": "TDU",
    "en": "TANDUR",
    "se": "TELANGANA"
  },
  {
    "sc": "TDW",
    "en": "TANDWAL",
    "se": "HARYANA"
  },
  {
    "sc": "TNGN",
    "en": "TANGANI",
    "se": "ASSAM"
  },
  {
    "sc": "TGB",
    "en": "TANGARBASULI",
    "se": "JHARKHAND"
  },
  {
    "sc": "TGM",
    "en": "TANGARMUNDA",
    "se": "ODISHA"
  },
  {
    "sc": "TGRL",
    "en": "TANGIRIAPAL",
    "se": "ODISHA"
  },
  {
    "sc": "TNL",
    "en": "TANGLA",
    "se": "ASSAM"
  },
  {
    "sc": "TRA",
    "en": "TANGRA",
    "se": "PUNJAB"
  },
  {
    "sc": "TNR",
    "en": "TANGUTURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TUJ",
    "en": "TANIJAN",
    "se": "ASSAM"
  },
  {
    "sc": "TNKA",
    "en": "TANKHALA",
    "se": "GUJARAT"
  },
  {
    "sc": "TKN",
    "en": "TANKUPPA",
    "se": "BIHAR"
  },
  {
    "sc": "TPO",
    "en": "TANTPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TNKU",
    "en": "TANUKU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TA",
    "en": "TANUR",
    "se": "KERALA"
  },
  {
    "sc": "TAPA",
    "en": "TAPA",
    "se": "PUNJAB"
  },
  {
    "sc": "TAP",
    "en": "TAPANG",
    "se": "ODISHA"
  },
  {
    "sc": "TOP",
    "en": "TAPASI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "THWM",
    "en": "TAPESHWARNATH D",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TPN",
    "en": "TAPONA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TPZ",
    "en": "TAPRI",
    "ec": "SAHARANPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TVI",
    "en": "TARADEVI",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "TNX",
    "en": "TARAK NAGAR",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TAK",
    "en": "TARAKESWAR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TRMN",
    "en": "TARAMANI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TAN",
    "en": "TARANA ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TRAH",
    "en": "TARANGA HILL",
    "se": "GUJARAT"
  },
  {
    "sc": "TRN",
    "en": "TARAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TRR",
    "en": "TARAORI",
    "se": "HARYANA"
  },
  {
    "sc": "TPF",
    "en": "TARAPITH ROAD",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TRP",
    "en": "TARAPUR JN",
    "se": "GUJARAT"
  },
  {
    "sc": "TRWT",
    "en": "TARAVATA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TBL",
    "en": "TARCHERRA BRLRM",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TEA",
    "en": "TAREGNA",
    "se": "BIHAR"
  },
  {
    "sc": "TAZ",
    "en": "TARGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TRJ",
    "en": "TARIASUJAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TRG",
    "en": "TARIGHAT",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TGU",
    "en": "TARIGOPPULA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TKE",
    "en": "TARIKERE JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "TLU",
    "en": "TARLUPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TTO",
    "en": "TARN TARAN",
    "se": "PUNJAB"
  },
  {
    "sc": "TRF",
    "en": "TAROPA",
    "se": "GUJARAT"
  },
  {
    "sc": "TRSR",
    "en": "TARSAI",
    "se": "GUJARAT"
  },
  {
    "sc": "TRS",
    "en": "TARSARAI",
    "se": "BIHAR"
  },
  {
    "sc": "TRW",
    "en": "TARSOD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TR",
    "en": "TARUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TRV",
    "en": "TARVA",
    "se": "GUJARAT"
  },
  {
    "sc": "TATI",
    "en": "TATI",
    "se": "JHARKHAND"
  },
  {
    "sc": "TBH",
    "en": "TATIBAHAR",
    "se": "ASSAM"
  },
  {
    "sc": "TAC",
    "en": "TATICHERLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TIS",
    "en": "TATISILWAI",
    "ec": "HATIA/RANCHI",
    "se": "JHARKHAND"
  },
  {
    "sc": "TIP",
    "en": "TATTAPPARAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TVG",
    "en": "TAVARGATTI",
    "se": "KARNATAKA"
  },
  {
    "sc": "TEO",
    "en": "TEEGAON",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TGA",
    "en": "TEGHRA",
    "se": "BIHAR"
  },
  {
    "sc": "TKA",
    "en": "TEHARKA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "THA",
    "en": "TEHTA",
    "se": "BIHAR"
  },
  {
    "sc": "TNPR",
    "en": "TEJNARAYANPUR",
    "se": "BIHAR"
  },
  {
    "sc": "TKBG",
    "en": "TEKKABIGHA",
    "se": "BIHAR"
  },
  {
    "sc": "TEK",
    "en": "TEKKALI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TQR",
    "en": "TEKTAR",
    "se": "BIHAR"
  },
  {
    "sc": "TQM",
    "en": "TELAM",
    "se": "ASSAM"
  },
  {
    "sc": "TOU",
    "en": "TELAPROLU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TLPR",
    "en": "TELAPUR JN",
    "se": "TELANGANA"
  },
  {
    "sc": "TELI",
    "en": "TELI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TELY",
    "en": "TELIA HALT",
    "se": "BIHAR"
  },
  {
    "sc": "TLMR",
    "en": "TELIAMURA",
    "se": "TRIPURA"
  },
  {
    "sc": "TLGI",
    "en": "TELIGI",
    "se": "KARNATAKA"
  },
  {
    "sc": "TELO",
    "en": "TELO",
    "se": "JHARKHAND"
  },
  {
    "sc": "TETA",
    "en": "TELTA",
    "se": "BIHAR"
  },
  {
    "sc": "TLB",
    "en": "TELWA BAZAR H",
    "se": "BIHAR"
  },
  {
    "sc": "TMB",
    "en": "TEMBURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TEP",
    "en": "TEMPA P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TV",
    "en": "TEN TALAV",
    "se": "GUJARAT"
  },
  {
    "sc": "TEL",
    "en": "TENALI JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TGQ",
    "en": "TENGANMADA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "TENI",
    "en": "TENI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TSI",
    "en": "TENKASI JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TML",
    "en": "TENMALAI",
    "se": "KERALA"
  },
  {
    "sc": "TNRU",
    "en": "TENNERU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TNJE",
    "en": "TENTULLA",
    "se": "JHARKHAND"
  },
  {
    "sc": "TYAE",
    "en": "TENYA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TTLA",
    "en": "TETELIA",
    "se": "ASSAM"
  },
  {
    "sc": "TTU",
    "en": "TETTU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TET",
    "en": "TETULMARI",
    "se": "JHARKHAND"
  },
  {
    "sc": "TZTB",
    "en": "TEZPORE",
    "ec": "DEKARGAON"
  },
  {
    "sc": "TYK",
    "en": "THABALKE",
    "se": "PUNJAB"
  },
  {
    "sc": "THY",
    "en": "THADI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "THTW",
    "en": "THAILIK TWISA",
    "se": "TRIPURA"
  },
  {
    "sc": "TER",
    "en": "THAIR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TKG",
    "en": "THAKURGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "TKC",
    "en": "THAKURKUCHI",
    "se": "ASSAM"
  },
  {
    "sc": "THK",
    "en": "THAKURLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TKNR",
    "en": "THAKURNAGAR",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TKH",
    "en": "THAKURTOTA",
    "se": "ODISHA"
  },
  {
    "sc": "TUG",
    "en": "THALANGAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TLY",
    "en": "THALASSERY",
    "se": "KERALA"
  },
  {
    "sc": "THEA",
    "en": "THALERA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "THKU",
    "en": "THALLAK",
    "se": "KARNATAKA"
  },
  {
    "sc": "TLWA",
    "en": "THALWARA",
    "se": "BIHAR"
  },
  {
    "sc": "THM",
    "en": "THALYAT HAMIRA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TMGN",
    "en": "THAMLA MOGANA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "THAN",
    "en": "THAN JN",
    "se": "GUJARAT"
  },
  {
    "sc": "THBN",
    "en": "THANA BHAWAN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TBTN",
    "en": "THANA BHAWAN TN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "THB",
    "en": "THANA BIHPUR JN",
    "se": "BIHAR"
  },
  {
    "sc": "THDR",
    "en": "THANDLA RD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TGDE",
    "en": "THANGUNDI",
    "se": "KARNATAKA"
  },
  {
    "sc": "TJ",
    "en": "THANJAVUR JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TNW",
    "en": "THAPAR NAGAR",
    "se": "JHARKHAND"
  },
  {
    "sc": "TBU",
    "en": "THARBAN",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TB",
    "en": "THARBITIA",
    "se": "BIHAR"
  },
  {
    "sc": "TAR",
    "en": "THARSA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "THW",
    "en": "THARWAI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TAS",
    "en": "THASRA",
    "se": "GUJARAT"
  },
  {
    "sc": "THMR",
    "en": "THATHANA MITHRI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TTQ",
    "en": "THATHANKULAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "THE",
    "en": "THAWE JN",
    "ec": "SIWAN",
    "se": "BIHAR"
  },
  {
    "sc": "TQL",
    "en": "THEH QALANDAR",
    "se": "PUNJAB"
  },
  {
    "sc": "TGE",
    "en": "THEKERAGURI",
    "se": "ASSAM"
  },
  {
    "sc": "THV",
    "en": "THERUBALI",
    "se": "ODISHA"
  },
  {
    "sc": "TGBP",
    "en": "THINGOU",
    "se": "MANIPUR"
  },
  {
    "sc": "TPPI",
    "en": "THIPPARTHI",
    "se": "TELANGANA"
  },
  {
    "sc": "TASA",
    "en": "THIPPASANDRA",
    "se": "KARNATAKA"
  },
  {
    "sc": "MTMY",
    "en": "THIRUMAYILAI",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TUY",
    "en": "THIRUTHURAIYUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TVR",
    "en": "THIRUVARUR JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "THVM",
    "en": "THIVIM",
    "ec": "MADGAON",
    "se": "GOA"
  },
  {
    "sc": "TOK",
    "en": "THOKUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "TDV",
    "en": "THONDEBHAVI",
    "se": "KARNATAKA"
  },
  {
    "sc": "TNGR",
    "en": "THONGANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "THUR",
    "en": "THURIA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TWV",
    "en": "THUWAVI",
    "se": "GUJARAT"
  },
  {
    "sc": "TIBI",
    "en": "TIBI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TIHU",
    "en": "TIHU",
    "se": "ASSAM"
  },
  {
    "sc": "TIK",
    "en": "TIK",
    "se": "HARYANA"
  },
  {
    "sc": "TKMG",
    "en": "TIKAMGARH",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TKLE",
    "en": "TIKANI",
    "se": "BIHAR"
  },
  {
    "sc": "TKYR",
    "en": "TIKARIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TKRP",
    "en": "TIKAULI RAWATPR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TKWD",
    "en": "TIKEKARWADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TPKR",
    "en": "TIKIAPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TKRI",
    "en": "TIKIRI",
    "se": "ODISHA"
  },
  {
    "sc": "TKT",
    "en": "TIKKOTTI",
    "se": "KERALA"
  },
  {
    "sc": "TKRA",
    "en": "TIKRA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TRE",
    "en": "TIKRI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TQN",
    "en": "TIKUNIA",
    "ec": "LAKHIMPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TILA",
    "en": "TILA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TAM",
    "en": "TILAIVILAGAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TKJ",
    "en": "TILAK BRIDGE",
    "se": "DELHI"
  },
  {
    "sc": "TIU",
    "en": "TILARU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TLT",
    "en": "TILATI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TLNH",
    "en": "TILAUNCHI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TIA",
    "en": "TILAYA",
    "se": "BIHAR"
  },
  {
    "sc": "TBB",
    "en": "TILBHITA",
    "se": "JHARKHAND"
  },
  {
    "sc": "TBX",
    "en": "TILBHUM",
    "se": "ASSAM"
  },
  {
    "sc": "TLD",
    "en": "TILDA NEORA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "TDLE",
    "en": "TILDANGA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TLH",
    "en": "TILHAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TL",
    "en": "TILONIYA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TIL",
    "en": "TILRATH",
    "se": "BIHAR"
  },
  {
    "sc": "TWL",
    "en": "TILWARA",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TBN",
    "en": "TIMARNI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TBA",
    "en": "TIMBA ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "TBV",
    "en": "TIMBARVA",
    "se": "GUJARAT"
  },
  {
    "sc": "TIC",
    "en": "TIMMACHIPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TIM",
    "en": "TIMMANACHERLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TMX",
    "en": "TIMMAPUR",
    "se": "TELANGANA"
  },
  {
    "sc": "TMPM",
    "en": "TIMMAPURAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TMT",
    "en": "TIMTALA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TMH",
    "en": "TIN MILE HAT",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TGT",
    "en": "TINAI GHAT",
    "se": "KARNATAKA"
  },
  {
    "sc": "TNUE",
    "en": "TINDAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TDH",
    "en": "TINDHARIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TMV",
    "en": "TINDIVANAM",
    "ec": "PONDICHERRY/PUDUCHERRY",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TII",
    "en": "TINGRAI",
    "se": "ASSAM"
  },
  {
    "sc": "TH",
    "en": "TINICH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TNH",
    "en": "TINKHEDA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TNT",
    "en": "TINNAPPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TPH",
    "en": "TINPAHAR JN",
    "ec": "SAHIBGANJ",
    "se": "JHARKHAND"
  },
  {
    "sc": "TPV",
    "en": "TINPHERIA",
    "se": "BIHAR"
  },
  {
    "sc": "TSK",
    "en": "TINSUKIA JN",
    "ec": "TINSUKIA",
    "se": "ASSAM"
  },
  {
    "sc": "TTRA",
    "en": "TINTODA",
    "se": "GUJARAT"
  },
  {
    "sc": "TPK",
    "en": "TIPKAI",
    "se": "ASSAM"
  },
  {
    "sc": "TPG",
    "en": "TIPLING",
    "se": "ASSAM"
  },
  {
    "sc": "THPR",
    "en": "TIPPAPUR",
    "se": "TELANGANA"
  },
  {
    "sc": "TTR",
    "en": "TIPTUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "TUL",
    "en": "TIRALDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "TEG",
    "en": "TIRBEDIGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TP",
    "en": "TIRCHRPALI FORT",
    "ec": "TIRUCHCHIRAPALI/SRIRANGAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TRDI",
    "en": "TIRODI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TRO",
    "en": "TIRORA",
    "ec": "GONDIA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TCNR",
    "en": "TIRUCHANUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TCT",
    "en": "TIRUCHCHITRMBLM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TCH",
    "en": "TIRUCHCHULI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TCN",
    "en": "TIRUCHENDUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TPTN",
    "en": "TIRUCHRPALI TWN",
    "ec": "TIRUCHCHIRAPALI/SRIRANGAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TPE",
    "en": "TIRUCHRPLI PLKI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TRK",
    "en": "TIRUKOILUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TMPT",
    "en": "TIRUMALAIRAYAN",
    "se": "PUDUCHERRY"
  },
  {
    "sc": "TMLP",
    "en": "TIRUMALPUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TMQ",
    "en": "TIRUMANGALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TMU",
    "en": "TIRUMANTHIKUNAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TYM",
    "en": "TIRUMAYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TTH",
    "en": "TIRUMLAI HLS OA",
    "ec": "TIRUPATI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TRM",
    "en": "TIRUNAGESVARAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TNK",
    "en": "TIRUNELLIKAVAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TYT",
    "en": "TIRUNELVELI TWN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TI",
    "en": "TIRUNINRAVUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TUA",
    "en": "TIRUNNAVAYA",
    "se": "KERALA"
  },
  {
    "sc": "TDPR",
    "en": "TIRUPADRIPULYUR",
    "ec": "CUDDALORE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TDN",
    "en": "TIRUPARANKNDRM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TPW",
    "en": "TIRUPATI W HLT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TPT",
    "en": "TIRUPATTUR JN",
    "ec": "JOLARPETTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TPC",
    "en": "TIRUPPACHETTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TUP",
    "en": "TIRUPPUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TVN",
    "en": "TIRUPPUVANAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TIR",
    "en": "TIRUR",
    "se": "KERALA"
  },
  {
    "sc": "TLM",
    "en": "TIRUSULAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TTL",
    "en": "TIRUTTANGAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TRT",
    "en": "TIRUTTANI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TTP",
    "en": "TIRUTURAIPUNDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "THL",
    "en": "TIRUVALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TRVL",
    "en": "TIRUVALLA",
    "se": "KERALA"
  },
  {
    "sc": "TRL",
    "en": "TIRUVALLUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TYMR",
    "en": "TIRUVANMIYUR",
    "ec": "CHENNAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TNM",
    "en": "TIRUVANNAMALAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TRB",
    "en": "TIRUVERUMBUR",
    "ec": "TIRUCHCHIRAPALI/SRIRANGAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TDR",
    "en": "TIRUVIDALMARUDR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TVT",
    "en": "TIRUVOTTIYUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TVNL",
    "en": "TIRVNLNLUR ROAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TISI",
    "en": "TISI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TSA",
    "en": "TISUA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TTB",
    "en": "TITABAR",
    "ec": "JORHAT",
    "se": "ASSAM"
  },
  {
    "sc": "TGH",
    "en": "TITAGARH",
    "ec": "Howrah / Kolkata",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TIG",
    "en": "TITLAGARH",
    "ec": "TITLAGARH",
    "se": "ODISHA"
  },
  {
    "sc": "TT",
    "en": "TITTE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TOR",
    "en": "TITUR P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TLA",
    "en": "TITVALA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TTW",
    "en": "TITWA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TIW",
    "en": "TIVARI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "DJRZ",
    "en": "TO DARJEELING"
  },
  {
    "sc": "KGND",
    "en": "TO KURSEONG"
  },
  {
    "sc": "MJMG",
    "en": "TO MARWAR JN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TDP",
    "en": "TODARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TUN",
    "en": "TOHANA",
    "se": "HARYANA"
  },
  {
    "sc": "TKS",
    "en": "TOKISUD",
    "se": "JHARKHAND"
  },
  {
    "sc": "TKOT",
    "en": "TOKKOTTU",
    "se": "KARNATAKA"
  },
  {
    "sc": "THN",
    "en": "TOLAHUNSE",
    "se": "KARNATAKA"
  },
  {
    "sc": "TWI",
    "en": "TOLEWAHI P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TRZ",
    "en": "TOLRA",
    "se": "JHARKHAND"
  },
  {
    "sc": "TMKA",
    "en": "TOMKA",
    "se": "ODISHA"
  },
  {
    "sc": "TNGM",
    "en": "TONDALAGPAVARAM",
    "se": "TELANGANA"
  },
  {
    "sc": "TOM",
    "en": "TONDAMANPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TNP",
    "en": "TONDIARPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TNWR",
    "en": "TONKARWAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "TPQ",
    "en": "TOPOKAL",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "TPP",
    "en": "TOPPUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TNGL",
    "en": "TORANAGALLU",
    "se": "KARNATAKA"
  },
  {
    "sc": "TRAN",
    "en": "TORANG",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TORI",
    "en": "TORI",
    "se": "JHARKHAND"
  },
  {
    "sc": "TRNA",
    "en": "TORNA",
    "se": "GUJARAT"
  },
  {
    "sc": "TORA",
    "en": "TORNIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "TPM",
    "en": "TOTIYAPALAYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "THX",
    "en": "TOVALAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TZD",
    "en": "TOZHUPPEDU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TSM",
    "en": "TRAISAMADH",
    "se": "GUJARAT"
  },
  {
    "sc": "TBAE",
    "en": "TRIBENI",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TKQ",
    "en": "TRIKARPUR",
    "se": "KERALA"
  },
  {
    "sc": "TLMD",
    "en": "TRILOCHAN MAHDO",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TPB",
    "en": "TRILOKPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TRTR",
    "en": "TRIUPUNITTURA",
    "ec": "KOCHI / ERNAKULAM",
    "se": "KERALA"
  },
  {
    "sc": "TVP",
    "en": "TRIVANDRUM PETT",
    "se": "KERALA"
  },
  {
    "sc": "TVCN",
    "en": "TRIVANDRUMNORTH",
    "ec": "THIRUVANANTHAPURAM",
    "se": "KERALA"
  },
  {
    "sc": "TVCS",
    "en": "TRIVANDRUMSOUTH",
    "se": "KERALA"
  },
  {
    "sc": "TMBY",
    "en": "TROMBAY",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TKBN",
    "en": "TSAKIBANDA",
    "se": "KARNATAKA"
  },
  {
    "sc": "TSR",
    "en": "TSUNDURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TO",
    "en": "TTIRUVALANGADU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TFGN",
    "en": "TUFANGANJ",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TGL",
    "en": "TUGGALI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TKD",
    "en": "TUGLAKABAD",
    "ec": "NEW DELHI",
    "se": "DELHI"
  },
  {
    "sc": "TPNI",
    "en": "TUIYA PANI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TTZ",
    "en": "TUKAITHAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "THO",
    "en": "TULIN",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TGP",
    "en": "TULJAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TLAM",
    "en": "TULSI ASHRAM",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TLGR",
    "en": "TULSI NAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TUM",
    "en": "TULSIGAM",
    "se": "GUJARAT"
  },
  {
    "sc": "TLR",
    "en": "TULSIPUR",
    "ec": "GONDA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TY",
    "en": "TULUKAPATI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TK",
    "en": "TUMAKURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "TMLU",
    "en": "TUMMALACHERUVU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TAT",
    "en": "TUMMANAMGUTTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TMR",
    "en": "TUMSAR ROAD",
    "ec": "GONDIA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TMS",
    "en": "TUMSAR TOWN P H",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "TDL",
    "en": "TUNDLA JN",
    "ec": "AGRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TNO",
    "en": "TUNDU",
    "se": "JHARKHAND"
  },
  {
    "sc": "TUNG",
    "en": "TUNG",
    "se": "WEST BENGAL"
  },
  {
    "sc": "TBDM",
    "en": "TUNGABHADRA DAM",
    "se": "KARNATAKA"
  },
  {
    "sc": "TUNI",
    "en": "TUNI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TUX",
    "en": "TUNIA",
    "se": "JHARKHAND"
  },
  {
    "sc": "TKB",
    "en": "TUPKADIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "TUVR",
    "en": "TURAVUR",
    "se": "KERALA"
  },
  {
    "sc": "TRKR",
    "en": "TUREKALA ROAD",
    "se": "ODISHA"
  },
  {
    "sc": "TJM",
    "en": "TURINJAPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TKPY",
    "en": "TURKAPALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TUR",
    "en": "TURKI",
    "se": "BIHAR"
  },
  {
    "sc": "TZR",
    "en": "TURKI ROAD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "TTI",
    "en": "TURTIPAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "TME",
    "en": "TUTI MELUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TN",
    "en": "TUTICORIN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "TUV",
    "en": "TUVVUR",
    "se": "KERALA"
  },
  {
    "sc": "TUWA",
    "en": "TUWA",
    "se": "GUJARAT"
  },
  {
    "sc": "TWG",
    "en": "TWINING GANJ",
    "se": "BIHAR"
  },
  {
    "sc": "TXD",
    "en": "TYADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "TCL",
    "en": "TYAKAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "UAMR",
    "en": "UAM ROUND TRIP",
    "se": "TAMIL NADU"
  },
  {
    "sc": "UBN",
    "en": "UBARNI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UCA",
    "en": "UCHANA",
    "se": "HARYANA"
  },
  {
    "sc": "UCP",
    "en": "UCHIPPULI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "UAM",
    "en": "UDAGAMANDALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "UDKL",
    "en": "UDAI KALAN",
    "se": "RAJASTHAN"
  },
  {
    "sc": "UDPU",
    "en": "UDAIPUR",
    "se": "TRIPURA"
  },
  {
    "sc": "UDPR",
    "en": "UDAIPURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ULG",
    "en": "UDALGURI",
    "se": "ASSAM"
  },
  {
    "sc": "UKR",
    "en": "UDALKACHAR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "UDS",
    "en": "UDASAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "UDGR",
    "en": "UDGIR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "UDN",
    "en": "UDHNA JN",
    "se": "GUJARAT"
  },
  {
    "sc": "UDMR",
    "en": "UDI MOR JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UMS",
    "en": "UDRAMSAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "UDT",
    "en": "UDUMALAIPPETTAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "UD",
    "en": "UDUPI",
    "ec": "UDUPI",
    "se": "KARNATAKA"
  },
  {
    "sc": "UVD",
    "en": "UDVADA",
    "se": "GUJARAT"
  },
  {
    "sc": "UDK",
    "en": "UDYAN KHERI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "UGN",
    "en": "UGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "UGR",
    "en": "UGAR KHURD",
    "se": "KARNATAKA"
  },
  {
    "sc": "UGP",
    "en": "UGARPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UGNA",
    "en": "UGNA HALT",
    "se": "BIHAR"
  },
  {
    "sc": "URPR",
    "en": "UGRASENPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UGU",
    "en": "UGU",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UGWE",
    "en": "UGWE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "UJ",
    "en": "UJALVAV",
    "se": "GUJARAT"
  },
  {
    "sc": "UJH",
    "en": "UJHANI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UJP",
    "en": "UJIARPUR",
    "se": "BIHAR"
  },
  {
    "sc": "USD",
    "en": "UKAI SONGADH",
    "se": "GUJARAT"
  },
  {
    "sc": "UKH",
    "en": "UKHALI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "UKA",
    "en": "UKHRA",
    "ec": "ASANSOL & ANDAL",
    "se": "WEST BENGAL"
  },
  {
    "sc": "UKN",
    "en": "UKLANA",
    "se": "HARYANA"
  },
  {
    "sc": "UKC",
    "en": "UKSHI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "UPD",
    "en": "ULAVAPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ULNR",
    "en": "ULHASNAGAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "UKD",
    "en": "ULINDAKONDA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ULL",
    "en": "ULLAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "ULN",
    "en": "ULNA BHARI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ULB",
    "en": "ULUBARIA",
    "ec": "MECHEDA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "ULU",
    "en": "ULUNDURPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "UML",
    "en": "UMALLA",
    "se": "GUJARAT"
  },
  {
    "sc": "UTA",
    "en": "UMAR TALI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UM",
    "en": "UMARDASHI",
    "se": "GUJARAT"
  },
  {
    "sc": "UMR",
    "en": "UMARIA",
    "ec": "KATNI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "UIH",
    "en": "UMARIA ISPA HLT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "UMPD",
    "en": "UMARPADA",
    "se": "GUJARAT"
  },
  {
    "sc": "UBR",
    "en": "UMBARGAM ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "UR",
    "en": "UMDANAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "UMED",
    "en": "UMED",
    "se": "RAJASTHAN"
  },
  {
    "sc": "UMNR",
    "en": "UMESHNAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "UMRA",
    "en": "UMRA",
    "ec": "UDAIPUR CITY",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ULA",
    "en": "UMRA NALA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "URT",
    "en": "UMRALA",
    "se": "GUJARAT"
  },
  {
    "sc": "UMM",
    "en": "UMRAM",
    "se": "TELANGANA"
  },
  {
    "sc": "URR",
    "en": "UMRED",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "UMH",
    "en": "UMRETH",
    "se": "GUJARAT"
  },
  {
    "sc": "UMRI",
    "en": "UMRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "UOI",
    "en": "UMROLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "UNA",
    "en": "UNA",
    "se": "GUJARAT"
  },
  {
    "sc": "UHL",
    "en": "UNA HIMACHAL",
    "se": "HIMACHAL PRADESH"
  },
  {
    "sc": "UNI",
    "en": "UNAI VANSADA RD",
    "se": "GUJARAT"
  },
  {
    "sc": "UNLA",
    "en": "UNAULA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UAR",
    "en": "UNAWA AITHOR",
    "se": "GUJARAT"
  },
  {
    "sc": "UVSN",
    "en": "UNAWA VASAN",
    "se": "GUJARAT"
  },
  {
    "sc": "UCR",
    "en": "UNCHAHAR JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UCH",
    "en": "UNCHAULIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UND",
    "en": "UNCHDIH",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UHR",
    "en": "UNCHHERA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "UCB",
    "en": "UNCHI BASSI",
    "se": "PUNJAB"
  },
  {
    "sc": "UDM",
    "en": "UNDASA MADHAWPU",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "UNDI",
    "en": "UNDI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VGT",
    "en": "UNGUTURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "UNL",
    "en": "UNHEL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "URL",
    "en": "UNJALUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "UJA",
    "en": "UNJHA",
    "se": "GUJARAT"
  },
  {
    "sc": "UNK",
    "en": "UNKAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "ON",
    "en": "UNNAO JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "URD",
    "en": "UNTARE ROAD",
    "se": "JHARKHAND"
  },
  {
    "sc": "UAL",
    "en": "UPARIYALA",
    "se": "GUJARAT"
  },
  {
    "sc": "URML",
    "en": "UPARMAL",
    "se": "RAJASTHAN"
  },
  {
    "sc": "UPI",
    "en": "UPLAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "UA",
    "en": "UPLETA",
    "se": "GUJARAT"
  },
  {
    "sc": "OPL",
    "en": "UPPAL",
    "se": "TELANGANA"
  },
  {
    "sc": "UAA",
    "en": "UPPALA",
    "se": "KARNATAKA"
  },
  {
    "sc": "UPW",
    "en": "UPPALAVAI",
    "se": "TELANGANA"
  },
  {
    "sc": "UPL",
    "en": "UPPALUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "UGD",
    "en": "UPPUGUNDURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "UNCT",
    "en": "URAN CITY",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "UPM",
    "en": "URAPPAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "UDX",
    "en": "URDAULI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UREN",
    "en": "UREN",
    "se": "BIHAR"
  },
  {
    "sc": "URGA",
    "en": "URGA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "URK",
    "en": "URKURA",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "ULM",
    "en": "URLAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "URMA",
    "en": "URMA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "URI",
    "en": "URULI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "URG",
    "en": "USARGAON",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "USLP",
    "en": "USILAMPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "UB",
    "en": "USKA BAZAR",
    "ec": "GORAKHPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "USL",
    "en": "USLAPUR",
    "ec": "BILASPUR",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "UPR",
    "en": "USMANPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "USRA",
    "en": "USRA",
    "se": "GUJARAT"
  },
  {
    "sc": "UTL",
    "en": "UTARLAI",
    "se": "RAJASTHAN"
  },
  {
    "sc": "UTD",
    "en": "UTARSANDA",
    "se": "GUJARAT"
  },
  {
    "sc": "UTR",
    "en": "UTRAHTIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "URN",
    "en": "UTRAN",
    "se": "GUJARAT"
  },
  {
    "sc": "UTP",
    "en": "UTRIPURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "UKV",
    "en": "UTTAMARKOVIL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "UMG",
    "en": "UTTANGAL MANGLM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "UKE",
    "en": "UTTARKATHANI",
    "se": "ASSAM"
  },
  {
    "sc": "UPA",
    "en": "UTTARPARA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "UKL",
    "en": "UTTUKULI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VKZ",
    "en": "V N RAJUVARIPTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VOC",
    "en": "V O C NAGAR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VPH",
    "en": "VACHASPATINAGAR",
    "se": "BIHAR"
  },
  {
    "sc": "VRJ",
    "en": "VADAJ",
    "se": "GUJARAT"
  },
  {
    "sc": "VDK",
    "en": "VADAKANNIKAPURM",
    "se": "KERALA"
  },
  {
    "sc": "BDJ",
    "en": "VADAKARA",
    "se": "KERALA"
  },
  {
    "sc": "VAL",
    "en": "VADAL",
    "se": "GUJARAT"
  },
  {
    "sc": "VDGT",
    "en": "VADALA GRANTHIN",
    "se": "PUNJAB"
  },
  {
    "sc": "VDLR",
    "en": "VADALA ROAD BBY",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VAE",
    "en": "VADALI",
    "se": "GUJARAT"
  },
  {
    "sc": "VLU",
    "en": "VADALUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VDM",
    "en": "VADAMADURA",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VAU",
    "en": "VADARLAPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VDN",
    "en": "VADGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WDN",
    "en": "VADGAON NILA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VAN",
    "en": "VADHVANA",
    "se": "GUJARAT"
  },
  {
    "sc": "VDP",
    "en": "VADIPPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VDV",
    "en": "VADIYA DEVLI",
    "se": "GUJARAT"
  },
  {
    "sc": "VMD",
    "en": "VADLAMANNADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VDG",
    "en": "VADNAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "VXD",
    "en": "VADOD",
    "se": "GUJARAT"
  },
  {
    "sc": "BRCE",
    "en": "VADORA CBO",
    "ec": "VADODARA",
    "se": "GUJARAT"
  },
  {
    "sc": "VTL",
    "en": "VADTAL SWAMNRYN",
    "se": "GUJARAT"
  },
  {
    "sc": "VVL",
    "en": "VADVIYALA",
    "se": "GUJARAT"
  },
  {
    "sc": "VD",
    "en": "VAGDIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "VGL",
    "en": "VAGHLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VU",
    "en": "VAGHPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "VHL",
    "en": "VAHLYAL",
    "se": "GUJARAT"
  },
  {
    "sc": "VBW",
    "en": "VAIBHAVWADI RD",
    "ec": "RATNAGIRI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VARD",
    "en": "VAIKOM",
    "se": "KERALA"
  },
  {
    "sc": "VPZ",
    "en": "VAILAPUZHA",
    "se": "KERALA"
  },
  {
    "sc": "VTN",
    "en": "VAITARNA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VDL",
    "en": "VAITISVARANKOIL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VPJ",
    "en": "VAIYAMPATTI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VRO",
    "en": "VAJDI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "VJRD",
    "en": "VAJIRABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "WKA",
    "en": "VAKAV",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VLDR",
    "en": "VALADAR",
    "se": "GUJARAT"
  },
  {
    "sc": "VLDE",
    "en": "VALADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VTV",
    "en": "VALANTARAVAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VAPM",
    "en": "VALAPATTANAM",
    "se": "KERALA"
  },
  {
    "sc": "VGE",
    "en": "VALAPPADI G HLT",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VMM",
    "en": "VALARAMANIKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VLT",
    "en": "VALATHOOR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VRA",
    "en": "VALAVANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "WLH",
    "en": "VALHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VLG",
    "en": "VALIGONDA",
    "se": "TELANGANA"
  },
  {
    "sc": "VV",
    "en": "VALIVADE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VLV",
    "en": "VALIVEDU HALT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VLYN",
    "en": "VALLABH VDYANGR",
    "se": "GUJARAT"
  },
  {
    "sc": "VBN",
    "en": "VALLABHNAGAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "VMP",
    "en": "VALLAMPADUGAI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VTK",
    "en": "VALLATHOL NAGAR",
    "se": "KERALA"
  },
  {
    "sc": "VLI",
    "en": "VALLIKUNNU",
    "se": "KERALA"
  },
  {
    "sc": "VRU",
    "en": "VALLIVERU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VLY",
    "en": "VALLIYUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VKNR",
    "en": "VALMIKINAGAR RD",
    "se": "BIHAR"
  },
  {
    "sc": "BL",
    "en": "VALSAD",
    "se": "GUJARAT"
  },
  {
    "sc": "WLA",
    "en": "VALTOHA",
    "se": "PUNJAB"
  },
  {
    "sc": "VBR",
    "en": "VAMBORI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "MEJ",
    "en": "VANCHIMANIYACHI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VDR",
    "en": "VANDALUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VNGP",
    "en": "VANGAICHUNGPAO",
    "se": "MANIPUR"
  },
  {
    "sc": "VNGL",
    "en": "VANGAL HALT",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VGI",
    "en": "VANGANI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VRN",
    "en": "VANGANUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VGN",
    "en": "VANGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VNRD",
    "en": "VANI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "VN",
    "en": "VANIYAMBADI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VNB",
    "en": "VANIYAMBALAM",
    "se": "KERALA"
  },
  {
    "sc": "VNJ",
    "en": "VANJIPALAIYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VKL",
    "en": "VANKAL",
    "se": "GUJARAT"
  },
  {
    "sc": "VNKA",
    "en": "VANKIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "VRX",
    "en": "VARAHI",
    "se": "GUJARAT"
  },
  {
    "sc": "VKP",
    "en": "VARAKALPATTU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "BCY",
    "en": "VARANASI CITY",
    "ec": "BANARAS",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "VNA",
    "en": "VARANGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VRE",
    "en": "VAREDIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "VTDI",
    "en": "VARETHA",
    "se": "GUJARAT"
  },
  {
    "sc": "VAK",
    "en": "VARKALASIVAGIRI",
    "se": "KERALA"
  },
  {
    "sc": "VRKD",
    "en": "VARKHEDI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VRM",
    "en": "VARNAMA",
    "se": "GUJARAT"
  },
  {
    "sc": "VTJ",
    "en": "VARTEJ",
    "se": "GUJARAT"
  },
  {
    "sc": "VVA",
    "en": "VARVALA",
    "se": "GUJARAT"
  },
  {
    "sc": "VDA",
    "en": "VASAD JN",
    "se": "GUJARAT"
  },
  {
    "sc": "VSV",
    "en": "VASADVA",
    "se": "GUJARAT"
  },
  {
    "sc": "VAS",
    "en": "VASAI DABHLA",
    "se": "GUJARAT"
  },
  {
    "sc": "BSR",
    "en": "VASAI ROAD",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WSE",
    "en": "VASAN IYAWA",
    "se": "GUJARAT"
  },
  {
    "sc": "VSG",
    "en": "VASCO DA GAMA",
    "se": "GOA"
  },
  {
    "sc": "VSH",
    "en": "VASHI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VSD",
    "en": "VASIND",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VASO",
    "en": "VASO",
    "se": "GUJARAT"
  },
  {
    "sc": "VTP",
    "en": "VASTRAPUR",
    "ec": "AHMEDABAD",
    "se": "GUJARAT"
  },
  {
    "sc": "VAT",
    "en": "VATLUR",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VTA",
    "en": "VATVA",
    "se": "GUJARAT"
  },
  {
    "sc": "VKG",
    "en": "VAVADI KHURD",
    "se": "GUJARAT"
  },
  {
    "sc": "WWA",
    "en": "VAVANIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "VVD",
    "en": "VAVDI",
    "se": "GUJARAT"
  },
  {
    "sc": "VVV",
    "en": "VAVERA",
    "se": "GUJARAT"
  },
  {
    "sc": "VLD",
    "en": "VAYALPAD",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VDY",
    "en": "VEDARANNIYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VDE",
    "en": "VEDAYAPALEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VDH",
    "en": "VEDCHHA",
    "se": "GUJARAT"
  },
  {
    "sc": "VEER",
    "en": "VEER",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VGP",
    "en": "VEGANPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "VJK",
    "en": "VEJALKA",
    "se": "GUJARAT"
  },
  {
    "sc": "VJA",
    "en": "VEJANDLA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "WJP",
    "en": "VEJPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "VLCY",
    "en": "VELACHERI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VLC",
    "en": "VELACHHA",
    "se": "GUJARAT"
  },
  {
    "sc": "VNL",
    "en": "VELANANDAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VAD",
    "en": "VELAVADAR",
    "se": "GUJARAT"
  },
  {
    "sc": "VDI",
    "en": "VELDURTI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VELI",
    "en": "VELI",
    "se": "KERALA"
  },
  {
    "sc": "VLE",
    "en": "VELLACHERUVU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VLNK",
    "en": "VELLANKANNI",
    "ec": "NAGAPPATTINAM/VELANKANNI/KARAIKAL",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VEL",
    "en": "VELLANUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VEK",
    "en": "VELLARAKKAD",
    "se": "KERALA"
  },
  {
    "sc": "VLL",
    "en": "VELLAYIL",
    "se": "KERALA"
  },
  {
    "sc": "VO",
    "en": "VELLODU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VLR",
    "en": "VELLORE CANT",
    "ec": "VELLORE",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VT",
    "en": "VELLORE TOWN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VXM",
    "en": "VELLPAPALYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VPU",
    "en": "VELPURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VMR",
    "en": "VEMAR",
    "se": "GUJARAT"
  },
  {
    "sc": "VML",
    "en": "VEMULAPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VMLD",
    "en": "VEMULURIPADU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VMU",
    "en": "VEMURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VDD",
    "en": "VENDODU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VND",
    "en": "VENDRA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VKT",
    "en": "VENKATACHALAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VKI",
    "en": "VENKATAGIRI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VPL",
    "en": "VENKATAMPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VKM",
    "en": "VENKATESAPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VKR",
    "en": "VENKATNAGRA",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "VPG",
    "en": "VENTRAPRAGADA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VGA",
    "en": "VEPAGUNTA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VEU",
    "en": "VEPPAMPATTU",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VRL",
    "en": "VERAVAL",
    "se": "GUJARAT"
  },
  {
    "sc": "VRLI",
    "en": "VERAVALI (H)",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VKA",
    "en": "VERKA JN",
    "se": "PUNJAB"
  },
  {
    "sc": "VEN",
    "en": "VERNA",
    "se": "GOA"
  },
  {
    "sc": "VTM",
    "en": "VETAPALEM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VCT",
    "en": "VICTOR",
    "se": "GUJARAT"
  },
  {
    "sc": "BHS",
    "en": "VIDISHA",
    "ec": "BHOPAL",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "VWA",
    "en": "VIDURASWATTHA",
    "se": "KARNATAKA"
  },
  {
    "sc": "VAR",
    "en": "VIDYANAGAR",
    "se": "TELANGANA"
  },
  {
    "sc": "VPDA",
    "en": "VIDYAPATIDHAM",
    "se": "BIHAR"
  },
  {
    "sc": "VDS",
    "en": "VIDYASAGAR",
    "ec": "ASANSOL",
    "se": "JHARKHAND"
  },
  {
    "sc": "VVH",
    "en": "VIDYAVIHAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VJF",
    "en": "VIJAPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "VJP",
    "en": "VIJAY PUR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "VZ",
    "en": "VIJAYAMANGALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VJR",
    "en": "VIJAYANAGAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "BJP",
    "en": "VIJAYAPURA",
    "se": "KARNATAKA"
  },
  {
    "sc": "VJPJ",
    "en": "VIJIYPUR JAMMU",
    "se": "JAMMU AND KASHMIR"
  },
  {
    "sc": "VJD",
    "en": "VIJPADI ROAD",
    "se": "GUJARAT"
  },
  {
    "sc": "VKB",
    "en": "VIKARABAD JN",
    "se": "TELANGANA"
  },
  {
    "sc": "VKH",
    "en": "VIKHRAN ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VK",
    "en": "VIKHROLI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VMA",
    "en": "VIKRAMGARH ALOT",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "VRG",
    "en": "VIKRAMNAGAR",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "VVN",
    "en": "VIKRAVANDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VL",
    "en": "VILAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VGD",
    "en": "VILANGUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VID",
    "en": "VILAVADE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VYK",
    "en": "VILAYATKALAN RD",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "VLN",
    "en": "VILEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VLP",
    "en": "VILLE PARLE",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VI",
    "en": "VILLIANUR",
    "se": "PUDUCHERRY"
  },
  {
    "sc": "VLK",
    "en": "VILLIVAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VB",
    "en": "VILLIYAMBAKKAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VM",
    "en": "VILLUPURAM JN",
    "ec": "PONDICHERRY/PUDUCHERRY",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VINA",
    "en": "VINA",
    "se": "GUJARAT"
  },
  {
    "sc": "BNKM",
    "en": "VINAEKMA HALT",
    "se": "BIHAR"
  },
  {
    "sc": "VCA",
    "en": "VINCHIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "BDL",
    "en": "VINDHYACHAL",
    "ec": "MIRZAPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "VINH",
    "en": "VINHERE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VGM",
    "en": "VINNAMANGALAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VKN",
    "en": "VINUKONDA",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VQD",
    "en": "VIRAMDAD",
    "se": "GUJARAT"
  },
  {
    "sc": "VG",
    "en": "VIRAMGAM JN",
    "se": "GUJARAT"
  },
  {
    "sc": "VRLR",
    "en": "VIRANI ALUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VRPD",
    "en": "VIRAPANDY ROAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VP",
    "en": "VIRAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "VR",
    "en": "VIRAR",
    "ec": "MUMBAI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VRQ",
    "en": "VIRARAKKIYAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VRV",
    "en": "VIRAVADA",
    "se": "GUJARAT"
  },
  {
    "sc": "VRVL",
    "en": "VIRAVALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VVR",
    "en": "VIRAVANALLUR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VVM",
    "en": "VIRAVASARAM",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VRH",
    "en": "VIRBHADRA",
    "se": "UTTARAKHAND"
  },
  {
    "sc": "VRD",
    "en": "VIRDEL ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VJ",
    "en": "VIRINCHIPURAM",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VRK",
    "en": "VIRKUDI",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VCN",
    "en": "VIROCHANNAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "VOL",
    "en": "VIROL",
    "se": "GUJARAT"
  },
  {
    "sc": "VRR",
    "en": "VIRPUR",
    "se": "GUJARAT"
  },
  {
    "sc": "VRS",
    "en": "VIRSAD",
    "se": "GUJARAT"
  },
  {
    "sc": "VPT",
    "en": "VIRUDUNAGAR JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VUL",
    "en": "VIRUL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VPR",
    "en": "VISAPUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VSW",
    "en": "VISAVADAR",
    "se": "GUJARAT"
  },
  {
    "sc": "VNUP",
    "en": "VISHNUPURAM JN",
    "se": "TELANGANA"
  },
  {
    "sc": "VRB",
    "en": "VISHRAMBAG",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WMP",
    "en": "VISHRAMPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "VS",
    "en": "VISHVAMITRI",
    "ec": "VADODARA",
    "se": "GUJARAT"
  },
  {
    "sc": "VSI",
    "en": "VISHVAMITRI",
    "se": "GUJARAT"
  },
  {
    "sc": "VWP",
    "en": "VISHWANATH PURI",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "VNG",
    "en": "VISNAGAR",
    "se": "GUJARAT"
  },
  {
    "sc": "VNE",
    "en": "VISWANATH CHRLI",
    "se": "ASSAM"
  },
  {
    "sc": "VLDI",
    "en": "VITHALWADI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VVB",
    "en": "VIVEKA VIHAR",
    "se": "DELHI"
  },
  {
    "sc": "VVKP",
    "en": "VIVEKNNDAPURI H",
    "se": "DELHI"
  },
  {
    "sc": "VZM",
    "en": "VIZIANAGRAM JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "VONB",
    "en": "VONDH",
    "se": "GUJARAT"
  },
  {
    "sc": "VRT",
    "en": "VRIDDHACHALM TN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VRI",
    "en": "VRIDHACHALAM JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VRBD",
    "en": "VRINDABAN ROAD",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "BDB",
    "en": "VRINDAVAN",
    "ec": "MATHURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "VNT",
    "en": "VYANKATPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "VYA",
    "en": "VYARA",
    "se": "GUJARAT"
  },
  {
    "sc": "VC",
    "en": "VYASA COLONY JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "VYS",
    "en": "VYASANAKERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "VJM",
    "en": "VYASARPADI JIVA",
    "se": "TAMIL NADU"
  },
  {
    "sc": "VYN",
    "en": "VYASNAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "WKI",
    "en": "WADAKANCHERI",
    "se": "KERALA"
  },
  {
    "sc": "BPTW",
    "en": "WADALA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WAD",
    "en": "WADALI",
    "se": "GUJARAT"
  },
  {
    "sc": "WDG",
    "en": "WADEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WC",
    "en": "WADHWAN CITY",
    "se": "GUJARAT"
  },
  {
    "sc": "WADI",
    "en": "WADI",
    "se": "KARNATAKA"
  },
  {
    "sc": "WDR",
    "en": "WADIARAM",
    "se": "TELANGANA"
  },
  {
    "sc": "WDA",
    "en": "WADRENGDISA",
    "se": "ASSAM"
  },
  {
    "sc": "WSA",
    "en": "WADSA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WDS",
    "en": "WADSINGE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WDLN",
    "en": "WADWAL NAGNATH",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WGI",
    "en": "WAGHAI",
    "se": "GUJARAT"
  },
  {
    "sc": "WGN",
    "en": "WAGHANIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "WGA",
    "en": "WAGHODA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WGR",
    "en": "WAGHORIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "WAIR",
    "en": "WAIR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "WJ",
    "en": "WALAJABAD",
    "se": "TAMIL NADU"
  },
  {
    "sc": "WJR",
    "en": "WALAJAH ROAD JN",
    "se": "TAMIL NADU"
  },
  {
    "sc": "WRA",
    "en": "WALAYAR",
    "se": "KERALA"
  },
  {
    "sc": "WLGN",
    "en": "WALGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WND",
    "en": "WAN ROAD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WDL",
    "en": "WANDAL",
    "se": "KARNATAKA"
  },
  {
    "sc": "WDJ",
    "en": "WANDERJATANA",
    "se": "PUNJAB"
  },
  {
    "sc": "WNG",
    "en": "WANEGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WP",
    "en": "WANGAPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "WANI",
    "en": "WANI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WKRC",
    "en": "WANKANER CITY",
    "se": "GUJARAT"
  },
  {
    "sc": "WKR",
    "en": "WANKANER JN",
    "se": "GUJARAT"
  },
  {
    "sc": "WPR",
    "en": "WANPARTI ROAD",
    "se": "TELANGANA"
  },
  {
    "sc": "WSJ",
    "en": "WANSJALIYA",
    "se": "GUJARAT"
  },
  {
    "sc": "WL",
    "en": "WARANGAL",
    "ec": "WARANGAL",
    "se": "TELANGANA"
  },
  {
    "sc": "WRI",
    "en": "WARASEONI",
    "se": "MADHYA PRADESH"
  },
  {
    "sc": "WR",
    "en": "WARDHA JN",
    "ec": "WARDHA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "OYR",
    "en": "WARIA",
    "se": "WEST BENGAL"
  },
  {
    "sc": "WRGN",
    "en": "WARIGAON NEWADA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "WRS",
    "en": "WARIS ALEGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "WRR",
    "en": "WARORA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WOC",
    "en": "WARUD ORANGE CT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WRD",
    "en": "WARUDKHED",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "VSP",
    "en": "WASANAPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "WST",
    "en": "WASHERMANPET",
    "se": "TAMIL NADU"
  },
  {
    "sc": "WHM",
    "en": "WASHIM",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WSB",
    "en": "WASHIMBE",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WSD",
    "en": "WASUD",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WTR",
    "en": "WATHAR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WZJ",
    "en": "WAZERGANJ",
    "se": "BIHAR"
  },
  {
    "sc": "WEL",
    "en": "WELLINGTON",
    "se": "TAMIL NADU"
  },
  {
    "sc": "WENA",
    "en": "WENA",
    "se": "BIHAR"
  },
  {
    "sc": "WH",
    "en": "WEST HILL",
    "se": "KERALA"
  },
  {
    "sc": "WFD",
    "en": "WHITEFIELD",
    "se": "KARNATAKA"
  },
  {
    "sc": "VHGN",
    "en": "WIHIRGAON",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WCN",
    "en": "WIMCO NAGAR",
    "se": "TAMIL NADU"
  },
  {
    "sc": "WIRR",
    "en": "WIRUR",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "WRC",
    "en": "WRS COLONY P H",
    "se": "CHHATTISGARH"
  },
  {
    "sc": "WDM",
    "en": "WYNDHAMGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "YADD",
    "en": "YADADRI",
    "se": "TELANGANA"
  },
  {
    "sc": "YADA",
    "en": "YADAVALLI",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "YG",
    "en": "YADGIR",
    "se": "KARNATAKA"
  },
  {
    "sc": "YDLP",
    "en": "YADLAPUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "YDD",
    "en": "YADUDIH",
    "se": "JHARKHAND"
  },
  {
    "sc": "YDV",
    "en": "YADVENDRANAGAR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "YKA",
    "en": "YAKUTPURA KCG",
    "se": "TELANGANA"
  },
  {
    "sc": "YLG",
    "en": "YALVIGI",
    "se": "KARNATAKA"
  },
  {
    "sc": "JAB",
    "en": "YAMUNA BDG AGRA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "JSB",
    "en": "YAMUNA SOUTH BK",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "YJUD",
    "en": "YAMUNANAGAR JUD",
    "se": "HARYANA"
  },
  {
    "sc": "YAG",
    "en": "YAQUTGANJ",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "YSPM",
    "en": "YASANTAPUR",
    "se": "TELANGANA"
  },
  {
    "sc": "YAL",
    "en": "YATALURU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "YTL",
    "en": "YAVATMAL",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "YVP",
    "en": "YAWARPURA",
    "se": "GUJARAT"
  },
  {
    "sc": "YDM",
    "en": "YEDAMANGALA",
    "se": "KARNATAKA"
  },
  {
    "sc": "YDP",
    "en": "YEDAPALLI",
    "se": "TELANGANA"
  },
  {
    "sc": "YDK",
    "en": "YEDEKUMERI",
    "se": "KARNATAKA"
  },
  {
    "sc": "YY",
    "en": "YEDIYURU",
    "se": "KARNATAKA"
  },
  {
    "sc": "YSI",
    "en": "YEDSHI",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "YLBA",
    "en": "YELBURGA",
    "se": "KARNATAKA"
  },
  {
    "sc": "YGL",
    "en": "YELGUR",
    "se": "TELANGANA"
  },
  {
    "sc": "YNK",
    "en": "YELHANKA JN",
    "se": "KARNATAKA"
  },
  {
    "sc": "Y",
    "en": "YELIYUR",
    "se": "KARNATAKA"
  },
  {
    "sc": "YLK",
    "en": "YELLAKARU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "YNG",
    "en": "YENUGONDA",
    "se": "TELANGANA"
  },
  {
    "sc": "YL",
    "en": "YEOLA",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "YGA",
    "en": "YERAGOPPA",
    "se": "KARNATAKA"
  },
  {
    "sc": "YS",
    "en": "YERMARAS",
    "se": "KARNATAKA"
  },
  {
    "sc": "YPD",
    "en": "YERPEDU",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "YGD",
    "en": "YERRAGUDIPAD",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "YA",
    "en": "YERRAGUNTLA JN",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "YTG",
    "en": "YESHWANTNAGAR",
    "se": "KARNATAKA"
  },
  {
    "sc": "YAD",
    "en": "YEULKHED",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "YT",
    "en": "YEVAT",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "YNRK",
    "en": "YOG N RISHIKESH",
    "ec": "HARIDWAR",
    "se": "UTTARAKHAND",
    "tg": "BADRINATH,KEDARNATH"
  },
  {
    "sc": "YFP",
    "en": "YUSUFPUR",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ZBD",
    "en": "ZAFARABAD JN",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ZB",
    "en": "ZAHIRABAD",
    "se": "TELANGANA"
  },
  {
    "sc": "ZNA",
    "en": "ZAMANIA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ZPI",
    "en": "ZAMPANI HALT",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ZPL",
    "en": "ZANGALAPALLE",
    "se": "ANDHRA PRADESH"
  },
  {
    "sc": "ZKV",
    "en": "ZANKHAVAV",
    "se": "GUJARAT"
  },
  {
    "sc": "ZARP",
    "en": "ZARAP",
    "se": "MAHARASHTRA"
  },
  {
    "sc": "ZW",
    "en": "ZAWAR",
    "se": "RAJASTHAN"
  },
  {
    "sc": "ZP",
    "en": "ZERPUR PALI",
    "se": "HARYANA"
  },
  {
    "sc": "ZNP",
    "en": "ZINDPURA",
    "se": "UTTAR PRADESH"
  },
  {
    "sc": "ZPR",
    "en": "ZORAWARPURA",
    "se": "RAJASTHAN"
  }
]
