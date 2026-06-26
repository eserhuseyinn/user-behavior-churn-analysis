import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# 1. VERİYİ OKU
# -------------------------
df = pd.read_excel(
    r"C:/Users/pc/Desktop/veri6.xlsx",
    sheet_name="abonelikler",
    usecols=["kullanici_id", "paket_adi", "baslangic_tarihi", "bitis_tarihi", "abonelik_durumu"]
)

# -------------------------
# 2. TARİH DÖNÜŞÜMÜ
# -------------------------
df["baslangic_tarihi"] = pd.to_datetime(df["baslangic_tarihi"])
df["bitis_tarihi"] = pd.to_datetime(df["bitis_tarihi"])

# -------------------------
# 3. CHURN
# -------------------------
df["churn"] = df["bitis_tarihi"].notna()
#NOTNA BİTİŞ TARİHİ DOLU OLANLARA TRUE ATAR---BOŞ OLANLARA FALSE ATAR 

# -------------------------
# 4. İPTALLER
# -------------------------
iptaller = df[df["churn"] == True].copy()
iptaller["ay"] = iptaller["bitis_tarihi"].dt.to_period("M")
print("\n--- İPTALLER ---\n")
print(iptaller)
print("\n--- İPTALLER AY ---\n")
print(iptaller["ay"])

iptal_sayisi = (
    iptaller
    .groupby(["ay", "paket_adi"])
    .size()
    .reset_index(name="iptal")
)

# -------------------------
# 5. AKTİF (DAHA DOĞRU MODEL)
# -------------------------
aktif = (
    df
    .groupby([df["baslangic_tarihi"].dt.to_period("M"), "paket_adi"])
    .size()
    .reset_index(name="aktif")
)

aktif = aktif.rename(columns={"baslangic_tarihi": "ay"})

# -------------------------
# 6. BİRLEŞTİR
# -------------------------
churn_df = pd.merge(
    aktif,
    iptal_sayisi,
    on=["ay", "paket_adi"],
    how="left"
)

churn_df["iptal"] = churn_df["iptal"].fillna(0).astype(int)

# churn rate
churn_df["churn_rate"] = (churn_df["iptal"] / churn_df["aktif"]) * 100

# -------------------------
# 7. KRİTİK DÜZELTME → SIRALAMA
# -------------------------
churn_df["ay_dt"] = churn_df["ay"].dt.to_timestamp()
churn_df = churn_df.sort_values("ay_dt")

# -------------------------
# 8. ÇIKTILARI GÖSTER
# -------------------------
print("\n--- CHURN TABLOSU ---\n")
print(churn_df[["ay", "paket_adi", "aktif", "iptal", "churn_rate"]])

# -------------------------
# 9. GRAFİK (DÜZELTİLMİŞ)
# -------------------------
plt.figure(figsize=(12,6))

for paket in churn_df["paket_adi"].unique():
    data = churn_df[churn_df["paket_adi"] == paket]
    
    plt.plot(
        data["ay_dt"],   # <-- artık gerçek datetime
        data["churn_rate"],
        marker="o",
        label=paket
    )

plt.title("Aylık Paket Bazlı Churn Rate (İptal)%",fontsize=30)
plt.xlabel("Ay",labelpad=20,fontsize=20)
plt.ylabel("Churn Rate (%)",labelpad=20,fontsize=20)
plt.legend()
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()