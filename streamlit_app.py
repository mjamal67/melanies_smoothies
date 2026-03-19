# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import requests  

# Write directly to the app
#st.title(f"Example Streamlit App :balloon: {st.__version__}")
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name of Smoothie:')
st.write ('The name of your smoothie will be: ', name_on_order)

# st.selectbox(label, options, index=0, format_func=special_internal_function, key=None, help=None, on_change=None, args=None, kwargs=None, *, placeholder=None, disabled=False, label_visibility="visible", accept_new_options=False, width="stretch", bind=None)
# option = st.selectbox("What is your favourite fruit?", ('Banana','Strawberry','Peaches'))

# st.write('You favourite fruit is:', option)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

#st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list = st.multiselect (
    'Choose upto 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredients_string = ''
    
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen) 
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    #st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    
    time_to_insert = st.button('Submit Order')

    #st.write(my_insert_stmt)
    #st.stop()

       
    # if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
 
# st.text(smoothiefroot_response)
# st.text(smoothiefroot_response.json())

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon") 
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
