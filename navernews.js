const request = require('request-promise')
const cheerio = require('cheerio');
const iconv = require('iconv-lite');

async function getlist(){
    return request({
        method: 'GET',
        url: 'https://news.naver.com',
        encoding: null
    }).then(async (body) => {
        const $ = cheerio.load(iconv.decode(body, 'EUC-KR'));
        var news_list = [];
        $('#today_main_news').find('div > a', '.newsnow_tx_inner').each(function (index, element) {
            const href = $(element).attr('href');
            if (href.includes('read.nhn'))
                news_list.push({
                    'head': $(element).text().replace('동영상기사', '').trim(),
                    'src': $(element).attr('href')
                });
        });
        return news_list;
    })
}

async function getcontent(url){
    // console.log('[*] URL:', url)
    return request({
        method: 'GET',
        url: url,
        encoding: null
    }).then(async (body) => {
        const $ = cheerio.load(iconv.decode(body, 'EUC-KR'));
        return {
            'title': $('#articleTitle').text(),
            'src': url,
            'date-written': '',
            'date-modified': '', // date parsing in progress
            'content': $('#articleBodyContents').text().trim()
        }
    })
}

getlist().then(function(news){
    getcontent(news[0]['src']).then(console.log);
});
