import streamlit as st
import pandas as pd
import numpy as np
import pickle

# st.set_page_config(page_title = "Prediction")

# Load file
with open('model.pkl', 'rb') as file_1:
    model = pickle.load(file_1)

def run():
    
    # Judul
    st.title("E-Commerce Shipping Data")

    # Subheader
    st.subheader("Prediction")     

    # Body
    st.write('''Model yang digunakan untuk memprediksi adalah Random Forest (n_estimators = 400, max_depth = 45, min_samples_split = 3, min_samples_leaf = 2).''')

    # Buat form input
    with st.form("Data shipping"):
        id = st.text_input('ID', 'X')
        warehouse_block = st.selectbox('Warehouse Block', ('A', 'B', 'C', 'D', 'E', 'F'), index = 0)
        shipment_mode = st.selectbox('Mode of Shipment', ('Flight', 'Road', 'Ship'), index = 0)
        cust_care_calls = st.slider("Customer Care Calls", value = 2, min_value = 0, max_value = 7)
        cust_rating = st.slider("Customer Rating", value = 5, min_value = 1, max_value = 5)
        product_cost = st.number_input("Cost of Product", min_value = 0, max_value = 300, value = 100)
        purchase_prior = st.slider("Prior Purchases", value = 2, min_value = 0, max_value = 10)
        product_importance = st.selectbox('Product Importance', ('low', 'medium', 'high'), index = 2)
        gender = st.selectbox('Gender', ('M', 'F'), index = 0, help = 'M: Male, F: Female')
        discount = st.number_input("Discount", min_value = 0, max_value = 75, value = 10, help = 'Dalam %. Contoh: 30')
        weight = st.number_input("Weight of Product", min_value = 0, max_value = 8000, value = 2000, help = 'Dalam gram')
      
        # Submit
        submitted = st.form_submit_button('Delayed delivery?')

    # Buat data inferens sesuai input user yang sudah di-submit
    
    
    data_inf = {
        'id':id,
        'warehouse_block':warehouse_block,
        'shipment_mode':shipment_mode,
        'cust_care_calls':cust_care_calls,
        'cust_rating':cust_rating,
        'product_cost':product_cost,
        'purchase_prior':purchase_prior,
        'product_importance':product_importance,
        'gender':gender,
        'discount':discount,
        'weight':weight,
    }

    df_inf = pd.DataFrame([data_inf])
    df_inf_select = df_inf[['purchase_prior', 'discount', 'weight']]

    if submitted:
        # Memprediksi data inferens
        y_pred_inf = model.predict(df_inf_select)

        # Menampilkan hasil prediksi
        if y_pred_inf == 1:
            st.write('Order will not arrive on time.')
        else:
            st.write('Order will arrive on time.')
      
if __name__ == "__main__":
  run()