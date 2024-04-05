import streamlit as st
import pandas as pd
from PIL import Image

# st.set_page_config(page_title = "Home")

def run():
    
    # Judul
    st.title("E-Commerce Shipping Data")
    
    # Subheader
    st.subheader("Home")
    
    # Intro
    st.write("**Milestones 2**")
    st.write('''Nama: Wilona Natalie Elvaretta  
    Batch: RMT-028''')
    st.markdown("---")

    # Problem statement
    st.write("**Problem**")
    image = Image.open('image_home.jpg')
    st.image(image)
    st.write('''Di jaman digital seperti sekarang ini, semakin banyak orang  yang berbelanja online. Kemudahan, kecepatan dan akses yang ditawarkan memang berbeda dengan berbelanja secara konvensional. Contohnya, pembeli tidak harus mengeluarkan tenaga atau usaha untuk mengunjungi toko tertentu, dan mereka bisa menunggu kiriman belanja datang ke rumah. 
             Keunikan berbelanja online datang dengan aspek-aspek baru yang harus diperhatikan, dan salah satu yang paling penting adalah ketepatan waktu sampainya pesanan. Hal ini menjadi krusial karena berbeda dengan belanja konvensional, pembeli harus menunggu untuk bisa memakai atau menggunakan barang tersebut.''')
    st.markdown('''Oleh karena itu, program ini ingin memprediksi apakah barang akan sampai tepat waktu atau tidak berdasarkan beberapa data dari database pembeli sebuah perusahaan yang bergerak di usaha elektronik. Model untuk memprediksi akan dipilih dari 5 jenis algoritma klasifikasi: K-Nearest Neighbors (KNN), Support Vector Machine (SVM), Decision Tree, Random Forest, dan Ada Boosting.  
             Pemilihan model terbaik dilakukan dengan cross-validation, dan dioptimalkan menggunakan hyperparameter tuning. Metric yang digunakan adalah recall, karena kita ingin fokus meminimalisir False Negative, yaitu barang yang tidak sampai tepat waktu tetapi diprediksi sampai tepat waktu.
             Program ini diharapkan selesai tanggal 7 Maret 2024.''')
    st.markdown("---")
    
    # Dataset
    st.write("**Dataset**")
    st.write("Dataset berasal dari sebuah perusahan elektronik dan dapat diakses [di sini](https://www.kaggle.com/datasets/prachi13/customer-analytics).")
    st.write("Ada 10999 observasi dengan 12 atribut seperti terlihat di bawah, dengan schema data pada gambar di bawahnya:")
    df = pd.read_csv('product_shipment.csv')
    st.dataframe(df)
    image_2 = Image.open('schema.png')
    st.image(image_2)

if __name__ == "__main__":
  run()