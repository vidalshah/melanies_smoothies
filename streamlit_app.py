# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the Fruits you want in your Custom Smoothie!"""
)

# Input for the name on the smoothie
name_on_order = st.text_input("Name on the smoothie")
st.write("The name on the Smoothie will be", name_on_order)

# Establish Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Query Snowflake to get the available fruit options
try:
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
    # Collect the Snowpark DataFrame into a list of fruit names
    fruits = my_dataframe.collect()

    # Check if fruits are available
    if not fruits:
        st.error("No fruit options found in the database.")
    else:
        fruit_list = [row['FRUIT_NAME'] for row in fruits]
except Exception as e:
    st.error(f"An error occurred while fetching data from Snowflake: {e}")

# Create the multiselect widget for selecting up to 5 fruits
if fruits:
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        fruit_list,  # Passing the list of fruits from Snowflake
        max_selections=5
    )

    # Check if the user has selected ingredients
    if ingredients_list:
        # Create a string of the selected fruits
        ingredients_string = ', '.join(ingredients_list)

        # SQL statement to insert the order into the Snowflake database
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        # Display the SQL insert statement (for debugging)
        st.write("SQL Insert Statement:", my_insert_stmt)

        # Button to submit the order
        time_to_insert = st.button('Submit Order')

        # If the user clicks submit, execute the SQL statement
        if time_to_insert:
            try:
                session.sql(my_insert_stmt).collect()
                st.success(f'Your Smoothie is ordered! {name_on_order}', icon="✅")
            except Exception as e:
                st.error(f"An error occurred while submitting the order: {e}")


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

