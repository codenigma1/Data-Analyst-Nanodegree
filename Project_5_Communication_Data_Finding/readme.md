# Project 5: Ford GoBike System Data

## by Vaibhav Khobragade


## Dataset

> 1818202 obeservation and 19 variable that help me get insight and achive the goal.


### These are main feature(s) of interest in the dataset?

1. **`duration_sec`.** that bike riding the duration in seconds. 
2. **`start_station_latitude`, `start_station_longitude`, `end_station_latitude`, and `end_station_longitude`.** that explain the journey of the rider from one place to other
3. **`user_type`** has 'subscriber' and 'customer'.
4. **`bike_share_for_all_trip`**  whether share or not. Also, people get discount if they have low income.
5. **`day`,  which day most bike riding will be done, `hours` timing of riding the most will be done, and same for the `month`**
6.  **`start_city`** of the lacation and **`end_city`** of the loacation of the bike.

Final dataset after assesing and cleaning.

**`duration_sec`**                        int64
**`start_time`**                 datetime64[ns]
**`end_time`**                   datetime64[ns]
**`start_station_id`**                    int64
**`start_station_name`**                 object
**`start_station_latitude`**            float64
**`start_station_longitude`**           float64
**`end_station_id`**                      int64
**`end_station_name`**                   object
**`end_station_latitude`**              float64
**`end_station_longitude`**             float64
**`bike_id`**                             int64
**`user_type`**                        category
**`bike_share_for_all_trip`**              bool
**`month`**                              object
**`day`**                              category
**`hour`**                                int64
**`start_city`**                       category
**`end_city`**                         category


### Assessing and Cleaning data:

> **`start_time`** and **`end_time`** should be **datetime** format

> **`start_station_id`** and **`end_station_id`** should be **int64** format

> **`user_type`** and **`bike_share_for_all_trip`** should be **category** format

> We extract some hidden variable from the **`start_date`** columns that we will add **`hour, day, and month`**. Then convert them into categorical datatype.

> Also, we add some city labels with the help of **latitude** and **logitude**. Also make them categorical datatype.


## Summary of Findings

> San Fransciso has highest to used go bikes among the cities. But we saw the result of bike sharing pretty low due to more station avaliable. So people don't need to bother for pickup the bikes. Also, bizzare result only `subscriber` has been type sharing the bikes bacause of it may office, shop and busniess related work happen that we saw in `weekdays` result.

> We saw the rush hours at 8 to 9'O clock in the morning and  at 16 to 17'O clock in the evening those timing insinuate busniess and office hour tranvelling. Also, In the weekends, Customer average `duration` time surprisingly higher than subscriber in each days. Moreover, busniess days average trip timing less than weekends that we can predict people love to go long dive, picnic, and meet relatives.


## Key Insights for Presentation

> One key insight of the presentation that we predicted in the folium map customer mean time may be greter than subscriber that result is true saw in the point plot mean estimation. Customer drive longer than subscriber.