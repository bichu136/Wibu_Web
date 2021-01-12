import pandas as pd

def read_csv(csv_path):
    data = pd.read_csv(csv_path)
    return DataManager(data)

class DataManager():
    num_row= 8
    num_col=4
    def __init__(self,DataFrame):
        self.Data = DataFrame
        f_mapper = open('mapping_category.txt',encoding='utf-8').readlines()
        self.__mapper = {i.strip().split('|')[0]: i.strip().split('|')[1] for i in f_mapper}
        self.__mapper_reverse = {i.strip().split('|')[1]: i.strip().split('|')[0] for i in f_mapper}
        self.__invert_mapper = {i.strip().split('|')[1]: i.strip().split('|')[2] for i in f_mapper}
        self.Data = self.Data.sort_values(by='aired_str',ascending=False)
    def __get_genres(self,x):
        _x = x[['genre_Comedy','genre_Sci-Fi','genre_Romance','genre_Adventure','genre_Action','genre_School','genre_Drama','genre_Slice of Life','genre_Mecha','genre_Supernatural']]
        print(_x)
        genres_list = _x.columns[_x.eq(True).any()]
        result = []
        for i in genres_list:
            print(i)
            result.append((self.__invert_mapper[i.split('_')[1]],self.__mapper_reverse[i.split('_')[1]]))
        return result
    def get_anime_info_by_name(self,film_name):
        x = self.Data[self.Data['title']==film_name]
        title =  x['title'].iloc[0]
        genres = self.__get_genres(x)
        episodes = x['episodes'].iloc[0]
        # content = x['content']
        year=x['aired_str'].iloc[0].split('-')[0]
        return title,genres,episodes,year

    def __max_page(self,df):
        l = len(df)
        if l% (DataManager.num_col*DataManager.num_row)==0:
            return l//(DataManager.num_col*DataManager.num_row)
        else:
            return l//(DataManager.num_col*DataManager.num_row) +1
    def __get_rows(self,url_D,num_row,num_col,p):
        r=[]
        while(r==[] and p!=0):
            r = [
                [
                [
                url_D['title'].iloc[num_row*num_col*(p-1)+j+i*num_col],
                url_D['image_url'].iloc[num_row*num_col*(p-1)+j+i*num_col]
                ] 
                for j in range(num_col) if num_row*num_col*(p-1)+j+i*num_col < len(url_D)
                ] 
                for i in range(num_row) 
                ]
            p-=1
        return r


    def get_rows_and_list_page_for_list(self,page):
        url_D = self.Data[["image_url","title"]]
        p = int(page)
        rows = self.__get_rows(url_D,DataManager.num_row,DataManager.num_col,p)
        list_page= self.__create_list_page(url_D,p,'/list')
        return rows,list_page


    def get_rows_and_list_page_for_category(self,category_name,page):
        data8 = self.Data[self.Data["genre_"+self.__mapper[category_name]]==True]
        p = int(page)
        url_D = data8[["image_url","title"]]
        rows = self.__get_rows(url_D,DataManager.num_row,DataManager.num_col,p)
        list_page= self.__create_list_page(url_D,p,'/category/'+category_name)
        return rows,list_page


    def __create_list_page(self,URL_D,page,page_path):
        max_page = self.__max_page(URL_D)
        r = [[i,'clickable',page_path+'/'+str(i)] for i in range(page-2,page+3) if i>0 and i<max_page]
        for i in r:
            if i[0]==page:
                i[1]='onit'
        if r[0][0]==1 and r[0][1]=='onit':
            return [['previous','disable',page_path+'/'+str(page-1)]]+r+[['next','clickable',page_path+'/'+str(page+1)]]
        else :
            return [['previous','clickable',page_path+'/'+str(page+1)]]+r+[['next','clickable',page_path+'/'+str(page+1)]]

    def get_rows_and_list_page_for_year(self,year,page):
        data8 = self.Data['premiered'].str.contains(str(year)).any()
        print(data8)
        url_D = self.Data[["image_url","title"]]
        p = int(page)
        rows = self.__get_rows(url_D,DataManager.num_row,DataManager.num_col,p)
        list_page= self.__create_list_page(url_D,p,'/year/'+year)
        return rows,list_page