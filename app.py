import streamlit as st
import pandas as pd
from dbfread import DBF
from io import BytesIO
import tempfile

st.title("🔍 Wyszukiwarka DBF Online (170k+ rekordów)")

uploaded_file = st.file_uploader("Wgraj plik .dbf", type="dbf")

if uploaded_file is not None:
    # Zapisz tymczasowo plik
    with tempfile.NamedTemporaryFile(delete=False, suffix='.dbf') as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    
    try:
        # Odczytaj DBF
        st.info(f"Ładowanie pliku... ({uploaded_file.size / 1024 / 1024:.1f} MB)")
        table = DBF(tmp_path, encoding='cp852', load=True)
        df = pd.DataFrame(list(table))
        st.success(f"Załadowano {len(df):,} rekordów!")
        
        # Sidebar z opcjami
        st.sidebar.header("Filtrowanie")
        search_imie = st.sidebar.text_input("Imię", key="imie")
        search_nazwisko = st.sidebar.text_input("Nazwisko", key="nazwisko")
        search_pesel = st.sidebar.text_input("PESEL", key="pesel")
        
        # Filtruj
        filtered_df = df.copy()
        if search_imie:
            filtered_df = filtered_df[filtered_df['A'].astype(str).str.contains(search_imie, case=False, na=False)]
        if search_nazwisko:
            filtered_df = filtered_df[filtered_df['C'].astype(str).str.contains(search_nazwisko, case=False, na=False)]
        if search_pesel:
            filtered_df = filtered_df[filtered_df['D'].astype(str).str.contains(search_pesel, case=False, na=False)]
        
        # Paginacja
        page_size = st.sidebar.slider("Rekordów na stronę", 50, 2000, 500)
        total_pages = (len(filtered_df) + page_size - 1) // page_size
        page = st.sidebar.number_input("Strona", 1, total_pages, 1)
        start = (page - 1) * page_size
        end = start + page_size
        page_df = filtered_df.iloc[start:end]
        
        st.subheader(f"Wyniki: {len(filtered_df):,} / {len(df):,} (Strona {page}/{total_pages})")
        
        # Tabela interaktywna
        st.dataframe(
            page_df.rename(columns={
                'A': 'Imię', 'B': 'Miejscowość', 'C': 'Nazwisko', 'D': 'PESEL',
                'E': 'Ulica', 'F': 'Nr domu', 'G': 'Nr mieszkania'
            }),
            use_container_width=True,
            height=500
        )
        
        # Eksport
        csv = page_df.to_csv(index=False).encode('utf-8')
        st.download_button("Pobierz stronę CSV", csv, "wyniki.csv", "text/csv")
        
    except Exception as e:
        st.error(f"Błąd: {e}")
    finally:
        # Usuń temp plik
        import os
        os.unlink(tmp_path)
