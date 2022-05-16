import streamlit
import requests
import pandas as pd
import snowflake.connector
from urllib.error import URLError

streamlit.title(' This is a snowflake demo excercise part -1')

streamlit.header('Excercise using streamlit')

streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list=pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')


fruits_selected=streamlit.multiselect("Pick some fruits",list(my_fruit_list.index),['Avocado','Strawberries','Peach'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


def get_fruityvice_data(this_fruit_choice):
  fruityvice_response=requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized=pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized




streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice=streamlit.text_input('What fruit would you like information about ?')
  if not fruit_choice:
    streamlit.error("select a fruit to get information")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    

except URLError as e:
  streamlit.error()    
    
streamlit.header("the fruit load list contains")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
  
  
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from streamlit') ")
    return "Thanks for adding " + new_fruit
  
add_my_fruit=streamlit.text_input('what fruit would you like to add ? ')
if streamlit.button('add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)

