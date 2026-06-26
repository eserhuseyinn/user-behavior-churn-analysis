import pandas as pd
import matplotlib.pyplot as plt

df2 = pd.read_excel(r"C:/Users/pc/Desktop/veri6.xlsx", sheet_name="abonelikler")
df3 = pd.read_excel(r"C:/Users/pc/Desktop/veri6.xlsx", sheet_name="uaktivite")

df = df2.merge(df3, on="kullanici_id", how="inner")
#df df2vedf3 ün birleşmiş hali merge(birleştir) on(neye göre) how(ortak olanlar)

print(df["abonelik_durumu"].value_counts(normalize=True) * 100)
#valuecounts fonksiyon analizi

print(df.groupby(["paket_adi", "abonelik_durumu"]).size())

df["abonelik_durumu"].value_counts().plot(kind="pie")
plt.title("Kullanıcıların Abonelik Durumu")
plt.show()

df.groupby(["paket_adi", "abonelik_durumu"]).size().unstack().plot(kind="bar")
plt.title("Paketlere Göre Abonelik Durumu")
plt.ylim(0,50)
plt.xticks(rotation=0)
plt.ylabel("Abonelik Sayıları",labelpad=30,fontsize=20)
plt.xlabel("Paket Adları",labelpad=30,fontsize=20)
plt.show()

