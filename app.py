import streamlit as st
import math

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ferit Sundurma Profesyonel", layout="wide")

# --- TASARIM (CSS) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    .ana-baslik { font-size:42px !important; font-weight: bold; color: #1F618D; text-align: center; margin-bottom: 10px; }
    .kutu { background-color: #fdfefe; padding: 20px; border-radius: 12px; border: 2px solid #2E86C1; margin-bottom: 10px; }
    .sonuc-tablo { width: 100%; border-collapse: collapse; margin-top: 10px; }
    .sonuc-tablo td, .sonuc-tablo th { border: 1px solid #ddd; padding: 12px; text-align: left; }
    .sonuc-tablo th { background-color: #2E86C1; color: white; }
    .fiyat-vurgu { font-size:45px !important; color: #27AE60; font-weight: bold; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="ana-baslik">🏗️ FERİT SUNDURMA HESAPLAMA SİSTEMİ</p>', unsafe_allow_html=True)

# --- 1. VERİ TABANI ---
hea_db = {
    "HEA 100": {"kg": 16.7, "ix": 349}, "HEA 120": {"kg": 19.9, "ix": 606},
    "HEA 140": {"kg": 24.7, "ix": 1030}, "HEA 160": {"kg": 30.4, "ix": 1670},
    "HEA 180": {"kg": 35.5, "ix": 2510}, "HEA 200": {"kg": 42.3, "ix": 3690}
}
kutu_db = {
    "40x40x3": 3.45, "60x60x3": 5.33, "80x80x3": 7.22, "100x100x4": 11.6, "120x120x4": 14.1
}

# --- 2. GİRİŞ PANELİ ---
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="kutu">', unsafe_allow_html=True)
    st.subheader("📏 Proje Ölçüleri")
    uzunluk = st.number_input("Sundurma Toplam Uzunluk (m)", value=50.0)
    genislik = st.number_input("Makas Açıklığı (m)", value=12.0)
    mahya_h = st.number_input("Makas Mahya Yüksekliği (m)", value=1.5)
    secilen_hea = st.selectbox("HEA Kesiti (Kolon)", list(hea_db.keys()), index=3) # HEA 160 Varsayılan
    secilen_kutu = st.selectbox("Kutu Profil (Makas/Aşık)", list(kutu_db.keys()), index=2) # 80x80 Varsayılan
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="kutu">', unsafe_allow_html=True)
    st.subheader("💰 Günlük Fiyat & Kâr")
    hea_fiyat = st.number_input("HEA Birim Fiyat (TL/Kg)", value=31.5)
    kutu_fiyat = st.number_input("Kutu Profil Birim Fiyat (TL/Kg)", value=34.0)
    st.divider()
    kar_orani = st.number_input("Uygulanacak Kâr Oranı (%)", value=30, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. HESAPLAMA MOTORU ---
# Aks ve Adetler (6 metre arayla)
aks_sayisi = int((uzunluk / 6) + 1)
kolon_adet = aks_sayisi * 2
# Makas Geometrisi
hipotenus = math.sqrt((genislik/2)**2 + mahya_h**2)
makas_m = aks_sayisi * (genislik + 2 * hipotenus) * 1.45 # %45 diyagonal payı
asik_m = (int((hipotenus * 100) / 100) * 2 + 1) * uzunluk # 1m arayla aşık

# Ağırlıklar
kg_hea = (kolon_adet * 6.0) * hea_db[secilen_hea]["kg"]
kg_kutu = (makas_m + asik_m) * kutu_db[secilen_kutu]
ekstra_kg = (kg_hea + kg_kutu) * 0.07 # %7 plaka/kaynak/cıvata

# Maliyetler
maliyet_hea = kg_hea * hea_fiyat
maliyet_kutu = kg_kutu * kutu_fiyat
maliyet_ekstra = ekstra_kg * ((hea_fiyat + kutu_fiyat) / 2)

toplam_maliyet = maliyet_hea + maliyet_kutu + maliyet_ekstra
toplam_kar = toplam_maliyet * (kar_orani / 100)
toplam_teklif = toplam_maliyet + toplam_kar

# Marmara Statik Analiz (Sehim)
# 100kg/m2 toplam yük (Kar+Zati)
sehim_cm = (5 * (1.0) * (genislik*100)**4) / (384 * 2100000 * hea_db[secilen_hea]["ix"])
sehim_limit = (genislik * 100) / 300

# --- 4. SONUÇ EKRANI ---
st.markdown('<div class="kutu">', unsafe_allow_html=True)
st.subheader("📋 Malzeme Detayları ve Statik Onay")

tablo_html = f"""
<table class="sonuc-tablo">
    <tr><th>Profil</th><th>Kesit</th><th>Miktar</th><th>Maliyet</th></tr>
    <tr><td>Ana Kolonlar</td><td>{secilen_hea}</td><td>{kg_hea:,.0f} Kg</td><td>{maliyet_hea:,.0f} TL</td></tr>
    <tr><td>Makas & Aşıklar</td><td>{secilen_kutu}</td><td>{kg_kutu:,.0f} Kg</td><td>{maliyet_kutu:,.0f} TL</td></tr>
    <tr><td>Ekstralar</td><td>Plaka/Kaynak</td><td>{ekstra_kg:,.0f} Kg</td><td>{maliyet_ekstra:,.0f} TL</td></tr>
    <tr style="font-weight:bold; background-color:#f2f2f2;"><td>NET TOPLAM</td><td>-</td><td>{(kg_hea+kg_kutu+ekstra_kg)/1000:.2f} Ton</td><td>{toplam_maliyet:,.0f} TL</td></tr>
</table>
"""
st.markdown(tablo_html, unsafe_allow_html=True)

# Statik Uyarı
if sehim_cm <= sehim_limit:
    st.success(f"✅ STATİK ONAY: 12m açıklıkta sehim ({sehim_cm:.2f} cm) limitler dahilinde.")
else:
    st.error(f"⚠️ STATİK RİSK: Sehim ({sehim_cm:.2f} cm) çok yüksek! Lütfen HEA kesitini büyütün.")

# Final Teklif
st.divider()
c3, c4 = st.columns(2)
with c3:
    st.write("💰 **TOPLAM TEKLİF TUTARI**")
    st.markdown(f'<p class="fiyat-vurgu">{toplam_teklif:,.0f} TL</p>', unsafe_allow_html=True)
with c4:
    st.write(f"📈 **Net Kârınız:** {toplam_kar:,.0f} TL")
    st.write(f"⚖️ **Toplam Ağırlık:** {(kg_hea+kg_kutu+ekstra_kg)/1000:.2f} Ton")
st.markdown('</div>', unsafe_allow_html=True)
