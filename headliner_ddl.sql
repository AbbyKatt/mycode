create Table Feeds(
   id Integer primary key autoincrement,
   feeddate date,
   feed string,
   title string,
   blurb string,
   url string);

create Table rClassify(
	id Integer primary key autoincrement,
	classifier string,
	url string,
	feeddate date,
	headline string
);

   
--Clear down
DELETE from Feeds where feed="feedname";
vacuum;
 
 --Dedudplicate URLS
select distinct url,title,blurb from Feeds;
select distinct url,title from Feeds; --less

--Dedup from jack!
select s1.* FROM
(select url,max(date_posted) as date_posted from sample group by url) s2 join
sample s1 on s1.url=s2.url and s1.date_posted=s2.date_posted 


--Jacks awesome dedup as a view
CREATE VIEW vw_FeedsDedup AS
select s1.* FROM
(select url,max(feeddate) as date_posted from Feeds group by url) s2 
join
Feeds s1 on s1.url=s2.url and s1.feeddate=s2.date_posted;

--Interest rates view
create view referencedata.vInterestRates as
  SELECT PARSE_DATE("%d-%b-%y",Date_Changed) as Change_Date,Rate  FROM `datawx.referencedata.rInterestRates`
  order by Change_Date asc
  

--Results  
create table.results.out_Results ASworkflow_uuid:STRING,
solver_uuid:STRING,
solver_name:STRING,
channel_name:STRING,
cURL:STRING,
cClassification:STRING,
cClassifcationConfidence:FLOAT,
cClassificationSecondChoice:STRING,
XTime:DATETIME,
YValue:FLOAT



--Deduplicate table by URL
--select feeddate,feed,blurb,url from referencedata.sFeeds

select uniqURLS.* from
(SELECT url,feed FROM datawx.referencedata.sFeeds
group by url, feed
order by feeddate asc
) uniqURLS
(select url,feeddate from datawx.referencedata.sFeeds
group by url, feeddate
order by feeddate asc
) uniqURLS
  


-- --Todays Dedup
-- --vw_DistinctFeeds
-- select distinct url, feed, title, blurb from `referencedata.sFeeds`
--   where feeddate is not null

-- --Stage 2 get min date of article
-- SELECT url, min(feeddate) as ArticleReleased FROM `datawx.referencedata.sFeeds` 
--   where feeddate is not null
--   group by url
--   order by ArticleReleased asc

--Select first row in group

-- --Stage 2 - stitch Distinct Feeds and Min Date of article
-- select src1.*,src2.ArticleReleased as feeddate from `referencedata.vw_DistinctFeeds` src1
--   join `referencedata.vw_URLArticleReleasedDate` src2 on src1.url=src2.url


-- --Build skeletal deudiplication backbone
-- select url, min(feeddate) as feeddate from `referencedata.sFeeds`
-- group by url
-- order by feeddate asc) uniqURLS


-- left join
-- (select url,feed,min(feeddate), from `referencedata.sFeeds` 
-- group by url,feeddate,feed
-- order by feeddate asc) as uniqFeedName
-- on uniqURLS.url=uniqFeedName.url and uniqURLS.feeddate=uniqFeedName.feeddate

---------------------------------------------------------------------------------------------------------------------------
--Deplication logic from HELL
---------------------------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------------------------
-- --First stage, get distinct URLS and first date/time they were seen in feed (527561)
-- create view referencedata.vw_FeedsDedup0_URL as
-- select url, min(feeddate) as feeddate from `referencedata.sFeeds`
-- group by url
-- order by feeddate asc

-- ---------------------------------------------------------------------------------------------------------------------------
-- --2nd stage, get first feed, title, blurb where unuqie URL appears (535453)
-- create view referencedata.vw_FeedsDedup1_TitleBlurb as
-- select url,title,blurb,min(feeddate) as feeddate from `referencedata.sFeeds`
-- group by url,title,blurb

-- ---------------------------------------------------------------------------------------------------------------------------
-- --3rd stage, get the feed name (655359) << problem here
-- create view referencedata.vw_FeedsDedup3_FeedName as
-- select url,feed,min(feeddate) as feeddate from `referencedata.sFeeds`
-- group by url,feeddate,feed
-- order by feeddate asc

-- WITH summary AS (
--     SELECT p.url, 
--            p.feed, 
--            p.feeddate, 
--            ROW_NUMBER() OVER(PARTITION BY p.url
--                                  ORDER BY p.feeddate DESC) AS rank
--       FROM `referencedata.sFeeds` p)
--  SELECT *
--    FROM summary
--  WHERE rank = 1


-- ---------------------------------------------------------------------------------------------------------------------------
-- --Final stage: join it alllll up (523953)

-- select
--   src1.url,
--   src3.feed,
--   src2.title,
--   src2.blurb,
--   src1.feeddate

-- from referencedata.vw_FeedsDedup0_URL src1
--   join referencedata.vw_FeedsDedup1_TitleBlurb src2 on src1.url=src2.url and src1.feeddate=src2.feeddate
--   join referencedata.vw_FeedsDedup3_FeedName src3 on src1.url=src3.url and src1.feeddate=src3.feeddate
  


---------------------------------------------------------------------------------------------------------------------------
--Deduplication logic from HEAVEN!
create view referencedata.vw_Feeds as
WITH summary AS (
    SELECT p.url, 
           p.feed,
           p.title,
           p.blurb, 
           p.feeddate, 
           ROW_NUMBER() OVER(PARTITION BY p.url
                                 ORDER BY p.feeddate ASC) AS rank
      FROM `referencedata.sFeeds` p)
 SELECT *
   FROM summary
 WHERE rank = 1



---------------------------------------------------------------------------------------------------------------------------
--Helios views

--Basic report on classification metrics
create view results.vw_HeliosClassificationSummary as
SELECT 
  extract(DATE from res.XTime) as XDate,
  res.workflow_uuid,
  res.channel_type,
  res.channel,
  res.cClassification,
  count(*) as RowCount
 FROM `datawx.results.out_Results` res
 group by
 XDate,
 res.workflow_uuid,
 res.channel_type,
 res.channel,
 res.cClassification
 order by XDate

---------------------------------------------------------------
--Manifest View
create view results.vw_Manifest as 
SELECT workflow_uuid, solver_name, channel,channel_type,cClassification, min(XTime) as MinT,max(XTime) as MaxT,count(*) as RecordCount
FROM `datawx.results.out_Results`
group by workflow_uuid, solver_name, channel,channel_type,cClassification
order by workflow_uuid, solver_name, channel,channel_type,cClassification


---------------------------------------------------------------
--BREXIT view
create view referencedata.vw_brexit as
  SELECT * FROM `datawx.referencedata.vw_Feeds` 
  where lower(title) like "%brexit%"
  or blurb like "%brexit%"
  and feeddate is not null
  order by feeddate asc

--Summed up by month
create view results.vw_Brexit_Sentiment as

  SELECT  
    url,
    EXTRACT(year from feeddate) as year,
    EXTRACT(month from feeddate) as month,
    
    avg(
      case 
        when sentiment_label="NEU" then 0
        when sentiment_label="NEG" then -1
        else 1
      END) as sentiment_label

  FROM `datawx.results.res_brexit_sentiment` 
  group by year,month,url --,sentiment_label
  having year is not null and month is not null
  order by year,month


---------------------------------------------------------------
--Population Report
create view referencedata.vw_PopulationReport as
  select feed, EXTRACT(year from feeddate) as year,EXTRACT(month from feeddate) as month, count(*) as totalrecords
  from referencedata.vw_Feeds
  where feeddate is not null 
  group by feed, year, month
  order by year,month asc

--Total rows by year/month from population report
--Demo: delete SQL before flight :)
--Demo, also delete view before flight :)

-- create view referencedata.vw_PopulationReportTotals as
--   select EXTRACT(year from feeddate) as year,EXTRACT(month from feeddate) as month, count(*) as totalrecords
--   from referencedata.vw_Feeds
--   where feeddate is not null 
--   group by year, month
--   order by year,month asc


--Randomly sample first 1000 rows from vw_Feeds and insert into referenceData.sRandomSample10K Table
select outerStruct.pyear,outerStruct.pmonth,
      innerStruct.*
 from

(select EXTRACT(year from feeddate) as pyear,EXTRACT(month from feeddate) as pmonth
  from referencedata.vw_Feeds
  where feeddate is not null 
  group by pyear, pmonth
  order by pyear,pmonth asc) as outerStruct

inner join 

(select EXTRACT(year from feeddate) as pyear,EXTRACT(month from feeddate) as pmonth,feed,title,blurb,url
  from referencedata.vw_Feeds
  where feeddate is not null 
  order by rand()
  limit 1000
  ) as innerStruct

on outerStruct.pyear=innerStruct.pyear and outerStruct.pmonth=innerStruct.pmonth



