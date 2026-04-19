import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import datetime

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

st.set_page_config(page_title="Nexro Plant AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #060810; }
.stApp > header { background: transparent; }

/* NAV */
.nav-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.2rem 2rem; border-bottom: 1px solid #1a2235;
    background: rgba(6,8,16,0.95); backdrop-filter: blur(20px);
    position: sticky; top: 0; z-index: 100; margin-bottom: 0;
}
.nav-logo { font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800; color:white; letter-spacing:-0.03em; }
.nav-logo span { color:#00D4AA; }
.nav-badge { background:rgba(0,212,170,0.12); border:1px solid rgba(0,212,170,0.3); color:#00D4AA;
    padding:4px 12px; border-radius:100px; font-size:0.75rem; font-weight:600; letter-spacing:0.05em; }

/* HERO */
.hero { padding: 4rem 2rem 2rem; text-align: center; position: relative; overflow: hidden; }
.hero::before {
    content:''; position:absolute; top:-200px; left:50%; transform:translateX(-50%);
    width:600px; height:600px;
    background: radial-gradient(circle, rgba(0,212,170,0.07) 0%, transparent 70%);
    pointer-events:none;
}
.hero-tag { display:inline-flex; align-items:center; gap:8px; background:rgba(0,212,170,0.08);
    border:1px solid rgba(0,212,170,0.2); color:#00D4AA; padding:6px 16px;
    border-radius:100px; font-size:0.78rem; font-weight:600; letter-spacing:0.08em;
    text-transform:uppercase; margin-bottom:1.5rem; }
.hero-tag::before { content:''; width:6px; height:6px; background:#00D4AA; border-radius:50%;
    animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.7)} }
.hero h1 { font-family:'Syne',sans-serif; font-size:clamp(2.2rem,5vw,3.8rem); font-weight:800;
    color:white; letter-spacing:-0.04em; line-height:1.05; margin:0 0 1rem; }
.hero h1 span { color:#00D4AA; }
.hero-sub { color:#6B7B8D; font-size:1.05rem; font-weight:300; max-width:560px;
    margin:0 auto 2rem; line-height:1.7; }

/* STATS */
.stats-row { display:flex; justify-content:center; gap:2rem; flex-wrap:wrap; margin-bottom:3rem; }
.stat-pill { background:#111820; border:1px solid #1E2A38; border-radius:100px;
    padding:8px 20px; display:flex; align-items:center; gap:8px; }
.stat-num { font-family:'Syne',sans-serif; font-size:1rem; font-weight:800; color:#00D4AA; }
.stat-lbl { font-size:0.82rem; color:#6B7B8D; }

/* UPLOAD ZONE */
.upload-section { max-width:900px; margin:0 auto; padding:0 1rem; }
.upload-card { background:#0D1117; border:2px dashed #1E2A38; border-radius:20px;
    padding:2.5rem; text-align:center; transition:border-color 0.3s; margin-bottom:1.5rem; }
.upload-card:hover { border-color:rgba(0,212,170,0.4); }

/* BUTTONS */
.btn-row { display:flex; gap:12px; justify-content:center; flex-wrap:wrap; margin:1rem 0; }
.stButton > button {
    border-radius:10px !important; font-weight:600 !important; font-size:0.9rem !important;
    padding:0.6rem 1.8rem !important; transition:all 0.2s !important; border:none !important;
}
.stButton > button:first-child { background:#00D4AA !important; color:#060810 !important; }
.stButton > button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 20px rgba(0,212,170,0.25) !important; }

/* RESULT */
.result-wrap { background:#0D1117; border:1px solid #1E2A38; border-radius:20px;
    overflow:hidden; margin:2rem 0; }
.result-header { padding:1.5rem 2rem; border-bottom:1px solid #1E2A38;
    background:linear-gradient(135deg,#0D1117,#111820); }
.disease-label { font-size:0.75rem; font-weight:700; letter-spacing:0.1em;
    text-transform:uppercase; margin:0 0 4px; }
.disease-name { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800;
    color:white; margin:0 0 4px; line-height:1.1; }
.disease-class { color:#6B7B8D; font-size:0.82rem; font-style:italic; margin:0; }
.confidence-num { font-family:'Syne',sans-serif; font-size:2.2rem; font-weight:800; margin:0; }
.result-body { padding:1.5rem 2rem; display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem; }
.info-card { background:#111820; border:1px solid #1E2A38; border-radius:12px; padding:1rem 1.2rem; }
.info-card-title { font-size:0.75rem; font-weight:700; letter-spacing:0.08em;
    text-transform:uppercase; margin:0 0 6px; }
.info-card-body { color:#B8C5D0; font-size:0.88rem; line-height:1.6; margin:0; }

/* CATALOGO */
.catalog-section { max-width:1200px; margin:3rem auto; padding:0 1rem; }
.section-header { margin-bottom:2rem; }
.section-tag { font-size:0.72rem; font-weight:700; letter-spacing:0.12em;
    text-transform:uppercase; color:#00D4AA; display:flex; align-items:center; gap:8px; margin-bottom:8px; }
.section-tag::before { content:''; width:20px; height:1px; background:#00D4AA; }
.section-h2 { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800;
    color:white; letter-spacing:-0.03em; margin:0; }

/* CULTIVO CARDS */
.cultivo-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:12px; }
.cultivo-card { background:#0D1117; border:1px solid #1E2A38; border-radius:14px;
    padding:1.2rem; transition:all 0.2s; cursor:default; }
.cultivo-card:hover { border-color:rgba(0,212,170,0.3); transform:translateY(-2px); }
.cultivo-emoji { font-size:2rem; margin-bottom:8px; }
.cultivo-name { font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:white; margin:0 0 4px; }
.cultivo-count { font-size:0.78rem; color:#00D4AA; font-weight:600; }
.cultivo-enf { font-size:0.75rem; color:#6B7B8D; margin-top:6px; line-height:1.4; }

/* OTRAS POSIBILIDADES */
.others-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:1.2rem; }
.other-card { background:#111820; border:1px solid #1E2A38; border-radius:10px; padding:10px 14px; }
.other-pct { font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:800; color:#6B7B8D; }
.other-name { font-size:0.75rem; color:#4A5568; margin-top:2px; }

/* FOOTER */
.footer { text-align:center; color:#4A5568; font-size:0.78rem;
    padding:2rem 1rem; border-top:1px solid #1a2235; margin-top:3rem; }
.footer strong { color:#6B7B8D; }

div[data-testid="stFileUploadDropzone"] { background:#0D1117 !important; border:none !important; }
.stFileUploader label { display:none !important; }
h3,h2,h1 { color:white !important; }
p { color:#B8C5D0; }
.stProgress > div > div { background:#00D4AA !important; border-radius:100px !important; }
.stProgress { border-radius:100px !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
INFO = {
    "Apple__black_rot":{"n":"Pudricion Negra del Manzano","e":"🍎","g":"muy alta","d":"Botryosphaeria obtusa. Manchas purpuras en hojas y pudricion negra en frutos.","t":"Podar ramas infectadas. Fungicidas sistemicos. Eliminar frutos momificados.","p":"Buena poda para ventilacion. Retirar material muerto del huerto."},
    "Apple__healthy":{"n":"Manzano Saludable","e":"✅","g":"ninguna","d":"Planta en excelente estado sin signos de enfermedad.","t":"Ninguno requerido.","p":"Mantener programa de fertilizacion y riego."},
    "Apple__rust":{"n":"Roya del Manzano","e":"🍎","g":"media","d":"Gymnosporangium juniperi-virginianae. Manchas amarillo-naranja en hojas.","t":"Fungicidas preventivos miclobutanil. Aplicar en floracion.","p":"Eliminar cedros cercanos. Variedades resistentes."},
    "Apple__scab":{"n":"Sarna del Manzano","e":"🍎","g":"alta","d":"Venturia inaequalis. Manchas olivaceas en hojas y frutos corchosos.","t":"Fungicidas captan o mancozeb. Eliminar hojas caidas.","p":"Variedades resistentes. Fungicidas preventivos en primavera."},
    "Cassava__bacterial_blight":{"n":"Marchitez Bacteriana de la Yuca","e":"🌿","g":"muy alta","d":"Xanthomonas axonopodis causa marchitez y pudricion vascular.","t":"No hay cura. Eliminar plantas infectadas. Estacas certificadas.","p":"Material de siembra certificado. Herramientas desinfectadas."},
    "Cassava__brown_streak_disease":{"n":"Rayas Marrones de Yuca","e":"🌿","g":"muy alta","d":"Virus CBSD. Rayas marrones en tallo y necrosis en raices.","t":"Sin cura. Eliminar plantas infectadas inmediatamente.","p":"Variedades resistentes. Control de mosca blanca."},
    "Cassava__green_mottle":{"n":"Moteado Verde de la Yuca","e":"🌿","g":"media","d":"Virus que causa moteado verde-amarillo en hojas jovenes.","t":"No hay tratamiento. Manejar insectos vectores.","p":"Material de siembra sano. Control de trips."},
    "Cassava__healthy":{"n":"Yuca Saludable","e":"✅","g":"ninguna","d":"La yuca se encuentra en excelente estado.","t":"Ninguno requerido.","p":"Estacas certificadas. Rotacion de cultivos."},
    "Cassava__mosaic_disease":{"n":"Mosaico de la Yuca","e":"🌿","g":"alta","d":"CMD — virus mas destructivo de la yuca. Mosaico y distorsion foliar.","t":"Sin cura. Eliminar plantas. Controlar mosca blanca.","p":"Variedades resistentes. Nunca usar estacas de plantas enfermas."},
    "Cherry__healthy":{"n":"Cerezo Saludable","e":"✅","g":"ninguna","d":"El cerezo se encuentra libre de enfermedades.","t":"Ninguno requerido.","p":"Poda anual. Control preventivo."},
    "Cherry__powdery_mildew":{"n":"Oidio del Cerezo","e":"🍒","g":"media","d":"Podosphaera clandestina. Polvo blanco en hojas jovenes.","t":"Fungicidas azufre o bicarbonato. Eliminar partes afectadas.","p":"Buena ventilacion. Evitar exceso de nitrogeno."},
    "Chili__healthy":{"n":"Aji Saludable","e":"✅","g":"ninguna","d":"La planta de aji se encuentra en excelente estado.","t":"Ninguno requerido.","p":"Rotacion de cultivos. Riego adecuado."},
    "Chili__leaf curl":{"n":"Enrollamiento Foliar del Aji","e":"🌶️","g":"alta","d":"Virus transmitido por trips. Enrollamiento y deformacion severa.","t":"Sin cura. Eliminar plantas. Control urgente de insectos.","p":"Mallas antiinsectos. Insecticidas sistemicos preventivos."},
    "Chili__leaf spot":{"n":"Mancha Foliar del Aji","e":"🌶️","g":"media","d":"Complejo fungico-bacteriano. Manchas oscuras con halo amarillo.","t":"Fungicidas o bactericidas cobricos. Eliminar hojas afectadas.","p":"Evitar mojar follaje. Rotacion de cultivos."},
    "Chili__whitefly":{"n":"Mosca Blanca en Aji","e":"🌶️","g":"alta","d":"Bemisia tabaci causa amarillamiento y transmite virus.","t":"Insecticidas sistemicos imidacloprid. Trampas amarillas.","p":"Mallas antiinsectos. Control biologico con Encarsia."},
    "Chili__yellowish":{"n":"Amarillamiento del Aji","e":"🌶️","g":"media","d":"Amarillamiento por deficiencias, riego excesivo o patogenos.","t":"Corregir deficiencias con fertilizacion foliar. Revisar riego.","p":"Analisis de suelo previo. Fertilizacion equilibrada."},
    "Coffee__cercospora_leaf_spot":{"n":"Mancha Cercospora en Cafe","e":"☕","g":"media","d":"Cercospora coffeicola. Manchas circulares con centro grisaceo.","t":"Fungicidas cobricos o mancozeb. Mejorar nutricion.","p":"Sombra regulada. Fertilizacion adecuada."},
    "Coffee__healthy":{"n":"Cafe Saludable","e":"✅","g":"ninguna","d":"El cafeto se encuentra en excelente estado fitosanitario.","t":"Ninguno requerido.","p":"Fertilizacion equilibrada. Sombra regulada. Monitoreo mensual."},
    "Coffee__red_spider_mite":{"n":"Arana Roja del Cafe","e":"☕","g":"alta","d":"Oligonychus ilicis. Bronceado y caida de hojas. Peor en verano seco.","t":"Acaricidas abamectina. Aumentar humedad. Depredadores naturales.","p":"Monitoreo con lupa. Sombra adecuada. Evitar estres hidrico."},
    "Coffee__rust":{"n":"Roya del Cafe","e":"☕","g":"muy alta","d":"Hemileia vastatrix — la mas devastadora del cafe. Polvo naranja en enves de hojas.","t":"URGENTE: Fungicidas triazoles propiconazol. Aplicar preventivamente cada 3 meses.","p":"Variedades resistentes Colombia o Castillo. Fungicidas preventivos."},
    "Corn__common_rust":{"n":"Roya Comun del Maiz","e":"🌽","g":"media","d":"Puccinia sorghi. Pustulas color oxido en ambas caras de hojas.","t":"Fungicidas triazoles preventivos al ver primeras pustulas.","p":"Siembra temprana. Hibridos resistentes."},
    "Corn__gray_leaf_spot":{"n":"Mancha Gris del Maiz","e":"🌽","g":"alta","d":"Cercospora zeae-maydis. Manchas rectangulares grises entre nervaduras.","t":"Fungicidas triazoles o estrobilurinas. Aplicar al inicio.","p":"Rotacion de cultivos. Variedades resistentes."},
    "Corn__healthy":{"n":"Maiz Saludable","e":"✅","g":"ninguna","d":"Cultivo en excelente estado sin enfermedades.","t":"Ninguno requerido.","p":"Rotacion bienal. Densidad adecuada."},
    "Corn__northern_leaf_blight":{"n":"Tizon Foliar Norte en Maiz","e":"🌽","g":"alta","d":"Exserohilum turcicum. Lesiones elipticas largas verde-grisaceas.","t":"Fungicidas estrobilurinas + triazoles antes de VT.","p":"Variedades resistentes. Rotacion con leguminosas."},
    "Cucumber__diseased":{"n":"Pepino Enfermo","e":"🥒","g":"alta","d":"Presencia de oidio, mildiu o mancha angular en pepino.","t":"Identificar enfermedad y aplicar fungicida o bactericida.","p":"Rotacion de cultivos. Buena ventilacion. Semillas certificadas."},
    "Cucumber__healthy":{"n":"Pepino Saludable","e":"✅","g":"ninguna","d":"El pepino se encuentra en excelente estado.","t":"Ninguno requerido.","p":"Rotacion anual. Riego por goteo."},
    "Gauva__diseased":{"n":"Guayabo Enfermo","e":"🍐","g":"alta","d":"Presencia de enfermedad fungica o bacteriana en guayabo.","t":"Fungicidas o bactericidas. Poda de partes afectadas.","p":"Poda sanitaria anual. Buena ventilacion del arbol."},
    "Gauva__healthy":{"n":"Guayabo Saludable","e":"✅","g":"ninguna","d":"El guayabo se encuentra libre de enfermedades.","t":"Ninguno requerido.","p":"Fertilizacion adecuada. Monitoreo regular."},
    "Grape__black_measles":{"n":"Esca de la Vid","e":"🍇","g":"muy alta","d":"Complejo fungico. Manchas en hojas, madera podrida y muerte subita.","t":"No hay cura. Podar con herramientas desinfectadas.","p":"Proteger heridas de poda con pasta fungicida."},
    "Grape__black_rot":{"n":"Pudricion Negra de la Vid","e":"🍇","g":"muy alta","d":"Guignardia bidwellii. Manchas marrones y uvas momificadas.","t":"URGENTE: Fungicidas captan. Eliminar uvas infectadas.","p":"Poda correcta para ventilacion. Eliminar momias."},
    "Grape__healthy":{"n":"Vid Saludable","e":"✅","g":"ninguna","d":"La vid se encuentra en perfecto estado fitosanitario.","t":"Ninguno requerido.","p":"Monitoreo semanal. Poda anual correcta."},
    "Grape__leaf_blight_(isariopsis_leaf_spot)":{"n":"Tizon Foliar de la Vid","e":"🍇","g":"media","d":"Isariopsis clavispora. Manchas marrones en bordes de hojas.","t":"Fungicidas cobricos. Eliminar hojas caidas.","p":"Buena ventilacion. Evitar exceso de humedad."},
    "Jamun__diseased":{"n":"Jambolan Enfermo","e":"🫐","g":"alta","d":"Antracnosis o mancha foliar en jambolan.","t":"Fungicidas sistemicos. Poda de partes afectadas.","p":"Poda sanitaria. Buena ventilacion."},
    "Jamun__healthy":{"n":"Jambolan Saludable","e":"✅","g":"ninguna","d":"El jambolan se encuentra en buen estado.","t":"Ninguno requerido.","p":"Monitoreo regular. Fertilizacion equilibrada."},
    "Lemon__diseased":{"n":"Limonero Enfermo","e":"🍋","g":"alta","d":"Cancro citrico, mancha negra u otras enfermedades en limonero.","t":"Bactericidas o fungicidas segun diagnostico. Poda de ramas.","p":"Plantas certificadas. Control de insectos vectores."},
    "Lemon__healthy":{"n":"Limonero Saludable","e":"✅","g":"ninguna","d":"El limonero se encuentra libre de enfermedades.","t":"Ninguno requerido.","p":"Fertilizacion adecuada. Control preventivo de plagas."},
    "Mango__diseased":{"n":"Mango Enfermo","e":"🥭","g":"alta","d":"Antracnosis, oidio o mancha angular en mango.","t":"Fungicidas sistemicos. Poda de ramas con sintomas.","p":"Poda sanitaria post-cosecha. Fungicidas en floracion."},
    "Mango__healthy":{"n":"Mango Saludable","e":"✅","g":"ninguna","d":"El mango se encuentra en excelente estado.","t":"Ninguno requerido.","p":"Poda anual. Monitoreo en floracion."},
    "Peach__bacterial_spot":{"n":"Mancha Bacteriana del Melocoton","e":"🍑","g":"alta","d":"Xanthomonas arboricola. Manchas acuosas en hojas y frutos.","t":"Bactericidas cobricos en primavera. Evitar heridas.","p":"Variedades resistentes. Proteger de viento."},
    "Peach__healthy":{"n":"Melocotonero Saludable","e":"✅","g":"ninguna","d":"El melocotonero se encuentra libre de enfermedades.","t":"Ninguno requerido.","p":"Poda anual. Control preventivo en primavera."},
    "Pepper_bell__bacterial_spot":{"n":"Mancha Bacteriana del Pimiento","e":"🫑","g":"alta","d":"Xanthomonas campestris. Manchas oscuras en hojas y frutos.","t":"Bactericidas cobricos. Eliminar plantas infectadas.","p":"Semillas certificadas. Rotacion de cultivos."},
    "Pepper_bell__healthy":{"n":"Pimiento Saludable","e":"✅","g":"ninguna","d":"El pimiento se encuentra en excelente estado.","t":"Ninguno requerido.","p":"Fertilizacion y riego adecuados."},
    "Pomegranate__diseased":{"n":"Granada Enferma","e":"🍎","g":"alta","d":"Mancha foliar o pudricion de fruto en granada.","t":"Fungicidas sistemicos. Poda de partes afectadas.","p":"Buena ventilacion. Evitar riego excesivo."},
    "Pomegranate__healthy":{"n":"Granada Saludable","e":"✅","g":"ninguna","d":"La granada se encuentra en buen estado.","t":"Ninguno requerido.","p":"Poda anual. Riego controlado."},
    "Potato__early_blight":{"n":"Tizon Temprano de la Papa","e":"🥔","g":"media","d":"Alternaria solani. Manchas oscuras concentricas en hojas inferiores.","t":"Fungicidas mancozeb o clorotalonil cada 7-10 dias.","p":"No mojar follaje. Buena ventilacion entre plantas."},
    "Potato__healthy":{"n":"Papa Saludable","e":"✅","g":"ninguna","d":"La papa se encuentra en buen estado sin enfermedades.","t":"Ninguno requerido.","p":"Continuar manejo agronomico actual."},
    "Potato__late_blight":{"n":"Tizon Tardio de la Papa","e":"🥔","g":"muy alta","d":"ALERTA: Phytophthora infestans. Puede destruir cosecha en 10 dias.","t":"URGENTE: Fungicidas sistemicos metalaxil. Destruir plantas afectadas.","p":"Vigilancia en epocas humedas. Variedades resistentes."},
    "Rice__brown_spot":{"n":"Mancha Parda del Arroz","e":"🌾","g":"alta","d":"Bipolaris oryzae. Manchas ovaladas marrones en hojas y granos.","t":"Fungicidas triazoles. Mejorar nutricion con potasio.","p":"Semilla certificada. Fertilizacion equilibrada."},
    "Rice__healthy":{"n":"Arroz Saludable","e":"✅","g":"ninguna","d":"El cultivo de arroz se encuentra en excelente estado.","t":"Ninguno requerido.","p":"Semilla certificada. Manejo integrado de plagas."},
    "Rice__hispa":{"n":"Hispa del Arroz","e":"🌾","g":"alta","d":"Dicladispa armigera. Raspa y mina hojas dejando estrias blancas.","t":"Insecticidas sistemicos. Eliminar plantas muy afectadas en bordes.","p":"Monitoreo temprano. Evitar exceso de nitrogeno."},
    "Rice__leaf_blast":{"n":"Piricularia del Arroz","e":"🌾","g":"muy alta","d":"Magnaporthe oryzae — la mas importante del arroz mundial. Manchas romboidales.","t":"URGENTE: Fungicidas triazoles o estrobilurinas al inicio de sintomas.","p":"Variedades resistentes. Evitar exceso de nitrogeno."},
    "Rice__neck_blast":{"n":"Blast del Cuello del Arroz","e":"🌾","g":"muy alta","d":"Magnaporthe oryzae en cuello de panicula. Perdida total del grano.","t":"CRITICO: Fungicidas sistemicos en paniculacion antes de sintomas.","p":"Fungicidas preventivos en embuche. Variedades resistentes."},
    "Soybean__bacterial_blight":{"n":"Tizon Bacteriano de la Soya","e":"🌱","g":"alta","d":"Pseudomonas savastanoi. Manchas acuosas angulares amarillas en hojas.","t":"Bactericidas cobricos. Evitar labores con plantas mojadas.","p":"Semillas certificadas. Rotacion con cereales."},
    "Soybean__caterpillar":{"n":"Oruga de la Soya","e":"🌱","g":"alta","d":"Anticarsia gemmatalis defolia rapidamente el cultivo.","t":"Insecticidas biologicos Bt o quimicos. Monitoreo con umbrales.","p":"Monitoreo semanal desde V2. Control biologico."},
    "Soybean__diabrotica_speciosa":{"n":"Vaquita en Soya","e":"🌱","g":"media","d":"Diabrotica speciosa defolia hojas y ataca raices.","t":"Insecticidas al follaje. Tratamiento de semilla.","p":"Rotacion de cultivos. Monitoreo de adultos en bordes."},
    "Soybean__downy_mildew":{"n":"Mildiu Velloso de la Soya","e":"🌱","g":"media","d":"Peronospora manshurica. Polvo grisaceo en enves de hojas jovenes.","t":"Fungicidas metalaxil o fosetil. Aplicar preventivamente.","p":"Semilla tratada. Variedades resistentes."},
    "Soybean__healthy":{"n":"Soya Saludable","e":"✅","g":"ninguna","d":"El cultivo de soya se encuentra libre de enfermedades.","t":"Ninguno requerido.","p":"Rotacion de cultivos. Monitoreo regular."},
    "Soybean__mosaic_virus":{"n":"Virus Mosaico de la Soya","e":"🌱","g":"alta","d":"SMV transmitido por pulgones. Mosaico y reduccion de rendimiento.","t":"Sin cura. Control urgente de pulgones vectores.","p":"Semilla certificada libre de virus."},
    "Soybean__powdery_mildew":{"n":"Oidio de la Soya","e":"🌱","g":"media","d":"Microsphaera diffusa. Polvo blanco en hojas en etapas reproductivas.","t":"Fungicidas azufre o triazoles al inicio de sintomas.","p":"Variedades tolerantes. Densidades adecuadas."},
    "Soybean__rust":{"n":"Roya Asiatica de la Soya","e":"🌱","g":"muy alta","d":"Phakopsora pachyrhizi — la mas destructiva de la soya. Pustulas beige.","t":"URGENTE: Fungicidas triazoles + estrobilurinas preventivamente.","p":"Monitoreo semanal. Fungicidas desde R1. Siembra temprana."},
    "Soybean__southern_blight":{"n":"Tizon del Sur en Soya","e":"🌱","g":"muy alta","d":"Athelia rolfsii. Marchitez subita y pudricion del tallo a nivel del suelo.","t":"Fungicidas en suelo. Eliminar y enterrar plantas afectadas.","p":"Rotacion larga. Materia organica. Evitar exceso de humedad."},
    "Strawberry__healthy":{"n":"Fresa Saludable","e":"✅","g":"ninguna","d":"La fresa se encuentra en optimas condiciones.","t":"Ninguno requerido.","p":"Renovar plantacion cada 2-3 anos."},
    "Strawberry___leaf_scorch":{"n":"Quemadura Foliar de la Fresa","e":"🍓","g":"media","d":"Diplocarpon earlianum. Manchas purpuras que secan los bordes foliares.","t":"Fungicidas captan o tiram cada 10 dias. Eliminar hojas infectadas.","p":"Evitar riego por aspersion. Buen drenaje."},
    "Sugarcane__bacterial_blight":{"n":"Escaldadura de la Cana","e":"🌾","g":"muy alta","d":"Xanthomonas albilineans. Rayas blancas en hojas y muerte subita.","t":"No hay cura. Eliminar plantas. Desinfectar toda la maquinaria.","p":"Variedades resistentes. Semilla sana certificada."},
    "Sugarcane__healthy":{"n":"Cana de Azucar Saludable","e":"✅","g":"ninguna","d":"El cultivo de cana se encuentra en excelente estado.","t":"Ninguno requerido.","p":"Semilla certificada. Monitoreo regular."},
    "Sugarcane__red_rot":{"n":"Pudricion Roja de la Cana","e":"🌾","g":"muy alta","d":"Colletotrichum falcatum. Pudricion roja interna con olor a alcohol.","t":"No hay cura. Eliminar y quemar plantas afectadas.","p":"Variedades resistentes. Semilla certificada. Buen drenaje."},
    "Sugarcane__red_stripe":{"n":"Raya Roja de la Cana","e":"🌾","g":"alta","d":"Acidovorax avenae. Rayas rojas en hojas jovenes que se necrosan.","t":"Bactericidas cobricos. Eliminar hojas afectadas. Desinfectar herramientas.","p":"Semilla certificada. Evitar heridas durante labores."},
    "Sugarcane__rust":{"n":"Roya de la Cana de Azucar","e":"🌾","g":"alta","d":"Puccinia melanocephala. Pustulas marrones en hojas que reducen fotosintesis.","t":"Fungicidas triazoles al inicio de sintomas.","p":"Variedades resistentes. Monitoreo en epocas humedas."},
    "Tea__algal_leaf":{"n":"Mancha Algal del Te","e":"🍵","g":"media","d":"Cephaleuros virescens. Manchas circulares verde-anaranjadas en hojas.","t":"Fungicidas cobricos. Mejorar ventilacion y drenaje.","p":"Poda regular para ventilacion. Evitar exceso de humedad."},
    "Tea__anthracnose":{"n":"Antracnosis del Te","e":"🍵","g":"alta","d":"Colletotrichum spp. Manchas oscuras en hojas y muerte de brotes.","t":"Fungicidas carbendazim o azoxistrobina. Eliminar brotes afectados.","p":"Cosecha frecuente. Buena ventilacion entre plantas."},
    "Tea__bird_eye_spot":{"n":"Mancha Ojo de Pajaro en Te","e":"🍵","g":"media","d":"Cercospora theae. Manchas circulares con centro gris y halo oscuro.","t":"Fungicidas cobricos o mancozeb cada 10-14 dias.","p":"Cosecha regular. Fertilizacion equilibrada."},
    "Tea__brown_blight":{"n":"Tizon Pardo del Te","e":"🍵","g":"alta","d":"Colletotrichum camelliae. Tizon y muerte de brotes jovenes.","t":"Fungicidas sistemicos. Eliminar brotes afectados durante cosecha.","p":"Cosecha frecuente. Buen drenaje. Evitar heridas."},
    "Tea__healthy":{"n":"Te Saludable","e":"✅","g":"ninguna","d":"El cultivo de te se encuentra en excelente estado.","t":"Ninguno requerido.","p":"Cosecha regular. Fertilizacion adecuada. Monitoreo mensual."},
    "Tea__red_leaf_spot":{"n":"Mancha Roja del Te","e":"🍵","g":"media","d":"Phyllosticta theicola. Manchas rojas circulares en hojas maduras.","t":"Fungicidas cobricos. Mejorar condiciones de crecimiento.","p":"Fertilizacion equilibrada. Buena ventilacion entre plantas."},
    "Tomato__bacterial_spot":{"n":"Mancha Bacteriana del Tomate","e":"🍅","g":"alta","d":"Xanthomonas campestris. Manchas acuosas necrosas en hojas y frutos.","t":"Bactericidas cobricos. Evitar trabajar con plantas mojadas.","p":"Semillas tratadas. Evitar salpicaduras de suelo."},
    "Tomato__early_blight":{"n":"Tizon Temprano del Tomate","e":"🍅","g":"media","d":"Alternaria solani. Manchas marrones con anillos concentricos en hojas.","t":"Mancozeb o azoxistrobina cada 7-10 dias. Eliminar hojas afectadas.","p":"Mulching. Riego por goteo. Plantas bien nutridas."},
    "Tomato__healthy":{"n":"Tomate Saludable","e":"✅","g":"ninguna","d":"Excelente estado fitosanitario sin presencia de enfermedades.","t":"Ninguno requerido.","p":"Mantener programa de nutricion y riego actual."},
    "Tomato__late_blight":{"n":"Tizon Tardio del Tomate","e":"🍅","g":"muy alta","d":"ALERTA CRITICA: Phytophthora infestans. Manchas verde-grisaceas de avance rapido.","t":"ACCION INMEDIATA: Fungicidas sistemicos. Aislar plantas afectadas.","p":"Monitoreo diario en clima humedo. Fungicidas preventivos en lluvias."},
    "Tomato__leaf_mold":{"n":"Moho de la Hoja del Tomate","e":"🍅","g":"media","d":"Passalora fulva. Manchas amarillas en haz y moho olivaceo en enves.","t":"Fungicidas azufre. Mejorar ventilacion del cultivo urgentemente.","p":"Reducir humedad relativa. Espaciado adecuado entre plantas."},
    "Tomato__mosaic_virus":{"n":"Virus Mosaico del Tomate","e":"🦠","g":"muy alta","d":"Virus sin cura. Mosaico verde-amarillo, deformacion y perdida de cosecha.","t":"NO hay cura. Eliminar plantas infectadas INMEDIATAMENTE.","p":"Control de vectores. Herramientas desinfectadas. Semilla certificada."},
    "Tomato__septoria_leaf_spot":{"n":"Mancha Septoria en Tomate","e":"🍅","g":"media","d":"Septoria lycopersici. Manchas circulares con centro gris y borde oscuro.","t":"Fungicidas protectores mancozeb o clorotalonil. Eliminar hojas basales.","p":"No mojar follaje. Mulching. Rotacion de cultivos."},
    "Tomato__spider_mites_(two_spotted_spider_mite)":{"n":"Arana Roja del Tomate","e":"🕷️","g":"alta","d":"Tetranychus urticae. Punteado amarillo plateado y bronceado de hojas.","t":"Acaricidas abamectina o bifenazato. Depredadores naturales Phytoseiulus.","p":"Monitoreo semanal con lupa. Evitar estres hidrico."},
    "Tomato__target_spot":{"n":"Mancha Diana del Tomate","e":"🍅","g":"media","d":"Corynespora cassiicola. Manchas concentricas similares a una diana.","t":"Fungicidas sistemicos azoxistrobina. Eliminar residuos de cosecha.","p":"Buena aireacion. Evitar exceso de nitrogeno."},
    "Tomato__yellow_leaf_curl_virus":{"n":"Virus Enrollamiento Amarillo Tomate","e":"🦠","g":"muy alta","d":"TYLCV transmitido por mosca blanca. Amarillamiento y enrollamiento severo.","t":"Sin cura. Control urgente de mosca blanca con insecticidas sistemicos.","p":"Mallas antiinsectos 50 mesh. Variedades resistentes TYLCV."},
    "Wheat__brown_rust":{"n":"Roya Parda del Trigo","e":"🌾","g":"alta","d":"Puccinia triticina. Pustulas marrones en hojas reducen rendimiento hasta 40%.","t":"Fungicidas triazoles o estrobilurinas preventivamente.","p":"Variedades resistentes. Siembra en epocas de menor presion."},
    "Wheat__healthy":{"n":"Trigo Saludable","e":"✅","g":"ninguna","d":"El cultivo de trigo se encuentra en excelente estado.","t":"Ninguno requerido.","p":"Semilla certificada. Monitoreo regular."},
    "Wheat__septoria":{"n":"Septoriosis del Trigo","e":"🌾","g":"alta","d":"Zymoseptoria tritici. Manchas alargadas con puntos negros en hojas.","t":"Fungicidas triazoles + estrobilurinas en aplicacion en hoja bandera.","p":"Variedades resistentes. Rotacion de cultivos. Semilla tratada."},
    "Wheat__yellow_rust":{"n":"Roya Amarilla del Trigo","e":"🌾","g":"muy alta","d":"Puccinia striiformis. Pustulas amarillas en rayas. Muy agresiva en clima frio.","t":"URGENTE: Fungicidas triazoles inmediatamente al ver primeros sintomas.","p":"Variedades resistentes. Monitoreo en clima frio y humedo."},
}

CULTIVOS = {
    "🍎 Manzana": ["Apple__black_rot","Apple__healthy","Apple__rust","Apple__scab"],
    "🌿 Yuca": ["Cassava__bacterial_blight","Cassava__brown_streak_disease","Cassava__green_mottle","Cassava__healthy","Cassava__mosaic_disease"],
    "🍒 Cerezo": ["Cherry__healthy","Cherry__powdery_mildew"],
    "🌶️ Aji": ["Chili__healthy","Chili__leaf curl","Chili__leaf spot","Chili__whitefly","Chili__yellowish"],
    "☕ Cafe": ["Coffee__cercospora_leaf_spot","Coffee__healthy","Coffee__red_spider_mite","Coffee__rust"],
    "🌽 Maiz": ["Corn__common_rust","Corn__gray_leaf_spot","Corn__healthy","Corn__northern_leaf_blight"],
    "🥒 Pepino": ["Cucumber__diseased","Cucumber__healthy"],
    "🍐 Guayabo": ["Gauva__diseased","Gauva__healthy"],
    "🍇 Uva": ["Grape__black_measles","Grape__black_rot","Grape__healthy","Grape__leaf_blight_(isariopsis_leaf_spot)"],
    "🫐 Jambolan": ["Jamun__diseased","Jamun__healthy"],
    "🍋 Limon": ["Lemon__diseased","Lemon__healthy"],
    "🥭 Mango": ["Mango__diseased","Mango__healthy"],
    "🍑 Melocoton": ["Peach__bacterial_spot","Peach__healthy"],
    "🫑 Pimenton": ["Pepper_bell__bacterial_spot","Pepper_bell__healthy"],
    "🍎 Granada": ["Pomegranate__diseased","Pomegranate__healthy"],
    "🥔 Papa": ["Potato__early_blight","Potato__healthy","Potato__late_blight"],
    "🌾 Arroz": ["Rice__brown_spot","Rice__healthy","Rice__hispa","Rice__leaf_blast","Rice__neck_blast"],
    "🌱 Soya": ["Soybean__bacterial_blight","Soybean__caterpillar","Soybean__diabrotica_speciosa","Soybean__downy_mildew","Soybean__healthy","Soybean__mosaic_virus","Soybean__powdery_mildew","Soybean__rust","Soybean__southern_blight"],
    "🍓 Fresa": ["Strawberry__healthy","Strawberry___leaf_scorch"],
    "🌾 Cana": ["Sugarcane__bacterial_blight","Sugarcane__healthy","Sugarcane__red_rot","Sugarcane__red_stripe","Sugarcane__rust"],
    "🍵 Te": ["Tea__algal_leaf","Tea__anthracnose","Tea__bird_eye_spot","Tea__brown_blight","Tea__healthy","Tea__red_leaf_spot"],
    "🍅 Tomate": ["Tomato__bacterial_spot","Tomato__early_blight","Tomato__healthy","Tomato__late_blight","Tomato__leaf_mold","Tomato__mosaic_virus","Tomato__septoria_leaf_spot","Tomato__spider_mites_(two_spotted_spider_mite)","Tomato__target_spot","Tomato__yellow_leaf_curl_virus"],
    "🌾 Trigo": ["Wheat__brown_rust","Wheat__healthy","Wheat__septoria","Wheat__yellow_rust"],
}

COLORES = {
    "ninguna":  ("#27AE60","✅ PLANTA SANA","#D5F5E3"),
    "media":    ("#F39C12","⚠️ ATENCION REQUERIDA","#FEF9E7"),
    "alta":     ("#E67E22","🚨 ENFERMEDAD DETECTADA","#FDEBD0"),
    "muy alta": ("#E94560","🔴 ALERTA CRITICA","#FADBD8"),
}

@st.cache_resource
def cargar_modelo():
    return YOLO(r"D:\NEXRO_PLANT_AI\runs\nexro_plant_v3_full\weights\best.pt")

def generar_excel(clase, conf, info, top5_nombres, top5_confs):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Diagnostico"

    def fill(c): return PatternFill("solid", start_color=c, fgColor=c)
    def font(bold=False, size=11, color="000000"):
        return Font(name="Arial", bold=bold, size=size, color=color)
    def align(h="left", v="center", wrap=False):
        return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 55
    ws.merge_cells("A1:B1")
    ws["A1"] = "NEXRO PLANT AI — REPORTE DE DIAGNOSTICO FITOSANITARIO"
    ws["A1"].font = Font(name="Arial", bold=True, size=14, color="FFFFFF")
    ws["A1"].fill = fill("080A0E")
    ws["A1"].alignment = align("center")
    ws.row_dimensions[1].height = 36

    ws.merge_cells("A2:B2")
    ws["A2"] = f"Generado el {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')} — Nexro Systems"
    ws["A2"].font = Font(name="Arial", size=9, color="00D4AA")
    ws["A2"].fill = fill("0D1117")
    ws["A2"].alignment = align("center")
    ws.row_dimensions[2].height = 20

    datos = [
        ("Cultivo / Clase detectada", clase),
        ("Enfermedad identificada", info.get("n", clase)),
        ("Nivel de confianza", f"{conf:.1f}%"),
        ("Gravedad", info.get("g","").upper()),
        ("Descripcion", info.get("d","")),
        ("Tratamiento recomendado", info.get("t","")),
        ("Medidas de prevencion", info.get("p","")),
    ]

    g = info.get("g","media")
    g_colors = {"ninguna":"D5F5E3","media":"FEF9E7","alta":"FDEBD0","muy alta":"FADBD8"}
    g_bg = g_colors.get(g,"F0F4F8")

    row = 4
    for label, value in datos:
        ws.row_dimensions[row].height = 40 if len(str(value)) > 80 else 28
        ws[f"A{row}"] = label
        ws[f"A{row}"].font = Font(name="Arial", bold=True, size=10, color="0F3460")
        ws[f"A{row}"].fill = fill("F0F4F8")
        ws[f"A{row}"].alignment = align("left", wrap=True)
        ws[f"B{row}"] = value
        ws[f"B{row}"].font = Font(name="Arial", size=10, color="2C3E50")
        bg = g_bg if label == "Gravedad" else "FAFBFC"
        ws[f"B{row}"].fill = fill(bg)
        ws[f"B{row}"].alignment = align("left", "center", wrap=True)
        row += 1

    row += 1
    ws.merge_cells(f"A{row}:B{row}")
    ws[f"A{row}"] = "OTRAS POSIBILIDADES DETECTADAS"
    ws[f"A{row}"].font = Font(name="Arial", bold=True, size=11, color="FFFFFF")
    ws[f"A{row}"].fill = fill("0F3460")
    ws[f"A{row}"].alignment = align("center")
    ws.row_dimensions[row].height = 26
    row += 1

    for i, (n, c) in enumerate(zip(top5_nombres[1:], top5_confs[1:]), 2):
        inf2 = INFO.get(n, {"n": n})
        ws[f"A{row}"] = f"#{i} — {inf2.get('n', n)}"
        ws[f"A{row}"].font = Font(name="Arial", size=9, color="2C3E50")
        ws[f"A{row}"].fill = fill("FAFBFC" if i%2==0 else "FFFFFF")
        ws[f"B{row}"] = f"{c*100:.1f}% de confianza"
        ws[f"B{row}"].font = Font(name="Arial", bold=True, size=9, color="6B7B8D")
        ws[f"B{row}"].fill = fill("FAFBFC" if i%2==0 else "FFFFFF")
        ws.row_dimensions[row].height = 22
        row += 1

    row += 1
    ws.merge_cells(f"A{row}:B{row}")
    ws[f"A{row}"] = "Nexro Systems © 2026 | nexrosystems@gmail.com | +57 321 521 7396 | nexrosystems-alt.github.io/nexro-systems"
    ws[f"A{row}"].font = Font(name="Arial", size=8, color="6B7B8D", italic=True)
    ws[f"A{row}"].fill = fill("F0F4F8")
    ws[f"A{row}"].alignment = align("center")

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
    <div class="nav-logo">Nexro<span>.</span> Plant AI</div>
    <div class="nav-badge">v3 · 88 Clases · Campo Real</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-tag">Sistema de Diagnostico Fitosanitario con IA</div>
    <h1>Detecta enfermedades en<br>tus cultivos con <span>IA</span></h1>
    <p class="hero-sub">Sube una foto de una hoja y recibe un diagnostico preciso en segundos. 88 enfermedades en 20 cultivos. Entrenado con fotos reales de campo.</p>
    <div class="stats-row">
        <div class="stat-pill"><span class="stat-num">88</span><span class="stat-lbl">Enfermedades</span></div>
        <div class="stat-pill"><span class="stat-num">20</span><span class="stat-lbl">Cultivos</span></div>
        <div class="stat-pill"><span class="stat-num">93.7%</span><span class="stat-lbl">Precision</span></div>
        <div class="stat-pill"><span class="stat-num">&lt;2s</span><span class="stat-lbl">Diagnostico</span></div>
        <div class="stat-pill"><span class="stat-num">79K+</span><span class="stat-lbl">Imagenes reales</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="upload-section">', unsafe_allow_html=True)

if "resultado" not in st.session_state:
    st.session_state.resultado = None
if "imagen_pil" not in st.session_state:
    st.session_state.imagen_pil = None

st.markdown("""
<div style="background:#0D1117; border:1px solid #1E2A38; border-radius:16px; padding:1.5rem 2rem; margin-bottom:1.2rem;">
    <p style="font-family:'Syne',sans-serif; font-size:1rem; font-weight:700; color:white; margin:0 0 1rem;">
        📌 Como tomar la foto para mejor resultado
    </p>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.8rem;">
        <div style="display:flex; gap:10px; align-items:flex-start;">
            <span style="font-size:1.3rem;">✅</span>
            <span style="color:#B8C5D0; font-size:0.88rem; line-height:1.5;">Una sola hoja en el centro de la imagen</span>
        </div>
        <div style="display:flex; gap:10px; align-items:flex-start;">
            <span style="font-size:1.3rem;">✅</span>
            <span style="color:#B8C5D0; font-size:0.88rem; line-height:1.5;">Buena iluminacion natural, sin sombras fuertes</span>
        </div>
        <div style="display:flex; gap:10px; align-items:flex-start;">
            <span style="font-size:1.3rem;">✅</span>
            <span style="color:#B8C5D0; font-size:0.88rem; line-height:1.5;">La enfermedad visible y enfocada claramente</span>
        </div>
        <div style="display:flex; gap:10px; align-items:flex-start;">
            <span style="font-size:1.3rem;">✅</span>
            <span style="color:#B8C5D0; font-size:0.88rem; line-height:1.5;">Fondo lo mas uniforme posible</span>
        </div>
        <div style="display:flex; gap:10px; align-items:flex-start;">
            <span style="font-size:1.3rem;">❌</span>
            <span style="color:#6B7B8D; font-size:0.88rem; line-height:1.5;">No multiples hojas superpuestas</span>
        </div>
        <div style="display:flex; gap:10px; align-items:flex-start;">
            <span style="font-size:1.3rem;">❌</span>
            <span style="color:#6B7B8D; font-size:0.88rem; line-height:1.5;">No manos sosteniendo la hoja</span>
        </div>
        <div style="display:flex; gap:10px; align-items:flex-start;">
            <span style="font-size:1.3rem;">❌</span>
            <span style="color:#6B7B8D; font-size:0.88rem; line-height:1.5;">No fotos borrosas o muy oscuras</span>
        </div>
        <div style="display:flex; gap:10px; align-items:flex-start;">
            <span style="font-size:1.3rem;">❌</span>
            <span style="color:#6B7B8D; font-size:0.88rem; line-height:1.5;">No zoom excesivo ni muy lejano</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

imagen_subida = st.file_uploader("Sube tu imagen", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")

col_a, col_b, col_c = st.columns([2,2,2])
with col_a:
    analizar = st.button("🔍  Analizar imagen", use_container_width=True)
with col_b:
    limpiar = st.button("🗑️  Limpiar resultados", use_container_width=True)
with col_c:
    descargar_placeholder = st.empty()

if limpiar:
    st.session_state.resultado = None
    st.session_state.imagen_pil = None
    st.rerun()

if analizar and imagen_subida:
    imagen = Image.open(imagen_subida).convert("RGB")
    st.session_state.imagen_pil = imagen
    with st.spinner("Analizando con IA..."):
        modelo = cargar_modelo()
        r = modelo(imagen)[0]
        top5_idx = r.probs.top5
        top5_conf = r.probs.top5conf.tolist()
        nombres = r.names
    clase = nombres[top5_idx[0]]
    conf = top5_conf[0] * 100
    info = INFO.get(clase, {"n":clase.replace("_"," ").replace("__"," — "),"e":"🌿","g":"media","d":"Enfermedad detectada.","t":"Consultar agronomo.","p":"Monitoreo regular."})
    st.session_state.resultado = {"clase":clase,"conf":conf,"info":info,"top5_idx":top5_idx,"top5_conf":top5_conf,"nombres":nombres}

if st.session_state.resultado and st.session_state.imagen_pil:
    res = st.session_state.resultado
    clase = res["clase"]; conf = res["conf"]; info = res["info"]
    top5_idx = res["top5_idx"]; top5_conf = res["top5_conf"]; nombres = res["nombres"]
    g = info.get("g","media")
    color, etiqueta, gbg = COLORES.get(g, ("#6B7B8D","DESCONOCIDO","#F0F4F8"))

    top5_nombres = [nombres[i] for i in top5_idx]

    excel_buf = generar_excel(clase, conf, info, top5_nombres, top5_conf)
    with col_c:
        st.download_button(
            label="📥  Descargar reporte Excel",
            data=excel_buf,
            file_name=f"nexro_diagnostico_{clase}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    col1, col2 = st.columns([1,1])
    with col1:
        st.image(st.session_state.imagen_pil, use_container_width=True, caption="Hoja analizada")
    with col2:
        st.markdown(f"""
        <div class="result-wrap">
            <div class="result-header">
                <p class="disease-label" style="color:{color};">{etiqueta}</p>
                <p class="disease-name">{info.get('e','🌿')} {info.get('n',clase)}</p>
                <p class="disease-class">{clase}</p>
                <p class="confidence-num" style="color:{color}; margin-top:12px;">
                    {conf:.1f}%
                    <span style="font-size:0.85rem;font-weight:400;color:#6B7B8D;"> de confianza</span>
                </p>
            </div>
            <div class="result-body">
                <div class="info-card">
                    <p class="info-card-title" style="color:#00D4AA;">🔬 Descripcion</p>
                    <p class="info-card-body">{info.get('d','')}</p>
                </div>
                <div class="info-card">
                    <p class="info-card-title" style="color:#E94560;">💊 Tratamiento</p>
                    <p class="info-card-body">{info.get('t','')}</p>
                </div>
                <div class="info-card">
                    <p class="info-card-title" style="color:#F39C12;">🛡️ Prevencion</p>
                    <p class="info-card-body">{info.get('p','')}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📊 Otras posibilidades")
    cols = st.columns(4)
    for i in range(1, min(5, len(top5_idx))):
        c = top5_conf[i]*100
        n = nombres[top5_idx[i]]
        i2 = INFO.get(n,{"n":n.replace("_"," "),"e":"🌿"})
        nom = i2.get("n",n)
        if len(nom)>24: nom=nom[:24]+"..."
        with cols[i-1]:
            st.markdown(f"""
            <div class="other-card">
                <div class="other-pct">{c:.1f}%</div>
                <div class="other-name">{i2.get('e','🌿')} {nom}</div>
            </div>
            """, unsafe_allow_html=True)
elif analizar and not imagen_subida:
    st.warning("Primero sube una imagen para analizar.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div class="catalog-section">
    <div class="section-header">
        <div class="section-tag">Cultivos soportados</div>
        <h2 class="section-h2">20 cultivos · 88 enfermedades detectables</h2>
    </div>
""", unsafe_allow_html=True)

cols = st.columns(4)
for i, (cultivo, clases) in enumerate(CULTIVOS.items()):
    enfs = [INFO.get(c,{}).get("n","") for c in clases if "healthy" not in c.lower()]
    enfs_str = ", ".join(enfs[:2]) + ("..." if len(enfs)>2 else "")
    parts = cultivo.split(" ", 1)
    emoji = parts[0]
    nombre = parts[1] if len(parts) > 1 else cultivo
    with cols[i % 4]:
        st.markdown(f"""
        <div class="cultivo-card">
            <div class="cultivo-emoji">{emoji}</div>
            <p class="cultivo-name">{nombre}</p>
            <p class="cultivo-count">{len(clases)} condiciones</p>
            <p class="cultivo-enf">{enfs_str if enfs_str else "Saludable"}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <strong>Nexro Plant AI v3</strong> — Nexro Systems © 2026<br>
    nexrosystems@gmail.com &nbsp;·&nbsp; +57 321 521 7396 &nbsp;·&nbsp;
    <a href="https://nexrosystems-alt.github.io/nexro-systems" style="color:#00D4AA;">nexrosystems-alt.github.io</a><br><br>
    Modelo: YOLOv8n &nbsp;·&nbsp; 88 clases &nbsp;·&nbsp; 20 cultivos &nbsp;·&nbsp; 93.7% Precision &nbsp;·&nbsp; 79,000+ imagenes reales de campo
</div>
""", unsafe_allow_html=True)