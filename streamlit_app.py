# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the Fruits you want in your Custom Smoothie!
  """
) 


name_on_order = st.text_input("Name on the smoothie")
st.write("The name on the Smoothie will be", name_on_order)


# Establish Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect (
    'Choose upto 5 ingredients:'
    , my_dataframe
    , max_selections=5
)


if(ingredients_list):
    ingredients_string = ''
    for Fruit_chosen  in ingredients_list:
        ingredients_string += Fruit_chosen + ' '
        st.subheader(Fruit_chosen + 'Nutrtion Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + Fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)        


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

    st.write(my_insert_stmt)

    
    time_to_insert = st.button ('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered!, {name_on_order}', icon="✅")


    
