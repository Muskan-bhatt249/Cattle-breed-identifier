/* ========= Languages ========= */
const LANGUAGES = { en: "English", hi: "हिन्दी", mr: "मराठी", gu: "ગુજરાતી" };

const translations = {
  en: {
    "nav-home": "Home",
    "nav-breeds": "Breeds",
    "nav-identify": "Identify",
    "all_breeds": "All Breeds",
    "cattle_heading": "Cattle Breeds",
    "buffalo_heading": "Buffalo Breeds",
    "footer_text": "Preserving India’s Heritage"
  },
  hi: {
    "nav-home": "होम",
    "nav-breeds": "नस्लें",
    "nav-identify": "पहचानें",
    "all_breeds": "सभी नस्लें",
    "cattle_heading": "गाय की नस्लें",
    "buffalo_heading": "भैंस की नस्लें",
    "footer_text": "भारत की धरोहर संरक्षित करना"
  },
  mr: {
    "nav-home": "मुख्यपृष्ठ",
    "nav-breeds": "वंश",
    "nav-identify": "ओळखा",
    "all_breeds": "सर्व वंश",
    "cattle_heading": "गायीचे वंश",
    "buffalo_heading": "म्हशीचे वंश",
    "footer_text": "भारताचा वारसा जतन करणे"
  },
  gu: {
    "nav-home": "હોમ",
    "nav-breeds": "જાતિઓ",
    "nav-identify": "ઓળવો",
    "all_breeds": "બધી જાતિઓ",
    "cattle_heading": "ગાયની જાતિઓ",
    "buffalo_heading": "ભેંસની જાતિઓ",
    "footer_text": "ભારતની વારસાની રક્ષા"
  }
};

function getSavedLang(){ const l=localStorage.getItem("siteLang"); return l&&LANGUAGES[l]?l:"en"; }
function saveLang(l){ localStorage.setItem("siteLang", l); }
function populateLanguageSelectors(){
  document.querySelectorAll("#langSelect").forEach(select=>{
    if(select.options.length===0){
      Object.keys(LANGUAGES).forEach(code=>{
        const opt=document.createElement("option"); opt.value=code; opt.textContent=LANGUAGES[code]; select.appendChild(opt);
      });
    }
    select.value=getSavedLang();
    select.addEventListener("change", e=> setLanguage(e.target.value));
  });
}
function setLanguage(lang){
  saveLang(lang);
  document.querySelectorAll("[data-i18n]").forEach(el=>{
    const key=el.getAttribute("data-i18n");
    if(translations[lang] && translations[lang][key]) el.textContent = translations[lang][key];
  });
  document.querySelectorAll("[data-i18n-breed]").forEach(el=>{
    const slug=el.getAttribute("data-i18n-breed");
    if(breedDetails[slug] && breedDetails[slug].name[lang]) el.textContent = breedDetails[slug].name[lang];
  });
  const modal=document.getElementById("breedModal");
  if(modal && modal.dataset.currentBreed) updateModalContent(modal.dataset.currentBreed, lang);
}

/* ========= Breed Data (23 breeds) ========= */
const breedDetails = {
  // — Existing from your list —
  amritmahal:{img:"assets/amritmahal.jpg", name:{en:"Amritmahal",hi:"अमृतमहल",mr:"अमृतमहल",gu:"અમૃતમહલ"}, info:{en:"Origin: Karnataka. Strong draught breed.",hi:"मूल: कर्नाटक। मज़बूत बैल नस्ल।",mr:"मूळ: कर्नाटक. मजबूत बैल जात.",gu:"મૂળ: કર્ણાટક. મજબૂત બળદ જાતિ."}, milk:"2–4 L/day", traits:"Strong draught, endurance", pair:"Deoni", cost:"₹45,000–70,000"},
  kangayam:{img:"assets/kangayam.jpg", name:{en:"Kangayam",hi:"कांगायम",mr:"कांगायम",gu:"કાંગાયમ"}, info:{en:"Origin: Tamil Nadu. Hardy draught cattle.",hi:"मूल: तमिलनाडु। कठोर बैल नस्ल।",mr:"मूळ: तामिळनाडू. कणखर बैल जात.",gu:"મૂળ: તમિલનાડુ. કઠોર બળદ જાતિ."}, milk:"3–5 L/day", traits:"Heat tolerant, hardy", pair:"Jersey", cost:"₹50,000–80,000"},
  bargur:{img:"assets/bargur.jpg", name:{en:"Bargur",hi:"बरगुर",mr:"बरगुर",gu:"બર્ગુર"}, info:{en:"Origin: Tamil Nadu. Agile; hilly terrain.",hi:"मूल: तमिलनाडु। पहाड़ी इलाकों में उपयोगी।",mr:"मूळ: तामिळनाडू. डोंगराळ भागात उपयुक्त.",gu:"મૂળ: તમિલનાડુ. પહાડી વિસ્તારો માટે યોગ્ય."}, milk:"2–3 L/day", traits:"Agile, hilly terrain use", pair:"Kangayam", cost:"₹35,000–60,000"},
  umblachery:{img:"assets/umblachery.jpg", name:{en:"Umblachery",hi:"उम्बलाचेरी",mr:"उम्बलाचेरी",gu:"ઉમ્બલાચેરી"}, info:{en:"Origin: Tamil Nadu. Good draught; disease resistance.",hi:"मूल: तमिलनाडु। अच्छा बैल, रोग प्रतिरोध।",mr:"मूळ: तामिळनाडू. चांगला बैल, रोग प्रतिकार.",gu:"મૂળ: તમિલનાડુ. સારું બળદ, રોગ પ્રતિરોધક."}, milk:"3–5 L/day", traits:"Good draught, disease resistant", pair:"Hariana", cost:"₹40,000–65,000"},
  pulikulam:{img:"assets/pulikulam.jpg", name:{en:"Pulikulam",hi:"पुलिकुलम",mr:"पुलिकुलम",gu:"પુલિકુલમ"}, info:{en:"Origin: Tamil Nadu. Hardy; famous in Jallikattu.",hi:"मूल: तमिलनाडु। जल्लीकट्टू में प्रसिद्ध।",mr:"मूळ: तामिळनाडू. जल्लीकट्टूसाठी प्रसिद्ध.",gu:"મૂળ: તમિલનાડુ. જલિકટ્ટુમાં પ્રખ્યાત."}, milk:"2–3 L/day", traits:"Hardy, Jallikattu", pair:"Kangayam", cost:"₹35,000–55,000"},
  hariana:{img:"assets/hariana.jpg", name:{en:"Hariana",hi:"हरियाणा",mr:"हरियाणा",gu:"હરિયાણા"}, info:{en:"Origin: Haryana. Dual-purpose breed.",hi:"मूल: हरियाणा। दूध व बैल दोनों।",mr:"मूळ: हरियाणा. दुहेरी उद्देश.",gu:"મૂળ: હરિયાણા. દૂધ અને બળદ."}, milk:"5–10 L/day", traits:"Dual-purpose", pair:"Holstein Friesian", cost:"₹55,000–90,000"},
  deoni:{img:"assets/deoni.jpg", name:{en:"Deoni",hi:"देओनी",mr:"देओनी",gu:"દેઓની"}, info:{en:"Origin: Maharashtra. Dual-purpose; disease resistant.",hi:"मूल: महाराष्ट्र। दुग्ध व बैल; रोग प्रतिरोध।",mr:"मूळ: महाराष्ट्र. दुहेरी उपयोग; रोग प्रतिकार.",gu:"મૂળ: મહારાષ્ટ્ર. દૂધ/બળદ; રોગ પ્રતિરોધક."}, milk:"8–10 L/day", traits:"Dual-purpose, disease resistant", pair:"Amritmahal", cost:"₹60,000–95,000"},
  jersey:{img:"assets/Jersey.jpeg", name:{en:"Jersey",hi:"जर्सी",mr:"जर्सी",gu:"જર્સી"}, info:{en:"Origin: Channel Islands. High fat milk.",hi:"मूल: चैनल द्वीप। उच्च वसा दूध।",mr:"मूळ: चॅनेल बेटे. जास्त चरबी दूध.",gu:"મૂળ: ચેનલ આઇલેન્ડ્સ. ઉચ્ચ ચરબી દૂધ."}, milk:"15–20 L/day", traits:"High fat milk, adaptable", pair:"Kangayam", cost:"₹80,000–1,20,000"},
  holstein:{img:"assets/Holstein Friesian.jpg", name:{en:"Holstein Friesian",hi:"होल्स्टीन फ्रिज़ियन",mr:"होल्स्टीन फ्रिज़ियन",gu:"હોલ્સ્ટીન ફ્રિઝિયન"}, info:{en:"Origin: Netherlands. Highest milk yields.",hi:"मूल: नीदरलैंड। सर्वाधिक दुग्ध।",mr:"मूळ: नेदरलँड्स. सर्वाधिक दूध.",gu:"મૂળ: નેધરલેન્ડ. સર્વોચ્ચ દૂધ."}, milk:"25–30 L/day", traits:"Highest milk yield", pair:"Hariana", cost:"₹1,00,000–1,50,000"},
  brownswiss:{img:"assets/brownswiss.jpg", name:{en:"Brown Swiss",hi:"ब्राउन स्विस",mr:"ब्राउन स्विस",gu:"બ્રાઉન સ્વિસ"}, info:{en:"Origin: Switzerland. High protein milk.",hi:"मूल: स्विट्जरलैंड। उच्च प्रोटीन दूध।",mr:"मूळ: स्वित्झर्लंड. उच्च प्रथिन.",gu:"મૂળ: સ્વિટ્ઝર્લૅન્ડ. ઉચ્ચ પ્રોટીન દૂધ."}, milk:"18–22 L/day", traits:"Docile, high protein milk", pair:"Jersey", cost:"₹90,000–1,40,000"},
  reddane:{img:"assets/reddane.jpg", name:{en:"Red Dane",hi:"रेड डेन",mr:"रेड डेन",gu:"રેડ ડેન"}, info:{en:"Origin: Denmark. Balanced production.",hi:"मूल: डेनमार्क। संतुलित उत्पादन।",mr:"मूळ: डेन्मार्क. संतुलित उत्पादन.",gu:"મૂળ: ડેનમાર્ક. સંતુલિત ઉત્પાદન."}, milk:"15–20 L/day", traits:"Balanced production", pair:"Brown Swiss", cost:"₹85,000–1,30,000"},
  ayrshire:{img:"assets/ayrshier.jpg", name:{en:"Ayrshire",hi:"एयर्शायर",mr:"एयर्शायर",gu:"એયરશાયર"}, info:{en:"Origin: Scotland. Efficient grazers.",hi:"मूल: स्कॉटलैंड। घास चरने में कुशल।",mr:"मूळ: स्कॉटलंड. कार्यक्षम चारण.",gu:"મૂળ: સ્કોટલેન્ડ. ઘાસ ચરવામાં કુશળ."}, milk:"20–25 L/day", traits:"Efficient grazers", pair:"Jersey", cost:"₹95,000–1,35,000"},
  toda:{img:"assets/toda.jpg", name:{en:"Toda Buffalo",hi:"टोडा भैंस",mr:"टोडा म्हैस",gu:"ટોડા ભેંસ"}, info:{en:"Origin: Nilgiris. High fat buffalo milk.",hi:"मूल: नीलगिरि। उच्च वसा दूध।",mr:"मूळ: निलगिरी. जास्त चरबी दूध.",gu:"મૂળ: નીલગિરી. ઉચ્ચ ચરબી દૂધ."}, milk:"4–6 L/day", traits:"High fat milk", pair:"Murrah", cost:"₹70,000–1,00,000"},
  murrah:{img:"assets/murrah.jpg", name:{en:"Murrah",hi:"मुर्रा",mr:"मुर्रा",gu:"મુર્રાહ"}, info:{en:"Origin: Haryana/Punjab. Top milch buffalo.",hi:"मूल: हरियाणा/पंजाब। प्रमुख दुग्ध भैंस।",mr:"मूळ: हरियाणा/पंजाब. प्रमुख दूधाळ.",gu:"મૂળ: હરિયાણા/પંજાબ. મુખ્ય દૂધાળ."}, milk:"25–30 L/day", traits:"Top buffalo breed; high fat", pair:"Surti", cost:"₹1,00,000–1,50,000"},
  surti:{img:"assets/surti.webp", name:{en:"Surti",hi:"सुरती",mr:"सुरती",gu:"સુરતી"}, info:{en:"Origin: Gujarat. High fat, medium yield.",hi:"मूल: गुजरात। उच्च वसा; मध्यम उत्पादन।",mr:"मूळ: गुजरात. उच्च चरबी; मध्यम उत्पादन.",gu:"મૂળ: ગુજરાત. ઊંચી ચરબી; મધ્યમ ઉત્પાદન."}, milk:"8–10 L/day", traits:"Compact, high fat", pair:"Murrah", cost:"₹70,000–1,10,000"},
  gir:{img:"assets/gir.jpg", name:{en:"Gir",hi:"गिर",mr:"गिर",gu:"ગીર"}, info:{en:"Origin: Gujarat. High fat milk; hardy.",hi:"मूल: गुजरात। ऊंची वसा; कणखर।",mr:"मूळ: गुजरात. जास्त चरबी; कणखर.",gu:"મૂળ: ગુજરાત. ઊંચી ચરબી; કઠોર."}, milk:"12–20 L/day", traits:"High fat, disease resistant", pair:"Holstein", cost:"₹80,000–1,20,000"},
  sahiwal:{img:"assets/sahiwal.jpg", name:{en:"Sahiwal",hi:"साहीवाल",mr:"साहीवाल",gu:"સાહિવાલ"}, info:{en:"Origin: Punjab. Excellent milch zebu.",hi:"मूल: पंजाब। उत्तम दुग्ध।",mr:"मूळ: पंजाब. उत्कृष्ट दूधाळ.",gu:"મૂળ: પંજાબ. ઉત્તમ દૂધાળ."}, milk:"10–18 L/day", traits:"Good temperament; heat tolerant", pair:"Holstein", cost:"₹85,000–1,30,000"},
  kankrej:{img:"assets/kankreja.jpg", name:{en:"Kankrej",hi:"कांकरेज",mr:"कांकरेज",gu:"કાંક્રેજ"}, info:{en:"Origin: Gujarat/Rajasthan. Dual-purpose.",hi:"मूल: गुजरात/राजस्थान। दुहेरी उपयोग।",mr:"मूळ: गुजरात/राज. दुहेरी उपयोग.",gu:"મૂળ: ગુજરાત/રાજ. દ્વિહેતુ."}, milk:"8–12 L/day", traits:"Draught + dairy", pair:"Jersey", cost:"₹60,000–1,00,000"},
  tharparkar:{img:"assets/tharparkar.jpg", name:{en:"Tharparkar",hi:"थारपारकर",mr:"थारपारकर",gu:"થારપારકર"}, info:{en:"Origin: Thar desert. Good dairy zebu.",hi:"मूल: थार। अच्छा दुग्ध।",mr:"मूळ: थार. चांगले दूध.",gu:"મૂળ: થાર. સારું દૂધ."}, milk:"8–12 L/day", traits:"Heat tolerant", pair:"Holstein", cost:"₹70,000–1,10,000"},
  red_sindhi:{img:"assets/redsindhi.webp", name:{en:"Red Sindhi",hi:"रेड सिंधी",mr:"रेड सिंधी",gu:"રેડ સિંધિ"}, info:{en:"Origin: Sindh. Good milk and fat.",hi:"मूल: सिंध। अच्छा दूध/वसा।",mr:"मूळ: सिंध. चांगले दूध/चरबी.",gu:"મૂળ: સિંધ. સારું દૂધ/ચરબી."}, milk:"8–12 L/day", traits:"High fat; hardy", pair:"Jersey", cost:"₹65,000–1,00,000"},
  rathi:{img:"assets/rathi.jpg", name:{en:"Rathi",hi:"राठी",mr:"राठी",gu:"રાઠી"}, info:{en:"Origin: Rajasthan. Adapted to arid zones.",hi:"मूल: राजस्थान। शुष्क अनुकूल।",mr:"मूळ: राजस्थान. कोरड्या भागात अनुकूल.",gu:"મૂળ: રાજસ્થાન. શુષ્ક અનુકૂળ."}, milk:"6–10 L/day", traits:"Heat tolerant", pair:"Holstein", cost:"₹55,000–90,000"},
  ongole:{img:"assets/ongole.jpg", name:{en:"Ongole",hi:"ओंगोल",mr:"ओंगोले",gu:"ઓંગોલે"}, info:{en:"Origin: Andhra Pradesh. Heavy draught.",hi:"मूल: आंध्र। भारी बैल।",mr:"मूळ: आंध्र. जड बैल.",gu:"મૂળ: આંધ્ર. ભારે બળદ."}, milk:"3–5 L/day", traits:"Strong draught", pair:"Jersey", cost:"₹50,000–80,000"},
  vechur:{img:"assets/vechur.jpg", name:{en:"Vechur",hi:"वेचुर",mr:"वेचुर",gu:"વેચુર"}, info:{en:"Origin: Kerala. Dwarf cattle; low input.",hi:"मूल: केरल। बौनी; कम खर्च।",mr:"मूळ: केरळ. बोने; कमी खर्च.",gu:"મૂળ: કેરળ. બૌને; ઓછું ખર્ચ."}, milk:"2–3 L/day", traits:"Low input, hardy", pair:"Gir", cost:"₹40,000–70,000"},
  jaffarabadi:{img:"assets/jaffrabadi.jpg", name:{en:"Jaffarabadi",hi:"जाफराबादी",mr:"जाफराबादी",gu:"જાફરાબાદી"}, info:{en:"Origin: Gujarat. Large buffalo; high fat.",hi:"मूल: गुजरात। बड़ी भैंस; उच्च वसा।",mr:"मूळ: गुजरात. मोठी म्हैस; जास्त चरबी.",gu:"મૂળ: ગુજરાત. મોટી ભેંસ; ઊંચી ચરબી."}, milk:"10–14 L/day", traits:"Robust; high fat", pair:"Surti", cost:"₹1,00,000–1,60,000"},
  mehsana:{img:"assets/mehsana.jpg", name:{en:"Mehsana",hi:"मेहसाणा",mr:"मेहसाणा",gu:"મેહસાણા"}, info:{en:"Origin: Gujarat. Murrah×Surti type.",hi:"मूल: गुजरात। मुर्रा×सुरती।",mr:"मूळ: गुजरात. मुर्रा×सुरती.",gu:"મૂળ: ગુજરાત. મુર્રા×સુરતી."}, milk:"8–12 L/day", traits:"Good milk fat", pair:"Murrah", cost:"₹80,000–1,30,000"},
  pandharpuri:{img:"assets/pandharpuri.jpg", name:{en:"Pandharpuri",hi:"पंढरपुरी",mr:"पंढरपुरी",gu:"પંઢરપુરી"}, info:{en:"Origin: Maharashtra. Long sickle horns.",hi:"मूल: महाराष्ट्र। लंबी सींग।",mr:"मूळ: महाराष्ट्र. लांब वाकडी शिंगे.",gu:"મૂળ: મહારાષ્ટ્ર. લાંબા શિંગડા."}, milk:"6–8 L/day", traits:"Adapted to dry zones", pair:"Murrah", cost:"₹70,000–1,00,000"},
  nili_ravi:{img:"assets/nilliravi.webp", name:{en:"Nili-Ravi",hi:"नीली-रवि",mr:"नीली-रवि",gu:"નીલી-રવિ"}, info:{en:"Origin: Punjab. Elite milch buffalo.",hi:"मूल: पंजाब। उत्कृष्ठ दुग्ध।",mr:"मूळ: पंजाब. उत्कृष्ट दूधाळ.",gu:"મૂળ: પંજાબ. ઉત્તમ દૂધાળ."}, milk:"20–25 L/day", traits:"High yield; good fat", pair:"Murrah", cost:"₹1,00,000–1,50,000"}
};

/* ========= Labels for modal ========= */
function translateField(field, lang) {
  const labels = {
    en: { "Milk Production":"Milk Production", "Best Traits":"Best Traits", "Best Paired With":"Best Paired With", "Estimated Cost":"Estimated Cost" },
    hi: { "Milk Production":"दूध उत्पादन", "Best Traits":"सर्वश्रेष्ठ गुण", "Best Paired With":"किसके साथ सर्वोत्तम", "Estimated Cost":"अनुमानित लागत" },
    mr: { "Milk Production":"दुध उत्पादन", "Best Traits":"सर्वोत्तम गुणधर्म", "Best Paired With":"कोणासोबत सर्वोत्तम", "Estimated Cost":"अनुमानित किंमत" },
    gu: { "Milk Production":"દૂધ ઉત્પાદન", "Best Traits":"શ્રેષ્ઠ લક્ષણો", "Best Paired With":"કયાં સાથે શ્રેષ્ઠ", "Estimated Cost":"અંદાજિત કિંમત" }
  };
  return labels[lang] && labels[lang][field] ? labels[lang][field] : field;
}

/* ========= Modal ========= */
function openModalForBreed(slug){
  const modal=document.getElementById("breedModal");
  if(!modal) return;
  modal.style.display="flex";
  modal.setAttribute("aria-hidden","false");
  modal.dataset.currentBreed=slug;
  updateModalContent(slug, getSavedLang());
}
function updateModalContent(slug, lang){
  const breed=breedDetails[slug]; if(!breed) return;
  document.getElementById("modalImage").src=breed.img;
  document.getElementById("modalTitle").textContent=breed.name[lang]||breed.name.en;
  document.getElementById("modalDetails").innerHTML=`
    <li><strong>${translateField("Milk Production", lang)}:</strong> ${breed.milk}</li>
    <li><strong>${translateField("Best Traits", lang)}:</strong> ${breed.traits}</li>
    <li><strong>${translateField("Best Paired With", lang)}:</strong> ${breed.pair||"—"}</li>
    <li><strong>${translateField("Estimated Cost", lang)}:</strong> ${breed.cost||"—"}</li>
    <li class="text-gray-600"><em>${breed.info[lang]||breed.info.en}</em></li>
  `;
}
function closeModal(){
  const modal=document.getElementById("breedModal");
  if(!modal) return;
  modal.style.display="none";
  modal.setAttribute("aria-hidden","true");
  delete modal.dataset.currentBreed;
}

/* ========= HERO Carousel ========= */
/* ======== HERO Carousel ======== */
let heroIndex = 0, heroSlides, heroTimer;

function showHero(n) {
  heroSlides.forEach((s, i) => {
    if (i === n) {
      s.style.opacity = "1";
      s.style.zIndex = "1";
    } else {
      s.style.opacity = "0";
      s.style.zIndex = "0";
    }
  });
}

function nextHero() {
  heroIndex = (heroIndex + 1) % heroSlides.length;
  showHero(heroIndex);
}

function prevHero() {
  heroIndex = (heroIndex - 1 + heroSlides.length) % heroSlides.length;
  showHero(heroIndex);
}

function startHero() {
  heroSlides = document.querySelectorAll(".hero-slide");
  if (heroSlides.length === 0) return;

  showHero(heroIndex);
  heroTimer = setInterval(nextHero, 4000);

  const nextBtn = document.querySelector(".hero-next");
  const prevBtn = document.querySelector(".hero-prev");

  if (nextBtn) nextBtn.addEventListener("click", () => { nextHero(); resetHero(); });
  if (prevBtn) prevBtn.addEventListener("click", () => { prevHero(); resetHero(); });
}

function resetHero() {
  clearInterval(heroTimer);
  heroTimer = setInterval(nextHero, 4000);
}

document.addEventListener("DOMContentLoaded", startHero);


/* ========= Marquee (dual carousels) ========= */
function cardHTML(slug){
  const b=breedDetails[slug]; if(!b) return "";
  return `
    <div class="min-w-[220px] max-w-[220px] bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden cursor-pointer" data-breed="${slug}">
      <img src="${b.img}" alt="${b.name.en}" class="h-36 w-full object-cover">
      <div class="p-3">
        <div class="font-semibold text-sm" data-i18n-breed="${slug}">${b.name.en}</div>
        <div class="text-xs text-gray-600">${b.milk} • ${b.traits}</div>
      </div>
    </div>
  `;
}
function buildMarquees(){
  const featured=['gir','sahiwal','murrah','holstein','jersey','deoni','hariana','kangayam'];
  const allKeys=Object.keys(breedDetails);
  const remaining=allKeys.filter(k=>!featured.includes(k));
  const top=document.getElementById("marqueeTopTrack");
  const bot=document.getElementById("marqueeBottomTrack");
  if(top){ top.innerHTML = [...featured, ...featured].map(cardHTML).join(""); }
  if(bot){ bot.innerHTML = [...remaining, ...remaining].map(cardHTML).join(""); }
}

// Ensure both marquees move at same pixel speed regardless of content width
function normalizeMarqueeSpeeds(){
  const SPEED_PX_PER_S = 50; // slower, comfortable reading speed
  [
    document.getElementById("marqueeTopTrack"),
    document.getElementById("marqueeBottomTrack")
  ].forEach(track=>{
    if(!track) return;
    // Total distance animated is 50% of track width
    const w = track.scrollWidth || track.offsetWidth || 0;
    if(w>0){
      const durationSec = (w * 0.5) / SPEED_PX_PER_S;
      track.style.animationDuration = `${durationSec}s`;
    }
  });
}

/* ========= Breeds Grid & Search ========= */
function buildBreedsGrid(){
  const grid=document.getElementById("breedGrid"); if(!grid) return;
  const lang=getSavedLang();
  grid.innerHTML = Object.keys(breedDetails).map(slug=>{
    const b=breedDetails[slug];
    return `
      <div class="bg-white rounded-2xl shadow hover:shadow-lg transition overflow-hidden cursor-pointer" data-breed="${slug}">
        <img src="${b.img}" alt="${b.name[lang]||b.name.en}" class="h-48 w-full object-cover">
        <div class="p-4">
          <h3 class="font-semibold text-lg" data-i18n-breed="${slug}">${b.name[lang]||b.name.en}</h3>
          <p class="text-sm text-gray-600 mt-1">${b.info[lang]||b.info.en}</p>
          <div class="mt-3 text-sm text-gray-700">${b.milk} • ${b.traits}</div>
        </div>
      </div>
    `;
  }).join("");
  const search=document.getElementById("breedSearch");
  if(search){
    search.addEventListener("input",(e)=>{
      const q=e.target.value.toLowerCase();
      Array.from(grid.children).forEach(card=>{
        const slug=card.getAttribute("data-breed");
        const b=breedDetails[slug];
        const hay=(b.name.en+" "+(b.traits||"")+" "+(b.info.en||"")).toLowerCase();
        card.style.display = hay.includes(q) ? "" : "none";
      });
    });
  }
}

/* ========= Identify Page ========= */
let identifyModel=null; let identifyLabels=[]; let identifyInputSize=224;
const API_BASE = (window.__IDENTIFY_API__ || "http://127.0.0.1:8000");

async function apiPredict(file){
  const fd=new FormData();
  fd.append("file", file, file.name||"upload.jpg");
  let res;
  const controller = new AbortController();
  const timeoutId = setTimeout(()=> controller.abort(), 20000); // 20s timeout
  try{
    res = await fetch(`${API_BASE}/predict`, { method:"POST", body: fd, mode:"cors", signal: controller.signal });
  }catch(err){
    const warn=document.getElementById("apiWarning");
    if(warn) warn.classList.remove("hidden");
    console.error("apiPredict: fetch error", err);
    clearTimeout(timeoutId);
    throw err;
  }
  clearTimeout(timeoutId);
  if(!res.ok){
    const warn=document.getElementById("apiWarning");
    if(warn) warn.classList.remove("hidden");
    throw new Error(`API ${res.status}`);
  }
  const data = await res.json();
  return data;
}

async function loadIdentifyAssets(){
  if(identifyModel && identifyLabels.length) return;
  if(typeof tf === "undefined") throw new Error("TensorFlow.js not loaded");
  const candidateBases=["train/", "models/", "assets/train/"];
  let lastErr;
  for(const base of candidateBases){
    try{
      identifyModel = await tf.loadGraphModel(`${base}model.json`);
    }catch(e){
      try{ identifyModel = await tf.loadLayersModel(`${base}model.json`); }
      catch(e2){ lastErr=e2; identifyModel=null; continue; }
    }
    // If model loaded, try labels next
    try{
      const res = await fetch(`${base}labels.json`, {cache:"no-store"});
      if(res.ok){ identifyLabels = await res.json(); }
      else { identifyLabels = []; }
    }catch(_){ identifyLabels = []; }
    // If labels missing, synthesize from model output
    if(identifyLabels.length===0){
      const out = identifyModel.outputs[0];
      const shape = out && out.shape ? out.shape : identifyModel.outputs[0].shape;
      const num = Array.isArray(shape) ? (shape[shape.length-1]||0) : 0;
      identifyLabels = Array.from({length:num}, (_,i)=>`Class ${i}`);
    }
    // store chosen base for later (optional)
    loadIdentifyAssets.base = base;
    break;
  }
  if(!identifyModel){
    throw new Error("Model not found at train/model.json (also tried models/ and assets/train/)");
  }
  // best guess input size if known
  const inTensor = identifyModel.inputs && identifyModel.inputs[0];
  const inShape = inTensor && inTensor.shape ? inTensor.shape : [];
  const h = inShape[inShape.length-3]; const w = inShape[inShape.length-2];
  if(Number.isInteger(h) && Number.isInteger(w) && h===w) identifyInputSize=h;
}

function preprocessImageForModel(imgEl){
  return tf.tidy(()=>{
    let t = tf.browser.fromPixels(imgEl);
    t = tf.image.resizeBilinear(t, [identifyInputSize, identifyInputSize]);
    t = t.toFloat().div(255);
    // If model expects grayscale or different channels, rely on broadcasting
    return t.expandDims(0);
  });
}

async function predictIdentify(imgEl){
  await loadIdentifyAssets();
  const input = preprocessImageForModel(imgEl);
  let logits;
  try{
    logits = identifyModel.execute ? identifyModel.execute(input) : identifyModel.predict(input);
  }catch(e){ input.dispose(); throw e; }
  const probs = tf.tidy(()=>{
    const p = Array.isArray(logits) ? logits[0] : logits;
    // If not normalized, apply softmax
    return tf.softmax(p);
  });
  const data = await probs.data();
  input.dispose(); probs.dispose(); if(Array.isArray(logits)) logits.forEach(x=>x.dispose()); else logits.dispose();
  let bestIdx=0; let best=data[0]||0;
  for(let i=1;i<data.length;i++){ if(data[i]>best){ best=data[i]; bestIdx=i; } }
  return { label: identifyLabels[bestIdx]||`Class ${bestIdx}`, confidence: best };
}

function initIdentify(){
  const fileUpload=document.getElementById("fileUpload");
  const preview=document.getElementById("preview");
  const previewImg=document.getElementById("previewImg");
  const identifyBtn=document.getElementById("identifyBtn");
  const result=document.getElementById("identifyResult");
  const predictionText=document.getElementById("predictionText");
  const confidenceBar=document.getElementById("confidenceBar");
  const confidenceFill = document.getElementById("confidenceFill");
  const confidenceValue = document.getElementById("confidenceValue");
  const setConfidenceBar = (pct)=>{
    if(!confidenceFill) return;
    const p = Math.max(0, Math.min(100, Number(pct)||0));
    const width = p; // 0-100 maps directly to 0-100%
    confidenceFill.style.width = `${width}%`;
    if(confidenceValue){ confidenceValue.textContent = `${Math.round(p)}%`; }
  };
  const breedInfoPanel=document.getElementById("breedInfoPanel");
  const breedInfoBody=document.getElementById("breedInfoBody");
  const processingStars=document.getElementById("processingStars");
  const dropzone=document.querySelector('label[for="fileUpload"]');
  let selectedFile=null;
  if(!fileUpload) return;
  // Disable identify until a file is chosen
  if(identifyBtn){ identifyBtn.disabled = true; identifyBtn.classList.add("opacity-60","cursor-not-allowed"); }
  fileUpload.addEventListener("change", e=>{
    const file=e.target.files[0];
    selectedFile=file||null;
    if(file){ previewImg.src=URL.createObjectURL(file); preview.classList.remove("hidden"); }
    if(identifyBtn){ identifyBtn.disabled = !file; identifyBtn.classList.toggle("opacity-60", !file); identifyBtn.classList.toggle("cursor-not-allowed", !file); }
  });
  // Prevent default browser open on drop anywhere
  ["dragover","drop"].forEach(evt=>{
    window.addEventListener(evt, e=>{ e.preventDefault(); }, false);
    document.addEventListener(evt, e=>{ e.preventDefault(); }, false);
  });
  // Dropzone interactions
  if(dropzone){
    dropzone.addEventListener("dragover", e=>{
      e.preventDefault();
      dropzone.classList.add("ring-2","ring-[#f9b233]");
    });
    dropzone.addEventListener("dragleave", ()=>{
      dropzone.classList.remove("ring-2","ring-[#f9b233]");
    });
    dropzone.addEventListener("drop", e=>{
      e.preventDefault();
      dropzone.classList.remove("ring-2","ring-[#f9b233]");
      const dt = e.dataTransfer;
      if(!dt || !dt.files || dt.files.length===0) return;
      const file = dt.files[0];
      selectedFile=file;
      previewImg.src=URL.createObjectURL(file);
      preview.classList.remove("hidden");
      if(identifyBtn){ identifyBtn.disabled = false; identifyBtn.classList.remove("opacity-60","cursor-not-allowed"); }
    });
  }
  identifyBtn && identifyBtn.addEventListener("click", async ()=>{
    result.classList.remove("hidden");
    // Reset panels
    if(breedInfoPanel) breedInfoPanel.classList.add("hidden");
    if(confidenceBar){ confidenceBar.classList.add("hidden"); const bar=confidenceBar.querySelector("div"); bar.style.width="0%"; bar.textContent=""; }
    if(processingStars) processingStars.classList.remove("hidden");
    predictionText.textContent = "Processing...";
    // Prefer backend API if available and file selected
    if(!selectedFile){
      predictionText.textContent = "Please upload an image first.";
      return;
    }
    if(selectedFile){
      try{
        console.log("Identify: calling API /predict at", API_BASE);
        const data = await apiPredict(selectedFile);
        const best = data && data.prediction ? data.prediction : null;
        if(best){
          const pct = Math.round((best.probability||0)*100);
          if(best.label === "Not a cow or buffalo"){
            predictionText.textContent = "❌ This doesn't appear to be a cow or buffalo. Please upload a clear image of cattle.";
            predictionText.className = "text-lg text-red-600 mb-3";
            // Show lower confidence for non-cattle detection
            setConfidenceBar(15);  // Fixed low confidence for non-cattle
          } else {
            predictionText.textContent = `Predicted Breed: ${best.label}`;
            predictionText.className = "text-lg text-gray-800 mb-3";
            setConfidenceBar(pct);
          }
          // remove vertical bar from view to use full width for gauge
          if(confidenceBar){ confidenceBar.classList.add("hidden"); }
          if(processingStars) processingStars.classList.add("hidden");
          // Breed info rendering from API (if available) - skip for non-cattle
          if(best.label !== "Not a cow or buffalo"){
            const info = data && data.info ? data.info : null;
            if(info && breedInfoPanel && breedInfoBody){
            const sections = [];
            if(info.description){
              sections.push(`<div><strong>Description:</strong> <span class="text-gray-700">${info.description}</span></div>`);
            }
            if(Array.isArray(info.characteristics) && info.characteristics.length){
              sections.push(`<div><strong>Characteristics:</strong><ul class="list-disc pl-5 mt-1">${info.characteristics.map(c=>`<li>${c}</li>`).join("")}</ul></div>`);
            }
            if(Array.isArray(info.fodder_requirements) && info.fodder_requirements.length){
              sections.push(`<div><strong>Fodder requirements:</strong><ul class="list-disc pl-5 mt-1">${info.fodder_requirements.map(f=>`<li>${f}</li>`).join("")}</ul></div>`);
            }
            if(Array.isArray(info.government_schemes) && info.government_schemes.length){
              sections.push(`<div><strong>Government schemes:</strong><ul class="list-disc pl-5 mt-1">${info.government_schemes.map(s=>`<li>${s}</li>`).join("")}</ul></div>`);
            }
            if(Array.isArray(info.best_practices) && info.best_practices.length){
              sections.push(`<div><strong>Best practices:</strong><ul class="list-disc pl-5 mt-1">${info.best_practices.map(b=>`<li>${b}</li>`).join("")}</ul></div>`);
            }
            breedInfoBody.innerHTML = sections.join("") || `<div class="text-gray-600">No detailed info available for this breed.</div>`;
            breedInfoPanel.classList.remove("hidden");
            }
          }
          return;
        }
        predictionText.textContent = "No prediction returned by API.";
        if(processingStars) processingStars.classList.add("hidden");
      }catch(err){
        const warn=document.getElementById("apiWarning");
        if(warn) warn.classList.remove("hidden");
        console.error("Identify: API error", err);
        if(processingStars) processingStars.classList.add("hidden");
        // fall through to TF.js
      }
    }
    // Fallback: run in-browser TF.js if present, else demo
    if(typeof tf !== "undefined"){
      try{
        const {label, confidence} = await predictIdentify(previewImg);
        predictionText.textContent = `Predicted Breed: ${label}`;
        if(confidenceBar){ confidenceBar.classList.add("hidden"); }
        if(processingStars) processingStars.classList.add("hidden");
        setConfidenceBar(Math.round(confidence*100));
        return;
      }catch(err){ console.error("Identify: TF.js error", err); /* continue to demo */ }
    }
    const keys=Object.keys(breedDetails);
    const pick=breedDetails[keys[Math.floor(Math.random()*keys.length)]];
    predictionText.textContent = `Predicted (demo): ${pick.name.en}`;
    if(confidenceBar){ confidenceBar.classList.add("hidden"); }
    if(processingStars) processingStars.classList.add("hidden");
    setConfidenceBar(10);
  });
}

/* ========= Subsidy Page (sample dynamic-ready) ========= */
const sampleSchemes = [
  { name:"Dairy Entrepreneurship Development Scheme", state:"Central", type:"Dairy", benefit:"Back-ended subsidy up to 25% on dairy units" },
  { name:"Fodder Development Program", state:"Maharashtra", type:"Fodder", benefit:"Support for fodder seed & silage units" },
  { name:"Livestock Insurance Scheme", state:"Central", type:"Insurance", benefit:"Premium subsidy for cattle insurance" },
  { name:"Gokul Mission - RGM", state:"Central", type:"Breeding", benefit:"Support for indigenous breed improvement" },
  { name:"Dairy Infra Development Fund", state:"Gujarat", type:"Infrastructure", benefit:"Interest subvention for processing plants" },
  { name:"Pashudhan Vikash Yojana", state:"Bihar", type:"Breeding", benefit:"Artificial insemination outreach" },
  { name:"Kamdhenu Scheme", state:"Rajasthan", type:"Dairy", benefit:"Support to dairy farmers for heifer rearing" },
  { name:"Nandini Scheme", state:"Karnataka", type:"Dairy", benefit:"Subsidy for dairy expansion & chilling" }
];
function initSubsidy(){
  const body=document.getElementById("schemeBody"); if(!body) return;
  const search=document.getElementById("schemeSearch");
  const stateFilter=document.getElementById("stateFilter");
  const typeFilter=document.getElementById("typeFilter");
  // populate states
  const states=[...new Set(sampleSchemes.map(s=>s.state))].sort();
  states.forEach(st=>{ const opt=document.createElement("option"); opt.value=st; opt.textContent=st; stateFilter.appendChild(opt); });
  function render(){
    const q=(search.value||"").toLowerCase();
    const st=stateFilter.value; const tp=typeFilter.value;
    const rows=sampleSchemes.filter(s=>{
      return (st? s.state===st : true) && (tp? s.type===tp : true) &&
             (s.name.toLowerCase().includes(q) || s.benefit.toLowerCase().includes(q));
    }).map(s=>`
      <tr class="border-t">
        <td class="px-4 py-3">${s.name}</td>
        <td class="px-4 py-3">${s.state}</td>
        <td class="px-4 py-3">${s.type}</td>
        <td class="px-4 py-3">${s.benefit}</td>
      </tr>
    `).join("");
    body.innerHTML = rows || `<tr><td class="px-4 py-3" colspan="4">No schemes found.</td></tr>`;
  }
  [search,stateFilter,typeFilter].forEach(el=> el.addEventListener("input", render));
  render();
}

/* ========= Milk Page (simple plan) ========= */
function initMilk(){
  const btn=document.getElementById("milkPlanBtn");
  if(!btn) return;
  const list=document.getElementById("milkPlanList");
  const wrap=document.getElementById("milkPlan");
  btn.addEventListener("click", ()=>{
    const breed=(document.getElementById("milkBreed").value||"").trim();
    const age=parseFloat(document.getElementById("milkAge").value||0);
    const yieldNow=parseFloat(document.getElementById("milkYield").value||0);
    const region=(document.getElementById("milkRegion").value||"").trim();
    const tips=[
      `Balanced ration with 16–18% CP; add mineral mixture.`,
      `Clean water ad-lib; ~60–80 L/day for high yielders.`,
      `Deworm quarterly; de-tick monthly; hoof care every 6–8 weeks.`,
      `Heat stress management: shade + misting in hot regions (${region||"region"}).`,
      `Breeding: AI at correct heat signs; maintain BCS 2.75–3.25.`,
      `Expected improvement: +10–25% over 8–12 weeks with consistency.`
    ];
    list.innerHTML = tips.map(t=>`<li>${t}</li>`).join("");
    wrap.classList.remove("hidden");
  });
}

/* ========= Price Estimator (simple mock) ========= */
function initPrice(){
  const btn=document.getElementById("priceBtn");
  if(!btn) return;
  const out=document.getElementById("priceText");
  const panel=document.getElementById("priceResult");
  btn.addEventListener("click", ()=>{
    const breed=(document.getElementById("priceBreed").value||"").toLowerCase();
    const age=+document.getElementById("priceAge").value||0;
    const y=+document.getElementById("priceYield").value||0;
    // simple heuristic
    let base=60000;
    if(breed.includes("murrah")||breed.includes("holstein")||breed.includes("gir")) base=100000;
    if(y>10) base+=40000; else if(y>6) base+=20000;
    if(age>=3 && age<=6) base+=15000;
    out.textContent = `₹${(base).toLocaleString("en-IN")}`;
    panel.classList.remove("hidden");
  });
}

/* ========= Navbar mobile toggle ========= */
function initNav(){
  const btn=document.getElementById("mobileMenuBtn");
  const menu=document.getElementById("mobileMenu");
  btn && btn.addEventListener("click", ()=> menu.classList.toggle("hidden"));
}

/* ========= Global Clicks (cards & modal close) ========= */
document.addEventListener("click", e=>{
  const card=e.target.closest("[data-breed]");
  if(card) openModalForBreed(card.dataset.breed);
  if(e.target.classList.contains("modal-close") || e.target.id==="breedModal") closeModal();
});

/* ========= Init ========= */
document.addEventListener("DOMContentLoaded", ()=>{
  initNav();
  populateLanguageSelectors();
  setLanguage(getSavedLang());

  startHero();
  buildMarquees();
  // After DOM has cards, compute consistent marquee speeds
  setTimeout(normalizeMarqueeSpeeds, 0);
  window.addEventListener("resize", ()=>{ setTimeout(normalizeMarqueeSpeeds, 100); });
  buildBreedsGrid();     // breeds page only (safe if grid absent)
  initIdentify();        // identify page only
  initSubsidy();         // subsidy page only
  initMilk();            // milk page only
  initPrice();           // price page only
});
