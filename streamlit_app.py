import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError



fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
fruit_list = fruit_list.set_index('Fruit')


streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg🥣 🥗 🐔 🥑🍞')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruits_selected = streamlit.multiselect("Pick some", list(fruit_list.index), ['Apple', 'Lime'])
fruits_to_show = fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header('FruityV')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #Uses pandas to normalize the json 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # display normalized json
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()




my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("List contains:")
streamlit.dataframe(my_data_rows)

streamlit.header("Add fruit?")
fruit_choice_insert = streamlit.text_input('What fruit would you like add?')

if fruit_choice_insert != '':
  my_cur.execute(f"insert into fruit_load_list values('{fruit_choice_insert}');")
