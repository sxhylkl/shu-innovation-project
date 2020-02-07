from includes import *
import saving
def safe_get(index,priceDict):
    try:
        return priceDict[index]
    except:
        return ''
def get_details(html):
    allItems = html('div.item-bg>div').items()
    dictList=[]
    urlLists=[]
    url='https://ds.suning.com/ds/generalForTile/'
    count=0
    for item in allItems:
        link = item('div > div.res-img > div.img-block>a').attr('href')
        count+=1
        if link==None:
            continue
        link = 'https:' + link
        title=item('div.title-selling-point').text()
        Info=item('div.res-info > div.price-box > span')
        datasku=Info.attr('datasku')
        brand_id=Info.attr('brand_id')
        threegroup_id=Info.attr('threegroup_id')
        dataStr=''
        for k in range(len(datasku)):
            if datasku[k]!='|':
                dataStr+=datasku[k]
            else:
                break
        length=18-len(dataStr)
        for i in range(length):
            dataStr='0'+dataStr
        finId = link.split('/')[3]
        if count%5==0:
            url = url + dataStr + '__2_' +finId+'_'+ threegroup_id + '_' + brand_id + '-010-2-' + str(
                finId) + '-1--ds0000000003206.jsonp?callback=ds0000000003206'
            urlLists.append(url)
            url='https://ds.suning.com/ds/generalForTile/'
        else:
            url=url+dataStr+'__2_'+finId+'_'+threegroup_id+'_'+brand_id+','
        commitNum=item('div.res-info > div.evaluate-old.clearfix > div>a').text()
        shop=item('div.res-info > div.store-stock > a').text()
        dict={
            'link':link,
            'title':title,
            #'price':price,
            'commitNum':commitNum,
            'shop':shop,
            #'tags':tags
        }
        dictList.append(dict)
    count=0
    for i in range(len(urlLists)):
        response = requests.get(urlLists[i])
        text = response.text
        jsonText = text.replace('ds0000000003206(', '').replace(');', '')
        jsonText = json.loads(jsonText)
        rs = safe_get('rs', jsonText)
        for i in range(len(rs)):
            temp = safe_get(i, rs)
            price = safe_get('price', temp)
            if price != '':
                price += '元'
            tags = temp['promotionLable']
            Info = temp['promotionList']
            for key in Info:
                tags += ' ' + key['simple']
            dictList[count]['price']=price
            dictList[count]['tags']=tags
            count+=1
    return dictList
def get_page(page,keyword,id):
    totalList=[]
    for paging in range(4):
        param={
            'keyword':quote(keyword),
            'ci':'0',
            'pg':'01',
            'cp':str(page-1),
            'li':'0',
            'st':'0',
            'iy':'0',
            'adNumber':'2',
            'isNoResult':'0',
            'n':'1',
            'sesab':'ACAABAABCAAA',
            'id':'IDENTIFYING',
            'cc':'010',
            'paging':str(paging),
            'sub':'1',
            'jzq':str(id)
        }
        url='https://search.suning.com/emall/searchV1Product.do?'
        for k in param:
            if k!='jzq':
                url+=k+'='+param[k]+'&'
            else:
                url += k + '=' + param[k]
        response=requests.get(url)
        html=pq(response.text)
        tempList=get_details(html)
        for item in tempList:
            totalList.append(item)
    return totalList
def get_all(keyword):
    totalDict = {}
    totalDict['name'] = 'suning'
    totalDict['keyword'] = keyword
    totalDict['pages'] = 50
    totalList=[]
    response = requests.get('https://search.suning.com/' + quote(keyword) + '/')
    id = re.compile('\n"categoryId": (.*),').findall(response.text)[0]
    for i in range(1,51):
        lists=get_page(i, keyword,id)
        for item in lists:
            totalList.append(item)
    totalDict['data']=totalList
    return totalDict
def run(keyword,page):
    totalDict={}
    totalDict['name']='suning'
    totalDict['keyword']=keyword
    totalDict['pages']=50
    response = requests.get('https://search.suning.com/'+quote(keyword)+'/')
    html=pq(response.text)
    id=html('#totalCount').attr('value')
    totalDict['data']=get_page(page,keyword,id)
    jsonText=json.dumps(totalDict,ensure_ascii=False)
    return jsonText
