import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import config
from pathlib import Path

class Visualizador:
    """
    Clase encargada de la capa de presentación (View).
    Genera reportes gráficos con anotaciones técnicas embebidas.
    """
    
    def __init__(self):
        # Configuración estética global
        sns.set_theme(style="whitegrid")
        plt.rcParams['figure.figsize'] = (10, 7)
        plt.rcParams['figure.dpi'] = 100
        self.output_dir = config.DIR_GRAFICOS

    def generar_dashboard(self, df_clima: pd.DataFrame, df_btc: pd.DataFrame):
        """Orquestador de gráficos."""
        print("[VISUALIZADOR] Renderizando dashboard con insights...")
        
        self._plot_clima_sensacion(df_clima)
        self._plot_clima_correlacion(df_clima)
        self._plot_clima_humedad_lluvia(df_clima)
        self._plot_crypto_tendencia(df_btc)
        self._plot_crypto_volatilidad(df_btc)
        self._plot_comparativo_reto_avanzado(df_clima, df_btc)
        
        print(f"[VISUALIZADOR] Gráficos guardados en: {self.output_dir}")

    # --- Gráficos Básicos ---
    def _plot_clima_sensacion(self, df):
        plt.figure()
        plt.plot(df['fecha_hora'], df['temperatura_c'], label='Temp. Real', marker='o', color='#E67E22')
        plt.plot(df['fecha_hora'], df['sensacion_termica_c'], label='Sensación', linestyle='--', color='#D35400')
        plt.title("1. Realidad vs. Sensación Térmica")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.output_dir / "01_clima_sensacion.png")
        plt.close()

    def _plot_clima_correlacion(self, df):
        plt.figure(figsize=(8, 6))
        cols = ['temperatura_c', 'humedad_relativa_%', 'probabilidad_lluvia_%', 'velocidad_viento_kmh']
        sns.heatmap(df[cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("2. Matriz de Correlación Climática")
        plt.tight_layout()
        plt.savefig(self.output_dir / "02_clima_correlacion.png")
        plt.close()

    def _plot_clima_humedad_lluvia(self, df):
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('Hora')
        ax1.set_ylabel('Humedad (%)', color='tab:blue')
        ax1.plot(df['fecha_hora'], df['humedad_relativa_%'], color='tab:blue')
        
        ax2 = ax1.twinx()
        ax2.set_ylabel('Prob. Lluvia (%)', color='gray')
        ax2.bar(df['fecha_hora'], df['probabilidad_lluvia_%'], color='gray', alpha=0.3)
        plt.title("3. Humedad y Riesgo de Lluvia")
        plt.tight_layout()
        plt.savefig(self.output_dir / "03_clima_riesgo.png")
        plt.close()

    def _plot_crypto_tendencia(self, df):
        plt.figure()
        sns.lineplot(data=df, x='fecha_hora', y='precio_btc_usd', color='#2980B9')
        plt.title("4. Tendencia Bitcoin (USD)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.output_dir / "04_crypto_tendencia.png")
        plt.close()

    def _plot_crypto_volatilidad(self, df):
        plt.figure()
        sns.boxplot(y=df['precio_btc_usd'], color='lightblue')
        plt.title("5. Dispersión/Volatilidad (Boxplot)")
        plt.tight_layout()
        plt.savefig(self.output_dir / "05_crypto_volatilidad.png")
        plt.close()

    # --- Gráfico Avanzado con Justificación Técnica ---
    def _plot_comparativo_reto_avanzado(self, df_clima, df_btc):
        # Gráfico combinado con justificación técnica embebida
        fig, ax1 = plt.subplots(figsize=(10, 8)) # Más alto para el texto
        
        # Eje 1: Clima (Rojo)
        color_1 = '#C0392B' # Rojo oscuro profesional
        ax1.set_xlabel('Tiempo (UTC)', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Temperatura (°C)', color=color_1, fontsize=11, fontweight='bold')
        ax1.plot(df_clima['fecha_hora'], df_clima['temperatura_c'], 
                 color=color_1, linestyle='-', linewidth=2, alpha=0.8, label="Variable Física")
        ax1.tick_params(axis='y', labelcolor=color_1)

        # Eje 2: Bitcoin (Azul)
        ax2 = ax1.twinx()
        color_2 = '#2980B9' # Azul profesional
        ax2.set_ylabel('Bitcoin (USD)', color=color_2, fontsize=11, fontweight='bold')
        ax2.plot(df_btc['fecha_hora'], df_btc['precio_btc_usd'], 
                 color=color_2, linewidth=1.5, alpha=0.9, label="Variable Financiera")
        ax2.tick_params(axis='y', labelcolor=color_2)

        # Título
        plt.title("6. RETO: Contraste de Naturaleza de Datos (Física vs Mercado)", fontsize=13, pad=20)
        
        # Leyenda combinada
        texto_justificacion = (
            "JUSTIFICACIÓN TÉCNICA DE LAS DIFERENCIAS:\n"
            "───────────────\n"
            "A) Inercia (Curva Roja): La variable climática muestra suavidad y cambios graduales,\n"
            "   obedeciendo a leyes físicas de termodinámica (Inercia Térmica).\n\n"
            "B) Estocasticidad (Curva Azul): La variable financiera presenta ruido de alta frecuencia\n"
            "   y cambios abruptos, característicos de sistemas especulativos no deterministas.\n\n"
            "CONCLUSIÓN: Aunque comparten el eje temporal, las series son estructuralmente disjuntas."
        )

        # Ajustamos el margen inferior para hacer espacio al texto
        plt.subplots_adjust(bottom=0.28) 

        # Insertamos el cuadro de texto en el pie de página del gráfico
        plt.figtext(
            0.5, 0.02,              # Coordenadas (x=centro, y=abajo)
            texto_justificacion,    # El texto
            ha="center",            # Alineación horizontal
            fontsize=9, 
            fontfamily='monospace', # Fuente tipo código/técnica
            bbox={
                "facecolor": "#f8f9fa", # Fondo gris muy claro
                "edgecolor": "#bdc3c7", # Borde gris
                "boxstyle": "round,pad=1",
                "alpha": 1
            }
        )

        # Guardar
        plt.savefig(self.output_dir / "06_reto_comparativa_analisis.png")
        plt.close()