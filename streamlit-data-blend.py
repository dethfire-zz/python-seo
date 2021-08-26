import streamlit as st
import pandas as pd
import seaborn as sns

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<p class="big-font">SEO Data Blender</p>
<b>Directions: </b></ br><ol>
<li>Export Performance data (60 days clicks, impressions, CTR, positon) in Google Search Console. Upload pages.csv from the zip file.</li>
<li>Export Google Analytics Landing Page Data (60 days, 1000 items).</li>
<li>Export Ahrefs Top Pages Data (Full, UTF-8).</li>
<li>Export Screaming Frog Crawl. HTML only.</li></ol>
""", unsafe_allow_html=True)


domain = st.text_input('Your Root Domain URL','ex https://www.yourdomain.com')

get_gsc_file = st.file_uploader("Upload GSC CSV File",type=['csv'])  
get_ga_file = st.file_uploader("Upload GA XLSX File",type=['xlsx'])
get_ahrefs_file = st.file_uploader("Upload ahrefs CSV File",type=['csv'])
get_sf_file = st.file_uploader("Upload SF CSV File",type=['csv'])

if get_gsc_file is not None and get_ga_file is not None and get_ahrefs_file is not None and get_sf_file is not None and get_sf_file is not None:
    st.write("Data upload success :sunglasses:")
    
    # GSC to dataframe
    df_gsc = pd.read_csv(get_gsc_file)
    df_gsc["CTR"] = df_gsc["CTR"].replace({'%':''}, regex=True).astype(float)
    
    # GA to dataframe
    df_ga = pd.read_excel(get_ga_file,'Dataset1')[["Landing Page","Sessions","New Users","Bounce Rate"]]
    df_ga['Landing Page'] = domain + df_ga['Landing Page'].astype(str)
    df_ga["Bounce Rate"] = round(df_ga["Bounce Rate"] * 100).astype(int)
    
    # ahrefs to dataframe
    df_ahrefs = pd.read_csv(get_ahrefs_file)[["# of Keywords","URL"]]
    df_ahrefs.rename(columns={"# of Keywords": "Keywords"}, inplace = True)
    
    # ScreamingFrog to dataframe
    df_sf = pd.read_csv(get_sf_file)[["Address","Title 1", "Word Count","Crawl Depth"]]
    df_sf.rename(columns={"Title 1": "Title"}, inplace = True)
    
    # Join GSC and GA dataframes
    df_gsc_ga = pd.merge(df_gsc, df_ga, left_on='Top Pages', right_on='Landing Page', how='inner')
    
    # Join GSC/GA and ScreamingFrog dataframes
    df_gsc_ga_sf = pd.merge(df_gsc_ga, df_sf, left_on='Top Pages', right_on='Address', how='inner')
    
    # Join GSC/GA/SF and ahrefs dataframes
    df_final = pd.merge(df_gsc_ga_sf, df_ahrefs, left_on='Top Pages', right_on='URL', how='inner')
    
    # Filter final dataframe
    #df_final = df_final[df_final['Page'].str.contains('education') & (df_final['Word Count'] > 1000)]
    df_final.sort_values(by=['Clicks'], ascending=False)
    df_final = df_final[ ['Title'] + ['URL'] + ['Keywords'] + [col for col in df_final.columns if col != 'Title' and col != 'Keywords' and col != 'URL']]
    df_final['URL'] = df_final['URL'].replace({domain:''}, regex=False)
    df_final.drop(['Landing Page', 'Top Pages' ,'Address'], axis=1, inplace=True)
    df_final.reset_index()
    
    cm = sns.light_palette("green",as_cmap=True)
    df_final = df_final.style.background_gradient(cmap=cm)
    
    st.dataframe(df_final)
        
    if st.button("Download Blended Data CSV"):
        df_final.to_csv("Ahrefs-GSC-GA-SF-DataBlend.csv")

st.write('Author: [Greg Bernhardt](https://twitter.com/GregBernhardt4) | Friends: [Rocket Clicks](https://www.rocketclicks.com) and [Physics Forums](https://www.physicsforums.com)')
