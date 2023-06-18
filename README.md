# Baidu migration python crawler

> Crawl Baidu migration data, divided into 3 types: city, province, country

## Description:
Use python to crawl the population flow data in the Baidu migration platform: http://qianxi.baidu.com/, and uncomment the corresponding code according to the required type.
The crawled content will be saved as an Excel file in the **move_in**, **move_out** folders in the root directory of the code

## Terms and Conditions:
1. **Path**: Please modify the absolute path before use

2. **Date**: Please modify the date in the [migration_all_date] function (note that the left interval includes, and the right interval does not include)

3. **City interval**: Since there is no asynchronous operation set during crawling, it will result in a timeout (time_out) if too many cities are crawled at one time.
Therefore, it is recommended to crawl between partitions, you can copy multiple source program files, and start crawling multiple times in different intervals at the same time

4. **Run**: Run the main.py file directly after making sure the above information is correct
## required python packages
- requests
- xlwt

## crawled data
- [【2020-01-01—2020-02-14】City-level migration and migration data](https://mochenzx.lanzoux.com/iRsLUhqfm3i)
