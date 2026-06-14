import pandas as pd
import json

def generate_dashboard():
    # Load langsung dari file Excel
    file = 'Rencana Infrastruktur Persampahan 2030.xlsx'
    
    # Baca dua sheet utama
    df_k = pd.read_excel(file, sheet_name='Kebutuhan_Sarana_prasarana')
    df_t = pd.read_excel(file, sheet_name='Sarana_prasarana_tersedia')
    
    # Merge data berdasarkan Kode_Desa
    df = pd.merge(df_k, df_t, on=['Kode_Desa', 'Kecamatan', 'Desa_Kelurahan'], how='left').fillna(0)
    
    # Kalkulasi Gap & Biaya (Asumsi harga per unit)
    df['gap_tps'] = df['Kebutuhan_TPS_6m3_(unit)'] - df['Jumlah_TPS_Tersedia']
    df['gap_tps'] = df['gap_tps'].clip(lower=0)
    df['estimasi_biaya'] = df['gap_tps'] * 200_000_000
    
    # Agregasi untuk chart
    chart_data = df.groupby('Kecamatan')[['gap_tps', 'estimasi_biaya']].sum().reset_index()
    
    # Generate JSON
    # Generate JSON dengan tambahan table_data agar tabel muncul!
    payload = {
        "summary": {
            "total_tps": int(df['gap_tps'].sum()),
            "total_biaya": f"Rp {(df['estimasi_biaya'].sum()/1e9):,.2f} Milyar"
        },
        "chart": {
            "labels": chart_data['Kecamatan'].tolist(),
            "data": chart_data['gap_tps'].tolist()
        },
        "table_data": df.to_dict(orient='records') # <--- WAJIB ADA INI
    }

    with open('dashboard_data.json', 'w') as f:
        json.dump(payload, f)

if __name__ == '__main__':
    generate_dashboard()