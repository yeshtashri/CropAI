"""
recommendations.py
------------------
Maps each disease class name to a detailed recommendation dictionary
containing:
    - description  : What the disease is
    - symptoms     : Key visual symptoms
    - treatment    : Actionable treatment steps (list)
    - prevention   : Prevention tips (list)
    - severity     : "low" | "medium" | "high"
    - pesticides   : Recommended products / chemicals (list)
"""

RECOMMENDATIONS = {
    # -------------------------------------------------------------------------
    # PEPPER
    # -------------------------------------------------------------------------
    "Pepper__bell___Bacterial_spot": {
        "description": (
            "Bacterial spot is caused by Xanthomonas campestris and is one of the "
            "most destructive diseases of pepper in warm, humid climates. It affects "
            "leaves, stems, and fruits."
        ),
        "symptoms": (
            "Small, water-soaked spots on leaves that turn brown with yellow halos. "
            "Spots may merge causing large necrotic areas. Infected fruits show raised, "
            "scab-like lesions."
        ),
        "treatment": [
            "Remove and destroy all infected plant parts immediately.",
            "Apply copper-based bactericides (e.g., Copper Hydroxide or Copper Oxychloride) every 7–10 days.",
            "Use streptomycin sulfate sprays in early infection stages.",
            "Avoid overhead irrigation to reduce leaf wetness.",
            "Disinfect garden tools with 10% bleach solution between uses.",
        ],
        "prevention": [
            "Use certified disease-free seeds or transplants.",
            "Rotate crops — avoid planting pepper or tomato in the same field for at least 2 years.",
            "Maintain proper plant spacing for good air circulation.",
            "Apply mulch to prevent soil splash onto lower leaves.",
            "Select resistant pepper varieties when available.",
        ],
        "severity": "high",
        "pesticides": [
            "Kocide 3000 (Copper Hydroxide)",
            "Badge X2 (Copper Oxychloride + Copper Hydroxide)",
            "Actigard 50WG (Acibenzolar-S-methyl) — systemic resistance activator",
        ],
    },

    "Pepper__bell___healthy": {
        "description": "Your pepper plant appears healthy with no signs of disease.",
        "symptoms": "No symptoms detected. Leaves are uniformly green without spots or lesions.",
        "treatment": [
            "Continue regular monitoring every 3–5 days.",
            "Maintain consistent watering and fertilisation schedules.",
        ],
        "prevention": [
            "Keep the growing area clean and free of debris.",
            "Ensure adequate sunlight (6–8 hours/day) and air circulation.",
            "Practice crop rotation yearly.",
        ],
        "severity": "low",
        "pesticides": [],
    },

    # -------------------------------------------------------------------------
    # POTATO
    # -------------------------------------------------------------------------
    "Potato___Early_blight": {
        "description": (
            "Early blight (Alternaria solani) is a common fungal disease affecting "
            "potatoes and tomatoes. It typically attacks older leaves first and spreads "
            "under warm, humid conditions."
        ),
        "symptoms": (
            "Dark brown to black lesions with concentric rings (target-board pattern) "
            "surrounded by yellow halos on older leaves. Severe infection causes "
            "defoliation and reduced yield."
        ),
        "treatment": [
            "Remove infected lower leaves and dispose of them away from the field.",
            "Apply fungicides containing Chlorothalonil, Mancozeb, or Azoxystrobin.",
            "Start fungicide applications when symptoms first appear and repeat every 7–14 days.",
            "Improve plant nutrition — nitrogen-deficient plants are more susceptible.",
        ],
        "prevention": [
            "Use certified disease-free seed potatoes.",
            "Rotate crops with non-solanaceous crops for 2–3 years.",
            "Plant resistant varieties such as Defender or Jacqueline Lee.",
            "Avoid excessive nitrogen fertilisation.",
            "Irrigate at the base of plants early in the day.",
        ],
        "severity": "medium",
        "pesticides": [
            "Bravo WeatherStik (Chlorothalonil)",
            "Mancozeb 80 WP",
            "Quadris (Azoxystrobin)",
            "Revus Top (Mandipropamid + difenoconazole)",
        ],
    },

    "Potato___Late_blight": {
        "description": (
            "Late blight (Phytophthora infestans) is one of the most devastating "
            "plant diseases in history — it caused the Irish Potato Famine. "
            "It spreads rapidly in cool, wet weather."
        ),
        "symptoms": (
            "Pale green or water-soaked lesions on leaves that quickly turn brown-black "
            "with a water-soaked border. White mould may be visible on the underside "
            "of leaves in humid conditions. Tubers show reddish-brown rot."
        ),
        "treatment": [
            "Destroy infected plants or plant parts immediately — do NOT compost them.",
            "Apply systemic fungicides: Metalaxyl, Dimethomorph, or Cymoxanil.",
            "Use protective fungicides like Mancozeb or Chlorothalonil as a barrier.",
            "Harvest tubers carefully; avoid wounding them.",
        ],
        "prevention": [
            "Plant only certified disease-free seed potatoes.",
            "Use resistant varieties (e.g., Sarpo Mira, Defender).",
            "Avoid overhead irrigation; use drip irrigation instead.",
            "Hill soil around stems to protect developing tubers.",
            "Monitor weather forecasts — apply preventive sprays before humid periods.",
        ],
        "severity": "high",
        "pesticides": [
            "Ridomil Gold MZ (Metalaxyl + Mancozeb)",
            "Acrobat MZ (Dimethomorph + Mancozeb)",
            "Curzate (Cymoxanil + Mancozeb)",
            "Infinito (Propamocarb + Fluopicolide)",
        ],
    },

    "Potato___healthy": {
        "description": "Your potato plant appears healthy with no signs of disease.",
        "symptoms": "Leaves are dark green and vigorous with no lesions or abnormal coloration.",
        "treatment": [
            "Continue regular scouting for early signs of disease.",
            "Maintain balanced fertilisation especially potassium and phosphorus.",
        ],
        "prevention": [
            "Hill soil around plants as they grow.",
            "Maintain adequate soil moisture without waterlogging.",
            "Practice 3–4 year crop rotation.",
        ],
        "severity": "low",
        "pesticides": [],
    },

    # -------------------------------------------------------------------------
    # TOMATO
    # -------------------------------------------------------------------------
    "Tomato_Bacterial_spot": {
        "description": (
            "Bacterial spot (Xanthomonas vesicatoria) is a serious tomato disease "
            "causing significant yield losses in warm, rainy seasons."
        ),
        "symptoms": (
            "Small, water-soaked spots on leaves and fruit. Spots turn brown with "
            "yellow margins. Fruit lesions appear raised and scabby, reducing marketability."
        ),
        "treatment": [
            "Remove and burn heavily infected plant material.",
            "Apply copper bactericides (Copper Hydroxide or Copper Octanoate) weekly.",
            "Use fixed copper sprays combined with mancozeb for better control.",
            "Avoid working in field when plants are wet.",
        ],
        "prevention": [
            "Use disease-free transplants and seeds — hot water treat seeds at 50°C for 25 minutes.",
            "Stake and prune plants for better air circulation.",
            "Rotate crops for 2+ years away from tomato/pepper.",
            "Avoid overhead watering.",
        ],
        "severity": "high",
        "pesticides": [
            "Kocide 3000 (Copper Hydroxide)",
            "Cuprofix Ultra 40D (Copper Sulfate)",
            "Badge SC (Copper Oxychloride)",
        ],
    },

    "Tomato_Early_blight": {
        "description": (
            "Early blight (Alternaria solani) is a widespread fungal disease of "
            "tomatoes causing dark lesions with concentric rings on older leaves."
        ),
        "symptoms": (
            "Dark brown lesions with concentric rings and yellow halo on lower/older leaves. "
            "Fruit develops dark, leathery, sunken spots at the stem end."
        ),
        "treatment": [
            "Prune lower infected leaves and dispose of debris.",
            "Apply Chlorothalonil, Mancozeb, or Azoxystrobin on a 7–10 day schedule.",
            "Improve plant nutrition — calcium and potassium deficiency worsen symptoms.",
        ],
        "prevention": [
            "Use resistant tomato varieties where available.",
            "Mulch around plants to prevent soil splash.",
            "Water early morning at the base; avoid wetting foliage.",
            "Practice 2-year crop rotation.",
        ],
        "severity": "medium",
        "pesticides": [
            "Bravo WeatherStik (Chlorothalonil)",
            "Dithane M-45 (Mancozeb)",
            "Quadris (Azoxystrobin)",
            "Cabrio EG (Pyraclostrobin)",
        ],
    },

    "Tomato_Late_blight": {
        "description": (
            "Late blight (Phytophthora infestans) can devastate entire tomato crops "
            "within days under cool, moist conditions. Emergency response is required."
        ),
        "symptoms": (
            "Large, irregular, water-soaked grey-green patches on leaves turning dark. "
            "White cottony sporulation on leaf undersides in humid weather. "
            "Soft, brown, greasy-looking rot on fruit."
        ),
        "treatment": [
            "Remove all infected plant material immediately — bag and dispose away from farm.",
            "Apply systemic fungicides: Metalaxyl-M, Fluopicolide, or Amisulbrom.",
            "Alternate between contact and systemic fungicides to prevent resistance.",
        ],
        "prevention": [
            "Monitor weather and apply preventive sprays before cool/wet spells.",
            "Use resistant varieties (Mountain Magic, Plum Regal).",
            "Avoid overhead irrigation.",
            "Destroy crop debris thoroughly after harvest.",
        ],
        "severity": "high",
        "pesticides": [
            "Ridomil Gold MZ (Metalaxyl-M + Mancozeb)",
            "Infinito (Propamocarb + Fluopicolide)",
            "Revus (Mandipropamid)",
            "Forum (Dimethomorph)",
        ],
    },

    "Tomato_Leaf_Mold": {
        "description": (
            "Leaf mold (Fulvia fulva / Passalora fulva) thrives in high humidity "
            "(>85%) and moderate temperatures. Common in greenhouse-grown tomatoes."
        ),
        "symptoms": (
            "Pale green or yellowish patches on upper leaf surface with olive-green "
            "to brown velvety mould on the underside. Severely infected leaves curl "
            "upward and drop prematurely."
        ),
        "treatment": [
            "Reduce greenhouse humidity below 85% — improve ventilation.",
            "Remove and destroy infected leaves.",
            "Apply fungicides: Chlorothalonil, Copper fungicides, or Fenhexamid.",
        ],
        "prevention": [
            "Use leaf mold-resistant tomato varieties (e.g., Clarance, Blitz).",
            "Maintain good ventilation in greenhouses.",
            "Avoid dense planting — allow air flow.",
            "Water early morning to allow foliage to dry during the day.",
        ],
        "severity": "medium",
        "pesticides": [
            "Bravo WeatherStik (Chlorothalonil)",
            "Teldor (Fenhexamid)",
            "Copper-based fungicides",
        ],
    },

    "Tomato_Septoria_leaf_spot": {
        "description": (
            "Septoria leaf spot (Septoria lycopersici) is a very common fungal "
            "disease that starts on lower leaves and moves upward, causing premature "
            "defoliation and yield loss."
        ),
        "symptoms": (
            "Numerous small circular spots (3–5 mm) with white-grey centres and dark "
            "brown borders on lower leaves. Dark specks (pycnidia) visible in spot "
            "centres. Severe infection causes complete defoliation."
        ),
        "treatment": [
            "Remove infected lower leaves promptly.",
            "Apply Chlorothalonil, Mancozeb, or Copper fungicides every 7–10 days.",
            "Ensure adequate plant nutrition to support recovery.",
        ],
        "prevention": [
            "Rotate away from tomato and solanaceous crops for 2 years.",
            "Stake plants to improve air circulation.",
            "Use mulch to prevent soil splash.",
            "Remove and destroy plant debris at season end.",
        ],
        "severity": "medium",
        "pesticides": [
            "Bravo WeatherStik (Chlorothalonil)",
            "Dithane M-45 (Mancozeb)",
            "Copper Octanoate",
            "Amistar (Azoxystrobin)",
        ],
    },

    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "description": (
            "Two-spotted spider mite (Tetranychus urticae) is an arachnid pest, not "
            "a fungal disease. It thrives in hot, dry conditions and can cause rapid "
            "leaf damage and crop loss."
        ),
        "symptoms": (
            "Tiny yellow or white speckles on upper leaf surface (stippling). Leaves "
            "turn bronze, then brown and dry. Fine webbing visible on underside of "
            "leaves. Tiny moving mites visible under magnification."
        ),
        "treatment": [
            "Apply miticides/acaricides: Abamectin, Bifenazate, or Spiromesifen.",
            "Use insecticidal soap or neem oil sprays — cover underside of leaves thoroughly.",
            "Release predatory mites (Phytoseiulus persimilis) as biological control.",
            "Avoid excessive nitrogen fertilisation which promotes mite populations.",
        ],
        "prevention": [
            "Monitor plants regularly, especially during hot/dry weather.",
            "Maintain adequate soil moisture — mites prefer drought-stressed plants.",
            "Use reflective mulches to deter mites.",
            "Avoid broad-spectrum insecticides that kill natural predators.",
        ],
        "severity": "medium",
        "pesticides": [
            "Agri-Mek (Abamectin)",
            "Floramite (Bifenazate)",
            "Oberon (Spiromesifen)",
            "Neem Oil (organic option)",
        ],
    },

    "Tomato__Target_Spot": {
        "description": (
            "Target spot (Corynespora cassiicola) is a fungal disease producing "
            "distinctive concentric ring lesions on tomato leaves, stems, and fruits."
        ),
        "symptoms": (
            "Brown spots with concentric rings (target-board appearance) on leaves. "
            "Spots have yellow halos and may cause premature leaf drop. "
            "On fruit: sunken, dark lesions with concentric rings."
        ),
        "treatment": [
            "Remove and destroy infected leaves and fruit.",
            "Apply fungicides: Chlorothalonil, Mancozeb, or Fluxapyroxad.",
            "Repeat applications every 7–14 days during wet weather.",
        ],
        "prevention": [
            "Improve air circulation through staking and proper spacing.",
            "Avoid wetting foliage during irrigation.",
            "Use plastic mulch to reduce soil splash.",
            "Rotate crops and remove all debris after harvest.",
        ],
        "severity": "medium",
        "pesticides": [
            "Bravo WeatherStik (Chlorothalonil)",
            "Mancozeb 80 WP",
            "Merivon (Fluxapyroxad + Pyraclostrobin)",
        ],
    },

    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "description": (
            "Tomato Yellow Leaf Curl Virus (TYLCV) is a devastating viral disease "
            "transmitted by the whitefly Bemisia tabaci. There is no cure — "
            "management focuses on prevention and vector control."
        ),
        "symptoms": (
            "Upward curling and yellowing of young leaves, giving them a cup-like "
            "appearance. Stunted plant growth, reduced fruit size, and low yield. "
            "Flowers may drop before fruit sets."
        ),
        "treatment": [
            "Remove and destroy infected plants to prevent spread.",
            "Control whitefly vectors using imidacloprid or thiamethoxam systemic insecticides.",
            "Apply neem oil or insecticidal soap to reduce whitefly populations.",
            "Use yellow sticky traps to monitor and trap whiteflies.",
        ],
        "prevention": [
            "Plant TYLCV-resistant tomato varieties (e.g., Ty-1 gene carriers).",
            "Use reflective silver mulches to repel whiteflies.",
            "Install 50-mesh insect-proof netting in greenhouses.",
            "Avoid planting near other infected solanaceous crops.",
            "Apply prophylactic systemic insecticides at transplanting.",
        ],
        "severity": "high",
        "pesticides": [
            "Admire (Imidacloprid) — for whitefly vector control",
            "Actara (Thiamethoxam) — systemic whitefly control",
            "Neem Oil — organic whitefly repellent",
            "Movento (Spirotetramat) — phloem-active insecticide",
        ],
    },

    "Tomato__Tomato_mosaic_virus": {
        "description": (
            "Tomato mosaic virus (ToMV) is a highly stable RNA virus that can "
            "persist on tools, hands, and clothing for years. It is mechanically "
            "transmitted and causes significant quality loss."
        ),
        "symptoms": (
            "Mosaic pattern of light and dark green on leaves. Leaves may show "
            "mottling, curling, or fern-like distortion. Fruits may have uneven "
            "ripening, internal browning, and reduced size."
        ),
        "treatment": [
            "Remove and destroy infected plants immediately.",
            "Disinfect all tools, stakes, and hands with 10% bleach solution or 70% alcohol.",
            "There is no chemical cure for viral infections — focus on containment.",
        ],
        "prevention": [
            "Use ToMV-resistant varieties with Tm-2 resistance gene.",
            "Use disease-free transplants and seeds.",
            "Wash hands thoroughly before and after handling plants.",
            "Control aphids and other sap-sucking insects that may spread virus.",
            "Avoid using tobacco products near tomato plants (TMV cross-infection risk).",
        ],
        "severity": "high",
        "pesticides": [
            "No direct pesticide treatment for virus.",
            "Control insect vectors with Imidacloprid or Pyrethrins.",
        ],
    },

    "Tomato_healthy": {
        "description": "Your tomato plant appears healthy with no signs of disease or pest infestation.",
        "symptoms": "Leaves are uniformly dark green without spots, lesions, curling, or discoloration.",
        "treatment": [
            "Continue regular monitoring and scouting (every 3–5 days).",
            "Maintain consistent watering schedule to avoid stress.",
        ],
        "prevention": [
            "Apply balanced fertiliser to maintain plant vigour.",
            "Stake plants to keep foliage off the ground.",
            "Practice preventive fungicide sprays during high-humidity periods.",
            "Practice 2-3 year crop rotation.",
        ],
        "severity": "low",
        "pesticides": [],
    },

    "PlantVillage_mixed": {
        "description": "The plant appears healthy based on the image analysis.",
        "symptoms": "No significant disease symptoms detected in the uploaded image.",
        "treatment": [
            "Continue regular plant monitoring.",
            "Maintain good agricultural practices.",
        ],
        "prevention": [
            "Ensure proper spacing, watering, and nutrition.",
            "Scout regularly for early signs of pests or disease.",
        ],
        "severity": "low",
        "pesticides": [],
    },
}


def get_recommendation(disease_name: str) -> dict:
    """
    Return the recommendation dict for 'disease_name'.
    Falls back to a generic healthy response if the class is unknown.
    """
    if disease_name in RECOMMENDATIONS:
        return RECOMMENDATIONS[disease_name]

    # Fallback for any unknown class
    return {
        "description": f"Analysis result: {disease_name.replace('_', ' ')}.",
        "symptoms": "Please consult an agricultural expert for precise diagnosis.",
        "treatment": [
            "Consult your local agricultural extension officer.",
            "Collect a physical sample for laboratory testing.",
        ],
        "prevention": [
            "Maintain good field hygiene.",
            "Follow integrated pest management (IPM) practices.",
        ],
        "severity": "medium",
        "pesticides": [],
    }
