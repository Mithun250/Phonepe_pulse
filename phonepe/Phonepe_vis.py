import pandas as pd
import mysql.connector
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.graph_objects as go

st.set_page_config(
                   layout="wide", 
                   page_title= "Phonepe Pulse Data Visualization",
                   page_icon= "phone-fill",
                   initial_sidebar_state= "expanded",
)

mithun=mysql.connector.connect(host='localhost',user='root',password='Nuhtim25*',database='phonepe_pulse')
suresh=mithun.cursor()


select = option_menu(menu_title="Phonepe Pulse Data Visualization",
                           options=["About","Home","Explore Data","Analyse"],
                           menu_icon="phone-fill",
                           icons=["arrow-down-circle-fill","house","toggles","search"],
                           default_index=0,
                           orientation="horizontal",

)

if select == "About":
    col1,col2, = st.columns(2)
    col1.image(Image.open("C:/Users/91915/Downloads/Phonepe_image2.png"),width = 300)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("C:/Users/91915/Downloads/phonepe.mp4") 
    st.write("---")

    col1,col2 = st.columns(2)
    with col1:
        st.title("THE BEAT OF PHONEPE")
        st.write("---")
        st.subheader("Phonepe became a leading digital payments company")
        st.image(Image.open("C:/Users/91915/Downloads/about_phonepe.jpg"),width = 400)
        with open("C:/Users/91915/Downloads/about_phonepe1.png","rb") as f:
            data = f.read()
        st.download_button("DOWNLOAD REPORT",data,file_name="annual report.pdf")

    with col2: 
        st.image(Image.open("C:/Users/91915/Downloads/about_phonepe1.png"),width = 800)


if select=="Home":
    col1,col2 = st.columns(2)
    with col1:
        st.image(Image.open("C:/Users/91915/Downloads/phonepe_beat.jpg"),width = 500)        
    with col2:
        st.title(':violet[PHONEPE PULSE DATA VISUALISATION]')
        st.subheader(':violet[Phonepe Pulse]:')
        st.write('PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.')
        st.subheader(':violet[Phonepe Pulse Data Visualisation]:')
        st.write('Data visualization refers to the graphical representation of data using charts, graphs, and other visual elements to facilitate understanding and analysis in a visually appealing manner.'
                 'The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.')
        st.markdown("## :violet[Done by] : MITHUN S")
        st.markdown("[Inspired from](https://www.phonepe.com/pulse/)")
        st.markdown("[Githublink](https://github.com/Mithun250/Phonepe_pulse)")
    st.write("---")        


if select == "Explore Data":
    st.markdown("## Explore Data")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    col1= st.columns(2)[0]
    with col1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    col1,col2 = st.columns(2)

    if Type == "Transactions":
        
        with col1:
            st.markdown("### :violet[Top 10 States on Transaction Amount]")
            suresh.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df_state = pd.DataFrame(suresh.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])

            fig_state = px.bar(df_state, x='State', y='Total_Amount',
                                text='Transactions_Count',
                                color='Total_Amount',
                                color_continuous_scale=px.colors.sequential.Agsunset,

                                )

            fig_state.update_traces(textposition='outside', texttemplate='%{text}', textfont_size=12)
            fig_state.update_layout(xaxis_title='State', yaxis_title='Total Amount')
            st.plotly_chart(fig_state, use_container_width=True)

                    

        with col2:

            st.markdown("## :violet[Top Payment Type]")
            suresh.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
            df = pd.DataFrame(suresh.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

            fig = px.bar(df,
                        text='Total_amount',
                        x="Transaction_type",
                        y="Total_Transactions",
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_traces(textposition='outside', texttemplate='%{text}', textfont_size=12)
            fig.update_layout(xaxis_title='Transaction Type', yaxis_title='Total Transactions')
            st.plotly_chart(fig, use_container_width=False)  
        
        col3,col4 =st.columns(2)
        with col3:    
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            suresh.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(suresh.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r"C:\Users\91915\OneDrive\Desktop\phonepe\Statenames.csv")
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
        
        with col4:
            st.markdown("## :violet[State]")
            suresh.execute(f"SELECT state, SUM(Transaction_amount) AS Total_Transaction_Amount FROM agg_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY state ORDER BY Total_Transaction_Amount DESC")
            df1 = pd.DataFrame(suresh.fetchall(), columns=['State', 'Total_Transaction_Amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.State = df2

            fig = px.choropleth(
                df1,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                title="Transaction Amount",
                color='Total_Transaction_Amount',
                color_continuous_scale='sunset'
            )

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)



        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        suresh.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(suresh.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)


    if Type == "Users":
        
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        suresh.execute(f"select state, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(suresh.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv(r"C:\Users\91915\OneDrive\Desktop\phonepe\Statenames.csv")
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        suresh.execute(f"select State,year,quarter,District,sum(Registereduser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df = pd.DataFrame(suresh.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

        col1, col2 = st.columns([1, 1], gap="medium")

        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2, 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                suresh.execute(
                    f"SELECT brands, SUM(count) AS Total_Count, AVG(percentage)*100 AS Avg_Percentage FROM agg_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY brands ORDER BY Total_Count DESC LIMIT 10")
                df = pd.DataFrame(
                    suresh.fetchall(), columns=["Brand", "Total_Users", "Avg_Percentage"])

                fig = px.bar(
                    df,
                    y="Total_Users",
                    x="Brand",
                    color="Avg_Percentage",
                    color_continuous_scale=px.colors.sequential.Agsunset,
                    title="Top 10 Brands on Users",)
                st.plotly_chart(fig, use_container_width=True)


    
if select=="Analyse":
    st.title(':violet[Data Analysis]')
    options = ["--select--",

               "Top 10 Districts based on the Transaction Amount",
               "Least 10 Districts based on the Transaction Amount",
                "Top 10 States and Districts based on Registered Users",
               "Least 10 States and Districts based on Registered Users",
                "Top 10 Districts based on the Transaction count",
                "Least 10 Districts based on the Transaction count"]
    
    select = st.selectbox(":violet[Select the option]",options)

    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    col1= st.columns(2)[0]
    with col1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4) 


    if Type == "Users":
        if select == "Top 10 Districts based on the Transaction Amount" or select == "Least 10 Districts based on the Transaction Amount" or select=="Top 10 Districts based on the Transaction count" or select == "Least 10 Districts based on the Transaction count":
            st.warning("No data available for this combination of Type and Question.")
        elif select == "Top 10 States and Districts based on Registered Users" :
            col1,col2=st.columns(2)
            with col1:
                st.markdown("### :violet[District]")
                suresh.execute(f"SELECT district, SUM(RegisteredUser) AS Total_Users FROM map_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY district ORDER BY Total_Users DESC LIMIT 10")
                
                df = pd.DataFrame(suresh.fetchall(), columns=["District", "Total_Users"])
                df.Total_Users = df.Total_Users.astype(float)

                fig = px.bar(
                    df,
                    y="Total_Users",
                    x="District",
                    color="Total_Users",
                    color_continuous_scale=px.colors.sequential.Agsunset,
                    title="Top 10 Districts on Users",
                )
                st.plotly_chart(fig, use_container_width=True)
                st.write(df)

        
            with col2:
                st.markdown("### :violet[State]")
                suresh.execute(f"SELECT state, SUM(Registereduser) AS Total_Users FROM map_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY state ORDER BY Total_Users DESC LIMIT 10")
                df = pd.DataFrame(suresh.fetchall(), columns=["State", "Total_Users"])

                fig = px.pie(
                    df,
                    values="Total_Users",
                    names="State",
                    title="Top 10 States by Users",
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hole=0.4
                )
                fig.update_traces(textposition="inside", textinfo="percent+label")
                st.plotly_chart(fig, use_container_width=True)
                st.write(df)

        elif select == "Least 10 States and Districts based on Registered Users":

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### :violet[District]")
                suresh.execute(f"SELECT district, SUM(RegisteredUser) AS Total_Users FROM map_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY district ORDER BY Total_Users ASC LIMIT 10")
                df = pd.DataFrame( suresh.fetchall(), columns=["District", "Total_Users"])
                df.Total_Users = df.Total_Users.astype(float)

                fig_district = px.pie(
                    df,
                    values="Total_Users",
                    names="District",
                    title="Least 10 Districts on Users",
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                )

                fig_district.update_traces(textposition="inside", textinfo="percent+label")
                st.plotly_chart(fig_district, use_container_width=True)
                st.write(df)

            with col2:
                st.markdown("### :violet[State]")
                suresh.execute(f"SELECT state, SUM(Registereduser) AS Total_Users FROM map_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY state ORDER BY Total_Users ASC LIMIT 10")
                df = pd.DataFrame(suresh.fetchall(), columns=["State", "Total_Users"])

                fig_state = px.pie(
                    df,
                    values="Total_Users",
                    names="State",
                    title="Least 10 States by Users",
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hole=0.4
                )

                fig_state.update_traces(textposition="inside", textinfo="percent+label")

                st.plotly_chart(fig_state, use_container_width=True)
                st.write(df)



        elif select == "Top 10 Districts based on the Transaction count" or select == "Least 10 Districts based on the Transaction count":
            st.warning("No data available for this combination of Type and Question.")
    else:
        if select=="Top 10 Districts based on the Transaction Amount":
            suresh.execute(f"select district, sum(Count) as Total_Transactions_Count, sum(Amount) as Total_Amount from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total_Amount desc limit 10")
            df_district = pd.DataFrame(suresh.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

            fig_district = px.bar(df_district, x='District', y='Total_Amount',
                                    text='Transactions_Count',
                                    title='Top 10 Districts on Transaction Amount',
                                    color='Total_Amount',
                                    color_continuous_scale=px.colors.sequential.Agsunset,

                                    ) 

            fig_district.update_traces(textposition='outside', texttemplate='%{text}', textfont_size=12)
            fig_district.update_layout(xaxis_title='District', yaxis_title='Total Amount')
            st.plotly_chart(fig_district, use_container_width=True)
            st.write(df_district)
        
        elif select == "Least 10 Districts based on the Transaction Amount":

            suresh.execute(f"SELECT district, SUM(Amount) AS Total_Amount FROM map_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY district ORDER BY Total_Amount ASC LIMIT 10")
            df_district = pd.DataFrame(suresh.fetchall(), columns=['District', 'Total_Amount'])

            fig_district = px.bar(
                df_district, x='District', y='Total_Amount',
                text='Total_Amount',
                title='Least 10 Districts based on Transaction Amount',
                color='Total_Amount',
                color_continuous_scale=px.colors.sequential.Agsunset,
            )

            fig_district.update_traces(textposition='outside', texttemplate='%{text}', textfont_size=12)
            fig_district.update_layout(xaxis_title='District', yaxis_title='Total Amount')
            st.plotly_chart(fig_district, use_container_width=True)
            st.write(df_district)


        elif select == "Top 10 Districts based on the Transaction count":

            suresh.execute(f"SELECT district, SUM(Count) AS Total_Transactions_Count, SUM(Amount) AS Total_Amount FROM map_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY district ORDER BY Total_Transactions_Count DESC LIMIT 10")
            df_district = pd.DataFrame(suresh.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

            fig_district = px.bar(
                df_district, x='District', y='Transactions_Count',
                text='Transactions_Count',
                title='Top 10 Districts based on Transaction count',
                color='Transactions_Count',
                color_continuous_scale=px.colors.sequential.Agsunset,
            )

            fig_district.update_traces(textposition='outside', texttemplate='%{text}', textfont_size=12)
            fig_district.update_layout(xaxis_title='District', yaxis_title='Total Transaction Count')
            st.plotly_chart(fig_district, use_container_width=True)
            st.write(df_district)


        elif select == "Least 10 Districts based on the Transaction count":

            suresh.execute(f"SELECT district, SUM(Count) AS Total_Transactions_Count, SUM(Amount) AS Total_Amount FROM map_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY district ORDER BY Total_Transactions_Count ASC LIMIT 10")
            df_district = pd.DataFrame(suresh.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

            fig_district = px.bar(
                df_district, x='District', y='Transactions_Count',
                text='Transactions_Count',
                title='Least 10 Districts based on Transaction count',
                color='Transactions_Count',
                color_continuous_scale=px.colors.sequential.Agsunset,
            )

            fig_district.update_traces(textposition='outside', texttemplate='%{text}', textfont_size=12)
            fig_district.update_layout(xaxis_title='District', yaxis_title='Total Transaction Count')
            st.plotly_chart(fig_district, use_container_width=True)
            st.write(df_district)



      