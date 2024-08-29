window.searchIndex = {"fields":["title","body"],"pipeline":["trimmer-ja","stemmer-ja"],"ref":"id","version":"0.9.5","index":{"body":{"root":{"docs":{},"df":0,"パ":{"docs":{},"df":0,"フ":{"docs":{},"df":0,"ォ":{"docs":{},"df":0,"ー":{"docs":{},"df":0,"マ":{"docs":{},"df":0,"ン":{"docs":{},"df":0,"ス":{"docs":{"https://jbcurtin.io/ja/articles/":{"tf":1.0}},"df":1}}}}}}},"分":{"docs":{},"df":0,"析":{"docs":{"https://jbcurtin.io/ja/articles/":{"tf":1.0}},"df":1}},"日":{"docs":{},"df":0,"本":{"docs":{},"df":0,"語":{"docs":{"https://jbcurtin.io/ja/search/":{"tf":1.0}},"df":1}}}}},"title":{"root":{"docs":{},"df":0,"パ":{"docs":{},"df":0,"フ":{"docs":{},"df":0,"ォ":{"docs":{},"df":0,"ー":{"docs":{},"df":0,"マ":{"docs":{},"df":0,"ン":{"docs":{},"df":0,"ス":{"docs":{"https://jbcurtin.io/ja/articles/":{"tf":1.0}},"df":1}}}}}}},"分":{"docs":{},"df":0,"析":{"docs":{"https://jbcurtin.io/ja/articles/":{"tf":1.0}},"df":1}},"日":{"docs":{},"df":0,"本":{"docs":{},"df":0,"語":{"docs":{"https://jbcurtin.io/ja/search/":{"tf":1.0}},"df":1}}}}}},"documentStore":{"save":true,"docs":{"https://jbcurtin.io/ja/":{"body":"","id":"https://jbcurtin.io/ja/","title":""},"https://jbcurtin.io/ja/articles/":{"body":"","id":"https://jbcurtin.io/ja/articles/","title":"パフォーマンス分析"},"https://jbcurtin.io/ja/articles/postgresql-compression-benchmark/":{"body":"By far, my favorite RDBMS is PostgreSQL. Having worked with MySQL, MSSQL, Cassandra, Redis and more; the versatility of PostgreSQL continues to inspire me to write better and more complex SQL. I have a piece of software that reaches out to various news websites following best practices for crawling. Scraping content using provided by the sitemap.xml and following the rules set forth by the robots.txt file. The content of these sites can be anything, but the general approach is to collect as much news as possible to see if I can develop a series of heuristics to provide as technical indicators.\nI've been running the software for about two years now, and a massize PostgreSQL table has been created from the result of it. Today, I'd like to start making regular backups of the data in the table. This article will focus on benchmarking how long it'll take to backup a table using the pg_dump program &amp; Docker.\nStanding on the shoulders of giants, I've found a comprehensive review of algorithms used for compression. I'm not concerned with parallel processing; I'll stick to evaluating the programs as provided. What I'm looking to glean is a definitive and consistent measurement of how long it'll take to export and compress information for the massive PostgreSQL table.\nBenchmark Setup\nBenchmark setup is fairly straightforward. A table called location tracks various metrics about URLs such as crawl_delay, domain of the URL, change_ferq, and lastmod. Properties provided by a sites' sitemap.xml. Which in turn allows for the development of an algrothim to select more relivent pages, yet still allow the crawler to search for archived content while not overburdening the website. The location table will be used to identify the best compression algorithm benchmark for the much larger table\n\nThe database is ran using docker, specifically the postgis:15-3.3-alpine image. Port 5432 is exposed to the host, but we won't use it because it seems that connecting to a port exposed to the host will route traffic through the LAN. Instead we'll export data in the container and compress the output from the exec command to a filepath on the host.\nHow the database has been initalized using Docker\n\nThe compression algorithms to be tested are zstd, gzip, bzip2, lz4, and xz.\nHere is the full script to run the benchmark\n\nBenchmark Results\n\nA core trade off when selecting an optimal compression algorithm is the amount of time taken; relative to the ratio of the file before compression size over after compression size.\n$$ Compression Ratio = {Uncompressed Size\\over{Compressed Size}} $$\nUndersatnding the Benchmark Results\nI'm more interested in the backup running quickly and am willing to accept slightly larger archived files. bzip2 and xz both provided the smallest filesize, but the time to archive took well over twenty minutes for each. ztsd took about a minute and a half, and provided a slightly larger file at 1.6GB in size\nData Stream\nI'm not archiving files. I'm archiving a stream coming from a docker exec command and that has additional overhead to consider. Rather than understanding the overhead, lets produce a metric for how many MB/s of information is being transmitted from the docker exec command. How much data is being piped into the various compression algorithms?\nExporting the same stream to dd for about a minute will tell us enough about how much data is being sent to the various compression algorithms\n\nKnowing an average of 98.4 MB/s is beind transmitted, we now have enough information to estimate the compression ratio of each archive.\n$$ Seconds \\times \\text{Average MB/s} \\over {Compressed Size} $$\nAlgorithmMathRatio\nzstd$$ 88 \\times 98.4 \\over {1.6} $$5412.0\ngzip$$ 200 \\times 200 \\over {1.7} $$11576.471\nbzip2$$ 1144 \\times 98.4 \\over {1.3} $$86592.0\nlz4$$ 88 \\times 98.4 \\over {2.5} $$3463.680\nxz$$ 2262 \\times 98.4 \\over {1.3} $$201492.923\n\nCompression Ratios can vary based on a multitude of factors, most notibly is the amount of repeated information in the file being archived. For instance, text data often repeats while random data does not. Therefore we'll be able to achieve higher compression ratios on archives with text data (such as a PostgreSQL dump).\nArticle References\n\nhttps://www.rootusers.com/gzip-vs-bzip2-vs-xz-performance-comparison/\nhttps://linuxreviews.org/Comparison_of_Compression_Algorithms\nhttps://en.wikipedia.org/wiki/Data_compression_ratio#Definition\n\n","id":"https://jbcurtin.io/ja/articles/postgresql-compression-benchmark/","title":"Compression Benchmarks for PostgreSQL Archives"},"https://jbcurtin.io/ja/search/":{"body":"","id":"https://jbcurtin.io/ja/search/","title":"Article Search 日本語"}},"docInfo":{"https://jbcurtin.io/ja/":{"body":0,"title":0},"https://jbcurtin.io/ja/articles/":{"body":0,"title":2},"https://jbcurtin.io/ja/articles/postgresql-compression-benchmark/":{"body":0,"title":0},"https://jbcurtin.io/ja/search/":{"body":0,"title":1}},"length":4},"lang":"Japanese"}