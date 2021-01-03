import streamlit as st
import streamlit.components.v1 as components
import codecs
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd
import numpy as np
from prettytable import PrettyTable
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

#Page Setup
st.set_page_config( layout='wide')
st.title('Convexting: Personalized Real Estate Investing Guide')
#st.markdown ('Personalized Real Estate Investing Guide')

###Sidebar variables
st.sidebar.title("How Do You Stack Up?")
st.sidebar.markdown ("Scale is relative to cost of living at area you are investing in.")
st.sidebar.markdown ("(1=very low, 2=low, 3=med, 4=high, 5=very high)")

###Sidebar variables
user_module = st.sidebar.selectbox('Module', 
                                   ["Primary Residence (PR)","Investment Property (IP)","House Hacking (HH)","Repair & Renovation (RR)"])
user_strategy_category = st.sidebar.selectbox('Strategy Category', 
                                   ["All", "1. Foundation","2. Resource","3. Analysis","4. Buy Transaction", "5. Mortgage", "6. Tax","7. Value Add","8. Property Management","9. Legal","10. Sell Transaction"])
user_income_level = st.sidebar.slider('Financial - Income Level', min_value=1, max_value=5, value=3, step=1)
user_income_stability = st.sidebar.slider('Financial -Income Stability',min_value=1, max_value=5, value=3, step=1)
user_capital_availability = st.sidebar.slider('Financial - Capital Availability',min_value=1, max_value=5, value=3, step=1)
user_credit_score = st.sidebar.slider('Financial - Credit Score',min_value=1, max_value=5, value=3, step=1)
user_risk_tolerance = st.sidebar.slider('Preference - Risk Tolerance',min_value=1, max_value=5, value=3, step=1)
user_complexity = st.sidebar.slider('Preference - Complexity (e.g. 5 = I can handle very high complexity tasks)',min_value=1, max_value=5, value=3, step=1)
user_effort = st.sidebar.slider('Preference - Effort (e.g. 5 = I am willing to put in very high amount of effort)',min_value=1, max_value=5, value=3, step=1)
user_high_impact = st.sidebar.selectbox('Only show "High Impact" strategy? (i.e. strategies that directly add to the bottom line)', 
                                   ["High Impact Strategies Only ", "Show All Strategies"])

###
### User Input Matrix Setup
user_input_matrix = {
                     'User': ["User 2134"],
                     'Module': [user_module],
                     'Income Level': [user_income_level],
                     'Income Stability': [user_income_stability],
                     'Capital Availability': [user_capital_availability],
                     'Credit Score': [user_credit_score],
                     'Risk Tolerance': [user_risk_tolerance],
                     'Complexity': [user_complexity],
                     'Effort': [user_effort],
                     }
user_input_matrix = pd.DataFrame(data=user_input_matrix)



### User Input Matrix Graphing and Formatting
user_input_matrix_fig = go.Figure(data=[go.Table(
    columnwidth = [70,40],
    header=dict(values=list(user_input_matrix.columns),
                fill_color='royalblue',
                line_color='darkslategray',
                align=['left','center'],
                font=dict(color='white', size=10),
                height=40),
    cells=dict(values=[user_input_matrix['User'],
                       user_input_matrix['Module'],
                       user_input_matrix['Income Level'],
                       user_input_matrix['Income Stability'], 
                       user_input_matrix['Capital Availability'], 
                       user_input_matrix['Credit Score'],
                       user_input_matrix['Risk Tolerance'],
                       user_input_matrix['Complexity'],
                       user_input_matrix['Effort']],
               #fill_color='lavender',
               align=['left','center'],
               fill=dict(color=['paleturquoise', 'white']),
               line_color='darkslategray',
               font_size=10))
])


user_input_matrix_fig.update_layout(width=1100, 
                  height=265,
                  margin_autoexpand=True,
                  autosize=True,
                  dragmode=False,
                  title="The following are <b>User Inputs</b> for <b>" + user_module + "</b> module",
                  )




### Strategy Weights
weights=pd.read_excel("streamlit_sample.xls", 
                      sheet_name="weights", 
                      index_col=("Strategy"))


#Load data into excel
strategy_matrix_original=pd.read_excel("streamlit_sample.xls", 
                      sheet_name="strategy", 
                      index_col=("strategy_name"))

strategy_matrix_unfiltered = strategy_matrix_original[[
             "name_short",
             "Module",
             "Income Level", 
             "Income Stability",
             "Capital Availability",
             "Credit Score",
             "Risk Tolerance",
             "Complexity",
             "Effort"]]

strategy_matrix_filtered=strategy_matrix_unfiltered[strategy_matrix_unfiltered['Module']==user_module]




###Weighted Score Calculation

###############Check for column numbers
x=strategy_matrix_filtered.iloc[:, 2:9] #get strategy matrix
y=user_input_matrix.iloc[:, 2:9] #get user input matrix
z=np.subtract(x, y) #find difference
z_pow=abs(z)*abs(z) #power of abs value
weighted_matrix = np.multiply (z_pow, weights)


strategy_matrix_qualified = strategy_matrix_filtered

###strategy_matrix_not qualified


### Calculate by amount of Deviation
strategy_matrix_qualified["Deviation"]=weighted_matrix.sum(axis=1)

###Test if all "User Input" is greater than "Strategy Parameters"
###If the difference of "Strategy Parameters" Minus "User Inputs" is >= 0, then users qualify for the strategy.
strategy_matrix_qualified["Qualify?"]=np.amax(z, axis=1)<=0


##Filtering and Sorting
strategy_matrix_qualified=strategy_matrix_qualified[strategy_matrix_qualified['Module']==user_module]
strategy_matrix_qualified=strategy_matrix_qualified[strategy_matrix_qualified['Qualify?']==True]
strategy_matrix_qualified = strategy_matrix_qualified.sort_values(by=['Deviation'])



###Check to see if all qualify


### Strategy_matrix

strategy_matrix_qualified_fig = go.Figure(data=[go.Table(
    columnwidth = [70,45],
    header=dict(values=list(strategy_matrix_qualified.columns),
                fill_color='royalblue',
                line_color='darkslategray',
                align=['left','center'],
                font=dict(color='white', size=10),
                height=40),
    cells=dict(values=[strategy_matrix_qualified['name_short'],
                       strategy_matrix_qualified['Module'],
                       strategy_matrix_qualified['Income Level'],
                       strategy_matrix_qualified['Income Stability'], 
                       strategy_matrix_qualified['Capital Availability'], 
                       strategy_matrix_qualified['Credit Score'],
                       strategy_matrix_qualified['Risk Tolerance'],
                       strategy_matrix_qualified['Complexity'],
                       strategy_matrix_qualified['Effort'],
                       strategy_matrix_qualified['Deviation'],
                       strategy_matrix_qualified['Qualify?'],
                       ],
               #fill_color='lavender',
               align=['left','center'],
               fill=dict(color=['paleturquoise', 'white']),
               line_color='darkslategray',
               font_size=10))
])

strategy_matrix_qualified_fig.update_layout(
                  width=1100, 
                  #height=250,
                  margin_autoexpand=True,
                  autosize=True,
                  dragmode=False,
                  title="Strategies in <b>" + user_module + "</b> module that are <b>suitable</b> based on all parameters of your answers",
                  )




###strategy_matrix_not qualified
strategy_matrix_not_qualified = strategy_matrix_filtered
strategy_matrix_not_qualified["Deviation"]=weighted_matrix.sum(axis=1)
strategy_matrix_not_qualified["Qualify?"]=np.amax(z, axis=1)<=0

#Filtering
strategy_matrix_not_qualified=strategy_matrix_not_qualified[strategy_matrix_not_qualified['Module']==user_module]
strategy_matrix_not_qualified=strategy_matrix_not_qualified[strategy_matrix_not_qualified['Qualify?']==False]
strategy_matrix_not_qualified = strategy_matrix_not_qualified.sort_values(by=['Deviation'])


strategy_matrix_not_qualified_fig = go.Figure(data=[go.Table(
    columnwidth = [70,45],
    header=dict(values=list(strategy_matrix_not_qualified.columns),
                fill_color='royalblue',
                line_color='darkslategray',
                align=['left','center'],
                font=dict(color='white', size=10),
                height=40),
    cells=dict(values=[strategy_matrix_not_qualified['name_short'],
                       strategy_matrix_not_qualified['Module'],
                       strategy_matrix_not_qualified['Income Level'],
                       strategy_matrix_not_qualified['Income Stability'], 
                       strategy_matrix_not_qualified['Capital Availability'], 
                       strategy_matrix_not_qualified['Credit Score'],
                       strategy_matrix_not_qualified['Risk Tolerance'],
                       strategy_matrix_not_qualified['Complexity'],
                       strategy_matrix_not_qualified['Effort'],
                       strategy_matrix_not_qualified['Deviation'],
                       strategy_matrix_not_qualified['Qualify?'],
                       ],
               #fill_color='lavender',
               align=['left','center'],
               fill=dict(color=['paleturquoise', 'white']),
               line_color='darkslategray',
               font_size=10))
])

strategy_matrix_not_qualified_fig.update_layout(width=1100, 
                  #height=700,
                  margin_autoexpand=True,
                  autosize=True,
                  dragmode=False,
                  title="Strategies in <b>" + user_module + "</b> module that are <b>NOT suitable</b> , but may be just a touch shy from qualifying ",
                  
                  )




####Print
st.write(user_input_matrix_fig)
st.write(strategy_matrix_qualified_fig)
st.write(strategy_matrix_not_qualified_fig)






