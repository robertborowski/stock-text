import psycopg2
from psycopg2 import Error

def select_users_received_text_this_week_function(connection_postgres, cursor):
  """Returns: Pulls the user email info and texts they've received this week"""
  try:
    cursor.execute("WITH subquery1 AS(SELECT sent.tracking_sent_text_date_time,login.email,login.first_name,stock.symbol,news.google_news_link,CONCAT(login.email,stock.symbol)AS concat_field,login.uuid FROM sent_texts_table AS sent LEFT JOIN login_information_table AS LOGIN ON sent.fk_uuid_email=login.uuid LEFT JOIN stock_tracking_table AS stock ON sent.fk_uuid_symbol=stock.uuid LEFT JOIN stock_news_links_table AS news ON news.pk_symbol=stock.symbol WHERE sent.tracking_sent_text_date_time>=DATE(NOW())-5 ORDER BY sent.tracking_sent_text_date_time,login.email)SELECT DISTINCT concat_field,subquery1.email,subquery1.first_name,subquery1.symbol,subquery1.google_news_link,subquery1.uuid FROM subquery1")
    result_list = cursor.fetchall()
    return result_list
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      result_list = 'none'
      return result_list