"""
Language translation module for leaf detection recommendations.
Supports: English, Hindi, Tamil, Telugu, Malayalam
"""

# Translation dictionary for recommendations
# Structure: {english_text: {language_code: translated_text}}

RECOMMENDATION_TRANSLATIONS = {
    # API Key Related
    "Get a free API key from https://my.plantnet.org/": {
        "hi": "https://my.plantnet.org/ से एक मुफ्त API कुंजी प्राप्त करें",
        "ta": "https://my.plantnet.org/ இலிருந்து இலவச API விசையைப் பெறுங்கள்",
        "te": "https://my.plantnet.org/ నుండి ఉచిత API కీని పొందండి",
        "ml": "https://my.plantnet.org/ സൗജന്യ API കീ നേടുക"
    },
    "The free tier allows 500 requests per day": {
        "hi": "मुफ्त टियर 500 अनुरोध प्रति दिन की अनुमति देता है",
        "ta": "இலவச அளவு தினசரி 500 கோரிக்கைகளை அனுமதிக்கிறது",
        "te": "ఉచిత టైర్‌కు రోజుకు 500 అభ్యర్థనలు ఇస్తుంది",
        "ml": "സൗജന്യ ടയറിന് ദിവസം 500 അഭ്യര്‍ഥനകള്‍ അനുവദിക്കുന്നു"
    },
    "Enter your API key in the input field above": {
        "hi": "ऊपर इनपुट फ़ील्ड में अपना API की दर्ज करें",
        "ta": "மேலே உள்ள உள்ளீட்டு புலத்தில் உங்கள் API விசையை உள்ளிடுக",
        "te": "పై ఇన్‌పుట్ ఫీల్డ్‌లో మీ API కీను నమోదు చేయండి",
        "ml": "മുകളിലെ ഇന്‍പുട്ട് ഫീല്‍ഡില്‍ നിങ്ങളുടെ API കീ നല്‍കുക"
    },
    "Please enter your PlantNet API key to use the detection feature.": {
        "hi": "डिटेक्शन फीचर का उपयोग करने के लिए कृपया अपना PlantNet API की दर्ज करें।",
        "ta": "கண்டறியும் அம்சத்தைப் பயன்படுத்த உங்கள் PlantNet API விசையை உள்ளிடவும்.",
        "te": "డిటెక్షన్ ఫీచర్‌ను ఉపయోగించుటకు దయచేసి మీ PlantNet API కీను నమోదు చేయండి.",
        "ml": "ഡിറ്റക്ഷന്‍ ഫീചറിനായി നിങ്ങളുടെ PlantNet API കീ നല്‍കുക."
    },
    
    # Error Messages
    "Take a clearer photo": {
        "hi": "एक स्पष्ट फोटो लें",
        "ta": "தெளிவான புகைப்படம் எடுக்க",
        "te": "తెలిసైన ఫోటో తీసుకోండి",
        "ml": "കൂടുതല്‍ വ്യക്തമായ ഫോട്ടോ എടുക്കുക"
    },
    "Ensure leaf is well-lit": {
        "hi": "सुनिश्चित करें कि पत्ती अच्छी तरह से रोशन हो",
        "ta": "இலை நன்கு ஒளிருவதை உறுதிசெய்",
        "te": "ఆకు బాగా వెలుగుతున్నట్టు నిర్ధరణ చేసుకోండి",
        "ml": "ഇല നന്നായി പ്രകാശിക്കപ്പെട്ടിരിക്കണം"
    },
    "Include both sides of leaf if possible": {
        "hi": "यदि संभव हो तो पत्ती के दोनों तरफ शामिल करें",
        "ta": "இலையின் இரு பக்கங்களையும் சேர்க்கவும்",
        "te": "ఆకు యొక్క ఇరువైపులా చేర్చుకోండి",
        "ml": "സാധ്യമാണെങ്കില്‍ ഇലയുടെ രണ്ട് വശങ്ങളും ഉള്‍പ്പെടുത്തുക"
    },
    "Could not identify the plant. Try with a clearer image.": {
        "hi": "पौधे की पहचान नहीं हो सकी। स्पष्ट छवि के साथ प्रयास करें।",
        "ta": "தாவரத்தை அடையாளம் காண முடியவில்லை. தெளிவான படத்துடன் முயல்க.",
        "te": "पौधे की पहचान नहीं हो सकी। स्पष्ट छवि के साथ प्रयास करें।",
        "ml": "സസ്യത്തെ തിരിച്ചറിഞ്ഞില്ല. കൂടുതല്‍ വ്യക്തമായ ചിത്രത്തിനായി ശ്രമിക്കുക."
    },
    "Invalid API key. Please check and enter a valid PlantNet API key.": {
        "hi": "अमान्य API कुंजी। कृपया जांचें और एक वैध PlantNet API कुंजी दर्ज करें।",
        "ta": "தவறான API விசை. ஒரு சரியான PlantNet API விசையை சரிபார்க்கவும்.",
        "te": "अमान्य API कुंजी। कृपया जांचें और एक वैध PlantNet API कुंजी दर्ज करें।",
        "ml": "തെറ്റായ API കീ. ശരിയായ PlantNet API കീ പരിശോധിച്ച് നല്‍കുക."
    },
    "Get a new API key from https://my.plantnet.org/": {
        "hi": "https://my.plantnet.org/ से एक नया API कुंजी प्राप्त करें",
        "ta": "https://my.plantnet.org/ இலிருந்து புதிய API விசையைப் பெறுங்கள்",
        "te": "https://my.plantnet.org/ నుండి కొత्त API కీని పొందండి",
        "ml": "https://my.plantnet.org/ പുതിയ API കീ നേടുക"
    },
    "Make sure to copy the key correctly": {
        "hi": "सुनिश्चित करें कि आपने कुंजी को सही कॉपी किया है",
        "ta": "விசையை சரியாக கॉपி செய்துள்ளதை உறுதிசெய்",
        "te": "కీను సరిగ్గా కాపీ చేశాడని నిర్ధరణ చేసుకోండి",
        "ml": "കീ ശരിയായി കോപ്പി ചെയ്ത കാര്യം ഉറപ്പാക്കുക"
    },
    "The key should be a long alphanumeric string": {
        "hi": "कुंजी एक लंबी अल्फान्यूमेरिक स्ट्रिंग होनी चाहिए",
        "ta": "விசை ஒரு நீண்ட எண்-எழுத்து சரம் இருக்க வேண்டும்",
        "te": "కీ ఒక పెద్ద ఆల్ఫాన్యూమరిక్ స్ట్రింగ్ కావాలి",
        "ml": "കീ ഒരു നീണ്ട അക്ഷരാക്കസംഖ്യാ സ്ട്രിംഗായിരിക്കണം"
    },
    "Your IP address is blocked by PlantNet API.": {
        "hi": "आपका IP पता PlantNet API द्वारा ब्लॉक किया गया है।",
        "ta": "உங்கள் IP முகவரி PlantNet API மூலம் தடுக்கப்பட்டுள்ளது.",
        "te": "మీ IP Address PlantNet API చేత బ्लాక్ చేయబడింది.",
        "ml": "നിങ്ങളുടെ IP അഡ്രസ് PlantNet API മൂലം തടയപ്പെട്ടിരിക്കുന്നു."
    },
    "Log in to https://my.plantnet.org/ and whitelist your IP in account settings": {
        "hi": "https://my.plantnet.org/ में लॉग इन करें और खाता सेटिंग्स में अपना IP व्हाइटलिस्ट करें",
        "ta": "https://my.plantnet.org/ இல் உள்நுழைந்து கணக்கு அமைகளில் உங்கள் IPஐ வெள்ளைப் பட்டியலில் சேர்க்க",
        "te": "https://my.plantnet.org/ లాగిన్ ఐది మరియు ఖాతా సెట్టింగ్స్ లో IP whitelist చేయండి",
        "ml": "https://my.plantnet.org/ ലേക്ക് ലോഗിന്‍ ചെയ്ത് അക്കൗണ്ട് സെറ്റിംഗില്‍ നിങ്ങളുടെ IP വൈറ്റ്‌ലിസ്റ്റ് ചെയ്യുക"
    },
    "Alternatively, use a different network or contact PlantNet support": {
        "hi": "वैकल्पिक रूप से, एक अलग नेटवर्क का उपयोग करें या PlantNet सहायता से संपर्क करें",
        "ta": "மாற்றாக, வேறு பிணையத்தைப் பயன்படுத்தவோ அல்லது PlantNet ஆதரவைத் தொடர்பு கொள்ளவோ",
        "te": "లేకుంటే వేరు network ఉపయోгізіть లేదా PlantNet support ను CONTACT చేయండి",
        "ml": "അല്ലിയായി മറ്റൊരു നെറ്റ്‌വർക്ക് ഉപയോഗിക്കുകയോ PlantNet സപ്പോര്‍ട്ടിനെ ബന്ധപ്പെടുകയോ ചെയ്യുക"
    },
    "API rate limit exceeded. Try again later.": {
        "hi": "API दर सीमा पार हो गई। बाद में पुनः प्रयास करें।",
        "ta": "API விகிதம் மீறியது. பின்னர் மீண்டும் முயல்க.",
        "te": "API rate limit exceed अయ్యింది. తరువాత retry చేయండి.",
        "ml": "API റേറ്റ് ലിമിറ്റ് കവിഞ്ഞിരിക്കുന്നു. പിന്നീട് വീണ്ടും ശ്രമിക്കുക."
    },
    "Wait a few minutes before trying again": {
        "hi": "पुनः प्रयास करने से पहले कुछ मिनट प्रतीक्षा करें",
        "ta": "மீண்டும் முயற்சிக்கும் முன் சில நிமிடங்கள் காத்திருக்க",
        "te": "Retry చేయ్యడానకి ముందు కొన్ని నిమిషాలు వెయ్యండి",
        "ml": "വീണ്ടും ശ്രമിക്കുന്നതിന് മുമ്പായി കുറച്ച് മിനിറ്റുകള്‍ കാത്തിരിക്കുക"
    },
    "Check your API key": {
        "hi": "अपना API कुंजी जांचें",
        "ta": "உங்கள் API விசையை சரிபார்",
        "te": "API Key చెక్ చేయండి",
        "ml": "നിങ്ങളുടെ API കീ പരിശോധിക്കുക"
    },
    "Try again later": {
        "hi": "बाद में पुनः प्रयास करें",
        "ta": "பின்னர் மீண்டும் முயல்க",
        "te": "తరువాత retry చేయండి",
        "ml": "പിന്നീട് വീണ്ടും ശ്രമിക്കുക"
    },
    "Could not connect to PlantNet API. Check your internet connection.": {
        "hi": "PlantNet API से कनेक्ट नहीं हो सका। अपना इंटरनेट कनेक्शन जांचें।",
        "ta": "PlantNet APIஇல் இணைக்க முடியவில்லை. உங்கள் இணைய இணைப்பை சரிபார்.",
        "te": "PlantNet API कनेक्ट कలేకపోతుంది. Internet connection చెక్ చేయండి.",
        "ml": "PlantNet API-യിലേക്ക് കണക്റ്റ് ചെയ്യാനായില്ല. നിങ്ങളുടെ ഇന്റര്‍നെറ്റ് കണക്ഷന്‍ പരിശോധിക്കുക."
    },
    "Check internet connection": {
        "hi": "इंटरनेट कनेक्शन जांचें",
        "ta": "இணைய இணைப்பை சரிபார்",
        "te": "Internet connection చెక్ చేయండి",
        "ml": "ഇന്റര്‍നെറ്റ് കണക്ഷന്‍ പരിശോധിക്കുക"
    },
    "Try again with a different image": {
        "hi": "एक अलग छवि के साथ पुनः प्रयास करें",
        "ta": "வேறு படத்துடன் மீண்டும் முயல்க",
        "te": " వేరు imageతో retry చేయండి",
        "ml": "മറ്റൊരു ചിത്രത്തിനായി വീണ്ടും ശ്രമിക്കുക"
    },
    
    # Disease Related - Healthy
    "Continue regular maintenance": {
        "hi": "नियमित रखरखाव जारी रखें",
        "ta": "முறையான பராமரிப்பைத் தொடரவும்",
        "te": "नियमित देखभाल जारी राखండి",
        "ml": "സാധാരണ പരിപാലനം തുടരുക"
    },
    "Monitor for early disease signs": {
        "hi": "बीमारी के शुरुआती लक्षणों की निगरानी करें",
        "ta": "நோயின் ஆரம்ப அறிகுறிகளைக் கவனியுங்கள்",
        "te": "తుది లక్షణాలు గమనిస్తుండు",
        "ml": "രോഗത്തിന്റെ ആദ്യകാല ലക്ഷണങ്ങള്‍ നിരീക്ഷിക്കുക"
    },
    "Monitor for early disease signs weekly": {
        "hi": "साप्ताहिक रूप से बीमारी के शुरुआती लक्षणों की निगरानी करें",
        "ta": "வாராந்திர நோய் அறிகுறிகளைக் கவனியுங்கள்",
        "te": "वीकली�ా disease signs గమనిస్తుండు",
        "ml": "ആഴ്ചതോറും രോഗത്തിന്റെ ആദ്യകാല ലക്ഷണങ്ങള്‍ നിരീക്ഷിക്കുക"
    },
    "Maintain proper watering schedule": {
        "hi": "उचित पानी देने की अनुसूची बनाए रखें",
        "ta": "முறையான பாசன நேரத்தை பராமரிக்க",
        "te": "正确的 జల విత్తనం scheduleను maintain చేయండి",
        "ml": "ശരിയായ ജലസേചന ഷെഡ്യൂള്‍ പാലിക്കുക"
    },
    "Ensure adequate sunlight": {
        "hi": "पर्याप्त धूप सुनिश्चित करें",
        "ta": "போதுமான சூரிய ஒளியை உறுதிப்படுத்த",
        "te": " достаточно sunlight ఉండేలా చేయండి",
        "ml": "മതിയായ സൂര്യപ്രകാശം ഉറപ്പാക്കുക"
    },
    "Ensure adequate sunlight (6-8 hours daily)": {
        "hi": "पर्याप्त धूप सुनिश्चित करें (प्रतिदिन 6-8 घंटे)",
        "ta": "தினமும் 6-8 மணி நேரம் சூரிய ஒளியை உறுதிப்படுத்த",
        "te": "రోజుకు 6-8 గంటల sunlight ఉండేలా చేయండి",
        "ml": "ദിവസം 6-8 മണിക്കാല്‍ മതിയായ സൂര്യപ്രകാശം ഉറപ്പാക്കുക"
    },
    "Keep area free of dead plant debris": {
        "hi": "क्षेत्र को मृत पौधों के अवशेषों से मुक्त रखें",
        "ta": "பகுதியை தாவர கழிவுகள் இல்லாமல் வைக்க",
        "te": "area లో dead plant debris లేకుండా ఉంచండి",
        "ml": "മരിച്ച സസ്യ അവശിഷ്ടങ്ങളില്ലാതെ പ്രദേശം നിലനിര്‍ത്തുക"
    },
    "Avoid overhead watering to prevent fungal growth": {
        "hi": "फफूंदी वृद्धि को रोकने के लिए ऊपर से पानी देना से बचें",
        "ta": "பூஞ்சை வளர்ச்சியைத் தடுக்க மேலிருந்து பாசனம் செய்யாதீர்கள்",
        "te": "fungal growth ట.prevent करుటకు over head watering ను avoid చేయండి",
        "ml": "ഫംഗസ് വളര്‍ച്ച തടയാന്‍ മുകളില്‍ നിന്ന് വെള്ളം ഒഴിവാക്കുക"
    },
    "Inspect plants regularly for pests": {
        "hi": "कीटों के लिए नियमित रूप से पौधों का निरीक्षण करें",
        "ta": "தாவரங்களை கீடுகளுக்காக नियमितமுறையில் ஆய்வு செய்ய",
        "te": "pests కోసం regularly plants inspect చేయండి",
        "ml": "കീടങ്ങള്‍ക്കായി സസ്യങ്ങള്‍ പതിവായി പരിശോധിക്കുക"
    },
    "Maintain proper nutrition with balanced fertilizer": {
        "hi": "संतुलित उर्वरक के साथ उचित पोषण बनाए रखें",
        "ta": "சமச்சீர் உரத்துடன் முறையான ஊட்டச்சத்தை பராமரிக்க",
        "te": "balanced fertilizerతో proper nutrition maintain చేయండి",
        "ml": "സമതുലിതമായ വളത്തിലൂടെ ശരിയായ പോഷണം നിലനിര്‍ത്തുക"
    },
    "Continue regular maintenance and watering schedule": {
        "hi": "नियमित रखरखाव और पानी देने की अनुसूची जारी रखें",
        "ta": "முறையான பராமரிப்பு மற்றும் பாசன அட்டவணையைத் தொடரவும்",
        "te": "regular maintenance మరియు watering schedule జరుగుతుండు",
        "ml": "സാധാരണ പരിപാലനവും ജലസേചന ഷെഡ്യൂളും തുടരുക"
    },
    "Maintain proper watering schedule": {
        "hi": "उचित पानी देने की अनुसूची बनाए रखें",
        "ta": "முறையான பாசன அட்டவணையை பராமரிக்க",
        "te": "proper watering schedule maintain చేయండి",
        "ml": "ശരിയായ ജലസേചന ഷെഡ്യൂള്‍ പാലിക്കുക"
    },
    "Ensure good nutrition": {
        "hi": "अच्छा पोषण सुनिश्चित करें",
        "ta": "நல்ல ஊட்டச்சத்தை உறுதிப்படுத்த",
        "te": "good nutrition ensure చేయండి",
        "ml": "നല്ല പോഷണം ഉറപ്പാക്കുക"
    },
    "Provide adequate sunlight": {
        "hi": "पर्याप्त धूप प्रदान करें",
        "ta": "போதுமான சூரிய ஒளியை வழங்க",
        "te": "adequate sunlight provide చేయండి",
        "ml": "മതിയായ സൂര്യപ്രകാശം നല്‍കുക"
    },
    "Keep area clean": {
        "hi": "क्षेत्र को साफ रखें",
        "ta": "பகுதியை சுத்தமாக வைக்க",
        "te": "area clean గా ఉంచండి",
        "ml": "പ്രദേശം വൃത്തിയാക്കിയിരിക്കണം"
    },
    "Inspect for pests regularly": {
        "hi": "नियमित रूप से कीटों के लिए निरीक्षण करें",
        "ta": "கீடுகளுக்காக नियमितமுறையில் ஆய்வு செய்ய",
        "te": "pestsకోసం regularly inspect చేయండి",
        "ml": "കീടങ്ങള്‍ക്കായി പതിവായി പരിശോധിക്കുക"
    },
    
    # Disease Related - Early Blight
    "Remove infected leaves immediately - do not compost them": {
        "hi": "संक्रमित पत्तियों को तुरंत हटाएं - उन्हें खाद में न डालें",
        "ta": "பாதிக்கப்பட்ட இலைகளை உடனடியாக அகற்றுங்கள் - கம்போஸ்ட் செய்யாதீர்கள்",
        "te": "infected leavesని hemmediately remove చేయండి - compost చేయకండి",
        "ml": "ബാധിതഇലകള്‍ ഉടനടി നീക്കം ചെയ്യുക - കമ്പോസ്റ്റില്‍ ഇടരുത്"
    },
    "Apply chlorothalonil or mancozeb fungicide every 7-10 days": {
        "hi": "हर 7-10 दिनों में क्लोरोथैलोनिल या मैंकोजेब कवकनाशी लगाएं",
        "ta": "ஒவ்வொரு 7-10 நாட்களுக்கு குளோரோதலோனில் அல்லது மாங்கோசெப் பூஞ்சைக்கொல்லி",
        "te": "7-10 daysకు chlorothalonil లేదా mancozeb fungicide apply చేయండి",
        "ml": "every 7-10 ദിവസത്തില്‍ ക്ലോറോതലോണിലോ മാങ്കോസെബോ ഫംഗിസൈഡോ പ്രയോഗിക്കുക"
    },
    "Improve air circulation around plants by proper spacing": {
        "hi": "उचित दूरी से पौधों के चारों ओर वायु संचार में सुधार करें",
        "ta": "தாவரங்களைச் சுற்றியுள்ள காற்றுஇயக்கத்தை மேம்படுத்த",
        "te": "plants around air circulation improve చేయండి",
        "ml": "സസ്യങ്ങള്‍ക്ക് ചുറ്റുമുള്ള വായു സഞ്ചാരം മെച്ചപ്പെടുത്തുക"
    },
    "Water at soil level only, avoid wetting foliage": {
        "hi": "केवल मिट्टी के स्तर पर पानी दें, पत्तियों को गीला करने से बचें",
        "ta": "மண் மட்டுமே பாசனம் செய்ய, இலைகளை நனைக்கத் தவிர்க்க",
        "te": "soil leveliter only water చేయ, foliage wet agundu avoid చేయండి",
        "ml": "മണ്ണ് നിരപ്പില്‍ മാത്രം വെള്ളം കൊടുക്കുക, ഇലകള്‍ നനയ്ക്കാതിരിക്കാന്‍ ശ്രമിക്കുക"
    },
    "Mulch around plants to prevent soil splash": {
        "hi": "मिट्टी के छींटने को रोकने के लिए पौधों के चारों ओर মাল্চ করें",
        "ta": "மண் பகிர்ச்சியைத் தடுக்க தாவரங்களைச் சுற்றி mulching",
        "te": "soil splash prevent करుటకు plants around mulch apply చేయండి",
        "ml": "മണ്ണിന്റെ തളിര്‍പ്പ് തടയാന്‍ സസ്യങ്ങള്‍ക്ക് ചുറ്റും മൽച്ചിംഗ് ചെയ്യുക"
    },
    "Remove plant debris after harvest": {
        "hi": "फसल कटाई के बाद पौधों के अवशेष हटाएं",
        "ta": "அறுவடைக்குப் பிறகு தாவர கழிவுகளை அகற்ற",
        "te": "harvest వెంట plant debris remove చేయండి",
        "ml": "വിളവെടുപ്പിന് ശേഷം സസ്യ അവശിഷ്ടങ്ങള്‍ നീക്കം ചെയ്യുക"
    },
    "Practice crop rotation for 2-3 years": {
        "hi": "2-3 वर्षों के लिए फसल चक्र का अभ्यास करें",
        "ta": "2-3 வருடங்களுக்கு பயிர் சுழற்சி",
        "te": "2-3 years crop rotation practice చేయండి",
        "ml": "2-3 വര്‍ഷത്തേക്ക് കൃഷി ചക്രത്തിന്റെ രീതി പാലിക്കുക"
    },
    
    # Disease Related - Late Blight
    "Apply copper or mancozeb fungicide urgently": {
        "hi": "तुरंत तांबा या मैंकोजेब कवकनाशी लगाएं",
        "ta": "செம்பு அல்லது மாங்கோசெப் பூஞ்சைக்கொல்லியை உடனடியாக",
        "te": "copper or mancozeb fungicide urgently apply చేయండి",
        "ml": "അടിയന്തിരമായി ചെമ്പോ മാങ്കോസെബോ ഫംഗിസൈഡോ പ്രയോഗിക്കുക"
    },
    "Maintain low humidity (below 30%) around plants": {
        "hi": "पौधों के चारों ओर कम आर्द्रता (30% से कम) बनाए रखें",
        "ta": "தாவரங்களைச் சுற்றி குறைந்த dampness (30% கீழ்)",
        "te": "plants around low humidity (30% below) maintain చేయండి",
        "ml": "സസ്യങ്ങള്‍ക്ക് ചുറ്റും കുറഞ്ഞ ഈര്‍പ്പം (30% കീഴില്‍) നിലനിര്‍ത്തുക"
    },
    "Destroy infected plants completely - DO NOT COMPOST": {
        "hi": "संक्रमित पौधों को पूरी तरह से नष्ट करें - खाद में न डालें",
        "ta": "பாதிக்கப்பட்ட தாவரங்களை முற்றாக அழித்து - COMPOST செய்யாதீர்கள்",
        "te": "infected plants completely destroy చేయండి - COMPOST చేయకండి",
        "ml": "ബാധിതസസ്യങ്ങളെ പൂര്‍ണമായും നശിപ്പിക്കുക - കമ്പോസ്റ്റ് ചെയ്യരുത്"
    },
    "Use 3-year crop rotation with non-solanaceous crops": {
        "hi": "गैर-सोलेनेसियस फसलों के साथ 3-वर्षीय फसल चक्र का उपयोग करें",
        "ta": "3-வருட பயிர் சுழல்",
        "te": "3-year crop rotation practice చేయండి",
        "ml": "3-വര്‍ഷത്തെ കൃഷി ചക്രം ഉപയോഗിക്കുക"
    },
    "Plant resistant varieties if available": {
        "hi": "यदि उपलब्ध हो तो प्रतिरोधी किस्में लगाएं",
        "ta": "இருப்பின் எதிர்ப்பு разновидности",
        "te": "resistant varieties plant చేయండి",
        "ml": "ലഭ്യമാണെങ്കില്‍ പ്രതിരോധശക്തിയുള്ള ഇനങ്ങള്‍ നടുക"
    },
    "Monitor nearby plants for early signs": {
        "hi": "शुरुआती लक्षणों के लिए नजदीकी पौधों की निगरानी करें",
        "ta": "அருகிலுள்ள தாவரங்களைக் கவனியுங்கள்",
        "te": "nearby plants early signs monitor చేయండి",
        "ml": "അടുത്തുള്ള സസ്യങ്ങള്‍ നിരീക്ഷിക്കുക"
    },
    "Remove ALL infected parts immediately": {
        "hi": "सभी संक्रमित भागों को तुरंत हटाएं",
        "ta": "அனைத்து பாதிக்கப்பட்ட பகுதிகளையும் உடனடியாக",
        "te": "ALL infected parts immediately remove చేయండి",
        "ml": "എല്ലാ ബാധിത ഭാഗങ്ങളും ഉടനടി നീക്കം ചെയ്യുക"
    },
    "Apply fungicide regularly": {
        "hi": "नियमित रूप से कवकनाशी लगाएं",
        "ta": "பூஞ்சைக்கொல்லியை",
        "te": "regularly fungicide apply చేయండి",
        "ml": "ഫംഗിസൈഡോ പതിവായി പ്രയോഗിക്കുക"
    },
    "Avoid watering on leaves": {
        "hi": "पत्तियों पर पानी देना से बचें",
        "ta": "இலைகளில் பாசனம்",
        "te": "leaves में water agundu avoid చేయండి",
        "ml": "ഇലകളില്‍ വെള്ളം ഒഴിവാക്കുക"
    },
    "Use mulch to prevent soil splash": {
        "hi": "मिट्टी के छींटने को रोकने के लिए मल्च का उपयोग करें",
        "ta": "மண் பகிர்ச்சியைத் தடுக்க",
        "te": "soil splash prevent করుటకు mulch use చేయండి",
        "ml": "മണ്ണിന്റെ തളിര്‍പ്പ് തടയാന്‍ മല്‍ച്ചിംഗ് ഉപയോഗിക്കുക"
    },
    "Clean up plant debris": {
        "hi": "पौधों के अवशेषों को साफ करें",
        "ta": "தாவர கழிவுகளை",
        "te": "plant debris clean up చేయండి",
        "ml": "സസ്യ അവശിഷ്ടങ്ങള്‍ വൃത്തിയാക്കുക"
    },
    "Rotate crops annually": {
        "hi": "सालाना फसल चक्र का अभ्यास करें",
        "ta": "வருடாந்திர பயிர்",
        "te": "annually crops rotate చేయండి",
        "ml": "വര്‍ഷം തോറും കൃഷി മാറ്റം വരുത്തുക"
    },
    "Apply copper fungicide urgently": {
        "hi": "तुरंत तांबा कवकनाशी लगाएं",
        "ta": "செம்பு பூஞ்சைக்கொல்லி",
        "te": "urgently copper fungicide apply చేయండి",
        "ml": "അടിയന്തിരമായി ചെമ്പ് ഫംഗിസൈഡോ പ്രയോഗിക്കുക"
    },
    "Destroy infected plants completely": {
        "hi": "संक्रमित पौधों को पूरी तरह से नष्ट करें",
        "ta": "பாதிக்கப்பட்ட தாவரங்களை",
        "te": "infected plants completely destroy చేయండి",
        "ml": "ബാധിതസസ്യങ്ങളെ പൂര്‍ണമായും നശിപ്പിക്കുക"
    },
    "Maintain low humidity": {
        "hi": "कम आर्द्रता बनाए रखें",
        "ta": "குறைந்த dampness",
        "te": "low humidity maintain చేయండి",
        "ml": "കുറഞ്ഞ ഈര്‍പ്പം നിലനിര്‍ത്തുക"
    },
    "Use resistant varieties": {
        "hi": "प्रतिरोधी किस्मों का उपयोग करें",
        "ta": "எதிர்ப்பு разновидности",
        "te": "resistant varieties use చేయండి",
        "ml": "പ്രതിരോധശക്തിയുള്ള ഇനങ്ങള്‍ ഉപയോഗിക്കുക"
    },
    "Practice crop rotation": {
        "hi": "फसल चक्र का अभ्यास करें",
        "ta": "பயிர் சுழல்",
        "te": "crop rotation practice చేయండি",
        "ml": "കൃഷി ചക്രം പാലിക്കുക"
    },
    # Generic Disease Recommendations
    "Consult plant pathologist for treatment": {
        "hi": "उपचार के लिए पादप रोग विशेषज्ञ से परामर्श लें",
        "ta": "தாவர",
        "te": "plant pathologistతో consult చేయండి",
        "ml": "ചികിത്സയ്ക്കായി സസ്യരോഗ വിദഗ്ദനെ കാണുക"
    },
    "Isolate infected plant": {
        "hi": "संक्रमित पौधे को अलग करें",
        "ta": "பாதிக்கப்பட்ட",
        "te": "infected plant isolate చేయండి",
        "ml": "ബാധിതസസ്യത്തെ അകറ്റി നിര്‍ത്തുക"
    },
    "Monitor symptom progression": {
        "hi": "लक्षणों की प्रगति की निगरानी करें",
        "ta": "அறிகுறி",
        "te": "symptom progression monitor చేయండి",
        "ml": "ലക്ഷണങ്ങളുടെ പുരോഗതി നിരീക്ഷിക്കുക"
    },
    "Apply preventive measures to nearby plants": {
        "hi": "नजदीकी पौधों पर निवारक उपाय लागू करें",
        "ta": "அருகில்",
        "te": "nearby plants preventive measures apply చేయండి",
        "ml": "അടുത്തുള്ള സസ്യങ്ങള്‍ക്ക് പ്രതിരോധ നടപടികള്‍ സ്വീകരിക്കുക"
    },
    "Take a photo of any spots, lesions, or discoloration": {
        "hi": "किसी भी धब्बों, घावों या रंग बदलाव की फोटो लें",
        "ta": "எந்த",
        "te": "spots, lesions or discoloration photo take చేయండి",
        "ml": "ഏതെങ്കിലും പാടുകളോ മുറിവുകളോ വര്‍ണ്ണമാറ്റമോ ഉള്ള ഫോട്ടോ എടുക്കുക"
    },
    "Compare with common diseases for this plant type": {
        "hi": "इस पौधे के प्रकार के लिए सामान्य बीमारियों से तुलना करें",
        "ta": "இந்த",
        "te": "this plant type common diseases compare చేయండి",
        "ml": "ഈ സസ്യത്തിന്റെ തരത്തിനുള്ള സാധാരണ രോഗങ്ങളുമായി താരതമ്യം ചെയ്യുക"
    },
    "Consult plant disease databases for specific symptoms": {
        "hi": "विशिष्ट लक्षणों के लिए पौधों की बीमारी डेटाबेस से परामर्श लें",
        "ta": "இலையின்",
        "te": "plant disease databases consult చేయండి",
        "ml": "പ്രത്യേക ലക്ഷണങ്ങള്‍ക്കായി സസ്യരോഗ ഡാറ്റാബേസുകളുമായി ബന്ധപ്പെടുക"
    },
    "Consider consulting a local agricultural extension": {
        "hi": "स्थानीय कृषि विस्तार से परामर्श लेने पर विचार करें",
        "ta": "உள்ளூர்",
        "te": "local agricultural extension consult చేయ考虑",
        "ml": "പ്രാദേശിക കാര്‍ഷിക വിപുലീകരണവുമായി കാണുന്നത് പരിഗണിക്കുക"
    },
    "Disease:": {
        "hi": "बीमारी:",
        "ta": "நோய்:",
        "te": "रोग:",
        "ml": "രോഗം:"
    }
}

# Status translations
STATUS_TRANSLATIONS = {
    "✅ Healthy Plant": {
        "hi": "✅ स्वस्थ पौधा",
        "ta": "✅ ஆரோக்கியமான தாவரம்",
        "te": "✅ स्वस्थ మెక",
        "ml": "✅ ആരോഗ്യമുള്ള ചെടി"
    },
    "📋 Plant Identified": {
        "hi": "📋 पौधे की पहचान की गई",
        "ta": "📋 தாவரம் அடையாளம் காணப்பட்டது",
        "te": "📋 पौधे की पहचान की गई",
        "ml": "📋 സസ്യം തിരിച്ചറിഞ്ഞിരിക്കുന്നു"
    },
    "🟡 Fungal Disease": {
        "hi": "🟡 कवक रोग",
        "ta": "🟡 பூஞ்சை நோய்",
        "te": "🟡 champu rogu",
        "ml": "🟡 ഫംഗസ് രോഗം"
    },
    "🔴 Critical Disease": {
        "hi": "🔴 गंभीर रोग",
        "ta": "🔴 Critical நோối",
        "te": "🔴 गंभीर रोग",
        "ml": "🔴 ഗുരുതര രോഗം"
    },
    "✅ Healthy": {
        "hi": "✅ स्वस्थ",
        "ta": "✅ ஆரோக்கியமான",
        "te": "✅ स्वस्थ",
        "ml": "✅ ആരോഗ്യമുള്ള"
    },
    "📋 Identified": {
        "hi": "📋 पहचाना गया",
        "ta": "📋 அடையாளம் காணப்பட்ட",
        "te": "📋 पहचाना गया",
        "ml": "📋 തിരിച്ചറിഞ്ഞ"
    },
    "⚠️ API Key Required": {
        "hi": "⚠️ API कुंजी आवश्यक",
        "ta": "⚠️ API Key தேவை",
        "te": "⚠️ API Key आवश्यक",
        "ml": "⚠️ API കീ ആവശ്യമാണ്"
    },
    "❓ Unknown Plant": {
        "hi": "❓ अज्ञात पौधा",
        "ta": "❓ தெரியாத தாவரம்",
        "te": "❓ Unknown plant",
        "ml": "❓ അറിയാത്ത സസ്യം"
    },
    "⚠️ Invalid API Key": {
        "hi": "⚠️ अमान्य API कुंजी",
        "ta": "⚠️ Invalid API Key",
        "te": "⚠️ Invalid API Key",
        "ml": "⚠️ തെറ്റായ API കീ"
    },
    "⚠️ IP Blocked": {
        "hi": "⚠️ IP ब्लॉक किया गया",
        "ta": "⚠️ IP Blocked",
        "te": "⚠️ IP Blocked",
        "ml": "⚠️ IP തടയപ്പെട്ടിരിക്കുന്നു"
    },
    "⚠️ Rate Limited": {
        "hi": "⚠️ दर सीमित",
        "ta": "⚠️ Rate Limited",
        "te": "⚠️ Rate Limited",
        "ml": "⚠️ റേറ്റ് ലിമിറ്റഡ്"
    },
    "⚠️ API Error": {
        "hi": "⚠️ API त्रुटि",
        "ta": "⚠️ API Error",
        "te": "⚠️ API Error",
        "ml": "⚠️ API പിഴവ്"
    },
    "❌ Connection Error": {
        "hi": "❌ कनेक्शन त्रुटि",
        "ta": "❌ Connection Error",
        "te": "❌ Connection Error",
        "ml": "❌ കണക്ഷന്‍ പിഴവ്"
    },
    "❌ Error": {
        "hi": "❌ त्रुटि",
        "ta": "❌ பிழை",
        "te": "❌ Error",
        "ml": "❌ പിഴവ്"
    }
}

# Language names for display
LANGUAGE_NAMES = {
    "en": "English",
    "hi": "हिंदी (Hindi)",
    "ta": "தமிழ் (Tamil)",
    "te": "తెలుగు (Telugu)",
    "ml": "മലയാളം (Malayalam)"
}

def translate_text(text: str, target_lang: str) -> str:
    """
    Translate a single text string to the target language.
    
    Args:
        text: The English text to translate
        target_lang: Target language code (hi, ta, te, ml)
    
    Returns:
        Translated text, or original if translation not found
    """
    if target_lang == "en":
        return text
    
    # Check if we have a translation
    if text in RECOMMENDATION_TRANSLATIONS:
        translations = RECOMMENDATION_TRANSLATIONS[text]
        if target_lang in translations:
            return translations[target_lang]
    
    # Return original if no translation found
    return text


def translate_recommendations(recommendations: list, target_lang: str) -> list:
    """
    Translate a list of recommendation strings.
    
    Args:
        recommendations: List of English recommendation strings
        target_lang: Target language code (hi, ta, te, ml)
    
    Returns:
        List of translated recommendations
    """
    if target_lang == "en":
        return recommendations
    
    return [translate_text(rec, target_lang) for rec in recommendations]


def translate_status(status: str, target_lang: str) -> str:
    """
    Translate a status message.
    
    Args:
        status: The English status string
        target_lang: Target language code (hi, ta, te, ml)
    
    Returns:
        Translated status, or original if translation not found
    """
    if target_lang == "en":
        return status
    
    if status in STATUS_TRANSLATIONS:
        translations = STATUS_TRANSLATIONS[status]
        if target_lang in translations:
            return translations[target_lang]
    
    return status


def translate_disease_info(disease_info: dict, target_lang: str) -> dict:
    """
    Translate entire disease info dictionary including status and recommendations.
    
    Args:
        disease_info: Dictionary with 'status', 'description', 'recommendations', etc.
        target_lang: Target language code
    
    Returns:
        Dictionary with translated values
    """
    if target_lang == "en":
        return disease_info
    
    translated_info = disease_info.copy()
    
    # Translate status
    if "status" in translated_info:
        translated_info["status"] = translate_status(translated_info["status"], target_lang)
    
    # Translate description if needed (optional)
    if "description" in translated_info:
        # Description is usually technical, can add translations if needed
        pass
    
    # Translate recommendations
    if "recommendations" in translated_info and isinstance(translated_info["recommendations"], list):
        translated_info["recommendations"] = translate_recommendations(
            translated_info["recommendations"], 
            target_lang
        )
    
    return translated_info

