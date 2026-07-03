import streamlit as st
import random
import datetime
import base64

# --- IMPOSTAZIONI PAGINA (Deve essere SEMPRE il primo comando) ---
st.set_page_config(
    page_title="Stima Quadro Economico Rilievi PA", 
    page_icon="🏛️", 
    layout="centered"
)

# 1. Definisci questa funzione in alto
def imposta_sfondo_app(percorso_immagine):
    """
    Legge un'immagine locale e la imposta come sfondo dell'app Streamlit,
    creando un riquadro semitrasparente per i contenuti.
    """
    try:
        with open(percorso_immagine, 'rb') as f:
            data = f.read()
        img_base64 = base64.b64encode(data).decode()
        
        css_sfondo = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.92); 
            padding: 3rem;
            border-radius: 15px;
            box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.15);
        }}
        </style>
        """
        st.markdown(css_sfondo, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error(f"Errore: L'immagine '{percorso_immagine}' non è stata trovata.")

# 2. Richiami lo sfondo
# inserire tra le virgolette tra parentesi il nome del file immagine con il suffisso di formato
imposta_sfondo_app("")

# --- STILI CSS PERSONALIZZATI ---
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1a252f;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #34495e;
        text-align: center;
        margin-bottom: 30px;
        font-style: italic;
    }
    .section-title {
        color: #c5a880;
        border-bottom: 2px solid #1a252f;
        padding-bottom: 5px;
    }
    .result-box {
        background-color: #f4f6f7;
        border-left: 5px solid #1a252f;
        padding: 20px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INTESTAZIONE ---
st.markdown('<div class="main-header">CALCOLATORE PARCELLE PA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Stima Parametrica per Affidamento Rilievi 3D e Restituzione Architettonica</div>', unsafe_allow_html=True)
st.divider()

# --- SEZIONE 1: INPUT DATI ---
st.markdown('<h3 class="section-title">1. Parametri di Rilievo</h3>', unsafe_allow_html=True)

superficie = st.number_input("Superficie stimata dell'immobile (mq):", min_value=50, value=1200, step=50, help="Indicare la superficie lorda complessiva da rilevare.")

finalita_options = {
    "Censimento / Fascicolo Fabbricato": 1.00,
    "Piani Eliminazione Barriere (PEBA)": 1.15,
    "Adeguamento Sismico / Antincendio": 1.35,
    "Restauro Beni Culturali / Ville Venete": 1.60
}
finalita = st.selectbox(
    "Finalità del Rilievo (Determina la complessità della restituzione):", 
    list(finalita_options.keys())
)
molt_finalita = finalita_options[finalita]

livello_options = [
    "Livello 1 - Solo Nuvola di Punti (Navigatore Web)",
    "Livello 2 - Restituzione CAD 2D (Piante, Prospetti, Sezioni)",
    "Livello 3 - Modello HBIM (Historic Building Information Modeling)"
]
livello = st.selectbox("Livello di Restituzione Richiesto:", livello_options)

# Imposto la variabile fissa per i calcoli matematici
spese_fisse = 300.00

# Lo mostro a schermo come semplice testo bloccato (senza pulsanti)
st.text_input(
    "Spese Fisse Istruttoria (Oneri sicurezza, MEPA, Pratiche):", 
    value="300,00 €", 
    disabled=True, 
    help="Quota fissa non modificabile."
)

st.divider()

# --- MOTORE DI CALCOLO ---
# 1. Costo Base Acquisizione in sito (Economia di scala)
if superficie <= 500:
    costo_acq_base = 1.50
elif superficie <= 2000:
    costo_acq_base = 1.00
else:
    costo_acq_base = 0.70

# 2. Costo Base Elaborazione CAD (Economia di scala)
if superficie <= 500:
    costo_cad_base = 3.50
elif superficie <= 2000:
    costo_cad_base = 2.50
else:
    costo_cad_base = 1.80

# 3. Calcolo Voci di Costo
quota_acquisizione = superficie * costo_acq_base

if livello == "Livello 1 - Solo Nuvola di Punti (Navigatore Web)":
    quota_elaborazione = 0
elif livello == "Livello 3 - Modello HBIM (Historic Building Information Modeling)":
    # Costo fisso base BIM (es. 12€) moltiplicato per la finalità
    quota_elaborazione = superficie * 12.00 * molt_finalita
else:
    # Livello 2 (CAD)
    quota_elaborazione = superficie * costo_cad_base * molt_finalita

totale_imponibile = quota_acquisizione + quota_elaborazione + spese_fisse
cassa = totale_imponibile * 0.04
subtotale = totale_imponibile + cassa
iva = subtotale * 0.22
totale_lordo = subtotale + iva

# --- SEZIONE 2: QUADRO ECONOMICO ---
st.markdown('<h3 class="section-title">2. Quadro Economico Preliminare</h3>', unsafe_allow_html=True)

# Apro il div del box grigio
st.markdown('<div class="result-box">', unsafe_allow_html=True)

st.markdown(f"**Quota Acquisizione Dato in Sito (SLAM):** {quota_acquisizione:,.2f} €")
st.markdown(f"**Quota Post-Produzione ed Elaborazione:** {quota_elaborazione:,.2f} €")
st.markdown(f"**Spese Fisse / Tecniche:** {spese_fisse:,.2f} €")
st.markdown("---")
st.markdown(f"#### **TOTALE IMPONIBILE (Base per Affidamento): {totale_imponibile:,.2f} €**")
st.markdown(f"Contributo Integrativo Inarcassa (4%): {cassa:,.2f} €")
st.markdown(f"IVA (22%): {iva:,.2f} €")
st.markdown(f"### **TOTALE LORDO COMPLESSIVO: {totale_lordo:,.2f} €**")

# Chiudo il div del box grigio
st.markdown('</div>', unsafe_allow_html=True)

# Avviso normativo
if totale_imponibile < 140000:
    st.success("✅ **Importo compatibile con l'Affidamento Diretto** ai sensi del D.Lgs. 36/2023 (Codice degli Appalti) per l'acquisizione di servizi di Ingegneria e Architettura.")
else:
    st.warning("⚠️ L'importo stimato supera la soglia per l'affidamento diretto. Richiede procedura negoziata o bando di gara.")

st.caption("Il presente calcolo è da intendersi come stima preliminare e non costituisce offerta formale.")

st.divider()

# --- SEZIONE 3: RICHIESTA INCONTRO TECNICO ---
st.markdown('<h3 class="section-title">3. Richiesta Incontro Istruttorio</h3>', unsafe_allow_html=True)
st.write("Compili i campi sottostanti per richiedere un sopralluogo tecnico o un incontro conoscitivo con il nostro studio.")

col_ente, col_rup = st.columns(2)
with col_ente:
    nome_ente = st.text_input("Ente Richiedente (Es. Comune di Noventa Vicentina):")
with col_rup:
    nome_rup = st.text_input("Referente / RUP:")

col_mail, col_tel = st.columns(2)
with col_mail:
    email_ente = st.text_input("Email / PEC Istituzionale:")
with col_tel:
    telefono_ente = st.text_input("Recapito Telefonico:")

indirizzo_immobile = st.text_input("Indirizzo dell'immobile oggetto di potenziale rilievo:")

# Captcha
if 'captcha_a' not in st.session_state:
    st.session_state.captcha_a = random.randint(1, 9)
    st.session_state.captcha_b = random.randint(1, 9)

st.write(f"🤖 **Controllo di sicurezza: {st.session_state.captcha_a} + {st.session_state.captcha_b}?**")
risposta_captcha = st.text_input("Inserire il risultato per abilitare l'invio:")
somma_corretta = str(st.session_state.captcha_a + st.session_state.captcha_b)

# Invio Email
if st.button("✉️ Invia Richiesta all'Ufficio Tecnico", type="primary"):
    if not (nome_ente and nome_rup and email_ente and telefono_ente and indirizzo_immobile):
        st.error("Compilare tutti i campi richiesti.")
    elif risposta_captcha != somma_corretta:
        st.error("Risultato matematico errato.")
    else:
        oggetto = f"Richiesta Rilievo PA - {nome_ente}"
        corpo_email = f"""È stata generata una nuova stima quadro economico dal portale PA.

DATI ENTE:
- Ente: {nome_ente}
- Referente: {nome_rup}
- Recapiti: {telefono_ente} | {email_ente}
- Immobile: {indirizzo_immobile}

DETTAGLIO STIMA:
- Superficie: {superficie} mq
- Finalità: {finalita}
- Livello richiesto: {livello}

QUADRO ECONOMICO:
- Imponibile: {totale_imponibile:,.2f} €
- Totale Lordo: {totale_lordo:,.2f} €
"""
        try:
            import smtplib
            from email.mime.text import MIMEText

            msg = MIMEText(corpo_email)
            msg['Subject'] = oggetto
            msg['From'] = "studioandriolo@gmail.com"
            msg['To'] = "studioandriolo@gmail.com"

            # Nota: Assicurati di aver configurato i secrets su Streamlit Cloud!
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("studioandriolo@gmail.com", st.secrets["GMAIL_PASSWORD"])
            server.send_message(msg)
            server.quit()

            st.success("✅ Richiesta inoltrata con successo. Il nostro studio La ricontatterà a breve.")
            
            # Reset captcha
            st.session_state.captcha_a = random.randint(1, 9)
            st.session_state.captcha_b = random.randint(1, 9)
            
        except Exception as e:
            st.error(f"⚠️ Errore nell'invio della comunicazione. Verificare la configurazione del server SMTP.")
