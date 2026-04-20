import streamlit as st
import numpy as np 
import matplotlib.pyplot as plt 
import scipy.stats as stats

# header page 
st.set_page_config(page_title="CLT Visualizer", layout="wide")
st.title("📊 Central Limit Theorem (CLT) Visualizer")
st.markdown("""
Dashboard ini dikembangkan oleh **Ilham Rasyid** untuk mendemostrasikan kekuatan
**Teorema Limit Pusat**. Meskipun populasi aslinya tidak normal, distribusi rata-rata sampelnya akan tetap normal. 
""")

# sidebar input
st.sidebar.header("Pengaturan Simulasi")
dist_type = st.sidebar.selectbox(
    "Pilih Distribusi Populasi", 
    ("Normal", "Exponential", "Uniform", "Gamma", "Weibull", "Rayleigh", "Cauchy")
)

n_size = st.sidebar.slider("Ukuran Sampel (n)", min_value=1, max_value=1000, value=30)
n_simulations = st.sidebar.slider("Jumlah Simulasi (Berapa kali ambil sampel)", 100, 10000, 1000, 100)

# 1. Generate Populasi Berdasarkan Pilihan 
np.random.seed(2026)
size_pop = 20000

if dist_type == "Normal":
    population = np.random.normal(loc=50, scale=10, size=size_pop)
elif dist_type == "Exponential":
    population = np.random.exponential(scale=2.0, size=size_pop)
elif dist_type == "Uniform":
    population = np.random.uniform(low=0, high=100, size=size_pop)
elif dist_type == "Gamma":
    population = np.random.gamma(shape=2, scale=2, size=size_pop)
elif dist_type == "Weibull":
    population = np.random.weibull(a=1.5, size=size_pop) * 20 # dikali 20 agar skalanya terlihat jelas
elif dist_type == "Rayleigh":
    population = np.random.rayleigh(scale=5.0, size=size_pop)
elif dist_type == "Cauchy":
    population = np.random.standard_cauchy(size=size_pop)

# 2. Proses Simulasi
sample_means = []
for _ in range(n_simulations):
    sample = np.random.choice(population, size=n_size)
    sample_means.append(np.mean(sample))

# 3. Visualisasi dengan Matplotlib
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"1. Distribusi Populasi Asli ({dist_type})")
    fig1, ax1 = plt.subplots()

    if dist_type == "Cauchy":
        ax1.hist(population, bins=100, range=(-20, 20), color='#3498db', edgecolor='white', alpha=0.7)
    else:
        ax1.hist(population, bins=50, color='#3498db', edgecolor='white', alpha=0.7)

    ax1.set_xlabel("Nilai Data")
    ax1.set_ylabel("Frekuensi")
    st.pyplot(fig1)

with col2:
    st.subheader(f"2. Distribusi Rata-rata Sampel (n={n_size})")
    fig2, ax2 = plt.subplots()

    if dist_type == "Cauchy":
        count, bins, ignored = ax2.hist(sample_means, bins=100, range=(-20, 20), color='#e74c3c', edgecolor='white', density=True, alpha=0.7)
    else:
        count, bins, ignored = ax2.hist(sample_means, bins=50, color='#e74c3c', edgecolor='white', density=True, alpha=0.7)

        # tambahkan kurva normal ideal (kecuali cauchy)
        mu, std = stats.norm.fit(sample_means)
        x = np.linspace(min(bins), max(bins), 100)
        p = stats.norm.pdf(x, mu, std)
        ax2.plot(x, p, 'k', linewidth=2, label='Kurva Normal') 
        ax2.legend()

    ax2.set_xlabel("Rata-rata Sampel")
    ax2.set_ylabel("Densitas")
    st.pyplot(fig2)

# interpretasi dinamis
st.divider()
st.subheader("💡 Apa yang sedang terjadi?")

if dist_type == "Normal":
    st.write(f"""
    Karena populasi asal sudah berdistribusi **Normal**, distribusi rata-rata sampelya akan selalu berdistribusi normal, 
    bahkan saat $n=1$. seiring dengan bertambahnya ukuran sampel ($n$), Anda akan melihat bahwa distribusinya menjadi
    semakin sempit (varians mengecil). Ini membuktikan bahwa rata-rata sampel menjadi penaksir yang lebih presisi
    terhadap rata-rata populasi.
    """)
elif dist_type == "Cauchy":
    st.write(f"""
    **Pengecualian Teorema Limit Pusat!** Distribusi **Cauchy** adalah distribusi *heavy-tailed* yang varians dan 
    nilai harapannya tidak terdefinisi. Perhatikan grafik di atas: berapapun Anda memperbesar ukuran sampel ($n$), 
    distribusi rata-rata sampelnya tidak akan pernah konvergen menjadi bentuk lonceng (**Normal**). Ia tetap akan 
    meghasilkan nilai-nilai ekstrem secara acak.
    """)
else:
    st.write(f"""
    Perhatikan Grafik sebelah kanan. Walaupun Anda memilihdistribusi **{dist_type}** yang bentuk aslinya 
    miring atau asimetris, rata-ratanya akan membentuk pola 'lonceng' atau Distribusi Normal ketika menarik sampel berulang kali.
    Garis hitam pada grafik kanan menunjukkan betapa dekatnyahasil simulasi Anda dengan distribusi normal teoritis.

    Variasi ukuran sampel juga dimaksudkan untuk mengamati kecepatan konvergensi distribusi sampling terhadap normalitas sebagaimana dijelaskan dalam CLT.
    """)

# untuk menjalankan: stramlit run final_clt.py

