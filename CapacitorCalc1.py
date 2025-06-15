import streamlit as st
import pdfplumber
import pandas as pd
import re
from io import BytesIO
from fpdf import FPDF
import math
import tempfile
import os 
st.set_page_config(
    page_title="CapacitoresCalc",
    layout="wide",      # <--- esto activa el modo ancho completo
    initial_sidebar_state="collapsed",
    page_icon="⚡",
    menu_items={
        'Get Help': None,
        'Report a bug': "mailto:guillermoocdiego19@gmail.com",
        'About': "Desarrollado por Guillermo Diego Ojeda Cueto"
    }
    
)
# Cambia el icono de la pestaña a un rayo

# --- CSS PARA DISEÑO PREMIUM "OLD MONEY" MEJORADO ---


st.markdown(r"""
<style>
            
/* --- Fondo azul marino premium --- */
[data-testid="stAppViewContainer"],
[data-testid="stMainContainer"] {
    background: #0A1929 !important;  /* Azul marino profundo */
    color: #E8E6E1 !important;      /* Marfil suave */
    padding: 20px !important;
    padding: 0 !important;
    margin: 0 auto !important;
    width: 100% !important;
    overflow-x: hidden !important; /* evita scroll horizontal y recortes */
}

            
/* --- Tipografía clásica premium con tamaño aumentado --- */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Montserrat:wght@300;400;500&display=swap');

html, body, .stMarkdown, .stText, p, label, input, .css-1lsmgbg.e1fqkh3o1 {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 24px !important;  /* Tamaño aumentado para mejor visibilidad */
    color: #E8E6E1 !important;
    line-height: 1.7;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 700 !important;
    color: #D4AF37 !important; /* Dorado clásico */
    letter-spacing: -0.5px;
    text-align: center;
    margin-bottom: 40px !important;  /* Más espacio */
}

h1 {
    font-size: 56px !important;  /* Tamaño aumentado */
    margin-top: 30px !important;
    border-bottom: 3px solid #D4AF37 !important;  /* Línea más gruesa */
    padding-bottom: 30px !important;
    text-transform: uppercase;
    letter-spacing: 2px;
}

h2 {
    font-size: 42px !important;  /* Tamaño aumentado */
    margin-top: 50px !important;
    border-bottom: 2px solid rgba(212, 175, 55, 0.3) !important;  /* Línea más gruesa */
    padding-bottom: 20px !important;
}

/* --- Diseño de pantalla completa --- */
.main-container {
    max-width: 100% !important;  /* Ocupa toda la pantalla */
    padding: 40px;
}

/* --- Tabs con estilo clásico y tamaño aumentado --- */
/* --- Tabs full-width y centradas --- */
.stTabs [role="tablist"] {
    display: flex !important;
    justify-content: center !important;
    border-bottom: 2px solid #2A4466 !important;
    margin-bottom: 20px !important;
    overflow: visible !important;
}
.stTabs [role="tablist"] button[role="tab"] {
    font-size: 28px !important;
    padding: 20px 40px !important;
    color: #A0B1C5 !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.3s;
    margin: 0 20px !important;
}
.stTabs [role="tablist"] button[role="tab"][data-selected="true"] {
    color: #D4AF37 !important;
    font-size: 32px !important;
    position: relative;
}
.stTabs [role="tablist"] button[role="tab"][data-selected="true"]::after {
    content: "";
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 4px;
    background: #D4AF37;
}

/* --- File Uploader premium con tamaño aumentado --- */
.stFileUploader > div > div {
    background: rgba(26, 54, 85, 0.5) !important;
    border: 3px dashed #2A4466 !important;  /* Borde más grueso */
    border-radius: 12px !important;  /* Bordes más redondeados */
    padding: 60px !important;  /* Más espacio interno */
    transition: all 0.3s;
    text-align: center;
    margin: 40px 0;  /* Más espacio */
    font-size: 28px !important;  /* Tamaño aumentado */
}

.stFileUploader > div > div:hover {
    border-color: #D4AF37 !important;
    background: rgba(26, 54, 85, 0.7) !important;
}

/* --- Botones con estilo clásico y tamaño aumentado --- */
.stButton > button {
    font-size: 28px !important;  /* Tamaño aumentado */
    padding: 24px 48px !important;  /* Más espacio interno */
    background: transparent !important;
    color: #D4AF37 !important;
    border: 3px solid #D4AF37 !important;  /* Borde más grueso */
    border-radius: 0 !important;
    transition: all 0.3s;
    font-weight: 500;
    letter-spacing: 2px;  /* Más espacio entre letras */
    margin: 30px auto;  /* Más espacio */
    display: block;
    width: 70%;  /* Más ancho */
}

.stButton > button:hover {
    background: rgba(212, 175, 55, 0.1) !important;
    transform: translateY(-5px);  /* Efecto más pronunciado */
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);  /* Sombra más pronunciada */
}

/* --- Tablas con estilo elegante y tamaño aumentado --- */
.stDataFrame {
    border: 2px solid #2A4466 !important;  /* Borde más grueso */
    border-radius: 0 !important;
    overflow: hidden;
    background: rgba(26, 54, 85, 0.3) !important;
    margin: 40px 0;  /* Más espacio */
    font-size: 24px !important;  /* Tamaño aumentado */
}

.stDataFrame th {
    background: #1A3658 !important;
    color: #D4AF37 !important;
    font-weight: 600 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 28px !important;  /* Tamaño aumentado */
    padding: 20px !important;  /* Más espacio interno */
}

.stDataFrame td {
    font-size: 24px !important;  /* Tamaño aumentado */
    padding: 20px !important;  /* Más espacio interno */
}

/* --- Mensajes de estado con tamaño aumentado --- */
.stAlert {
    border-radius: 0 !important;
    border-left: 5px solid #D4AF37 !important;  /* Línea más gruesa */
    background: rgba(26, 54, 85, 0.4) !important;
    margin: 30px 0;  /* Más espacio */
    font-size: 24px !important;  /* Tamaño aumentado */
    padding: 25px !important;  /* Más espacio interno */
}

/* --- Contenedores con borde dorado y tamaño aumentado --- */
.css-1v3fvcr {
    border: 2px solid #2A4466 !important;  /* Borde más grueso */
    border-radius: 0 !important;
    padding: 50px !important;  /* Más espacio interno */
    background: rgba(26, 54, 85, 0.3) !important;
    margin: 50px 0;  /* Más espacio */
    position: relative;
}

.css-1v3fvcr:before {
    content: "";
    position: absolute;
    top: 15px;  /* Más espacio */
    left: 15px;  /* Más espacio */
    right: 15px;  /* Más espacio */
    bottom: 15px;  /* Más espacio */
    border: 2px solid rgba(212, 175, 55, 0.3);  /* Borde más grueso */
    pointer-events: none;
}

/* --- Texto centrado --- */
.stMarkdown, .stText {
    text-align: center !important;
    font-size: 24px !important;  /* Tamaño aumentado */
}

/* --- Pie de página clásico con tamaño aumentado --- */
.footer {
    text-align: center;
    padding: 40px;
    margin-top: 60px;
    border-top: 2px solid #2A4466;  /* Línea más gruesa */
    color: #A0B1C5;
    font-size: 24px !important;  /* Tamaño aumentado */
    letter-spacing: 2px;  /* Más espacio entre letras */
}

/* --- Inputs elegantes con tamaño aumentado --- */
.stNumberInput, .stTextInput {
    background: rgba(26, 54, 85, 0.3) !important;
    border: 2px solid #2A4466 !important;  /* Borde más grueso */
    border-radius: 0 !important;
    color: #E8E6E1 !important;
    margin: 25px 0;  /* Más espacio */
    padding: 20px !important;  /* Más espacio interno */
    font-size: 24px !important;  /* Tamaño aumentado */
}

.stNumberInput input, .stTextInput input {
    color: #FFFFFF !important;
    font-size: 24px !important;  /* Tamaño aumentado */
    padding: 20px !important;  /* Más espacio interno */
}

/* --- Mejoras de accesibilidad --- */
/* Aumentar contraste para mejor visibilidad */
.stNumberInput label, .stTextInput label {
    color: #D4AF37 !important;
    font-size: 26px !important;
    font-weight: 500 !important;
}

/* Mejorar visibilidad de placeholders */
input::placeholder {
    color: #A0B1C5 !important;
    font-size: 24px !important;
}

/* Aumentar tamaño de iconos */
.stAlert svg {
    width: 36px !important;
    height: 36px !important;
}
            
</style>



""", unsafe_allow_html=True)
st.markdown("""
<style>
    /* --- Móvil (<768px): contenedor full-width y padding reducido --- */
    @media (max-width: 767px) {
        [data-testid="stAppViewContainer"],
        [data-testid="stMainContainer"] {
            width: 100% !important;
            margin: 0 !important;
            padding: 8px !important;
        }
        /* Hace que las tabs se apilen y ocupen 100% */
        .stTabs [role="tablist"] {
            flex-direction: column !important;
            align-items: stretch !important;
        }
        .stTabs [role="tablist"] button[role="tab"] {
            width: 100% !important;
            margin-bottom: 8px !important;
        }
        /* Tablas responsivas: scroll horizontal suave */
        .stDataFrame {
            display: block !important;
            width: 100% !important;
            overflow-x: auto !important;
        }
        /* Título responsivo */
        h1 {
            font-size: 32px !important; /* Tamaño reducido para pantallas pequeñas */
            margin-top: 20px !important;
        }
    }

    /* ——— Desktop / Tablet (>768px): mantén tu wide layout actual ——— */
    @media (min-width: 768px) {
        [data-testid="stAppViewContainer"],
        [data-testid="stMainContainer"] {
            width: 100% !important;     /* o usa max-width si prefieres centrar */
            padding: 20px !important;   /* tu padding normal */
        }
        /* Tabs en fila como ahora */
        .stTabs [role="tablist"] {
            flex-direction: row !important;
            justify-content: center !important;
        }
        /* Título en tamaño completo */
        h1 {
            font-size: 56px !important; /* Tamaño aumentado para pantallas grandes */
            margin-top: 30px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# CONTENIDO CON DISEÑO MEJORADO
# ------------------------------------------------
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# Encabezado premium con tamaño responsivo
st.markdown("<h1>COMPENSACIÓN ENERGÉTICA</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:32px; text-align:center; margin-bottom:50px;'>La herramienta definitiva para análisis avanzado de facturas eléctricas</p>", unsafe_allow_html=True)

# ------------------------------------------------
# PESTAÑAS PARA SELECCIÓN DE MODO
# ------------------------------------------------
tab_pdf, tab_manual = st.tabs([
    "📄 Extracción Automática desde PDF",
    "✍️ Ingreso Manual de Valores"
])



# --- FUNCIÓN UNIFICADA PARA CÁLCULO Y REPORTE ---
def calcular_y_reporte(
    df_cons, df_imp,
    modo_cable="Selección automática",
    corrientes_fijas=None, corrientes_variables=None,
    k_alimentacion=1.65, k_fijas=1.65, k_variables=1.65, k_contactor=1.45,
    cable_manual=None, etapas_fijas_manual=None, etapas_variables_manual=None,
    columna_sel=None, seccion_alimentacion=None, seccion_fijas=None, seccion_variables=None,
    st=st,mode=None
):
    
    # --- CÁLCULO DE FACTOR DE POTENCIA ---
    

    if "Tipo de Consumo" not in df_cons.columns:
        st.warning("No se ingresaron datos de consumo válidos.")
        return
    
    if "Concepto" not in df_imp.columns:
        st.warning("No se ingresaron datos de consumo válidos.")
        return
    df_cons["Tipo de Consumo"] = df_cons["Tipo de Consumo"].astype(str).str.strip().str.lower()
    fila_q = df_cons[df_cons["Tipo de Consumo"] == "reactiva mt"]
    q_mt = int(fila_q["Csmo. Result."].iloc[0]) if not fila_q.empty else 0

    if q_mt == 0:
        st.success("No hay necesidad de compensar (Reactiva MT = 0).")
        return

    p_fuera = df_cons.loc[df_cons["Tipo de Consumo"] == "activa fuera", "Csmo. Result."].sum()
    p_punta = df_cons.loc[df_cons["Tipo de Consumo"] == "activa punta", "Csmo. Result."].sum()
    activa = p_fuera + p_punta
    fp_medio = activa / math.sqrt(activa**2 + q_mt**2)

    st.markdown(f"""
    <div style='border: 2px solid #D4AF37; padding: 20px; background-color: rgba(212, 175, 55, 0.1);'>
        <h3 style='color: #D4AF37; text-align: center;'>Factor de Potencia Medio del Mes</h3>
        <p style='font-size: 36px; text-align: center; font-weight: bold;'>{fp_medio:.3f}</p>
    </div>
    """, unsafe_allow_html=True)

    if fp_medio < 0.92:
        penalidad = (0.92 - fp_medio) * 100 * 4
        st.error(f"""
        ⚠️ Según la reglamentación vigente de ANDE (Resolución N° 46984), se aplicará una multa del 4% por cada centésima por debajo de 0,92.
        Tu factor de potencia ({fp_medio:.3f}) implica una penalización aproximada del {penalidad:.2f}%.
        """)
    else:
        st.success("✅ Tu factor de potencia es superior a 0,92, no aplica multa según la Resolución N° 46984 de ANDE.")
        st.stop()

    # Suma exacta de importes específicos (MEA)
    total_energia_activa = df_imp.loc[
        df_imp['Concepto'].str.strip().str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').isin([
            'energia activa pc 10%', 'energia activa fpc 10%'
        ]),
        'Importe en G.'
    ].sum()

    multa_mer = (0.92 - fp_medio)* 4 * total_energia_activa

    st.markdown(f"""
    <div style='border: 2px solid #FF6B6B; padding: 20px; background-color: rgba(255, 107, 107, 0.1);'>
        <h3 style='color: #FF6B6B; text-align: center;'>Multa por Energía Reactiva (MER)</h3>
        <p style='font-size: 32px; text-align: center; font-weight: bold;'>Gs {multa_mer:,.2f}</p>
        <p style='text-align: center;'>Esta multa corresponde a la penalización por bajo factor de potencia según la Resolución N° 46984 de ANDE.</p>
    </div>
    """, unsafe_allow_html=True)

    # Cálculo de Potencia Activa máxima entre Potencia Fpc y Potencia Pc
    potencia_fpc = df_cons.loc[df_cons["Tipo de Consumo"] == "potencia fpc", "Csmo. Result."].iloc[0] if not df_cons.loc[df_cons["Tipo de Consumo"] == "potencia fpc"].empty else 0
    potencia_pc = df_cons.loc[df_cons["Tipo de Consumo"] == "potencia pc", "Csmo. Result."].iloc[0] if not df_cons.loc[df_cons["Tipo de Consumo"] == "potencia pc"].empty else 0
    Pactiva_max = max(potencia_fpc, potencia_pc)

    # --- Presentación del cálculo Qcapacitor ---
    st.markdown("""
    <div style='border: 3px solid #4CAF50; padding: 25px; background-color: rgba(76, 175, 80, 0.1); margin-top:30px;'>
        <h2 style='color: #4CAF50; text-align: center;'>📌 Solución: Utilización de Banco de Capacitores 📌</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <h2 style='color: #D4AF37; text-align: center; margin-bottom: 10px;'>Selecciona el Factor de Potencia Objetivo</h2>
    <p style='text-align: center; font-size: 22px;'>Recomendado: <strong>0.96</strong></p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fp_objetivo = st.slider(
            label=f"{mode}s", min_value=0.95, max_value=0.99, value=0.96, step=0.01,
            help="Selecciona el FP al que deseas llegar. Recomendado: 0.96"
        )

    # --- Cálculo por fórmula Qcap: Método trigonométrico ---
    Qcap_formula = Pactiva_max * (math.tan(math.acos(fp_medio)) - math.tan(math.acos(fp_objetivo)))

    # --- Cálculo por tabla ---
    tabla_raw = {
        0.77: {0.95: 0.5,   0.96: 0.537, 0.97: 0.578, 0.98: 0.626, 0.99: 0.680},
        0.78: {0.95: 0.473, 0.96: 0.510, 0.97: 0.551, 0.98: 0.599, 0.99: 0.659},
        0.79: {0.95: 0.447, 0.96: 0.484, 0.97: 0.525, 0.98: 0.573, 0.99: 0.633},
        0.80: {0.95: 0.421, 0.96: 0.458, 0.97: 0.499, 0.98: 0.547, 0.99: 0.609},
        0.81: {0.95: 0.395, 0.96: 0.432, 0.97: 0.473, 0.98: 0.521, 0.99: 0.581},
        0.82: {0.95: 0.369, 0.96: 0.406, 0.97: 0.447, 0.98: 0.495, 0.99: 0.555},
        0.83: {0.95: 0.343, 0.96: 0.380, 0.97: 0.421, 0.98: 0.469, 0.99: 0.529},
        0.84: {0.95: 0.317, 0.96: 0.354, 0.97: 0.395, 0.98: 0.443, 0.99: 0.503},
        0.85: {0.95: 0.291, 0.96: 0.328, 0.97: 0.369, 0.98: 0.417, 0.99: 0.477},
        0.86: {0.95: 0.264, 0.96: 0.301, 0.97: 0.342, 0.98: 0.390, 0.99: 0.450},
        0.87: {0.95: 0.238, 0.96: 0.275, 0.97: 0.316, 0.98: 0.364, 0.99: 0.424},
        0.88: {0.95: 0.211, 0.96: 0.248, 0.97: 0.289, 0.98: 0.337, 0.99: 0.397},
        0.89: {0.95: 0.183, 0.96: 0.220, 0.97: 0.261, 0.98: 0.309, 0.99: 0.369},
        0.90: {0.95: 0.155, 0.96: 0.192, 0.97: 0.233, 0.98: 0.281, 0.99: 0.341},
        0.91: {0.95: 0.127, 0.96: 0.164, 0.97: 0.205, 0.98: 0.253, 0.99: 0.313},
        0.92: {0.95: 0.097, 0.96: 0.134, 0.97: 0.175, 0.98: 0.223, 0.99: 0.283},
        0.93: {0.95: 0.066, 0.96: 0.103, 0.97: 0.144, 0.98: 0.192, 0.99: 0.252},
        0.94: {0.95: 0.034, 0.96: 0.071, 0.97: 0.112, 0.98: 0.160, 0.99: 0.220},
    }
    tabla_factor = pd.DataFrame(tabla_raw).T
    fp_orig_uso = max([f for f in tabla_factor.index if f <= fp_medio], default=fp_medio)
    fp_obj_uso = max([c for c in tabla_factor.columns if c <= fp_objetivo], default=fp_objetivo)
    try:
        k = tabla_factor.loc[fp_orig_uso, fp_obj_uso]
        Qcap_tabla = Pactiva_max * k
        metodo_usado = "tabla" if Qcap_tabla > Qcap_formula else "formula"
        Qcap_final = max(Qcap_formula, Qcap_tabla)
    except Exception:
        Qcap_final = Qcap_formula
        metodo_usado = "formula"
        k = None

    st.markdown(f"""
    <h3 style='color: #4CAF50; text-align: center;'>Potencia Reactiva Capacitiva Requerida (Qcap)</h3>
    <p style='font-size: 32px; text-align: center; font-weight: bold;'>{Qcap_final:.2f} kVAR</p>
    """, unsafe_allow_html=True)

    with st.expander("🔍 Saber más sobre este cálculo"):
        if metodo_usado == "formula":
            st.markdown(r"""
            Se utilizó el **método trigonométrico** por ser más conservador que la tabla:

            $$Q_{cap} = P_{activa\\_max} \\cdot [\\tan(\\cos^{-1}(FP_{medio})) - \\tan(\\cos^{-1}(FP_{objetivo}))]$$
            """)
        elif metodo_usado == "tabla":
            st.markdown(f"""
            Se utilizó el valor de la **tabla 'Fator de Potência ANDE'** por ser mayor que el método trigonométrico.

            $$Q_{{cap}} = {Pactiva_max:.2f} \\cdot {k:.3f} = {Qcap_tabla:.3f}\\ \\t{{kVAR}} $$

            Factor original considerado: **{fp_orig_uso}**  
            Factor objetivo buscado: **{fp_obj_uso}**
            """)

    valores_comerciales = [5, 7.5, 10, 15, 20, 25, 30, 40, 45, 50, 60, 70, 80, 90]
    valor_comercial_elegido = min(valores_comerciales, key=lambda x: abs(x - Qcap_final))

    st.markdown(f"""
    <div style='border: 2px solid #3E7C17; padding: 20px; background-color: rgba(62, 124, 23, 0.1);'>
        <h3 style='color: #3E7C17; text-align: center;'>📊 Selección del Banco de Capacitores</h3>
        <p style='font-size: 24px; text-align: center;'>
            Se recomienda optar por un banco de capacitores trifásico <strong>{valor_comercial_elegido:.1f} kVAR</strong>,
            que es el valor comercial más cercano a la potencia requerida de compensación ({Qcap_final:.2f} kVAR).
        </p>
    </div>
    """, unsafe_allow_html=True)

    valor_total = valor_comercial_elegido
    total_kvar = valor_comercial_elegido

    # --- Selección de etapas para banco de capacitores ---
    modo_etapas = st.radio(
        "\U0001F4CB Selecciona el modo de configuración de etapas:",
        ["Automática (recomendada)", "Personalizada por el usuario"],
        key=f'{mode}sss'
    )
    fijas = []
    variables = []

    if modo_etapas == "Automática (recomendada)":
        opcion_valida = False
        for etapa_fija in sorted(valores_comerciales, reverse=True):
            if etapa_fija / total_kvar <= 0.35:
                kvar_restante = total_kvar - etapa_fija
                posibles = [v for v in valores_comerciales if v <= etapa_fija and v / total_kvar <= 0.35]
                for n in range(1, 9):
                    combinaciones = [combo for combo in __import__('itertools').combinations_with_replacement(posibles, n)
                                    if sum(combo) == kvar_restante and 5 <= (1 + len(combo)) <= 8]
                    if combinaciones:
                        etapas_variables = combinaciones[0]
                        opcion_valida = True
                        break
            if opcion_valida:
                break

        if opcion_valida:
            fijas = [etapa_fija]
            variables = list(etapas_variables)
            st.success(f"\u2705 Opción recomendada: {etapa_fija} kVAR (etapa fija) + {len(etapas_variables)} etapas variables de {etapas_variables} kVAR")
        else:
            st.warning("\u26A0\ufe0f No se encontró una combinación óptima automática bajo los criterios establecidos.")
    else:
        etapa_fija_input = st.text_input("Ingresa valores de etapas fijas separados por coma (ej: 20,20)")
        etapa_variable_input = st.text_input("Ingresa valores de etapas variables separados por coma (ej: 10,10,10,10)")

        if etapa_fija_input and etapa_variable_input:
            try:
                fijas = [float(x.strip()) for x in etapa_fija_input.split(",")]
                variables = [float(x.strip()) for x in etapa_variable_input.split(",")]
                total_personal = sum(fijas) + sum(variables)
                etapas_total = len(fijas) + len(variables)

                if total_personal != total_kvar:
                    st.error(f"\u274C La suma total ingresada ({total_personal} kVAR) no coincide con el valor necesario ({total_kvar} kVAR).")
                elif etapas_total < 5 or etapas_total > 8:
                    st.error(f"\u274C La cantidad total de etapas debe estar entre 5 y 8. Actualmente hay {etapas_total}.")
                elif any(v > max(fijas) for v in variables):
                    st.error("\u274C Ninguna etapa variable puede tener un valor mayor al de las fijas.")
                elif any(v / total_kvar > 0.35 for v in fijas + variables):
                    st.error("\u274C Todas las etapas deben ser menores al 35% del total del banco.")
                else:
                    st.success(f"\u2705 Configuración personalizada válida:\n- Etapas fijas: {fijas}\n- Etapas variables: {variables}")
            except:
                st.error("\u274C Error en el formato. Asegúrate de usar comas y solo números válidos.")

    # --- Cálculo de corrientes ---
    def calcular_corrientes_por_etapa(lista_kvar, voltaje):
        corrientes = {}
        for kvar in set(lista_kvar):
            I = round(kvar * 1000 / (math.sqrt(3) * voltaje), 2)
            corrientes[kvar] = I
        return corrientes

    voltaje_nominal = 380
    corriente_total = round(valor_comercial_elegido * 1000 / (math.sqrt(3) * voltaje_nominal), 2)
    corrientes_fijas = calcular_corrientes_por_etapa(fijas, voltaje_nominal)
    corrientes_variables = calcular_corrientes_por_etapa(variables, voltaje_nominal)

    st.markdown(f"""
    <h3 style='color: #1E88E5; text-align: center; margin-top:40px; font-size: 40px;'>Corrientes por Etapa</h3>
    <p style='text-align: center; font-size: 32px;'>Corriente total: <strong>{corriente_total} A</strong></p>
    <p style='text-align: left; margin-left: 20%; font-size: 28px;'><strong>🔌 Etapas fijas:</strong></p>
    <ul style='margin-left: 25%; font-size: 26px;'>
        {''.join([f"<li>{k} kVAR → {v} A</li>" for k, v in corrientes_fijas.items()])}
    </ul>
    <p style='text-align: left; margin-left: 20%; font-size: 28px;'><strong>🔄 Etapas variables:</strong></p>
    <ul style='margin-left: 25%; font-size: 26px;'>
        {''.join([f"<li>{k} kVAR → {v} A</li>" for k, v in corrientes_variables.items()])}
    </ul>
    """, unsafe_allow_html=True)

    # --- Entrada de coeficientes de sobredimensionamiento ---
    st.markdown("#### Coeficientes para Sobredimensionamiento de Fusibles")
    col_a, col_f, col_v = st.columns(3)
    with col_a:
        k_alimentacion = st.number_input(
            "Coeficiente para fusible de alimentación",
            min_value=1.0, max_value=3.0, value=k_alimentacion, step=0.05,
            help="Recomendado entre 1.4 - 2.0",
            key=f"{mode}_k_alimentacion"
        )
    with col_f:
        k_fijas = st.number_input(
            "Coeficiente para fusibles de etapas fijas",
            min_value=1.0, max_value=3.0, value=k_fijas, step=0.05,
            help="Recomendado entre 1.4 - 2.0",
            key=f"{mode}_k_fijas"
        )
    with col_v:
        k_variables = st.number_input(
            "Coeficiente para fusibles de etapas variables",
            min_value=1.0, max_value=3.0, value=k_variables, step=0.05,
            help="Recomendado entre 1.4 - 2.0",
            key=f"{mode}_k_variables"
        )

    fusible_alimentacion = round(k_alimentacion * corriente_total, 2)
    fusibles_fijos = {k: round(v * k_fijas, 2) for k, v in corrientes_fijas.items()}
    fusibles_variables = {k: round(v * k_variables, 2) for k, v in corrientes_variables.items()}

    valores_comerciales_fusibles = [
        2, 4, 6, 10, 12, 16, 20, 25, 32, 40, 50, 63, 80, 100,
        125, 160, 200, 250, 315, 355, 400, 500, 630, 800
    ]
    def valor_comercial_mas_cercano(i_deseado, valores=valores_comerciales_fusibles):
        candidatos = [v for v in valores if v <= i_deseado]
        if candidatos:
            return max(candidatos)
        return min(valores)

    # --- TABLA DE FUSIBLES ---
    st.markdown(f"""
    <div style='border: 2px solid #3E7C17; padding: 25px; background-color: rgba(62, 124, 23, 0.1); border-radius: 10px;'>
        <h3 style='color: #3E7C17; text-align: center;'>Selección de Fusibles Comerciales (APR tipo GI)</h3>
        <table style='margin-left:auto; margin-right:auto; border-collapse:collapse; margin-bottom:20px;'>
            <thead>
                <tr style='background:#1A3658;'>
                    <th style='padding:10px 24px; color:#D4AF37; font-size:26px;'>Tipo</th>
                    <th style='padding:10px 24px; color:#D4AF37; font-size:26px;'>Etapa</th>
                    <th style='padding:10px 24px; color:#D4AF37; font-size:26px;'>I<sub>nom</sub> (A)</th>
                    <th style='padding:10px 24px; color:#D4AF37; font-size:26px;'>I<sub>fusible</sub> (A)</th>
                    <th style='padding:10px 24px; color:#D4AF37; font-size:26px;'>Fusible comercial (A)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style='padding:8px 24px; font-size:24px; color:#4CAF50; text-align:center;'>Alimentación</td>
                    <td style='padding:8px 24px; font-size:24px; color:#E8E6E1; text-align:center;'>{valor_total:.1f}kVAR</td>
                    <td style='padding:8px 24px; font-size:24px; color:#E8E6E1; text-align:center;'>{corriente_total:.2f}</td>
                    <td style='padding:8px 24px; font-size:24px; color:#E8E6E1; text-align:center;'>{corriente_total * k_alimentacion:.2f}</td>
                    <td style='padding:8px 24px; font-size:24px; color:#D4AF37; font-weight:bold; text-align:center;'>{valor_comercial_mas_cercano(corriente_total * k_alimentacion)}</td>
                </tr>
                {"".join([
                    f"<tr><td style='padding:8px 24px; font-size:24px; color:#4CAF50; text-align:center;'>Fija</td>"
                    f"<td style='padding:8px 24px; font-size:24px; color:#E8E6E1; text-align:center;'>{k:.1f} kVAR</td>"
                    f"<td style='padding:8px 24px; font-size:24px; color:#E8E6E1; text-align:center;'>{corrientes_fijas[k]:.2f}</td>"
                    f"<td style='padding:8px 24px; font-size:24px; color:#E8E6E1; text-align:center;'>{corrientes_fijas[k] * k_fijas:.2f}</td>"
                    f"<td style='padding:8px 24px; font-size:24px; color:#D4AF37; font-weight:bold; text-align:center;'>{valor_comercial_mas_cercano(corrientes_fijas[k] * k_fijas)}</td></tr>"
                    for k in sorted(corrientes_fijas)
                ])}
                {"".join([
                    f"<tr><td style='padding:8px 24px; font-size:24px; color:#4CAF50; text-align:center;'>Variable</td>"
                    f"<td style='padding:8px 24px; font-size:24px; color:#E8E6E1; text-align:center;'>{k:.1f} kVAR</td>"
                    f"<td style='padding:8px 24px; font-size:24px; color:#E8E6E1; text-align:center;'>{corrientes_variables[k]:.2f}</td>"
                    f"<td style='padding:8px 24px; font-size:24px; color:#E8E6E1; text-align:center;'>{corrientes_variables[k] * k_variables:.2f}</td>"
                    f"<td style='padding:8px 24px; font-size:24px; color:#D4AF37; font-weight:bold; text-align:center;'>{valor_comercial_mas_cercano(corrientes_variables[k] * k_variables)}</td></tr>"
                    for k in sorted(corrientes_variables)
                ])}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # --- Contactores ---
    st.markdown("#### Factor de Dimensionamiento para Contactores")
    k_contactor = st.number_input(
        "Factor de dimensionamiento para contactores",
        min_value=1.0, max_value=3.0, value=k_contactor, step=0.05,
        help="Recomendado entre 1.4 - 1.6",
        key=f"{mode}_k_contactor"
    )
    contactores_fijos = {k: round(v * k_contactor, 2) for k, v in corrientes_fijas.items()}
    contactores_variables = {k: round(v * k_contactor, 2) for k, v in corrientes_variables.items()}
    valores_comerciales_contactores = [
        10, 12, 16, 25, 32, 38, 40, 50, 65, 80, 95, 115, 150, 185, 225, 300, 400
    ]
    def valor_comercial_contactor(i_deseado, valores=valores_comerciales_contactores):
        for v in valores:
            if v >= i_deseado:
                return v
        return valores[-1]

    st.markdown(f"""
    <div style='border: 2px solid #3E7C17; padding: 25px; background-color: rgba(62, 124, 23, 0.1); border-radius: 10px;'>
        <h3 style='color: #3E7C17; text-align: center;'>Selección de Contactores Comerciales</h3>
        <table style='margin-left:auto; margin-right:auto; border-collapse:collapse; width:100%;'>
            <thead>
                <tr style='background:#1A3658;'>
                    <th style='padding:12px 16px; color:#D4AF37; font-size:20px;'>Tipo</th>
                    <th style='padding:12px 16px; color:#D4AF37; font-size:20px;'>Etapa</th>
                    <th style='padding:12px 16px; color:#D4AF37; font-size:20px;'>I<sub>cap</sub> (A)</th>
                    <th style='padding:12px 16px; color:#D4AF37; font-size:20px;'>I<sub>contactor</sub> (A)</th>
                    <th style='padding:12px 16px; color:#D4AF37; font-size:20px;'>Contactor comercial (A)</th>
                </tr>
            </thead>
            <tbody>
                {"".join([
                    f"<tr><td style='padding:10px 16px; font-size:18px; color:#4CAF50; text-align:center;'>Fija</td>"
                    f"<td style='padding:10px 16px; font-size:18px; color:#E8E6E1; text-align:center;'>{k:.1f} kVAR</td>"
                    f"<td style='padding:10px 16px; font-size:18px; color:#E8E6E1; text-align:center;'>{corrientes_fijas[k]:.2f}</td>"
                    f"<td style='padding:10px 16px; font-size:18px; color:#E8E6E1; text-align:center;'>{contactores_fijos[k]:.2f}</td>"
                    f"<td style='padding:10px 16px; font-size:18px; color:#D4AF37; font-weight:bold; text-align:center;'>{valor_comercial_contactor(contactores_fijos[k])}</td></tr>"
                    for k in sorted(contactores_fijos)
                ])}
                {"".join([
                    f"<tr><td style='padding:10px 16px; font-size:18px; color:#4CAF50; text-align:center;'>Variable</td>"
                    f"<td style='padding:10px 16px; font-size:18px; color:#E8E6E1; text-align:center;'>{k:.1f} kVAR</td>"
                    f"<td style='padding:10px 16px; font-size:18px; color:#E8E6E1; text-align:center;'>{corrientes_variables[k]:.2f}</td>"
                    f"<td style='padding:10px 16px; font-size:18px; color:#E8E6E1; text-align:center;'>{contactores_variables[k]:.2f}</td>"
                    f"<td style='padding:10px 16px; font-size:18px; color:#D4AF37; font-weight:bold; text-align:center;'>{valor_comercial_contactor(contactores_variables[k])}</td></tr>"
                    for k in sorted(contactores_variables)
                ])}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # --- Selección de cables (solo ejemplo, puedes adaptar para modo manual/auto) ---
    # Aquí puedes poner la lógica de selección automática o manual de cables, usando los argumentos recibidos

    # --- Botón para generar reporte PDF ---
    # ... (puedes mover aquí el código de generación de PDF, usando los argumentos y variables locales)

    ## Dimensionamiento de cables
                        # ---------------------------------------
                        # Interfaz principal
                        # ---------------------------------------
    st.title("📊 Selección de Sección de Cable")
    st.markdown("""
    Elige entre **Selección automática** (tabla Inpaco 2024)  
    o **Carga manual** de tus datos de cable.  
    Siempre se asume **sistema trifásico** (3 conductores cargados).
    """)

    modo = st.radio("Modo de entrada:", ("Selección automática", "Carga manual"), key=f"{mode}_modo_entrada")

    if modo == "Selección automática":
        # DataFrame cargado manualmente con las opciones de columnas
        df = pd.DataFrame({
"Seccion (mm²)": [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240],
"A1": [11.5, 16.0, 21.0, 27.0, 36.0, 48.0, 63.0, 78.0, 94.0, 118.0, 142.0, 164.0, 188.0, 213.0, 249.0],
"A2": [11.0, 15.0, 20.0, 25.0, 34.0, 45.0, 59.0, 72.0, 86.0, 109.0, 130.0, 150.0, 171.0, 194.0, 227.0],
"B1": [13.5, 18.0, 25.0, 32.0, 44.0, 59.0, 78.0, 96.0, 116.0, 148.0, 180.0, 208.0, 240.0, 273.0, 322.0],
"B2": [13.0, 17.5, 23.0, 30.0, 40.0, 54.0, 70.0, 86.0, 103.0, 130.0, 156.0, 180.0, 205.0, 233.0, 272.0],
"C": [15.0, 21.0, 28.0, 36.0, 50.0, 66.0, 98.0, 120.0, 146.0, 186.0, 225.0, 260.0, 299.0, 341.0, 401.0],
"D": [20.0, 27.0, 35.0, 44.0, 58.0, 75.0, 96.0, 116.0, 137.0, 169.0, 200.0, 228.0, 258.0, 289.0, 333.0],
})

        # Selección de columna por parte del usuario
        columna_sel = st.selectbox(
            "1) Selecciona el tipo de instalación:",
            ["A1", "A2", "B1", "B2", "C", "D"],
            help=(
                "A1: si el cable va embutido en pared o moldura (unipolar en tubo o multipolar directamente).\n\n"
                "A2: mismo caso que A1 pero exclusivo para cable multipolar en tubo circular embutido.\n\n"
                "B1: si el cable va en conducto o canaleta adosado a pared o suelo (distancia ≤ 0,3 D).\n\n"
                "B2: si ese conducto o canaleta queda dentro de un falso techo, piso técnico o galería "
                "(1,5 D ≤ espacio < 20 D).\n\n"
                "C: si el cable está fijado en superficie (muro, bandeja no perforada) sin conducto.\n\n"
                "D: si va enterrado (con o sin tubo, protegido mecánicamente)."
            ),
            key=f"{mode}_columna_sel"
        )

        # Mostrar DataFrame cargado
        st.markdown("**Tabla de cables (Inpaco 2024):**")
        st.dataframe(df)

        # Cálculo de Ifusible para alimentador, etapa fija y etapa variable
        Ifus_al = valor_comercial_mas_cercano(corriente_total * k_alimentacion)
        Ifus_fijas = {k: valor_comercial_mas_cercano(v * k_fijas) for k, v in corrientes_fijas.items()}
        Ifus_variables = {k: valor_comercial_mas_cercano(v * k_variables) for k, v in corrientes_variables.items()}

        # Filtrar sección que cumpla Icable > Ifusible para cada caso
        seccion_alimentacion = df[df[columna_sel] > Ifus_al].iloc[0]
        seccion_fijas = {k: df[df[columna_sel] > Ifus_fijas[k]].iloc[0] for k in corrientes_fijas}
        seccion_variables = {k: df[df[columna_sel] > Ifus_variables[k]].iloc[0] for k in corrientes_variables}

        # Mostrar resultados
        st.markdown("---")
        st.markdown("### Resultados de Selección de Cables")
        st.markdown("### Verificación de Condiciones para Alimentación y Etapas")
        st.markdown(f"**Alimentación:**")
        cumple_al = corriente_total < Ifus_al < seccion_alimentacion[columna_sel]
        st.markdown(f"- Corriente base: {corriente_total:.2f} A, Ifusible: {Ifus_al} A, Icable: {seccion_alimentacion[columna_sel]} A, Sección: {seccion_alimentacion['Seccion (mm²)']} mm²")
        st.markdown(f"- **Condición:** {'✅ Cumple' if cumple_al else '❌ No cumple'}")

        st.markdown("**Etapas Fijas:**")
        for k, s in seccion_fijas.items():
            cumple_fija = corrientes_fijas[k] < Ifus_fijas[k] < s[columna_sel]
            st.markdown(f"- Corriente base: {corrientes_fijas[k]:.2f} A, Ifusible: {Ifus_fijas[k]} A, Icable: {s[columna_sel]} A, Sección: {s['Seccion (mm²)']} mm²")
            st.markdown(f"- **Condición:** {'✅ Cumple' if cumple_fija else '❌ No cumple'}")

        st.markdown("**Etapas Variables:**")
        for k, s in seccion_variables.items():
            cumple_variable = corrientes_variables[k] < Ifus_variables[k] < s[columna_sel]
            st.markdown(f"- Corriente base: {corrientes_variables[k]:.2f} A, Ifusible: {Ifus_variables[k]} A, Icable: {s[columna_sel]} A, Sección: {s['Seccion (mm²)']} mm²")
            st.markdown(f"- **Condición:** {'✅ Cumple' if cumple_variable else '❌ No cumple'}")

    elif modo == "Carga manual":
        
        st.subheader("Carga manual de cables por tramo")
        st.markdown("### Verificación de Condiciones: Icable > Ifusible > Ibase")

        # --- Alimentador ---
        st.markdown("### Alimentador")
        Ifus_al = valor_comercial_mas_cercano(corriente_total * k_alimentacion)
        cable_al = st.text_input(
            "Nombre del cable alimentador",
            value="Cable X",
            key=f"{mode}_cable_alimentador",
        )
        icable_al = st.number_input(
            "Icable alimentador (A)",
            min_value=0.0,
            step=0.1,
            value=59.0,
            key=f"{mode}_icable_alimentador",
        )
        sec_al = st.number_input(
            "Sección del cable alimentador (mm²)",
            min_value=0.0,
            step=0.1,
            value=16.0,
            key=f"{mode}_sec_alimentador"
        )

        if icable_al <= Ifus_al:
            st.error(f"❌ Error: Icable alimentador ({icable_al:.2f} A) debe ser mayor que Ifusible comercial ({Ifus_al} A).")

        # --- Etapas Fijas ---
        st.markdown("### Etapas fijas")
        etapas_fijas = []
        for k in sorted(corrientes_fijas):
            st.markdown(f"#### Etapa fija {k} kVAR")
            cable_fj = st.text_input(
                f"Nombre del cable de etapa fija {k} kVAR",
                key=f"cable_fj_{k}_{mode}",
                value=f"{k} kVAR"
            )
            icable_fj = st.number_input(
                f"Icable de etapa fija {k} kVAR (A)",
                min_value=0.0,
                step=0.1,
                value=corrientes_fijas[k],
                key=f"icable_fj_{k}_{mode}",
                help=f"Advertencia: Este valor debe ser mayor al valor comercial del fusible. Ifusible comercial = {valor_comercial_mas_cercano(k_fijas * corrientes_fijas[k])} A"
            )
            sec_fj = st.number_input(
                f"Sección del cable de etapa fija {k} kVAR (mm²)",
                min_value=0.0,
                step=0.1,
                key=f"sec_fj_{k}_{mode}",
                value=16.0
            )
            if icable_fj <= valor_comercial_mas_cercano(k_fijas * corrientes_fijas[k]):
                st.error(f"❌ Error: Icable etapa fija {k} kVAR ({icable_fj:.2f} A) debe ser mayor que Ifusible comercial ({valor_comercial_mas_cercano(k_fijas * corrientes_fijas[k])} A).")
            etapas_fijas.append((cable_fj, icable_fj, sec_fj))

        # --- Etapas Variables ---
        st.markdown("### Etapas variables")
        etapas_variables = []
        for k in sorted(corrientes_variables):
            st.markdown(f"#### Etapa variable {k} kVAR")
            cable_var = st.text_input(
                f"Nombre del cable de etapa variable {k} kVAR",
                key=f"cable_var_{k}_{mode}",
                value=f"{k} kVAR"
            )
            icable_var = st.number_input(
                f"Icable de etapa variable {k} kVAR (A)",
                min_value=0.0,
                step=0.1,
                value=corrientes_variables[k],
                key=f"icable_var_{k}_{mode}",
                help=f"Advertencia: Este valor debe ser mayor al valor comercial del fusible. Ifusible comercial = {valor_comercial_mas_cercano(k_variables * corrientes_variables[k])} A"
            )
            sec_var = st.number_input(
                f"Sección del cable de etapa variable {k} kVAR (mm²)",
                min_value=0.0,
                step=0.1,
                key=f"sec_var_{k}_{mode}",
                value=16.0
            )
            if icable_var <= valor_comercial_mas_cercano(k_variables * corrientes_variables[k]):
                st.error(f"❌ Error: Icable etapa variable {k} kVAR ({icable_var:.2f} A) debe ser mayor que Ifusible comercial ({valor_comercial_mas_cercano(k_variables * corrientes_variables[k])} A).")
            etapas_variables.append((cable_var, icable_var, sec_var))
    
# --- Botón para generar reporte PDF ---

# --- Botón para generar reporte PDF --- 
    

    class PDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(0, 51, 102)  # Azul oscuro
            self.cell(0, 10, "Reporte de Compensación Energética", border=False, ln=True, align="C")
            self.ln(5)
            self.set_draw_color(0, 51, 102)
            self.set_line_width(0.5)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(128, 128, 128)  # Gris
            self.cell(0, 10, "HOUND ENERGY © 2025 | Página " + str(self.page_no()), align="C")

    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()

    # Título
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 51, 102)  # Azul oscuro
    pdf.cell(0, 10, "REPORTE DE COMPENSACIÓN ENERGÉTICA", ln=True, align="C")
    pdf.ln(10)

    # 1. Consumos extraídos
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 102, 204)  # Azul claro
    pdf.cell(0, 8, "1. Resumen de Consumos", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)  # Negro
    if df_cons.empty:
        pdf.cell(0, 6, "- No se encontraron consumos válidos", ln=True)
    else:
        for _, row in df_cons.iterrows():
            unidad = "KVARh" if "reactiva mt" in row['Tipo de Consumo'].lower() else "KWh"
            pdf.cell(0, 6,
                f"- {row['Tipo de Consumo']}: {row['Csmo. Result.']} {unidad}",
                ln=True
            )
    pdf.ln(5)

    # 2. Importes extraídos
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 102, 204)  # Azul claro
    pdf.cell(0, 8, "2. Detalle de Importes", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)  # Negro
    if df_imp.empty:
        pdf.cell(0, 6, "- No se encontraron importes válidos", ln=True)
    else:
        for _, row in df_imp.iterrows():
            pdf.cell(0, 6,
                f"- {row['Concepto']}: Gs {row['Importe en G.']:,}",
                ln=True
            )
    pdf.ln(5)

    # 3. Factor de potencia y penalización
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 102, 204)  # Azul claro
    pdf.cell(0, 8, "3. Factor de Potencia y Penalización", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)  # Negro
    pdf.cell(0, 6, f"- FP medio: {fp_medio:.3f}", ln=True)
    if fp_medio < 0.92:
        pdf.cell(0, 6, f"- Multa MER: Gs {multa_mer:,.2f}", ln=True)
    else:
        pdf.cell(0, 6, "- No aplica multa (FP ≥ 0.92)", ln=True)
    pdf.ln(5)

    # 4. Banco de capacitores
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 102, 204)  # Azul claro
    pdf.cell(0, 8, "4. Banco de Capacitores", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)  # Negro
    pdf.cell(0, 6, f"- Q requerido: {Qcap_final:.2f} kVAR", ln=True)
    pdf.cell(0, 6, f"- Comercial elegido: {valor_comercial_elegido:.1f} kVAR", ln=True)
    pdf.ln(5)

    # 5. Configuración de etapas
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 102, 204)  # Azul claro
    pdf.cell(0, 8, "5. Configuración de Etapas", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)  # Negro
    pdf.cell(0, 6,
        f"- Etapas fijas: {', '.join(str(v) for v in fijas)} kVAR", ln=True
    )
    pdf.cell(0, 6,
        f"- Etapas variables: {', '.join(str(v) for v in variables)} kVAR", ln=True
    )
    pdf.ln(5)


    # --- Agregar tabla de contactores comerciales al PDF ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 102, 204)  # Azul claro
    pdf.cell(0, 8, "6. Selección de Contactores Comerciales", ln=True)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, f"Factor de dimensionamiento utilizado para contactores: {k_contactor:.2f}", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)  # Negro

    # Encabezado de tabla
    pdf.cell(30, 7, "Tipo", border=1, align="C")
    pdf.cell(30, 7, "Etapa", border=1, align="C")
    pdf.cell(35, 7, "Icap (A)", border=1, align="C")
    pdf.cell(40, 7, "Icontactor (A)", border=1, align="C")
    pdf.cell(45, 7, "Contactor comercial (A)", border=1, align="C")
    pdf.ln()

    # Fijas
    for k in sorted(contactores_fijos):
        pdf.cell(30, 7, "Fija", border=1, align="C")
        pdf.cell(30, 7, f"{k:.1f} kVAR", border=1, align="C")
        pdf.cell(35, 7, f"{corrientes_fijas[k]:.2f}", border=1, align="C")
        pdf.cell(40, 7, f"{contactores_fijos[k]:.2f}", border=1, align="C")
        pdf.cell(45, 7, f"{valor_comercial_contactor(contactores_fijos[k])}", border=1, align="C")
        pdf.ln()
    # Variables
    for k in sorted(contactores_variables):
        pdf.cell(30, 7, "Variable", border=1, align="C")
        pdf.cell(30, 7, f"{k:.1f} kVAR", border=1, align="C")
        pdf.cell(35, 7, f"{corrientes_variables[k]:.2f}", border=1, align="C")
        pdf.cell(40, 7, f"{contactores_variables[k]:.2f}", border=1, align="C")
        pdf.cell(45, 7, f"{valor_comercial_contactor(contactores_variables[k])}", border=1, align="C")
        pdf.ln()
    pdf.ln(5)

# Mostrar tablas premium para fusibles
    # --- Agregar tabla de fusibles comerciales al PDF ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 102, 204)  # Azul claro
    pdf.cell(0, 8, "7. Selección de Fusibles Comerciales (APR tipo GI)", ln=True)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, f"Coeficiente de sobredimensionamiento alimentación: {k_alimentacion:.2f}", ln=True)
    pdf.cell(0, 6, f"Coeficiente de sobredimensionamiento etapas fijas: {k_fijas:.2f}", ln=True)
    pdf.cell(0, 6, f"Coeficiente de sobredimensionamiento etapas variables: {k_variables:.2f}", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)  # Negro

    # Encabezado de tabla
    pdf.cell(30, 7, "Tipo", border=1, align="C")
    pdf.cell(30, 7, "Etapa", border=1, align="C")
    pdf.cell(30, 7, "I_nom (A)", border=1, align="C")
    pdf.cell(35, 7, "I_fusible (A)", border=1, align="C")
    pdf.cell(45, 7, "Fusible comercial (A)", border=1, align="C")
    pdf.ln()

    # Alimentación
    pdf.cell(30, 7, "Alimentación", border=1, align="C")
    pdf.cell(30, 7, f"{valor_total:.1f} kVAR", border=1, align="C")
    pdf.cell(30, 7, f"{corriente_total:.2f}", border=1, align="C")
    pdf.cell(35, 7, f"{corriente_total * k_alimentacion:.2f}", border=1, align="C")
    pdf.cell(45, 7, f"{valor_comercial_mas_cercano(corriente_total * k_alimentacion)}", border=1, align="C")
    pdf.ln()

    # Etapas fijas
    for k in sorted(corrientes_fijas):
        pdf.cell(30, 7, "Fija", border=1, align="C")
        pdf.cell(30, 7, f"{k:.1f} kVAR", border=1, align="C")
        pdf.cell(30, 7, f"{corrientes_fijas[k]:.2f}", border=1, align="C")
        pdf.cell(35, 7, f"{corrientes_fijas[k] * k_fijas:.2f}", border=1, align="C")
        pdf.cell(45, 7, f"{valor_comercial_mas_cercano(corrientes_fijas[k] * k_fijas)}", border=1, align="C")
        pdf.ln()

    # Etapas variables
    for k in sorted(corrientes_variables):
        pdf.cell(30, 7, "Variable", border=1, align="C")
        pdf.cell(30, 7, f"{k:.1f} kVAR", border=1, align="C")
        pdf.cell(30, 7, f"{corrientes_variables[k]:.2f}", border=1, align="C")
        pdf.cell(35, 7, f"{corrientes_variables[k] * k_variables:.2f}", border=1, align="C")
        pdf.cell(45, 7, f"{valor_comercial_mas_cercano(corrientes_variables[k] * k_variables)}", border=1, align="C")
        pdf.ln()


    # 6. Selección de sección de cable
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 102, 204)  # Azul claro
    pdf.cell(0, 8, "8. Selección de Cable (3 conductores cargados)", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)  # Negro
    if modo == "Selección automática":
        pdf.cell(0, 6, "- Catálogo INPACO 2024:", ln=True)
        # Alimentador
        pdf.cell(0, 6,
            f"  - Alimentador ({columna_sel}): sección {seccion_alimentacion['Seccion (mm²)']} mm², "
            f"Icable {seccion_alimentacion[columna_sel]:.1f} A", ln=True
        )
        # Fijas
        pdf.cell(0, 6, "  - Etapas Fijas:", ln=True)
        for k, s in seccion_fijas.items():
            pdf.cell(0, 6,
                f"     - {k} kVAR: sección {s['Seccion (mm²)']} mm², "
                f"Icable {s[columna_sel]:.1f} A", ln=True
            )
        # Variables
        pdf.cell(0, 6, "  - Etapas Variables:", ln=True)
        for k, s in seccion_variables.items():
            pdf.cell(0, 6,
                f"     - {k} kVAR: sección {s['Seccion (mm²)']} mm², "
                f"Icable {s[columna_sel]:.1f} A", ln=True
            )
    elif modo == "Carga manual":
        # Alimentador
        pdf.cell(0, 6,
            f"- Alimentador ({cable_al}): sección {sec_al:.1f} mm², "
            f"Icable {icable_al:.2f} A", ln=True
        )
        # Fijas
        pdf.cell(0, 6, "- Etapas Fijas:", ln=True)
        for etapa in etapas_fijas:
            cable_fj, icable_fj, sec_fj = etapa
            pdf.cell(0, 6,
                f"   * {cable_fj}: sección {sec_fj:.1f} mm², "
                f"Icable {icable_fj:.2f} A", ln=True
            )
        # Variables
        pdf.cell(0, 6, "- Etapas Variables:", ln=True)
        for etapa in etapas_variables:
            cable_var, icable_var, sec_var = etapa
            pdf.cell(0, 6,
                f"   * {cable_var}: sección {sec_var:.1f} mm², "
                f"Icable {icable_var:.2f} A", ln=True
            )
    pdf.ln(10)

    # Pie de página
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(128, 128, 128)  # Gris
    pdf.cell(0, 6, "HOUND ENERGY © 2025", align="C")

    # Botón de descarga con diseño centrado y estilizado
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    st.download_button(
        label="📥 Descargar Reporte PDF",
        data=pdf_bytes,
        file_name="reporte_compensacion_energetica.pdf",
        mime="application/pdf",
        help="Haz clic para descargar el reporte en formato PDF",
        key=f"{mode}_download_pdf"
    )







# ------------------------------------------------
# Pestaña: Automático desde PDF
# ------------------------------------------------
# Carga de PDF compatible con PyInstaller (solo file_uploader, sin rutas locales)
with tab_pdf:
    st.markdown("<div class='css-1v3fvcr'>", unsafe_allow_html=True)
    st.header("📄 Extracción Automática desde PDF")
    st.markdown("""
    <p style='font-size:28px; text-align:center;'>
    Sube tu factura ANDE para un análisis automático de consumos e importes.<br>
    Si tienes problemas con la carga, asegúrate de que el archivo PDF no esté abierto en otro programa.
    </p>
    """, unsafe_allow_html=True)

    uploaded_pdf = st.file_uploader(
        "Selecciona tu factura ANDE en PDF",
        type=["pdf"],
        accept_multiple_files=False,
        help="Carga aquí tu factura ANDE en formato PDF para análisis automático."
    )

    if not uploaded_pdf:
        st.info("Por favor, selecciona un archivo PDF de factura para continuar.")
    else:
        try:
            file_bytes = uploaded_pdf.read()
            if not file_bytes:
                st.error("❌ No se pudo leer el archivo PDF. Intenta seleccionarlo nuevamente.")
            else:
                with st.spinner("🔍 Analizando documento..."):
                    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                        page = pdf.pages[0]
                        text = page.extract_text() or ""

                    if not text:
                        st.error("⚠️ No se pudo extraer texto del documento. ¿Es un PDF escaneado?")
                    else:
                        # Regex para consumos (incluye "Activa" y variaciones)
                        pat_cons = re.compile(
                            r"\d+\s+(Potencia FPC|Potencia PC|Reactiva MT|Activa(?: BT| fuera| punta)?)\s+\d+\s+\d+\s+\d+\s+(\d+)",
                            re.IGNORECASE
                        )
                        cons = pat_cons.findall(text)
                        df_cons = pd.DataFrame(cons, columns=["Tipo de Consumo", "Csmo. Result."])
                        df_cons["Tipo de Consumo"] = df_cons["Tipo de Consumo"].str.title().str.strip()
                        df_cons["Csmo. Result."] = df_cons["Csmo. Result."].astype(int)

                        # Regex para importes (incluye acentos y variantes PC/FPC)
                        pat_imp = re.compile(
                            r"(Energ[ií]a Activa(?: PC| FPC)? 10%|Energ[ií]a Reactiva 10%)\s+([\d\.]+)",
                            re.IGNORECASE
                        )
                        imps = pat_imp.findall(text)
                        df_imp = pd.DataFrame(imps, columns=["Concepto", "Importe en G."])
                        df_imp["Concepto"] = df_imp["Concepto"].str.title().str.strip()
                        df_imp["Importe en G."] = (
                            df_imp["Importe en G."].str.replace(".", "", regex=False).astype(int)
                        )

                        # Mostrar resultados
                        st.markdown("<div style='margin-top:40px;'>", unsafe_allow_html=True)
                        st.subheader("📊 Información de Consumos")
                        if df_cons.empty:
                            st.warning("ℹ️ No se encontraron consumos válidos en el documento")
                        else:
                            st.dataframe(df_cons.style.format(thousands=",", precision=0))

                        st.subheader("💰 Detalle de Importes")
                        if df_imp.empty:
                            st.warning("ℹ️ No se encontraron importes de Energía Activa/Reactiva")
                        else:
                            st.dataframe(df_imp.style.format({
                                "Importe en G.": lambda x: f"Gs {x:,.0f}"
                            }))

                        # Llamada al reporte final
                        calcular_y_reporte(df_cons, df_imp, mode="Auto")
        except Exception as e:
            st.error(f"❌ Error en el procesamiento: {e}")

    st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------------------------
# Pestaña: Ingreso Manual
# ------------------------------------------------
with tab_manual:
    st.markdown("<div class='css-1v3fvcr'>", unsafe_allow_html=True)
    st.header("✍️ Ingreso Manual de Valores")
    st.markdown("""
    <p style='font-size:28px; text-align:center;'>
    Ingresa manualmente los datos de tu factura para un análisis personalizado.<br>
    Utiliza esta opción si prefieres introducir los valores directamente.
    </p>
    """, unsafe_allow_html=True)
    
    # Consumos en sección premium con tamaño aumentado
    st.markdown("<div style='margin-top:30px; padding:30px; background: rgba(26, 54, 85, 0.5);'>", unsafe_allow_html=True)
    st.subheader("⚡️ Consumos (Csmo. Result.)")
    tipos = ["Potencia FPC", "Potencia PC", "Reactiva MT", "Activa BT", "Activa fuera", "Activa punta"]
    
    cols = st.columns(2)
    consumos = {}
    for i, t in enumerate(tipos):
        with cols[i % 2]:
            st.markdown(f"<div style='font-size:28px; margin-bottom:15px; color:#D4AF37;'>{t}</div>", unsafe_allow_html=True)
            consumos[t] = st.number_input(
                "a",
                min_value=0,
                step=1,
                key=f"num_{t}",
                format="%d",
                help=f"Ingrese el valor de {t}",
                label_visibility="collapsed"
            )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Importes en sección premium con tamaño aumentado
    st.markdown("<div style='margin-top:40px; padding:30px; background: rgba(26, 54, 85, 0.5);'>", unsafe_allow_html=True)
    st.subheader("💰 Importes (Gs.)")
    conceptos = ["Energía Activa PC 10%", "Energía Activa FPC 10%", "Energía Reactiva 10%"]
    
    importes = {}
    for c in conceptos:
        st.markdown(f"<div style='font-size:28px; margin-bottom:15px; color:#D4AF37;'>{c}</div>", unsafe_allow_html=True)
        importes[c] = st.number_input(
            label=f"Ingrese el importe de {c}",
            min_value=0,
            step=1,
            key=f"num_{c}",
            format="%d",
            help=f"Ingrese el importe de {c}",
            label_visibility="collapsed"
        )

    st.markdown("</div>", unsafe_allow_html=True)
    
    # Construcción de DataFrames para la función
    df_cons_m = pd.DataFrame(
        [{"Tipo de Consumo": t, "Csmo. Result.": v} for t, v in consumos.items() if v > 0]
    )
    df_imp_m = pd.DataFrame(
        [{"Concepto": c, "Importe en G.": v} for c, v in importes.items() if v > 0]
    )
    
    if not df_cons_m.empty or not df_imp_m.empty:
        st.subheader("📋 Resumen de Datos Ingresados")
        if not df_cons_m.empty:
            st.markdown("<div style='font-size:32px; margin-bottom:20px;'>Consumos</div>", unsafe_allow_html=True)
            st.dataframe(df_cons_m.style.format(thousands=",", precision=0))
        if not df_imp_m.empty:
            st.markdown("<div style='font-size:32px; margin-bottom:20px; margin-top:40px;'>Importes</div>", unsafe_allow_html=True)
            st.dataframe(df_imp_m.style.format({
                "Importe en G.": lambda x: f"Gs {x:,.0f}"
            }))
    else:
        st.info("ℹ️ Ingresa valores en los campos anteriores para ver el resumen")
    
    
    calcular_y_reporte(df_cons_m, df_imp_m,mode="Manual")

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# Pie de página premium con tamaño aumentado
# ------------------------------------------------
st.markdown("</div>", unsafe_allow_html=True)  # Cierre del contenedor principal
st.markdown("""
<div class='footer'>
    ⚡ HOUND ENERGY © 2025 | Tecnología de análisis eléctrico avanzado
    <div style='text-align:center; font-size:16px; color:#A0B1C5; margin-top:10px;'>
        Developed by Guillermo Diego Ojeda Cueto
    </div>
</div>
""", unsafe_allow_html=True)
