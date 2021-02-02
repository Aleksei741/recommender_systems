def prefilter_items(data_train, 
                    item_features=None,
                    drop_popular_amount=50, 
                    drop_unpopular_amount=50, 
                    uninteresting_department_list=None,
                    low_price=1,
                    high_price=100):
          
    popularity_table = data_train.groupby('item_id')['quantity'].sum().reset_index()
    popularity_table.rename(columns={'quantity': 'n_sold'}, inplace=True)
    popularity_table.sort_values('n_sold', ascending=True, inplace=True)
    
    # Уберем самые популярные 
    top_list = popularity_table.head(drop_popular_amount).item_id.tolist()
    data_train.loc[data_train['item_id'].isin(top_list), 'item_id'] = 999999    
    # Уберем самые непопулряные 
    bot_list = popularity_table.tail(drop_unpopular_amount).item_id.tolist()
    data_train.loc[data_train['item_id'].isin(bot_list), 'item_id'] = 999999
    # Уберем товары, которые не продавались за последние 12 месяцев
    # Нет инфы. Времятранспортировки это я так понял не оно
    # Уберем не интересные для рекоммендаций категории (department)
    if uninteresting_department_list and item_features:
        uninteresting_list = uninteresting_list = item_features.loc[item_features['department'].\
                                                                    isin(uninteresting_department_list), :]\
                                                                    ['item_id'].unique().tolist()
        data_train.loc[data_train['item_id'].isin(uninteresting_list), 'item_id'] = 999999
    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб. 
    data_train['price'] = data_train['sales_value'] / data_train['quantity']
    data_train.loc[data_train['quantity']==0, ['price']]=data_train['sales_value']
    data_train.loc[data_train['price'] < low_price, 'item_id'] = 999999
    # Уберем слишком дорогие товары
    data_train.loc[data_train['price'] > high_price, 'item_id'] = 999999
	
	# Оставим только 5000 самых популярных товаров
    popularity = data_train.groupby('item_id')['quantity'].sum().reset_index()
    popularity.rename(columns={'quantity': 'n_sold'}, inplace=True)
    top_5000 = popularity.sort_values('n_sold', ascending=False).head(5000).item_id.tolist()
    #добавим, чтобы не потерять юзеров
    data_train.loc[~data_train['item_id'].isin(top_5000), 'item_id'] = 999999 

    return data_train

def postfilter_items():
    pass