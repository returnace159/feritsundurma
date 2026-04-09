import streamlit as st
import math

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ferit Sundurma Şantiye Paneli", layout="wide")

# --- CSS: SIFIR BOŞLUK VE PROFESYONEL TABLO ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    .ana-baslik { font-size:42px !important; font-weight: bold; color: #1F618D; text-align: center; margin-bottom: 10px; }
    .kutu { background-color: #fdfefe; padding: 20px; border-radius: 12px; border: 2px solid #2E86C1; margin-bottom: 10px; }
    .sonuc-tablo { width: 100%; border-collapse: collapse; margin-top: 10px; }
    .sonuc-tablo td, .sonuc-tablo th { border: 1px solid #ddd; padding: 8px; text-align: left; }
    .sonuc-tablo th { background-color: #2E86C1; color: white; }
    .fiyat-vurgu { font-size:40px !important; color: #27AE60; font-weight: bold; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="ana-baslik">🏗️ FERİT SUNDURMA: ŞANTİYE ÖZETİ</p>', unsafe_allow_html=True)

# --- 1. VERİ BANKASI ---
hea_db = {
    "HEA 100": {"kg": 16.7, "ix": 349}, "HEA 120": {"kg": 19.9, "ix": 606},
    "HEA 140": {"kg": 24.7, "ix": 1030}, "HEA 160": {"kg": 30.4, "ix": 1670},
    "HEA 180": {"kg": 35.5, "ix": 2510}, "HEA 200": {"kg": 42.3, "ix": 3690}
}
kutu_db = {
    "40x40x3": 3.45, "60x60x3": 5.33, "80x80x3": 7.22, "100x100x4": 11.6, "120x120x4": 14.1
}

# --- 2. GİRDİ ALANI ---
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="kutu">', unsafe_allow_html=True)
    st.subheader("📐 Ölçüler ve Kesitler")
    uzunluk = st.number_input("Toplam Uzunluk (m)", value=50.0)
    genislik = st.number_input("Makas Açıklığı (m)", value=12.0)
    mahya_h = st.number_input("Mahya Yüksekliği (m)", value=1.5)
    secilen_hea = st.selectbox("HEA (Kolon)", list(hea_db.keys()))
    secilen_kutu = st.selectbox("Kutu Profil (Makas/Aşık)", list(kutu_db.keys()))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="kutu">', unsafe_allow_html=True)
    st.subheader("💹 Günlük Fiyatlar")
    hea_fiyat = st.number_input("HEA Fiyatı (TL/Kg)", value=31.0)
    kutu_fiyat = st.number_input("Kutu Profil Fiyatı (TL/Kg)", value=34.0)
    st.divider()
    kar_orani = st.number_input("Uygulanacak Kâr Oranı (%)", value=30, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. HESAPLAMA MOTORU ---
# Adetler
aks_sayisi = int((uzunluk / 6) + 1)
kolon_adet = aks_sayisi * 2
makas_adet = aks_sayisi

# Metrajlar
kolon_m = kolon_adet * 6.0 # Direkler 6m fix
hipotenus = math.sqrt((genislik/2)**2 + mahya_h**2)
makas_m = makas_adet * (genislik + 2 * hipotenus) * 1.45 # Ara kayıt payı dahil
asik_m = (int((hipotenus * 100) / 100) * 2 + 1) * uzunluk

# Ağırlıklar
kg_hea = kolon_m * hea_db[secilen_hea]["kg"]
kg_kutu = (makas_m + asik_m) * kutu_db[secilen_kutu]
ekstra_kg = (kg_hea + kg_kutu) * 0.07 # %7 plaka/kaynak

# Maliyetler
maliyet_hea = kg_hea * hea_fiyat
maliyet_kutu = kg_kutu * kutu_fiyat
maliyet_ekstra = ekstra_kg * ((hea_fiyat + kutu_fiyat)/2) # Ortalama fiyat

toplam_maliyet = maliyet_hea + maliyet_kutu + maliyet_ekstra
toplam_kar = toplam_maliyet * (kar_orani / 100)
toplam_teklif = toplam_maliyet + toplam_kar

# --- 4. SONUÇ EKRANI: KALEM KALEM DÖKÜM ---
st.markdown('<div class="kutu">', unsafe_allow_html=True)
st.subheader("📋 Malzeme ve Maliyet Detay Tablosu")

tablo_html = f"""
<table class="sonuc-tablo">
    <tr>
        <th>Profil Adı / Detay</th>
        <th>Ebat/Kesit</th>
        <th>Miktar</th>
        <th>Birim Fiyat</th>
        <th>Toplam Maliyet</th>
    </tr>
    <tr>
        <td>Ana Kolonlar (6m)</td>
        <td>{secilen_hea}</td>
        <td>{kg_hea:,.0f} Kg</td>
        <td>{hea_fiyat} TL</td>
        <td>{maliyet_hea:,.0f} TL</td>
    </tr>
    <tr>
        <td>Makaslar + Aşıklar</td>
        <td>{secilen_kutu}</td>
        <td>{kg_kutu:,.0f} Kg</td>
        <td>{kutu_fiyat} TL</td>
        <td>{maliyet_kutu:,.0f} TL</td>
    </tr>
    <tr>
        <td>Bağlantı Elemanları (Flanş/Kaynak)</td>
        <td>Plaka/Cıvata</td>
        <td>{ekstra_kg:,.0f} Kg</td>
        <td>Ort. Fiyat</td>
        <td>{maliyet_ekstra:,.0f} TL</td>
    </tr>
    <tr style="background-color: #f2f2f2; font-weight: bold;">
        <td colspan="4" style="text-align: right;">TOPLAM NET MALİYET:</td>
        <td>{toplam_maliyet:,.0f} TL</td>
    </tr>
    <tr style="color: #27AE60; font-weight: bold;">
        <td colspan="4" style="text-align: right;">HESAPLANAN KÂR ({kar_orani}%):</td>
        <td>{toplam_kar:,.0f} TL</td>
    </tr>
</table>
"""
st.markdown(tablo_html, unsafe_allow_html=True)

# GÖSTERİŞLİ FİNAL TEKLİF
st.divider()
c1, c2 = st.columns(2)
with c1:
    st.write("💰 **MÜŞTERİYE VERİLECEK TEKLİF:**")
    st.markdown(f'<p class="fiyat-vurgu">{toplam_teklif:,.0f} TL</p>', unsafe_allow_html=True)
with c2:
    st.info(f"🏗️ **Toplam Tonaj:** { (kg_hea + kg_kutu + ekstra_kg)/1000:.2f} Ton")
    st.success(f"📈 **Net Kârın:** {toplam_kar:,.0f} TL")

st.markdown('</div>', unsafe_allow_html=True)
