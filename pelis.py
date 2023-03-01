import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt



df = pd.read_csv("peliculas.csv")


st.title("Peliculas")

#columnas en español
df = df.rename(columns={
    "Title": "Título",
    "Genre": "Género",
    "Director": "Director",
    "Actors": "Actores",
    "Year": "Año",
    "Runtime (Minutes)": "Duración (Minutos)",
    "Rating": "Calificación",
    "Votes": "Votos",
    "Revenue (Millions)": "Ingresos (Millones)",
    "Metascore": "Puntuación"
})

#tabla con las 10 películas con más ingresos
st.write("Las 10 películas con más ingresos:")
tabla_ingresos = df[["Título", "Director", "Ingresos (Millones)"]].sort_values(by="Ingresos (Millones)", ascending=False).head(10)
st.table(tabla_ingresos)





# relación entre duración y millones en ingresos
relacion_duracion_ingresos = df[["Duración (Minutos)", "Ingresos (Millones)"]].corr(method="pearson").iloc[0, 1]




#gráfico de dispersión con la relación entre calificación y duración
st.write("Relación entre calificación y duración:")
grafico_calificacion_duracion = df.plot(kind="scatter", x="Duración (Minutos)", y="Calificación")
st.pyplot(grafico_calificacion_duracion.get_figure())





# Obtener los actores que más aparecen
top_actores = df['Actores'].str.split(', ').explode().value_counts().head(10)

# Renombrar las columnas en español
top_actores = top_actores.rename_axis('Actor').reset_index(name='Apariciones')

# Mostrar la tabla
st.write("Actores que más aparecen en esta lista:")
st.table(top_actores)




#gráfico de barras con los actores que más aparecen
st.write("Actores que más aparecen en esta lista:")
grafico_actores = alt.Chart(top_actores).mark_bar().encode(
    x="Apariciones",
    y=alt.Y("Actor", sort="-x"),
    color="Apariciones"
)
st.altair_chart(grafico_actores, use_container_width=True)





#gráfico de barras con los géneros más populares
st.write("Géneros más populares:")
generos = df['Género'].str.split(', ').explode().value_counts().reset_index()
grafico_generos = alt.Chart(generos).mark_bar().encode(
    x=alt.X('index:N', axis=alt.Axis(title='Género')),
    y=alt.Y('Género:Q', axis=alt.Axis(title='Número de películas')),
    color=alt.Color('Género:N', legend=None)
)
st.altair_chart(grafico_generos, use_container_width=True)







#gráfico de barras con los directores más populares
st.write("Directores más populares:")
directores = df['Director'].str.split(', ').explode().value_counts().head(10).reset_index()
grafico_directores = alt.Chart(directores).mark_bar().encode(
    x=alt.X('index:N', axis=alt.Axis(title='Director')),
    y=alt.Y('Director:Q', axis=alt.Axis(title='Número de películas')),
    color=alt.Color('Director:N', legend=None)
)
st.altair_chart(grafico_directores, use_container_width=True)



# cantidad de géneros
generos = df['Género'].str.split(', ').explode().value_counts()

# gráfico de pastel
grafico_generos = alt.Chart(generos.reset_index()).mark_arc().encode(
    theta='Género:Q',
    color='index:N',
    tooltip=['index:N', 'Género:Q']
).properties(
    width=500,
    height=500
)


st.write("Distribución de géneros:")
st.altair_chart(grafico_generos, use_container_width=True)



calificacion_promedio_por_anio = df.groupby(df['Año'].astype(int))['Calificación'].mean().reset_index()

calificacion_promedio_por_anio['Año'] = calificacion_promedio_por_anio['Año'].astype(int).astype(str)

grafico_calificacion_promedio = alt.Chart(calificacion_promedio_por_anio).mark_line().encode(
    x='Año',
    y='Calificación',
).properties(
    width=600,
    height=400,
    title='Evolución de la calificación promedio de las películas'
)

st.altair_chart(grafico_calificacion_promedio, use_container_width=True)




# Agrupar las películas por año y encontrar la fila con la calificación más alta para cada grupo
idx = df.groupby('Año')['Calificación'].idxmax()

# Seleccionar las filas correspondientes de la tabla original y ordenarlas por año
top_movies = df.loc[idx, ['Título', 'Año', 'Calificación']].sort_values('Año')

# Redondear la columna "Calificación" a 2 decimales
top_movies['Calificación'] = top_movies['Calificación'].apply(lambda x: round(x, 2))

# Mostrar la tabla en Streamlit
st.write("Película más valorada por cada año:")
st.table(top_movies)





# Seleccionar solo las películas de los años 2014
st.write("Puntuación de Metacritic para películas de IMDB en 2014:")
df_filtered = df[(df['Año'] == 2014)]

# Crear el gráfico de barras
bars = alt.Chart(df_filtered).mark_bar().encode(
    x=alt.X('Puntuación:Q', axis=alt.Axis(title='Puntuación')),
    y=alt.Y('Título:N', axis=alt.Axis(title='Película'))
)

# Agregar título al gráfico
title = alt.Chart({'values': [{'text': 'Puntuación de Metacritic para películas de IMDB'}]}).mark_text(size=20, align='center').encode(text='text:N')

# Mostrar el gráfico
st.altair_chart(bars + title, use_container_width=True)




st.write("Géneros menos votados:")
# Calcular la media de votos por género y ordenar de menor a mayor media
media_votos_por_genero = df.groupby('Género')['Votos'].mean().sort_values()

# Tomar los 5 géneros con la media de votos más baja
generos_menos_votados = media_votos_por_genero.head(5)

# Mostrar los resultados en una tabla con Streamlit
st.write(generos_menos_votados)


