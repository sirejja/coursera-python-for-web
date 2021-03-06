use test;
set names utf8;

-- 1. Выбрать все товары (все поля)
select * 
from store;

-- 2. Выбрать названия всех автоматизированных складов
select name 
from store 
where is_automated = 1;

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total) 
from sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select distinct store_id 
from sale 
where total is not null;


-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select distinct store_id 
from sale 
where total is null;

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
SELECT name, avg(total/quantity) 
from sale 
	join product using(product_id)
group by name;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select name 
from product 
	natural join sale 
group by product_id having count(distinct store_id) = 1

-- 8. Получить названия всех складов, с которых продавался только один продукт
select name 
from store 
	natural join sale 
group by store_id having count(distinct product_id) = 1

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * 
from sale 
where total = (select max(total) from sale);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date 
from sale 
group by date 
order by sum(total) DESC, date ASC LIMIT 1
