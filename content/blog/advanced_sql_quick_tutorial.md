---
title: "Quick Tutorial to Advanced SQL"
date: 2021-12-23T18:03:05-06:00
draft: false
---

Everybody knows the basics, and yet the more advanced tricks are only learned when we need it. Here is a systematic overview of the more common patterns in what's usually considered "advanced SQL". We will use PostgreSQL syntax as an example (MySQL, and T-SQL are similar enough), and start from the easier ones, but quickly advance to more difficult ones.

#### Set Up

This is intended for interactive practice. Once a Postgre server is setup, insert some data using [this script](https://github.com/yulunz/sql_tutorial/blob/main/prepare_data.sql).

#### How many cats are in this table?

```
select count(1) from cats;
```

#### How many kinds of cats are in this table?

```
select count(distinct kind) from cats;
```

#### How many cats are `Grey`?

```
select count(1) from cats where color = 'Grey';
```

#### How many cats' names end with "e"?

```
select count(1) from cats where name like '%e';
```

#### What's the name of the oldest cat, and how old is it?

```
select name, age from cats order by age desc limit 1;
```

#### Which is the heaviest Maine Coon, and how heavy is it?

```
select
  name, weight
from cats
where kind = 'Maine Coon'
order by weight desc
limit 1;
```

#### Which cat is the heaviest un-neutered cat?

```
select name from cats where is_neutered is FALSE order by weight desc limit 1;
```

#### What are all neutered "Domestic", and "Persian" cats?

```
select * from cats
where
  is_neutered is TRUE and
  kind in ('Domestic', 'Persian');
```

#### What are the average weights per kind? Can you order them from most heavy on average and least heavy on average?

```
select kind, avg(weight) from cats group by 1 order by avg desc;
```

#### What are the kinds of cats of which the minimum weight is more than 7 lbs?

```
select kind, min(weight) from cats group by 1 having min(weight) > 7;
```

#### How many cats are added each year?

```
select extract(year from added_time), count(1) from cats group by 1;
```

#### List the cat names and their owner names by joining with the "owners" table.

```
select
  c.name as cat_name,
  o.name as owner_name
from cats c
left join owners o
on c.owner = o.name;
```

#### List all cats whose best friend is of a different color.

```
select
  c1.name, c1.color, c1.best_friend, c2.color as best_friend_color
from cats c1
left join cats c2
on c1.best_friend = c2.name
where c1.color != c2.color;
```

#### Which kind has the largest range of weights?

```
with w as (
  select kind, max(weight)-min(weight) as range
  from cats
  group by 1
)
select * from w order by range desc limit 1;
```

#### What's the percentage of cats that are neutered?

In PostgreSQL, you can cast an integer type to float by appending `::float` to it. In other SQL variant, you might be able to do so by `* 1.0`.

```
select
  sum(
    case
      when is_neutered is TRUE then 1
      else 0
    end
  )::float / count(1) as pct_neutered
from cats;
```

#### Which is the heaviest cat per kind?

Here is a slightly challenging one. First we need to find the maximum weight per kind. This is done by using the `max` function over each "window" partitioned by `kind`. After having the max's we just need to select only those having their weights equal to the max of that kind.

```
select kind, name, weight
from (
  select
    kind, name, weight,
    max(weight) over (partition by kind) as max_weight
  from cats
) t
where weight = max_weight;
```

Alternatively,

```
with t as (
  select
    kind, name, weight,
    max(weight) over (partition by kind) as max_weight
  from cats
)
select kind, name, weight from t
where weight = max_weight;
```

#### Which cat was added the earliest per kind?

Same trick as above.

```
select kind, name, added_time from (
  select
    kind, name, added_time,
    min(added_time) over (partition by kind) as min_added
  from cats
) t
where min_added = added_time;
```

#### Which cat was added before Billie?

We need to give a ranking number per `added_time`, then find the rank of Billie, and find the cat that has that rank minus 1.

```
with ranked as (
  select
    *,
    row_number() over (order by added_time asc) as rank
  from cats
)
select
  name
from ranked
where rank = (
  select rank-1 from ranked where name = 'Billie'
);
```
Alternatively we can use the `lag` function on name.

```
select last from (
  select
    name,
    lag(name) over (order by added_time asc) as last
  from cats
) t
where name = 'Billie';
```

#### What's the percentage for each color? Replace NULL with "Unknown".

Use `coalesce` function to replace NULL.

```
select
  coalesce(color, 'Unknown') as color,
  count(1)::float/(select count(1) from cats) as percentage
from cats
group by 1;
```

#### What's the percentage of color per kind? Replace NULL with "Unknown".

We need three columns: kind, color, percentage. The percentages for each kind must add up to 100%.

```
with color_ct as (
  select
    kind,
    coalesce(color, 'Unknown') as color,
    count(1) as ct
  from cats
  group by 1, 2
)
select
  kind,
  color,
  ct::float / sum(ct) over (partition by kind) as percentage
from color_ct;
```
