
from selenium import webdriver
import urllib2
import time
import re
def draw_data(content):
    profile={}
    profile['influencer']='no'
    result_influencer=re.findall((">Influencer<"),content)
    if len(result_influencer) ==1:
        print 'yes'
        profile['influencer']='yes'
    #基本资料
    profile['fullname']='no'
    result_fullname=re.findall("class=\"full-name\">([^<]+)<",content)
    if len(result_fullname)==1:
        print result_fullname[0]
        profile['fullname']=result_fullname[0]
    #职位
    profile['current']='no'
    result_title=re.findall("class=\"title\">([^<]+)<",content)
    if len(result_title)==1:
        print result_title[0]
        profile['current']=result_title
    #地理位置
    profile['location']='no'
    result_location=re.findall("(<span class=\"locality\">.*?</span>)",content)
    if len(result_location)==1:
        dr=re.compile(r'<[^>]+>',re.S)
        dd=dr.sub('',result_location[0])
        if dd:
            print dd
            profile['location']=dd
    #工业界
    profile['industry']='no'
    result_industry=re.findall("(<dd class=\"industry\">.*?</dd>)",content)
    if len(result_industry)==1:
        dr=re.compile(r'<[^>]+>',re.S)
        dd=dr.sub('',result_industry[0])
        if dd:
            print dd
            profile['industry']=dd

    #粉丝数
    profile['follower']='0'
    result_follower=re.findall("follower-count\"><strong>([^<]+)</strong>",content)
    if result_follower:
        print result_follower[0]
        profile['follower']=result_follower[0]

    #Posts
    profile['posts']=[]
    result_post_title=re.findall("trk=prof-post\">([^<]+)</a>",content)
    for i in range(len(result_post_title)):
        profile['posts'].append({})
    if result_post_title:
        for each in result_post_title :
            print each,
            profile['posts'][result_post_title.index(each)]['title']=each

    result_post_time=re.findall("post-published\">([^<]+)</span>",content)
    if result_post_time:
        for each in result_post_time:
            print each,
            profile['posts'][result_post_time.index(each)]['time']=each

    #Background
    profile['summary']='no'
    result_summary=re.findall("<p dir=\"...\" class=\"description\">(.*?)<br",content)
    if result_summary:
        print result_summary[0]
        profile['summary']=result_summary[0]

    #Experience
    profile['experiences']=[]
    result_pre_title=re.findall("trk=mprofile_title\">([^<]+)</a>",content)
    for i in range(len(result_pre_title)):
        profile['experiences'].append({})
    if result_pre_title:
        for each in result_pre_title:
            print each,
            profile['experiences'][result_pre_title.index(each)]['title']=each

    result_pre_company=re.findall("trk=prof-exp-company-name\">([^<]+)</a>",content)
    if result_pre_company:
        for each in result_pre_company:
            print each,
            profile['experiences'][result_pre_company.index(each)]['company']=each

    result_pre_time=re.findall("<span class=\"experience-date-locale\"><time>([^<]*)</time>([^<]*)</span>",content)
    if result_pre_time:
        for each in result_pre_time:
            print each[0],each[1],
            profile['experiences'][result_pre_time.index(each)]['time']=each[0]+'-'+each[1].strip(' – ')

    #Language
    profile['lanuages']=['no']
    result_language=re.findall("<li class=\"section-item\"><h4><span dir=\"auto\">([^<]*)</span>",content)
    if result_language:
        profile['lanuages'].remove('no')
        for each in result_language:
            print each,
            profile['lanuages'].append(each)

    #Skills
    profile['skills']=['no']
    result_skill=re.findall("trk=mprofile_topic\">([^<]*)</a>",content)
    if result_skill:
        profile['skills'].remove('no')
        for each in result_skill:
            print each,
            profile['skills'].append(each)

    #Education
    profile['education']=['no']
    result_education_school=re.findall("trk=prof-edu-school-name\">([^<]+)</a>",content)
    if result_education_school:
        profile['education'].remove('no')
        for k in range(len(result_education_school)):
            profile['education'].append({})

        if result_education_school:
            for each in result_education_school:
                print each.strip(' – '),
                profile['education'][result_education_school.index(each)]['school']=each
        result_education_major=re.findall("trk=prof-edu-field_of_study\">([^<]+)</a>",content)
        if result_education_major:
            for each in result_education_major:
                print each,
                profile['education'][result_education_major.index(each)]['major']=each
        result_education_time=re.findall("class=\"education-date\"><time>([^<]*)</time><time>([^<]*)</time>",content)
        if result_education_time:
            for each in result_education_time:
                print each[0],each[1],
                profile['education'][result_education_time.index(each)]['time']=each[0]+'-'+each[1].strip(' – ')

    #Following
    profile['following']=['no']
    cc=re.findall("(<h2>Following</h2>)",content)
    if cc:
        profile['following'].remove('no')
        profile['following']={}
        #News
        result_news_title=re.findall("trk=prof-following-chan-icon\">([^<]+)</a>",content)
        if result_news_title:
            profile['following']['news']=[]
            for each in range(len(result_news_title)):
                profile['following']['news'].append({})
            for each in result_news_title:
                profile['following']['news'][result_news_title.index(each)]['title']=each
                print each,

        result_news_followers=re.findall("class=\"following.stats\">([^<]*)</p>",content)
        if result_news_followers:
            for each in result_news_followers:
                print each,
                profile['following']['news'][result_news_followers.index(each)]['followers']=each


        #Companies
        result_companies_title=re.findall("<strong dir=\"auto\">([^<]+)</strong></a></p><p class=\"following-field\">([^<]+)</p>",content)
        if result_companies_title:
            profile['following']['companies']=[]
            for each in range(len(result_companies_title)):
                profile['following']['companies'].append({})
            for each in result_companies_title:
                profile['following']['companies'][result_companies_title.index(each)]['title']=each[0]
                profile['following']['companies'][result_companies_title.index(each)]['industry']=each[1]
                print each[0],each[1],

        #Schools
        result_school_title=re.findall("<strong dir=\"auto\">([^<]+)</strong></a></p><p dir=\"auto\" class=\"following-field\">([^<]+)</p>",content)
        if result_school_title:
            profile['following']['schools']=[]
            for each in range(len(result_school_title)):
                profile['following']['schools'].append({})
            for each in result_school_title:
                profile['following']['schools'][result_school_title.index(each)]['title']=each[0]
                profile['following']['schools'][result_school_title.index(each)]['location']=each[1]
                print each[0],each[1],



    total_data=json.dumps(profile,indent=4)
    fff=open('./data/'+profile['fullname']+'.txt','w')
    fff.write(total_data)
    fff.close()
    other_person_profile_url=re.findall("<a href=\"(http://www.linkedin.com/profile/view.id=[^;]*?;authType[^\"]+)\">",content)
    if other_person_profile_url:
        return other_person_profile_url
    else :
        return []

def zhuyao():
    driver=webdriver.Firefox()
    driver.get('https://www.linkedin.com/uas/login?fromSignIn=true&trk=uno-reg-guest-home')
    print driver.title
    driver.find_element_by_name("session_key").send_keys("user-account")
    driver.find_element_by_name("session_password").send_keys("user-password")
    driver.find_element_by_name("signin").click()
    time.sleep(3)
    driver.get('http://www.linkedin.com/vsearch/f?type=people&keywords=facebook')
    #driver.find_element_by_name("trkInfo").send_keys("facebook")
    #driver.find_element_by_name("search").click()
    time.sleep(3)
    #driver.get('http://www.linkedin.com/vsearch/p?type=people&keywords=facebook&page_num=3')
    #result=driver.find_text_link("About").text
    #print results
    aa=driver.page_source.encode('utf-8')
    f=open("./result.txt",'w')
    f.write(aa)
    f.close()

    result=re.findall("<li data-li-position=\".*?people\"><a href=\"([^\"]*)\".*?</li>",aa)
    for each in result:
        print result.index(each)
        driver.get(each)
        time.sleep(5)
        bb=driver.page_source.encode('utf-8')
        ff=open('./raw_data/'+str(result.index(each))+'.txt','w')
        ff.write(bb)
        ff.close()
        new_result=draw_data(bb)
        for each_new in new_result:
            if each_new not in result:
                result.append(each_new)
   
if __name__=="__main__":
    zhuyao()

