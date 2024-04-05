import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# st.set_page_config(page_title = "EDA")

def run():
    
    # Judul
    st.title("E-Commerce Shipping Data")
    
    # Subheader
    st.subheader("Exploratory Data Analysis (EDA)")
    
    # Data load, rename, type
    df = pd.read_csv('product_shipment.csv')
    df.rename(columns = {
        'ID':'id', 
        'Warehouse_block':'warehouse_block', 
        'Mode_of_Shipment':'shipment_mode', 
        'Customer_care_calls':'cust_care_calls', 
        'Customer_rating':'cust_rating', 
        'Cost_of_the_Product':'product_cost', 
        'Prior_purchases':'purchase_prior', 
        'Product_importance':'product_importance', 
        'Gender':'gender', 
        'Discount_offered':'discount', 
        'Weight_in_gms':'weight', 
        'Reached.on.Time_Y.N':'delay', 
    }, inplace = True)
    cat_nom_col = ['warehouse_block', 'shipment_mode', 'gender', 'delay']
    for cat in cat_nom_col:
        df[cat] = pd.Categorical(df[cat], ordered = False)
    df['cust_rating'] = pd.Categorical(df['cust_rating'], ordered = True)
    df['product_importance'] = pd.Categorical(df['product_importance'], ordered = True, categories = ['low', 'medium', 'high'])


    # EDA 1: Rating & delayed deliveries
    st.write("**Rating & Delayed Deliveries**")
    st.write('''Perusahaan paling banyak menerima rating 3.0, ingin dilihat lebih lanjut bagaimana porsinya dalam data. Ternyata, pemberian rating oleh pelanggan sangat merata, hampir sama semua persentasenya.
             Rating seperti ini tidak baik untuk perusahaan, karena selalu diinginkan pembeli yang puas dan bisa menilai experiencenya berbelanja serta produk yang dibeli dengan memuaskan. Setidaknya mayoritas pembeli harus bisa menilai 4.0 untuk experience belanja serta produk yang didapatkan, dan meminimalkan rating < 4.0. Jika ini berlangsung terus menerus, hampir pasti akan terjadi penurunan sales karena di masa sekarang, rating sebuah toko cukup menentukan apakah customer akan berbelanja di sana atau tidak (belajar dari pengalaman orang lain).
             Lebih jauh, tidak ada perbedaan signifikan antara pemberian rating untuk pesanan on-time dengan delayed. Maka, dapat disimpulkan delayed deliveries tidak memengaruhi bagaimana customer memberikan rating.''')
    fig = plt.figure(figsize = (12, 4))
    df[df['delay'] == 0]['cust_rating'].value_counts().plot(kind = 'pie', colormap = 'viridis', autopct = '%1.1f%%', ax = plt.subplot(1,2,1))
    plt.title('On-time')
    plt.ylabel('')
    df[df['delay'] == 1]['cust_rating'].value_counts().plot(kind = 'pie', colormap = 'viridis', autopct = '%1.1f%%', ax = plt.subplot(1,2,2))
    plt.title('Delayed')
    plt.ylabel('')
    plt.suptitle('Customer Rating')
    plt.tight_layout()
    plt.show()
    st.pyplot(fig)
    st.markdown("---")


    # EDA 2: Discounts
    st.write("**Discounts**")
    st.write('''Ada banyak cara diskon diberikan. Dua di antaranya adalah diskon langsung ke harga produk, dan diskon yang diberikan sebagai reward pada pelanggan.''') 
    st.write('''Pertama, di plot sebelah kiri adalah line plot antara harga produk dan rata-rata diskon untuk produk dengan harga yang sama. Terlihat ada penurunan diskon seiring naiknya harga produk. Hal lainnya yang ditunjukkan adalah barang yang lebih murah cenderung lebih bervariasi diskonnya. Dua hal ini wajar terjadi, karena penjual ingin menjaga agar harga produk (terutama yang di kelas tinggi, karena mungkin tidak banyak stoknya) tidak jatuh, atau bisa dibilang untuk menjaga harga pasaran.
             Kedua, plot sebelah kanan menunjukkan bagaimana dampak frekuensi pembelian terhadap diskon. Tidak ada perbedaan yang signifikan untuk rata-rata diskon yang diterima, namun ada pola yang menarik di mana mereka yang 2-3 kali berbelanja dan yang berbelanja 7 kali atau lebih, mendapat diskon lebih besar dari lainnya. Ada program berpola seperti ini, di mana penjual berusaha unutk attract pelanggan untuk join membership dengan cara memberikan diskons sebelumnya. Mungkin penjual menawarkan membership setelah melihat potensi customer menjadi pelanggan tetap. Sedangkan untuk mereka yang sudah jadi pelanggan tetap, semakin sering berbelanja bisa mengumpulkan poin atau entitled untuk memperoleh diskon yang lebih besar.''')
    fig_2 = plt.figure(figsize = (18, 5))
    df.groupby('product_cost')['discount'].mean().plot(kind = 'line', colormap = 'viridis', ax = plt.subplot(1,2,1))
    plt.title('Product Cost & Discount')
    plt.xlabel('Cost (USD)')
    plt.ylabel('Discount (%)')
    sns.barplot(data = df, x = 'purchase_prior', y = 'discount', palette = 'viridis', ax = plt.subplot(1,2,2))
    plt.title('# Prior Purchases & Discount')
    plt.ylabel('Discount (%)')
    plt.xlabel('# of purchases')
    plt.suptitle('Discount Offered')
    plt.tight_layout()
    plt.show()
    st.pyplot(fig_2)
    st.write('''Selanjutnya, plot di bawah ini menunjukkan transaksi untuk setiap tingkat diskon, dibedakan dengan apakah pesanan sampai terlambat atau tepat waktu.
             Untuk produk yang diskon < 20%, terlihat lebih banyak pengantaran tepat waktu dibandingkan dari yang delay. Yang menarik adalah saat diskon > 20%, di mana semua pengantaran behind schedule. 
             Fenomena ini ditemui juga sehari-hari, di mana ada tanggal-tanggal tertentu atau "tanggal cantik" saat banyak penjual memberikan diskon yang lebih besar secara bersamaan, dan akibatnya adalah lonjakan pesanan di berbagai platform e-commerce. Ini berimbas pada sistem pengantaran pesanan-pesanan tersebut, di mana jauh lebih banyak pesanan yang harus diantarkan dengan jumlah kurir kurang lebih sama di hari-hari lainnya. Oleh karena itu, jasa pengantaran seringkali kewalahan menghadapi order membludak dan konsekuensinya adalah pesanan terlambat sampai di rumah konsumen.''')
    fig_3 = plt.figure(figsize = (18, 4))
    option_fig_3 = st.selectbox("Discount distribution if delay: ", ("Yes", "No"))
    if option_fig_3 == "Yes":
        data_fig_3 = df[df['delay'] == 1]
    else:
        data_fig_3 = df[df['delay'] == 0]
    sns.histplot(data = data_fig_3, x = 'discount', bins = 30, palette = 'viridis', fill = False, ax = plt.subplot(1,2,1))
    plt.title('Histogram')
    plt.xlabel('Discount (%)')
    sns.kdeplot(data = data_fig_3, x = 'discount', palette = 'viridis', ax = plt.subplot(1,2,2))
    plt.title('KDE')
    plt.xlabel('Discount (%)')
    plt.suptitle('Discount & Delay')
    plt.tight_layout()
    plt.show()
    st.pyplot(fig_3)
    st.markdown("---")


    # EDA 3: Product costs & customer call
    st.write("**Product Costs & Customer Call**")
    st.write('''Didapati rata-rata pelanggan menghubungi customer care sebanyak 4 kali. Ingin dilihat bagaimana frekuensi telepon dipengaruhi oleh harga produk, dan apakah ada pola yang berbeda untuk barang yang terlambat dan yang tepat waktu.
             Jelas terlihat ada tren naik, di mana semakin tinggi harga produk, semakin sering juga pelanggan menghubungi customer care. Ada beberapa kemungkinan untuk ini terjadi:
             - Jika membeli produk dengan harga tinggi, customer lebih waswas atau kuatir akan proses pembeliannya, dari pembayaran ke barang sampai di rumah dengan baik-baik saja
             - Produk lebih mahal lebih sulit untuk dipahami penggunaannya, atau menuntut maintenance yang lebih rumit dan rutin
             - Customer ingin mendapatkan informasi karena biaya yang dikeluarkan tidak kecil, seperti informasi produk atau layanan after-sales yang diperoleh
             Menarik melihat bahwa hampir tidak ada perbedaan untuk garis transaksi on-time dan delay, yang berarti kecil kemungkinan customer call yang dilakukan adalah terkait delayed deliveries.''')
    option_fig_4 = st.selectbox("Product cost & customer calls if delay: ", ("Yes", "No"))
    if option_fig_4 == "Yes":
        data_fig_4 = df[df['delay'] == 1]
    else:
        data_fig_4 = df[df['delay'] == 0]
    fig_4 = plt.figure(figsize = (15, 3))
    sns.lineplot(data = data_fig_4, x = 'product_cost', y = 'cust_care_calls', ci = None, palette = 'viridis')
    plt.title('Product Cost & Customer Calls')
    plt.xlabel('Cost (USD)')
    plt.ylabel('Calls')
    plt.show()
    st.pyplot(fig_4)
    st.markdown("---")


    # EDA 4: Product importance
    st.write("**Product Importance**")
    st.write('''Perusahaan mengkategorikan produknya berdasarkan importance: low, medium, high. Tidak diketahui dasar dari pengkategorian ini, namun ingin dianalisa apakah produk yang high importance lebih diprioritaskan untuk sampai tepat waktu.
             Dari pie chart di bawah, ternyata itu tidak terjadi. Malahan persentase produk dengan predikat high importance lebih besar porsinya pada pie chart Delay, dibandingkan dengan pada pie chart On-time. Dapat disimpulkan bahwa customer yang memesan barang dengan tingkat importance lebih tinggi, tidak mendapat privilege berupa kepastian memperoleh pesanannya tepat waktu.
             Bisa digali kembali ke perusahaan, apa yang dimaksud dengan tingkat importance produk.''')
    fig_5 = plt.figure(figsize = (10, 4))
    df[df['delay'] == 0]['product_importance'].value_counts().plot(kind = 'pie', autopct='%1.1f%%', colormap = 'viridis', ax = plt.subplot(1,2,1))
    plt.title('On-time')
    plt.ylabel('')
    df[df['delay'] == 1]['product_importance'].value_counts().plot(kind = 'pie', autopct='%1.1f%%', colormap = 'viridis', ax = plt.subplot(1,2,2))
    plt.title('Delay')
    plt.ylabel('')
    plt.suptitle('Product Importance')
    plt.tight_layout()
    plt.show()
    st.pyplot(fig_5)
    st.markdown("---")


    # EDA 5: Product weight, shipment & warehouse
    st.write("**Product Weight, Shipment & Warehouse**")
    st.write('''Ada 3 faktor lain yang memengaruhi seberapa cepat pesanan sampai ke tujuan: berat produk, di mana produk disimpan, dan moda transportasi pengantaran. Ketiga hal ini berkaitan juga satu sama lain. 
             Produk yang berat membutuhkan usaha khusus untuk memindahkannya, dan terlihat bahwa pengantaran menggunakan moda transportasi Ship punya rentang berat produk yang lebih lebar. Dengan kata lain, produk yang berat diantar oleh Ship, dan yang ringan kebanyakan diantar dengan pesawat atau Flight. Masuk akal karena biaya transportasi dengan pesawat cukup mahal dengan kapasitas ruang yang tidak semasif kapal. 
             Terlihat juga bahwa untuk pesanan tepat waktu, berat produknya kurang lebih sama untuk setiap moda transportasi. Namun ini berbeda ketika melihat delayed deliveries, di mana produk cenderung lebih berat. 
             Di plot sebelah kanan, terlihat bahwa rata-rata berat produk yang disimpan di masing-masing warehouse kurang lebih sama, sehingga keterlambatan produk yang berat dapat disimpulkan disebabkan oleh moda pengantarannya, dan bukan dari lokasi warehouse.''')
    fig_6 = plt.figure(figsize = (15, 5))
    sns.boxplot(data = df, x = 'shipment_mode', y = 'weight', hue = 'delay', palette = 'viridis', fill = False, legend = 'brief',  ax = plt.subplot(1,2,1))
    plt.title('Weight')
    plt.ylabel('Weight (grams)')
    plt.xlabel('Mode of Shipment')
    plt.legend(title = 'Delay')
    df.groupby('warehouse_block')['weight'].mean().plot(kind = 'bar', colormap = 'viridis', ax = plt.subplot(1,2,2))
    plt.title('Warehouse Block')
    plt.ylabel('Weight (grams)')
    plt.xlabel('Warehouse Block')
    plt.xticks(rotation = 0)
    plt.suptitle('Mode of Shipment')
    plt.tight_layout()
    plt.show()
    st.pyplot(fig_6)
    st.write('''Lebih lanjut, di bawah ini bisa dilihat bahwa pesanan paling banyak diantar dari Warehouse Block F. Namun mengonfirmasi dugaan di atas, porsi delivery yang on-time dan delayed kurang lebih sama di masing-masing warehouse, sehingga lokasi warehouse bukan alasan mengapa pesanan terlambat sampai.
             Ditunjukkan juga moda shipment untuk setiap warehouse, yang porsinya kurang lebih sama di mana paling banyak shipment dilakukan dengan Ship. Melihat pengantaran dengan Ship biasanya untuk produk lebih berat dan ini terjadi di semua warehouse, menjadi masuk akal bagaimana setiap warehouse punya persentase keterlambatan pengantaran pesanan dari total pesanan masing-masing per warehouse.''')
    fig_7 = plt.figure(figsize = (15, 5))
    df.groupby('warehouse_block')['delay'].value_counts().unstack().plot(kind = 'bar', colormap = 'viridis', stacked = True, ax = plt.subplot(1,2,1))
    plt.title('Deliveries')
    plt.ylabel('# of Orders')
    plt.xlabel('Warehouse')
    plt.xticks(rotation = 0)
    plt.legend(title = 'Delay', labels = ['No', 'Yes'])
    df.groupby('warehouse_block')['shipment_mode'].value_counts().unstack().plot(kind = 'barh', colormap = 'viridis', stacked = True, ax = plt.subplot(1,2,2))
    plt.title('Shipment')
    plt.ylabel('Warehouse')
    plt.xlabel('# of Orders')
    plt.xticks(rotation = 0)
    plt.legend()
    plt.suptitle('Warehouse Block')
    plt.tight_layout()
    plt.show()
    st.pyplot(fig_7)
    st.markdown("---")


if __name__ == "__main__":
    run()