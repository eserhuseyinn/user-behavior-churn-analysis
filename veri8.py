import pandas as pd
import matplotlib.pyplot as plt

# 1. Veriyi Oku
df1 = pd.read_excel(r"C:/Users/pc/Desktop/veri6.xlsx", sheet_name="uaktivite")
df2 = pd.read_excel(r"C:/Users/pc/Desktop/veri6.xlsx", sheet_name="abonelikler")

# 2. Verileri Birleştir ve Grupla
df3 = df2.merge(df1, on="kullanici_id", how="inner")
df3_group = df3.groupby("abonelik_durumu")[["oturum_suresi_dk", "tiklama_sayisi", "hata_aldi_mi"]].mean()
print(df3_group)

# ------------------------------------------------------------------
# 3. 3'LÜ SUBPLOT OLUŞTURMA (Her Metrik Kendi Ölçeğinde)
# ------------------------------------------------------------------
# 1 satır, 3 sütundan oluşan geniş bir grafik alanı yaratıyoruz.
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))

# --- 1. GRAFİK (Sol): Oturum Süresi ---
df3_group["oturum_suresi_dk"].plot(kind="bar", ax=axes[0], color=["#3498db", "#e74c3c"])
axes[0].set_title("Ortalama Oturum Süresi", fontsize=12, fontweight='bold')
axes[0].set_ylabel("Dakika", fontsize=11)
axes[0].set_xticklabels(df3_group.index, rotation=0)
axes[0].grid(True, linestyle="--", alpha=0.5)

# --- 2. GRAFİK (Orta): Tıklama Sayısı ---
df3_group["tiklama_sayisi"].plot(kind="bar", ax=axes[1], color=["#2ecc71", "#27ae60"])
axes[1].set_title("Ortalama Tıklama Sayısı", fontsize=12, fontweight='bold')
axes[1].set_ylabel("Tıklama Adedi", fontsize=11)
axes[1].set_xticklabels(df3_group.index, rotation=0)
axes[1].grid(True, linestyle="--", alpha=0.5)

# --- 3. GRAFİK (Sağ): Hata Alma Oranı ---
# Burada değerler küçük (0-1 arası) olduğu için artık tamamen net görünecek!
df3_group["hata_aldi_mi"].plot(kind="bar", ax=axes[2], color=["#e67e22", "#d35400"])
axes[2].set_title("Ortalama Hata Alma Oranı", fontsize=12, fontweight='bold')
axes[2].set_ylabel("Hata Oranı (0 - 1)", fontsize=11)
axes[2].set_xticklabels(df3_group.index, rotation=0)
axes[2].grid(True, linestyle="--", alpha=0.5)

# ------------------------------------------------------------------
# KODUN EN SONUNDAKİ GÖSTERME KISMI
# ------------------------------------------------------------------

# tight_layout() yerine bunu kullanıyoruz, üstten %15 boşluk bırakır (top=0.85)
plt.subplots_adjust(top=0.85, bottom=0.15, wspace=0.3)

# Ana başlığı ekliyoruz
plt.suptitle("Abonelik Durumuna Göre Kullanıcı Davranış Analizi", fontsize=16, fontweight='bold')

plt.show()