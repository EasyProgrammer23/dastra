import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker
import altair as alt
from streamlit_option_menu import option_menu


pdrb = pd.read_excel('PDRB.xlsx')
adhk_Lapus = pd.read_excel("ADHK_Lapus.xlsx")
adhb_Lapus = pd.read_excel("ADHB_Lapus.xlsx")
Kependudukan = pd.read_excel('Kependudukan.xlsx')
ketenagakerjaan = pd.read_excel("Ketenagakerjaan.xlsx")
kemiskinan = pd.read_excel("Kemiskinan.xlsx")
PManusia = pd.read_excel("PembangunanManusia.xlsx")

##with st.sidebar:
##    selected = option_menu(
##        menu_title = "Main Menu",
##        options =["PDRB", "Kependudukan", "Ketenagakerjaan", "Kemiskinan", "Pembangunan Manusia"],
##    )
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #212d0d;  /* hijau tua */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content
with st.sidebar:
    st.markdown("<h1 style='color: white;'>Data Strategis</h1>", unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["PDRB", "Kependudukan", "Ketenagakerjaan", "Kemiskinan", "Pembangunan Manusia"],
        icons=["person", "info-circle", "bar-chart", "people", "briefcase"],
        default_index=0,
        styles={
            "container": {
                "padding": "5!important",
                "background-color": "#212d0d",  # warna dalam container
                "border-radius": "10px"
            },
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "color": "white",
                "text-align": "left",
                "margin": "2px",
                "--hover-color": "#212d0d"
            },
            "nav-link-selected": {
                "background-color": "#3e4c1f",
                "color": "white",
                "font-weight": "bold"
            }
        }
    )

if selected == "PDRB":
    st.title(f"Anda Memasuki Data {selected}")
    st.write("## PDRB")
    st.write("Nilai keseluruhan semua barang dan jasa yang diproduksi dalam suatu wilayah  dalam suatu jangka waktu tertentu (biasanya satu tahun). PDRB terbagi menjadi dua  jenis, yaitu PDRB atas dasar harga berlaku (nominal) dan PDRB atas dasar harga  konstan (riil). PDRB atas dasar harga konstan digunakan untuk mengetahui  pertumbuhan ekonomi dari tahun ke tahun, sedangkan PDRB atas dasar harga berlaku  digunakan untuk menunjukkan kemampuan sumber daya ekonomi yang dihasilkan  suatu wilayah. ")
    # Pilihan kolom PDRB untuk divisualisasikan
    pdrb_option = st.selectbox("Pilih jenis PDRB untuk divisualisasikan:", ["PDRB ADHB", "PDRB ADHK"])

    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()

    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )

    # Filter data sesuai tahun
    filter_pdrb = pdrb[(pdrb["Tahun"] >= start_year) & (pdrb["Tahun"] <= end_year)]
    # Chart
    chart_pdrb = alt.Chart(filter_pdrb).mark_line(point=True).encode(
        x='Tahun:O',
        y=alt.Y(pdrb_option, title="PDRB", scale=alt.Scale(zero=False))
    ).properties(
        title=f"{pdrb_option} dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_pdrb, use_container_width=True)

    if pdrb_option == "PDRB ADHB":
       pdrb_lapus = adhb_Lapus
    else:
       pdrb_lapus = adhk_Lapus

    selected_year = st.selectbox("Pilih Tahun", pdrb_lapus['Tahun'])
    row = pdrb_lapus.loc[pdrb_lapus['Tahun'] == selected_year].iloc[0]
    sektor_data = {
        'Pertanian, Kehutanan, dan Perikanan': row['Pertanian, Kehutanan, dan Perikanan'],
        'Pertambangan dan Penggalian ': row['Pertambangan dan Penggalian '],
        'Industri Pengolahan': row['Industri Pengolahan'],
        'Pengadaan Listrik dan Gas': row['Pengadaan Listrik dan Gas'],
        'Pengadaan Air, Pengelolaan Sampah, Limbah dan Daur Ulang': row['Pengadaan Air, Pengelolaan Sampah, Limbah dan Daur Ulang'],
        'Konstruksi': row['Konstruksi'],
        'Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor': row['Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor'],
        'Transportasi dan Pergudangan ': row['Transportasi dan Pergudangan '],
        'Penyediaan Akomodasi dan Makan Minum': row['Penyediaan Akomodasi dan Makan Minum'],
        'Informasi dan Komunikasi': row['Informasi dan Komunikasi'],
        'Jasa Keuangan dan Asuransi': row['Jasa Keuangan dan Asuransi'],
        'Real Estate': row['Real Estate'],
        'Jasa perusahaan': row['Jasa perusahaan'],
        'Administrasi pemerintahan, pertahanan, dan Jaminan sosial wajib': row['Administrasi pemerintahan, pertahanan, dan Jaminan sosial wajib'],
        'Jasa Pendidikan': row['Jasa Pendidikan'],
        'Jasa Kesehatan dan Kegiatan Sosial': row['Jasa Kesehatan dan Kegiatan Sosial'],
        'Jasa Lainnya': row['Jasa Lainnya']
    }
    st.bar_chart(sektor_data) 
        
    st.subheader("Contoh Intepretasi")
    st.write("Misalnya pada tahun 2024 diketahui PDRB Kabupaten Sanggau sebesar 26.523.743.32 juta rupiah, artinya jumlah barang dan jasa yang dihasilkan di Kabupaten Sanggau pada tahun  2024 adalah 26.523.743.32 juta rupiah.")
    st.subheader("Sumber Data")
    st.write("Susenas; Dokumen Pemberitahuan Ekspor Barang (PEB) dan Pemberitahuan Impor Barang(PIB) yang diterima BPS dari kantor Bea Cukai; Data sayur- sayuran dan buah-buahandiperoleh dari Dinas Pertanian; data produksi tanaman perkebunan besar dari BPS, dataproduksi perkebunan rakyat dari Dinas Pertanian; Laporan Tahunan Pertambangan Energi,Departemen Energi dan Sumber Daya Mineral, Survei Tahunan Industri Besar Sedang,Laporan Tahunan Pertambangan Migas dan Pertamina; PN Gas, dan PDAM; LaporanKeuangan perusahaan, dll.")
    st.write("## PDRB Per Kapita")
    st.write("Merupakan nilai PDRB dibagi jumlah penduduk dalam suatu wilayah per periode  tertentu.")
    # Pilihan kolom PDRB untuk divisualisasikan
    pdrb_option2 = st.selectbox("Pilih jenis PDRB untuk divisualisasikan:", ["PDRB ADHB Per Kapita", "PDRB ADHK Per Kapita" ])

    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "pdrb_kapita"
    )

    # Filter data sesuai tahun
    filter_pdrb = pdrb[(pdrb["Tahun"] >= start_year) & (pdrb["Tahun"] <= end_year)]

    # Chart
    chart_pdrb = alt.Chart(filter_pdrb).mark_line(point=True).encode(
        x='Tahun:O',
        y=alt.Y(pdrb_option2, title="PDRB per Kapita", scale=alt.Scale(zero=False))
    ).properties(
        title=f"{pdrb_option2} dari {start_year} hingga {end_year}"
    )

    st.altair_chart(chart_pdrb, use_container_width=True)

    st.subheader("Contoh Intepretasi")
    st.write("Saat ini PDRB per kapita Kabupaten Sanggau sudah mencapai 51,96 juta rupiah. Nilai PDRB  per kapita tersebut dapat diartikan bahwa dalam setahun pendapatan tiap penduduk  Kabupaten Sanggau secara rata-rata sudah mencapai 51,96 juta.")
    st.subheader("Sumber Data")
    st.write("Susenas; Dokumen Pemberitahuan Ekspor Barang (PEB) dan Pemberitahuan Impor Barang(PIB) yang diterima BPS dari kantor Bea Cukai; Data sayur- sayuran dan buah-buahandiperoleh dari Dinas Pertanian; data produksi tanaman perkebunan besar dari BPS, dataproduksi perkebunan rakyat dari Dinas Pertanian; Laporan Tahunan Pertambangan Energi,Departemen Energi dan Sumber Daya Mineral, Survei Tahunan Industri Besar Sedang,Laporan Tahunan Pertambangan Migas dan Pertamina; PN Gas, dan PDAM; LaporanKeuangan perusahaan, dll.")
            
    st.write("## Laju Pertumbuhan PDRB")
    st.write("Menunjukkan pertumbuhan produksi barang dan jasa di suatu wilayah perekonomian dalam selang waktu tertentu. Penghitungan pertumbuhan ekonomi menggunakan PDRB atas dasar harga konstan dengan tahun dasar tertentu untuk mengeliminasi faktor kenaikan harga.")

    start_year, end_year, = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key="slider_laju"
    )

    # Filter data sesuai tahun
    filter_pdrb= pdrb[(pdrb["Tahun"] >= start_year) & (pdrb["Tahun"] <= end_year)]

    chart_pdrb= alt.Chart(filter_pdrb).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("Laju PDRB:Q", title="Laju PDRB", scale=alt.Scale(zero=False))
    ).properties(
        title=f"{pdrb_option} dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_pdrb, use_container_width=True)

    st.subheader("Contoh Intepretasi")
    st.write("Pertumbuhan ekonomi menunjukkan pertumbuhan produksi barang dan jasa di suatu wilayah perekonomian dalam selang waktu tertentu. Semakin tinggi pertumbuhan ekonomi suatu wilayah menandakan semakin bergairahnya perekonomian di wilayah tersebut. Dengan asumsi pertumbuhan ekonomi yang tinggi akan menyerap tenaga kerja yang tinggi pula, yang pada hakikatnya meningkatkan pendapatan dan daya beli masyarakat.")
    st.subheader("Sumber Data")
    st.write("Susenas; Dokumen Pemberitahuan Ekspor Barang (PEB) dan Pemberitahuan Impor Barang(PIB) yang diterima BPS dari kantor Bea Cukai; Data sayur- sayuran dan buah-buahandiperoleh dari Dinas Pertanian; data produksi tanaman perkebunan besar dari BPS, dataproduksi perkebunan rakyat dari Dinas Pertanian; Laporan Tahunan Pertambangan Energi,Departemen Energi dan Sumber Daya Mineral, Survei Tahunan Industri Besar Sedang,Laporan Tahunan Pertambangan Migas dan Pertamina; PN Gas, dan PDAM; LaporanKeuangan perusahaan, dll.")

    st.write("## Indeks Implisit PDRB")
    st.write("Suatu indeks yang menunjukkan tingkat perkembangan harga di tingkat produsen (producer price index).")

    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key="slider_imp"
    )

    # Filter data sesuai tahun
    filter_pdrb = pdrb[(pdrb["Tahun"] >= start_year) & (pdrb["Tahun"] <= end_year)]

    chart_pdrb= alt.Chart(filter_pdrb).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("Indeks Implisit:Q", title="Indeks Implisit", scale=alt.Scale(zero=False))
    ).properties(
        title=f"{pdrb_option} dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_pdrb, use_container_width=True)
    st.subheader("Contoh Intepretasi")
    st.write("Besarnya indeks implisit menunjukkan perubahan harga produsen sebesar (100 dikurangi besarnya indeks implisit) dibandingkan harga produsen pada tahun dasar (2010). Laju Indeks Implisit Kabupaten Sanggau pada tahun 2019 mencapai 2,03.")
    st.subheader("Sumber Data")
    st.write("Susenas; Dokumen Pemberitahuan Ekspor Barang (PEB) dan Pemberitahuan Impor Barang(PIB) yang diterima BPS dari kantor Bea Cukai; Data sayur- sayuran dan buah-buahandiperoleh dari Dinas Pertanian; data produksi tanaman perkebunan besar dari BPS, dataproduksi perkebunan rakyat dari Dinas Pertanian; Laporan Tahunan Pertambangan Energi,Departemen Energi dan Sumber Daya Mineral, Survei Tahunan Industri Besar Sedang,Laporan Tahunan Pertambangan Migas dan Pertamina; PN Gas, dan PDAM; LaporanKeuangan perusahaan, dll.")

if selected == "Kependudukan":
    st.title(f"Anda Memasuki Data {selected}")
    st.write("## Penduduk")
    st.write("Penduduk adalah semua orang yang berdomisili di wilayah yang bersangkutan selama 6 bulan atau lebih dan atau mereka yang berdomisili kurang dari 6 bulan tetapi bertujuan untuk menetap")
    # Pilihan kolom PDRB untuk divisualisasikan
    penduduk_option2 = st.selectbox("Pilih jumlah Penduduk yang ingin divisualisasikan:", ["Sanggau", "Toba", "Meliau", "Kapuas", "Mukok", "Jangkang", "Bonti", "Parindu", "Tayan Hilir", "Balai", "Tayan Hulu", "Kembayan", "Beduai", "Noyan", "Sekayam", "Entikong"],key="penduduk_select_1")

    min_year = Kependudukan["Tahun"].min()
    max_year = Kependudukan["Tahun"].max()

    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "jlh_pndk"
    )
 
    # Filter data sesuai tahun
    filter_penduduk = Kependudukan[(Kependudukan["Tahun"] >= start_year) & (Kependudukan["Tahun"] <= end_year)]

    # Checkbox pilihan jenis kelamin
    col1, col2, col3 = st.columns(3)
    with col1:
        show_total = st.checkbox("Total", value=True)
    with col2:
        show_lk = st.checkbox("Laki-laki", value=True)
    with col3:
        show_pr = st.checkbox("Perempuan", value=True)

    # Siapkan data untuk visualisasi
    data_dict = {"Tahun": filter_penduduk["Tahun"]}
    if show_total:
        data_dict["Total"] = filter_penduduk[penduduk_option2]
    if show_lk:
        data_dict["Laki-laki"] = filter_penduduk.get(f"{penduduk_option2} LK", pd.Series([None]*len(filter_penduduk)))
    if show_pr:
        data_dict["Perempuan"] = filter_penduduk.get(f"{penduduk_option2} PR", pd.Series([None]*len(filter_penduduk)))

    # Hanya lanjut jika ada yang dicentang
    if len(data_dict) > 1:
        df_vis = pd.DataFrame(data_dict)
        df_melt = df_vis.melt(id_vars="Tahun", var_name="Kategori", value_name="Jumlah")

        # Visualisasi
        chart = alt.Chart(df_melt).mark_line(point=True).encode(
            x=alt.X("Tahun:O", title="Tahun"),
            y=alt.Y("Jumlah:Q", title="Jumlah Penduduk", scale=alt.Scale(zero=False)),
            color=alt.Color("Kategori:N", title="Kategori")
        ).properties(
            title=f"Jumlah Penduduk {penduduk_option2} berdasarkan Jenis Kelamin ({start_year}–{end_year})"
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Pilih minimal satu kategori untuk ditampilkan.")
        
    st.subheader("Contoh Intepretasi")
    st.write("Semakin tinggi jumlah penduduk maka semakin banyak penduduk yang mendiami suatu wilayah.")
    st.subheader("Sumber Data")
    st.write("Sensus Penduduk, Survei Penduduk Antar Sensus (SUPAS), dan Perhitungan Proyeksi Penduduk.")
    
    st.write("## Kepadatan Penduduk")
    st.write("Kepadatan penduduk kasar merupakan ukuran kepadatan penduduk yang umum digunakan, karena data dan perhitungannya sederhana, juga ukuran ini sudah distandardisasi dengan luas wilayah. Kepadatan penduduk kasar (Crude population density), yaitu menunjukkan banyaknya jumlah penduduk untuk setiap kilometer persegi luas wilayah.")
    # Pilihan kolom PDRB untuk divisualisasikan
    penduduk_option2 = st.selectbox("Pilih jumlah Penduduk yang ingin divisualisasikan:", ["Sanggau", "Toba", "Meliau", "Kapuas", "Mukok", "Jangkang", "Bonti", "Parindu", "Tayan Hilir", "Balai", "Tayan Hulu", "Kembayan", "Beduai", "Noyan", "Sekayam", "Entikong"],key="penduduk_select_2")


    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "kepadatan_pndk"
    )

    # Filter data sesuai tahun
    filter_penduduk = Kependudukan[(Kependudukan["Tahun"] >= start_year) & (Kependudukan["Tahun"] <= end_year)]

    # Chart
    chart_kepadatan = alt.Chart(filter_penduduk ).mark_line(point=True).encode(
        x='Tahun:O',
        y=alt.Y(penduduk_option2 + " Kepadatan", title="Kepadatan Penduduk", scale=alt.Scale(zero=False))
    ).properties(
        title=f"{penduduk_option2} dari {start_year} hingga {end_year}"
    )

    st.altair_chart(chart_kepadatan , use_container_width=True)

    st.subheader("Contoh Intepretasi")
    st.write("Angka kepadatan penduduk menunjukkan rata-rata jumlah penduduk tiap 1 kilo meter  persegi. Semakin besar angka kepadatan penduduk menunjukkan bahwa semakin padat  penduduk yang mendiami wilayah tersebut. Misalnya kepadatan penduduk Kabupaten  Sanggau tahun 2024 sebesar 44, hal tersebut dapat diinterpretasikan bahwa secara rata-rata  terdapat 44 penduduk setiap 1 kilometer persegi.")
    st.subheader("Sumber Data")
    st.write("Sensus Penduduk, Survei Penduduk Antar Sensus (SUPAS), dan Perhitungan Proyeksi Penduduk.")
            
    st.write("## Laju Pertumbuhan Penduduk")
    st.write("Angka yang menunjukkan tingkat pertumbuhan penduduk per tahun dalam jangka waktu tertentu. Angka ini dinyatakan sebagai persentase dari penduduk dasar. Laju pertumbuhan penduduk dapat dihitung menggunakan tiga metode, yaitu aritmatik, geometrik, dan eksponensial. Metode yang digunakan di BPS adalah metode geometrik.")
    # Pilihan kolom PDRB untuk divisualisasikan
    penduduk_option2 = st.selectbox("Pilih jumlah Penduduk yang ingin divisualisasikan:", ["Sanggau", "Toba", "Meliau", "Kapuas", "Mukok", "Jangkang", "Bonti", "Parindu", "Tayan Hilir", "Balai", "Tayan Hulu", "Kembayan", "Beduai", "Noyan", "Sekayam", "Entikong"],key="penduduk_select_3")


    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "laju_pndk"
    )

    # Filter data sesuai tahun
    filter_penduduk = Kependudukan[(Kependudukan["Tahun"] >= start_year) & (Kependudukan["Tahun"] <= end_year)]

    # Chart
    chart_laju= alt.Chart(filter_penduduk ).mark_line(point=True).encode(
        x='Tahun:O',
        y=alt.Y(penduduk_option2 + " LPP", title="Laju Pertumbuhan", scale=alt.Scale(zero=False))
    ).properties(
        title=f"{penduduk_option2} dari {start_year} hingga {end_year}"
    )

    st.altair_chart(chart_laju , use_container_width=True)

    st.subheader("Contoh Intepretasi")
    st.write("a.r > 0, artinya terjadi penambahan jumlah penduduk pada tahun t dibandingkan tahun awal sebanyak r persen.")
    st.write(" b. r = 0, artinya tidak terjadi perubahan jumlah penduduk pada tahun t dibandingkan tahun awal.")
    st.write("c. r < 0, artinya terjadi pengurangan jumlah penduduk pada tahun t dibandingkan dengan tahun awal sebanyak mutlak r persen.")
    st.subheader("Sumber Data")
    st.write("Sensus Penduduk & Survei Penduduk Antar Sensus (SUPAS) ")
    
    st.write("## Rasio Jenis Kelamin")
    st.write("Rasio jenis kelamin adalah perbandingan antara jumlah penduduk laki-laki dan jumlah penduduk perempuan pada suatu daerah dan pada waktu tertentu, yang biasanya dinyatakan dalam banyaknya penduduk laki-laki per 100 penduduk perempuan.")
    # Pilihan kolom PDRB untuk divisualisasikan
    penduduk_option2 = st.selectbox("Pilih jumlah Penduduk yang ingin divisualisasikan:", ["Sanggau", "Toba", "Meliau", "Kapuas", "Mukok", "Jangkang", "Bonti", "Parindu", "Tayan Hilir", "Balai", "Tayan Hulu", "Kembayan", "Beduai", "Noyan", "Sekayam", "Entikong"],key="penduduk_select_4")


    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "rjk_pndk"
    )
    # Filter data sesuai tahun
    filter_penduduk = Kependudukan[(Kependudukan["Tahun"] >= start_year) & (Kependudukan["Tahun"] <= end_year)]

    # Chart
    chart_Rasiojk= alt.Chart(filter_penduduk ).mark_line(point=True).encode(
        x='Tahun:O',
        y=alt.Y(penduduk_option2 + " RJK", title="Rasio", scale=alt.Scale(zero=False))
    ).properties(
        title=f"{penduduk_option2} dari {start_year} hingga {end_year}"
    )

    st.altair_chart(chart_Rasiojk , use_container_width=True)

    st.subheader("Contoh Intepretasi")
    st.write("a. 𝑆𝑅 > 0, artinya jumlah penduduk laki-laki lebih banyak dibandingkan jumlah penduduk perempuan sebanyak SR kali penduduk perempuan.")
    st.write(" b. 𝑆𝑅 = 0, artinya jumlah penduduk laki-laki sama dengan jumlah penduduk perempuan. ")
    st.write("c. 𝑆𝑅 < 0, artinya jumlah penduduk perempuan lebih banyak dibandingkan jumlah penduduk laki-laki sebanyak (1-SR) kali penduduk perempuan.")
    st.subheader("Sumber Data")
    st.write("Sensus Penduduk & Survei Penduduk Antar Sensus (SUPAS)")

if selected == "Ketenagakerjaan":
    st.title(f"Anda Memasuki Data {selected}")
    st.write("## Angkatan Kerja")
    st.write("Angkatan Kerja adalah penduduk usia kerja (15 tahun ke atas) yang bekerja, atau punya pekerjaan namun sementara tidak bekerja, dan pengangguran. Sebaliknya, Bukan Angkatan Kerja adalah penduduk usia kerja (15 tahun ke atas) yang tidak bekerja karena bersekolah, mengurus rumah tangga, dan/atau melakukan kegiatan lainnya.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "angkt_kerja"
    )
    # Filter data sesuai tahun
    filter_kerja = ketenagakerjaan[(ketenagakerjaan["Tahun"] >= start_year) & (ketenagakerjaan["Tahun"] <= end_year)]

        # Checkbox pilihan jenis kelamin
    col1, col2, col3 = st.columns(3)
    with col1:
        show_total = st.checkbox("Total", value=True)
    with col2:
        show_lk = st.checkbox("Laki-laki", value=True)
    with col3:
        show_pr = st.checkbox("Perempuan", value=True)
    # Siapkan data untuk visualisasi
    data_dict = {"Tahun": filter_kerja["Tahun"]}
    if show_total:
        data_dict["Total"] = filter_kerja["Angkatan Kerja"]
    if show_lk:
        data_dict["Laki-laki"] = filter_kerja.get(f"Angkatan Kerja LK", pd.Series([None]*len(filter_kerja)))
    if show_pr:
        data_dict["Perempuan"] = filter_kerja.get(f"Angkatan Kerja PR", pd.Series([None]*len(filter_kerja)))

    # Hanya lanjut jika ada yang dicentang
    if len(data_dict) > 1:
        df_vis = pd.DataFrame(data_dict)
        df_melt = df_vis.melt(id_vars="Tahun", var_name="Kategori", value_name="Jumlah")

        # Visualisasi
        chart = alt.Chart(df_melt).mark_line(point=True).encode(
            x=alt.X("Tahun:O", title="Tahun"),
            y=alt.Y("Jumlah:Q", title="Jumlah", scale=alt.Scale(zero=False)),
            color=alt.Color("Kategori:N", title="Kategori")
        ).properties(
            title=f"Jumlah Angkatan Kerja berdasarkan Jenis Kelamin ({start_year}–{end_year})"
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Pilih minimal satu kategori untuk ditampilkan.")

    st.subheader("Contoh Intepretasi")
    st.write("Semakin tinggi jumlah angkatan kerja berarti semakin banyak jumlah penduduk yang berpotensi untuk bekerja.")
    st.subheader("Sumber Data")
    st.write("Survei Angkatan Kerja Nasional (SAKERNAS), Survei Sosial Ekonomi Nasional (SUSENAS), SUPAS, dan Sensus Penduduk.")

    st.write("## Tingkat Partisipasi Angkatan Kerja")
    st.write("ersentase angkatan kerja terhadap penduduk usia kerja.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "tpak"
    )

    # Filter data sesuai tahun
    filter_kerja = ketenagakerjaan[(ketenagakerjaan["Tahun"] >= start_year) & (ketenagakerjaan["Tahun"] <= end_year)]

        # Checkbox pilihan jenis kelamin
    col1, col2, col3 = st.columns(3)
    with col1:
        show_total = st.checkbox("Total", value=True, key="total_checkbox_3")
    with col2:
        show_lk = st.checkbox("Laki-laki", value=True, key="lk_checkbox_3")
    with col3:
        show_pr = st.checkbox("Perempuan", value=True, key="pr_checkbox_3")
    # Siapkan data untuk visualisasi
    data_dict = {"Tahun": filter_kerja["Tahun"]}
    if show_total:
        data_dict["Total"] = filter_kerja["TPAK"]
    if show_lk:
        data_dict["Laki-laki"] = filter_kerja.get(f"TPAK LK", pd.Series([None]*len(filter_kerja)))
    if show_pr:
        data_dict["Perempuan"] = filter_kerja.get(f"TPAK PR", pd.Series([None]*len(filter_kerja)))

    # Hanya lanjut jika ada yang dicentang
    if len(data_dict) > 1:
        df_vis = pd.DataFrame(data_dict)
        df_melt = df_vis.melt(id_vars="Tahun", var_name="Kategori", value_name="Jumlah")

        # Visualisasi
        chart = alt.Chart(df_melt).mark_line(point=True).encode(
            x=alt.X("Tahun:O", title="Tahun"),
            y=alt.Y("Jumlah:Q", title="Jumlah", scale=alt.Scale(zero=False)),
            color=alt.Color("Kategori:N", title="Kategori")
        ).properties(
            title=f"Jumlah TPAK berdasarkan Jenis Kelamin ({start_year}–{end_year})"
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Pilih minimal satu kategori untuk ditampilkan.")
        
    st.subheader("Contoh Intepretasi")
    st.write("Semakin tinggi TPAK menunjukkan bahwa semakin tinggi pula pasokan tenaga kerja (labor supply ) yang tersedia untuk memproduksi barang dan jasa dalam suatu perekonomian. Contoh: Jika TPAK sebesar 71.69 persen di Kab. Sanggau tahun 2024, maka dari 100 penduduk usia 15 tahun ke atas, terdapat sebanyak 71 hingga 72 orang tersedia untuk memproduksi pada periode tertentu di Kab. Sanggau tahun 2024.")
    st.subheader("Sumber Data")
    st.write("Survei Angkatan Kerja Nasional (SAKERNAS)")

    st.write("## Tingkat Pengangguran Terbuka")
    st.write("Persentase penduduk yang mencari pekerjaan, yang mempersiapkan usaha, yang tidak mencari pekerjaan karena merasa tidak mungkin pekerjaan, yang sudah mempunyai pekerjaan tetapi belum mulai bekerja dari sejumlah angkatan kerja yang ada.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "tpt"
    )

    # Filter data sesuai tahun
    filter_kerja = ketenagakerjaan[(ketenagakerjaan["Tahun"] >= start_year) & (ketenagakerjaan["Tahun"] <= end_year)]

        # Checkbox pilihan jenis kelamin
    col1, col2, col3 = st.columns(3)
    with col1:
        show_total = st.checkbox("Total", value=True, key="total_checkbox_1")
    with col2:
        show_lk = st.checkbox("Laki-laki", value=True, key="lk_checkbox_1")
    with col3:
        show_pr = st.checkbox("Perempuan", value=True, key="pr_checkbox_1")
    # Siapkan data untuk visualisasi
    data_dict = {"Tahun": filter_kerja["Tahun"]}
    if show_total:
        data_dict["Total"] = filter_kerja["TPT"]
    if show_lk:
        data_dict["Laki-laki"] = filter_kerja.get(f"TPT LK", pd.Series([None]*len(filter_kerja)))
    if show_pr:
        data_dict["Perempuan"] = filter_kerja.get(f"TPT PR", pd.Series([None]*len(filter_kerja)))

    # Hanya lanjut jika ada yang dicentang
    if len(data_dict) > 1:
        df_vis = pd.DataFrame(data_dict)
        df_melt = df_vis.melt(id_vars="Tahun", var_name="Kategori", value_name="Jumlah")

        # Visualisasi
        chart = alt.Chart(df_melt).mark_line(point=True).encode(
            x=alt.X("Tahun:O", title="Tahun"),
            y=alt.Y("Jumlah:Q", title="Jumlah", scale=alt.Scale(zero=False)),
            color=alt.Color("Kategori:N", title="Kategori")
        ).properties(
            title=f"Jumlah TPT berdasarkan Jenis Kelamin ({start_year}–{end_year})"
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Pilih minimal satu kategori untuk ditampilkan.")
        
    st.subheader("Contoh Intepretasi")
    st.write("TPT yang tinggi menunjukkan bahwa terdapat banyak angkatan kerja yang tidak diserap pada pasar kerja. Misal: TPT Sanggau pada tahun 2024 adalah 3.71, artinya dari 100 penduduk usia 15 tahun ke atas yang tersedia untuk memproduksi barang dan jasa (angkatan kerja) terdapat 3 hingga 4 orang merupakan pengangguran")
    st.subheader("Sumber Data")
    st.write("Survei Angkatan Kerja Nasional (SAKERNAS), Survei Sosial Ekonomi Nasional (SUSENAS), dan Sensus Penduduk.")

    st.write("## Tingkat Kesempatan Bekerja")
    st.write("Peluang seorang penduduk usia kerja yang termasuk angkatan kerja untuk bekerja. ")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "TKK"
    )

    # Filter data sesuai tahun
    filter_kerja = ketenagakerjaan[(ketenagakerjaan["Tahun"] >= start_year) & (ketenagakerjaan["Tahun"] <= end_year)]

            # Checkbox pilihan jenis kelamin
    col1, col2, col3 = st.columns(3)
    with col1:
        show_total = st.checkbox("Total", value=True, key="total_checkbox_2")
    with col2:
        show_lk = st.checkbox("Laki-laki", value=True, key="lk_checkbox_2")
    with col3:
        show_pr = st.checkbox("Perempuan", value=True, key="pr_checkbox_2")
    # Siapkan data untuk visualisasi
    data_dict = {"Tahun": filter_kerja["Tahun"]}
    if show_total:
        data_dict["Total"] = filter_kerja["TKK"]
    if show_lk:
        data_dict["Laki-laki"] = filter_kerja.get(f"TKK LK", pd.Series([None]*len(filter_kerja)))
    if show_pr:
        data_dict["Perempuan"] = filter_kerja.get(f"TKK PR", pd.Series([None]*len(filter_kerja)))

    # Hanya lanjut jika ada yang dicentang
    if len(data_dict) > 1:
        df_vis = pd.DataFrame(data_dict)
        df_melt = df_vis.melt(id_vars="Tahun", var_name="Kategori", value_name="Jumlah")

        # Visualisasi
        chart = alt.Chart(df_melt).mark_line(point=True).encode(
            x=alt.X("Tahun:O", title="Tahun"),
            y=alt.Y("Jumlah:Q", title="Jumlah", scale=alt.Scale(zero=False)),
            color=alt.Color("Kategori:N", title="Kategori")
        ).properties(
            title=f"Jumlah TKK berdasarkan Jenis Kelamin ({start_year}–{end_year})"
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Pilih minimal satu kategori untuk ditampilkan.")

    st.subheader("Contoh Intepretasi")
    st.write("Peluang seseorang yang termasuk dalam angkatan kerja untuk dapat terserap dalam pasar kerja atau dapat bekerja. Semakin besar RK, maka semakin baik pula kondisi ketenagakerjaan dalam suatu wilayah.")
    st.subheader("Sumber Data")
    st.write("Sakernas, Susenas, dan Sensus Penduduk ")

    st.write("## Rasio Ketergantungan")
    st.write("Rasio ketergantungan (depandency ratio) adalah perbandingan antara jumlah penduduk umur 0-14 tahun ditambah dengan penduduk umur 65 tahun ke atas (keduanya disebut sebagai bukan angkatan kerja) dibandingkan dengan jumlah penduduk umur 15-64 tahun (angkatan kerja).")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "tkk"
    )

    # Filter data sesuai tahun
    filter_kerja = ketenagakerjaan[(ketenagakerjaan["Tahun"] >= start_year) & (ketenagakerjaan["Tahun"] <= end_year)]
    chart_RK= alt.Chart(filter_kerja).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("RK:Q", title="Jumlah", scale=alt.Scale(zero=False))
    ).properties(
        title=f"RK dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_RK, use_container_width=True)
    st.subheader("Contoh Intepretasi")
    st.write("   Rasio ketergantungan merupakan salah satu indikator yang penting. Rasio ketergantungan menunjukkan tingginya beban yang harus ditanggung penduduk yang produktif untuk membiayai hidup penduduk yang belum produktif dan penduduk yang sudah tidak produktif lagi. Misalnya terdapat rasio ketergantungan sebesar 43 persen sanggau pada tahun 2024, artinya setiap 100 orang yang berusia produktif di sanggau pada tahun 2024 mempunyai tanggungan sebanyak 43 orang yang tidak produktif.")
    st.subheader("Sumber Data")
    st.write("SUPAS dan Sensus Penduduk ")

if selected == "Kemiskinan":
    st.title(f"Anda Memasuki Data {selected}")
    st.write("## Garis Kemiskinan")
    st.write("Garis kemiskinan merupakan representasi dari jumlah rupiah minimum yangdibutuhkan untuk memenuhi kebutuhan pokok minimum makanan yang setara dengan2100 kilokalori per kapita per hari dan kebutuhan pokok bukan makanan. Gariskemiskinan (GK) merupakan penjumlahan dari Garis Kemiskinan Makanan (GKM)dan Garis Kemiskinan non Makanan (GKNM). Garis kemiskinan makanan merupakannilai pengeluaran kebutuhan minimum makanan yang disetarakan dengan 2100kilokalori per kapita per hari. Paket komoditi kebutuhan dasar makanan diwakili oleh52 jenis komoditi (padi- padian, umbi-umbian, ikan, daging, telur dan susu, sayuran,kacang- kacangan, buah-buahan, minyak, dll.). Garis kemiskinan non makanan adalahkebutuhan minimum untuk perumahan, sandang, Pendidikan, dan Kesehatan. Paketkomoditi kebutuhan dasar non makanan diwakili oleh 51 jenis komoditi di perkotaandan 47 jenis di perdesaan.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "GK"
    )
    # Filter data sesuai tahun
    filter_kemiskinan = kemiskinan[(kemiskinan["Tahun"] >= start_year) & (kemiskinan["Tahun"] <= end_year)]
    chart_GK= alt.Chart(filter_kemiskinan).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("GK:Q", title="Persentase", scale=alt.Scale(zero=False))
    ).properties(
        title=f"Garis Kemiskinan dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_GK, use_container_width=True)
    st.subheader("Contoh Intepretasi")
    st.write("Garis kemiskinan menunjukkan jumlah rupiah minimum yang dibutuhkan untuk memenuhi kebutuhan pokok minimum makanan yang setara dengan 2100 kilokalori per kapita per hari dan kebutuhan pokok non makanan. Penduduk yang memiliki rata-rata pengeluaran konsumsi per kapita per bulan di bawah garis kemiskinan dikategorikan sebagai penduduk miskin.")
    st.subheader("Sumber Data")
    st.write("Susenas Modul Konsumsi dan Kor.")

    st.write("## Persentase Penduduk Miskin")
    st.write("Persentase penduduk miskin yang berada di bawah garis kemiskinan. Headcount index secara sederhana mengukur proporsi yang dikategorikan miskin.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "PPM"
    )
    # Filter data sesuai tahun
    filter_kemiskinan = kemiskinan[(kemiskinan["Tahun"] >= start_year) & (kemiskinan["Tahun"] <= end_year)]
    chart_GK= alt.Chart(filter_kemiskinan).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("PersentaseKemiskinan:Q", title="Persentase", scale=alt.Scale(zero=False))
    ).properties(
        title=f"Persentase Penduduk Miskin dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_GK, use_container_width=True)
    st.subheader("Contoh Intepretasi")
    st.write("Angka yang ditunjukkan oleh P0 menunjukkan proporsi penduduk miskin di suatu wilayah. Persentase penduduk miskin (P0) yang tinggi menunjukkan bahwa tingkat kemiskinan di suatu wilayah juga tinggi.")
    st.subheader("Sumber Data")
    st.write("Survei Sosial Ekonomi Nasional (SUSENAS)")

    st.write("## Indeks Kedalaman Kemiskinan")
    st.write("Indeks kedalaman kemiskinan (Poverty Gap Index – P1) merupakan ukuran rata rata kesenjangan pengeluaran masing-masing penduduk miskin terhadap garis kemiskinan.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "KedalamanKemiskinan"
    )
    # Filter data sesuai tahun
    filter_kemiskinan = kemiskinan[(kemiskinan["Tahun"] >= start_year) & (kemiskinan["Tahun"] <= end_year)]
    chart_GK= alt.Chart(filter_kemiskinan).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("KedalamanKemiskinan:Q", title="Nilai", scale=alt.Scale(zero=False))
    ).properties(
        title=f"Kedalaman Miskin dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_GK, use_container_width=True)
    st.subheader("Contoh Intepretasi")
    st.write("Penurunan nilai indeks kedalaman kemiskinan mengindikasikan bahwa rata- rata pengeluaran penduduk miskin cenderung semakin mendekati garis kemiskinan dan ketimpangan pengeluaran penduduk miskin juga semakin menyempit.")
    st.subheader("Sumber Data")
    st.write("Survei Sosial Ekonomi Nasional (SUSENAS)")

    st.write("## Indeks Keparahan Kemiskinan")
    st.write("Indeks keparahan kemiskinan (Poverty Severity Index – P1) memberikan gambaran mengenai penyebaran pengeluaran di antara penduduk miskin.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "KeparahanKemiskinan"
    )
    # Filter data sesuai tahun
    filter_kemiskinan = kemiskinan[(kemiskinan["Tahun"] >= start_year) & (kemiskinan["Tahun"] <= end_year)]
    chart_GK= alt.Chart(filter_kemiskinan).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("KeparahanKemiskinan:Q", title="Nilai", scale=alt.Scale(zero=False))
    ).properties(
        title=f"Keparahan Miskin dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_GK, use_container_width=True)
    st.subheader("Contoh Intepretasi")
    st.write("Semakin tinggi nilai indeks, semakin tinggi ketimpangan pengeluaran di antara penduduk miskin.")
    st.subheader("Sumber Data")
    st.write("Survei Sosial Ekonomi Nasional (SUSENAS)")

if selected == "Pembangunan Manusia":
    st.title(f"Anda Memasuki Data {selected}")
    st.write("## Angka Harapan Hidup")
    st.write("Rata-rata tahun hidup yang masih akan dijalani oleh seseorang yang telah berhasil mencapai umur x, pada suatu tahun tertentu dalam situasi mortalitas yang berlaku di lingkungan masyarakat. Penggunaan AHH didasarkan atas pertimbangan bahwa angka ini merupakan hasil dari berbagai indikator kesehatan. AHH merupakan cerminan dari ketersediaan sarana dan prasarana kesehatan, sanitasi lingkungan, pengetahuan ibu tentang kesehatan, gaya hidup masyarakat, pemenuhan gizi ibu dan bayi, dan lain- lain.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "AHH"
    )
    # Filter data sesuai tahun
    filter_pembangunan = PManusia[(PManusia["Tahun"] >= start_year) & (PManusia["Tahun"] <= end_year)]
    chart_AHH= alt.Chart(filter_pembangunan).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("AHH:Q", title="Tahun", scale=alt.Scale(zero=False)),
        tooltip=["Tahun:O", "AHH:Q"] 
    ).properties(
        title=f"Angka Harapan Hidup dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_AHH, use_container_width=True)
    st.subheader("Contoh Intepretasi")
    st.write("Angka harapan hidup menggambarkan rata-rata tahun hidup yang dijalani oleh seseorang. Misalnya angka harapan hidup Indonesia yang terhitung untuk Indonesia dari Sensus Penduduk tahun 1971 adalah 47,7 tahun, artinya bayi-bayi yang dilahirkan menjelang tahun 1971 akan dapat hidup sampai 47 sampai 48 tahun.")
    st.subheader("Sumber Data")
    st.write("Sensus Penduduk, Registrasi Penduduk, Survei Penduduk Antar Sensus (SUPAS), Survei Sosial Ekonomi Nasional (Susenas).")

    st.write("## Rata-rata Lama Sekolah")
    st.write("Rata-rata lama sekolah (Mean Years School/MYS) adalah jumlah tahun yang digunakan oleh penduduk dalam menjalani pendudukan formal. Diasumsikan bahwa dalam kondisi normal rata-rata lama sekolah suatu wilayah tidak akan turun. Cakupan penduduk yang dihitung dalam penghitungan rata-rata lama sekolah adalah penduduk berusia 25 tahun ke atas.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "RLS"
    )
    # Filter data sesuai tahun
    filter_pembangunan = PManusia[(PManusia["Tahun"] >= start_year) & (PManusia["Tahun"] <= end_year)]
    chart_RLS= alt.Chart(filter_pembangunan).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("RLS:Q", title="Tahun", scale=alt.Scale(zero=False)),
        tooltip=["Tahun:O", "RLS:Q"] 
    ).properties(
        title=f"Rata-rata lama sekolah dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_RLS, use_container_width=True)
    st.subheader("Contoh Intepretasi")
    st.write("Tingginya angka Rata-rata lama sekolah menunjukkan jenjang Pendidikan yang pernah/sedang diduduki oleh seseorang. Semakin tinggi angka RLS maka semakin lama/tinggi jenjang Pendidikan yang ditamatkannya.")
    st.subheader("Sumber Data")
    st.write("Sensus Penduduk, Survei Penduduk Antar Sensus (SUPAS), Survei Sosial Ekonomi Nasional (SUSENAS).")

    st.write("## Harapan Lama Sekolah")
    st.write("Angka Harapan Lama Sekolah (HLS) dihitung pada penduduk berusia 7 tahun ke atas. HLS dihitung pada usia 7 tahun ke atas karena mengikuti kebijakan pemerintah yaitu program wajib belajar. Diasumsikan bahwa peluang anak tersebut akan tetap bersekolah pada umur-umur berikutnya sama dengan peluang penduduk yang bersekolah per jumlah penduduk untuk umur yang sama saat ini.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "HLS"
    )
    # Filter data sesuai tahun
    filter_pembangunan = PManusia[(PManusia["Tahun"] >= start_year) & (PManusia["Tahun"] <= end_year)]
    chart_HLS= alt.Chart(filter_pembangunan).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("HLS:Q", title="Tahun", scale=alt.Scale(zero=False)),
        tooltip=["Tahun:O", "HLS:Q"] 
    ).properties(
        title=f"Harapan lama sekolah dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_HLS, use_container_width=True)
    st.subheader("Contoh Intepretasi")
    st.write("Tingginya angka harapan lama sekolah (HLS) menunjukkan lamanya sekolah yang diharapkan oleh anak pada umur tertentu di masa mendatang. Semakin tinggi angka HLS maka semakin lama/tinggi jenjang Pendidikan yang diharapkan akan ditamatkannya.")
    st.subheader("Sumber Data")
    st.write("Sensus Penduduk, Survei Penduduk Antar Sensus (SUPAS), Survei Sosial Ekonomi Nasional (SUSENAS), Direktorat Pendidikan Islam Kemenag.")
   
    st.write("## Rata-rata Pengeluaran Per Kapita yang Disesuaikan")
    st.write("Rata-rata pengeluaran per kapita yang disesuaikan (Purchasing Power Parity/PPP) atau daya beli adalah kemampuan masyarakat dalam membelanjakan uangnya dalam bentuk barang maupun jasa. Penghitungan paritas daya beli menggunakan 96komoditas dimana 66 komoditas merupakan makanan dan 30 komoditas merupakan komoditas non makanan.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "RPP"
    )
    # Filter data sesuai tahun
    filter_pembangunan = PManusia[(PManusia["Tahun"] >= start_year) & (PManusia["Tahun"] <= end_year)]
    chart_RPP= alt.Chart(filter_pembangunan).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("RatarataPengeluaran:Q", title="juta Rp/Thn", scale=alt.Scale(zero=False)),
        tooltip=["Tahun:O", "RatarataPengeluaran:Q"] 
    ).properties(
        title=f"Rata-rata pengeluaran per kapita yang disesuaikan dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_RPP, use_container_width=True)
    st.subheader("Contoh Intepretasi")
    st.write("Kemampuan daya beli antar daerah berbeda-beda. Semakin rendahnya nilai daya beli suatu masyarakat berkaitan erat dengan kondisi perekonomian pada saat itu yang sedang memburuk yang berarti semakin rendah kemampuan masyarakat untuk membeli suatu barang atau jasa.")
    st.subheader("Sumber Data")
    st.write("Survei Sosial Ekonomi Nasional (SUSENAS)")

    st.write("## Indeks Pembangunan Manusia ")
    st.write("IPM adalah indeks yang mengukur pembangunan manusia dari tiga aspek dasar yaitu umur Panjang dan hidup sehat; pengetahuan/Pendidikan; dan standar hidup layak. Ketiga aspek tersebut memiliki pengertian yang sangat luas karena merupakan gabungan dari berbagai faktor. Untuk mengukur dimensi Kesehatan, digunakan angka harapan hidup waktu lahir. Selanjutnya untuk mengukur dimensi Pendidikan digunakan gabungan indikator rata-rata lama sekolah dan angka harapan lama sekolah. Adapun untuk mengukur dimensi hidup layak digunakan indikator kemampuan daya beli masyarakat terhadap sejumlah kebutuhan pokok yang dilihat dari rata-rata besarnya pengeluaran per kapita.")
    # Pilihan kolom PDRB untuk divisualisasikan
    min_year = pdrb["Tahun"].min()
    max_year = pdrb["Tahun"].max()
    start_year, end_year = st.slider(
        "Pilih rentang tahun:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key = "IPM"
    )
    # Filter data sesuai tahun
    filter_pembangunan = PManusia[(PManusia["Tahun"] >= start_year) & (PManusia["Tahun"] <= end_year)]
    chart_IPM= alt.Chart(filter_pembangunan).mark_line(point=True).encode(
        x= alt.X("Tahun:O", title="Tahun"),
        y= alt.Y("IPM:Q", title="Poin", scale=alt.Scale(zero=False)),
        tooltip=["Tahun:O", "IPM:Q"] 
    ).properties(
        title=f"Indeks Pembangunan Manusia dari {start_year} hingga {end_year}"
    )
    st.altair_chart(chart_IPM, use_container_width=True)
    st.subheader("Contoh Intepretasi")
    st.write("Angka IPM memberikan gambaran komprehensif mengenai tingkat pencapaian pembangunan manusia sebagai dampak dari kegiatan pembangunan yang dilakukan oleh suatu negara/daerah. Semakin tinggi nilai IPM suatu negara/daerah, menunjukkan pencapaian pembangunan manusianya semakin baik.")
    st.subheader("Sumber Data")
    st.write("Survei Sosial Ekonomi Nasional (SUSENAS) dan Survei Angkatan Kerja Nasional (SAKERNAS) ")