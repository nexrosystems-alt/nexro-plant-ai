"""
Nexro Plant AI - Datos
Base de datos de enfermedades y cultivos
"""

# ═══════════════════════════════════════════════════════════════════════════════
# PALETA DE COLORES
# ═══════════════════════════════════════════════════════════════════════════════
C_BG      = "#0a0d14"
C_BG2     = "#080b12"
C_CARD    = "#111520"
C_CARD2   = "#161b2a"
C_ACC     = "#00e5a0"
C_ACC2    = "#00c853"
C_ACC_DK  = "#0a2a1f"
C_TEXT    = "#ffffff"
C_SUB     = "#7a8599"
C_SUB2    = "#a8b3c7"
C_BOR     = "#1e2436"
C_DANGER  = "#ff4757"
C_WARN    = "#ffab00"

GSEV = {
    "ninguna":  "#00e5a0",
    "media":    "#ffab00",
    "alta":     "#ff6d00",
    "muy alta": "#d50000",
}

GSEV_LABEL = {
    "ninguna":  "✅ PLANTA SANA",
    "media":    "⚠️ ATENCIÓN REQUERIDA",
    "alta":     "🚨 ENFERMEDAD DETECTADA",
    "muy alta": "🔴 ALERTA CRÍTICA",
}

GSEV_BG = {
    "ninguna":  "#0a2a1f",
    "media":    "#2a1f0a",
    "alta":     "#2a150a",
    "muy alta": "#2a0a0a",
}

# ═══════════════════════════════════════════════════════════════════════════════
# BASE DE DATOS DE ENFERMEDADES
# ═══════════════════════════════════════════════════════════════════════════════
INFO = {
    "Apple__black_rot":{"n":"Pudricion Negra del Manzano","e":"🍎","g":"muy alta","d":"Botryosphaeria obtusa. Manchas purpuras en hojas y pudricion negra en frutos.","t":"Podar ramas infectadas. Fungicidas sistemicos. Eliminar frutos momificados.","p":"Buena poda para ventilacion. Retirar material muerto del huerto."},
    "Apple__healthy":{"n":"Manzano Saludable","e":"✅","g":"ninguna","d":"Planta en excelente estado sin signos de enfermedad.","t":"Ninguno requerido.","p":"Mantener programa de fertilizacion y riego."},
    "Apple__rust":{"n":"Roya del Manzano","e":"🍎","g":"media","d":"Gymnosporangium juniperi-virginianae. Manchas amarillo-naranja en hojas.","t":"Fungicidas preventivos miclobutanil. Aplicar en floracion.","p":"Eliminar cedros cercanos. Variedades resistentes."},
    "Apple__scab":{"n":"Sarna del Manzano","e":"🍎","g":"alta","d":"Venturia inaequalis. Manchas olivaceas en hojas y frutos corchosos.","t":"Fungicidas captan o mancozeb. Eliminar hojas caidas.","p":"Variedades resistentes. Fungicidas preventivos en primavera."},
    "Cassava__bacterial_blight":{"n":"Marchitez Bacteriana de la Yuca","e":"🌿","g":"muy alta","d":"Xanthomonas axonopodis causa marchitez y pudricion vascular.","t":"No hay cura. Eliminar plantas infectadas. Estacas certificadas.","p":"Material de siembra certificado. Herramientas desinfectadas."},
    "Cassava__brown_streak_disease":{"n":"Rayas Marrones de Yuca","e":"🌿","g":"muy alta","d":"Virus CBSD. Rayas marrones en tallo y necrosis en raices.","t":"Sin cura. Eliminar plantas infectadas inmediatamente.","p":"Variedades resistentes. Control de mosca blanca."},
    "Cassava__green_mottle":{"n":"Moteado Verde de la Yuca","e":"🌿","g":"media","d":"Virus que causa moteado verde-amarillo en hojas jovenes.","t":"No hay tratamiento. Manejar insectos vectores.","p":"Material de siembra sano. Control de trips."},
    "Cassava__healthy":{"n":"Yuca Saludable","e":"✅","g":"ninguna","d":"La yuca se encuentra en excelente estado.","t":"Ninguno requerido.","p":"Estacas certificadas. Rotacion de cultivos."},
    "Cassava__mosaic_disease":{"n":"Mosaico de la Yuca","e":"🌿","g":"alta","d":"CMD virus mas destructivo de la yuca. Mosaico y distorsion foliar.","t":"Sin cura. Eliminar plantas. Controlar mosca blanca.","p":"Variedades resistentes. Nunca usar estacas de plantas enfermas."},
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
    "Coffee__rust":{"n":"Roya del Cafe","e":"☕","g":"muy alta","d":"Hemileia vastatrix la mas devastadora del cafe. Polvo naranja en enves de hojas.","t":"URGENTE: Fungicidas triazoles propiconazol. Aplicar preventivamente cada 3 meses.","p":"Variedades resistentes Colombia o Castillo. Fungicidas preventivos."},
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
    "Rice__leaf_blast":{"n":"Piricularia del Arroz","e":"🌾","g":"muy alta","d":"Magnaporthe oryzae la mas importante del arroz mundial. Manchas romboidales.","t":"URGENTE: Fungicidas triazoles o estrobilurinas al inicio de sintomas.","p":"Variedades resistentes. Evitar exceso de nitrogeno."},
    "Rice__neck_blast":{"n":"Blast del Cuello del Arroz","e":"🌾","g":"muy alta","d":"Magnaporthe oryzae en cuello de panicula. Perdida total del grano.","t":"CRITICO: Fungicidas sistemicos en paniculacion antes de sintomas.","p":"Fungicidas preventivos en embuche. Variedades resistentes."},
    "Soybean__bacterial_blight":{"n":"Tizon Bacteriano de la Soya","e":"🌱","g":"alta","d":"Pseudomonas savastanoi. Manchas acuosas angulares amarillas en hojas.","t":"Bactericidas cobricos. Evitar labores con plantas mojadas.","p":"Semillas certificadas. Rotacion con cereales."},
    "Soybean__caterpillar":{"n":"Oruga de la Soya","e":"🌱","g":"alta","d":"Anticarsia gemmatalis defolia rapidamente el cultivo.","t":"Insecticidas biologicos Bt o quimicos. Monitoreo con umbrales.","p":"Monitoreo semanal desde V2. Control biologico."},
    "Soybean__diabrotica_speciosa":{"n":"Vaquita en Soya","e":"🌱","g":"media","d":"Diabrotica speciosa defolia hojas y ataca raices.","t":"Insecticidas al follaje. Tratamiento de semilla.","p":"Rotacion de cultivos. Monitoreo de adultos en bordes."},
    "Soybean__downy_mildew":{"n":"Mildiu Velloso de la Soya","e":"🌱","g":"media","d":"Peronospora manshurica. Polvo grisaceo en enves de hojas jovenes.","t":"Fungicidas metalaxil o fosetil. Aplicar preventivamente.","p":"Semilla tratada. Variedades resistentes."},
    "Soybean__healthy":{"n":"Soya Saludable","e":"✅","g":"ninguna","d":"El cultivo de soya se encuentra libre de enfermedades.","t":"Ninguno requerido.","p":"Rotacion de cultivos. Monitoreo regular."},
    "Soybean__mosaic_virus":{"n":"Virus Mosaico de la Soya","e":"🌱","g":"alta","d":"SMV transmitido por pulgones. Mosaico y reduccion de rendimiento.","t":"Sin cura. Control urgente de pulgones vectores.","p":"Semilla certificada libre de virus."},
    "Soybean__powdery_mildew":{"n":"Oidio de la Soya","e":"🌱","g":"media","d":"Microsphaera diffusa. Polvo blanco en hojas en etapas reproductivas.","t":"Fungicidas azufre o triazoles al inicio de sintomas.","p":"Variedades tolerantes. Densidades adecuadas."},
    "Soybean__rust":{"n":"Roya Asiatica de la Soya","e":"🌱","g":"muy alta","d":"Phakopsora pachyrhizi la mas destructiva de la soya. Pustulas beige.","t":"URGENTE: Fungicidas triazoles + estrobilurinas preventivamente.","p":"Monitoreo semanal. Fungicidas desde R1. Siembra temprana."},
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
    "Manzana":   {"e":"🍎","cls":["Apple__black_rot","Apple__healthy","Apple__rust","Apple__scab"]},
    "Yuca":      {"e":"🌿","cls":["Cassava__bacterial_blight","Cassava__brown_streak_disease","Cassava__green_mottle","Cassava__healthy","Cassava__mosaic_disease"]},
    "Cerezo":    {"e":"🍒","cls":["Cherry__healthy","Cherry__powdery_mildew"]},
    "Aji":       {"e":"🌶️","cls":["Chili__healthy","Chili__leaf curl","Chili__leaf spot","Chili__whitefly","Chili__yellowish"]},
    "Cafe":      {"e":"☕","cls":["Coffee__cercospora_leaf_spot","Coffee__healthy","Coffee__red_spider_mite","Coffee__rust"]},
    "Maiz":      {"e":"🌽","cls":["Corn__common_rust","Corn__gray_leaf_spot","Corn__healthy","Corn__northern_leaf_blight"]},
    "Pepino":    {"e":"🥒","cls":["Cucumber__diseased","Cucumber__healthy"]},
    "Guayabo":   {"e":"🍐","cls":["Gauva__diseased","Gauva__healthy"]},
    "Uva":       {"e":"🍇","cls":["Grape__black_measles","Grape__black_rot","Grape__healthy","Grape__leaf_blight_(isariopsis_leaf_spot)"]},
    "Jambolan":  {"e":"🫐","cls":["Jamun__diseased","Jamun__healthy"]},
    "Limon":     {"e":"🍋","cls":["Lemon__diseased","Lemon__healthy"]},
    "Mango":     {"e":"🥭","cls":["Mango__diseased","Mango__healthy"]},
    "Melocoton": {"e":"🍑","cls":["Peach__bacterial_spot","Peach__healthy"]},
    "Pimenton":  {"e":"🫑","cls":["Pepper_bell__bacterial_spot","Pepper_bell__healthy"]},
    "Granada":   {"e":"🍎","cls":["Pomegranate__diseased","Pomegranate__healthy"]},
    "Papa":      {"e":"🥔","cls":["Potato__early_blight","Potato__healthy","Potato__late_blight"]},
    "Arroz":     {"e":"🌾","cls":["Rice__brown_spot","Rice__healthy","Rice__hispa","Rice__leaf_blast","Rice__neck_blast"]},
    "Soya":      {"e":"🌱","cls":["Soybean__bacterial_blight","Soybean__caterpillar","Soybean__diabrotica_speciosa","Soybean__downy_mildew","Soybean__healthy","Soybean__mosaic_virus","Soybean__powdery_mildew","Soybean__rust","Soybean__southern_blight"]},
    "Fresa":     {"e":"🍓","cls":["Strawberry__healthy","Strawberry___leaf_scorch"]},
    "Cana":      {"e":"🌾","cls":["Sugarcane__bacterial_blight","Sugarcane__healthy","Sugarcane__red_rot","Sugarcane__red_stripe","Sugarcane__rust"]},
    "Te":        {"e":"🍵","cls":["Tea__algal_leaf","Tea__anthracnose","Tea__bird_eye_spot","Tea__brown_blight","Tea__healthy","Tea__red_leaf_spot"]},
    "Tomate":    {"e":"🍅","cls":["Tomato__bacterial_spot","Tomato__early_blight","Tomato__healthy","Tomato__late_blight","Tomato__leaf_mold","Tomato__mosaic_virus","Tomato__septoria_leaf_spot","Tomato__spider_mites_(two_spotted_spider_mite)","Tomato__target_spot","Tomato__yellow_leaf_curl_virus"]},
    "Trigo":     {"e":"🌾","cls":["Wheat__brown_rust","Wheat__healthy","Wheat__septoria","Wheat__yellow_rust"]},
}

# Map de clase -> cultivo
CLASE_A_CULTIVO = {}
for cult, dat in CULTIVOS.items():
    for c in dat["cls"]:
        CLASE_A_CULTIVO[c] = cult
