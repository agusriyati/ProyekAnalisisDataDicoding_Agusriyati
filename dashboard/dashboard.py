#!/usr/bin/env python
# coding: utf-8

# ## Import semua library yang diperlukan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# ## Fungsi untuk membersihkan data
def clean_data(bike_df, dataset_type):
    if bike_df is not None:
        # Ubah kolom 'dteday' ke tipe datetime untuk dataset harian
        if dataset_type == "day":
            bike_df["dteday"] = pd.to_datetime(bike_df["dteday"])
    return bike_df


# ## Fungsi untuk analisis data (EDA)
def analyze_data(bike_df, dataset_type):
    avg_casual = bike_df["casual"].mean()
    avg_registered = bike_df["registered"].mean()

    if dataset_type == "day":
        # Kelompokkan berdasarkan tahun dan bulan untuk penggunaan bulanan (hanya untuk dataset harian)
        monthly_usage = bike_df.groupby(["yr", "mnth"])["cnt"].mean().unstack()
        return avg_casual, avg_registered, monthly_usage
    else:
        return avg_casual, avg_registered, None


# ## Fungsi untuk visualisasi
def plot_user_comparison(avg_casual, avg_registered):
    categories = ["Kasual", "Terdaftar"]
    avg_counts = [avg_casual, avg_registered]

    plt.figure(figsize=(8, 5))
    sns.barplot(x=categories, y=avg_counts, palette="coolwarm")
    plt.xlabel("Jenis Pengguna")
    plt.ylabel("Rata-rata Jumlah Pengguna")
    plt.title("Rata-rata Pengguna Kasual vs Terdaftar")
    plt.grid(axis="y")
    st.pyplot(plt)
    plt.close()  # Tutup plot setelah dirender


def plot_monthly_usage(monthly_usage):
    plt.figure(figsize=(12, 6))
    monthly_usage.T.plot(kind="line", marker="o", color=sns.color_palette("Paired"))
    plt.title("Penggunaan Sepeda Sepanjang Tahun")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Pengguna")
    plt.xticks(range(1, 13))
    plt.legend(["Tahun 0", "Tahun 1"], title="Tahun")
    plt.grid(True)
    st.pyplot(plt)
    plt.close()  # Tutup plot setelah dirender


# ## Fungsi utama untuk menjalankan aplikasi
def main():
    st.title("Bike Sharing Analysis")

    # Tampilkan dataset mentah
    st.subheader("Dataset")

    # Pilih antara dataset harian dan per jam
    dataset_choice = st.selectbox(
        "Pilih Dataset", ["Harian (dashboard/day.csv)", "Per Jam (dashboard/hour.csv)"]
    )

    # Muat dataset langsung tanpa fungsi load_data
    if dataset_choice == "Harian (dashboard/day.csv)":
        dataset_type = "day"
        try:
            bike_df = pd.read_csv("dashboard/day.csv")
        except FileNotFoundError:
            st.error(
                "File 'day.csv' tidak ditemukan. Pastikan file ada di direktori yang benar."
            )
            return
    else:
        dataset_type = "hour"
        try:
            bike_df = pd.read_csv("dashboard/hour.csv")
        except FileNotFoundError:
            st.error(
                "File 'hour.csv' tidak ditemukan. Pastikan file ada di direktori yang benar."
            )
            return

    # Bersihkan data berdasarkan tipe dataset
    bike_df = clean_data(bike_df, dataset_type)

    st.write(f"Ini adalah dataset penyewaan sepeda {dataset_type}:")
    st.dataframe(bike_df)  # Tampilkan seluruh dataset tanpa .head()

    # Analisis data, simpan di session_state agar tidak dihitung ulang
    if "avg_casual" not in st.session_state:
        avg_casual, avg_registered, monthly_usage = analyze_data(bike_df, dataset_type)
        st.session_state["avg_casual"] = avg_casual
        st.session_state["avg_registered"] = avg_registered
        st.session_state["monthly_usage"] = monthly_usage
    else:
        avg_casual = st.session_state["avg_casual"]
        avg_registered = st.session_state["avg_registered"]
        monthly_usage = st.session_state["monthly_usage"]

    # Tampilkan rata-rata pengguna
    st.subheader("Rata-rata Pengguna")
    if st.button("Tampilkan Rata-rata Pengguna"):
        st.metric(label="Rata-rata Pengguna Kasual", value=f"{avg_casual:.2f}")
        st.metric(label="Rata-rata Pengguna Terdaftar", value=f"{avg_registered:.2f}")

    # Plot perbandingan pengguna
    if st.button("Tampilkan Perbandingan Pengguna"):
        st.subheader("Perbandingan Pengguna")
        plot_user_comparison(avg_casual, avg_registered)

    # Plot penggunaan bulanan (hanya untuk dataset harian)
    if dataset_type == "day" and monthly_usage is not None:
        if st.button("Tampilkan Pola Penggunaan Bulanan"):
            st.subheader("Pola Penggunaan Bulanan")
            plot_monthly_usage(monthly_usage)


# Jalankan aplikasi
if __name__ == "__main__":
    main()
