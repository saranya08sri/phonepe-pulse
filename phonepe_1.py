# import packages
import json
import streamlit as st
import pandas as pd
import requests
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from PIL import Image

#dataframe creation

db_connection=psycopg2.connect(host= "localhost",
                               user= "postgres",
                               port= "5432",
                               database= "Phonepe_data",
                               password="admin@081828")

mycursor=db_connection.cursor()

#aggregated_insurance
mycursor.execute("SELECT * FROM aggregated_insurance")
db_connection.commit()
Table1= mycursor.fetchall()

Aggre_insurance = pd.DataFrame(Table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"))

#aggregated_transaction

mycursor.execute("SELECT * FROM aggregated_transaction")
db_connection.commit()
Table2= mycursor.fetchall()

Aggre_transaction = pd.DataFrame(Table2,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#aggregated_user

mycursor.execute("SELECT * FROM aggregated_user")
db_connection.commit()
Table3= mycursor.fetchall()

Aggre_user = pd.DataFrame(Table3,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))


#map_insurance

mycursor.execute("SELECT * FROM  map_insurance")
db_connection.commit()
Table4= mycursor.fetchall()

Map_insurance = pd.DataFrame(Table4,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))

#map_transaction

mycursor.execute("SELECT * FROM  map_transaction")
db_connection.commit()
Table5= mycursor.fetchall()

Map_transaction = pd.DataFrame(Table5,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#map_user

mycursor.execute("SELECT * FROM  map_user")
db_connection.commit()
Table6= mycursor.fetchall()

Map_user = pd.DataFrame(Table6,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

#top_insurance

mycursor.execute("SELECT * FROM  top_insurance")
db_connection.commit()
Table7= mycursor.fetchall()

Top_insurance = pd.DataFrame(Table7,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#top_transaction

mycursor.execute("SELECT * FROM  top_transaction")
db_connection.commit()
Table8= mycursor.fetchall()

Top_transaction = pd.DataFrame(Table8,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#top_user
mycursor.execute("SELECT * FROM  top_user")
db_connection.commit()
Table9= mycursor.fetchall()

Top_user = pd.DataFrame(Table9, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))

# Aggreagated insurance analysis

def Aggre_insurance_Y(df,year):
    aiy= df[df["Years"] == year]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(aiyg, x="States", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                           width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(aiyg, x="States", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                          width=600, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        

        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "ylorbr",
                                 range_color= (aiyg["Transaction_amount"].min(),aiyg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "ylgn",
                                 range_color= (aiyg["Transaction_count"].min(),aiyg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)

    return aiy


#aggregated insurance Quatrer wise analysis
def Aggre_insurance_Y_Q(df,quarter):
    aiyq= df[df["Quarter"] == quarter]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount = px.pie(aiyqg, values="Transaction_amount", names="States",
                      title=f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",
                      width=600, height=650, color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)


    with col2:
        fig_q_count= px.pie(aiyqg, names= "States", values= "Transaction_count", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "ylorbr",
                                 range_color= (aiyqg["Transaction_amount"].min(),aiyqg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "ylgn",
                                 range_color= (aiyqg["Transaction_count"].min(),aiyqg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)
    
    return aiyq

#aggregated transaction analysis with transaction_type

def Aggre_Transaction_type(df, state):

    aiyq= df[df["States"] == state]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace= True)
    
    col1,col2 = st.columns(2)
    with col1:

        fig_pie_1 = px.pie(data_frame=aiyqg, names = "Transaction_type", values = "Transaction_amount",
                        width = 700, title = f"{state.upper()} TRANSACTION AMOUNT",color_discrete_sequence=['#2ca02c'],hole=0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        
        fig_pie_2 = px.pie(data_frame=aiyqg, names = "Transaction_type", values = "Transaction_count",
                        width = 700, title = f"{state.upper()} TRANSACTION COUNT",color_discrete_sequence=['#2ca02c'],hole=0.5)
        st.plotly_chart(fig_pie_2)


#Aggregated user analysis 1
def Aggre_user_plot1(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True, inplace =True)

    aguy_g = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguy_g.reset_index(inplace = True)

    fig_bar_1 = px.bar(aguy, x="Brands", y="Transaction_count",title = f"{year} BRANDS AND TRANSACTION COUNT",
                    width = 1000,color_discrete_sequence=px.colors.sequential.Bluered_r,hover_name = "Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy

#aggregated_useranalysis 2

def aggre_user_plot_2(df,quarter):
    aguyq=df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True, inplace =True)

    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace = True)

    fig_bar_1 = px.bar(aguyqg, x="Brands", y="Transaction_count",title = f"{quarter}  QUARTER-BRANDS AND TRANSACTION COUNT",
                    width = 1000,color="Transaction_count", color_continuous_scale='Blues',hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguyq

#Aggregated user analysis plot 3

def Agg_user_plot_3(df,state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1=px.line(auyqs, x="Brands",y="Transaction_count",hover_data="Percentage",
                    title =f"{state.upper()} - TRANSACTION AND PERCENTAGE",width=1000,markers=True)
    st.plotly_chart(fig_line_1)

# Map insurance Disrticts

def Map_insu_District(df, state):

    aiyq= df[df["States"] == state]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2=st.columns(2)
    with col1:
    
        fig_bar_1 = px.bar(aiyq, x="Transaction_amount", y="Districts",orientation="h",height = 600,
                        title=f"{state.upper()} - DISTRICTS AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        
        fig_bar_2 =px.bar(aiyq, x="Transaction_count", y="Districts",orientation="h",height = 600,
                        title=f"{state.upper()} - DISTRICTS AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

# map user_plot_1

def map_user_plot_1(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True, inplace =True)

    muy_g = muy.groupby("States")[["RegisteredUser","AppOpens"]].sum()
    muy_g.reset_index(inplace = True)

    melted_df = pd.melt(
        muy_g, 
        id_vars=['States'], 
        value_vars=['RegisteredUser', 'AppOpens'], 
        var_name='Metric', 
        value_name='Value'
    )

    # Create sunburst chart
    fig_sunburst = px.sunburst(
        melted_df, 
        path=['Metric', 'States'],  # Define the hierarchical levels
        values='Value',
        color_discrete_sequence=['#A833FF'],
        width = 500,
        height = 1000,
        title=f"{year} - RegisteredUser and AppOpens by State")

    # Display the sunburst chart
    st.plotly_chart(fig_sunburst)
    
    return muy

# map_user plot_2

def map_user_plot_2(df,quarter):
    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True, inplace =True)

    muyq_g = muyq.groupby("States")[["RegisteredUser","AppOpens"]].sum()
    muyq_g.reset_index(inplace = True)
    
    fig_line_1 = px.line(muyq_g , x= "States",y = ["RegisteredUser","AppOpens"],
                         title = f"{df['Years'].min()} year {quarter}-REGISTERED USER AND APPONES BY QUARTER", width=1000,height=800,markers=True)
    st.plotly_chart(fig_line_1)
    
    return muyq

#map_user_plot_3

def map_user_plot_3(df,states):
    muyqs=df[df["States"] == states]
    muyqs.reset_index(drop=True, inplace =True)

    col1,col2=st.columns(2)
    with col1:
        fig_map_user_bar1 = px.bar(muyqs,x="RegisteredUser",y = "Districts",orientation="h",
                                title = f"{states.upper()} - REGISTERD USER" , height = 800,color_discrete_sequence=px.colors.sequential.Mint_r)

        st.plotly_chart(fig_map_user_bar1)

    with col2:
        fig_map_user_bar2 = px.bar(muyqs,x="AppOpens",y = "Districts",orientation="h",
                                title = f"{states.upper()} - APP OPENS" , height = 800,color_discrete_sequence=px.colors.sequential.Bluered_r)

        st.plotly_chart(fig_map_user_bar2)


# top_insurance_plot_1
def top_insurance_plot_1(df,state):
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True, inplace =True)

    col1,col2 = st.columns(2)
    with col1:
        fig_top_insu_bar1 = px.bar(tiy,x="Quarter",y = "Transaction_amount",hover_data = "Pincodes",
                                    title = f"{state.upper()} - TRANSACTION AMOUNT" , height = 800,color_discrete_sequence=px.colors.sequential.Mint_r)

        st.plotly_chart(fig_top_insu_bar1)
    with col2:
        fig_top_insu_bar2 = px.bar(tiy,x="Quarter",y = "Transaction_count",hover_data = "Pincodes",
                                    title = f"{state.upper()} - TRANSACTION COUNT" , height = 800,color_discrete_sequence=px.colors.sequential.Bluered_r)

        st.plotly_chart(fig_top_insu_bar2)

#top_user_plot_1
def top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True, inplace =True)

    tuy_g = pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUser"].sum())
    tuy_g.reset_index(inplace = True)

    fig_area_chart = px.area(
    tuy_g,
    x="States",
    y="RegisteredUser",
    color="Quarter",
    width=1000,
    height=800,
    title=f"{year} - REGISTERED USERS"
)

# Display the area chart using Streamlit
    st.plotly_chart(fig_area_chart)
    return tuy

#top_user_plot_2
def top_user_plot_2(df,state):
    tuys=df[df["States"]==state]
    tuys.reset_index(drop=True, inplace =True)

    fig_top_user_plot_2 = px.bar(tuys,x="Quarter",y="RegisteredUser",title = "RESIGTREDUSERS,PINCODES BY QUARTER",
                                width = 1000,height=800,color="RegisteredUser",hover_data="Pincodes",
                                color_continuous_scale = px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_user_plot_2)

def top_chart_transaction_amount(table_name):
    db_connection=psycopg2.connect(host= "localhost",
                                user= "postgres",
                                port= "5432",
                                database= "Phonepe_data",
                                password="admin@081828")

    mycursor=db_connection.cursor()


    #plot_1
    query1 = f'''select states,SUM(transaction_amount) as transaction_amount 
                    from {table_name}
                    GROUP BY states
                    order by transaction_amount desc
                    limit 10'''
    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    db_connection.commit()

    df1 = pd.DataFrame(table_1,columns=("states","transaction_amount"))
    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.bar(df1, x="states", y= "transaction_amount",title= " TOP 10 OF TRANSACTION AMOUNT",hover_name ="states",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)

    #plot_2
    query2 = f'''select states,SUM(transaction_amount) as transaction_amount 
                    from {table_name}
                    GROUP BY states
                    order by transaction_amount 
                    limit 10'''
    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    db_connection.commit()

    df2 = pd.DataFrame(table_2,columns=("states","transaction_amount"))
    
    with col2:
        fig_amount_2= px.bar(df2, x="states", y= "transaction_amount",title= "LAST 10 OF TRANSACTION AMOUNT",hover_name ="states",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3 = f'''select states,avg(transaction_amount) as transaction_amount 
                    from {table_name}
                    GROUP BY states
                    order by transaction_amount'''
    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    db_connection.commit()

    df3 = pd.DataFrame(table_3,columns=("states","transaction_amount"))
    fig_amount_3= px.bar(df3, x="transaction_amount", y= "states",title= "AVERAGE OF TRANSACTION AMOUNT",hover_name ="states",orientation="h",
                            width=1000, height= 800, color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_amount_3)

# chart visualisation functions for transaction amount and transaction count    
def top_chart_transaction_count(table_name):
    db_connection=psycopg2.connect(host= "localhost",
                                user= "postgres",
                                port= "5432",
                                database= "Phonepe_data",
                                password="admin@081828")

    mycursor=db_connection.cursor()



    query1 = f'''select states,SUM(transaction_count) as transaction_count
                    from {table_name}
                    GROUP BY states
                    order by transaction_count desc
                    limit 10'''
    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    db_connection.commit()

    df1 = pd.DataFrame(table_1,columns=("states","transaction_count"))
    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.pie(df1, names="states", values= "transaction_count",title= "TOP 10 OF TRANSACTION COUNT",hover_name ="states",
                                width=800, height= 700, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)


    query2 = f'''select states,SUM(transaction_count) as transaction_count 
                    from {table_name}
                    GROUP BY states
                    order by transaction_count 
                    limit 10'''
    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    db_connection.commit()

    df2 = pd.DataFrame(table_2,columns=("states","transaction_count"))
    with col2:
        fig_amount_2= px.pie(df2, names="states", values= "transaction_count",title= "LAST 10 OF TRANSACTION COUNT",hover_name ="states",
                                width=800, height= 700, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3 = f'''select states,avg(transaction_count) as transaction_count 
                    from {table_name}
                    GROUP BY states
                    order by transaction_count'''
    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    db_connection.commit()

    df3 = pd.DataFrame(table_3,columns=("states","transaction_count"))
    fig_amount_3= px.pie(df3, names="states", values= "transaction_count",title= "AVERAGE OF TRANSACTION COUNT",hover_name ="states",
                            width=1000, height= 800, color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig_amount_3)
#chart visualisation for registered user        
def top_chart_registered_user(table_name, state):
    db_connection=psycopg2.connect(host= "localhost",
                                user= "postgres",
                                port= "5432",
                                database= "Phonepe_data",
                                password="admin@081828")

    mycursor=db_connection.cursor()



    query1 = f'''select districts,sum(registereduser) as registereduser
                    from {table_name}
                    where states='{state}'
                    group by districts
                    order by registereduser desc
                    limit 10;'''
    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    db_connection.commit()

    df1 = pd.DataFrame(table_1,columns=("districts","registereduser"))
    
    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.bar(df1, x="districts", y= "registereduser",title= "TOP 10 OF REGISTERED USER",hover_name ="districts",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)


    query2 = f'''select districts,sum(registereduser) as registereduser
                    from {table_name}
                    where states='{state}'
                    group by districts
                    order by registereduser 
                    limit 10;'''
    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    db_connection.commit()

    df2 = pd.DataFrame(table_2,columns=("districts","registereduser"))
    
    with col2:
        fig_amount_2= px.bar(df2, x="districts", y= "registereduser",title= "LAST 10 OF REGISTERED USER",hover_name ="districts",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3 =f'''select districts,avg(registereduser) as registereduser
                    from map_user {table_name}
                    where states='{state}'
                    group by districts
                    order by registereduser;'''
    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    db_connection.commit()

    df3 = pd.DataFrame(table_3,columns=("districts","registereduser"))
    fig_amount_3= px.bar(df3, x="registereduser", y= "districts",title= "AVEREGE OF REISTERED USER",hover_name ="districts",orientation="h",
                            width=800, height= 1000, color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_amount_3)

#chart visualisation of appopens
def top_chart_appopens(table_name, state):
    db_connection=psycopg2.connect(host= "localhost",
                                user= "postgres",
                                port= "5432",
                                database= "Phonepe_data",
                                password="admin@081828")

    mycursor=db_connection.cursor()



    query1 = f'''select districts,sum(appopens) as appopens
                    from {table_name}
                    where states='{state}'
                    group by districts
                    order by appopens desc
                    limit 10;'''
    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    db_connection.commit()

    df1 = pd.DataFrame(table_1,columns=("districts","appopens"))
    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.bar(df1, x="districts", y= "appopens",title= "TOP 10 OF APP OPENS",hover_name ="districts",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)


    query2 = f'''select districts,sum(appopens) as appopens
                    from {table_name}
                    where states='{state}'
                    group by districts
                    order by appopens 
                    limit 10;'''
    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    db_connection.commit()

    df2 = pd.DataFrame(table_2,columns=("districts","appopens"))
    with col2:
        fig_amount_2= px.bar(df2, x="districts", y= "appopens",title= "LAST 10 OF APP OPENS",hover_name ="districts",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount_2)
    #plot_3
    query3 =f'''select districts,avg(appopens) as appopens
                    from map_user {table_name}
                    where states='{state}'
                    group by districts
                    order by appopens;'''
    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    db_connection.commit()

    df3 = pd.DataFrame(table_3,columns=("districts","appopens"))
    fig_amount_3= px.bar(df3, x="appopens", y= "districts",title= "AVEREGE OF APP OPENS",hover_name ="districts",orientation="h",
                            width=800, height= 1000, color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_amount_3)
    
# reagistrerd user
def top_chart_registered_user1(table_name):
    db_connection=psycopg2.connect(host= "localhost",
                                user= "postgres",
                                port= "5432",
                                database= "Phonepe_data",
                                password="admin@081828")

    mycursor=db_connection.cursor()



    query1 = f'''select states, sum(registereduser) as registereduser
                    from {table_name}
                    group by states
                    order by registereduser desc
                    limit 10;'''
    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    db_connection.commit()

    df1 = pd.DataFrame(table_1,columns=("states","registereduser"))
    
    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.pie(df1, names="states", values= "registereduser",title= "TOP 10 OF REGISTERED USER-1",hover_name ="states",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)


    query2 = f'''select states, sum(registereduser) as registereduser
                    from {table_name}
                    group by states
                    order by registereduser
                    limit 10;'''
    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    db_connection.commit()

    df2 = pd.DataFrame(table_2,columns=("states","registereduser"))
    
    with col2:
        fig_amount_2= px.pie(df2, names="states", values= "registereduser",title= "LAST 10 OF REGISTERED USER-1",hover_name ="states",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3 =f'''select states, avg(registereduser) as registereduser
                from {table_name}
                group by states
                order by registereduser;'''
    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    db_connection.commit()

    df3 = pd.DataFrame(table_3,columns=("states","registereduser"))
    fig_amount_3= px.pie(df3, values="registereduser", names= "states",title= "AVEREGE OF REISTERED USER-1",hover_name ="states",
                            width=800, height= 1000, color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_amount_3)
    
#chart visualisation of branda   
def top_chart_brands(table_name):
    db_connection=psycopg2.connect(host= "localhost",
                                user= "postgres",
                                port= "5432",
                                database= "Phonepe_data",
                                password="admin@081828")

    mycursor=db_connection.cursor()



    query1 = f'''select brands,sum(transaction_count) as transaction_count 
                    from {table_name}
                    group by brands
                    order by transaction_count 
                    limit 10;'''
    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    db_connection.commit()

    df1 = pd.DataFrame(table_1,columns=("brands","transaction_count"))
    
    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.pie(df1, names="brands", values= "transaction_count",title= "TOP 10 OF BRANDS",hover_name ="brands",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)


    query2 = f'''select brands,sum(transaction_count) as transaction_count 
                    from {table_name}
                    group by brands
                    order by transaction_count desc
                    limit 10;'''
    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    db_connection.commit()

    df2 = pd.DataFrame(table_2,columns=("brands","transaction_count"))
    
    with col2:
        fig_amount_2= px.pie(df2, names="brands", values= "transaction_count",title= "LAST 10 OF BRANDS",hover_name ="brands",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3 =f'''select brands,avg(transaction_count) as transaction_count 
                    from {table_name}
                    group by brands
                    order by transaction_count;'''
    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    db_connection.commit()

    df3 = pd.DataFrame(table_3,columns=("brands","transaction_count"))
    fig_amount_3= px.bar(df3, x="transaction_count", y= "brands",title= "AVEREGE OF BRANDS",hover_name ="brands",orientation="h",
                            width=800, height= 1000, color_discrete_sequence=px.colors.sequential.Bluered)
    st.plotly_chart(fig_amount_3)

#chart visualisation foe district analysis
def top_chart_district(table_name, state):
    db_connection=psycopg2.connect(host= "localhost",
                                user= "postgres",
                                port= "5432",
                                database= "Phonepe_data",
                                password="admin@081828")

    mycursor=db_connection.cursor()



    query1 = f'''select district, sum(transaction_amount) as transaction_amount 
                    from {table_name}
                    where states='{state}'
                    group by district
                    order by transaction_amount
                    limit 10;'''
    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    db_connection.commit()

    df1 = pd.DataFrame(table_1,columns=("district","transaction_amount"))
    
    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.pie(df1, names="district", values= "transaction_amount",title= "TOP 10  DISTRICTS",hover_name ="district",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)


    query2 = f'''select district, sum(transaction_amount) as transaction_amount 
                    from {table_name}
                    where states='{state}'
                    group by district
                    order by transaction_amount desc
                    limit 10;'''
    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    db_connection.commit()

    df2 = pd.DataFrame(table_2,columns=("district","transaction_amount"))
    
    with col2:
        fig_amount_2= px.pie(df2, names="district", values= "transaction_amount",title= "LAST 10 DISTRICTS",hover_name ="district",
                                width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3 =f'''select district, avg(transaction_amount) as transaction_amount 
                    from {table_name}
                    where states='{state}'
                    group by district
                    order by transaction_amount;'''
    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    db_connection.commit()

    df3 = pd.DataFrame(table_3,columns=("district","transaction_amount"))
    fig_amount_3= px.bar(df3, x="transaction_amount", y= "district",title= "AVEREGE OF DISTRICTS",hover_name ="district",orientation="h",
                            width=800, height= 1000, color_discrete_sequence=px.colors.sequential.Bluered)
    st.plotly_chart(fig_amount_3)

# cahrt visualsation for transaction_type analysis
def top_chart_transaction_type(table_name, state):
    db_connection=psycopg2.connect(host= "localhost",
                                user= "postgres",
                                port= "5432",
                                database= "Phonepe_data",
                                password="admin@081828")

    mycursor=db_connection.cursor()



    query1 = f'''select transaction_type, sum(transaction_amount) as transaction_amount 
                        from {table_name}
                        where states='{state}'
                        group by transaction_type
                        order by transaction_amount
                        limit 10;'''
    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    db_connection.commit()

    df1 = pd.DataFrame(table_1,columns=("transaction_type","transaction_amount"))
    
    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.pie(df1, names="transaction_type", values= "transaction_amount",title= "TOP 10 TRANSACTION_TYPE",hover_name ="transaction_type",
                                width=600, hole = 0.5,height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)


    query2 = f'''select transaction_type, sum(transaction_amount) as transaction_amount 
                        from {table_name}
                        where states='{state}'
                        group by transaction_type
                        order by transaction_amount desc
                        limit 10;'''
    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    db_connection.commit()

    df2 = pd.DataFrame(table_2,columns=("transaction_type","transaction_amount"))
    
    with col2:
        fig_amount_2= px.pie(df2, names="transaction_type", values= "transaction_amount",title= "LAST 10 TRANSACTION_TYPE",hover_name ="transaction_type",
                                width=600,hole=0.5, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3 =f'''select transaction_type, avg(transaction_amount) as transaction_amount 
                    from {table_name}
                    where states='{state}'
                    group by transaction_type
                    order by transaction_amount;'''
    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    db_connection.commit()

    df3 = pd.DataFrame(table_3,columns=("transaction_type","transaction_amount"))
    fig_amount_3= px.bar(df3, x="transaction_amount", y= "transaction_type",title= "AVEREGE OF TRANSACTION_TYPE",hover_name ="transaction_type",orientation="h",
                            width=800, height= 1000, color_discrete_sequence=px.colors.sequential.Bluered)
    st.plotly_chart(fig_amount_3)



#streamlit part
#heading part
st.set_page_config(layout="wide")
st.title(':violet[ PhonePe Pulse Data Visualization ]')


select = option_menu(None, ["HOME","DATA EXPLORATION","CHART VISUALIZATION"],
                       icons=["house","cloud-upload","pencil-square"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "35px", "text-align": "centre", "margin": "0px", "--hover-color": "#6495ED"},
                               "icon": {"font-size": "35px"},
                               "container" : {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#6495ED"}})

if select == "HOME":
    st.markdown("# About PhonePe Pulse Data")
    st.markdown("""PhonePe has launched PhonePe Pulse, a data analytics platform that provides insights into
               how Indians are using digital payments.Through this app, you 
               can now easily access and visualize the data provided by PhonePe Pulse, gaining deep 
               insights and interesting trends into how India transacts with digital payments.""")
    
    
    col1,col2 = st.columns(2)
    with col1:
        st.video("c:\\Users\\admin'\\Desktop\\Introducing PhonePe Pulse.mp4")
    with col2:
        st.header("FEATUERS OF PHONEPE")
        st.write("****Bill Payements****")
        st.write("****Mobile Rechare****")
        st.write("****Transfer Money****")
        st.write("****Bank Balance Check and etc..****")
        st.markdown("")
        st.markdown("")
        st.header("BENFITS OF PHONEPE")
        st.write("****>>>The app is safe to use****")
        st.write("****>>>PhonePe is one of the few user-friendly apps which takes very little time to get accustomed to.****")
        st.write("****>>>It allows quick money transfer****")
        st.write("****>>>The app can be used 24/7****")
    col3,col4 = st.columns(2)
    with col3:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.header("Indai's Best Transaction APP")
        st.write("****User-friendly interface: PhonePe has a simple and intuitive user interface that makes it easy for users to navigate and make payments.****")
        st.write("****Wide acceptability: PhonePe is widely accepted across various merchants and service providers in India, which makes it convenient for users to use it for various transactions****")
    with col4:
        st.image(Image.open(r"F:\new floder\Phonepay.jpg"))
        



elif select=="DATA EXPLORATION":
    
    tab1, tab2, tab3 = st.tabs(["AGGREGATED_ANALYSIS", "MAP ANALYSIS", "TOP_ANALYSIS"])
    
    with tab1:
        method = st.radio("**Select the Analysis Method**",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year**", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())

            df_agg_insur_Y= Aggre_insurance_Y(Aggre_insurance,years)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("**Select the Quarter**", df_agg_insur_Y["Quarter"].min(), df_agg_insur_Y["Quarter"].max(),df_agg_insur_Y["Quarter"].min())

            Aggre_insurance_Y_Q(df_agg_insur_Y, quarters)
            
        
        elif method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year**", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())

            df_agg_tran_Y= Aggre_insurance_Y(Aggre_transaction,years)
           
           # Select the State for Analyse the Transaction type
            col1,col2 =st.columns(2)
            with col1:
                states= st.selectbox("**Select the State**",df_agg_tran_Y["States"].unique())

            Aggre_Transaction_type( df_agg_tran_Y, states)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("**Select the Quarter**", df_agg_tran_Y["Quarter"].min(), df_agg_tran_Y["Quarter"].max(),df_agg_tran_Y["Quarter"].min())

            df_agg_tran_Y_Q = Aggre_insurance_Y_Q(df_agg_tran_Y, quarters)
            
            col1,col2 =st.columns(2)
            with col1:
                states= st.selectbox("**Select the State_quater**",df_agg_tran_Y_Q["States"].unique())

            Aggre_Transaction_type(df_agg_tran_Y_Q, states)
            
            
            
       
        elif method == "User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year**", Aggre_user["Years"].min(), Aggre_user["Years"].max(),Aggre_user["Years"].min())

            Agg_user_y= Aggre_user_plot1(Aggre_user,years)
            
            col1,col2= st.columns(2)
            with col1:
                seecetd_quarters= st.slider("**Select the Quarter**",Agg_user_y["Quarter"].min(), Agg_user_y["Quarter"].max(),Agg_user_y["Quarter"].min())

            Agg_user_y_q = aggre_user_plot_2(Agg_user_y, seecetd_quarters)
            
            col1,col2 =st.columns(2)
            with col1:
                states= st.selectbox("**Select the State1**",Agg_user_y_q["States"].unique())

            Agg_user_plot_3(Agg_user_y_q,states)
            
            
            
            
            
        
    with tab2:
        method2 = st.radio("Select the Method",["Map Insurance", "Map Transaction", "Map User"])
        
        if method2 == "Map Insurance":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year_map**",Map_insurance["Years"].min(), Map_insurance["Years"].max(),Map_insurance["Years"].min())

            map_insu_tran_Y= Aggre_insurance_Y(Map_insurance,years)
            
            col1,col2 =st.columns(2)
            with col1:
                states= st.selectbox("**Select the State_mi**",map_insu_tran_Y["States"].unique())

            Map_insu_District( map_insu_tran_Y, states)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("**Select the Quarter_map**", map_insu_tran_Y["Quarter"].min(), map_insu_tran_Y["Quarter"].max(),map_insu_tran_Y["Quarter"].min())

            map_insu_tran_Y_Q = Aggre_insurance_Y_Q(map_insu_tran_Y, quarters)
            
            col1,col2 =st.columns(2)
            with col1:
                states= st.selectbox("**Select the State_map**",map_insu_tran_Y_Q["States"].unique())

            Map_insu_District(map_insu_tran_Y_Q, states)
            
            
        elif method2 == "Map Transaction":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year_map**",Map_transaction["Years"].min(), Map_transaction["Years"].max(),Map_transaction["Years"].min())

            map_trans_tran_Y= Aggre_insurance_Y(Map_transaction,years)
            
            col1,col2 =st.columns(2)
            with col1:
                states= st.selectbox("**Select the State_mi**",map_trans_tran_Y["States"].unique())

            Map_insu_District( map_trans_tran_Y, states)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("**Select the Quarter_map**", map_trans_tran_Y["Quarter"].min(),map_trans_tran_Y["Quarter"].max(),map_trans_tran_Y["Quarter"].min())

            map_trans_tran_Y_Q = Aggre_insurance_Y_Q(map_trans_tran_Y, quarters)
            
            col1,col2 =st.columns(2)
            with col1:
                states= st.selectbox("**Select the State_map**",map_trans_tran_Y_Q ["States"].unique())

            Map_insu_District(map_trans_tran_Y_Q , states)
        
        
        elif method2 == "Map User":
            
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year_us**",Map_user["Years"].min(), Map_user["Years"].max(),Map_user["Years"].min())

            map_user_Y= map_user_plot_1(Map_user,years)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("**Select the Quarter_us**", map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())

            map_user_Y_Q =  map_user_plot_2(map_user_Y, quarters)
            
            
            col1,col2 =st.columns(2)
            with col1:
                states= st.selectbox("**Select the State_us**",map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q,states)
            
        
    with tab3:
        method3 = st.radio("Select the Method",["Top Insurance", "Top Transaction", "Top User"])
        
        if method3 == "Top Insurance":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year_ti**",Top_insurance["Years"].min(), Top_insurance["Years"].max(),Top_insurance["Years"].min())

            Top_insu_tran_Y= Aggre_insurance_Y(Top_insurance,years)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("**Select the State_t**",Top_insu_tran_Y["States"].unique())

            top_insurance_plot_1(Top_insu_tran_Y,states)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("**Select the Quarter_t**", Top_insu_tran_Y["Quarter"].min(),Top_insu_tran_Y["Quarter"].max(),Top_insu_tran_Y["Quarter"].min())

            Top_insu_tran_Y_q = Aggre_insurance_Y_Q(Top_insu_tran_Y, quarters)
            
        elif method3 == "Top Transaction":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year_tt**",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())

            Top_trans_tran_Y= Aggre_insurance_Y(Top_transaction,years)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("**Select the State_tt**",Top_trans_tran_Y["States"].unique())

            top_insurance_plot_1(Top_trans_tran_Y,states)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("**Select the Quarter_tt**", Top_trans_tran_Y["Quarter"].min(),Top_trans_tran_Y["Quarter"].max(),Top_trans_tran_Y["Quarter"].min())

            Top_trans_tran_Y_Q = Aggre_insurance_Y_Q(Top_trans_tran_Y, quarters)
            
        elif method3 == "Top User":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year_tu**",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())

            Top_user_Y= top_user_plot_1(Top_user,years)
            
            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("**Select the State_tu**",Top_user_Y["States"].unique())

            top_user_plot_2(Top_user_Y,states)
            
# chart visualization part
# questions and visualisation part using streamlit part
elif select== "CHART VISUALIZATION":
    questions = st.selectbox("Select the Questions",["1.Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Agrregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Registered user of Top User",
                                                    "11. Brands of Agrregated User",
                                                    "12. Districts analysis of Map Transaction",
                                                    "13. Transaction Type of Aggregated Transaction",
                                                    ])
        
    if questions == "1.Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        
        st.subheader("TRASACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif questions == "2. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        
        st.subheader("TRASACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif questions == "3. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        
        st.subheader("TRASACTION COUNT")
        top_chart_transaction_count("top_insurance")
        

    elif questions == "4. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        
        st.subheader("TRASACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif questions == "5. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        
        st.subheader("TRASACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif questions == "6. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        
        st.subheader("TRASACTION COUNT")
        top_chart_transaction_count("top_transaction")
    elif questions == "7. Transaction Count of Agrregated User":
        
        st.subheader("TRASACTION COUNT")
        top_chart_transaction_count("aggregated_user")
        
    elif questions == "8. Registered users of Map User":
        
        states = st.selectbox("Select the state",Map_user["States"].unique())
        
        st.subheader("REGISTERED USER")
        top_chart_registered_user("map_user",states)
            
    elif questions == "9. App opens of Map User":
        
        states = st.selectbox("Select the state_app",Map_user["States"].unique())
        
        st.subheader("APP OPENS")
        top_chart_appopens("map_user",states)    
           
    elif questions == "10. Registered user of Top User":
        
        st.subheader("REGISTERED USER")
        top_chart_registered_user1("top_user")    
        
    elif questions == "11. Brands of Agrregated User":
        
        st.subheader("BRANDS")
        top_chart_brands("aggregated_user")
        
    elif questions == "12. Districts analysis of Map Transaction":
    
        states = st.selectbox("Select the state_dis",Map_transaction["States"].unique())
        
        st.subheader("DISTRICTS")
        top_chart_district("map_transaction",states)
        
    elif questions == "13. Transaction Type of Aggregated Transaction":
    
        states = st.selectbox("Select the state_trans",Aggre_transaction["States"].unique())
        
        st.subheader("TRANSACTION_TYPE")
        top_chart_transaction_type("aggregated_transaction",states)
